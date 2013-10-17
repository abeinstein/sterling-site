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

