# This is where all of the algorithms should go
# Each algorithm should accept two arguments:
# <facebook_id> and <oauth_token>
import facebook

def toy_algorithm(facebook_id, oauth_token):
    return ['100006812678326']

def alphabetical(facebook_id, oauth_token):
    ''' Returns users in an alphabetical list '''
    graph = facebook.GraphAPI(oauth_token)
    friends = graph.get_connections("me", "friends")

    sorted_friends = sorted(friends['data'], key=lambda d: d['name'])
    return [d['id'] for d in sorted_friends]

# def beinstein_1(facebook_id, oauth_token):
#     ''' My first attempt at a fancy algorithm '''
#     graph = facebook.GraphAPI(oauth_token)

def splash_site(facebook_id, oauth_token):
    people = [
        'adamt.gluck',
        'andrew.beinstein',
        'zuck',
        'gc2maxpro',
        'gurevitch',
        'barackobama',
        'lossip',
        'emmie.schlessinger',
        'shreya.luthra',
        'brett.parket',
        'michael.warren.5220',
        '742541343']
    return people

def mutual_friends(facebook_id, oauth_token):
    '''Sorts friends by the mutual friend count'''
    '''Runs at EWess speed'''
    graph = facebook.GraphAPI(oauth_token)
    friends = graph.fql('''SELECT uid, mutual_friend_count 
                            FROM user WHERE uid IN 
                            (SELECT uid1 FROM friend WHERE uid2 = me()) 
                            ORDER BY mutual_friend_count DESC''')

    return [d['uid'] for d in friends]






