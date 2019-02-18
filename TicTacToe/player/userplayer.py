from .player import Player

class UserPlayer(Player):
	def __init__(self, symbol, game):
		self.symbol = symbol
		self.game = game
	
	def pick(self):
		i = input("Choose a position from 1 to 9: ")
		try:
			i = int(i)
		except:
			print("The input is not an integer between 1 to 9")

		if i<1 or i>9:
			print("The position chosen is not between 1 to 9")
		elif self.game.taken(i-1):
			print("The position chosen is occupied")
		else:
			self.game.board[i-1] = self.symbol
			self.game.flag -= 1
			res = self.game.check(self.game.board, self.symbol, i-1)
			if res:
				print("User" + "_" + self.symbol + " won!")
				self.game.flag = -1
				self.game.show()
				self.game.set_result(self.symbol)