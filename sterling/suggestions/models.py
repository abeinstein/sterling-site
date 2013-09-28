from django.db import models

from apps.models import MobileApp

# Create your models here.
class AppUser(models.Model):
    ''' Represents anyone who is signed up for an app, or is Facebook friends with 
    someone signed up for an app
    '''
    facebook_id = models.PositiveIntegerField()
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True,  null=True)
    mobile_apps = models.ManyToManyField(MobileApp, through='AppUserMembership')
    created = models.DateTimeField(auto_now_add=True)

class AppUserMembership(models.Model):
    ''' Through model between AppUser and MobileApp '''
    app_user = models.ForeignKey(AppUser)
    mobile_app = models.ForeignKey(MobileApp)
    oauth_token = models.TextField()
    algorithms = models.ManyToManyField('Algorithm', through='SuggestionList')
    created = models.DateTimeField(auto_now_add=True)


class Algorithm(models.Model):
    ''' Represents an algorithm used to sort a list of users '''
    name = models.CharField(max_length=200)
    number_times_used = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

class SuggestionList(models.Model):
    ''' Represents a list of suggestions. This is also a 'through' model betweeen 
    AppUserMembership and Algorithm 
    '''
    app_user_membership = models.ForeignKey(AppUserMembership)
    algorithm = models.ForeignKey(Algorithm)
    suggested_friends = models.ManyToManyField(AppUser, through='Suggestion')
    created = models.DateTimeField(auto_now_add=True)

class Suggestion(models.Model):
    ''' Represents a suggestion from one AppUser to another. A 'through' model
    between SuggestionList and AppUser
    '''
    suggestion_list = models.ForeignKey(SuggestionList)
    app_user = models.ForeignKey(AppUser)

    rank = models.PositiveIntegerField()
    invited = models.BooleanField(default=False) # Did the suggester actually invite?
    accepted = models.BooleanField(default=False) # Did the invited actually accept?
    created = models.DateTimeField(auto_now_add=True)




