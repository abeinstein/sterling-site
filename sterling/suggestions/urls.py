from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from django.views.generic.base import RedirectView
from django.conf.urls import patterns, include, url

from .views import AppUserViewSet, AppUserMembershipViewSet, AlgorithmViewSet, \
SuggestionListViewSet, SuggestionViewSet, AppUserLoginView, SuggestionsView, \
InvitationsView
from .models import AppUser, AppUserMembership


router = DefaultRouter()
router.register(r'appUsers', AppUserViewSet)
router.register(r'appUserMemberships', AppUserMembershipViewSet)
router.register(r'algorithms', AlgorithmViewSet)
router.register(r'suggestionLists', SuggestionListViewSet)
router.register(r'suggestions', SuggestionViewSet)

app_user_detail = AppUserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

app_user_membership_detail = AppUserMembershipViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

suggestion_list_detail = SuggestionListViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns(patterns('',
	url(r'^appUsers/facebook_id=(?P<facebook_id>[0-9]+)/$', app_user_detail, name='app_user_detail'),
	url(r'^appUserMemberships/facebook_id=(?P<app_user__facebook_id>[0-9]+)&app_facebook_id=(?P<mobile_app__facebook_id>[0-9]+)/$', app_user_membership_detail, name='app_user_membership_detail' ),
	url(r'^suggestionLists/facebook_id=(?P<app_user_membership__app_user__facebook_id>[0-9]+)&app_facebook_id=(?P<app_user_membership__mobile_app__facebook_id>[0-9]+)/$', suggestion_list_detail, name='suggestion_list_detail'),

    # URLS for Adam to use
    url(r'^appUserLogin/', AppUserLoginView.as_view(), name='app-user-login'),
    url(r'^suggestions/', SuggestionsView.as_view(), name='suggestions'),

    # Invitation redirect URL
    url(r'invitations/', InvitationsView.as_view(), name='invitations')
))

urlpatterns += patterns('',
	url(r'', include(router.urls)),
)
