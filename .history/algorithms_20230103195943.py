def dfs(graph, v):
    marked = len(graph.vs)*[False]
    edges = graph.get_edgelist()
    #start_node = [item[0] for item in list(graph.vs) if item[1] == v]
    return list(graph.vs)