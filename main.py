import tkinter as tk
from algorithms import *
from samples import *
from genesis import *
import igraph as ig
from PIL import ImageTk, Image
import os

class UI:

    def __init__(self):
        self.node_list = []
        self.edge_list = []
        self.weights = []
        self.row_count = 1
        self.root = tk.Tk()
        self.algorithms = ['DFS', 'Kruskal']
        self.weight_var = tk.BooleanVar()
        self.root.title('Graph Theory')
        self.root.geometry('1200x600')
        self.clicked = tk.StringVar()
        self.clicked.set( "Algorithm" )


        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nswe")
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.grid(row = 0, column=0, sticky="nswe")

        self.right_frame= tk.Frame(self.main_frame)
        self.right_frame.grid(row = 0, column=1,  sticky="nswe")

        self.nodebox = tk.Entry(self.left_frame,  font=('Iosevka', 24))
        self.nodebox.grid(row = 0, column=0)
        
        self.edgebox = tk.Entry(self.left_frame, font=('Iosevka', 24))
        self.edgebox.config(state='disabled')
        self.edgebox.grid(row = 2, column=0)

        self.weightbox = tk.Entry(self.left_frame, font=('Iosevka', 24))
        self.weightbox.config(state='disabled')
        self.weightbox.grid(row = 4, column=0)



        self.add_button = tk.Button(self.left_frame, text='Add Node', command=self.add_node)
        self.add_button.grid(row = 0, column= 1)

        self.edge_button = tk.Button(self.left_frame, text = 'Add Edges')
        self.edge_button.config(state='disabled')
        self.edge_button.grid(row = 2, column=1)

        self.add_weight = tk.Button(self.left_frame, text='Assign Weights', command=self.assign_weights)
        self.add_weight.grid(row = 4, column=1)
        

        self.weight_check = tk.Checkbutton(self.left_frame, text='Weighted', 
                                           variable = self.weight_var, onvalue=True, offvalue=False, command=self.assign_weights)
        self.weight_check.grid(row = 3, column=0)

        #self.display_button = tk.Button(self.root, text='Display Graph', command = self.display_graph)
        #self.display_button.grid(row = 3, column=0)

        self.clear_button = tk.Button(self.left_frame, text='Clear Graph', command = self.clear_graph)
        self.clear_button.grid(row = 5, column=0)

        self.dropdown_label = tk.Label(self.left_frame, text=  'Choose an Algorithm to apply')
        self.dropdown_label.grid(row = 7, column=0)

        self.drop = tk.OptionMenu(self.left_frame , self.clicked , *self.algorithms )
        self.drop.grid(row = 8, column=0)

        self.apply_algorithm_button = tk.Button(self.left_frame, text = 'Apply Algorithm', command = lambda: self.apply_algorithm(self.clicked))
        self.apply_algorithm_button.grid(row = 9, column=0)


        self.display_graph()
        self.root.mainloop()



    def show_dropdown(self):
        self.dropdown_label.config( text = self.clicked.get() )

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
        edges = [edge for edge in edges if edge != '']
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
        self.weightbox.config(state = 'normal')
        self.display_graph()



    def display_graph(self):
        self.graph = ig.Graph(n = len(self.node_list), edges = self.edge_list, directed = False)
        graph = self.graph
        graph.vs['name'] = self.node_list
        if self.weight_var.get() and self.weights:
            graph.es['weight'] = self.weights
        else:
            graph.es['weight'] = len(self.node_list)*[0]
        if self.weights:
            plotter(graph, self.weight_var.get())
        else:
            plotter(graph, False)
        img = Image.open(os.path.join(os.getcwd(), 'tmp', 'graph.png'))
        photo_image = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self.right_frame, text="Preview", font=('Iosevka', 24))
        self.image_label.grid(row = 1, column=2)
        self.image_frame = tk.Label(self.right_frame, image=photo_image)
        self.image = photo_image
        self.image_frame.grid(row = 2, column=2, rowspan=2, columnspan=2)
        self.right_frame.after(5000, self.display_graph)
        
    def assign_weights(self):
        self.weightbox.config(state='normal')
        weights = self.weightbox.get()
        if not weights:
            return len(self.node_list)*[0]
        weights = [int(weight.replace(' ', '')) for weight in weights.split(',')]
        self.weights.extend(weights)
        self.graph.es['weight'] = self.weights
        self.weightbox.delete(0, tk.END)
        self.weightbox.config(state='disabled')
        self.display_graph()


    def apply_algorithm(self, algorithm):
        algo_to_function = {'DFS': self.apply_dfs(self.graph)}
        return algo_to_function.get(algorithm)


    def apply_dfs(self, graph):
        self.selected_node = tk.StringVar()
        self.selected_node.set(self.node_list[0])
        self.node_drop = tk.OptionMenu(self.left_frame, self.selected_node, *self.node_list)
        self.node_drop.grid(row=10, column=0)
        x = self.selected_node.get()
        if x in self.node_list:
            path, dfs_graph = dfs(graph, self.node_dict.get(x), weighted=self.weight_var)
            self.path = tk.Label(self.left_frame, text=path)
            self.path.grid(row = 11, column=0)

            x = self.graph.es['weight'] if self.weight_var else None
            ig.plot(dfs_graph, os.path.join('tmp', 'dfs_graph.png'), vertex_label = self.graph.vs['name'], edge_label = x)

            img = Image.open(os.path.join(os.getcwd(), 'tmp', 'dfs_graph.png'))
            photo_image = ImageTk.PhotoImage(img)
            self.algo_frame = tk.Label(self.left_frame, image=photo_image)
            self.algo_image = photo_image
            self.algo_frame.grid(row = 12, column=0)


    def clear_graph(self):
        self.node_list = []
        self.node_dict = {}
        self.edge_list = []



        

UI() 