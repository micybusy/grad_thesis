import igraph as ig
import matplotlib.pyplot as plt


g = ig.Graph(n= 3, edges = [[0, 1], [1, 2], [2, 3]], directed = True)
g.vs["name"] = ["Daniel Morillas", "Kathy Archer", "Kyle Ding", "Joshua Walton"]

fig, ax = plt.subplots(figsize=(5,5))
ig.plot(g)
plt.show()