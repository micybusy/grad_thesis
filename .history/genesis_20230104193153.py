import igraph as ig
import matplotlib.pyplot as plt
from algorithms import dfs
from samples import connected, disconnected, consecutive


def generate_with_input(directed = False, weighted = False):

    '''
    This function takes user input as node names and edges and returns a graph object. 
    It is also up to the user to decide whether the returned graph is a directed and/or weighted one.
    If the graph is directed, the order in which the inputs are given matter. For example,
    if the user decides "A" to be a main node and tells the program that there exists an edge to "B" from "A",
    the direction of the edge is going to be from A to B (A -> B), not vice versa. If the opposite case is desired,
    the user must also declare "B" as a main node and establish an edge between "B" and "A".
    Type 'exit' as a node name to complete the construction.
    Type 'exit' as an edge name to move on to the next node.
    For a weighted graph, all weights must be assessed before completing the graph, so termination is not possible if
    there exists an edge without a weight. The program will insist on this weight to be declared. 
    
    Notes: 
    - Edges in the opposite directions betweeen two nodes can co-exist (A -> B and A <- B)
    - Multiple edges between two nodes can co-exist (declaring edges [A->B, A->B, A->B] means there is 
      going to be three edges from A to B.)
    - Weights of the edges, of course, must be numeric.
    - Node names are case sensitive and any number given as a node name will be converted to literal, 
      which means no calculation can be done via node names (also, it is not recommended to name nodes numerically
      as each node has a positive integer ID and numerical naming in this case can lead to confusion).

    input: directed, weighted = Bool, Bool
    output: g = igraph.Graph object
    ''' 

    inp = ''
    edge = ''
    mapp = {}
    counter = 0
    conns = []
    weights = []

    print(f"Generating Graph... (directed = {directed}, weighted = {weighted})")
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
                while True:
                    try:
                        weight = input('Enter a weight for this edge: ')
                        weights.append(float(weight))
                        break
                    except:
                        print('Weight must be a number.')
            if edge not in mapp:
                mapp[edge] = counter
                counter += 1
            conns.append([mapp[inp], mapp[edge]])

    g = ig.Graph(n = len(mapp), edges = conns, directed = directed)
    g.vs['name'] = list(mapp.keys())
    if weighted:
        g.es['weight'] = weights
    return g


def plotter(graph):
    _, ax = plt.subplots(figsize=(8,8))
    ig.plot(graph, target= ax, vertex_label = graph.vs['name']), 
    plt.show()    



x = generate_with_input(False, False)
plotter(x)