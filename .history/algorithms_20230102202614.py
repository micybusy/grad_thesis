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
    label = input('Enter a label for this node:')
    labels.append(label)
    edge = 0
    while edge!= '-' and inp != '-':
        if edge == '-':
            break
        edge = input('Enter a connection for this node:')
        edges.append([inp, edge])




g = ig.Graph(n= len(nodes), edges = edges)
g.vs["name"] = labels


fig, ax = plt.subplots(figsize=(5,5))
ig.plot(g, target= ax ,vertex_label = g.vs["name"])
plt.show()