global tail
tail = []
def dfs(graph, v):
    tail.append[v]
    nachbarn = graph.neighbors(v)
    for w in nachbarn:
        dfs(graph, w)
