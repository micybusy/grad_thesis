import igraph as ig
import matplotlib.pyplot as plt

edges = [[0, 1], [1, 2], [0, 2], [0, 3], [3, 1]]
g = ig.Graph(n = 5, edges = edges)