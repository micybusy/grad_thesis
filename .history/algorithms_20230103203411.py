def dfs(graph, v):
    tail = []
    tail.append(v)
    nachbarn = graph.neighbors(v)
