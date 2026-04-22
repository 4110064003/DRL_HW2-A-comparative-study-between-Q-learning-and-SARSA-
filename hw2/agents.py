"""Q-learning and SARSA agents for HW2 Cliff Walking.

This module implements two tabular TD control algorithms:
- QLearningAgent (off-policy): target uses max_a Q(s', a)
- SarsaAgent (on-policy): target uses Q(s', a') for the next action
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np


Action = int
State = int


@dataclass
class AgentConfig:
	"""Common hyperparameters for tabular agents."""

	epsilon: float = 0.1
	alpha: float = 0.1
	gamma: float = 0.9


class BaseTabularAgent:
	"""Base class for tabular control agents with an epsilon-greedy policy."""

	def __init__(
		self,
		n_states: int,
		n_actions: int,
		config: Optional[AgentConfig] = None,
		seed: Optional[int] = None,
	) -> None:
		self.n_states = n_states
		self.n_actions = n_actions
		self.config = config or AgentConfig()

		self.q_values = np.zeros((n_states, n_actions), dtype=float)
		self._rng = np.random.RandomState(seed)

	# ------------------------------------------------------------------
	# Policy
	# ------------------------------------------------------------------
	def select_action(self, state: State) -> Action:
		"""Select an action using epsilon-greedy over Q(s, a)."""

		if self._rng.rand() < self.config.epsilon:
			return int(self._rng.randint(self.n_actions))

		q_row = self.q_values[state]
		max_value = np.max(q_row)
		# Break ties randomly among best actions.
		best_actions = np.flatnonzero(q_row == max_value)
		return int(self._rng.choice(best_actions))

	# ------------------------------------------------------------------
	# Update (to be implemented by subclasses)
	# ------------------------------------------------------------------
	def update(
		self,
		state: State,
		action: Action,
		reward: float,
		next_state: State,
		next_action: Optional[Action],
		done: bool,
	) -> None:
		raise NotImplementedError


class QLearningAgent(BaseTabularAgent):
	"""Off-policy Q-learning agent.

	Update rule:
	Q(s, a) <- Q(s, a) + alpha * [r + gamma * max_a' Q(s', a') - Q(s, a)]
	For terminal next_state, the bootstrap term is omitted.
	"""

	def update(
		self,
		state: State,
		action: Action,
		reward: float,
		next_state: State,
		next_action: Optional[Action],  # unused but kept for common signature
		done: bool,
	) -> None:
		current_value = self.q_values[state, action]

		if done:
			target = reward
		else:
			max_next = float(np.max(self.q_values[next_state]))
			target = reward + self.config.gamma * max_next

		td_error = target - current_value
		self.q_values[state, action] = current_value + self.config.alpha * td_error


class SarsaAgent(BaseTabularAgent):
	"""On-policy SARSA agent.

	Update rule:
	Q(s, a) <- Q(s, a) + alpha * [r + gamma * Q(s', a') - Q(s, a)]
	where a' is the *actual* next action selected by the current policy.
	For terminal next_state, the bootstrap term is omitted.
	"""

	def update(
		self,
		state: State,
		action: Action,
		reward: float,
		next_state: State,
		next_action: Optional[Action],
		done: bool,
	) -> None:
		current_value = self.q_values[state, action]

		if done or next_action is None:
			target = reward
		else:
			next_value = self.q_values[next_state, next_action]
			target = reward + self.config.gamma * next_value

		td_error = target - current_value
		self.q_values[state, action] = current_value + self.config.alpha * td_error

