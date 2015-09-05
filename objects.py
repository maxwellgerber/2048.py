import random
import pickle
import os
from scoring import *
from game import *

class Box:
	def __init__(self, holder, x = -1):
		self.value = x
		self.holder = holder
		self.can_combine = True

	def __repr__(self):
		return (str(self.get_val()) if not self.empty else "__")

	def get_val(self):
		return self.value

	def set_val(self, x = -1):
		self.value = x

	def double(self):
		self.value = self.value * 2
		self.holder.score += self.value
		self.holder.scorekeeper.update(self.holder.score)
		self.can_combine = False

	@property
	def empty(self):
		return self.get_val() == -1

class Row:
	def __init__(self, n, holder):
		self.boxes = []
		for i in range(n):
			self.boxes.append(Box(holder))

	def __repr__(self):
		temp = [i.__repr__() for i in self.boxes]
		return '\t'.join(temp)

	@property
	def can_move(self):
		for i in range(len(self.boxes)-1):
			this_box = self.boxes[i]
			next_box = self.boxes[i+1]
			if this_box.get_val() == next_box.get_val() and not this_box.empty:
				return True
		return False

	def collapse(self, direction):
		"""
		if dir is 1 collapse towards front of list
		else collapse towards end
		"""		
		box_moved = True
		length = len(self.boxes)-1
		move_made = False
		for box in self.boxes:
			box.can_combine = True
		while box_moved:
			box_moved = False			
			for i in range(length):
				if direction == 1:
					this_box = self.boxes[i]
					next_box = self.boxes[i+1]
				else:
					this_box = self.boxes[length-i]
					next_box = self.boxes[length-i -1]
				if this_box.get_val() == next_box.get_val() and not this_box.empty and this_box.can_combine and next_box.can_combine:
					this_box.double()
					next_box.set_val()
					move_made = True
				elif this_box.empty and not next_box.empty:
					box_moved = True
					move_made = True
					this_box.set_val(next_box.get_val())
					next_box.set_val()
		return move_made


class Column(Row):
	def __init__(self, boxes = []):
		self.boxes = boxes

	def __repr__(self):
		temp = [i.__repr__() for i in self.boxes]
		return '\n'.join(temp) 

class Board:
	def __init__(self, n, holder):
		self.rows = []
		self.columns = []
		self.allboxes = []
		r = range(n)
		for i in r:
			self.rows.append(Row(n, holder))
			self.allboxes.append(self.rows[i].boxes)
		for j in r:
			temp = [self.rows[k].boxes[j] for k in r]
			self.columns.append(Column(temp))
		self.allboxes = sum(self.allboxes, [])

	def dispRows(self):
		for i in self.rows:
			print(i)

	def __repr__(self):
		self.dispRows()
		return ' '

	@property 
	def allemptyboxes(self):
		return [i for i in self.allboxes if i.empty]

	@property 
	def can_move(self):
		for i in self.rows:
			if i.can_move:
				return True
		for j in self.columns:
			if j.can_move:
				return True
		return False


	def randomDrop(self, x = 2):
		if self.allemptyboxes:
			random.choice(self.allemptyboxes).set_val(x)
		
	def left(self):
		complete = False
		for row in self.rows:
			complete = row.collapse(1) or complete
		return complete

	def right(self):
		complete = False
		for row in self.rows:
			complete = row.collapse(-1) or complete
		return complete

	def up(self):
		complete = False
		for column in self.columns:
			complete = column.collapse(1) or complete
		return complete

	def down(self):
		complete = False
		for column in self.columns:
			complete = column.collapse(-1) or complete
		return complete

class Game:
	def __init__(self, board_size = 4):
		self.score = 0
		self.board_size = board_size

	def new_game(self):
		self.board = Board(self.board_size, self)		
		self.board.randomDrop(2)
		self.board.randomDrop(2)
		self.board.randomDrop(4)
		self.play_game()

	def play_game(self):		
		self.scorekeeper = ScoreKeeperHandler(self.board_size)
		while 1:
			print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
			print("    Current Score: {0} \t Max Score:{1}".format(self.score, self.scorekeeper.max))
			print("\n")
			print(self.board)
			complete = False
			command = input('W A S D X >>>')
			if command.lower() in 'wasdx':
				if command.lower() == 'w':
					complete = self.board.up()
				elif command.lower() == 'a':
					complete = self.board.left()
				elif command.lower() == 's':
					complete = self.board.down()
				elif command.lower() == 'd':
					complete = self.board.right()
				elif command.lower() == 'x':
					break

				if complete:
					self.board.randomDrop(2)

				if not self.board.can_move and not self.board.allemptyboxes:
					print("\n\n\n\n\n")
					print(self.board)
					print("\n\n GAME OVER")
					pause()
					break

			elif command is 'P':
				f =  open("saved.p", "wb")
				pickle.dump(self,f)
				f.close()