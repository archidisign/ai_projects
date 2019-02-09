from player import *

class Game(object):
	def __init__(self, player_2="Random"):
		self.board = [i for i in range(1, 10)]
		self.flag = 9
		self.player = Player(type=player_2)

	def show(self):
	    print(self.board[0],'|',self.board[1],'|',self.board[2])
	    print('---------')
	    print(self.board[3],'|',self.board[4],'|',self.board[5])
	    print('---------')
	    print(self.board[6],'|',self.board[7],'|',self.board[8])

	def check(self, char, pos):
	    if pos == 4:
	        if (self.board[0] == self.board[8] and char == self.board[0]) or \
	            (self.board[2] == self.board[6] and char == self.board[2]) or \
	            (self.board[3] == self.board[5] and char == self.board[3]) or \
	            (self.board[1] == self.board[7] and char == self.board[1]):
	            return True
	    elif pos in [2, 6]:
	        if (self.board[2]==self.board[4] and self.board[6]==self.board[4]):
	            return True
	    elif pos in [0, 8]:
	        if (self.board[0]==self.board[4] and self.board[8]==self.board[4]):
	            return True
	    if pos in [0, 1, 2]:
	        if (self.board[pos+3] == char and self.board[pos+6] == char) or (self.board[0]==self.board[1] and self.board[0]==self.board[2]):
	            return True
	    if pos in [3, 4, 5]:
	        if (self.board[pos-3] == char and self.board[pos+3] == char) or (self.board[3]==self.board[4] and self.board[3]==self.board[5]):
	            return True
	    if pos in [6, 7, 8]:
	        if (self.board[pos-3] == char and self.board[pos-6] == char) or (self.board[6]==self.board[7] and self.board[6]==self.board[8]):
	            return True
	    return False

	def start(self):
		print("Each position is numbered: ")
		self.show()
		print("Time to play!")
		self.play()

	def play(self):
		while self.flag > 0:
			self.pick()

	def pick(self):
		if self.flag > 0:
    		i = input("Choose a position from 1 to 9: ")
		    try:
		        i = int(i)
		    except:
		        print("The input is not an integer between 1 to 9")
		    if i<1 or i>9:
		        print("The position chosen is not between 1 to 9")
		    elif self.board[i-1] == 'x' or self.board[i-1] == 'o':
		        print("The position chosen is occupied")
		    else:
		        self.board[i-1] = 'x'

		        if self.check('x', i-1):
		            print("You won!")
		            break
		        flag -= 1
		    self.player.pick()
		show()