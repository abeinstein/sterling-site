from rest_framework import viewsets
from fbNodes.models import FbNode, SuggestionsNode, InvitationNode, AppNode, InvitationsNode
from fbNodes.serializers import FbNodeSerializer, SuggestionsNodeSerializer, InvitationNodeSerializer, AppNodeSerializer, InvitationsNodeSerializer
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

class AppNodeViewSet(viewsets.ModelViewSet):
	queryset = AppNode.objects.all()
	serializer_class = AppNodeSerializer

class InvitationsNodeViewSet(viewsets.ModelViewSet):
	queryset = InvitationsNode.objects.all()
	serializer_class = InvitationsNodeSerializer
