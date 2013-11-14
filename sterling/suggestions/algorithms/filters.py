import json
import facebook
import urllib2
import re

def paging(f):
        ''' Decorator for paging through facebook responses '''
        def inner(response):
            data = []
            i=0
            while (True and (i < 10) ):
                data.extend(f(response))
                try:
                    response = json.loads(urllib2.urlopen(response["paging"]["next"]).readlines()[0])
                    i += 1
                except KeyError:
                    break
            return data
        return inner


@paging
def get_politicians(response):
    politicians = []
    for like in response['data']:
        if like['category'] == 'Politician':
            politicians.append(like)

    return politicians

@paging
def get_sports_likes(response):
    sports_likes = []
    categories = SPORTS_CATEGORIES
    for like in response['data']:
        if like['category'] in categories:
            sports_likes.append(like)

    return sports_likes

@paging
def get_books_likes(response):
    categories = BOOK_CATEGORIES

    books_likes = [like for like in response['data'] if like['category'] in categories]
    return books_likes

@paging
def get_games_likes(response):
    categories = GAME_CATEGORIES

    games_likes = [like for like in response['data'] if like['category'] in categories]
    return games_likes

@paging
def get_restaurants_likes(response):
    categories = RESTAURANT_CATEGORIES

    restaurants_likes = [like for like in response['data'] if like['category'] in categories]
    return restaurants_likes

@paging
def get_music_likes(response):
    categories = MUSIC_CATEGORIES
    music_likes = [like for like in response['data'] if like['category'] in categories]
    return music_likes

def sport_ranks(graph, friends_likes):
    score_dict = {}
    for uid in friends_likes.keys():
        score_dict[uid] = len([like for like in friends_likes[uid] if str(like['category']) in SPORTS_CATEGORIES])
    return sorted(score_dict.keys(), key=score_dict.get, reverse=True)

def political_ranks(graph, friends_likes):
    pass

def book_ranks(graph, friends_likes):
    score_dict = {}
    for uid in friends_likes.keys():
        score_dict[uid] = len([like for like in friends_likes[uid] if str(like['category']) in BOOK_CATEGORIES])
    return sorted(score_dict.keys(), key=score_dict.get, reverse=True)

def game_ranks(graph, friends_likes):
    score_dict = {}
    for uid in friends_likes.keys():
        score_dict[uid] = len([like for like in friends_likes[uid] if str(like['category']) in GAME_CATEGORIES])
    return sorted(score_dict.keys(), key=score_dict.get, reverse=True)

def restaurant_ranks(graph, friends_likes):
    score_dict = {}
    for uid in friends_likes.keys():
        score_dict[uid] = len([like for like in friends_likes[uid] if str(like['category']) in RESTAURANT_CATEGORIES])
    return sorted(score_dict.keys(), key=score_dict.get, reverse=True)

def music_ranks(graph, friends_likes):
    score_dict = {}
    for uid in friends_likes.keys():
        score_dict[uid] = len([like for like in friends_likes[uid] if str(like['category']) in MUSIC_CATEGORIES])
    return sorted(score_dict.keys(), key=score_dict.get, reverse=True)


def political_score(facebook_id, graph):
    ''' Returns a score describing poltitical beliefs
    Postitive score means left-leaning,
    Negative score means right-leaning
    '''
    score = 0

    # First, see if person has indicated political status
    person = graph.get_object(facebook_id)
    if 'political' in person:
        political = person['political']
        if political in ['Liberal', 'Democrat']:
            score += 3
        elif political in ['Conservative', 'Republican', 'Libertarian']:
            score -= 3

    # Then, look at their likes
    likes = graph.get_connections(facebook_id, "likes")
    politicians = get_politicians(likes)

    for p in politicians:
        if p['name'] in LIBERALS:
            score += 1
        if p['name'] in CONSERVATIVES:
            score -= 1 

    return score

def sports_score(facebook_id, graph):
    ''' Returns a score describing the intensity of how much
    a person likes sports.
    Right now, it does this pretty naively but it probably does the job.
    '''
    score = 0

    # First, see if person has indicated sports interests
    person = graph.get_object(facebook_id)
    if 'favorite_teams' in person:
        score += len(person['favorite_teams'])

    if 'favorite_athletes' in person:
        score += len(person['favorite_athletes'])

    if 'sports' in person:
        score += len(person['sports'])

    sports_likes = get_sports_likes(graph.get_connections(facebook_id, "likes"))
    score += len(sports_likes)

    return score

def books_score(facebook_id, graph):
    '''Returns a score describing the intensity of how much
    a person likes books'''
    return len(get_books_likes(graph.get_connections(facebook_id, "likes") ) )

def games_score(facebook_id, graph):
    '''Returns a score describing the intensity of how much
    a person likes books'''
    return len(get_games_likes(graph.get_connections(facebook_id, "likes") ) )

def restaurants_score(facebook_id, graph):
    '''Returns a score describing the intensity of how much
    a person likes books'''
    return len(get_restaurants_likes(graph.get_connections(facebook_id, "likes") ) )

def music_score(facebook_id, graph):
    '''Returns a score describing the intensity of how much
    a person likes books'''
    return len(get_music_likes(graph.get_connections(facebook_id, "likes") ) )

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


LIBERALS = [
    'Barack Obama',
    'Bill Clinton',
    'Joe Biden',
    'Al Franken',
    'Cory Booker',
    'Al Gore',
    'Hillary Clinton',
    'Elizabeth Warren',
    'Nancy Pelosi',
    'Harry Reid',
    'President Bill Clinton',
]

CONSERVATIVES = [
    'Mitt Romney',
    'Arnold Schwarzenegger',
    'Paul Ryan VP',
    'Sarah Palin',
    'George W. Bush',
    'Mike Huckabee',
    'Ron Paul',
    'John McCain',
    'Herman Cain',
    'Michelle Bachmann',
    'Paul Ryan',
    'Scott Brown',
    'Newt Gingrich',
    'Ronald Reagan',
    'Rick Perry',
    'Rick Santorum',
    'Chris Christie',
    'Marco Rubio,'
]

BOOK_CATEGORIES = [
    'Book',
    'Author',
    'Book Store',
    'Library',
    'Magazine',
]

GAME_CATEGORIES = [
    'Games/Toys',
    'Games',
    'Book Store',
    'Library',
    'Magazine',
    'App',
]

MUSIC_CATEGORIES = [
    'Music',
    'Band',
    'Musician',
    'Musician/Band',
    'Musical Instrument',
    'Song',
    'Album',
    'Concert Tour',
    'Playlist',
]

RESTAURANT_CATEGORIES = [
    'Restaurant',
    'Restaurant/cafe',
    'Food/Beverages',
    'Food',
    'Asian Restaurant',
    'Fine Dining Restaurant',
    'Dessert Restaurant',
    'Pub',
    'Italian Restaurant',
    'Mexican Restaurant',
    'Mediterranean Restaurant',
    'Steakhouse',
]

SPORTS_CATEGORIES = [
    'Professional sports team',
    'Sport',
    'Athlete',
    'Sports League',
    'Coach',
]