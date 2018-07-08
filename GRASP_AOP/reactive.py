import numpy as np

class Reactive(object):

	def __init__(self, num_classes):
		# TODO: Use NumPy datastructures.
		self.num_classes = num_classes
		# self.ps = [1/num_classes] * num_classes
		self.ps = np.zeros(num_classes, dtype="float")
		self.ps[:] = 1/num_classes
		# self.qs = [0] * num_classes
		self.qs = np.ones(num_classes, dtype="float")
		# self.alphas = [1/num_classes * i for i in range(num_classes)]
		self.alphas = np.fromiter((1/num_classes * i for i in range(num_classes)), dtype="float")
		# self.average_scores = [0] * num_classes  # Average scores found using individual alphas
		self.average_scores = np.zeros(num_classes, dtype="float")
		# self._score_sums = [0] * num_classes
		self._score_sums = np.zeros(num_classes, dtype="float")
		# self._score_nums = [0] * num_classes
		self._score_nums = np.zeros(num_classes, dtype="float")

	def update(self, sol_score, best_sol_score, used_alpha_idx):
		"""Update the reactive alpha stats."""
		self._score_sums[used_alpha_idx] += sol_score
		self._score_nums[used_alpha_idx] += 1
		# s = 0
		# for i in range(self.num_classes):
		# 	if self._score_nums[i] > 0:
		# 		self.qs[i] = best_sol_score / (self._score_sums[i] / self._score_nums[i])
		# 	s += self.qs[i]
		# self.average_scores[used_alpha_idx] = self._score_sums[used_alpha_idx] / self._score_nums[used_alpha_idx]
		self.qs = np.fromiter(((self._score_sums[i] / self._score_nums[i]) / best_sol_score if self._score_nums[i] > 0 else self.qs[i] for i in range(self.num_classes)), dtype="float")
		s = np.sum(self.qs, dtype="float")
		self.ps = np.fromiter((self.qs[i]/s for i in range(self.num_classes)), dtype="float")

	def get_alpha(self):
		"""Choose an alpha."""
		# return np.random.choice(self.alphas, 1, p=self.ps)[0]
		idx = np.random.choice(range(self.num_classes), 1, p=self.ps)[0]
		return idx, self.alphas[idx]
