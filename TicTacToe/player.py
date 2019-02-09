class Player(object):
	def __init__(self, type="Random"):
		self.type = type

	def pick(self):
		if self.type == "Random":
			self.pick_random()
		elif self.type == "Rule":
			self.pic_rule()
		elif self.type == "RL":
			self.pic_rl()
		else:
			raise Exception("Player 2 " + self.type + " type does not exist")

	def pick_random(self):
		random.seed()
        ai = random.randint(0, 8)
        if board[ai] != 'o' and board[ai] != 'x':
            board[ai] = 'o'
            if check('o', ai):
                print("You lost!")
                flag=0
            flag -= 1

    def pick_rule(self):
    	pass

   	def pick_rl(self):
   		pass