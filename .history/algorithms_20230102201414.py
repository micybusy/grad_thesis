import igraph as ig
import matplotlib.pyplot as plt


g = ig.Graph(edges = [(0, 1), (1, 2), (2, 3)])
fig, ax = plt.subplots(figsize=(5,5))
ig.plot(g)
plt.show()