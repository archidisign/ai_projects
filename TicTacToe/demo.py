from game import *

# Simple playing
g = Game(player_1="User", player_2="Random")
g.start()

# RL training
result = train(10000)
print(result[0])

# Playing with trained Agent
g2 = Game(player_1="User", player_2="RL")
g2.start()