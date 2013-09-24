from django.conf.urls import patterns, include, url
from fbNodes import views
from fbNodes.views import FbNodeViewSet, SuggestionsNodeViewSet, InvitationNodeViewSet, AppNodeViewSet, InvitationsNodeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'fbNodes', FbNodeViewSet)
router.register(r'suggestionsNodes', SuggestionsNodeViewSet)
router.register(r'invitationNodes', InvitationNodeViewSet)
router.register(r'appNodes', AppNodeViewSet)
router.register(r'invitationsNodes', InvitationsNodeViewSet)


urlpatterns = patterns('',
	url(r'invitationNodes/*+', RedirectView.as_view(url='http://itunes.com/apps/rushgogreek') ),
	url(r'', include(router.urls) ),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework') ),
)