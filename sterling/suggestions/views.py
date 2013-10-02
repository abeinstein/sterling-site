from rest_framework import viewsets
from suggestions.models import AppUser, AppUserMembership, Algorithm, SuggestionList, Suggestion
from apps.models import MobileApp

from suggestions.serializers import AppUserSerializer, AppUserMembershipSerializer, AlgorithmSerializer, SuggestionListSerializer, SuggestionSerializer

class AppUserViewSet(viewsets.ModelViewSet):
	queryset = AppUser.objects.all()
	serializer_class = AppUserSerializer

class AppUserMembershipViewSet(viewsets.ModelViewSet):
	queryset = AppUserMembership.objects.all()
	serializer_class = AppUserMembershipSerializer

class AlgorithmViewSet(viewsets.ModelViewSet):
	queryset = Algorithm.objects.all()
	serializer_class = AlgorithmSerializer

class SuggestionListViewSet(viewsets.ModelViewSet):
	queryset = SuggestionList.objects.all()
	serializer_class = SuggestionListSerializer

class SuggestionViewSet(viewsets.ModelViewSet):
	queryset = Suggestion.objects.all()
	serializer_class = SuggestionSerializer