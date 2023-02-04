def dfs(graph, v):
    marked = len(graph.vs)*[False]
    edges = graph.get_edgelist()
    start_node = [item for item in list(graph.vs) if item[1] == v]
    return 