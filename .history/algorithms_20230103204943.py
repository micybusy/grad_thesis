def dfs(graph, v, marked = {}, tail = []):
    tail.append(v)
    marked[v] = True
    nachbarn = graph.neighbors(v)
    if nachbarn:
        for w in nachbarn:
            if not marked[w]:
                dfs(graph, w, marked, tail)
            
    return tail