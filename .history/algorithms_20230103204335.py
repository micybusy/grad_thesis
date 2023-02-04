global tail
tail = []
global marked
marked = {}
def dfs(graph, v):
    tail.append(v)
    marked[v] = True
    nachbarn = graph.neighbors(v)
    if nachbarn and not marked[v]:
        for w in nachbarn:
            dfs(graph, w)
    return tail