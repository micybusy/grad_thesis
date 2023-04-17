import igraph as ig
import matplotlib.pyplot as plt
from algorithms import dfs
from samples import connected, disconnected, consecutive

def generate_with_input(directed = False, weighted = False):
    inp = ''
    edge = ''
    mapp = {}
    counter = 0
    conns = []
    weights = []
    while inp != 'exit':
        inp = input('Enter a node: ')
        print(inp)
        if inp == 'exit':
            print(inp)
            break
        if inp not in mapp and inp != 'exit':
            mapp[inp] = counter
            counter += 1
        while edge != 'exit':
            edge = input('Enter an edge for this node: ')
            if edge == 'exit':
                print(inp)
                edge = ''
                break
            if weighted:
                weight = input('Enter a weight for this edge: ')
                weights.append(float(weight))
            if edge not in mapp:
                mapp[edge] = counter
                counter += 1
            print(inp)
            conns.append([mapp[inp], mapp[edge]])
        print(inp)
        g = ig.Graph(n = len(mapp), edges = conns, directed = directed)
        g.vs['name'] = list(mapp.keys())
        if weighted:
            g.es['weight'] = weights
        return g


def plotter(graph):
    fig, ax = plt.subplots(figsize=(8,8))
    ig.plot(graph, target= ax, vertex_label = graph.vs['name']), 
    plt.show()    



#x = generate_with_input(False, False)
#plotter(x)
#y = generate_with_input(True, False)
#plotter(y)
generate_with_input(True, True)