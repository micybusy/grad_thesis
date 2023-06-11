from samples import *
import igraph as ig
import pandas as pd


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
    for ix, item in enumerate(vids):
        if ix != len(vids) - 1:
            path.append((item, vids[ix + 1]))

    dfs_tree = ig.Graph(edges=path)
    dfs_tree.vs["name"] = [graph.vs[vertex.index]["name"] for vertex in dfs_tree.vs]
    named_path = " -> ".join([graph.vs[idx]["name"] for idx in vids])
    return named_path, dfs_tree


def kruskal(graph):
    """
    This function computes a Minimum Spanning Tree of the graph using Kruskal's Algorithm
    """

    if not graph.is_connected():
        return
    source_target = [(edge.source, edge.target, edge["weight"]) for edge in graph.es]
    source_target = sorted(source_target, key=lambda x: x[2])
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
            mst_named.append((graph.vs[source]["name"], graph.vs[target]["name"]))
            visited[source] = True
            visited[target] = True
            cost += weight

    mst = ig.Graph(edges=mst_edges)
    mst.vs["name"] = [graph.vs[vertex.index]["name"] for vertex in mst.vs]
    mst.es["weight"] = weights
    return cost, mst, mst_named


def dijkstra(graph, source, target):
    try:
        graph.es["weight"]
    except:
        return "The graph must be weighted in order for Dijkstra's algorithm to work."

    if (type(source), type(target)) == (int, int):
        ret = graph.get_shortest_paths(
            source, to=target, weights=graph.es["weight"], output="epath"
        )
        if ret[0]:
            c = graph.copy()
            cost = 0
            for edge in ret[0]:
                c.es.select(edge)["color"] = "red"
                cost += c.es.select(edge)["weight"][0]
            return c, cost
        else:
            return f"""A path could not be found from 
                    {graph.vs.select(source)['name'][0]} to 
                    {graph.vs.select(target)['name'][0]}."""

    else:
        return


def articulation_point(graph):
    vertices = [vertex.index for vertex in list(graph.vs())]
    articulation_points = []
    articulation_points_named = []
    for vertex in vertices:
        x = graph.copy()
        x.delete_vertices(vertex)
        if not x.is_connected():
            articulation_points_named.append(graph.vs[vertex]["name"])
            articulation_points.append(vertex)

    graph_aps = graph.copy()
    for v in graph_aps.vs:
        if v["name"] in articulation_points_named:
            v["color"] = "yellow"

    return graph_aps, articulation_points_named, articulation_points


def find_bridges(graph):
    edges = [(edge.source, edge.target) for edge in list(graph.es())]
    num_clusters = len(graph.connected_components())
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
            edge["color"] = "green"

    bridges_named = [[graph.vs[t[0]]["name"],
                       graph.vs[t[1]]["name"]] for t in bridges]
    return bridges_named, bridged_graph


def biconnected_components(graph):
    _, _, points = articulation_point(graph)
    bicons = []
    if not points:
        return
    for point in points:
        x = graph.copy()
        x.delete_vertices(point)
        bicons.append(x)
    return bicons


def ddfs(graph, v, tail=[], edges=[]):
    if v not in tail:
        nachbarn = graph.neighbors(v, "out")
        tail.append(v)
        for vertex in nachbarn:
            edges.append((v, vertex))
            ddfs(graph, vertex, tail, edges)
    copy = graph.copy()
    for edge in copy.es:
        tmp = (edge.source, edge.target)
        if tmp in edges:
            edge["color"] = "green"
    return tail, copy


def reverse(graph):
    redges = [(edge.target, edge.source) for edge in graph.es()]
    rgraph = ig.Graph(edges=redges, directed=graph.is_directed())
    rgraph.vs["name"] = graph.vs["name"]
    return rgraph


def strongly_connected_components(graph):
    if not graph.is_directed():
        return "This search requires a directed graph, the input was not directed."
    else:
        return graph.clusters(mode="strong").subgraphs()


def topological_sort(graph):
    if not graph.is_directed():
        return "This search requires a directed graph, the input was not directed."
    elif not graph.is_dag():
        return "This search requires an acyclic graph, the input was cyclic."
    else:
        vertices = [vertex.index for vertex in list(graph.vs())]
        start_nodes = []
        for v in vertices:
            if not graph.neighbors(v, "in"):
                start_nodes.append(v)

        def visit(node, visited=[], edges={}, count=1):
            nachbarn = graph.neighbors(node, "out")
            if not nachbarn:
                return visited, edges
            if not node in visited:
                visited.append(node)
            for v in nachbarn:
                edges.update({(node, v): count})
                count += 1
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
                    edge["label"] = edges.get((a, b))
            visits = [graph.vs[vertex]["name"] for vertex in visits]
            ret_graphs.append([visits, copy])
        return ret_graphs


def hamiltonian_path(graph):
    if graph.is_directed():
        return "Hamiltonian path is limited to undirected graphs, but the input is directed."

    def visit(node, visited=[], edges=[]):
        if len(visited) == len(graph.vs):
            return visited, edges
        else:
            n = [v for v in graph.neighbors(node) if v not in visited]
            if n:
                visited.append(node)
                for vertex in n:
                    if vertex not in visited:
                        edges.append((node, vertex))
                        visit(vertex, visited, edges)

            else:
                visited.append(node)
                if len(visited) != len(graph.vs):
                    raise Exception

        return edges

    nodes = [vertex.index for vertex in graph.vs]
    paths = []
    for node in nodes:
        try:
            y = visit(node, [], [])
            x = []
            copy = graph.copy()
            for ix, edge in enumerate(y):
                x.extend(list(edge))
                e = copy.es.select(_source_in=[edge[0]], _target_in=[edge[1]])
                e["color"] = "red"
                e["label"] = ix + 1

            x = list(dict.fromkeys(x))
            x = "->".join([graph.vs[item]["name"] for item in x])
            paths.append((x, copy))

        except:
            pass

    return paths


def ford_fulkerson(graph, source=0, target=0):
    if not graph.is_directed():
        return "Ford-Fulkerson algorithm requires a directed graph."
    try:
        graph.es["weight"]
    except:
        return "Ford-Fulkerson algorithm requires a weighted graph."
    if not graph.copy().as_undirected().is_connected():
        return "Ford-Fulkerson algorithm requires a connected graph."

    try:
        c = graph.copy()
        ret = c.maxflow(source=source, target=target, capacity=c.es["weight"])
        for ix, val in enumerate(ret.flow):
            c.es[ix]["weight"] = int(val)
            if val != 0:
                c.es[ix]["color"] = "green"
            else:
                c.es[ix]["color"] = "gray"
        c2 = graph.copy()
        min_cut = [(e.source, e.target) for e in ret.es]
        for edge in c2.es():
            if (edge.source, edge.target) not in min_cut:
                edge["color"] = "gray"
            else:
                edge["color"] = "yellow"
        txt = f"Maximum flow for this setting is {int(ret.value)}."
        return txt, c, c2

    except:
        return None, None, None


def all_shortest_paths(graph):
    found = pd.DataFrame(columns=graph.vs["name"], index=graph.vs["name"])
    for v1 in graph.vs:
        found[v1["name"]] = {}
        for v2 in graph.vs:
            ret = dijkstra(graph, v1.index, v2.index)
            if v1 == v2:
                found[v1["name"]][v2["name"]] = 0
            elif type(ret) == str:
                found[v1["name"]][v2["name"]] = "INF"
            else:
                found[v1["name"]][v2["name"]] = ret[1]
    return found.T

