from fbNodes.models import FbNode, SuggestionsNode, InvitationNode, InvitationsNode
from apps.models import MobileApp
from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField

class FbNodeSerializer(serializers.HyperlinkedModelSerializer):	
	apps = PrimaryKeyRelatedField(many=True)
	
	class Meta:
		model = FbNode
		fields = ('created', 'current_app_id', 'apps', 'user_id', 'o_auth_token')

class SuggestionsNodeSerializer(serializers.HyperlinkedModelSerializer):
	app = PrimaryKeyRelatedField(many=False)
	user = PrimaryKeyRelatedField(many=False)
		
	class Meta:
		model = SuggestionsNode
		fields = ('created', 'user', 'app', 'suggestions_list', 'algorithm_id', 'node_id')


class InvitationNodeSerializer(serializers.HyperlinkedModelSerializer):
	inviter = PrimaryKeyRelatedField(many=False)
	app = PrimaryKeyRelatedField(many=False)
		
	class Meta:
		model = InvitationNode
		fields = ('node_id', 'created', 'inviter', 'invited_id', 'app', 'link_clicked', 'link_clicked_date', 'join_date')
		depth = 1


class InvitationsNodeSerializer(serializers.HyperlinkedModelSerializer):
	inviter = PrimaryKeyRelatedField(many=False)
	app = PrimaryKeyRelatedField(many=False)
		
	class Meta:
		model = InvitationsNode
		fields = ('node_id', 'created', 'inviter', 'invited_list', 'app')
		depth = 1
	

class MobileAppSerializer(serializers.HyperlinkedModelSerializer):
		
	class Meta:
		model = MobileApp
		fields = ('created', 'app_id')
	
