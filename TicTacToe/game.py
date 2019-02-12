from player.userplayer import UserPlayer
from player.randomplayer import RandomPlayer
from player.ruleplayer import RulePlayer
from player.rlplayer import RLPlayer

class Game(object):
	def __init__(self, player_1="User", player_2="Random"):
		self.board = [i for i in range(1, 10)]
		self.flag = 9
		self.player_1 = player_1
		self.player_2 = player_2
		self.result = "-"

	def show(self):
		print(self.board[0],'|',self.board[1],'|',self.board[2])
		print('---------')
		print(self.board[3],'|',self.board[4],'|',self.board[5])
		print('---------')
		print(self.board[6],'|',self.board[7],'|',self.board[8])
		print('-------------------------')

	def reset_board(self):
		self.board = [i for i in range(1, 10)]

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
			self.set_result('-')

	def pick_choice(self, player, symbol):
		if player == "User":
			UserPlayer(symbol, self).pick()
		elif player == "Random":
			RandomPlayer(symbol, self).pick()
		elif player == "Rule":
			RulePlayer(symbol, self).pick()
		elif player == "RL":
			RLPlayer(symbol, self).pick()
		else:
			raise Exception("Player 2 " + self.player_2 + " type does not exist")

	def set_result(self, symbol):
		self.result = symbol