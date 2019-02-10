import random

class Game(object):
	def __init__(self, player_1="User", player_2="Random"):
		self.board = [i for i in range(1, 10)]
		self.flag = 9
		self.player_1 = player_1
		self.player_2 = player_2

	def show(self):
		print(self.board[0],'|',self.board[1],'|',self.board[2])
		print('---------')
		print(self.board[3],'|',self.board[4],'|',self.board[5])
		print('---------')
		print(self.board[6],'|',self.board[7],'|',self.board[8])
		print('-------------------------')

	def check(self, board, char, pos):
		res = False
		if pos == 4:
			if (board[0] == board[8] and char == board[0]) or \
				(board[2] == board[6] and char == board[2]) or \
				(board[3] == board[5] and char == board[3]) or \
				(board[1] == board[7] and char == board[1]):
				res = True
		elif pos in [2, 6]:
			if (board[2]==board[4] and board[6]==board[4]):
				res = True
		elif pos in [0, 8]:
			if (board[0]==board[4] and board[8]==board[4]):
				res = True
		if pos in [0, 1, 2]:
			if (board[pos+3] == char and board[pos+6] == char) or (board[0]==board[1] and board[0]==board[2]):
				res = True
		if pos in [3, 4, 5]:
			if (board[pos-3] == char and board[pos+3] == char) or (board[3]==board[4] and board[3]==board[5]):
				res = True
		if pos in [6, 7, 8]:
			if (board[pos-3] == char and board[pos-6] == char) or (board[6]==board[7] and board[6]==board[8]):
				res = True
		return res

	def start(self):
		if self.player_1 == "User" or self.player_2 == "User":
			print("Each position is numbered: ")
			self.show()
		print("The game is between " + self.player_1 + " and " + self.player_2)
		self.play()

	def taken(self, i):
		return self.board[i] == 'x' or self.board[i] == 'o'

	def play(self):
		while self.flag > 0:
			self.show()
			self.pick_choice(self.player_1, 'x')
			if self.flag > 0:
				self.pick_choice(self.player_2, 'o')
		if self.flag == 0:
			print("Nobody won :(")
			self.show()

	def pick_choice(self, player, symbol):
		if player == "User":
			self.pick_user(symbol)
		elif player == "Random":
			self.pick_random(symbol)
		elif player == "Rule":
			self.pick_rule(symbol)
		elif player == "RL":
			self.pick_rl(symbol)
		else:
			raise Exception("Player 2 " + self.player_2 + " type does not exist")

	def pick_user(self, symbol):
		i = input("Choose a position from 1 to 9: ")
		try:
			i = int(i)
		except:
			print("The input is not an integer between 1 to 9")

		if i<1 or i>9:
			print("The position chosen is not between 1 to 9")
		elif self.taken(i-1):
			print("The position chosen is occupied")
		else:
			self.board[i-1] = symbol
			self.flag -= 1
			res = self.check(self.board, symbol, i-1)
			if res:
				print("User" + "_" + symbol + " won!")
				self.flag = -1
				self.show()
			

	def pick_random(self, symbol):
		random.seed()
		ai = random.randint(0, 8)
		if not self.taken(ai):
			self.board[ai] = symbol
			self.flag -= 1
			res = self.check(self.board, symbol, ai)
			if res:
				print("Random" + "_" + symbol + " won!")
				self.flag = -1
				self.show()
		else:
			self.pick_random(symbol)

	def pick_rule(self, symbol):
		d = {0: [[4, 8], [1, 2], [6, 3]],
			1: [[4, 7], [2, 1]],
			2: [[4, 6], [0, 1], [8, 5]],
			3: [[4, 5], [0, 6]],
			4: [[2, 6], [0, 8], [1, 7], [3, 5]],
			5: [[3, 4], [2, 8]],
			6: [[8, 7], [0, 3], [4, 2]],
			7: [[4, 1], [6, 8]],
			8: [[4, 0], [2, 5], [6, 7]]}
		# First, check if can win this round
		val = True
		try:
			for key, value in d.items():
				if self.board[key] == symbol:
					for l in value:
						if not self.taken(l[0]) and self.board[l[1]] == symbol:
							temp = l[0]
							raise Exception
						elif not self.taken(l[1]) and self.board[l[0]] == symbol:
							temp = l[1]
							raise Exception
		except:
			self.board[temp] = symbol
			print("Rule" + "_" + symbol + " won!")
			self.flag = -1
			self.show()
			val = False
		# Second, choose the one with 2 missing
		if val and self.flag != -1:
			try:
				for key, value in d.items():
					if self.board[key] == symbol:
						for l in value:
							if not self.taken(l[0]) and not self.taken(l[1]):
								raise Exception
			except:
				self.board[l[0]] = symbol
				self.flag -= 1
				val = False
		# Third, go for the one with 3 empty spots
		if val and self.flag != -1:
			try:
				ls = [[4, 2, 6], [4, 0, 8], [4, 1, 7], [4, 3, 5], [0, 2, 1], [6, 8, 7], [0, 6, 3], [2, 8, 5]]
				for l in ls:
					if all(not self.taken(i) for i in l):
						raise Exception
			except:
				self.board[l[0]] = symbol
				self.flag -= 1
				val = False
		# Go for first empty spot
		if val and self.flag != -1:
			for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
				if not self.taken(i):
					self.board[i] = symbol
					self.flag -= 1
					val = False
					break

	def pick_rl(self):
		pass