from graph import Graph

inp = 0
g = Graph()
while inp != '-':
    inp = input('Enter a node:')
    g.add_node(inp)
    edge = 0
    while edge!= '-':
        edge = input('Enter an edge for this node:')
        g.add_edge(inp, edge)

print(g)
