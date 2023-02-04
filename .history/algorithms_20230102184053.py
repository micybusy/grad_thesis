from graph import Graph
from graph.visuals import plot_2d

inp = 0
g = Graph()
while inp != '-':
    inp = input('Enter a node:')
    if inp == '-':
        break
    g.add_node(inp)
    edge = 0
    while edge!= '-' and inp != '-':
        if edge == '-':
            break
        edge = input('Enter an edge for this node:')
        g.add_edge(inp, edge)

#plot = plot_2d(g)
#plot.show()
print(g.nodes())
print(g.edges())
print(g.node('1'))