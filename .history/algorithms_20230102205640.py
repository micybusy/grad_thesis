import igraph as ig
import matplotlib.pyplot as plt


inp = ''
edge = ''
mapp = {}
counter = 0
conns = []
while inp != 'exit':
    inp = input('Enter a node: ')
    if inp == 'exit':
        break
    if inp not in mapp and inp != 'exit':
        mapp[inp] = counter
        counter += 1
    while edge != 'exit':
        edge = input('Enter a connection for this node: ')
        if edge == 'exit':
            edge = ''
            break
        if edge not in mapp:
            mapp[edge] = counter
            counter += 1
        conns.append([mapp[inp], mapp[edge]])
        


g = ig.Graph(n= len(mapp), edges = conns, directed = True)
g.vs["name"] = list(mapp.keys())


fig, ax = plt.subplots(figsize=(5,5))
ig.plot(g, target= ax ,vertex_label = g.vs["name"])
plt.show()