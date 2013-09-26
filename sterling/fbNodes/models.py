from django.db import models
from django.db.models.signals import post_save
from django.utils.simplejson import dumps
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect

from fbNodes.suggestions import fSuggestions
from fbNodes.facebookMessages import send_facebook_messages
from apps.models import MobileApp

from rest_framework.renderers import JSONRenderer

from datetime import datetime
import json
import ast

base_url = "http://sterling.herokuapp.com/"

class FbNode(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	user_id = models.TextField(max_length=50, primary_key=True)
	o_auth_token = models.TextField()
	current_app_id = models.CharField(max_length=50, null=True)
	apps = models.ManyToManyField(MobileApp, blank=True, null=True)
	
	def save(self, **kwargs):
		current_app = MobileApp.objects.get(facebook_id=self.current_app_id)
		super(FbNode, self).save()
		self.apps.add(current_app)
		FbNode.save(self)


class SuggestionsNode(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(FbNode)
	app = models.ForeignKey(MobileApp)
	suggestions_list = models.TextField()
	algorithm_id = models.TextField()
	node_id = models.TextField(primary_key=True)
	
	def get(self, request, format = None):
		new_suggestions_list = []
		
		suggestions_list = self.sugestions_list
		suggestions_list = ast.literal_eval(suggestions_list)
		
		for small_dict in suggestions_list:
			new_small_dict = dumps(ast.literal_eval(small_dict))
			new_suggestions_list.append(new_small_dict)
		
		content = dumps(content)
		for i in range(0, len(content) ):
			if (content[i] == "\\") or (content[i] == "\'"):
				del content[i]
		return Response(content)
	
	def save(self, **kwargs):
		self.node_id = "app_id=" + str(self.app.app_id) + "&user_id=" + str(self.user.user_id)
		#self.node_id = "app_id=%d&user_id=%d" % (self.app.app_id, self.user.user_id)
		super(SuggestionsNode, self).save()
	


class InvitationNode(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	inviter = models.ForeignKey(FbNode)
	invited_id = models.TextField()
	app = models.ForeignKey(MobileApp)
	link_clicked = models.BooleanField(default=False)
	link_clicked_date = models.DateTimeField(null=True)
	join_date = models.DateTimeField(null=True)	
	node_id = models.TextField(primary_key=True)
	
	def get(self, request, format = None):
		#setattr(self, 'link_clicked', True)
		#setattr(self, 'link_clicked_date', datetime.now())
		
		self.link_clicked = True
		self.link_clicked_date = datetime.now()
		super(InvitationNode, self).save()
		
		#return HttpResponseRedirect('http://itunes.com/apps/rushgogreek', permanent=True)
	
	def save(self, *args, **kwargs):
		self.created = datetime.now()
		super(InvitationNode, self).save()
	


class InvitationsNode(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	inviter = models.ForeignKey(FbNode)
	invited_list = models.TextField()
	app = models.ForeignKey(MobileApp)
	node_id = models.TextField(primary_key=True)
		
	def save(self, **kwargs):
		self.node_id = "app_id=" + str(self.app.app_id) + "&user_id=" + str(self.inviter.user_id)
		super(InvitationsNode, self).save()
	


def save_suggestions_list(sender, **kwargs):
	obj = kwargs['instance']
	if (obj.current_app_id != None):
		o_auth_token = obj.o_auth_token
		user_id = obj.user_id
		current_app_id = obj.current_app_id
		suggestions = fSuggestions(user_id, o_auth_token, current_app_id)
	
		suggestions_node = SuggestionsNode()
		suggestions_node.created = datetime.now()
		suggestions_node.user = FbNode.objects.get(user_id=user_id)
		suggestions_node.suggestions_list = suggestions[0]
		suggestions_node.algorithm_id = suggestions[1]
		suggestions_node.app = MobileApp.objects.get(facebook_id=suggestions[2])
		SuggestionsNode.save(suggestions_node)


post_save.connect(save_suggestions_list, sender=FbNode)

def save_invitation_nodes(sender, **kwargs):
	obj = kwargs['instance']
	invited_list_string = obj.invited_list
	invited_list = ast.literal_eval(invited_list_string)
		
	for invited_id in invited_list:
		invitation_node = InvitationNode()
		invitation_node.inviter = obj.inviter
		invitation_node.invited_id = invited_id
		invitation_node.app = obj.app
		invitation_node.created = obj.created
		invitation_node.node_id = "app_id=" + str(invitation_node.app.app_id) + "&inviter_id=" + str(invitation_node.inviter.user_id) + "&invited_id=" + str(invited_id)
		InvitationNode.save(invitation_node)	


post_save.connect(save_invitation_nodes, sender=InvitationsNode)

def send_invitations_by_fb_message(sender, **kwargs):
	obj = kwargs['instance']
	invited_list = obj.invited_list
	inviter = obj.inviter
	inviter_id = inviter.user_id
	o_auth_token = inviter.o_auth_token
	message = "This is a link to rush go greek: http://itunes.com/apps/rushgogreek"
	
	send_facebook_messages(inviter_id, invited_list, message, o_auth_token)


post_save.connect(send_invitations_by_fb_message, sender=InvitationsNode)
	
	
	
	
	
	
