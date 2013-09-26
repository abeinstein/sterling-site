from rest_framework import viewsets
from fbNodes.models import FbNode, SuggestionsNode, InvitationNode, InvitationsNode
from apps.models import MobileApp
from fbNodes.serializers import FbNodeSerializer, SuggestionsNodeSerializer, InvitationNodeSerializer, MobileAppSerializer, InvitationsNodeSerializer
from rest_framework.response import Response
from django.http import HttpResponse

class FbNodeViewSet(viewsets.ModelViewSet):
	queryset = FbNode.objects.all()
	serializer_class = FbNodeSerializer

class SuggestionsNodeViewSet(viewsets.ModelViewSet):
	queryset = SuggestionsNode.objects.all()
	serializer_class = SuggestionsNodeSerializer
	
class InvitationNodeViewSet(viewsets.ModelViewSet):
	queryset = InvitationNode.objects.all()
	serializer_class = InvitationNodeSerializer

class MobileAppViewSet(viewsets.ModelViewSet):
	queryset = MobileApp.objects.all()
	serializer_class = MobileAppSerializer

class InvitationsNodeViewSet(viewsets.ModelViewSet):
	queryset = InvitationsNode.objects.all()
	serializer_class = InvitationsNodeSerializer
