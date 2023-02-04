def dfs(graph, v):
    marked = len(graph.vs)*[False]
    edges = graph.get_edgelist()
    start_node = [vertex.index for vertex in graph.vs if vertex == v]
    return start_node.neighbors