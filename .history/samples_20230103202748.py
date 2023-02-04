import igraph as ig

def sample1():
    edges = [[0, 1], [1, 2], [0, 3], [3, 1]]
    g = ig.Graph(n = 4, edges = edges)
    g.vs['name'] = [str(vertex.index) for vertex in g.vs]
    return g