from annoying.fields import AutoOneToOneField

from django.conf import settings
from django.db import models

class MobileApp(models.Model):
    ''' Represents an app that is signed up for the platform '''
    facebook_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership')
    invitation_message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    ''' 'Through' model for app signups. '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    mobile_app = models.ForeignKey(MobileApp)
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)







    


