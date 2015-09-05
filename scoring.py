from objects import *
from game import *

class ScoreKeeperHandler:
	def __init__(self, board_size):
		self.board_size = board_size
		if os.path.isfile("scores.p"):
			f = open("scores.p", "rb")
			self.scorekeeper = pickle.load(f)
			self.scorekeeper.update(self.board_size, 0)
			f.close()
		else:
			self.scorekeeper = ScoreKeeper()
			f = open("scores.p", "wb")
			pickle.dump(self.scorekeeper, f)
			f.close()

	def update(self, n):
			self.scorekeeper.update(self.board_size, n)
			f = open("scores.p", "wb")
			pickle.dump(self.scorekeeper, f)
			f.close()
	@property
	def max(self):
		return self.scorekeeper.max_score()

class ScoreKeeper:
	def __init__(self, x = 0):
		self.scores = {}
		for i in range(2, 11):
			self.scores[i] = 0
		self.curr_board = 2

	def update(self, board_size, n):
		self.curr_board = board_size
		if board_size in self.scores:
			self.scores[board_size] = max(self.scores[board_size], n)
		else:
			self.scores[board_size] = n	

	def max_score(self):
		return self.scores[self.curr_board]

	def disp_scores(self):
		print("ALL TIME HIGH SCORES\n")
		print("Board\tScore")
		for i in self.scores:
			print(' ', i, '\t', self.scores[i])