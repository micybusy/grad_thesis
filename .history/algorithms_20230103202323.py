def dfs(graph, v):
    marked = len(graph.vs)*[False]
    edges = graph.get_edgelist()
    start_node = graph.vs[v].index
    return edges