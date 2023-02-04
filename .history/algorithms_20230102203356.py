import igraph as ig
import matplotlib.pyplot as plt


inp = ''
edge = ''
mapp = {}
counter = 0
while inp != 'exit':
    inp = input('Enter a node: ')
    if inp not in mapp:
        mapp[inp] = counter
        counter += 1
        
        




g = ig.Graph(n= len(nodes), edges = edges)
g.vs["name"] = labels


fig, ax = plt.subplots(figsize=(5,5))
ig.plot(g, target= ax ,vertex_label = g.vs["name"])
plt.show()