import tkinter as tk
from algorithms import *
from samples import *
from genesis import *
import igraph as ig


class UI:

    def __init__(self):
        self.node_list = []
        self.edge_list = []
        self.row_count = 1
        self.root = tk.Tk()
        self.root.title('Graph Theory')
        self.root.geometry('1000x500')

        self.nodebox = tk.Entry(self.root,  font=('Iosevka', 24))
        self.nodebox.grid(row = 0, column=0)
        
        self.edgebox = tk.Entry(self.root, font=('Iosevka', 24))
        self.edgebox.config(state='disabled')
        self.edgebox.grid(row = 2, column=0)

        self.edge_button = tk.Button(self.root, text = 'Add Edges')
        self.edge_button.config(state='disabled')
        self.edge_button.grid(row = 2, column=1)

        self.add_button = tk.Button(self.root, text='Add Node', command=self.add_node)
        self.add_button.grid(row = 0, column= 1)

        self.display_button = tk.Button(self.root, text='Display Graph', command = self.display_graph)
        self.display_button.grid(row = 3, column=0)

        self.display_button = tk.Button(self.root, text='Clear Graph', command = self.clear_graph)
        self.display_button.grid(row = 4, column=0)

        self.root.mainloop()

    def add_node(self):
        val = self.nodebox.get()
        if val == '' or val in self.node_list:
            pass
        else:
            self.node_list.append(val)
        
        self.get_connections(val)
        self.edgebox.config(state='normal')
        self.edge_button.config(state='normal')


        print('Node list', self.node_list)
        

    def get_connections(self, node):
        self.edge_button = tk.Button(self.root, text = 'Add Edges', command = lambda: self.add_edges(node))
        self.edge_button.grid(row = 2, column=1)
    
    def add_edges(self, node):
        edges = self.edgebox.get()
        edges = [edge.replace(' ', '') for edge in edges.split(',')]
        edges = [edge for edge in edges if edge != '']
        print('edges', edges)
        
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
        print(f'Edge list {self.edge_list}')



    def display_graph(self):
        self.graph = ig.Graph(n = len(self.node_list), edges = self.edge_list, directed = False)
        graph = self.graph
        graph.vs['name'] = self.node_list
        plotter(graph, False)

    def clear_graph(self):
        self.node_list = []
        self.node_dict = {}
        self.edge_list = []



        

UI() 