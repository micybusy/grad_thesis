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
        if inp == 'exit':
            break
        if inp not in mapp and inp != 'exit':
            mapp[inp] = counter
            counter += 1
        while edge != 'exit':
            edge = input('Enter an edge for this node: ')
            if edge == 'exit':
                edge = ''
                break
            if weighted:
                weight = input('Enter a weight for this edge: ')
                weights.append(float(weight))
            if edge not in mapp:
                mapp[edge] = counter
                counter += 1
            conns.append([mapp[inp], mapp[edge]])

        g.vs['name'] = [str(vertex.index) for vertex in g.vs]
        return g

def plotter(graph):
    fig, ax = plt.subplots(figsize=(8,8))
    ig.plot(graph, target= ax, vertex_label = graph.vs['name'])
    plt.show()    

