import pandas as pd
import numpy as np
import time
import timeit
import csv


def read_edges(edges_filename, headers=True):
	"""
	Reads edges of the searched graph from a given filename.

	:param edges_filename: Relative path to the file containing the graph edges.
	:param headers: Does the file contain headers?
	"""
	with open(edges_filename, mode="r") as f:
		if headers:
			f.readline()
		for l in f.readlines():
			l = list(map(float, l.split(' ')))
			edges.add((int(l[0]), int(l[1])))
			edges.add((int(l[1]), int(l[0])))
			lengths[(l[0], l[1])] = l[2]
			lengths[(l[1], l[0])] = l[2]
			scores[(l[0], l[1])] = l[3]
			scores[(l[1], l[0])] = l[3]

def generate_route(dist, scores, edges, start_node, end_node, tmax):
	"""
	Given distance matrix dist, along with scores, graph edges and path endpoints, calculate and print it.
	Refer to the Tsiligirides' paper for details.

	:param dist: The graph distance matrix.
	:param scores: The edge rewards.
	:param edges: The set of all (oriented) edges.
	:param start_node: The starting node.
	:param end_node: The end node.
	:param tmax: The route length limit.
	:return: The list of edges along the optimal path.
	"""
	curr_node = start_node
	rem_dist = tmax
	unvisited = edges.copy()
	total_score = 0
	path = []
	while True:
		# Construct all nodes reachable given current state
		feasible = np.fromiter((e for e in edges if curr_node != e[0] and
				dist[curr_node, e[0]] + lengths[(e[0], e[1])] + dist[end_node, e[1]] <= rem_dist), dtype=np.dtype('int,int'))

		# If there is no such node, finish
		if len(feasible) == 0:
			break
		# Heuristic for edge values
		A = np.fromiter(((scores[(e[0], e[1])]/dist[curr_node, e[0]])**4 for e in feasible), np.float)
		den = np.nansum(A, axis=0, dtype=np.float)
		if den == 0:
			break
		# Probability of visit
		P = np.divide(A, den)
		# Pick one edge using computed distribution
		next_edge = np.random.choice(feasible, 1, p=P)[0]
		# Find path to the first node, recompute state variables
		total_score, unvisited, path = reward_from_path(curr_node, next_edge[0], unvisited, total_score, path)
		total_score += scores[(next_edge[0], next_edge[1])]
		path += [next_edge[1]]
		unvisited -= {(next_edge[0], next_edge[1]), (next_edge[1], next_edge[0])}
		rem_dist -= dist[curr_node, next_edge[0]] + lengths[(next_edge[0], next_edge[1])]
		curr_node = int(next_edge[1])

	# If necessary, traverse to the end
	# total_score, unvisited, path = reward_from_path(curr_node, end_node, unvisited, total_score, path)
	print(path, total_score, rem_dist)
	return total_score


def reward_from_path(curr_node, next_node, unvisited, total_score, path):
	"""
	Compute reward obtain by traversing from current node to the next node, considering only unvisited nodes.

	:param curr_node: Current node on the path.
	:param next_node: Planned following node.
	:param unvisited: List of unvisited edges.
	:param total_score: Total score accumulated so far.
	:param path: Path traversed so far..
	:return:
	"""
	# total_score += scores[next_edge]
	previous_node = next_node
	new_path = [next_node]
	while previous_node != curr_node:
		previous_pred = previous_node
		previous_node = pred[curr_node, previous_node]
		new_path.insert(0, previous_node)
		if (previous_node, previous_pred) in unvisited:
			total_score += scores[(previous_node, previous_pred)]
			unvisited -= {(previous_node, previous_pred), (previous_pred, previous_node)}
	return total_score, unvisited, path+new_path

def tsiligirides(dist, scores, edges, iters=1000):
	"""
	Run the algorithm.

	:param dist: The graph distance matrix.
	:param scores: The edge rewards.
	:param edges: The edge lengths
	:param iters:
	:return:
	"""
	start_node = 0
	end_node = 0
	tmax = 10000
	max_res = 0
	start = time.time()
	for i in range(iters):
		res = generate_route(dist, scores, edges, start_node, end_node, tmax)
		if res > max_res:
			max_res = res
	return max_res, time.time() - start



# Read the experiment data.
dist = pd.read_csv("./data/dist", delim_whitespace=True, quoting=csv.QUOTE_NONE, index_col=None, header=None,
					engine='python', encoding = 'utf-8').values
pred = pd.read_csv("./data/predecessors", delim_whitespace=True, quoting=csv.QUOTE_NONE, index_col=None, header=None,
					engine='python', encoding = 'utf-8').values
edges = set()
lengths = {}
scores = {}
read_edges("./data/edges")

# Perform the experiment.
with open("res", "w") as f:
	for iters in range(1,200): # [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]:
		for run in range(200):
			max_res, t = tsiligirides(dist, scores, edges, iters)
			f.write("{} {} {}\n".format(iters, max_res, t))
max_res, t = tsiligirides(dist, scores, edges, 100)
print(max_res)


