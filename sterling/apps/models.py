from annoying.fields import AutoOneToOneField
import datetime

from django.conf import settings
from django.db import models

# from fbNodes.models import InvitationNode, FbNode

class MobileApp(models.Model):
    ''' Represents an app that is signed up for the platform '''
    facebook_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='DevMembership') # App admins
    invitation_message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def num_users(self, datetime=datetime.datetime.now()):
        ''' Returns number of users signed up for the app
        Optional datetime parameter that gets number of users before that datetime.
        '''
        return FbNode.objects.filter(apps=self, created__lt=datetime).count()


    def num_invited(self, datetime=datetime.datetime.now()):
        ''' Returns number of people invited to the app
        Optional datetime parameter that gets number of users invited before that datetime. 
        '''
        return InvitationNode.objects.filter(app=self, 
                                            created__lt=datetime,
                                            ).count()
    def num_invitations_clicked(self, datetime=datetime.datetime.now()):
        ''' Returns number of invitations that were clicked, with optional datetime parameter '''
        return InvitationNode.objects.filter(app=self, 
                                            link_clicked=True,
                                            created__lt=datetime).count()

    def num_invitations_joined(self, datetime=datetime.datetime.now()):
        ''' Returns number of invitations that resulted in app signups '''
        return InvitationNode.objects.filter(app=self,
                                            joined=True,
                                            created__lt=datetime).count()

    # def average_number_of_invites_per_user(self, datetime=datetime.datetime.now()):
    #     '''  '''


class DevMembership(models.Model):
    ''' 'Through' model for app signups. '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    mobile_app = models.ForeignKey(MobileApp)
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)







    


