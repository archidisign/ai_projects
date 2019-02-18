from player.userplayer import UserPlayer
from player.randomplayer import RandomPlayer
from player.ruleplayer import RulePlayer
from player.rlplayer import RLPlayer

class Game(object):
	def __init__(self, player_1="User", player_2="Random", verbose=False):
		self.board = [i for i in range(1, 10)]
		self.flag = 9
		self.result = "-"
		self.verbose = verbose
		self.player_1 = player_1
		self.player_2 = player_2
		self.agent_1 = self.agent_choice(player_1, 'x')
		self.agent_2 = self.agent_choice(player_2, 'o')

		if (self.player_1 == "RL") and (self.player_2 != "RL"):
			result = train(10000)
			self.agent_1 = result[1][0]
			self.reset_board()
			self.agent_1.game = self
		elif (self.player_1 != "RL") and (self.player_2 == "RL"):
			result = train(10000)
			self.agent_2 = result[1][1]
			self.reset_board()
			self.agent_2.game = self

	def show(self):
		if self.verbose:
			print(self.board[0],'|',self.board[1],'|',self.board[2])
			print('---------')
			print(self.board[3],'|',self.board[4],'|',self.board[5])
			print('---------')
			print(self.board[6],'|',self.board[7],'|',self.board[8])
			print('-------------------------')

	def reset_board(self):
		self.board = [i for i in range(1, 10)]
		self.flag = 9
		self.result = "-"

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

	def taken(self, i):
		return self.board[i] == 'x' or self.board[i] == 'o'

	def start(self):
		if (self.player_1 == "User" or self.player_2 == "User"):
			print("Each position is numbered: ")
			self.show()
			self.verbose = True
			print("The game is between " + self.player_1 + " and " + self.player_2)
		self.play()

	def play(self):
		while self.flag > 0:
			self.show()
			self.agent_1.pick()
			if self.flag > 0:
				self.agent_2.pick()
		if self.flag == 0:
			if self.verbose:
				print("Nobody won :(")
			self.show()
			self.set_result('-')

	def agent_choice(self, player, symbol):
		if player == "User":
			agent = UserPlayer(symbol, self)
		elif player == "Random":
			agent = RandomPlayer(symbol, self)
		elif player == "Rule":
			agent = RulePlayer(symbol, self)
		elif player == "RL":
			agent = RLPlayer(symbol, self)
		else:
			raise Exception("Player type does not exist")
		return agent

	def set_result(self, symbol):
		if symbol == "x":
			self.result = 1
		elif symbol == "o":
			self.result = 2
		else:
			self.result = 0
		if self.player_1 == "RL" and self.player_2 == "RL":
			self.set_reward(symbol)

	def set_reward(self, symbol):
		if symbol == "x":
			self.agent_1.on_reward(1)
			self.agent_2.on_reward(-1)
		elif symbol == "o":
			self.agent_1.on_reward(-1)
			self.agent_2.on_reward(1)
		else:
			pass


def train(n_epochs):
	n_player_1, n_player_2 = 0, 0
	game = Game(player_1="RL", player_2="RL")
	for i in range(n_epochs):
		game.reset_board()
		game.start()
		if game.result == 1:
			n_player_1 += 1
		elif game.result == 2:
			n_player_2 += 1

	counts = n_player_1, n_player_2
	agents = game.agent_1, game.agent_2
	return counts, agents
