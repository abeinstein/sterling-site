import json
import facebook
import urllib2

LIBERALS = [
'Barack Obama',
'Bill Clinton',
'Joe Biden',
'Al Franken',
'Cory Booker',
'Al Gore'
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
'Rick Santorum'
]



def paging(f):
        ''' Decorator for paging through facebook responses '''
        def inner(response):
            data = []
            while True:
                data.extend(f(response))
                try:
                    response = json.loads(urllib2.urlopen(response["paging"]["next"]).readlines()[0])
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
    categories = [
        'Professional sports team',
        'Sport',
        'Athlete',
        'Sports League',
        'Coach',
    ]
    for like in response['data']:
        if like['category'] in categories:
            sports_likes.append(like)

    return sports_likes

@paging
def get_books_likes(response):
    categories = [
        'Book',
        'Author',
        'Book Store',
        'Library',
        'Magazine',
    ]

    books_likes = [like for like in response['data'] if like['category'] in categories]
    return books_likes

def get_games_likes(response):
    categories = [
        'Games/Toys',
        'Games',
        'Book Store',
        'Library',
        'Magazine',
        'App',
    ]

    games_likes = [like for like in response['data'] if like['category'] in categories]
    return games_likes

def get_restaurants_likes(response):
    categories = [
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

    restaurants_likes = [like for like in response['data'] if like['category'] in categories]
    return restaurants_likes

def get_music_likes(response):
    categories = [
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

    music_likes = [like for like in response['data'] if like['category'] in categories]
    return music_likes


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
