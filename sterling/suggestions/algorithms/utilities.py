import facebook as fb
import networkx as nx

def mutual_friends_nx_graph(oauth_token, verbose = False):
    fbg = fb.GraphAPI(oauth_token)
    friends = fbg.get_connections("me", "friends")["data"]
    graph = nx.Graph()
    current = 0
    total = len(friends)
    for friend in friends:
        mutualFriends = fbg.fql("SELECT uid1, uid2 FROM friend where uid1=" + friend[u'id'] + "and uid2 in (SELECT uid2 FROM friend where uid1=me())")
        graph.add_edges_from([(x['uid1'], x['uid2']) for x in mutualFriends])
        if (verbose):
            current = current + 1
            print(str(current) + "/" + str(total))

    return graph

#algorithms
def disp(G, ego):
    nbunch = G.neighbors(ego)
    sub = G.subgraph(nbunch)

    disperse = 0
    graph_size = len(sub)
    shortest_paths = nx.shortest_path_length(sub)
    for source in shortest_paths:
        disperse += graph_size - len(shortest_paths[source])
        for target in shortest_paths[source]:
            length = shortest_paths[source][target]
            if length > 1:
                disperse += 1            

    return disperse

def norm(G, ego):
    dispv = disp(G, ego)
    mutv = len(G.neighbors(ego))
    return dispv / (mutv + 10)

def ordered_friends(G):
    ordered = {}
    for node in G.nodes_iter():
        strength = norm(G, node)
        ordered[node] = strength

    return sorted(ordered, key=ordered.get, reverse = True)
