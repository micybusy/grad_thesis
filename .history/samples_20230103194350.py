import igraph as ig
import matplotlib.pyplot as plt


def sample1():
    edges = [[0, 1], [1, 2], [0, 2], [0, 3], [3, 1]]
    g = ig.Graph(n = 5, edges = edges)
    g.vs['name'] = str(vs)
    return g