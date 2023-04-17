import igraph as ig
import matplotlib.pyplot as plt
from algorithms import dfs
from samples import sample1

def generate_with_input():
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

        mapp_rev = {v:k for k, v in mapp.items()}

    g = ig.Graph(n = len(mapp), edges = conns, directed = True)
    g.vs["name"] = list(mapp.keys())
    fig, ax = plt.subplots(figsize=(5,5))
    ig.plot(g, target= ax, vertex_label = g.vs["name"])
    plt.show()


sample1 = sample1()
fig, ax = plt.subplots(figsize=(8,8))
ig.plot(sample1, target= ax, vertex_label = sample1.vs['name'])
plt.show()    


print(dfs(sample1, 1))
