import pandas as pd
import numpy as np

class loader:
	"""Loads the data from a file and converts them to a problem instance"""

	# We should make it possible to read edge data in several formats
	# and allow for reading the distance matrix instead of generating it

	def __init__(self, edges_filename, dist_filename = ""):
		self.edges_filename = edges_filename
		self.dist_filename = dist_filename
		self.data = {
			"nodes" : [],
			"edges" : [],
			# "start" : 0,
			# "end" : 0,
			"lengths" : [],
			"scores" : [],
			"grid_cells_x": [],
			"grid_cells_y": [],
			"max_node": -100000,
			"min_node": 100000,
			"adj": [],
			"distmatrix": []
		}
		self.adj = np.zeros((553, 553))
		self.adj[:] = np.inf

	def read_edges(self, headers=True):
		"""Fills in the data"""
		with open(self.edges_filename, mode="r") as f:
			if headers:
				f.readline()
			for l in f.readlines():
				l = list(map(float, l.split(' ')))
				self.data["edges"].append((int(l[0]),int(l[1])))
				self.data["lengths"].append(l[2])
				self.data["scores"].append(l[3])
				self.data['grid_cells_x'].append(l[4])
				self.data["grid_cells_y"].append(l[5])
				self.data["max_node"] = max(l[0], l[1], self.data["max_node"])
				self.data["min_node"] = min(l[0], l[1], self.data["min_node"])
				self.adj[int(l[0])][int(l[1])] = l[2]
				self.adj[int(l[1])][int(l[0])] = l[2]
		self.data["adj"] = self.adj

	def read_distmatrix(self):
		self.data["distmatrix"] = pd.read_csv(self.dist_filename, sep=" ", header=None)
