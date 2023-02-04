from graph import Graph
from graph.visuals import plot_2d

inp = 0
g = Graph()
while inp != -1:
    inp = int(input('Enter a node:'))
    if inp == -1:
        break
    #g.add_node(inp)
    edge = 0
    while edge!= -1 and inp != -1:
        edge = int(input('Enter an edge for this node:'))
        if edge == '-':
            break
        g.add_node((inp, edge))

plot = plot_2d(g)
plot.show()
#print(g.nodes())
#print(g.edges())