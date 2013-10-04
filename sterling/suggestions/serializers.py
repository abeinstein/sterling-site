from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField

from suggestions.models import AppUser, AppUserMembership, Algorithm, SuggestionList, Suggestion
from apps.models import MobileApp

class AppUserSerializer(serializers.HyperlinkedModelSerializer):
	
	class Meta:
		model = AppUser
		fields = ('id', 'facebook_id', 'name', 'created')

class AppUserMembershipSerializer(serializers.HyperlinkedModelSerializer):
	app_user = PrimaryKeyRelatedField(many = False)
	mobile_app = PrimaryKeyRelatedField(many = False)
	# algorithms = PrimaryKeyRelatedField(many = True)
	
	class Meta:
		model = AppUserMembership
		#fields = ('id', 'app_user', 'mobile_app', 'oauth_token', 'algorithms')

class AlgorithmSerializer(serializers.HyperlinkedModelSerializer):
	
	class Meta:
		model = Algorithm
		#fields = ('id', 'name', 'number_times_used', 'created')

class SuggestionListSerializer(serializers.HyperlinkedModelSerializer):
	app_user_membership = PrimaryKeyRelatedField(many = False)
	algorithm = PrimaryKeyRelatedField(many = False)
	# suggested_friends = PrimaryKeyRelatedField(many = True)
	
	class Meta:
		model = SuggestionList
		#fields = ('id', 'app_user_membership', 'algorithm', 'suggested_friends', 'created')	

class SuggestionSerializer(serializers.HyperlinkedModelSerializer):
	suggestion_list = PrimaryKeyRelatedField(many = False)
	app_user = PrimaryKeyRelatedField(many = False)
	
	class Meta:
		model = Suggestion
		#fields = ('id', 'suggestion_list', 'app_user', 'rank', 'invited', 'accepted', 'created')
	
	
	
