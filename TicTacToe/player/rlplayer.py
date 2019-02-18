from .player import Player
import numpy as np

class RLPlayer(Player):
	def __init__(self, symbol, game):
		self.symbol = symbol
		self.game = game
		self.states = {}
		self.state_order = []
		self.exploration_rate = 0.33
		self.learning_rate = 0.5
		self.discount_factor = 0.01

	def play_seriously(self):
		self.exploration_rate = 0

	def learn_by_temporal_difference(self, reward, new_state_key, state_key):
		old_state = self.states.get(state_key, np.zeros((3,3)))
		return self.learning_rate * ((reward * self.states[new_state_key]) - old_state)

	def set_state(self, old_board, action):
		state_key = serialize_board(old_board)
		self.state_order.append((state_key, action))

	def on_reward(self, reward):
		if len(self.state_order) == 0:
			return None
		new_state_key, new_action = self.state_order.pop()

		self.states[new_state_key] = np.zeros((3,3))
		self.states[new_state_key].itemset(new_action, reward)
		
		while self.state_order:
			state_key, action = self.state_order.pop()
			reward *= self.discount_factor
			if state_key in self.states:
				reward += self.learn_by_temporal_difference(reward, new_state_key, state_key).item(new_action)
				self.states[state_key].itemset(action, reward)
			else:
				self.states[state_key] = np.zeros((3,3))
				reward = self.learn_by_temporal_difference(reward, new_state_key, state_key).item(new_action)
				self.states[state_key].itemset(action, reward)			
			new_state_key = state_key
			new_action = action

	def explore_board(self):
		vacant_cells = []
		for i in range(9):
			if not self.game.taken(i):
				vacant_cells += [i]
		n = np.random.choice(len(vacant_cells))
		return vacant_cells[n]
		
	def exploit_board(self, state_key):
		state_values = self.states[state_key]	
		best_actions_x, best_actions_y = np.where(state_values == state_values.max())
		best_value_indices = [x + 3*y for x,y in zip(best_actions_x, best_actions_y)]
		select_index = np.random.choice(len(best_value_indices))
		return best_value_indices[select_index]

	def pick(self):
		state_key = serialize_board(self.game.board)
		exploration = np.random.random() < self.exploration_rate
		if exploration or state_key not in self.states:
			action = self.explore_board()
		else:
			action = self.exploit_board(state_key)
		self.set_state(self.game.board, action)
		self.game.board[action] = self.symbol
		self.game.flag -= 1
		res = self.game.check(self.game.board, self.symbol, action)
		if res:
			if self.game.verbose:
				print("RL" + "_" + self.symbol + " won!")
			self.game.flag =- 1
			self.game.show()
			self.game.set_result(self.symbol)


def serialize_board(board):
	return ''.join([str(i) for i in board])
