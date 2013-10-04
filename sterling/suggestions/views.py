from rest_framework import viewsets
from suggestions.models import AppUser, AppUserMembership, Algorithm, SuggestionList, Suggestion
from apps.models import MobileApp
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

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
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object

class AppUserViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    multiple_lookup_fields = ['facebook_id']

    def put(self, request, pk, format=None):
        data = request.DATA
        serializer = AppUserSerializer(data)
        if serializer.is_valid():
            serializer.save()
        app_user = serializer.object()
        app_user.create_friends() 

        app_facebook_id = data.app_facebook_id
        oauth_token = data.oauth_token

        try:
            mobile_app = MobileApp.objects.get(pk=app_facebook_id)
        except ObjectDoesNotExist:
            return Response("App does not exist", status=400)

        app_user_membership = AppUserMembership(app_user=app_user, mobile_app=mobile_app, oauth_token=oauth_token)
        app_user_membership.save()
        algorithm = mobile_app.default_algorithm
        suggestion_list = SuggestionList.objects.create(app_user_membership=app_user_membership,
                                                        algorithm=algorithm)

        




class AppUserMembershipViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    queryset = AppUserMembership.objects.all()
    serializer_class = AppUserMembershipSerializer
    multiple_lookup_fields = ['app_user__facebook_id', 'mobile_app__facebook_id']

class AlgorithmViewSet(viewsets.ModelViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer

class SuggestionListViewSet(viewsets.ModelViewSet):
    queryset = SuggestionList.objects.all()
    serializer_class = SuggestionListSerializer
    multiple_lookup_fields = ['app_user_membership__app_user__facebook_id', 'app_user_membership__app_user__facebook_id', 'algorithm__pk']

class SuggestionViewSet(viewsets.ModelViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer