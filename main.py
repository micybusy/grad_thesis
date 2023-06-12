import tkinter as tk
from algorithms import *
from samples import *
from genesis import *
import igraph as ig
from PIL import ImageTk, Image
import os
import sys
from dataframe_image import export
import matplotlib.pyplot as plt


class UI:
    def __init__(self):
        if not os.path.exists(os.path.join(os.getcwd(), "out_graphs")):
            os.mkdir(os.path.join(os.getcwd(), "out_graphs"))
        self.node_list = []
        self.edge_list = []
        self.weight_dict = {}
        self.row_count = 1
        self.root = tk.Tk()
        self.algorithms = [
            "DFS (Depth First Search)",
            "Directed DFS",
            "Kruskal",
            "Dijkstra",
            "Find Cut Vertices",
            "Find Cut Edges",
            "Find Biconnected Components",
            "Reverse",
            "Find Strongly Connected Components",
            "Topological Sorting",
            "Find Hamiltonian Path",
            "Ford-Fulkerson",
            "All Shortest Paths",
        ]
        self.weight_var = tk.BooleanVar(value=False)
        self.weight_var.trace("w", self.del_weight_widgets)
        self.direction_var = tk.BooleanVar(value=False)
        self.direction_var.trace("w", self.del_direction_widgets)

        self.fig_height = tk.IntVar(value=5)
        self.fig_width = tk.IntVar(value=5)
        self.vertex_size = tk.IntVar(value=30)

        self.root.title("Graph Theory Algorithms")
        self.geo = (1920, 1080)
        self.root.geometry(f"{self.geo[0]}x{self.geo[1]}")
        self.clicked = tk.StringVar()
        self.clicked.set("Algorithm")
        self.dfs_node = tk.StringVar(value="DFS Node")
        self.dfs_node.trace("w", self.dfs_node_detector)
        self.ddfs_node = tk.StringVar(value="DDFS Node")
        self.ddfs_node.trace("w", self.ddfs_node_detector)
        self.vertex_size = 0.3
        self.vertex_size_scaled = tk.IntVar(value=30)

        self.direction_widgets = []
        self.weight_widgets = []
        self.edge_count = 0
        self.direction_count = 0

        self.dijkstra_source = tk.StringVar(value="Source")
        self.dijkstra_source.trace("w", self.dijkstra_node_detector)
        self.dijkstra_target = tk.StringVar(value="Target")
        self.dijkstra_target.trace("w", self.dijkstra_node_detector)

        self.ff_source = tk.StringVar(value="Source")
        self.ff_source.trace("w", self.ff_node_detector)
        self.ff_target = tk.StringVar(value="Target")
        self.ff_target.trace("w", self.ff_node_detector)
        self.ff_algorithm_var = tk.StringVar(value="Maximum Flow")
        self.ff_algorithm_var.trace("w", self.ff_display_algorithm)

        self.current_algortihm = tk.StringVar(
            value="Select an Algorithm to Apply",
        )
        self.current_algortihm.trace("w", self.algorithm_detector)
        self.widget_list = []
        self.bicon_image_number = tk.IntVar(value=1)
        self.bicon_image_number.trace("w", self.bicon_image_detector)
        self.scc_image_number = tk.IntVar(value=1)
        self.scc_image_number.trace("w", self.scc_image_detector)
        self.top_sort_image_number = tk.IntVar(value=1)
        self.top_sort_image_number.trace("w", self.top_sort_image_detector)
        self.hamiltonian_image_number = tk.IntVar(value=1)
        self.hamiltonian_image_number.trace("w", self.hamiltonian_image_detector)
        self.direction_dict = {}
        self.directed = tk.BooleanVar(value=False)
        self.directed.trace("w", self.display_graph)
        self.weighted = tk.BooleanVar(value=False)
        self.weighted.trace("w", self.display_graph)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(
            row=0, column=0, sticky="nswe", padx=(10, 10), pady=(10, 10)
        )
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nswe")

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=5, sticky="nswe")

        self.tweak_frame = tk.Frame(
            self.main_frame, highlightbackground="gray", highlightthickness=2
        )
        self.tweak_frame.grid(row=0, column=8, sticky="nswe", rowspan=1, columnspan=3)
        self.tweak_frame_title = tk.Label(
            master=self.tweak_frame,
            text="Tweak Visual Properties",
            font=("Helvetica", 12),
        ).grid(row=0, column=0)
        self.vertex_size_slider = tk.Scale(
            master=self.tweak_frame,
            from_=0,
            to=100,
            variable=self.vertex_size_scaled,
            command=self.change_vertex_size,
            orient="horizontal",
            label="Vertex Size",
        )
        self.vertex_size_slider.grid(row=1, column=0)
        self.graph_width_slider = tk.Scale(
            master=self.tweak_frame,
            from_=1,
            to=7,
            variable=self.fig_width,
            command=self.display_graph,
            orient="horizontal",
            label="Graph Width",
        )
        self.graph_width_slider.grid(row=2, column=0)

        self.graph_height_slider = tk.Scale(
            master=self.tweak_frame,
            from_=1,
            to=7,
            variable=self.fig_height,
            command=self.display_graph,
            orient="horizontal",
            label="Graph Height",
        )
        self.graph_height_slider.grid(row=3, column=0)

        self.nodebox = tk.Entry(self.left_frame, width=10, font=("Helvetica", 18))
        self.nodebox.grid(row=0, column=0)

        self.edgebox = tk.Entry(self.left_frame, width=10, font=("Helvetica", 18))
        self.edgebox.config(state="disabled")
        self.edgebox.grid(row=2, column=0)

        self.add_button = tk.Button(
            self.left_frame, text="Add Node", command=self.add_node
        )
        self.add_button.grid(row=0, column=1)

        self.edge_button = tk.Button(self.left_frame, text="Add Edges")
        self.edge_button.config(state="disabled")
        self.edge_button.grid(row=2, column=1)

        self.weight_assign = tk.Frame(self.main_frame, name="weights")
        self.weight_assign.grid(row=0, column=3, sticky="nswe")

        self.add_weight = tk.Button(
            self.weight_assign, text="Assign Weights", command=self.assign_weights
        )
        self.add_weight.grid(row=self.edge_count + 2, column=1)
        self.add_weight.grid_remove()

        self.direction_assign = tk.Frame(self.main_frame, name="direction_assign")
        self.direction_assign.grid(row=0, column=4, sticky="nswe")

        self.weight_check = tk.Checkbutton(
            self.left_frame,
            text="Weighted",
            variable=self.weight_var,
            onvalue=True,
            offvalue=False,
            command=self.generate_connections,
        )
        self.weight_check.grid(row=3, column=0)

        self.direction_check = tk.Checkbutton(
            self.left_frame,
            text="Directed",
            variable=self.direction_var,
            onvalue=True,
            offvalue=False,
            command=self.generate_directions,
        )
        self.direction_check.grid(row=4, column=0)

        self.clear_button = tk.Button(
            self.left_frame, text="Clear Graph", command=self.clear_graph
        )
        self.clear_button.grid(row=5, column=0)

        self.dropdown_label = tk.Label(
            self.left_frame, text="Choose an Algorithm to apply"
        )
        self.dropdown_label.grid(row=7, column=0)

        self.drop = tk.OptionMenu(
            self.left_frame, self.current_algortihm, *self.algorithms
        ).grid(row=8, column=0)

        self.restart_button = tk.Button(
            self.right_frame, text="Restart", command=lambda: self.restart()
        ).grid(row=1, column=6)

        self.display_graph()
        self.root.mainloop()

    def generate_connections(self):
        if self.edge_count == len(self.graph.es):
            return

        self.weight_label = tk.Label(self.weight_assign, text="Weights").grid(
            row=0, column=0
        )
        inv_node_dict = {v: k for k, v in self.node_dict.items()}

        def f(x):
            return inv_node_dict[x]

        for edge in self.graph.es:
            a, b = edge.source, edge.target
            if (a, b) not in self.weight_dict.keys():
                self.edge_label = tk.Label(
                    self.weight_assign, text=f"{f(a)} -> {f(b)}"
                ).grid(row=self.edge_count + 1, column=0)
                self.weight = tk.Entry(self.weight_assign, name=f"{(a, b)}")
                self.weight.grid(row=self.edge_count + 1, column=1)
                self.weight_dict.update({(a, b): self.weight, (b, a): self.weight})
                self.edge_count += 1

        self.add_weight.grid(row=self.edge_count + 2, column=1)
        children = [v for _, v in self.weight_assign.children.items()]
        self.weight_widgets.extend(children)
        self.widget_list.extend(children)

    def generate_directions(self):
        if self.direction_count == len(self.graph.es):
            return
        self.direction_label = tk.Label(self.direction_assign, text="Directions").grid(
            row=0, column=0
        )
        inv_node_dict = {v: k for k, v in self.node_dict.items()}

        def f(x):
            return inv_node_dict[x]

        self.edge_memory = {}

        def g(a, b):
            inv = {"->": "<-", "<-": "->"}
            self.btn_text.set(inv[self.btn_text.get()])
            bt = self.edge_memory[(a, b)]
            bt.config(text=self.btn_text.get())
            for ix, edge in enumerate(self.edge_list):
                tmp = (edge[0], edge[1])
                if tmp == (a, b):
                    self.graph.delete_edges([tmp])
                    self.edge_list.pop(ix)
                    self.graph.add_edge(b, a)
                    self.edge_list.insert(ix, (b, a))
                    break
                elif tmp == (b, a):
                    self.graph.delete_edges([tmp])
                    self.edge_list.pop(ix)
                    self.graph.add_edge(a, b)
                    self.edge_list.insert(ix, (a, b))
                    break

            self.display_graph()

        for edge in self.graph.copy().es:
            a, b = edge.source, edge.target
            c = self.direction_count + 1
            self.btn_text = tk.StringVar(value="->")
            self.source_label = tk.Label(self.direction_assign, text=f"{f(a)}").grid(
                row=c, column=1
            )
            self.target_label = tk.Label(self.direction_assign, text=f"{f(b)}").grid(
                row=c, column=3
            )
            self.direction_button = tk.Button(
                self.direction_assign, text=self.btn_text.get(), name=f"{(a, b)}"
            ).grid(row=c, column=2)

            self.edge_memory[(a, b)] = self.direction_assign.children[f"{(a, b)}"]
            self.edge_memory[(a, b)].config(command=lambda a=a, b=b: g(a, b))
            self.direction_count += 1

        children = [v for _, v in self.direction_assign.children.items()]
        self.widget_list.extend(children)

    def del_direction_widgets(self, *args):
        self.directed.set(not self.directed.get())
        if self.direction_var.get() == False:
            self.direction_count = 0
            self.direction_assign.grid_forget()
            for widget in self.direction_assign.children:
                del widget
        else:
            self.direction_assign.grid(row=0, column=4, sticky="nswe")

    def del_weight_widgets(self, *args):
        self.weighted.set(not self.weighted.get())
        if self.weight_var.get() == False:
            self.weight_assign.grid_forget()
            for widget in self.weight_assign.children:
                del widget
        else:
            self.weight_assign.grid(row=0, column=3, sticky="nswe")

    def algorithm_detector(self, *args):
        algorithm = self.current_algortihm.get()
        algo_to_function = {
            "DFS (Depth First Search)": self.apply_dfs,
            "Kruskal": self.apply_kruskal,
            "Dijkstra": self.apply_dijkstra,
            "Find Cut Vertices": self.apply_articulation_point,
            "Find Cut Edges": self.apply_find_bridges,
            "Find Biconnected Components": self.apply_biconnected_components,
            "Reverse": self.apply_reverse,
            "Directed DFS": self.apply_ddfs,
            "Find Strongly Connected Components": self.apply_scc,
            "Topological Sorting": self.apply_topological_sorting,
            "Find Hamiltonian Path": self.apply_hamiltonian_path,
            "Ford-Fulkerson": self.apply_ford_fulkerson,
            "All Shortest Paths": self.apply_all_shortest_paths,
        }

        try:
            self.algo_frame.config(border=0)
            self.algo_frame.grid_remove()
        except:
            pass
        for widget in self.widget_list:
            if widget.winfo_parent().split(".")[-1] in ["weights", "direction_assign"]:
                continue
            try:
                widget.config(border=0)
            except:
                pass
            widget.grid_remove()

        self.widget_list = []

        self.algo_summary = tk.Label(self.left_frame, text="")
        self.algo_summary.grid(row=11, column=0)

        return algo_to_function.get(algorithm)()

    def assign_weights(self):
        self.graph_copy = self.graph.copy()
        for edge in self.graph_copy.es:
            edge["weight"] = int(self.weight_dict.get((edge.source, edge.target)).get())
        self.display_graph()

    def show_dropdown(self):
        self.dropdown_label.config(text=self.clicked.get())

    def add_node(self):
        val = self.nodebox.get()
        if val == "" or val in self.node_list:
            pass
        else:
            self.node_list.append(val)

        self.get_connections(val)
        self.edgebox.config(state="normal")
        self.edge_button.config(state="normal")
        self.display_graph()

    def get_connections(self, node):
        self.edge_button = tk.Button(
            self.left_frame, text="Add Edges", command=lambda: self.add_edges(node)
        )
        self.edge_button.grid(row=2, column=1)

    def add_edges(self, node):
        edges = self.edgebox.get()
        edges = [edge.replace(" ", "") for edge in edges.split(",")]
        edges = [edge for edge in edges if edge]
        self.display_graph()

        for edge in edges:
            if edge not in self.node_list:
                self.node_list.append(edge)

            self.node_dict = {
                item: self.node_list.index(item) for item in self.node_list
            }
            k, v = self.node_dict.get(node), self.node_dict.get(edge)
            if (k, v) not in self.edge_list and edge != node:
                self.edge_list.append((k, v))
        self.edgebox.delete(0, tk.END)
        self.nodebox.delete(0, tk.END)
        self.edgebox.config(state="disabled")
        self.edge_button.config(state="disabled")
        self.display_graph()

    def display_graph(self, *args):
        self.graph = ig.Graph(
            n=len(self.node_list), edges=self.edge_list, directed=self.directed.get()
        )
        graph = self.graph
        graph.vs["name"] = self.node_list
        try:
            graph.es["weight"] = self.graph_copy.es["weight"]
        except:
            pass
        plotter(
            graph,
            vertex_size=self.vertex_size,
            fig_size=(self.fig_width.get(), self.fig_height.get()),
        )
        img = Image.open(os.path.join(os.getcwd(), "out_graphs", "graph.png"))
        photo_image = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(
            self.right_frame, text="Graph Preview", font=("Helvetica", 20)
        )
        self.image_label.grid(row=1, column=5)
        self.image_frame = tk.Label(self.right_frame, image=photo_image)
        self.image = photo_image
        self.image_frame.grid(row=2, column=5, rowspan=2, columnspan=2)

    def get_dijkstra_nodes(self):
        return self.dijkstra_source.get(), self.dijkstra_target.get()

    def dijkstra_node_detector(self, *args):
        return self.apply_dijkstra(self.dijkstra_source, self.dijkstra_target)

    def get_ff_nodes(self):
        try:
            return self.node_dict.get(self.ff_source.get()), self.node_dict.get(
                self.ff_target.get()
            )
        except:
            return 0, 0

    def ff_node_detector(self, *args):
        return self.apply_ford_fulkerson(self.ff_source, self.ff_target)

    def ff_display_algorithm(self, *args):
        if self.ff_algorithm_var.get() == "Maximum Flow":
            self.display_algorithm("ff_graph_max_flow.png", 13, 0)
            txt = self.ff_cost_result
        else:
            self.display_algorithm("ff_graph_min_cut.png", 13, 0)
            txt = "The minimum cut passes through the edges highlighted below."

        try:
            self.algo_summary.grid_remove()
        except:
            pass

        self.algo_summary = tk.Label(self.left_frame, text=40 * " ")
        self.algo_summary.config(text=txt)
        self.algo_summary.grid(row=12, column=0)
        self.widget_list.extend([self.algo_frame, self.algo_summary])

    def dfs_node_detector(self, *args):
        return self.apply_dfs(self.dfs_node.get())

    def ddfs_node_detector(self, *args):
        self.algo_summary.config(text="")
        return self.apply_ddfs(self.ddfs_node.get())

    def apply_dijkstra(self, source=None, target=None):
        ret = dijkstra(self.graph, source, target)
        if type(ret) == str:
            self.algo_summary = tk.Label(self.left_frame, text="")
            self.algo_summary.grid_forget()
            self.algo_summary.config(text=ret)
            self.algo_summary.grid(row=12, column=0)
            self.widget_list.append(self.algo_summary)
            return

        self.dijkstra_source_drop = tk.OptionMenu(
            self.left_frame, self.dijkstra_source, *self.node_list
        )
        self.dijkstra_source_drop.grid(row=10, column=0)
        self.dijkstra_target_drop = tk.OptionMenu(
            self.left_frame, self.dijkstra_target, *self.node_list
        )
        self.dijkstra_target_drop.grid(row=10, column=1)
        self.widget_list.extend([self.dijkstra_source_drop, self.dijkstra_target_drop])

        source, target = self.get_dijkstra_nodes()
        if source != "Source" and target != "Target":
            self.algo_summary = tk.Label(self.left_frame, text="")
            self.algo_summary.grid_forget()
            source, target = self.node_dict[source], self.node_dict[target]
            ret = dijkstra(self.graph, source, target)
            if type(ret) == str:
                try:
                    self.algo_frame.grid_forget()
                except:
                    pass
                self.algo_summary.config(text=ret)
                self.algo_summary.grid(row=12, column=0)
                self.widget_list.append(self.algo_summary)
            else:
                dijkstra_graph, cost = ret
                fig, ax = plt.subplots(
                    figsize=(self.fig_width.get(), self.fig_height.get())
                )
                ig.plot(
                    obj=dijkstra_graph,
                    target=ax,
                    vertex_label=self.graph.vs["name"],
                    edge_label=dijkstra_graph.es["weight"],
                    vertex_size=self.vertex_size,
                    margin=50,
                )
                fig.savefig(
                    os.path.join("out_graphs", "dijkstra_graph.png"), transparent=True
                )
                plt.close()

                self.algo_summary.config(text=f"The cost is {cost}.")
                self.algo_summary.grid(row=12, column=0)
                self.display_algorithm("dijkstra_graph.png", 13, 0)

        self.widget_list.append(self.algo_summary)

    def apply_dfs(self, node=None):
        self.node_drop = tk.OptionMenu(self.left_frame, self.dfs_node, *self.node_list)
        self.node_drop.grid(row=10, column=0)

        x = node
        if x in self.node_list:
            path, dfs_graph = dfs(self.graph, self.node_dict.get(x))
            path = f"The path of DFS is {path}."
            self.algo_summary = tk.Label(self.left_frame, text=path)
            self.algo_summary.grid(row=11, column=0)
            fig, ax = plt.subplots(
                figsize=(self.fig_width.get(), self.fig_height.get())
            )
            ig.plot(
                dfs_graph,
                target=ax,
                vertex_label=self.graph.vs["name"],
                vertex_size=self.vertex_size,
                margin=50,
            )
            fig.savefig(os.path.join("out_graphs", "dfs_graph.png"), transparent=True)
            plt.close()
            self.display_algorithm("dfs_graph.png", 12, 0)

        self.widget_list.extend([self.node_drop, self.algo_summary])

    def apply_kruskal(self):
        if not self.weighted.get() or not self.graph.is_connected():
            self.algo_summary = tk.Label(
                self.left_frame,
                text=f"Kruskal requires a weighted and connected graph, but this graph is not.",
            )
            self.algo_summary.grid(row=11, column=0)
            self.widget_list.append(self.algo_summary)
            return

        cost, mst, _ = kruskal(self.graph)
        self.algo_summary = tk.Label(
            self.left_frame, text=f"Minimum spanning tree with a cost of {cost}"
        )
        self.algo_summary.grid(row=11, column=0)
        self.widget_list.append(self.algo_summary)
        fig, ax = plt.subplots(figsize=(self.fig_width.get(), self.fig_height.get()))
        ig.plot(
            mst,
            target=ax,
            vertex_label=self.graph.vs["name"],
            edge_label=self.graph.es["weight"],
            vertex_size=self.vertex_size,
            margin=50,
        )
        fig.savefig(os.path.join("out_graphs", "kruskal_graph.png"), transparent=True)
        plt.close()
        self.display_algorithm("kruskal_graph.png", 12, 0)

    def apply_articulation_point(self):
        graph_aps, aps_named, _ = articulation_point(self.graph)
        txt = ", ".join(aps_named)

        if aps_named:
            txt = f"The articulation points are: {txt}."
        else:
            txt = "There are no articulation points for this graph."

        self.algo_summary = tk.Label(self.left_frame, text=txt)
        self.algo_summary.grid(row=11, column=0)
        fig, ax = plt.subplots(figsize=(self.fig_width.get(), self.fig_height.get()))
        ig.plot(
            graph_aps,
            target=ax,
            vertex_label=graph_aps.vs["name"],
            vertex_size=self.vertex_size,
            margin=50,
        )
        fig.savefig(
            os.path.join("out_graphs", "articulation_points_graph.png"),
            transparent=True,
        )
        plt.close()
        self.display_algorithm("articulation_points_graph.png", 12, 0)
        self.widget_list.append(self.algo_summary)

    def apply_find_bridges(self):
        bridges_named, bridged_graph = find_bridges(self.graph)
        txt = ""
        for ix, edge in enumerate(bridges_named):
            txt += " -> ".join(edge)
            if ix != len(bridges_named) - 1:
                txt += ", "
        if bridges_named:
            txt = f"The bridges are: {txt}."
        else:
            txt = "There are no bridges on this graph."
        self.algo_summary = tk.Label(self.left_frame, text=txt)
        self.algo_summary.grid(row=11, column=0)
        fig, ax = plt.subplots(figsize=(self.fig_width.get(), self.fig_height.get()))
        ig.plot(
            bridged_graph,
            target=ax,
            vertex_label=bridged_graph.vs["name"],
            vertex_size=self.vertex_size,
            margin=50,
        )
        fig.savefig(os.path.join("out_graphs", "bridges_graph.png"), transparent=True)
        plt.close()
        self.display_algorithm("bridges_graph.png", 12, 0)

        self.widget_list.append(self.algo_summary)

    def apply_biconnected_components(self):
        bicons = biconnected_components(self.graph)
        if not bicons:
            self.algo_summary = tk.Label(
                self.left_frame,
                text=f"There are no biconnected components of this graph.",
            )
            self.algo_summary.grid(row=11, column=1)
            return

        self.bicon_count = len(bicons)
        for ix, bicon in enumerate(bicons):
            fig, ax = plt.subplots(
                figsize=(self.fig_width.get(), self.fig_height.get())
            )
            ig.plot(
                bicon,
                target=ax,
                vertex_label=bicon.vs["name"],
                vertex_size=self.vertex_size,
                margin=50,
            )
            fig.savefig(
                os.path.join("out_graphs", f"bicon_graph_{ix+1}.png"), transparent=True
            )
            plt.close()

        self.display_algorithm(f"bicon_graph_1.png", 13, 1)

        self.algo_summary = tk.Label(
            self.left_frame,
            text=f"There are {len(bicons)} biconnected components of this graph.",
        )
        self.algo_summary.grid(row=11, column=1)

        self.prev_button = tk.Button(
            self.left_frame, text="<", command=self.prev_bicon_image
        )
        self.prev_button.grid(row=12, column=0)

        self.bicon_index = tk.Label(
            self.left_frame, text=f"{self.bicon_image_number.get()}"
        )
        self.bicon_index.grid(row=12, column=1)

        self.next_button = tk.Button(
            self.left_frame, text=">", command=self.next_bicon_image
        )
        self.next_button.grid(row=12, column=2)

        self.widget_list.extend(
            [self.algo_summary, self.prev_button, self.next_button, self.bicon_index]
        )

    def apply_ddfs(self, node=None):
        self.ddfs_node_drop = tk.OptionMenu(
            self.left_frame, self.ddfs_node, *self.node_list
        )
        self.ddfs_node_drop.grid(row=10, column=0)
        self.algo_summary = tk.Label(self.left_frame, text="")
        self.algo_summary.grid(row=11, column=0)
        self.widget_list.extend([self.ddfs_node_drop, self.algo_summary])

        if node is None:
            return
        if node in self.node_list:
            path, ddfs_graph = ddfs(
                self.graph, self.node_dict.get(node), tail=[], edges=[]
            )
            inv_node_dict = {v: k for k, v in self.node_dict.items()}
            if len(path) == 1:
                self.algo_summary.config(text=f"Node {node} is a terminal node.")
                self.algo_summary.grid()
                return
            path_str = "The path of Directed DFS is: "
            path_str += "->".join([inv_node_dict.get(x) for x in path])
            self.algo_summary.config(text=path_str)
            self.algo_summary.grid(row=11, column=0)
            fig, ax = plt.subplots(
                figsize=(self.fig_width.get(), self.fig_height.get())
            )
            ig.plot(
                ddfs_graph,
                target=ax,
                vertex_label=ddfs_graph.vs["name"],
                vertex_size=self.vertex_size,
                margin=50,
            )
            fig.savefig(os.path.join("out_graphs", "ddfs_graph.png"), transparent=True)
            plt.close()
            self.display_algorithm("ddfs_graph.png", 12, 0)

    def apply_reverse(self):
        reversed_graph = self.graph.copy()
        reversed_graph = reverse(reversed_graph)
        fig, ax = plt.subplots(figsize=(self.fig_width.get(), self.fig_height.get()))
        ig.plot(
            reversed_graph,
            target=ax,
            vertex_label=reversed_graph.vs["name"],
            vertex_size=self.vertex_size,
            margin=50,
        )
        fig.savefig(os.path.join("out_graphs", "reversed_graph.png"), transparent=True)
        plt.close()
        self.display_algorithm("reversed_graph.png", 12, 0)

    def apply_scc(self):
        ret = strongly_connected_components(self.graph.copy())

        if type(ret) == list:
            ret = [g for g in ret if len(g.vs) > 1]
            if len(ret) == 0:
                self.algo_summary = tk.Label(
                    self.left_frame,
                    text="There are no strongly connected components for this graph.",
                )
                self.algo_summary.grid(row=11, column=0)
                self.widget_list.append(self.algo_summary)
                return

        if type(ret) == str:
            self.algo_summary = tk.Label(self.left_frame, text=ret)
            self.algo_summary.grid(row=11, column=0)
            self.widget_list.append(self.algo_summary)
            return
        else:
            for ix, sg in enumerate(ret):
                fig, ax = plt.subplots(
                    figsize=(self.fig_width.get(), self.fig_height.get())
                )
                ig.plot(
                    sg,
                    target=ax,
                    vertex_label=sg.vs["name"],
                    vertex_size=self.vertex_size,
                    margin=50,
                )
                fig.savefig(
                    os.path.join("out_graphs", f"scc_graph_{ix+1}.png"),
                    transparent=True,
                )
                plt.close()
            self.scc_count = len(ret)
            self.algo_summary = tk.Label(
                self.left_frame,
                text=f"There are {len(ret)} strongly connected components of this graph.",
            )
            self.algo_summary.grid(row=11, column=1)

            self.prev_button = tk.Button(
                self.left_frame, text="<", command=self.prev_scc
            )
            self.prev_button.grid(row=12, column=0)

            self.scc_index = tk.Label(
                self.left_frame, text=f"{self.scc_image_number.get()}"
            )
            self.scc_index.grid(row=12, column=1)

            self.next_button = tk.Button(
                self.left_frame, text=">", command=self.next_scc
            )
            self.next_button.grid(row=12, column=2)
            self.display_algorithm(f"scc_graph_1.png", 13, 1)

            self.widget_list.extend(
                [self.algo_summary, self.prev_button, self.next_button, self.scc_index]
            )

    def apply_topological_sorting(self):
        ret = topological_sort(self.graph)
        if type(ret) == str:
            self.algo_summary = tk.Label(self.left_frame, text=ret)
            self.algo_summary.grid(row=11, column=0)
            self.widget_list.append(self.algo_summary)
        else:
            self.enum_labels = {}
            for ix, item in enumerate(ret):
                tmp_label, tmp_graph = item[0], item[1]
                tmp_label = "->".join([n for n in tmp_label])
                self.enum_labels.update({f"label_{ix+1}": tmp_label})
                fig, ax = plt.subplots(
                    figsize=(self.fig_width.get(), self.fig_height.get())
                )

                ig.plot(
                    tmp_graph,
                    target=ax,
                    vertex_label=tmp_graph.vs["name"],
                    vertex_size=self.vertex_size,
                    margin=50,
                )
                fig.savefig(
                    os.path.join("out_graphs", f"top_sort_graph_{ix+1}.png"),
                    transparent=True,
                )
                plt.close()

            self.top_sort_count = len(ret)
            self.algo_summary = tk.Label(
                self.left_frame,
                text=f"There are {len(ret)} possible topological sorts for this graph.",
            )
            self.algo_summary.grid(row=11, column=1)

            self.prev_button = tk.Button(
                self.left_frame, text="<", command=self.prev_top_sort
            )
            self.prev_button.grid(row=12, column=0)

            self.top_sort_index = tk.Label(
                self.left_frame, text=f"{self.top_sort_image_number.get()}"
            )
            self.top_sort_index.grid(row=12, column=1)

            self.next_button = tk.Button(
                self.left_frame, text=">", command=self.next_top_sort
            )
            self.next_button.grid(row=12, column=2)
            self.top_sort_path = tk.Label(
                self.left_frame, text=self.enum_labels.get("label_1")
            )
            self.top_sort_path.grid(row=14, column=1)
            self.display_algorithm(f"top_sort_graph_1.png", 13, 1)

            self.widget_list.extend(
                [
                    self.algo_summary,
                    self.next_button,
                    self.top_sort_index,
                    self.top_sort_path,
                ]
            )

    def apply_hamiltonian_path(self):
        ret = hamiltonian_path(self.graph)
        if type(ret) == str:
            self.algo_summary = tk.Label(self.left_frame, text=ret)
            self.algo_summary.grid(row=11, column=0)
            self.widget_list.append(self.algo_summary)
        else:
            self.enum_labels = {}
            for ix, item in enumerate(ret):
                tmp_label, tmp_graph = item[0], item[1]
                self.enum_labels.update({f"label_{ix+1}": tmp_label})
                fig, ax = plt.subplots(
                    figsize=(self.fig_width.get(), self.fig_height.get())
                )
                ig.plot(
                    tmp_graph,
                    target=ax,
                    vertex_label=tmp_graph.vs["name"],
                    edge_label=tmp_graph.es["label"],
                    vertex_size=self.vertex_size,
                    margin=50,
                )
                fig.savefig(
                    os.path.join("out_graphs", f"hamiltonian_graph_{ix+1}.png"),
                    transparent=True,
                )
                plt.close()

            self.hamiltonian_count = len(ret)
            self.algo_summary = tk.Label(self.left_frame, text="")

            if len(ret) == 0:
                self.algo_summary.config(
                    text="No hamiltonian paths found for this graph."
                )
                self.algo_summary.grid(row=11, column=0)
                self.widget_list.append(self.algo_summary)
                return
            else:
                self.algo_summary.config(
                    text=f"{len(ret)} Hamiltonian paths found for this graph, but there may be more."
                )
                self.algo_summary.grid(row=11, column=1)
                self.widget_list.append(self.algo_summary)

            self.prev_button = tk.Button(
                self.left_frame, text="<", command=self.prev_hamiltonian
            )
            self.prev_button.grid(row=12, column=0)

            self.hamiltonian_index = tk.Label(
                self.left_frame, text=f"{self.hamiltonian_image_number.get()}"
            )
            self.hamiltonian_index.grid(row=12, column=1)

            self.next_button = tk.Button(
                self.left_frame, text=">", command=self.next_hamiltonian
            )
            self.next_button.grid(row=12, column=2)

            self.hamiltonian_path = tk.Label(
                self.left_frame, text=self.enum_labels.get("label_1")
            )
            self.hamiltonian_path.grid(row=13, column=1)
            self.display_algorithm(f"hamiltonian_graph_1.png", 14, 1)
            self.widget_list.extend(
                [
                    self.prev_button,
                    self.next_button,
                    self.hamiltonian_index,
                    self.hamiltonian_path,
                ]
            )

    def apply_ford_fulkerson(self, source=0, target=0):
        ret = ford_fulkerson(self.graph, source, target)
        if type(ret) == str:
            self.algo_summary = tk.Label(self.left_frame, text=ret)
            self.algo_summary.grid(row=11, column=0)
            self.widget_list.append(self.algo_summary)
            return

        self.ff_source_drop = tk.OptionMenu(
            self.left_frame, self.ff_source, *self.node_list
        )
        self.ff_source_drop.grid(row=10, column=0)
        self.ff_target_drop = tk.OptionMenu(
            self.left_frame, self.ff_target, *self.node_list
        )
        self.ff_target_drop.grid(row=10, column=1)
        source, target = self.get_ff_nodes()
        txt, ff_graph_max, ff_graph_min = ford_fulkerson(self.graph, source, target)
        if not txt and not ff_graph_max and not ff_graph_min:
            return
        self.ff_cost_result = txt
        fig, ax = plt.subplots(figsize=(self.fig_width.get(), self.fig_height.get()))
        ig.plot(
            ff_graph_max,
            target=ax,
            vertex_label=ff_graph_max.vs["name"],
            edge_label=ff_graph_max.es["weight"],
            vertex_size=self.vertex_size,
            margin=50,
        )
        fig.savefig(
            os.path.join("out_graphs", "ff_graph_max_flow.png"), transparent=True
        )
        plt.close()

        fig, ax = plt.subplots(figsize=(self.fig_width.get(), self.fig_height.get()))
        ig.plot(
            ff_graph_min,
            target=ax,
            vertex_label=ff_graph_min.vs["name"],
            edge_label=ff_graph_min.es["weight"],
            vertex_size=self.vertex_size,
            margin=50,
        )
        fig.savefig(
            os.path.join("out_graphs", "ff_graph_min_cut.png"), transparent=True
        )
        plt.close()

        self.ff_algorithm_drop = tk.OptionMenu(
            self.left_frame, self.ff_algorithm_var, *["Maximum Flow", "Minimum Cut"]
        ).grid(row=11, column=0)

        self.widget_list.extend([self.algo_summary, self.ff_algorithm_drop])

    def apply_all_shortest_paths(self):
        ret = all_shortest_paths(self.graph)
        export(
            ret,
            os.path.join("out_graphs", "df_image.png"),
            table_conversion="matplotlib",
        )
        self.display_algorithm("df_image.png", 12, 0)

    def bicon_image_detector(self, *args):
        self.display_algorithm(
            f"bicon_graph_{self.bicon_image_number.get()}.png", 13, 1
        )

    def next_bicon_image(self):
        x = self.bicon_image_number.get()
        if x < self.bicon_count:
            self.bicon_image_number.set(x + 1)
            self.bicon_index.config(text=f"{self.bicon_image_number.get()}")

    def prev_bicon_image(self):
        x = self.bicon_image_number.get()
        if x > 1:
            self.bicon_image_number.set(x - 1)
            self.bicon_index.config(text=f"{self.bicon_image_number.get()}")

    def scc_image_detector(self, *args):
        self.display_algorithm(f"scc_graph_{self.scc_image_number.get()}.png", 13, 1)

    def next_scc(self):
        x = self.scc_image_number.get()
        if x < self.scc_count:
            self.scc_image_number.set(x + 1)
            self.scc_index.config(text=f"{self.scc_image_number.get()}")

    def prev_scc(self):
        x = self.scc_image_number.get()
        if x > 1:
            self.scc_image_number.set(x - 1)
            self.scc_index.config(text=f"{self.scc_image_number.get()}")

    def top_sort_image_detector(self, *args):
        self.top_sort_path.grid_forget()
        ix = self.top_sort_image_number.get()
        self.top_sort_path = tk.Label(self.left_frame, text=self.enum_labels.get(ix))
        self.top_sort_path.grid(row=13, column=1)
        self.display_algorithm(f"top_sort_graph_{ix}.png", 14, 1)

    def prev_top_sort(self):
        x = self.top_sort_image_number.get()
        if x > 1:
            self.top_sort_image_number.set(x - 1)
            self.top_sort_index.config(text=f"{self.top_sort_image_number.get()}")

    def next_top_sort(self):
        x = self.top_sort_image_number.get()
        if x < self.top_sort_count:
            self.top_sort_image_number.set(x + 1)
            self.top_sort_index.config(text=f"{self.top_sort_image_number.get()}")

    def hamiltonian_image_detector(self, *args):
        self.hamiltonian_path.grid_forget()
        ix = self.hamiltonian_image_number.get()
        self.hamiltonian_path = tk.Label(self.left_frame, text=self.enum_labels.get(ix))
        self.hamiltonian_path.grid(row=13, column=1)
        self.display_algorithm(f"hamiltonian_graph_{ix}.png", 14, 1)

    def prev_hamiltonian(self):
        x = self.hamiltonian_image_number.get()
        if x > 1:
            self.hamiltonian_image_number.set(x - 1)
            ix = f"label_{self.hamiltonian_image_number.get()}"
            self.hamiltonian_path.config(text=f"{self.enum_labels.get(ix)}")
            self.hamiltonian_index.config(text=self.hamiltonian_image_number.get())
            self.widget_list.append(self.hamiltonian_path)

    def next_hamiltonian(self):
        x = self.hamiltonian_image_number.get()
        if x < self.hamiltonian_count:
            self.hamiltonian_image_number.set(x + 1)
            ix = f"label_{self.hamiltonian_image_number.get()}"
            self.hamiltonian_path.config(text=f"{self.enum_labels.get(ix)}")
            self.hamiltonian_index.config(text=self.hamiltonian_image_number.get())
            self.widget_list.append(self.hamiltonian_path)

    def display_algorithm(self, filename, row, column):
        img = Image.open(os.path.join(os.getcwd(), "out_graphs", filename))
        photo_image = ImageTk.PhotoImage(img)
        self.algo_frame = tk.Label(
            self.left_frame, image=photo_image, borderwidth=2, relief="solid"
        )
        self.algo_image = photo_image
        self.algo_frame.grid(row=row, column=column)
        self.widget_list.append(self.algo_frame)

    def clear_graph(self):
        self.node_list = []
        self.node_dict = {}
        self.edge_list = []
        self.image_frame.grid_forget()
        self.directed.set(False)
        for widget in self.widget_list:
            widget.grid_remove()
        self.widget_list = []
        self.del_direction_widgets()
        self.del_weight_widgets()
        try:
            self.algo_frame.grid_forget()
        except:
            pass

    def change_vertex_size(self, *args):
        self.vertex_size = self.vertex_size_scaled.get() / 100
        self.display_graph()

    def restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


UI()
