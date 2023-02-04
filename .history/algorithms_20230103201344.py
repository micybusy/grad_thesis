def dfs(graph, v):
    marked = len(graph.vs)*[False]
    edges = graph.get_edgelist()
    start_node = [item for item in list(graph.vs) if item.index == v]
    return start_node.index