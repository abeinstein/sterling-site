from django.test import TestCase
from django.contrib.auth.models import User

from apps.models import MobileApp, DevMembership

class AppTests(TestCase):

    def setUp(self):
        self.app = MobileApp.objects.create(name="Rush: Go Greek", facebook_id="12345678")
        self.user = User.objects.create_user('abeinstein', 'andrew.beinstein@gmail.com', 'andrewpassword')
        
        self.mem = DevMembership(user=self.user, mobile_app=self.app, is_admin=False) 
        self.mem.save()       

    def test_user_is_member(self):
        self.assertQuerysetEqual(self.app.users.all(), [repr(self.user)]) # This is pretty hacky






