from django.db import models


# Create your models here.
class AppUser(models.Model):
    ''' Represents anyone who is signed up for an app, or is Facebook friends with 
    someone signed up for an app
    '''
    facebook_id = models.PositiveIntegerField()
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True,  null=True)
    
    # TODO: Should this be moved to the apps model? Probably...
    mobile_apps = models.ManyToManyField('apps.MobileApp', through='AppUserMembership')

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def create_friends(self, graph=None):
        ''' Make AppUser's for self's friends '''
        return NotImplemented

    def get_name(self, graph=None):
        ''' Returns the tuple (first_name, last_name) from Facebook data'''
        return NotImplemented

    def save(self, *args, **kwargs):
        return super(AppUser, self).save(args, kwargs)




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


class Algorithm(models.Model):
    ''' Represents an algorithm used to sort a list of users '''
    name = models.CharField(max_length=200)
    number_times_used = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class SuggestionList(models.Model):
    ''' Represents a list of suggestions. This is also a 'through' model betweeen 
    AppUserMembership and Algorithm 
    '''
    app_user_membership = models.ForeignKey(AppUserMembership)
    algorithm = models.ForeignKey(Algorithm)
    suggested_friends = models.ManyToManyField(AppUser, through='Suggestion')
    created = models.DateTimeField(auto_now_add=True)

    presented_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "%s suggestions for %s" % (self.algorithm, self.app_user_membership) 

    def save(self, *args, **kwargs):
        if not self.suggested_friends:
            # Create Suggestion models using self.algorithm
            pass
        return super(SuggestionList, self).save(args, kwargs)



class Suggestion(models.Model):
    ''' Represents a suggestion from one AppUser to another. A 'through' model
    between SuggestionList and AppUser
    '''
    suggestion_list = models.ForeignKey(SuggestionList)
    app_user = models.ForeignKey(AppUser) # A FB friend of suggestion_list.app_user_membership.app_user

    rank = models.PositiveIntegerField()

    presented = models.BooleanField(default=False) # Was this suggestion presented to the user?
    invited = models.BooleanField(default=False) # Did the suggester actually invite?
    accepted = models.BooleanField(default=False) # Did the invited actually accept?

    first_presentation_date = models.DateTimeField(blank=True, null=True)
    last_presentation_date = models.DateTimeField(blank=True, null=True)
    invited_date = models.DateTimeField(blank=True, null=True)
    accepted_date = models.DateTimeField(blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)




