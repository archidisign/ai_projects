import random
import pickle

def choose_random():
    ls = options()
    return random.choice(ls)-1

def reset():
    board = [i for i in range(1, 10)]

def options():
    opts = []
    for pos in board:
        if pos != 'o' and pos != 'x':
            opts += [int(pos)]
    return opts

def show():
    print(board[0],'|',board[1],'|',board[2])
    print('---------')
    print(board[3],'|',board[4],'|',board[5])
    print('---------')
    print(board[6],'|',board[7],'|',board[8])

def check(char, pos):
    if pos == 4:
        if (board[0] == board[8] and char == board[0]) or \
            (board[2] == board[6] and char == board[2]) or \
            (board[3] == board[5] and char == board[3]) or \
            (board[1] == board[7] and char == board[1]):
            return True
    elif pos in [2, 6]:
        if (board[2]==board[4] and board[6]==board[4]):
            return True
    elif pos in [0, 8]:
        if (board[0]==board[4] and board[8]==board[4]):
            return True
    if pos in [0, 1, 2]:
        if (board[pos+3] == char and board[pos+6] == char) or (board[0]==board[1] and board[0]==board[2]):
            return True
    if pos in [3, 4, 5]:
        if (board[pos-3] == char and board[pos+3] == char) or (board[3]==board[4] and board[3]==board[5]):
            return True
    if pos in [6, 7, 8]:
        if (board[pos-3] == char and board[pos-6] == char) or (board[6]==board[7] and board[6]==board[8]):
            return True
    return False

class Qlearning:
    def __init__(self,epsilon=0.2, alpha=0.3, gamma=0.9):
        self.epsilon=epsilon
        self.alpha=alpha
        self.gamma=gamma
        self.Q = {} #Q table
        self.last_board=None
        self.q_last=0.0
        self.state_action_last=None

    def game_begin(self):
        self.last_board = None
        self.q_last = 0.0
        self.state_action_last = None


    def epslion_greedy(self, state, possible_moves): #esplion greedy algorithm
        #return  action
        self.last_board = tuple(state)
        if(random.random() < self.epsilon):
            move = random.choice(possible_moves) ##action
            self.state_action_last=(self.last_board,move)
            self.q_last=self.getQ(self.last_board,move)
            return move
        else: #greedy strategy
            Q_list=[]
            for action in possible_moves:
                Q_list.append(self.getQ(self.last_board,action))
            maxQ=max(Q_list)

            if Q_list.count(maxQ) > 1:
                # more than 1 best option; choose among them randomly
                best_options = [i for i in range(len(possible_moves)) if Q_list[i] == maxQ]
                i = random.choice(best_options)
            else:
                i = Q_list.index(maxQ)
            self.state_action_last = (self.last_board, possible_moves[i])
            self.q_last = self.getQ(self.last_board, possible_moves[i])
            return possible_moves[i]


    def getQ(self, state, action): #get Q states
        if(self.Q.get((state,action))) is None:
            self.Q[(state,action)] = 1.0
        return self.Q.get((state,action))

    def updateQ(self, reward, state, possible_moves): # update Q states using Qleanning
        q_list=[]
        for moves in possible_moves:
            q_list.append(self.getQ(tuple(state), moves))
        if q_list:
            max_q_next = max(q_list)
        else:
            max_q_next=0.0
        self.Q[self.state_action_last] = self.q_last + self.alpha * ((reward + self.gamma*max_q_next) - self.q_last)

    def saveQtable(self,file_name):  #save table
        with open(file_name, 'wb') as handle:
            pickle.dump(self.Q, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadQtable(self,file_name): # load table
        with open(file_name, 'rb') as handle:
            self.Q = pickle.load(handle)

board = [i for i in range(1, 10)]
print("Each position is numbered: ")
show()
flag=9
while flag!=0:
    i = input("Choose a position from 1 to 9: ")
    try:
        i = int(i)
    except:
        print("The input is not an integer between 1 to 9")
    if i<1 or i>9:
        print("The position chosen is not between 1 to 9")
    elif board[i-1] == 'x' or board[i-1] == 'o':
        print("The position chosen is occupied")
    else:
        board[i-1] = 'x'
        if check('x', i-1):
            print("You won!")
            break
        flag -= 1        
        ai = choose_random()
        board[ai] = 'o'
        if check('o', ai):
            print("You lost!")
            flag=0
        flag -= 1
    show()