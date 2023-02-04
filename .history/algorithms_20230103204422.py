global tail
tail = []
global marked
marked = {}
def dfs(graph, v):
    tail.append(v)
    nachbarn = graph.neighbors(v)
    if nachbarn and (v not in tail):
        for w in nachbarn:
            dfs(graph, w)
    return tail