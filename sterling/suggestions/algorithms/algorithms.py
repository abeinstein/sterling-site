# This is where all of the algorithms should go
# Each algorithm should accept two arguments:
# <facebook_id> and <oauth_token>
import facebook

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
            weighted_friend_count = (friend['mutual_friend_count']**3)/(friend['friend_count']+0.0)
            score = weighted_friend_count
        else:
            score = 0
        wmf_score_dict[friend['uid']] = score

    return sorted(wmf_score_dict, key=wmf_score_dict.get, reverse = True)

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
    friends = graph.get_connections("me", "friends")['data']
    friends = [friend['id'] for friend in friends]

    relevant_friends = list(set(friends).intersection(set(score_dict.keys())))

    return sorted(relevant_friends, key=score_dict.get, reverse=True)

def add_value_to_dict(dict, key, value):
    try:
        dict[key] += value
    except LookupError:
        dict[key] = value





