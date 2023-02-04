import igraph as ig
import matplotlib.pyplot as plt


g = ig.Graph(edges = [(0, 1), (1, 2), (2, 3)])
ig.plot(g)
