import networkx as nx
import scipy as sp
from scipy import sparse
import numpy as np

class Problem(object):
	def __init__(self, data, startidx=0, endidx=0, capacity=0.0):
		# TODO: Maybe consider some numpy datatypes.
		self.nodes = data["nodes"]
		self.edges = data["edges"]
		self.lengths = data["lengths"]
		self.scores = data["scores"]
		self.grid_cells_x = data["grid_cells_x"]
		self.grid_cells_y = data["grid_cells_y"]
		self.min_node = data["min_node"]
		self.max_node = data["max_node"]
		self.adj = data["adj"]
		self.capacity = capacity
		self.nnodes = len(self.nodes)
		self.nedges = len(self.edges)
		self.startidx = startidx
		self.endidx = endidx
		self.graph = nx.Graph()
		for i, edge in enumerate(self.edges):
			self.graph.add_edge(edge[0], edge[1], length=self.lengths[i], score=self.scores[i])

		self.distmatrix = sp.sparse.csgraph.shortest_path(self.adj, directed=False) # if len(data["distmatrix"]) == 0 else data["distmatrix"]
		self.nodes = self.graph.nodes()
		self.shortest_path = nx.shortest_path(self.graph, startidx, endidx, "length")
		self.shortest_path_length = nx.shortest_path_length(self.graph, startidx, endidx, "length")
		self.init_score = self.init_score()

	def init_score(self):
		d = 0
		g = self.graph
		for node, next_node in zip(self.shortest_path, self.shortest_path[1:]):
			d += g[node][next_node]["score"]
		return d
