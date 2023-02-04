import igraph as ig
import matplotlib.pyplot as plt


inp = ''
edge = ''
mapp = {}
counter = 0
conns = []
while inp != 'exit':
    inp = input('Enter a node: ')
    if inp not in mapp:
        mapp[inp] = counter
        counter += 1
    while edge != 'exit':
        if edge not in mapp:
            mapp[edge] = counter
            counter += 1
        conns.append(mapp[inp], mapp[edge])
        




g = ig.Graph(n= len(mapp), edges = conns)
g.vs["name"] = mapp.keys()


fig, ax = plt.subplots(figsize=(5,5))
ig.plot(g, target= ax ,vertex_label = g.vs["name"])
plt.show()