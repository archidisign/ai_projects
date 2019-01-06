import random
board = [i for i in range(1, 10)]

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
        while True:
            random.seed()
            ai = random.randint(0, 8)
            if board[ai] != 'o' and board[ai] != 'x':
                board[ai] = 'o'
                if check('o', ai):
                    print("You lost!")
                    flag=0
                flag -= 1
                break
    show()