import tkinter as tk
from algorithms import *
from samples import *
from genesis import *
import igraph as ig
from PIL import ImageTk, Image
import os
import sys
class UI:

    def __init__(self):
        self.node_list = []
        self.edge_list = []
        self.weight_dict = {}
        self.row_count = 1
        self.root = tk.Tk()
        self.algorithms = ['DFS (Depth First Search)', 'Directed DFS', 'Kruskal', 'Dijkstra', 'Find Articulation Points', 'Find Bridges',
                            'Find Biconnected Components', 'Reverse', 'Find Strongly Connected Components', 'Topological Sorting']
        self.weight_var = tk.BooleanVar(value = False)
        self.weight_var.trace('w', self.del_weight_widgets)
        self.direction_var = tk.BooleanVar(value = False)
        self.direction_var.trace('w', self.del_direction_widgets)

        self.root.title('Graph Theory')
        self.root.geometry('1200x600')
        self.clicked = tk.StringVar()
        self.clicked.set( "Algorithm" )
        self.dfs_node = tk.StringVar(value = "DFS Node")
        self.dfs_node.trace('w', self.dfs_node_detector)
        self.ddfs_node = tk.StringVar(value = "DDFS Node")
        self.ddfs_node.trace('w', self.ddfs_node_detector)
        self.png_size = (0, 0, 600, 400)
        self.direction_widgets = []
        self.weight_widgets = []
        self.edge_count = 0
        self.direction_count = 0
        self.dijkstra_source = tk.StringVar(value = "Source")
        self.dijkstra_source.trace('w', self.dijkstra_node_detector)
        self.dijkstra_target = tk.StringVar(value="Target")
        self.dijkstra_target.trace('w', self.dijkstra_node_detector)
        self.current_algortihm = tk.StringVar(value = "Select an Algorithm to Apply",)
        self.current_algortihm.trace('w', self.algorithm_detector)
        self.widget_list = []
        self.bicon_image_number = tk.IntVar(value=1)
        self.bicon_image_number.trace('w', self.bicon_image_detector)
        self.scc_image_number = tk.IntVar(value = 1)
        self.scc_image_number.trace('w', self.scc_image_detector)
        self.direction_dict = {}
        self.directed = tk.BooleanVar(value=False)
        self.directed.trace('w', self.display_graph)
        self.weighted = tk.BooleanVar(value=False)
        self.weighted.trace('w', self.display_graph)
        




        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nswe")
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.grid(row = 0, column=0, sticky="nswe")

        self.right_frame= tk.Frame(self.main_frame)
        self.right_frame.grid(row = 0, column=5,  sticky="nswe")

        self.nodebox = tk.Entry(self.left_frame,  font=('Iosevka', 24))
        self.nodebox.grid(row = 0, column=0)
        
        self.edgebox = tk.Entry(self.left_frame, font=('Iosevka', 24))
        self.edgebox.config(state='disabled')
        self.edgebox.grid(row = 2, column=0)

        self.add_button = tk.Button(self.left_frame, text='Add Node', command=self.add_node)
        self.add_button.grid(row = 0, column= 1)

        self.edge_button = tk.Button(self.left_frame, text = 'Add Edges')
        self.edge_button.config(state='disabled')
        self.edge_button.grid(row = 2, column=1)


        self.weight_assign = tk.Frame(self.main_frame)
        self.weight_assign.grid(row = 0, column=3,  sticky="nswe")

        self.add_weight = tk.Button(self.weight_assign, text='Assign Weights', command=self.assign_weights)
        self.add_weight.grid(row = self.edge_count+2, column=1)
        self.add_weight.grid_remove()


        self.direction_assign = tk.Frame(self.main_frame, name = "direction_assign")
        self.direction_assign.grid(row = 0, column=4,  sticky="nswe")
        
        

        self.weight_check = tk.Checkbutton(self.left_frame, text='Weighted', 
                                           variable = self.weight_var, onvalue=True, offvalue=False, command=self.generate_connections)
        self.weight_check.grid(row = 3, column=0)

        self.direction_check = tk.Checkbutton(self.left_frame, text='Directed', 
                                           variable = self.direction_var, onvalue=True, offvalue=False, command=self.generate_directions)
        self.direction_check.grid(row = 4, column=0)
        


        self.clear_button = tk.Button(self.left_frame, text='Clear Graph', command = self.clear_graph)
        self.clear_button.grid(row = 5, column=0)

        self.dropdown_label = tk.Label(self.left_frame, text=  'Choose an Algorithm to apply')
        self.dropdown_label.grid(row = 7, column=0)

        self.drop = tk.OptionMenu(self.left_frame , self.current_algortihm,  *self.algorithms).grid(row = 8, column=0)
                
        self.restart_button = tk.Button(self.right_frame, text = 'Restart', command = lambda: self.restart()).grid(row = 1, column=6)
        
        self.display_graph()
        self.root.mainloop()



    def generate_connections(self):
            if self.edge_count == len(self.graph.es):
                return
            
            self.weight_label = tk.Label(self.weight_assign, text= 'Weights').grid(row = 0, column=0)
            inv_node_dict = {v:k for k, v in self.node_dict.items()}
            
            def f(x):
                return inv_node_dict[x]
            
            for edge in self.graph.es:
                a, b = edge.source, edge.target
                if (a,b) not in self.weight_dict.keys():
                    self.edge_label = tk.Label(self.weight_assign,  text = f'{f(a)} -> {f(b)}').grid(row = self.edge_count+1, column=0)
                    self.weight = tk.Entry(self.weight_assign, name=f'{(a, b)}')
                    self.weight.grid(row = self.edge_count+1, column=1)
                    self.weight_dict.update({(a, b): self.weight, (b, a): self.weight})
                    self.edge_count+=1

            self.add_weight.grid(row = self.edge_count + 2, column=1)
            children = [v for _, v in self.weight_assign.children.items()]
            self.weight_widgets.extend(children)



    def generate_directions(self):
            if self.direction_count == len(self.graph.es):
                return
            self.direction_label = tk.Label(self.direction_assign, text= 'Directions').grid(row = 0, column=0)
            inv_node_dict = {v:k for k, v in self.node_dict.items()}
            
            def f(x):
                return inv_node_dict[x]
            
            self.edge_memory = {}

            def g(a, b):
                inv = {'->':'<-', '<-': '->'}
                self.btn_text.set(inv[self.btn_text.get()])
                bt = self.edge_memory[(a,b)]
                bt.config(text = self.btn_text.get())
                for ix, edge in enumerate(self.edge_list):
                    tmp = (edge[0], edge[1])
                    if  tmp == (a, b):
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
                c = self.direction_count+1
                self.btn_text = tk.StringVar(value = '->')
                self.source_label = tk.Label(self.direction_assign, text = f'{f(a)}').grid(row = c, column=1)
                self.target_label = tk.Label(self.direction_assign, text = f'{f(b)}').grid(row = c, column=3)
                self.direction_button = tk.Button(self.direction_assign, text = self.btn_text.get(), name = f'{(a, b)}').grid(row = c, column=2)

                self.edge_memory[(a,b)] = self.direction_assign.children[f'{(a, b)}']
                self.edge_memory[(a,b)].config(command = lambda a = a, b = b: g(a, b))
                self.direction_count += 1
            
            
    

    def del_direction_widgets(self, *args):
        self.directed.set(not self.directed.get())
        if self.direction_var.get() == False:
            self.direction_count = 0
            self.direction_assign.grid_forget()
            for widget in self.direction_assign.children:
                del widget
        else:
            self.direction_assign.grid(row = 0, column=4,  sticky="nswe")

    def del_weight_widgets(self, *args):
        self.weighted.set(not self.weighted.get())
        if self.weight_var.get() == False:
            self.weight_assign.grid_forget()
        else:
            self.weight_assign.grid(row = 0, column=3,  sticky="nswe")
            

            
    
    def algorithm_detector(self, *args):
        algorithm = self.current_algortihm.get()
        algo_to_function = {'DFS (Depth First Search)': self.apply_dfs, 'Kruskal': self.apply_kruskal, 'Dijkstra': self.apply_dijkstra, 
                            'Find Articulation Points': self.apply_articulation_point, 'Find Bridges': self.apply_find_bridges,
                            'Find Biconnected Components': self.apply_biconnected_components, 'Reverse': self.apply_reverse,
                            'Directed DFS': self.apply_ddfs, 'Find Strongly Connected Components': self.apply_scc, 
                            'Topological Sorting': self.apply_topological_sorting}
        
        try:
            self.algo_frame.grid_remove()
        except:
            pass
        for ix, widget in enumerate(self.widget_list):
            widget.grid_remove()
            self.widget_list.pop(ix)

        self.algo_summary= tk.Label(self.left_frame, text="")
        self.algo_summary.grid(row = 11, column=0)

        return algo_to_function.get(algorithm)()


    def assign_weights(self):
        self.graph_copy = self.graph.copy()
        for edge in self.graph_copy.es:
            edge['weight'] = int(self.weight_dict.get((edge.source, edge.target)).get())
        self.display_graph()

    def show_dropdown(self):
        self.dropdown_label.config( text = self.clicked.get())

    def add_node(self):
        val = self.nodebox.get()
        if val == '' or val in self.node_list:
            pass
        else:
            self.node_list.append(val)
        
        self.get_connections(val)
        self.edgebox.config(state='normal')
        self.edge_button.config(state='normal')
        self.display_graph()

    

    def get_connections(self, node):
        self.edge_button = tk.Button(self.left_frame, text = 'Add Edges', command = lambda: self.add_edges(node))
        self.edge_button.grid(row = 2, column=1)
    
    def add_edges(self, node):
        edges = self.edgebox.get()
        edges = [edge.replace(' ', '') for edge in edges.split(',')]
        edges = [edge for edge in edges if edge]
        self.display_graph()

        for edge in edges:
            if edge not in self.node_list:
                self.node_list.append(edge)

            self.node_dict = {item: self.node_list.index(item) for item in self.node_list}
            k, v = self.node_dict.get(node), self.node_dict.get(edge)
            if (k, v) not in self.edge_list and edge != node:
                self.edge_list.append((k, v))
        self.edgebox.delete(0, tk.END)
        self.nodebox.delete(0, tk.END)
        self.edgebox.config(state='disabled')
        self.edge_button.config(state='disabled')
        self.display_graph()


    def display_graph(self, *args):
        self.graph = ig.Graph(n = len(self.node_list), edges = self.edge_list, directed = self.directed.get())
        graph = self.graph
        graph.vs['name'] = self.node_list
        try:
            graph.es['weight'] = self.graph_copy.es['weight']
        except:
            pass
        plotter(graph, self.weighted.get())
        img = Image.open(os.path.join(os.getcwd(), 'tmp', 'graph.png'))
        photo_image = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self.right_frame, text="Preview", font=('Iosevka', 24))
        self.image_label.grid(row = 1, column=5)
        self.image_frame = tk.Label(self.right_frame, image=photo_image)
        self.image = photo_image
        self.image_frame.grid(row = 2, column=5, rowspan=2, columnspan=2)

    def get_dijkstra_nodes(self):
        return self.dijkstra_source.get(), self.dijkstra_target.get()
    
    def dijkstra_node_detector(self, *args):
        return self.apply_dijkstra(self.dijkstra_source, self.dijkstra_target)

    def dfs_node_detector(self, *args):
        return self.apply_dfs(self.dfs_node.get())
    
    def ddfs_node_detector(self, *args):
        self.algo_summary.config(text = "")
        return self.apply_ddfs(self.ddfs_node.get())


    def apply_dijkstra(self, source = None, target = None):
        try:
            self.graph.es['weight']
        except:
            self.algo_summary = tk.Label(self.left_frame, text='Dijkstra requires a weighted graph, but this graph is not.')
            self.algo_summary.grid(row = 11, column=0)
            self.widget_list.append(self.algo_summary)
            return
        
        if not self.graph.is_connected():
            self.algo_summary = tk.Label(self.left_frame, text='Dijkstra requires connected graphs, but this graph is not (directed graphs are not connected).')
            self.algo_summary.grid(row = 11, column=0)
            self.widget_list.append(self.algo_summary)
            return

        self.dijkstra_source_drop = tk.OptionMenu(self.left_frame, self.dijkstra_source, *self.node_list)
        self.dijkstra_source_drop.grid(row = 10, column = 0)
        self.dijkstra_target_drop = tk.OptionMenu(self.left_frame, self.dijkstra_target, *self.node_list)
        self.dijkstra_target_drop.grid(row = 10, column = 1)
        
        source, target = self.get_dijkstra_nodes()
        if source != "Source" and target != "Target":
            source, target = self.node_dict[source], self.node_dict[target]
            (_, path_str, dijkstra_graph) = dijkstra(self.graph, source, target)

            self.algo_summary = tk.Label(self.left_frame, text=path_str)
            self.algo_summary.grid(row = 11, column=0)

            ig.plot(dijkstra_graph, os.path.join('tmp', 'dijkstra_graph.png'), vertex_label = self.graph.vs['name'],
                     bbox= self.png_size, edge_label = dijkstra_graph.es['weight'], vertex_size = 40)
            self.display_algorithm("dijkstra_graph.png", 12, 0)

        self.widget_list.extend([self.dijkstra_source_drop, self.algo_summary, self.dijkstra_target_drop])
        

    def apply_dfs(self, node = None):
        self.node_drop = tk.OptionMenu(self.left_frame, self.dfs_node, *self.node_list)
        self.node_drop.grid(row=10, column=0)

        x = node
        if x in self.node_list:
            path, dfs_graph = dfs(self.graph, self.node_dict.get(x))
            path = f'The path of DFS is {path}.'
            self.algo_summary = tk.Label(self.left_frame, text=path)
            self.algo_summary.grid(row = 11, column=0)
            ig.plot(dfs_graph, os.path.join('tmp', 'dfs_graph.png'), vertex_label = self.graph.vs['name'], bbox= self.png_size, vertex_size = 40)
            self.display_algorithm("dfs_graph.png", 12, 0)

        self.widget_list.extend([self.node_drop, self.algo_summary])


    def apply_kruskal(self):
        if not self.weighted.get() or not self.graph.is_connected():
            self.algo_summary= tk.Label(self.left_frame, text=f"Kruskal requires a weighted and connected graph, but this graph is not.")
            self.algo_summary.grid(row = 11, column=0)
            self.widget_list.append(self.algo_summary)
            return


        cost, mst, _ = kruskal(self.graph)
        self.algo_summary= tk.Label(self.left_frame, text=f"Minimum spanning tree with a cost of {cost}")
        self.algo_summary.grid(row = 11, column=0)
        self.widget_list.append(self.algo_summary)

        ig.plot(mst, os.path.join('tmp', 'kruskal_graph.png'), vertex_label = self.graph.vs['name'], edge_label = self.graph.es['weight'], bbox=self.png_size, vertex_size = 40)
        self.display_algorithm("kruskal_graph.png", 12, 0)

    def apply_articulation_point(self):
        graph_aps, aps_named, _ = articulation_point(self.graph)
        txt = ', '.join(aps_named)

        if aps_named:
            txt = f"The articulation points are: {txt}."
        else:
            txt = "There are no articulation points for this graph."

        self.algo_summary= tk.Label(self.left_frame, text=txt)
        self.algo_summary.grid(row = 11, column=0)
        ig.plot(graph_aps, os.path.join('tmp', 'articulation_points_graph.png'), vertex_label = graph_aps.vs['name'], bbox = self.png_size, vertex_size = 40)
        self.display_algorithm('articulation_points_graph.png', 12, 0)
        self.widget_list.append(self.algo_summary)

    def apply_find_bridges(self):
        bridges_named, bridged_graph = find_bridges(self.graph)
        txt = ''
        for ix, edge in enumerate(bridges_named):
            txt += ' -> '.join(edge)
            if ix != len(bridges_named) - 1:
                txt += ', '
        if bridges_named:
            txt = f'The bridges are: {txt}.'
        else:
            txt = 'There are no bridges on this graph.'
        self.algo_summary= tk.Label(self.left_frame, text=txt)
        self.algo_summary.grid(row = 11, column=0)
        ig.plot(bridged_graph, os.path.join('tmp', 'bridges_graph.png'), vertex_label = bridged_graph.vs['name'], bbox = self.png_size, vertex_size = 40)
        self.display_algorithm('bridges_graph.png', 12, 0)

        self.widget_list.append(self.algo_summary)
    
    
    def apply_biconnected_components(self):
        bicons = biconnected_components(self.graph)
        if not bicons:
            self.algo_summary= tk.Label(self.left_frame, text= f'There are no biconnected components of this graph.')
            self.algo_summary.grid(row = 11, column=1)
            return
        
        self.bicon_count = len(bicons)
        for ix, bicon in enumerate(bicons):
            ig.plot(bicon, os.path.join('tmp', f'bicon_graph_{ix+1}.png'), vertex_label = bicon.vs['name'], bbox = self.png_size, vertex_size = 40)

        self.display_algorithm(f'bicon_graph_1.png', 13, 1)


        self.algo_summary= tk.Label(self.left_frame, text= f'There are {len(bicons)} biconnected components of this graph.')
        self.algo_summary.grid(row = 11, column=1)

        
        self.prev_button = tk.Button(self.left_frame, text='<', command=self.prev_bicon_image)
        self.prev_button.grid(row = 12, column= 0)

        self.bicon_index = tk.Label(self.left_frame, text= f'{self.bicon_image_number.get()}')
        self.bicon_index.grid(row = 12, column=1)


        self.next_button = tk.Button(self.left_frame, text='>', command=self.next_bicon_image)
        self.next_button.grid(row = 12, column= 2)

        self.widget_list.extend([self.algo_summary, self.prev_button, self.next_button, self.bicon_index])



    def apply_ddfs(self, node = None):
        self.ddfs_node_drop = tk.OptionMenu(self.left_frame, self.ddfs_node, *self.node_list)
        self.ddfs_node_drop.grid(row=10, column=0)
        self.algo_summary= tk.Label(self.left_frame, text = "")
        self.algo_summary.grid(row = 11, column=0)
        self.widget_list.extend([self.ddfs_node_drop, self.algo_summary])

        if node is None:
            return
        if node in self.node_list:
            path, ddfs_graph = ddfs(self.graph, self.node_dict.get(node), tail = [], edges = [])
            inv_node_dict = {v:k for k, v in self.node_dict.items()}
            if len(path) == 1:
                self.algo_summary.config(text = f"Node {node} is a terminal node.")
                self.algo_summary.grid()
                return
            path_str = "The path of Directed DFS is: "
            path_str += '->'.join([inv_node_dict.get(x) for x in path])
            self.algo_summary.config(text= path_str)
            self.algo_summary.grid(row = 11, column=0)

            ig.plot(ddfs_graph, os.path.join('tmp', 'ddfs_graph.png'), vertex_label = ddfs_graph.vs['name'], bbox = self.png_size, vertex_size = 40)
            self.display_algorithm('ddfs_graph.png', 12, 0)

    def apply_reverse(self):
        reversed_graph = self.graph.copy()
        reversed_graph = reverse(reversed_graph)
        ig.plot(reversed_graph, os.path.join('tmp', 'reversed_graph.png'), vertex_label = reversed_graph.vs['name'], bbox = self.png_size, vertex_size = 40)
        self.display_algorithm('reversed_graph.png', 12, 0)
    
    
    def apply_scc(self):
        ret = strongly_connected_components(self.graph.copy())

        if type(ret) == list:
            ret = [g for g in ret if len(g.vs) > 1]
            if len(ret) == 0:
                self.algo_summary= tk.Label(self.left_frame, text = "There are no strongly connected components for this graph.")
                self.algo_summary.grid(row = 11, column=0)
                self.widget_list.append(self.algo_summary)
                return

        if type(ret) == str:
            self.algo_summary= tk.Label(self.left_frame, text = ret)
            self.algo_summary.grid(row = 11, column=0)
            self.widget_list.append(self.algo_summary)
            return
        else:
            for ix, sg in enumerate(ret):
                    ig.plot(sg, os.path.join('tmp', f'scc_graph_{ix+1}.png'), vertex_label = sg.vs['name'], bbox = self.png_size, vertex_size = 40)

            self.scc_count = len(ret)
            self.algo_summary= tk.Label(self.left_frame, text= f'There are {len(ret)} strongly connected components of this graph.')
            self.algo_summary.grid(row = 11, column=1)

        
            self.prev_button = tk.Button(self.left_frame, text='<', command=self.prev_scc)
            self.prev_button.grid(row = 12, column= 0)

            self.scc_index = tk.Label(self.left_frame, text= f'{self.scc_image_number.get()}')
            self.scc_index.grid(row = 12, column=1)


            self.next_button = tk.Button(self.left_frame, text='>', command=self.next_scc)
            self.next_button.grid(row = 12, column= 2)
            self.display_algorithm(f'scc_graph_1.png', 13, 1)

            self.widget_list.extend([self.algo_summary, self.prev_button, self.next_button, self.scc_index])


    def apply_topological_sorting(self):
        pass
            


    def bicon_image_detector(self, *args):
        self.display_algorithm(f'bicon_graph_{self.bicon_image_number.get()}.png', 13, 1)

    def next_bicon_image(self):
        x = self.bicon_image_number.get()
        if x < self.bicon_count:
            self.bicon_image_number.set(x+1)
            self.bicon_index.config(text = f'{self.bicon_image_number.get()}')


    def prev_bicon_image(self):
        x = self.bicon_image_number.get()
        if x > 1:
            self.bicon_image_number.set(x-1)
            self.bicon_index.config(text = f'{self.bicon_image_number.get()}')

    def scc_image_detector(self, *args):
        self.display_algorithm(f'scc_graph_{self.scc_image_number.get()}.png', 13, 1)

    def next_scc(self):
        x = self.scc_image_number.get()
        if x < self.scc_count:
            self.scc_image_number.set(x+1)
            self.scc_index.config(text = f'{self.scc_image_number.get()}')

    def prev_scc(self):
        x = self.scc_image_number.get()
        if x > 1:
            self.scc_image_number.set(x-1)
            self.scc_index.config(text = f'{self.scc_image_number.get()}')

    


    def display_algorithm(self, filename, row, column):
        img = Image.open(os.path.join(os.getcwd(), 'tmp', filename))
        photo_image = ImageTk.PhotoImage(img)
        self.algo_frame = tk.Label(self.left_frame, image=photo_image)
        self.algo_image = photo_image
        self.algo_frame.grid(row = row, column = column)


    def clear_graph(self):
        self.node_list = []
        self.node_dict = {}
        self.edge_list = []



    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

UI() 