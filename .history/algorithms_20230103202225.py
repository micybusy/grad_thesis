def dfs(graph, v):
    marked = len(graph.vs)*[False]
    edges = graph.get_edgelist()
    start_node = graph.vs[v].index
    starts = [item for item in edges if item[0] == start_node]
    tail = ''
    if len(starts) == 1:
        tail = tail + starts[0][1]
        return tail 
    elif len(starts) == 0:
        return tail
    else:
        print(starts)
        connection = starts.pop()
        tail = tail+dfs(graph, connection[1])
        return tail