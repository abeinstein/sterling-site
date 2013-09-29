from django.test import TestCase

from suggestions.models import AppUser, AppUserMembership, Algorithm, SuggestionList, Suggestion
from apps.models import MobileApp

class SuggestionsModelsTests(TestCase):
    def setUp(self):
        self.mobile_app = MobileApp.objects.create(facebook_id="123456",
                                                    name="Rush: Go Greek",
                                                )
        self.app_user = AppUser.objects.create(facebook_id="123414231",
                                                first_name="Mitch",
                                                last_name="Levy",
                                            )
        self.app_user_membership = AppUserMembership.objects.create(app_user=self.app_user, 
                                        mobile_app=self.mobile_app,
                                        oauth_token="23423534234234234",
                                        )
        self.algorithm = Algorithm.objects.create(name="Support Vector Machine")

        self.suggestion_list = SuggestionList.objects.create(app_user_membership=self.app_user_membership,
                                                            algorithm=self.algorithm)

        self.suggestion = Suggestion.objects.create(suggestion_list=self.suggestion_list,
                                                    app_user=self.app_user,
                                                    rank=1)

    def test_create_mobile_app(self):
        self.assertIsInstance(self.mobile_app, MobileApp)

    def test_create_app_user_membership(self):
        self.assertIsInstance(self.app_user_membership, AppUserMembership)

    def test_create_algorithm(self):
        self.assertIsInstance(self.algorithm, Algorithm)

    def test_create_suggestion_list(self):
        self.assertIsInstance(self.suggestion_list, SuggestionList)

    def test_create_suggestion(self):
        self.assertIsInstance(self.suggestion, Suggestion)