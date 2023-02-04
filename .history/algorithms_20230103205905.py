def dfs(graph, v,  tail = []):
    tail.append(v)
    nachbarn = graph.neighbors(v)
    print(v)
    print(nachbarn)
    if nachbarn:
        for w in nachbarn:
            if w not in tail:
                dfs(graph, w, tail)
    return tail