from samples import weighted
from genesis import plotter
def dfs(graph, v,  tail = []):
    tail.append(v)
    nachbarn = graph.neighbors(v)
    if nachbarn:
        for w in nachbarn:
            if w not in tail:
                dfs(graph, w, tail)
    return tail


def kruskal(graph):
    source_target = [(edge.source, edge.target, edge['weight']) for edge in graph.es]
    source_target = sorted(source_target, key = lambda x: x[2])
    visited = {vertex.index: False for vertex in graph.vs}
    path = []
    cost = 0
    for edge in source_target:
        source, target, weight = edge
        if not (visited[source] and visited[target]):
            path.append((source, target))
            visited[source] = True
            visited[target] = True
            cost += weight
        else:
            continue
    return path, weight



plotter(weighted(), False)
print(kruskal(weighted()))