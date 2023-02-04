import igraph as ig
import matplotlib.pyplot as plt


nodes = []
edges = []
labels = []
inp = ''
mapp = {}
counter = 0
while inp != 'exit':






g = ig.Graph(n= len(nodes), edges = edges)
g.vs["name"] = labels


fig, ax = plt.subplots(figsize=(5,5))
ig.plot(g, target= ax ,vertex_label = g.vs["name"])
plt.show()