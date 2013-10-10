from rest_framework.test import APITestCase
from rest_framework import status

from apps.models import MobileApp 
from suggestions.models import AppUser, Algorithm, AppUserMembership, SuggestionList, \
    Suggestion, ALGORITHM_ALPHABETICAL

STERLING_FACEBOOK_APP_ID = '466489223450195'
user_facebook_id = '100006825758175'

class SuggestionsAPITests(APITestCase):
    def setUp(self):
        self.algorithm = Algorithm.objects.create(
            name="Alphabetical",
            algorithm_method_id=ALGORITHM_ALPHABETICAL
        )

        self.mobile_app = MobileApp.objects.create(
            facebook_id=STERLING_FACEBOOK_APP_ID,
            name="Rush: Go Greek",
            invitation_message="Be the top frat on campus!",
            default_algorithm=self.algorithm
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
            'oauth_token': 'CAAGoRPx0jlMBABtCsuMswpNlBjFu5k2rTkADkytze7GK0GIoKudhDZCzmA0KNqZAhs25TpoeCZAU7tDJO4KZBqkkXZC5SM7JRZBhDABqYVTghJsBZAtouGZB9UextyWRDzr5MygUs2inTXGlAPdULbvojU7qs3e2uJKswOdncPOwf0d0S7XmKaZAA',
            'facebook_id': user_facebook_id
        }
        response = self.client.post('/appUserLogin/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


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

        # Check that suggestion objects were updated








