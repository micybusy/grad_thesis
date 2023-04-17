import igraph as ig
import matplotlib.pyplot as plt

while inp != '-':
    if inp == '-':
        break
    inp = input('Enter a node:')
    g.add_node(inp)
    edge = 0
    while edge!= '-' and inp != '-':
        if edge == '-':
            break
        edge = input('Enter an edge for this node:')
        g.add_edge(inp, edge)




g = ig.Graph(n= 3, edges = [[0, 1], [1, 2], [2, 3], [3, 2], [3, 0]])
g.vs["name"] = ["Daniel Morillas", "Kathy Archer", "Kyle Ding", "Joshua Walton"]


fig, ax = plt.subplots(figsize=(5,5))
ig.plot(g, target= ax ,vertex_label = g.vs["name"])
plt.show()