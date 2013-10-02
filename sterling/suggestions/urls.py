from django.conf.urls import patterns, include, url
from suggestions import views
from .views import AppUserViewSet, AppUserMembershipViewSet, AlgorithmViewSet, SuggestionListViewSet, SuggestionViewSet
from rest_framework.routers import DefaultRouter
from django.views.generic.base import RedirectView

router = DefaultRouter()
router.register(r'appUsers', AppUserViewSet)
router.register(r'appUserMemberships', AppUserMembershipViewSet)
router.register(r'algorithms', AlgorithmViewSet)
router.register(r'suggestionLists', SuggestionListViewSet)
router.register(r'suggestions', SuggestionViewSet)

urlpatterns = patterns('',
	url(r'', include(router.urls) ),
)