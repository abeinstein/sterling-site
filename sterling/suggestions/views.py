from rest_framework import viewsets
from suggestions.models import AppUser, AppUserMembership, Algorithm, SuggestionList, Suggestion
from apps.models import MobileApp
from rest_framework.response import Response
from rest_framework.decorators import action
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
            if field in self.kwargs:
                filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object

class AppUserViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    multiple_lookup_fields = ['facebook_id']

    @action(methods=['POST'])
    def add_app_user(self, request, pk=None):
        ''' Takes a request of the following form:
        'app_facebook_id': Facebook ID of the app
        'oauth_token': OAuth Token for the particular user
        'facebook_id': Facebook ID of the user
        '''
        data = request.DATA
        serializer = AppUserSerializer(data=data)

        # Django REST framework is hopefully dealing with new vs existing AppUser objects
        if serializer.is_valid():
            serializer.save()
        app_user = serializer.object

        # Mobile App should already be configured on the website
        try:
            mobile_app = MobileApp.objects.get(pk=data.get('app_facebook_id'))
        except ObjectDoesNotExist:
            return Response("Mobile app does not exist", status=400)

        try:
            import pdb; pdb.set_trace()
            app_user_membership, app_user_membership_created = AppUserMembership.objects.get_or_create(app_user=app_user, 
                                                                    mobile_app=mobile_app, 
                                                                    oauth_token=data.get('oauth_token'))
        except:
            return Response("AppUserMembership could not be saved", status=400)

        # If it's a new user, create new AppUser objects for his friends
        if not app_user.friends.all():
            app_user.create_friends() 

        if mobile_app.default_algorithm:
            # Creates a suggestion list if one doesn't yet exist
            # This will go off and start running the default algorithm
            sl, sl_created = SuggestionList.objects.get_or_create(app_user_membership=app_user_membership,
                                                algorithm=mobile_app.default_algorithm)
            #sl.generate_suggestions()
            return Response("Success!", status=201)
        else:
            return Response("No default algorithm set", status=400)


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

    # def retrieve(self, request, pk=None):
    #     import pdb; pdb.set_trace()



class SuggestionViewSet(viewsets.ModelViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer