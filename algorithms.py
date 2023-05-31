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
    articulation_points_named = []
    for vertex in vertices:
        x = graph.copy()
        x.delete_vertices(vertex)
        if not x.is_connected():
            articulation_points_named.append(graph.vs[vertex]['name'])
            articulation_points.append(vertex)

    graph_aps = graph.copy()
    for v in graph_aps.vs:
        if v['name'] in articulation_points_named: 
            v['color'] = 'yellow'
    
    return graph_aps, articulation_points_named, articulation_points

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
    
    bridged_graph = graph.copy()
    for edge in bridged_graph.es:
        st = (edge.source, edge.target)
        ts = (edge.target, edge.source)
        if st in bridges or ts in bridges:
            edge['color'] = 'green'

    bridges_named = [[graph.vs[t[0]]['name'], graph.vs[t[1]]['name']] for t in bridges]
    return bridges_named, bridged_graph


def biconnected_components(graph):
    _, _, points = articulation_point(graph)
    bicons = []
    if not points:
        print("There are no biconnected components on this graph.")
        return
    for point in points:
        x = graph.copy()
        x.delete_vertices(point)
        bicons.append(x)
    return bicons



def ddfs(graph, v, tail = [], edges = []):
    if v not in tail:
        nachbarn = graph.neighbors(v, 'out')
        tail.append(v)
        for vertex in nachbarn:
            edges.append((v, vertex))
            ddfs(graph, vertex, tail, edges)
    copy = graph.copy()
    for edge in copy.es:
        tmp = (edge.source, edge.target)
        if tmp in edges:
            edge['color'] = "green"
    return tail, copy

def reverse(graph):
    redges = [(edge.target, edge.source) for edge in graph.es()]
    rgraph = ig.Graph(edges = redges, directed = graph.is_directed())
    rgraph.vs['name'] = graph.vs['name']
    return rgraph

def strongly_connected_components(graph):
    if not graph.is_directed():
        return "This search requires a directed graph, the input was not directed."
    else:
        return graph.clusters(mode = "strong").subgraphs()
        


def topological_sort(graph):
    if not graph.is_directed():
        return "This search requires a directed graph, the input was not directed."
    elif not graph.is_dag():
        return "This search requires an acyclic graph, the input was cyclic."
    else:
        vertices = [vertex.index for vertex in list(graph.vs())]
        start_nodes = []
        for v in vertices:
            if not graph.neighbors(v, 'in'):
                start_nodes.append(v)

        def visit(node, visited = [], edges = {}, count = 1):
            nachbarn = graph.neighbors(node, 'out')
            if not nachbarn:
                return visited, edges
            if not node in visited:
                visited.append(node)
            for v in nachbarn:
                edges.update({(node, v): count})
                count +=1
            visited.extend(nachbarn)
            for v in nachbarn:
                visit(v, visited, edges, count)
            return visited, edges
        
        ret_graphs = []
        for node in start_nodes:
            x = visit(node, [], {}, 1)
            visits, edges = x
            copy = graph.copy()
            for edge in copy.es:
                (a, b) = (edge.source, edge.target)
                if (a, b) in edges.keys():
                    edge['label'] = edges.get((a, b))
            visits = [graph.vs[vertex]['name'] for vertex in visits]
            ret_graphs.append([visits, copy])
        return ret_graphs

def hamiltonian_path(graph):
    if graph.is_directed():
        return "Hamiltonian path is limited to undirected graphs, but the input is directed."
    
    def visit(node, visited =[], edges = []):
        if len(visited) == len(graph.vs):
            return visited, edges
        else:
            n = [v for v in graph.neighbors(node) if v not in visited]
            if n:
                visited.append(node)
                for vertex in n:
                    edges.append((node, vertex))
                    visit(vertex, visited, edges)

            else:
                visited.append(node)
                if len(visited) != len(graph.vs):
                    raise Exception
                        
        return visited, edges


    nodes = [vertex.index for vertex in graph.vs]
    paths = []
    for node in nodes:
        try:
            x, y = visit(node, [], [])
            x = '->'.join([graph.vs[item]["name"] for item in x])
            copy = graph.copy()
            for edge in graph.es:
                a,b= edge.source, edge.target
                if (a,b) in y:
                    edge['label'] = y.index((a, b)) + 1
                    edge['color'] = "red"
                elif (b,a) in y:
                    edge['label'] = y.index((b, a)) + 1
                    edge['color'] = "red"
            paths.append((x, copy))

        except:
            pass

    return paths
        


"""
Hamiltonian Path
Min-cut, Maximum flow
Minimum Cost Maximum Flow (ford fulkerson)
heap sort(algo comp sf. 36, 38)
ford fulkerson
floyd warshall 
Flood-fill Algorithm --needs grid and two dimensional graph with directions

"""