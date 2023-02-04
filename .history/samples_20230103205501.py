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