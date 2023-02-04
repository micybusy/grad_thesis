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
    source_target_named = []
    for edge in graph.es:
        source_target.append((edge.source, edge.target, edge['weight']))
        source_target_named.append((graph.vs[edge.source]['name'], graph.vs[edge.target]['name'], edge['weight']))
    return source_target, source_target_named
print(kruskal(weighted()))