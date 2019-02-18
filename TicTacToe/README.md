# Tic Tac Toe Implementation in Python

To run this code in Python:
```
from game import *
g = Game(player_1="User", player_2="Random")
g.start()

```

The player argument has 4 options: "User", Random", "Rule" and "RL" (for Reinforcement learning).



------------------------------------------------------------------------------------------------



<h2>Setting Up</h2>
In game.py, I initalized the Game class. Within it are all needed parameters such as board configuration, flag to count number of available spots, result, verbose state and agents are defined. Further, functions were written to show/print to console the board configuration, reset it, check if a solution was found, choose the agent if the game involves Reinforcement Learning, set the results, etc. Basically, this class has all the functions needed to have one or more instances of games. Notice also there is the global function to train the reinforcement learning.

Another folder called Player has all four type of players I will describe in more detail below. They are all child class of Player and have at least a function called "pick()" to choose the next move. The game is configured such that different agent can play with each other.
<h2>Methods Used</h2>
<strong>Method 1: User Input</strong>

In this method, we ask the user to input a value between 1 to 9. Each number is associated to a position in the game board. Rules are written to make sure the input value is valid and the game ends when one of the player wins. This is the most common algorithm presented in Tic Tac Toe programming tutorials online.

<strong>Method 2: Random</strong>

Instead of asking for the input, the random player will generate any position between 1 to 9 that is not already taken. This is also a fairly simple player to code out, but you have to be careful the values generated are possible. Else, recursively look for the next random value.

<strong>Method 3: Rule Based</strong>

If you are like me and played many games of Tic Tac Toe your whole life, it shouldn't be a surprise there are some rules your mind unconsciously set when playing. I tried to hard code those thoughts:
<ol>
	<li>Check if any row/column/diagonal is missing only one spot to end the game. If yes and that spot is available, choose it as next position.</li>
	<li>Check if any row/column/diagonal is missing two spots to end the game. If yes and both spots are available, choose the first of the two as next position.</li>
	<li>Check if any row/column/diagonal is fully empty. If yes, choose one of them. In this case, there should be an ordering of first filling the center, then the corners and finally the walls.</li>
	<li>Choose first available spot between the center, the corners and then the walls.</li>
</ol>
I only implemented these four basic rules. It performed fairly well, but may still be lacking. First, I could have randomized the choice of position if there are multiple available spot instead of always going for the first one. Second, we could easily also track the location of the second player such that even if we cannot win, we can stop the opponent from winning.

Now, these sound like easy rules to follow, but actually hard coding can be tedious and long to debug. Further, by following hard-coded rule, moves start becoming very predictable and boring to play against.

<strong>Method 4: Reinforcement Learning</strong>

Back to reinforcement learning. It is one of the most exciting subfield of machine learning and attracted a lot of attention at last year's NeurIPS conference. The idea is simple. Let the machine learn through experience and allocate reward each time it does a good move to reinforce its learning process. Unlike Deep Learning, Reinforcement Learning is fairly similar to human learning process and is much easier to understand its concept. The harder part is really to implement and choose the right reward function. I inspired myself heavily from Amresh Venugopal's <a href="https://github.com/AmreshVenugopal/tic_tac_toe">code</a> and you can read his <a href="https://becominghuman.ai/reinforcement-learning-step-by-step-17cde7dbc56c">blog post</a> for more detail on how exactly reinforcement learning works.

<strong>Some stats using RL</strong>
10 Epochs: 3 wins,  6 loses, 1 draw
100 Epochs: 49 wins, 37 loses, 14 draws
1000 Epochs: 588 wins, 284 loses, 128 draws
10000 Epochs: 5906 wins, 2840 loses, 1254 draws

<h2>Conclusion</h2>
Overall, this may sound like a simple exercise, but I actually found it very challenging and fun. I learned a lot more about reinforcement learning and about writing a full game with multi-classes. I had to think about what rules I want, which chunk of code can become a function and find the bugs. I definitely spend more time than I expected on this, so hopefully my description here can be useful to more people.