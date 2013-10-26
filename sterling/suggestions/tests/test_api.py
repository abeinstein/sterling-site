import time

from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status
from django_rq import get_worker

from apps.models import MobileApp 
from suggestions.models import AppUser, Algorithm, AppUserMembership, SuggestionList, \
    Suggestion, ALGORITHM_ALPHABETICAL


user_name = 'Mike Amfhbegehage Smithsen'
user_facebook_id = '100006825758175'

class SuggestionsAPITests(APITestCase):
    def setUp(self):
        self.algorithm = Algorithm.objects.create(
            name="Alphabetical",
            algorithm_method_id=ALGORITHM_ALPHABETICAL
        )

        self.mobile_app = MobileApp.objects.create(
            facebook_id=settings.STERLING_FACEBOOK_APP_ID,
            name="Rush: Go Greek",
            invitation_message="Be the top frat on campus!",
            default_algorithm=self.algorithm,
            link="http://itunes.com/apps/AdamGluck/Rush:GoGreek"
        )

        self.appUser = AppUser.objects.create(
            facebook_id="100006845670988",
            name="Margaret Amfhdefgjihh Shepardstein"
        )

        self.appUserMembership = AppUserMembership.objects.create(
            app_user=self.appUser,
            mobile_app=self.mobile_app,
            oauth_token='CAAGoRPx0jlMBALIk9Wm4YLIcT6ANBak8qXuxl3GvQy4dHMyvG9rO7emjLGAsmUsTx6tllitiCIvPZC7jKoF8dyO7IxJh2mb8lviIEmOVtlBQX3euZAZAgUtweadZCIhkYgOt9BKLrBYJjucy74pZBIUdDWk05lnYd5cG8e1Y3a9FUZBYTQZAlnv'
        )

        self.appUser.update_friends()

        self.suggestionList = SuggestionList.objects.create(
            app_user_membership=self.appUserMembership,
            algorithm=self.algorithm
        )

        self.suggestionList.generate_suggestions()

    def test_create_new_app_user(self):
        data = {
            'app_facebook_id': self.mobile_app.facebook_id,
            'oauth_token': 'CAAGoRPx0jlMBADLEqXp4aYwQZAR64jTvdtNZCxTqZAlVZAGDJD99pZAjKghVvmTzNrUyFZCk15sNeYkF4sCl0ddVsGxOQFIjCBCd5oStqpjB4nzSWHzCrrZB5j1v4KkfZBIF7jIxkLIpBypXa2JOMyXkJZChf0k0UUPoFFqzxCoFT24IOZAhewCV5ZAU9eGUek77SYZD',
            'facebook_id': user_facebook_id
        }
        response = self.client.post('/appUserLogin/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        get_worker().work(burst=True) # Process all jobs, then stop

        # Test that an AppUser was actually created
        user = AppUser.objects.get(facebook_id=user_facebook_id)
        self.assertEqual(isinstance(user, AppUser), True)

        # Test that his friends were created
        user_friends_count = user.friends.all().count()
        self.assertEqual(user_friends_count, 4)


    def test_get_suggestion_list(self):
        response = self.client.get('/suggestions/?facebook_id=%s&app_facebook_id=%s' % 
            (self.appUser.facebook_id, self.mobile_app.facebook_id))
        self.assertEqual(response.status_code, 200)

        self.assertListEqual(response.data.keys(), ['friends', 'list_id'])
        
        # Check that all names exist
        names = [f['name'] for f in response.data['friends']]
        self.assertNotIn(None, names)

    def test_post_suggestion_list(self):
        all_friends = self.appUser.friends.all().values_list('facebook_id', flat=True)
        friends_seen = all_friends
        friends_invited = friends_seen[:2]

        before_times_presented = list(Suggestion.objects.filter(
            suggestion_list=self.suggestionList,
            app_user__facebook_id__in=all_friends
        ).values_list('times_presented', flat=True))
        
        before_times_invited = list(Suggestion.objects.filter(
            suggestion_list=self.suggestionList,
            app_user__facebook_id__in=friends_invited
        ).values_list('times_invited', flat=True))

        data = {
            'list_id': self.suggestionList.pk,
            'friends_seen': friends_seen,
            'friends_invited': friends_invited
        }

        response = self.client.post('/suggestions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        after_times_presented = Suggestion.objects.filter(
            suggestion_list=self.suggestionList,
            app_user__facebook_id__in=all_friends
        ).values_list('times_presented', flat=True)

        after_times_invited = list(Suggestion.objects.filter(
            suggestion_list=self.suggestionList,
            app_user__facebook_id__in=friends_invited
        ).values_list('times_invited', flat=True))

        self.assertListEqual(map(lambda x: x+1, before_times_presented), list(after_times_presented))
        self.assertListEqual(map(lambda x: x+1, before_times_invited), list(after_times_invited))

    def test_invitation_redirect(self):
        sug = Suggestion.objects.all()[0] # Get first one
        response = self.client.get('/invitations/?suggestion=%s' % sug.pk)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertEqual(response['Location'], sug.suggestion_list.app_user_membership.mobile_app.link)
        new_sug = Suggestion.objects.get(pk=sug.pk)
        self.assertTrue(new_sug.clicked)









