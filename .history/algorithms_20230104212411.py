from samples import weighted
from igraph import Edge
def dfs(graph, v,  tail = []):
    tail.append(v)
    nachbarn = graph.neighbors(v)
    if nachbarn:
        for w in nachbarn:
            if w not in tail:
                dfs(graph, w, tail)
    return tail


def kruskal(graph):
    source_target = []
    for edge in graph.es:
        source_target.append({edge.source: edge.target})
    return source_target
print(kruskal(weighted()))