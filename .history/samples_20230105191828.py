import igraph as ig

def connected():
    edges = [[0, 1], [1, 2], [0, 3], [3, 1]]
    g = ig.Graph(edges = edges)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g

def disconnected():
    edges = [[0, 1], [1, 2], [0, 3], [3, 1], [4, 5], [5, 7]]
    g = ig.Graph(edges = edges)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g

def consecutive():
    edges = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 0]]
    g = ig.Graph(edges = edges)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g

def weighted():
    edges = [[0, 1], [1, 2], [0, 3], [3, 1]]
    weights = [1, 2, 3, 1]
    g = ig.Graph(edges = edges)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    g.es['weight'] = weights
    return g

def wcomplex():
    edges = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6],
             [6, 7], [0, 6], [0, 7], [1, 7], [3, 1], [3, 5],
             [3, 7], [5 ,7]]
    weights = [3, 5, 10, 4, 2, 1, 1, 2, 1, 4, 5, 3, 8, 3]
    g = ig.Graph(edges = edges)
    g.vs['name'] = ['X', 'Y', 'Z', 'T', 'S', 'U', 'W', 'V']
    g.es['weight'] = weights
    return g


def wcomplex2():
    edges   = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [0, 5],
               [1, 5], [2, 4], [2, 5]]
    weights = [2, 6, 9, 3, 2, 8, 5, 1, 3]

    g = ig.Graph(edges = edges)
    g.vs['name'] = ['A', 'B', 'E', 'C', 'F', 'D']
    g.es['weight'] = weights
    return g

def wcomplex3():
    edges = [[1, 2], [1, 4], [2, 3], [4, 3], [3, 5], [3, 6],
             [5, 6]]
    weights = [1, 2, 3, 4, 5, 6, 7]
    g = ig.Graph(edges = edges)
    g.vs['name'] = ['A', 'B', 'C', 'D', 'E', 'F']
    g.es['weight'] = weights
    return g