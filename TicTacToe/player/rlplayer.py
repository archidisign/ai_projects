from .player import Player

class RLPlayer(Player):
	def __init__(self, symbol, game):
		self.symbol = symbol
		self.game = game
	
	def pick(self):
		pass