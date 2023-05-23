from samples import *
from genesis import plotter, generate_with_input
import igraph as ig

def dfs(graph, v):
        nv = graph.vcount()
        added = [False for v in range(nv)]
        left_nodes = []
        vids = []
        left_nodes.append((v, graph.neighbors(v)))
        vids.append(v)
        added[v] = True

        while left_nodes:
            v, neighbors = left_nodes[-1]
            if neighbors:
                neighbor = neighbors.pop()
                if not added[neighbor]:
                    left_nodes.append((neighbor, graph.neighbors(neighbor)))
                    vids.append(neighbor)
                    added[neighbor] = True
            else:
                left_nodes.pop()
        path = []
        for  ix, item in enumerate(vids):
            if ix != len(vids) - 1:
                path.append((item, vids[ix+1]))

        dfs_tree = ig.Graph(edges = path)
        dfs_tree.vs['name'] = [graph.vs[vertex.index]['name'] for vertex in dfs_tree.vs]
        named_path = ' -> '.join([graph.vs[idx]['name'] for idx in vids])
        return named_path, dfs_tree

def kruskal(graph):

    '''
    This function computes a Minimum Spanning Tree of the graph using Kruskal's Algorithm
    ''' 

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

    '''
    This function computes the shortest path from a source node to a target node
    with dijkstra's algorithm.
    '''

    if not graph.is_connected():
        return("The graph must be connected in order for Dijkstra's algorithm to work.")
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
    path_str = " -> ".join(reversed([graph.vs[node]['name'] for node in path]))
    path_str = f'Path from {source_name} to {target_name} is {path_str} with a cost of {cost}.'
    path_edges = []
    for ix, item in enumerate(path):
        if ix == len(path) - 1:
            break
        path_edges.append([item, path[ix+1]])

    dijkstra_graph = graph.copy()
    for edge in dijkstra_graph.es:
        st = [edge.source, edge.target]
        ts = [edge.target, edge.source]
        if  st in path_edges or ts in path_edges:
            edge['color'] = 'red'


    return path, path_str, dijkstra_graph


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



def ddfs(graph, v, tail = []):
    vertices = [vertex.index for vertex in graph.vs]
    if v not in tail:
        nachbarn = graph.neighbors(v, 'out')
        tail.append(v)
        for vertex in nachbarn:
            ddfs(graph, vertex, tail)
    if set(tail) == set(vertices):
        return tail
    else:
        left = [vertex for vertex in vertices if vertex not in tail]
        for vertex in left:
            ddfs(graph, vertex, tail)

def reverse(graph):
    redges = [(edge.target, edge.source) for edge in graph.es()]
    rgraph = ig.Graph(edges = redges, directed = graph.is_directed())
    rgraph.vs['name'] = graph.vs['name']
    return rgraph

'''def strongly_connected_components(graph):
    if not graph.is_directed():
        print("This search requires a directed graph, the input was not directed.")
        return
    visited = []
    str_dfs = ddfs(graph, 0)[::-1]'''

#print(dfs(wcomplex3(directed= False), 0))
#print(ddfs(scc(), 0))


'''

find a way to measure the finish time of nodes while doing dfs. then follow this tutorial.
https://www.hackerearth.com/practice/algorithms/graphs/strongly-connected-components/tutorial/
''' 

# directed graphs are not recognized as connected. fix it.
# dijkstra does not work for wcomplex