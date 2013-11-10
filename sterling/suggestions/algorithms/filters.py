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



def political_score(facebook_id, oauth_token):
    score = 0
    graph = facebook.GraphAPI(oauth_token)

    # First, see if person has indicated political status
    person = graph.get_object('me')
    if 'political' in person:
        political = person['political']
        if political in ['Liberal', 'Democrat']:
            score += 3
        elif political in ['Conservative', 'Republican', 'Libertarian']:
            score -= 3

    # Then, look at their likes
    likes = graph.get_connections("me", "likes")
    politicians = get_politicians(likes)

    for p in politicians:
        if p['name'] in LIBERALS:
            score += 1
        if p['name'] in CONSERVATIVES:
            score -= 1 # lol

    return score



