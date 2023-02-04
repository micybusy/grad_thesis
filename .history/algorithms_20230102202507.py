import igraph as ig
import matplotlib.pyplot as plt


nodes = []
edges = []
labels = []
while inp != '-':
    if inp == '-':
        break
    inp = input('Enter a node:')
    nodes.append(inp)
    edge = 0
    while edge!= '-' and inp != '-':
        if edge == '-':
            break
        edge = input('Enter an connection for this node:')
        edges.append([inp, edge])




g = ig.Graph(n= 3, edges = )
g.vs["name"] = ["Daniel Morillas", "Kathy Archer", "Kyle Ding", "Joshua Walton"]


fig, ax = plt.subplots(figsize=(5,5))
ig.plot(g, target= ax ,vertex_label = g.vs["name"])
plt.show()