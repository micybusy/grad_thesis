def dfs(graph, v):
    marked = len(graph.vs)*[False]
    edges = graph.get_edgelist()
    start_node = graph.vs[v].index
    starts = [item for item in edges if item[0] == start_node]
    tail = ''
    if len(starts) == 0:
        return tail + starts[0][1]
    else:
        print(starts)
        connection = starts.pop()
        return tail+dfs(graph, connection[1])