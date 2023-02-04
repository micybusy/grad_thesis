from samples import weighted, wcomplex, wcomplex2, disconnected
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
            mst_edges.append([source, target])
            weights.append(weight)
            mst_named.append((graph.vs[source]['name'], graph.vs[target]['name']))
            visited[source] = True
            visited[target] = True
            cost += weight

    mst = ig.Graph(edges = mst_edges)
    mst.vs['name'] = [graph.vs[vertex.index]['name'] for vertex in mst.vs]
    mst.es['weight'] = weights
    return cost, mst, mst_named


def dijkstra(graph, source, target):
    distances = {vertex.index: [float('inf'), None] for vertex in graph.vs if vertex.index != source}
    distances[source] = [0, None]
    unvisited  = [vertex.index for vertex in graph.vs]
    weights = {edge: weight for edge, weight in zip(graph.get_edgelist(), graph.es['weight'])}
    visited = []
    while True:
        if not unvisited:
            break
        dummy = {k: v for k, v in distances.items() if k in unvisited}
        node = next(iter(sorted(dummy, key = lambda x: dummy[x][0])))
        for neighbor in graph.neighbors(node):
            if neighbor in visited:
                continue
            if distances[neighbor][0] == float('inf'):
                try:
                    distances[neighbor][0] = weights[(node, neighbor)]
                    distances[neighbor][1] = node
                except:
                    distances[neighbor][0] = weights[(neighbor, node)]
                    distances[neighbor][1] = node
            else: 
                try:
                    relative_cost = distances[neighbor][0] + weights[(node, neighbor)]
                except:
                    relative_cost = distances[neighbor][0] + weights[(neighbor, node)]
                
                try:
                    direct_cost = weights[(source, neighbor)]
                except:
                    direct_cost = weights[(neighbor, source)]

                if relative_cost => direct_cost:
                    distances[neighbor] = [direct_cost, source]
                else:
                    distances[neighbor] = [relative_cost, node]


        x = unvisited.pop(unvisited.index(node))
        visited.append(x)
    return distances

# there's a problem with finding distances. try finding it. this should help: https://youtu.be/bZkzH5x0SKU

#plotter(wcomplex2(), True)
print(dijkstra(wcomplex2(), 0, 4))
