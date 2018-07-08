import random
import sys
from solution import Solution
from reactive import Reactive


class GRASP:

	def __init__(self):
		self.found_solutions = []

	def generate_neighborhood(self, solution):
		n = []
		hmin = sys.maxsize
		hmax = -sys.maxsize
		for i,d in enumerate(solution.nodes):
			for j,f in enumerate(solution.nodes[i+1:]):
				for e in solution.avail_arcs(d,f):
					ins = solution.mk_ins(e,i,i+j+1)
					if ins.add_cost <= solution.problem.capacity:
						n.append(ins)
						hmin = hmin if ins.hval > hmin else ins.hval
						hmax = hmax if ins.hval < hmax else ins.hval
		return n, hmin, hmax

	def generate_neighborhood_stochastic(self, solution):
		n = []
		hmin = sys.maxsize
		hmax = -sys.maxsize
		i, j, d, f = solution.pick_random_ins()
		for e in solution.avail_arcs(d, f):
			ins = solution.mk_ins(e, i, j)
			if ins.add_cost <= solution.problem.capacity:
				n.append(ins)
				hmin = hmin if ins.hval > hmin else ins.hval
				hmax = hmax if ins.hval < hmax else ins.hval
		return n, hmin, hmax

	def search(self, problem, iters=10):
		best_score = 0
		best_sol = Solution(problem)
		for _ in range(iters):
			sol = Solution(problem)
			greediness = random.uniform(0,1)
			insertion_list, hmin, hmax = self.generate_neighborhood(sol)
			while len(insertion_list) > 0 and not sol.rem_dist <= 0:
				threshold = hmin + greediness * (hmax - hmin)
				insertion_list = [i for i in insertion_list if i.hval > threshold]
				if len(insertion_list) <= 0:
					break
				rand = insertion_list[random.randint(0,len(insertion_list)-1)]
				sol.insert_ins(rand)
				insertion_list, hmin, hmax = self.generate_neighborhood(sol)
			if sol.score > best_score:
				best_score = sol.score
				best_sol = sol
		return best_score, best_sol

	def search_stochastic(self, problem, iters=10):
		best_score = 0
		best_sol = Solution(problem)
		for _ in range(iters):
			sol = Solution(problem)
			greediness = random.uniform(0,1)
			insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			while len(insertion_list) > 0 and not sol.rem_dist <= 0:
				threshold = hmin + greediness * (hmax - hmin)
				insertion_list = [i for i in insertion_list if i.hval > threshold]
				if len(insertion_list) <= 0:
					break
				rand = insertion_list[random.randint(0,len(insertion_list)-1)]
				sol.insert_ins(rand)
				insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			if sol.score > best_score:
				best_score = sol.score
				best_sol = sol
		return best_score, best_sol

	def search_reactive(self, problem, iters=10):
		best_score = 0
		reactive = Reactive(10)
		best_sol = Solution(problem)
		for _ in range(iters):
			sol = Solution(problem)
			idx, greediness = reactive.get_alpha()
			insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			while len(insertion_list) > 0 and not sol.rem_dist <= 0:
				threshold = hmin + greediness * (hmax - hmin)
				insertion_list = [i for i in insertion_list if i.hval > threshold]
				if len(insertion_list) <= 0:
					break
				rand = insertion_list[random.randint(0, len(insertion_list) - 1)]
				sol.insert_ins(rand)
				insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			if sol.score > best_score:
				best_score = sol.score
				best_sol = sol
			reactive.update(sol.score, best_score, idx)
		return best_score, best_sol

	def search_biased(self, problem, iters=10):
		best_score = 0
		best_sol = Solution(problem)
		for _ in range(iters):
			sol = Solution(problem)
			greediness = random.uniform(0, 0.2)
			insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			while len(insertion_list) > 0 and not sol.rem_dist <= 0:
				threshold = hmin + greediness * (hmax - hmin)
				insertion_list = [i for i in insertion_list if i.hval >= threshold]
				if len(insertion_list) <= 0:
					break
				rand = insertion_list[random.randint(0, len(insertion_list) - 1)]
				sol.insert_ins(rand)
				insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			if sol.score > best_score:
				best_score = sol.score
				best_sol = sol
		return best_score, best_sol

	def search_fixed(self, problem, greediness = 0.8, iters=10):
		best_score = 0
		best_sol = Solution(problem)
		for _ in range(iters):
			sol = Solution(problem)
			insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			while len(insertion_list) > 0 and not sol.rem_dist <= 0:
				threshold = hmin + greediness * (hmax - hmin)
				insertion_list = [i for i in insertion_list if i.hval >= threshold]
				if len(insertion_list) <= 0:
					break
				rand = insertion_list[random.randint(0, len(insertion_list) - 1)]
				sol.insert_ins(rand)
				insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			if sol.score > best_score:
				best_score = sol.score
				best_sol = sol
		return best_score, best_sol

	def search_reactive_with_local_search(self, problem, iters=10):
		best_score = 0
		best_sol = Solution(problem)
		reactive = Reactive(10)
		for _ in range(iters):
			sol = Solution(problem)
			idx, greediness = reactive.get_alpha()
			insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			while len(insertion_list) > 0 and not sol.rem_dist <= 0:
				threshold = hmin + greediness * (hmax - hmin)
				insertion_list = [i for i in insertion_list if i.hval > threshold]
				if len(insertion_list) <= 0:
					break
				rand = insertion_list[random.randint(0, len(insertion_list) - 1)]
				sol.insert_ins(rand)
				insertion_list, hmin, hmax = self.generate_neighborhood_stochastic(sol)
			sol.local_search()
			if sol.score > best_score:
				best_score = sol.score
				best_sol = sol
			reactive.update(sol.score, best_score, idx)
		return best_score, best_sol

	# def search_alternative(self, problem, iters=1000):
	# 	best = self.init_best()
	# 	sol = Solution([], problem)
	# 	for i in range(iters):
	# 		alpha = self.get_alpha(i)
	# 		insertion_list = self.generate_neighborhood(sol)
	# 		while len(insertion_list) > 0 and not sol.full():
	# 			hmin, hmax = self.get_bounds(insertion_list)
	# 			threshold = hmin + (1 - alpha) * (hmax - hmin)
	# 			insertion_list = self.restrict(insertion_list, threshold)
	# 			rand = insertion_list[random.randint(0,len(insertion_list))]
	# 			sol.insert_ins(rand)
	# 		self.local_search(sol)
	# 		best = self.update_best(sol, best)
	# 		sol.perturb(beta)
	# 	return best
