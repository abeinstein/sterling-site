import facebook
import datetime

from celery import task

from django.db import models
from django.db.models import get_model
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from suggestions.algorithms.algorithms import alphabetical
from algorithms.algorithms import toy_algorithm, alphabetical, splash_site, mutual_friends, weighted_mutual_friends, photos, feed

# ALGORITHM IDS
ALGORITHM_ALPHABETICAL = 2
ALGORITHM_MUTUAL_FRIENDS = 4
ALGORITHM_WEIGHTED_MUTUAL_FRIENDS = 5
ALGORITHM_PHOTOS = 6
ALGORITHM_FEED = 7

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
        try:
            friends = graph.get_connections("me", "friends")
        except facebook.GraphAPIError:
            token = graph.extend_access_token(settings.STERLING_FACEBOOK_APP_ID,
                                    settings.STERLING_FACEBOOK_APP_SECRET)['access_token']
            graph.access_token = token
            friends = graph.get_connections("me", "friends")

        # TODO: Worry about paging
        # TODO: Bulk update?
        friendships = []
        new_friends = []

        for f in friends['data']:
            try:
                app_user = AppUser.objects.get(facebook_id=f['id'])
                friendships.append(app_user)
            except ObjectDoesNotExist:
                app_user = AppUser(facebook_id = f['id'], name=f['name'])
                new_friends.append(app_user)

        AppUser.objects.bulk_create(new_friends)

        for app_user in new_friends:
            friendships.append(AppUser.objects.get(facebook_id=app_user.facebook_id))

        self.friends.add(*friendships)

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
            #ALGORITHM_TOY: toy_algorithm,
            ALGORITHM_ALPHABETICAL: alphabetical,
            #ALGORITHM_SPLASH: splash_site,
            ALGORITHM_MUTUAL_FRIENDS: mutual_friends,
            ALGORITHM_WEIGHTED_MUTUAL_FRIENDS: weighted_mutual_friends,
            ALGORITHM_PHOTOS: photos,
            ALGORITHM_FEED: feed,

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

    def generate_suggestions(self):
        ''' Takes an AppUserMembership and calls an external function to 
        generate Suggestion objects '''
        # Call external function to actually run the algorithm
        facebook_id = self.app_user_membership.app_user.facebook_id
        oauth_token = self.app_user_membership.oauth_token

        # This is where the magic happens
        ordered_facebook_ids = self.algorithm.algorithm(facebook_id, oauth_token)
        suggestions = []
        
        for rank, friend_id in enumerate(ordered_facebook_ids):
            # TODO: get_or_create? What happens when their friend list has changed?
            try:
                app_user = AppUser.objects.get(facebook_id=friend_id)
            except AppUser.DoesNotExist:
                return Exception("Appuser does not exist" + str(friend_id))

            suggestion = Suggestion(
                    suggestion_list=self,
                    app_user=app_user,
                    rank=rank
            )
            suggestions.append(suggestion)

        Suggestion.objects.bulk_create(suggestions)



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

    clicked = models.BooleanField(default=False) # Did the user click the link?
    clicked_date = models.DateTimeField(blank=True, null=True)

    accepted = models.BooleanField(default=False) # Did the invited actually accept?
    accepted_date = models.DateTimeField(blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank']
        unique_together = ('suggestion_list', 'app_user')

    @property
    def link(self):
        return "http://sterling.herokuapp.com/invitations/?suggestion=%s" % self.id
