import igraph as ig

def connected(directed = False):
    edges = [[0, 1], [1, 2], [0, 3], [3, 1]]
    g = ig.Graph(edges = edges, directed = directed)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g

def disconnected(directed = False):
    edges = [[0, 1], [1, 2], [0, 3], [3, 1], [4, 5], [5, 7]]
    g = ig.Graph(edges = edges, directed = directed)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g

def consecutive(directed = False):
    edges = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
    g = ig.Graph(edges = edges, directed = directed)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g

def weighted(directed = False):
    edges = [[0, 1], [1, 2], [0, 3], [3, 1]]
    weights = [1, 2, 3, 1]
    g = ig.Graph(edges = edges, directed = directed)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    g.es['weight'] = weights
    return g

def wcomplex(directed = False):
    edges = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6],
             [6, 7], [0, 6], [0, 7], [1, 7], [3, 1], [3, 5],
             [3, 7], [5 ,7]]
    weights = [3, 5, 10, 4, 2, 1, 1, 2, 1, 4, 5, 3, 8, 3]
    g = ig.Graph(edges = edges, directed = directed)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    g.es['weight'] = weights
    return g


def wcomplex2(directed = False):
    edges   = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [0, 5],
               [1, 5], [2, 4], [2, 5]]
    weights = [2, 6, 9, 3, 2, 8, 5, 1, 3]

    g = ig.Graph(edges = edges, directed = directed)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    g.es['weight'] = weights
    return g

def wcomplex3(directed = False):
    edges = [[0, 1], [0, 3], [1, 2], [3, 2], [2, 4], [2, 5],
             [4, 5]]
    weights = [1, 2, 3, 4, 5, 6, 7]
    g = ig.Graph(edges = edges, directed = directed)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    g.es['weight'] = weights
    return g

def wcomplex4(directed = False):
    edges = [[0, 1], [0, 2], [0, 3], [1, 2], [3, 4]]
    g = ig.Graph(edges = edges, directed = directed)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g


    