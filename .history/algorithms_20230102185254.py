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
        edge = input('Enter an edge for this node:')
        if edge == '-':
            break
        g.add_edge(inp, edge, bidirectional= True)

#plot = plot_2d(g)
#plot.show()
print(g.to_list())
print(g.edges())