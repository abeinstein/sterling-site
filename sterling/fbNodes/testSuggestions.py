import facebook

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
			
	suggestions = get_suggestions_list(id_score_dict, id_name_dict)
	return suggestions

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
