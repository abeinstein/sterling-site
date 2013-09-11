import urllib2
import facebook
import re
import operator
import random
import json
import ast
from django.utils.simplejson import dumps

def fSuggestions(user_id, o_auth_token, app_id):
	algorithm_id = random.randint(1, len(algorithms) )
	algorithm = algorithms[algorithm_id]
	suggestions_list = algorithm(user_id.encode('utf-8'), o_auth_token.encode('utf-8'))
	suggestions = (suggestions_list, algorithm_id, app_id)
	
	return suggestions

#Algorithm based on number of mutual friends
#Pretty effective when run over a full friend list, but way too slow
#Maybe we can presort to <100 friends and then compute mutual friend
#	counts just for that group of users?
def sort_by_mutual_friends(user_id, o_auth_token):
	graph = facebook.GraphAPI(o_auth_token)
	friends = graph.get_connections("me", "friends")
	friend_id_list = [friend['id'].encode('utf-8') for friend in friends['data']]
	friend_name_list = [friend['name'].encode('utf-8') for friend in friends['data']]
	
	friend_id_name_dict = {}
	for i in range(0, len(friend_id_list) ):
		friend_id = friend_id_list[i]
		friend_name = friend_name_list[i]
		friend_id_name_dict[friend_id] = friend_name
	
	id_score_dict = {}
	suggestions = []
	
	mutual_friends_batch_request = get_mutual_friends_batch_request(user_id, friend_id_list)
	
	#Get all mutual friends for each friend, then do some parsing
	i = 0
	while (i< 100 ):
				
		#Batch requests 50 at a time due to facebook limitations
		batch_limit = min(i+50, len(mutual_friends_batch_request))
		partial_mutual_friends_batch_request = mutual_friends_batch_request[i:batch_limit]
		mutual_friends_list = graph.request("", post_args={"batch": partial_mutual_friends_batch_request} )
		
		#Parse out user id, mutual friend count from batch return to fill out id_mutual_friend_count_dict
		for mutual_friends_text in mutual_friends_list:
			mutual_friends = mutual_friends_text['body'].split('[')[1].split(']')[0].split('},{')
			if (mutual_friends_text['body'] != '{"data":[]}'):
				friend_id = re.findall("user=([0-9]+)", mutual_friends_text['body'])[0]
				mutual_friend_count = len(mutual_friends)			
				id_score_dict[friend_id] = mutual_friend_count
		
		#Increment i by 50 to continue process
		i = i + 50
		
	#Sort by scores and return a suggestions list
	suggestions = get_suggestions_list(id_score_dict, friend_id_name_dict)
	return suggestions	


#Algorithm based on recent photos
def sort_by_photos(user_id, o_auth_token):
	graph = facebook.GraphAPI(o_auth_token)
	photos = graph.get_object(user_id + "/photos")
	photo_id_list = [photo['id'] for photo in photos['data']]
	
	noTags = 0
	noComments = 0
	noLikes = 0
	id_score_dict = {}
	id_name_dict = {}
	
	for photo in photos['data']:
		try:
			tags = photo['tags']['data']
			for tag in tags:
				friend_id = tag['id'].encode('utf-8')
				friend_name = tag['name'].encode('utf-8')
				add_to_id_score_dict(friend_id, 5, id_score_dict)
				add_to_id_name_dict(friend_id, friend_name, id_name_dict)
		except KeyError:
			noTags = noTags + 1
			
		try:
			comments = photo['comments']['data']
			for comment in comments:
				friend_id = comment['id'].encode('utf-8')
				friend_name = comment['name'].encode('utf-8')
				add_to_id_score_dict(friend_id, 3, id_score_dict)
				add_to_id_name_dict(friend_id, friend_name, id_name_dict)
		except KeyError:
			noComments = noComments + 1
		
		try:
			likes = photo['likes']['data']
			for like in likes:
				friend_id = like['id'].encode('utf-8')
				friend_name = like['name'].encode('utf-8')
				add_to_id_score_dict(friend_id, 2, id_score_dict)
				add_to_id_name_dict(friend_id, friend_name, id_name_dict)
		except KeyError:
			noLikes = noLikes + 1
			
	try:
		del id_score_dict[user_id]
		del id_name_dict[user_id]
	except KeyError:
		print ""
		
	suggestions = get_suggestions_list(id_score_dict, id_name_dict)
	return suggestions


algorithms = {1: sort_by_photos}

#Take a dictionary of ids and scores and return a sorted suggestions list
def get_suggestions_list(id_score_dict, friend_id_name_dict):
	suggestions = []
	sorted_id_name_dicts = []
	returnString = ""
	
	sorted_id_score_dict = sorted(id_score_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
		
	for id_score in sorted_id_score_dict:
		small_dict = {}
		friend_id = id_score[0]
		small_dict[dumps("user_id")] = dumps(friend_id)
		small_dict[dumps("user_name")] = dumps(friend_id_name_dict[friend_id])
		sorted_id_name_dicts.append(small_dict)
			
	return str(sorted_id_name_dicts)
		
	#for friend_id in suggestions:
	#	returnString += '''{"user_id":''' + friend_id + "," + '''"name":"''' + friend_id_name_dict[friend_id] + '''"},'''
	
	#return "[" + returnString[:-1] + "]"


#Get the batch request to grab the mutual friends lists for a user and all his friends
def get_mutual_friends_batch_request(user_id, friend_id_list):
	mutual_friends_batch_request = []
	for i in range(0, len(friend_id_list) ):
		friend_id = friend_id_list[i]
		mutual_friends_request = get_mutual_friends_request(user_id, friend_id)
		mutual_friends_batch_request.append(mutual_friends_request)
		
	return mutual_friends_batch_request


#Get the request to grab the mutual friends list for a user and a friend using their ids
def get_mutual_friends_request(user_id, friend_id):
	mutual_friends_request = {"method":"GET", "relative_url":(str(user_id) + "/mutualfriends/" + str(friend_id))}
	return mutual_friends_request


def add_to_id_score_dict(friend_id, score, id_score_dict):
	try:
		id_score_dict[friend_id] = id_score_dict[friend_id] + score
	except LookupError:
		id_score_dict[friend_id] = score


def add_to_id_name_dict(friend_id, name, id_name_dict):
	try:
		id_name_dict[friend_id]
	except LookupError:
		id_name_dict[friend_id] = name

