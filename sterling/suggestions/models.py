import facebook
import datetime
from django.db import models
from django.db.models import get_model
from suggestions.algorithms.algorithms import alphabetical
from celery import task
from algorithms.algorithms import *
from django.core.exceptions import ObjectDoesNotExist

# ALGORITHM IDS
ALGORITHM_TOY = 1
ALGORITHM_ALPHABETICAL = 2

class AppUser(models.Model):
    ''' Represents anyone who is signed up for an app, or is Facebook friends with 
    someone signed up for an app
    '''
    facebook_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    friends = models.ManyToManyField("self")
    mobile_apps = models.ManyToManyField('apps.MobileApp', through='AppUserMembership')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.facebook_id

    def update_friends(self):
        ''' Make AppUser's for self's friends if they don't already exist'''
        # First, grab friends from Facebook
        graph = facebook.GraphAPI(self.get_oauth_token())
        friends = graph.get_connections("me", "friends")
        # TODO: Worry about paging
        # TODO: Bulk update?

        new_app_user_friends = []

        print "adding old friend relations: " + str(datetime.datetime.now())
        for f in friends['data']:
            try:
                app_user = AppUser.objects.get(facebook_id=f['id'])
                self.friends.add(AppUser.objects.get(facebook_id=app_user.facebook_id))
            except ObjectDoesNotExist:
                app_user = AppUser(facebook_id = f['id'])
                new_app_user_friends.append(app_user)

        print "calling bulk create: " + str(datetime.datetime.now())
        AppUser.objects.bulk_create(new_app_user_friends)

        print "adding new friend relationships: " + str(datetime.datetime.now())
        for app_user in new_app_user_friends:
            self.friends.add(AppUser.objects.get(facebook_id=app_user.facebook_id))
        print "done with update friends: " + str(datetime.datetime.now())



    def get_name(self, graph=None):
        ''' Returns the tuple (first_name, last_name) from Facebook data'''
        return NotImplemented

    # TODO: Only getting first mobile app will create problems!!
    def get_oauth_token(self, mobile_app=None):
        if not mobile_app:
            mobile_app = self.mobile_apps.all()[0] # Get first one
        app_user_membership = AppUserMembership.objects.get(app_user=self, mobile_app=mobile_app)
        return app_user_membership.oauth_token


class AppUserMembership(models.Model):
    ''' Through model between AppUser and MobileApp 
    Only created when a user actually signs up for an app
    '''
    app_user = models.ForeignKey(AppUser)
    mobile_app = models.ForeignKey('apps.MobileApp')
    oauth_token = models.TextField()
    algorithms = models.ManyToManyField('Algorithm', through='SuggestionList')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.mobile_app, self.app_user)

    class Meta:
        unique_together = ('app_user', 'mobile_app')

class Algorithm(models.Model):
    ''' Represents an algorithm used to sort a list of users '''
    name = models.CharField(max_length=200)
    number_times_used = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    algorithm_method_id = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name

    @property
    def algorithm(self):
        algorithm_dict = {
            ALGORITHM_TOY: toy_algorithm,
            ALGORITHM_ALPHABETICAL: alphabetical
        }
        return algorithm_dict[self.algorithm_method_id]



class SuggestionList(models.Model):
    ''' Represents a list of suggestions. This is also a 'through' model betweeen 
    AppUserMembership and Algorithm 
    '''
    app_user_membership = models.ForeignKey(AppUserMembership)
    algorithm = models.ForeignKey(Algorithm)
    suggested_friends = models.ManyToManyField(AppUser, through='Suggestion')
    created = models.DateTimeField(auto_now_add=True)

    presented_count = models.PositiveIntegerField(default=0)

    # def __unicode__(self):
    #     return "%s suggestions for %s" % (self.algorithm, self.app_user_membership) 

    class Meta:
        unique_together = ('app_user_membership', 'algorithm')

    #@task()
    def generate_suggestions(self):
        ''' Takes an AppUserMembership and calls an external function to 
        generate Suggestion objects '''
        # Call external function to actually run the algorithm
        facebook_id = self.app_user_membership.app_user.facebook_id
        oauth_token = self.app_user_membership.oauth_token
        
        # This is where the magic happens
        ordered_facebook_ids = self.algorithm.algorithm(facebook_id, oauth_token)
        
        for rank, friend_id in enumerate(ordered_facebook_ids):
            # TODO: get_or_create? What happens when their friend list has changed?
            try:
                app_user = AppUser.objects.get(facebook_id=friend_id)
            except AppUser.DoesNotExist:
                return Exception("Appuser does not exist")

            Suggestion.objects.create(
                    suggestion_list=self,
                    app_user=app_user,
                    rank=rank
            )


class Suggestion(models.Model):
    ''' Represents a suggestion from one AppUser to another. A 'through' model
    between SuggestionList and AppUser
    '''
    suggestion_list = models.ForeignKey(SuggestionList)
    app_user = models.ForeignKey(AppUser) # A FB friend of suggestion_list.app_user_membership.app_user

    rank = models.PositiveIntegerField()

    times_presented = models.PositiveIntegerField(default=0) # How many times was this suggestion presented to the user?
    last_presented_date = models.DateTimeField(blank=True, null=True)

    times_invited = models.PositiveIntegerField(default=0) # How many times was this user invited?
    last_invited_date = models.DateTimeField(blank=True, null=True)   

    accepted = models.BooleanField(default=False) # Did the invited actually accept?
    accepted_date = models.DateTimeField(blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank']
        unique_together = ('suggestion_list', 'app_user')