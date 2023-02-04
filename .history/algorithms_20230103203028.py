def dfs(graph, v):
    marked = {vertex.index: False  for vertex in graph.vs}
    edges = graph.get_edgelist()
    start_node = graph.vs[v].index
    tail = ''
    return marked