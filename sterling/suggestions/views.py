import datetime

from django.db.models import F
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.http import HttpResponseRedirect

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
# from rq import Queue
# from worker import conn
import django_rq


from apps.models import MobileApp
from suggestions.models import AppUser, AppUserMembership, Algorithm, SuggestionList, Suggestion
from suggestions.serializers import AppUserSerializer, AppUserMembershipSerializer, AlgorithmSerializer, SuggestionListSerializer, SuggestionSerializer
from suggestions.facebook_messenger import send_invitations_via_facebook_message

# # Setup Redis Queue
# q = Queue(connection=conn)

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
            error = {'error': "Invalid request"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        django_rq.enqueue(process_request, app_facebook_id, oauth_token, facebook_id)
        return Response(status=status.HTTP_201_CREATED)

def process_request(app_facebook_id, oauth_token, facebook_id):
    print "in process request"
    app_user, created = AppUser.objects.get_or_create(facebook_id=facebook_id)

    # If we have the AppUser in our system, it is possible that
    # he/she was invited from someone else. Let's check that
    # 
    if not created:
        # Get all suggestions that were made to app_user
        # TODO: Think more carefully about what we are accepting as accepted
        suggestions = Suggestion.objects.filter(app_user=app_user,
                                                times_invited__gt=0)

        suggestions.update(accepted=True, accepted_date=now())




    # Mobile App should already be configured on the website
    try:
        mobile_app = MobileApp.objects.get(pk=app_facebook_id)
    except ObjectDoesNotExist:
        error = {'error': "Mobile app does not exist"}
        # return Response(error, status=status.HTTP_400_BAD_REQUEST)
        print "Process request error: " + error
        return False

    try:
        app_user_membership, app_user_membership_created = AppUserMembership.objects.get_or_create(app_user=app_user, 
                                                                mobile_app=mobile_app)
    except:
        error = {'error': "AppUserMembership could not be created"}
        print "Process request error: " + error
        return False
        # return Response(error, status=status.HTTP_400_BAD_REQUEST)

    app_user_membership.oauth_token = oauth_token
    app_user_membership.save()

    # If it's a new user, create new AppUser objects for his friends
    app_user.update_friends() 

    if mobile_app.default_algorithm:
        # Creates a suggestion list if one doesn't yet exist
        # This will go off and start running the default algorithm
        sl, sl_created = SuggestionList.objects.get_or_create(app_user_membership=app_user_membership,
                                            algorithm=mobile_app.default_algorithm)

        if sl_created:
            sl.generate_suggestions()
        # return Response(status=status.HTTP_201_CREATED)
            return True
    else:
        # TODO: use less ghetto way of error handling
        error = "No default algorithm set"
        print "Process request error: " + error
        return False


class SuggestionsView(APIView):
    def get(self, request, format=None):
        ''' Returns an ordered list of suggestions '''
        data = request.QUERY_PARAMS

        try:
            app_facebook_id = data['app_facebook_id']
            facebook_id = data['facebook_id']
        except KeyError:
            error = {'error': "Invalid request"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        # Get objects
        try:
            app_user = AppUser.objects.get(facebook_id=facebook_id)
            mobile_app = MobileApp.objects.get(pk=app_facebook_id)
        except ObjectDoesNotExist:
            error = {'error': "AppUser or Mobile App does not exist"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

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
            error = {'error': "Invalid request"}
            return Response(error,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            suggestion_list = SuggestionList.objects.get(id=suggestion_list_id)
        except SuggestionList.DoesNotExist:
            error = {'error': "Suggestion List could not be found"}
            return Response(error, 
                            status=status.HTTP_400_BAD_REQUEST)


        '''Sends invitations through facebook messaging using XMPP client'''
        invitations_sent = send_invitations_via_facebook_message(suggestion_list=suggestion_list, 
                                                                friends_invited=friends_invited)
        # invitations_sent = send_invitations_via_facebook_message(sender=app_user.facebook_id, 
        #                                                        friends_invited=friends_invited, 
        #                                                        invitation_message=invitation_message, 
        #                                                        oauth_token=suggestion_list.app_user_membership.oauth_token,
        #                                                        app_facebook_id=mobile_app.facebook_id)

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

class InvitationsView(APIView):
    def get(self, request, format=None):
        data = request.QUERY_PARAMS

        try: 
            suggestion_id = data['suggestion']
        except KeyError:
            error = {'error': 'Malformed request. Need suggestion parameter'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        try:
            suggestion = Suggestion.objects.get(pk=suggestion_id)
        except Suggestion.DoesNotExist:
            error = {'error': "Could not find Suggestion object"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        suggestion.clicked = True
        suggestion.clicked_date = now()

        # TODO: Is this unacceptably slow? If so, figure out something else
        link = suggestion.suggestion_list.app_user_membership.mobile_app.link
        suggestion.save()

        if link:
            return HttpResponseRedirect(link)
        else:
            error = {'error': "Mobile app does not have a link"}
            return Response(error)







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