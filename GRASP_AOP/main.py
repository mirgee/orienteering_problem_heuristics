from problem import Problem
from grasp import GRASP
from loader import loader
import time
import timeit

l = loader("./data/edges")
l.read_edges()
# l.read_distmatrix()

problem = Problem(
	data=l.data,
	startidx=0,
	endidx=0,
	capacity=10000
)

g = GRASP()

# for _ in range(200):
# 	best_score = g.search_fixed(problem, 1, 20)
# 	print(best_score)
#
with open("res_stoch_timeit", mode="w") as f1, open("res_biased_timeit", mode="w") as f2, open("res_fixed_timeit", mode="w") as f3, open("res_reactive_timeit", mode="w") as f4:
	for iters in range(1,40): # [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]:
		for t in range(200):
			print("{} iterations".format(iters))

			# print("Original")
			# start = time.time()
			# best_score = g.search(problem, iters)
			# end = time.time()
			# print("Best score: {}".format(best_score))
			# print("Time: {} s / iteration".format((end - start) / iters))
			# f1.write("{} {} {}\n".format(iters, best_score, end-start))

			print("Stochastic")
			start = time.time()
			best_score, _ = g.search_stochastic(problem, iters)
			end = time.time()
			print("Best score: {}".format(best_score))
			print("Time: {} s / iteration".format((end - start) / iters))
			f1.write("{} {} {}\n".format(iters, best_score, (end - start)))

			print("Biased")
			start = time.time()
			best_score, _ = g.search_biased(problem, iters)
			end = time.time()
			print("Best score: {}".format(best_score))
			print("Time: {} s / iteration".format((end - start) / iters))
			f2.write("{} {} {}\n".format(iters, best_score, end - start))

			print("Fixed")
			start = time.time()
			best_score, _ = g.search_fixed(problem, 0.2, iters)
			end = time.time()
			print("Best score: {}".format(best_score))
			print("Time: {} s / iteration".format((end - start) / iters))
			# print(sol)
			f3.write("{} {} {}\n".format(iters, best_score, end - start))

			print("Reactive")
			start = time.time()
			best_score, _ = g.search_reactive(problem, iters)
			end = time.time()
			print("Best score: {}".format(best_score))
			print("Time: {} s / iteration".format((end - start) / iters))
			# print(sol)
			f4.write("{} {} {}\n".format(iters, best_score, end - start))

			print()

# with open("lambdas_1", mode="w") as f:
# 	for l in [0, 0.2, 0.4, 0.6, 0.8, 1]:
# 		for t in range(200):
# 			print("{} {}".format(l, t))
# 			start = time.time()
# 			best_score, _ = g.search_fixed(problem, l, 20)
# 			end = time.time()
# 			print("Best score: {}".format(best_score))
# 			print("Time: {} s / iteration".format((end - start) / 20))
# 			# print(sol)
# 			f.write("{} {} {} {}\n".format(l, t, end - start, best_score))

