import datetime

from django.db.models import F
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.models import MobileApp
from suggestions.models import AppUser, AppUserMembership, Algorithm, SuggestionList, Suggestion
from suggestions.serializers import AppUserSerializer, AppUserMembershipSerializer, AlgorithmSerializer, SuggestionListSerializer, SuggestionSerializer

class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.multiple_lookup_fields:
            if field in self.kwargs:
                filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object


class AppUserLoginView(APIView):
    def get_object(self, facebook_id):
        try:
            return AppUser.objects.get(facebook_id=facebook_id)
        except AppUser.DoesNotExist:
            return AppUser.objects.create(facebook_id=facebook_id)

    def post(self, request, format=None):
        ''' Takes a request of the following form:
        'app_facebook_id': Facebook ID of the app
        'oauth_token': OAuth Token for the particular user
        'facebook_id': Facebook ID of the user
        '''
        data = request.DATA
        try:
            app_facebook_id = data['app_facebook_id']
            oauth_token = data['oauth_token']
            facebook_id = data['facebook_id']
        except KeyError:
            return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)

        app_user = self.get_object(facebook_id)

        # Mobile App should already be configured on the website
        try:
            mobile_app = MobileApp.objects.get(pk=app_facebook_id)
        except ObjectDoesNotExist:
            return Response("Mobile app does not exist", status=status.HTTP_400_BAD_REQUEST)

        try:
            app_user_membership, app_user_membership_created = AppUserMembership.objects.get_or_create(app_user=app_user, 
                                                                    mobile_app=mobile_app, 
                                                                    oauth_token=oauth_token)
        except:
            return Response("AppUserMembership could not be saved", status=status.HTTP_400_BAD_REQUEST)

        # If it's a new user, create new AppUser objects for his friends
        app_user.update_friends() 

        if mobile_app.default_algorithm:
            # Creates a suggestion list if one doesn't yet exist
            # This will go off and start running the default algorithm
            sl, sl_created = SuggestionList.objects.get_or_create(app_user_membership=app_user_membership,
                                                algorithm=mobile_app.default_algorithm)
            #sl.generate_suggestions()
            return Response("Success!", status=status.HTTP_201_CREATED)
        else:
            return Response("No default algorithm set", status=status.HTTP_400_BAD_REQUEST)


class SuggestionsView(APIView):
    def get(self, request, format=None):
        ''' Returns an ordered list of suggestions '''
        data = request.QUERY_PARAMS

        try:
            app_facebook_id = data['app_facebook_id']
            facebook_id = data['facebook_id']
        except KeyError:
            return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)

        # Get objects
        try:
            app_user = AppUser.objects.get(facebook_id=facebook_id)
            mobile_app = MobileApp.objects.get(pk=app_facebook_id)
        except ObjectDoesNotExist:
            return Response("AppUser or Mobile App does not exist", status=status.HTTP_400_BAD_REQUEST)

        app_user_membership = AppUserMembership.objects.get(app_user=app_user,
                                                            mobile_app=mobile_app)

        # Gets first suggestion list
        # TODO -- more intelligent suggestion list choosing mechanism
        suggestion_list = app_user_membership.suggestionlist_set.all()[0]
        friends = suggestion_list.suggested_friends.all().order_by('suggestion__rank')

        # TODO: Custom friend suggestion serializer that takes a suggestion list?
        response_data = {'list_id': suggestion_list.pk, 'friends': []}
        for f in friends:
            response_data['friends'].append({'id': f.facebook_id,
                                'name': f.name })

        return Response(response_data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        ''' Captures person views and invites. Requires:
        - list_id (int)
        - friends_seen (list)
        - friends_invited (list)
        ''' 
        data = request.DATA

        try:
            suggestion_list_id = data['list_id']
            friends_seen = data['friends_seen']
            friends_invited = data['friends_invited']
        except KeyError:
            return Response("Invalid request",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            suggestion_list = SuggestionList.objects.get(id=suggestion_list_id)
        except SuggestionList.DoesNotExist:
            return Response("Suggestion List could not be found", 
                            status=status.HTTP_400_BAD_REQUEST)

        # FUCK YES!!
        Suggestion.objects.filter(
            suggestion_list=suggestion_list,
            app_user__facebook_id__in=friends_seen
        ).update(
            times_presented=F('times_presented') + 1,
            last_presented_date=now()
        )

        Suggestion.objects.filter(
            suggestion_list=suggestion_list,
            app_user__facebook_id__in=friends_invited
        ).update(
            times_invited = F('times_invited') + 1,
            last_invited_date = now()
        )

        return Response(status=status.HTTP_200_OK)



###
# Model Viewsets
# Deprecated
####
class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    multiple_lookup_fields = ['facebook_id']

class AppUserMembershipViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    queryset = AppUserMembership.objects.all()
    serializer_class = AppUserMembershipSerializer
    multiple_lookup_fields = ['app_user__facebook_id', 'mobile_app__facebook_id']

class AlgorithmViewSet(viewsets.ModelViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer

class SuggestionListViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    queryset = SuggestionList.objects.all()
    serializer_class = SuggestionListSerializer
    multiple_lookup_fields = ['app_user_membership__app_user__facebook_id', 'app_user_membership__app_user__facebook_id']

class SuggestionViewSet(viewsets.ModelViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer