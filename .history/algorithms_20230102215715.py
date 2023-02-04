def dfs(graph, v):
    marked = len(graph.vs)*[False]
    edges = graph.get_edgelist()
    ids = g.get_vertex_dataframe().to_dict()
    return ids, marked, edges