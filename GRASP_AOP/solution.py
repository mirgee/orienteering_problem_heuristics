from insertion import Insertion
from itertools import chain
import networkx as nx
import random
import sys


class Solution:
	"""Sequence of arcs"""
	def __init__(self, problem):
		# TODO: Initialize solution by inserting random arc
		self.edges_set = set()
		self.edges_list = []
		self.nodes = [problem.startidx, problem.endidx]
		# self.nodes = problem.shortest_path
		self.unvisited_nodes = set(problem.nodes) - set(self.nodes)
		self.problem = problem
		self.score = 0  # problem.init_score
		self.cost = 0  # problem.shortest_path_length
		self.iters = 0
		self.rem_dist = problem.capacity - self.cost
		self.dist_cache = {}
		self.score_cache = {}

	def __repr__(self):
		return str(self.nodes)

	def del_cost(self, ins):
		"""Compute the total cost after removing the item"""
		position = ins.start_position
		return self.cost - self.cost_delta(ins.arc, position)

	def mk_ins(self, arc, start_position, end_position):
		"""Build an appropriate insertion candidate"""
		ins = Insertion(arc, start_position, end_position)
		d = self.problem.distmatrix
		node1 = self.nodes[start_position]
		node2 = self.nodes[end_position]
		l = self.problem.graph[arc[0]][arc[1]]["length"]

		# Nezarucuju ze ta nejkratsi cesta nevede pres uz nalezene reseni -> hrany se muzou opakovat
		d1 = d[node1, arc[0]] + l + d[arc[1], node2]
		d2 = d[node1, arc[1]] + l + d[arc[0], node2]

		# if d1 < d2:
		# 	cost_delta = d1 - self.compute_dist(start_position, end_position)
		# else:
		# 	cost_delta = d2 - self.compute_dist(start_position, end_position)
		#
		# ins.add_cost = self.cost+cost_delta
		# TODO: This heuristic value is incorrect if cost_delta is negative!
		# ins.hval = self.problem.graph[arc[0]][arc[1]]["score"] / (cost_delta + 0.000001)
		ins.hval = self.problem.graph[arc[0]][arc[1]]["score"] / (min(d1, d2) + 0.000001)
		return ins

	def insert_ins(self, ins):
		"""Insert insertion candidate ins to the current solution."""
		source1 = self.nodes[ins.start_position]
		target1 = ins.arc[0]
		source2 = ins.arc[1]
		target2 = self.nodes[ins.end_position]

		path1 = nx.shortest_path(self.problem.graph, source1, target1, "length")
		path2 = nx.shortest_path(self.problem.graph, source2, target2, "length")

		# The endpoints are included
		path = path1[1:-1] + [ins.arc[0], ins.arc[1]] + path2[1:-1]

		# Cut the edge still if path1 or path2 are empty
		if len(path1) <= 1:
			path = path[1:]
		if len(path2) <= 1:
			path = path[:-1]

		# Insert the path
		# This is OK even if there is only an edge between them - path is empty - but still need to add the edge
		self.nodes[ins.start_position+1:ins.end_position] = path

		# We must delete the edges in self.nodes[ins.start_position+1:ins.end_position] from edges before deleting them
		self.edges_set -= {chain.from_iterable(((a,b),(b,a)) for (a,b) in zip(self.nodes[ins.start_position+1:ins.end_position],self.nodes[ins.start_position+2:ins.end_position+1]))}

		# NOT CACHEABLE!
		self.cost = self.compute_dist(0, len(self.nodes))
		self.score = self.compute_score(0, len(self.nodes))
		self.rem_dist = self.problem.capacity - self.cost

		d = self.problem.distmatrix
		# Remove all nodes which can't be reached with current rem_dist from added nodes
		self.unvisited_nodes = {node for node in self.unvisited_nodes - set(path) if d[ins.arc[0]][node] + d[node][self.problem.endidx] <= self.rem_dist or \
		                        d[ins.arc[1]][node] + d[node][self.problem.endidx] <= self.rem_dist}


	def compute_dist(self, start, end):
		"""Find distance from start to end along the route"""
		d = 0
		g = self.problem.graph
		# if (start, end) in self.dist_cache:
		# 	return self.dist_cache[(start, end)]
		# Temporary quick fix
		if len(self.nodes) <= 2:
			return 0
		for node, next_node in zip(self.nodes[start:end+1], self.nodes[start+1:end+1]):
			d += g[node][next_node]["length"] if node != next_node else 0
		# self.dist_cache[(start, end)] = d
		return d

	def compute_score(self, start, end):
		"""Find score from start to end along the route"""
		d = 0
		g = self.problem.graph
		# if (start, end) in self.score_cache:
		# 	return self.score_cache[(start, end)]
		# Temporary quick fix - what if first insertion is just the edge between start and end?
		if len(self.nodes) <= 2:
			return 0
		for node, next_node in zip(self.nodes[start:end+1], self.nodes[start+1:end+1]):
			# We must mark edges as visited while we are traversing them here, not in batch with insertion, because even here they can be visited twice
			if node != next_node and (node, next_node) not in self.edges_set:
				d += g[node][next_node]["score"]
				self.edges_set.update({(node, next_node), (next_node, node)})
		# self.score_cache[(start, end)] = d
		return d

	def avail_arcs(self, node, end_node):
		"""List of arcs which are reachable from node in rem_dist"""
		d = self.problem.distmatrix
		g = self.problem.graph
		r = self.rem_dist
		arcs = []
		# TODO: Is unvisited correct here? We don't mind repeated nodes, but repeated edges have zero score and thus (theoretically) 0 p. of being added
		for n in filter(lambda n: d[node, n] + d[n, end_node] < r, self.unvisited_nodes):
			for m in filter(lambda m: g[n][m]["length"] + d[node, n] + d[m, end_node] <= r and (m, n) not in self.edges_set,
						g.neighbors(n)):
				arcs.append((n,m))
		return arcs

	def pick_random_ins(self):
		i = random.randint(0, len(self.nodes)-2)
		j = random.randint(i+1, len(self.nodes)-1)
		return i, j, self.nodes[i], self.nodes[j]

	def swap_cost_delta(self, l, m):
		"""Calculates the cost after a swap."""
		d = self.problem.distmatrix
		# TODO: Solve out of range edge cases.
		n1 = self.nodes[l-1] if l >= 1 else self.nodes[l]
		n2 = self.nodes[l]
		n3 = self.nodes[m]
		n4 = self.nodes[m+1] if m +1 < len(self.nodes) else self.nodes[m]
		return -d[n1,n2] + d[n1,n3] - d[n3,n4] + d[n2,n4]

	def swap_score_delta(self, l, m):
		"""Calculates the score after a swap."""
		pass

	def local_search(self):
		"""Perform 2-opt local search procedure on the current solution."""
		# Minimizing only cost. Should consider score as well.
		improvement = sys.maxsize
		while improvement > 0.0001:
			best_i, best_j = 0, 0
			for i, n in enumerate(self.nodes):
				for j, m in enumerate(self.nodes[i+1:]):
					delta = self.swap_cost_delta(i, i+j+1)
					if improvement > delta:
						improvement = delta
						best_i, best_j = i, j
			# Perform 2-opt
			# TODO: Does this always work properly?
			self.nodes[best_i:best_j] = self.nodes[best_i:best_i:-1]
			# Recalculate score and cost
			self.score = self.compute_score(0, len(self.nodes))
			self.cost = self.compute_dist(0, len(self.nodes))
