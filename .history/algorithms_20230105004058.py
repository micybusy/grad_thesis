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
    visited  = {vertex.index: False for vertex in graph.vs}
    weights = {edge: weight for edge in graph.get_edgelist() for weight in graph.es['weight']}
    while True:
        if all(visited.values()):
            break
        dummy = {k: v for k, v in distances.items() if not visited[k]}
        node = next(iter(sorted(dummy, key = lambda x:  distances[x][0])))
        nachbarn = graph.neighbors(node)
        for neighbor in nachbarn:
            x = {graph.vs[k]['name']: [v[0], graph.vs[v[1]]['name']] for k, v in distances.items() if v[1] != None}
            print(x)
            try:
                if distances[neighbor][0] == float('inf'):
                    distances[neighbor][0] = weights[(node, neighbor)]
                else:
                    distances[neighbor][0] += weights[(node, neighbor)]
                distances[neighbor][1] = node
            except:
                continue
        
        visited[node] = True

    path = []
    cost = 0
    while target:
        path.append(graph.vs[target]['name'])
        dist, dest = distances[target]
        cost += dist
        target = dest
        
    return distances

#plotter(wcomplex2(), True)
print(dijkstra(wcomplex2(), 0, 4))