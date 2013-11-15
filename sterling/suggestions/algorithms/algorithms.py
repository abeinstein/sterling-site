# This is where all of the algorithms should go
# Each algorithm should accept two arguments:
# <facebook_id> and <oauth_token>
import facebook
import utilities
import networkx as nx
from collections import defaultdict
import re

from filters import sports_score, political_score, paging, books_score, music_score, restaurants_score, games_score
from filters import sport_ranks, political_ranks, book_ranks, game_ranks, restaurant_ranks, music_ranks

class AlgorithmManager():
    def __init__(self, facebook_id, oauth_token):
        self.facebook_id = facebook_id
        self.oauth_token = oauth_token
        self.graph = facebook.GraphAPI(self.oauth_token)

    def run(self, algorithm, params):
        best_friends = to_dict(algorithm(self.graph))

        params_lists = []
        filter_list = best_friends.keys() # Will only select friends in this list

        if ( (params['likes_sports']) or (params['political_bias'] is not 0) or (params['likes_books']) 
            or (params['likes_games']) or (params['likes_restaurants']) or (params['likes_music']) ):
            friends_likes = get_friends_likes(self.graph)

        if params['likes_sports']:
            sport_rankings = to_dict(sport_ranks(self.graph, friends_likes))
            params_lists.append(sport_rankings)

        if params['political_bias'] is not 0:
            #is_liberal = params['political_bias'] == 1
            political_rankings = to_dict(political_ranks(self.graph, friends_likes))
            params_lists.append(political_rankings)

        # Now, check social circles
        if params['social_circle'] is not None:
            social_circle = params['social_circle']
            # High school friends
            if social_circle == 'hsf':
                social_circle_friends = get_hs_friends(self.graph)
            elif social_circle == 'colf':
                social_circle_friends = get_col_friends(self.graph)
            elif social_circle == 'co':
                social_circle_friends = get_colleagues(self.graph)
            else:
                social_circle_friends = filter_list
            # shitty hackathon code:
            filter_list = list(set(social_circle_friends).intersection(set(filter_list)))

        if params['city'] is not None:
            friends_in_city = get_friends_in_city(self.graph, params['city'])
            filter_list = list(set(friends_in_city).intersection(set(filter_list)))

        if params['likes_books']:
            book_rankings = to_dict(book_ranks(self.graph, friends_likes))
            params_lists.append(book_rankings)

        if params['likes_games']:
            game_rankings = to_dict(game_ranks(self.graph, friends_likes))
            params_lists.append(game_rankings)

        if params['likes_restaurants']:
            restaurant_rankings = to_dict(restaurant_ranks(self.graph, friends_likes))
            params_lists.append(restaurant_rankings)

        if params['likes_music']:
            music_rankings = to_dict(music_ranks(self.graph, friends_likes))
            params_lists.append(music_rankings)
        
        # Now, create list combining the lists

        def rank(fbid):
            if len(params_lists) is 0:
                pref_score = 0
            else:
                pref_score = sum([ get_pref_score(li, fbid) for li in params_lists]) / (2.0*len(params_lists))
            bf_score = best_friends[fbid]
            return (pref_score + bf_score)

        return sorted(filter_list, key=rank) + sorted(list(set(best_friends.keys())-set(filter_list)), key=rank)

def get_pref_score(dict, fbid):
    try:
        return dict[fbid]
    except KeyError:
        return 0

def to_dict(ordered_list):
    return dict([(val, i) for i, val in enumerate(ordered_list)])

def get_friends_in_city(graph, city):
    args = {'fields': 'id,name,location'}
    friends = graph.get_connections("me", "friends", **args)

    friends_in_city = [f['id'] for f in friends['data'] if in_right_city(f, city)]
    return friends_in_city

def in_right_city(f, city):
    try:
        return (f['location']['name']==city)
    except KeyError:
        return False

def get_hs_friends(graph):
    ''' Gets a users HS friends '''
    high_schools = defaultdict(list)
    args = {'fields': 'id,name,education'}
    friends = graph.get_connections("me", "friends", **args)
    for f in friends['data']:
        try:
            hs = [school['school']['id'] for school in f['education'] if school['type'] == 'High School'][0]
            high_schools[hs].append(f['id'])
        except KeyError:
            pass
        except IndexError:
            pass

    high_school = max(high_schools.keys(), key=lambda hsid: len(high_schools[hsid]))

    return high_schools[high_school]
    #return [f['id'] for f in friends['data'] if 'education' in f if high_school in [s['school']['id'] for s in f['education']]]



def get_col_friends(graph):
    ''' Gets a users college friends '''
    colleges = defaultdict(list)
    args = {'fields': 'id,name,education'}
    friends = graph.get_connections("me", "friends", **args)
    for f in friends['data']:
        try:
            col = [school['school']['id'] for school in f['education'] if school['type'] == 'College'][0]
            colleges[col].append(f['id'])
        except KeyError:
            pass
        except IndexError:
            pass

    college = max(colleges.keys(), key=lambda colid: len(colleges[colid]))

    return colleges[college]
    #return [f['id'] for f in friends['data'] if 'education' in f if college in [s['school']['id'] for s in f['education']]]

def get_colleagues(graph):
    ''' Gets a users colleagues '''
    workplaces = defaultdict(list)
    args = {'fields': 'id,name,work'}
    friends = graph.get_connections("me", "friends", **args)
    for f in friends['data']:
        try:
            work_ids = [work['employer']['id'] for work in f['work']]
            for id in work_ids:
                workplaces[id].append(f['id'])
        except KeyError:
            pass

    workplace = max(workplaces.keys(), key=lambda workid: len(workplaces[workid]))
    return workplaces[workplace]

def get_family(graph):
    ''' Gets a users family '''
    raise NotImplementedError


def toy_algorithm(graph):
    '''TODO: deprecate'''
    return ['100006812678326']

def alphabetical(graph):
    ''' Returns users in an alphabetical list 
    FB Graph Calls: 1'''
    friends = graph.get_connections("me", "friends")

    sorted_friends = sorted(friends['data'], key=lambda d: d['name'])
    return [d['id'] for d in sorted_friends]


def splash_site(graph):
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

def dispersion_1(graph):
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

    graph = utilities.mutual_friends_nx_graph(graph.access_token, verbose=True)
    return utilities.ordered_friends(graph)

def mutual_friends(graph):
    '''Sorts friends by the mutual friend count
    Runs at EWess "I see a cake" speed
    FB Graph Calls: 1
    '''
    friends = graph.fql('''SELECT uid, mutual_friend_count 
                            FROM user WHERE uid IN 
                            (SELECT uid1 FROM friend WHERE uid2 = me()) 
                            ORDER BY mutual_friend_count DESC''')

    return [d['uid'] for d in friends]

def weighted_mutual_friends(graph):
    '''Sorts friends by the mutual friend count
    divided by the number of friends that the second user has
    - if the friend has less than 100 total friends they get
    bumped to the bottom'''

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

@paging
def get_feed(response):
    feed = []
    for f in response['data']:
        feed.append(f)
    return feed

def feed(graph):
    feed = get_feed(graph.get_object("me/feed"))
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

@paging
def get_photos(response):
    photos = []
    for p in response['data']:
        photos.append(p)
    return photos


def photos(graph):
    '''Looks at photos that the user has recently been tagged in
    and assigns scores to each friend based on their likes, comments
    and tags for those photos, weighting each relation differently
    FB Graph calls: 1
    '''
    photos = get_photos(graph.get_object("me/photos"))
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
    # try:
    #     del score_dict[str(facebook_id)]
    # except KeyError:
    #     pass

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

def get_friends_likes(graph):
    friends = [friend['id'] for friend in graph.get_connections("me", "friends")['data']]
    batch_request_list = [ (friend, likes_request(friend)) for friend in friends]
    like_lists = []
    while (len(batch_request_list) > 0):
        like_list = graph.request("", post_args={"batch": [batch[1] for batch in batch_request_list[0:50]]})
        friends_list = [batch[0] for batch in batch_request_list[0:50]]
        like_lists += [(friends_list[i], get_data(like_list[i]) ) for i in range(min(50, len(like_list)))]

        next_page_urls = [next_page(eval(person_likes['body'])) for person_likes in like_list if (next_page(eval(person_likes['body'])) is not None)]
        batch_request_list = batch_request_list[len(like_list):]

        for url in next_page_urls:
            uid = re.findall("https://graph.facebook.com/([0-9]+)", url)[0]
            limit = (re.findall("([&\?]limit=[0-9]+)\Z", url) + re.findall("([&\?]limit=[0-9]+)[&\?]", url))[0]
            after = (re.findall("([&\?]after=.*)\Z", url) + re.findall("([&\?]after=.*)[&\?]", url))[0]
            paging_info = "?" + limit[1:] + "&" + after[1:]

            next_batch_request = {"method": "GET", "relative_url": (str(uid) + "/likes?" + paging_info)}
            batch_request_list.append( (uid, next_batch_request))


    like_dict = {}
    for like_list in like_lists:
        person = like_list[0]
        try:
            like_dict[person] += like_list[1]
        except KeyError:
            like_dict[person] = like_list[1]
        except TypeError:
            pass

    return like_dict

def get_data(person_likes):
    try:
        return eval(person_likes['body'])['data']
    except KeyError:
        pass

def likes_request(friend):
    return {"method": "GET", "relative_url": (str(friend) + "/likes")}

def next_page(like_list):
    try:
        return like_list['paging']['next'].replace('\/', '/')
    except KeyError:
        pass





