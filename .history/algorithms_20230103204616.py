global tail
tail = []
global marked
marked = {}
def dfs(graph, v):
    tail.append(v)
    nachbarn = graph.neighbors(v)
    if nachbarn:
        for w in nachbarn:
            dfs(graph, w)
    else:
        break
    return tail