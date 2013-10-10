from annoying.fields import AutoOneToOneField
import datetime

from django.conf import settings
from django.db import models

from suggestions.models import AppUser, AppUserMembership, Suggestion, Algorithm

class MobileApp(models.Model):
    ''' Represents an app that is signed up for the platform '''
    facebook_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='DevMembership') # App admins
    invitation_message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    # TODO: Point to actual default algorithm
    default_algorithm = models.ForeignKey(Algorithm, blank=True, null=True)

    def __unicode__(self):
        return self.name

    # def algorithms_used(self):
    #     return Algorithm.objects.filter()

    def num_users(self, datetime=datetime.datetime.now()):
        ''' Returns number of users signed up for the app
        Optional datetime parameter that gets number of users before that datetime.
        '''
        return AppUserMembership.objects.filter(mobile_app=self, created__lt=datetime).count()

    # TODO: Investigate these queries to see if they're fast (they're probably not)
    # def num_suggested(self, datetime=datetime.datetime.now()):
    #     ''' Returns number of invitations that were clicked, with optional datetime parameter '''
    #     return Suggestion.objects.filter(suggestion_list__app_user_membership__mobile_app=self,
    #                                     created__lt=datetime).count()

    def num_invited(self, datetime=datetime.datetime.now()):
        ''' Returns number of people invited to the app
        Optional datetime parameter that gets number of users invited before that datetime. 
        '''
        return Suggestion.objects.filter(suggestion_list__app_user_membership__mobile_app=self,
                                         times_invited__gt=0,
                                         created__lt=datetime).count()



    def num_invitations_joined(self, datetime=datetime.datetime.now()):
        ''' Returns number of invitations that resulted in app signups '''
        return Suggestion.objects.filter(suggestion_list__app_user_membership__mobile_app=self,
                                            accepted=True,
                                            created__lt=datetime).count()



class DevMembership(models.Model):
    ''' 'Through' model for app signups. '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    mobile_app = models.ForeignKey(MobileApp)
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)







    


