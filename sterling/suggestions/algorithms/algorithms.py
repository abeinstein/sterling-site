# This is where all of the algorithms should go
# Each algorithm should accept two arguments:
# <facebook_id> and <oauth_token>
import facebook
import utilities
import networkx as nx

def toy_algorithm(facebook_id, oauth_token):
    '''TODO: deprecate'''
    return ['100006812678326']

def alphabetical(facebook_id, oauth_token):
    ''' Returns users in an alphabetical list 
    FB Graph Calls: 1'''
    graph = facebook.GraphAPI(oauth_token)
    friends = graph.get_connections("me", "friends")

    sorted_friends = sorted(friends['data'], key=lambda d: d['name'])
    return [d['id'] for d in sorted_friends]

# def beinstein_1(facebook_id, oauth_token):
#     ''' My first attempt at a fancy algorithm '''
#     graph = facebook.GraphAPI(oauth_token)

def splash_site(facebook_id, oauth_token):
    '''FB Graph Calls: 0'''
    people = [
        '1247010773',
        '1084382373',
        '1141801163',
        '4',
        '1602780032',
        '1141801063',
        '1536551919',
        '504898389',
        '1155930700',
        '1140420329',
        '1365240449',
        '1846397448']
    return people

def dispersion_1(facebook_id, oauth_token):
    '''
       Sorts friends by dispersion
       Where dg = graph theoretic distance
       Distance metric = { dg < 1 : 0
                           dg = undefined : 0
                           dg > 1 : 1
                          }
       Runs at EWess "I have to get off the couch, really?" speed
       Should work on that
       facebook_id is not used
    '''

    graph = utilities.mutual_friends_nx_graph(oauth_token, verbose=True)
    return utilities.ordered_friends(graph)

def mutual_friends(facebook_id, oauth_token):
    '''Sorts friends by the mutual friend count
    Runs at EWess "I see a cake" speed
    FB Graph Calls: 1
    '''
    graph = facebook.GraphAPI(oauth_token)
    friends = graph.fql('''SELECT uid, mutual_friend_count 
                            FROM user WHERE uid IN 
                            (SELECT uid1 FROM friend WHERE uid2 = me()) 
                            ORDER BY mutual_friend_count DESC''')

    return [d['uid'] for d in friends]

def weighted_mutual_friends(facebook_id, oauth_token):
    '''Sorts friends by the mutual friend count
    divided by the number of friends that the second user has
    - if the friend has less than 100 total friends they get
    bumped to the bottom'''

    graph = facebook.GraphAPI(oauth_token)
    wmf_score_dict = {}

    friends = graph.fql('''SELECT uid, mutual_friend_count, friend_count 
                            FROM user WHERE uid IN 
                            (SELECT uid1 FROM friend WHERE uid2 = me()) 
                            ORDER BY mutual_friend_count DESC''')

    for friend in friends:
        friend_count = friend['friend_count']
        if (friend_count >= 500):
            weighted_friend_count = (friend['mutual_friend_count']**2)/(friend['friend_count']+0.0)
            score = weighted_friend_count
        else:
            score = 0
        wmf_score_dict[friend['uid']] = score

    return sorted(wmf_score_dict, key=wmf_score_dict.get, reverse = True)

def feed(facebook_id, oauth_token):
    graph = facebook.GraphAPI(oauth_token)
    feed = graph.get_object(facebook_id + "/feed")['data']
    friends = [friend['id'] for friend in graph.get_connections("me","friends")['data']]
    entries = []
    feed_score_dict = {}

    posted_by_list = []
    liked_post_list = []

    for entry in feed:
        entries.append(entry)

    posted_by_list =  [entry['from']['id'] for entry in entries if catch_key_error(entry, 'from')]

    likes = [entry['likes'] for entry in entries if catch_key_error(entry,'likes')]
    uid_lists = [like['data'] for like in likes]
    for uid_list in uid_lists:
        for uid in uid_list:
            liked_post_list.append(uid['id'])

    for friend in friends:
        post_score = 5*len([uid for uid in posted_by_list if uid == friend])
        like_score = len([uid for uid in liked_post_list if uid == friend])
        feed_score_dict[friend] = post_score + like_score

    return sorted(friends, key= feed_score_dict.get, reverse=True)

def photos(facebook_id, oauth_token):
    '''Looks at photos that the user has recently been tagged in
    and assigns scores to each friend based on their likes, comments
    and tags for those photos, weighting each relation differently
    FB Graph calls: 1
    '''
    graph = facebook.GraphAPI(oauth_token)
    photos = graph.get_object(facebook_id + "/photos")['data']
    score_dict = {}

    for photo in photos:
        '''Trying to access tags/comments/likes will return 
        a KeyError if there are none for a photo'''
        try:
            tags = photo['tags']['data']
            for tag in tags:
                uid = tag['id']
                add_value_to_dict(score_dict, uid, 3)
        except KeyError:
            pass

        try:
            comments = photo['comments']['data']
            for comment in comments:
                uid = comment['from']['id']
                add_value_to_dict(score_dict, uid, 2)
        except KeyError:
            pass

        try:
            likes = photo['likes']['data']
            for like in likes:
                uid = like['id']
                add_value_to_dict(score_dict, uid, 1)
        except KeyError:
            pass

    '''Get rid of the original person'''
    try:
        del score_dict[str(facebook_id)]
    except KeyError:
        pass

    '''Get rid of anyone that isn't friends with the user'''
    friends = [friend['id'] for friend in graph.get_connections("me", "friends")['data']]
    relevant_friends = list(set(friends).intersection(set(score_dict.keys())))
    return sorted(relevant_friends, key=score_dict.get, reverse=True)

def add_value_to_dict(dict, key, value):
    try:
        dict[key] += value
    except LookupError:
        dict[key] = value

def catch_key_error(entry, key):
    try:
        dummy = entry[key]
        return True
    except KeyError:
        return False

