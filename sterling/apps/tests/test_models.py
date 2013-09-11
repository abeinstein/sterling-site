from django.test import TestCase
from django.contrib.auth.models import User

from apps.models import App, Membership

class AppTests(TestCase):

    def setUp(self):
        self.app = App.objects.create(name="Rush: Go Greek")
        self.user = User.objects.create_user('abeinstein', 'andrew.beinstein@gmail.com', 'andrewpassword')
        
        self.mem = Membership(user=self.user, app=self.app, is_admin=False) 
        self.mem.save()       

    def test_user_is_member(self):
        self.assertQuerysetEqual(self.app.users.all(), [repr(self.user)]) # This is pretty hacky






