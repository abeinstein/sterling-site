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
    photo_score_dict = {}
    photo_score_dict_2 = {}

    for photo in photos:
        '''Trying to access tags/comments/likes will return 
        a KeyError if there are none for a photo'''
        try:
            tags = photo['tags']['data']
            increment_scores(tags, photo_score_dict, 5)
        except KeyError:
            continue

        try:
            comments = photo['comments']['data']
            increment_scores(comments, photo_score_dict, 3)
        except KeyError:
            continue

        try:
            likes = photo['likes']['data']
            increment_scores(likes, photo_score_dict, 2)
        except KeyError:
            continue

    '''Get rid of the original person'''
    try:
        del photo_score_dict[str(facebook_id)]
    except KeyError:
        pass

    friends = graph.get_connections("me", "friends")['data']
    friends = [friend['id'] for friend in friends]

    for friend in friends:
        try:
            photo_score_dict_2[friend] = photo_score_dict[friend]
        except KeyError:
            continue

    return sorted(photo_score_dict_2, key=photo_score_dict_2.get, reverse = True)

def increment_scores(object_list, id_score_dict, object_weight):
    for attribute in object_list:
        friend_id = attribute['id']
        try:
            id_score_dict[friend_id] += object_weight
        except LookupError:
            id_score_dict[friend_id] = object_weight











