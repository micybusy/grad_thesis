from samples import weighted, complex
from genesis import plotter, generate_with_input
import igraph as ig
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
    mst_edges = []
    mst_named = []
    weights = []
    cost = 0
    for edge in source_target:
        source, target, weight = edge
        if not (visited[source] and visited[target]):
            mst_edges.append([source, target, weight])
            weights.append(weight)
            mst_named.append((graph.vs[source]['name'], graph.vs[target]['name']))
            visited[source] = True
            visited[target] = True
            cost += weight
        else:
            continue

    mst = ig.Graph(edges = mst_edges)
    return path, cost



plotter(complex(), True)
print(kruskal(complex()))