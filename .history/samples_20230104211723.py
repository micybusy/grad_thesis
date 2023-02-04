import igraph as ig
def connected():
    edges = [[0, 1], [1, 2], [0, 3], [3, 1]]
    g = ig.Graph(n = 4, edges = edges)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g

def disconnected():
    edges = [[0, 1], [1, 2], [0, 3], [3, 1], [4, 5], [5, 7]]
    g = ig.Graph(n = 4, edges = edges)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g

def consecutive():
    edges = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
    g = ig.Graph(n = 4, edges = edges)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g

def weighted():
    edges = [[0, 1], [1, 2], [0, 3], [3, 1]]
    weights = [1, 2, 3, 4]
    g = ig.Graph(n = 4, edges = edges)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g