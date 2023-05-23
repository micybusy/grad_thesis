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
        self.algorithms = ['DFS', 'Kruskal', 'Dijkstra']
        self.weight_var = tk.BooleanVar()
        self.weight_var = False
        self.root.title('Graph Theory')
        self.root.geometry('1200x600')
        self.clicked = tk.StringVar()
        self.clicked.set( "Algorithm" )
        self.dfs_node = tk.StringVar(value = "DFS Node")
        self.dfs_node.trace('w', self.dfs_node_detector)
        self.png_size = (0, 0, 500, 300)
        self.edge_count = 0
        self.dijkstra_source = tk.StringVar(value = "Source")
        self.dijkstra_source.trace('w', self.dijkstra_node_detector)
        self.dijkstra_target = tk.StringVar(value="Target")
        self.dijkstra_target.trace('w', self.dijkstra_node_detector)
        self.current_algortihm = tk.StringVar(value = "Select an Algorithm to Apply",)
        self.current_algortihm.trace('w', self.algorithm_detector)
        


        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nswe")
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.grid(row = 0, column=0, sticky="nswe")

        self.right_frame= tk.Frame(self.main_frame)
        self.right_frame.grid(row = 0, column=3,  sticky="nswe")

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
        self.weight_assign.grid(row = 0, column=2,  sticky="nswe")


        self.add_weight = tk.Button(self.weight_assign, text='Assign Weights', command=self.assign_weights)
        self.add_weight.grid(row = int(self.edge_count/2), column=3)
        

        self.weight_check = tk.Checkbutton(self.left_frame, text='Weighted', 
                                           variable = self.weight_var, onvalue=True, offvalue=False, command=self.generate_connections)
        self.weight_check.grid(row = 3, column=0)


        self.clear_button = tk.Button(self.left_frame, text='Clear Graph', command = self.clear_graph)
        self.clear_button.grid(row = 5, column=0)

        self.dropdown_label = tk.Label(self.left_frame, text=  'Choose an Algorithm to apply')
        self.dropdown_label.grid(row = 7, column=0)

        self.drop = tk.OptionMenu(self.left_frame , self.current_algortihm,  *self.algorithms)
        self.drop.grid(row = 8, column=0)

        
        self.restart_button = tk.Button(self.right_frame, text = 'Restart', command = lambda: self.restart())
        self.restart_button.grid(row = 1, column=4)
        
        self.display_graph()
        self.root.mainloop()



    def generate_connections(self):
            if self.edge_count == len(self.graph.es):
                return
            self.weight_label = tk.Label(self.weight_assign, text= 'Weights')
            self.weight_label.grid(row = 0, column=0)
            inv_node_dict = {v:k for k, v in self.node_dict.items()}
            
            def f(x):
                return inv_node_dict[x]
            
            for edge in self.graph.es:
                a, b = edge.source, edge.target
                if (a,b) not in self.weight_dict.keys():
                    self.edge_label = tk.Label(self.weight_assign, text = f'{f(a)} -> {f(b)}')
                    self.edge_label.grid(row = self.edge_count+1, column=0)
                    self.weight = tk.Entry(self.weight_assign)
                    self.weight.grid(row = self.edge_count+1, column=1)
                    self.weight_dict.update({(a, b): self.weight})
                    self.edge_count+=1

            self.add_weight.grid(row = int(self.edge_count/2), column=3)
            
    
    def algorithm_detector(self, *args):
        algorithm = self.current_algortihm.get()
        algo_to_function = {'DFS': self.apply_dfs, 'Kruskal': self.apply_kruskal, 'Dijkstra': self.apply_dijkstra}
        self.algo_summary= tk.Label(self.left_frame, text="")
        self.algo_summary.grid(row = 11, column=0)
        return algo_to_function.get(algorithm)()


    def assign_weights(self):
        self.graph_copy = self.graph.copy()
        for edge in self.graph_copy.es:
            edge['weight'] = int(self.weight_dict.get((edge.source, edge.target)).get())
        self.weight_var = True
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
            if [k, v] not in self.edge_list and edge != node:
                self.edge_list.append([k, v])
        self.edgebox.delete(0, tk.END)
        self.nodebox.delete(0, tk.END)
        self.edgebox.config(state='disabled')
        self.edge_button.config(state='disabled')
        self.display_graph()



    def display_graph(self):
        self.graph = ig.Graph(n = len(self.node_list), edges = self.edge_list, directed = False)
        graph = self.graph
        graph.vs['name'] = self.node_list
        try:
            graph.es['weight'] = self.graph_copy.es['weight']
        except:
            pass
        plotter(graph, self.weight_var)
        img = Image.open(os.path.join(os.getcwd(), 'tmp', 'graph.png'))
        photo_image = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self.right_frame, text="Preview", font=('Iosevka', 24))
        self.image_label.grid(row = 1, column=3)
        self.image_frame = tk.Label(self.right_frame, image=photo_image)
        self.image = photo_image
        self.image_frame.grid(row = 2, column=3, rowspan=2, columnspan=2)

    def get_dijkstra_nodes(self):
        return self.dijkstra_source.get(), self.dijkstra_target.get()
    
    def dijkstra_node_detector(self, *args):
        return self.apply_dijkstra(self.dijkstra_source, self.dijkstra_target)



    def apply_dijkstra(self, source = None, target = None):
        self.dijkstra_source_drop = tk.OptionMenu(self.left_frame, self.dijkstra_source, *self.node_list)
        self.dijkstra_source_drop.grid(row = 10, column = 0)
        self.dijkstra_target_drop = tk.OptionMenu(self.left_frame, self.dijkstra_target, *self.node_list)
        self.dijkstra_target_drop.grid(row = 10, column = 1)
        source, target = self.get_dijkstra_nodes()
        if source != "Source" and target != "Target":
            source, target = self.node_dict[source], self.node_dict[target]
            _, path_str, dijkstra_graph = dijkstra(self.graph, source, target)

            self.algo_summary = tk.Label(self.left_frame, text=path_str)
            self.algo_summary.grid(row = 11, column=0)

            ig.plot(dijkstra_graph, os.path.join('tmp', 'dijkstra_graph.png'), vertex_label = self.graph.vs['name'],
                     bbox= self.png_size, edge_label = dijkstra_graph.es['weight'])
            self.display_algorithm("dijkstra_graph.png")
            



    def dfs_node_detector(self, *args):
        return self.apply_dfs(self.dfs_node.get())
    

    def apply_dfs(self, node = None):
        self.node_drop = tk.OptionMenu(self.left_frame, self.dfs_node, *self.node_list)
        self.node_drop.grid(row=10, column=0)
        x = node
        if x in self.node_list:
            path, dfs_graph = dfs(self.graph, self.node_dict.get(x))
            self.algo_summary = tk.Label(self.left_frame, text=path)
            self.algo_summary.grid(row = 11, column=0)
            ig.plot(dfs_graph, os.path.join('tmp', 'dfs_graph.png'), vertex_label = self.graph.vs['name'], bbox= self.png_size)
            self.display_algorithm("dfs_graph.png")


    def apply_kruskal(self):
        cost, mst, _ = kruskal(self.graph)
        self.algo_summary= tk.Label(self.left_frame, text=f"Minimum spanning tree with a cost of {cost}")
        self.algo_summary.grid(row = 11, column=0)
        ig.plot(mst, os.path.join('tmp', 'kruskal_graph.png'), vertex_label = self.graph.vs['name'], bbox=self.png_size)
        self.display_algorithm("kruskal_graph.png")


    def display_algorithm(self, filename):
        img = Image.open(os.path.join(os.getcwd(), 'tmp', filename))
        photo_image = ImageTk.PhotoImage(img)
        self.algo_frame = tk.Label(self.left_frame, image=photo_image)
        self.algo_image = photo_image
        self.algo_frame.grid(row = 12, column=0)


    def clear_graph(self):
        self.node_list = []
        self.node_dict = {}
        self.edge_list = []



    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

UI() 