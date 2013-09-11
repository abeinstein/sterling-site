from django.conf import settings
from django.db import models

class App(models.Model):
    ''' Represents an app that is signed up for the platform '''
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership')

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    ''' 'Through' model for app signups. '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    app = models.ForeignKey(App)
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)







    

