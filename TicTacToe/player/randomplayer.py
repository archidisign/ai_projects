from .player import Player
import random

class RandomPlayer(Player):
	def __init__(self, symbol, game):
		self.symbol = symbol
		self.game = game

	def pick(self):
		random.seed()
		ai = random.randint(0, 8)
		if not self.game.taken(ai):
			self.game.board[ai] = self.symbol
			self.game.flag -= 1
			res = self.game.check(self.game.board, self.symbol, ai)
			if res:
				print("Random" + "_" + self.symbol + " won!")
				self.game.flag = -1
				self.game.show()
				self.game.set_result(symbol)
		else:
			self.game.pick_random(self.symbol)