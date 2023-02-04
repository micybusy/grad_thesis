from samples import *
from genesis import plotter, generate_with_input
import igraph as ig
from copy import copy
def dfs(graph, v,  tail = [], weighted = False):
    tail.append(v)
    nachbarn = graph.neighbors(v)
    if nachbarn:
        for w in nachbarn:
            if w not in tail:
                dfs(graph, w, tail, weighted)
    edges = [(edge.source, edge.target) for edge in graph.es]
    path = []
    for ix, item in enumerate(tail):
        if ix == len(tail)-1:
            break
        pair = (item, tail[ix+1])
        if pair in edges:
            path.append(pair)
        else:
            temp = ix
            while True:
                if (tail[temp], tail[ix+1]) in edges:
                    path.append((tail[temp], tail[ix+1]))
                    break
                else:
                    temp -= 1
    dfs_tree = ig.Graph(edges = path)
    dfs_tree.vs['name'] = [graph.vs[vertex.index]['name'] for vertex in dfs_tree.vs]
    if weighted:
        for edge in dfs_tree.es:
            certain = [item['weight'] for item in graph.es if (item.source, item.target) == (edge.source, edge.target)]
            edge['weight'] = certain[0]

    path = [(graph.vs[item[0]]['name'], graph.vs[item[1]]['name']) for item in path]
    return path, dfs_tree


def directed_dfs():
    pass

def kruskal(graph):
    if not graph.is_connected():
        print("The graph must be connected in order for Kruskal's algorithm to work.")
        return
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
    if not graph.is_connected():
        print("The graph must be connected in order for Dijkstra's algorithm to work.")
    source_name = graph.vs[source]['name']
    target_name = graph.vs[target]['name']
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
                    try:
                        direct_cost = weights[(neighbor, source)]
                    except:
                        direct_cost = float('inf')

                if relative_cost >= direct_cost:
                    distances[neighbor] = [direct_cost, source]
                else:
                    distances[neighbor] = [relative_cost, node]
        x = unvisited.pop(unvisited.index(node))
        visited.append(x)
    path = []
    cost = 0
    while True:
        dest = target
        step, target = distances[dest]
        cost += step
        path.append(dest)
        if not target:
            break

    path.append(source)
    path = " -> ".join(reversed([graph.vs[node]['name'] for node in path]))
    path = f'Path from {source_name} to {target_name} is {path} with a cost of {cost}.'
    return path


def articulation_point(graph):
    vertices = [vertex.index for vertex in list(graph.vs())]
    articulation_points = []
    for vertex in vertices:
        x = graph.copy()
        x.delete_vertices(vertex)
        if not x.is_connected():
            articulation_points.append(graph.vs[vertex]['name'])
                
    return articulation_points

def find_bridges(graph):
    edges = [(edge.source, edge.target) for edge in list(graph.es())]
    num_clusters = len(graph.connected_components())
    plotter(graph)
    bridges = []
    for edge in edges:
        x = graph.copy()
        x.delete_edges(edge)
        if len(x.connected_components()) != num_clusters:
            bridges.append(edge)
    if not bridges:
        print("There are no bridges on this graph.")
        return
    return bridges


def biconnected_components(graph):
    points = articulation_point(graph)
    bicons = []
    if not points:
        print("There are no biconnected components on this graph.")
        return
    for point in points:
        x = graph.copy()
        x.delete_vertices(point)
        bicons.append(x)
    return bicons


def strongly_connected_components(graph):
    if not graph.is_directed():
        print("This search requires a directed graph, the input was not directed.")
        return
    vertices = [vertex.index for vertex in graph.vs]
    edges = [(edge.source, edge.target) for edge in graph.es]
    outer = {}
    inner = {}
    for vertex in vertices:
        outer[vertex] = graph.neighbors(vertex, 'out')
        inner[vertex] = graph.neighbors(vertex, 'in')
    return nachbarn


ret = strongly_connected_components(wcomplex(directed=True))
print(ret)
plotter(wcomplex(directed=True))