from .player import Player

class RulePlayer(Player):
	def __init__(self, symbol, game):
		self.symbol = symbol
		self.game = game

	def pick(self):
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
				if self.game.board[key] == self.symbol:
					for l in value:
						if not self.game.taken(l[0]) and self.game.board[l[1]] == self.symbol:
							temp = l[0]
							raise Exception
						elif not self.game.taken(l[1]) and self.game.board[l[0]] == self.symbol:
							temp = l[1]
							raise Exception
		except:
			self.game.board[temp] = self.symbol
			print("Rule" + "_" + self.symbol + " won!")
			self.game.flag = -1
			self.game.show()
			val = False
			self.game.set_result(symbol)
		# Second, choose the one with 2 missing
		if val and self.game.flag != -1:
			try:
				for key, value in d.items():
					if self.game.board[key] == self.symbol:
						for l in value:
							if not self.game.taken(l[0]) and not self.game.taken(l[1]):
								raise Exception
			except:
				self.game.board[l[0]] = self.symbol
				self.game.flag -= 1
				val = False
		# Third, go for the one with 3 empty spots
		if val and self.game.flag != -1:
			try:
				ls = [[4, 2, 6], [4, 0, 8], [4, 1, 7], [4, 3, 5], [0, 2, 1], [6, 8, 7], [0, 6, 3], [2, 8, 5]]
				for l in ls:
					if all(not self.game.taken(i) for i in l):
						raise Exception
			except:
				self.game.board[l[0]] = self.symbol
				self.game.flag -= 1
				val = False
		# Go for first empty spot
		if val and self.game.flag != -1:
			for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
				if not self.game.taken(i):
					self.game.board[i] = self.symbol
					self.game.flag -= 1
					val = False
					break
