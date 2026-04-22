"""Cliff Walking 4x12 environment for HW2.

The environment follows a minimal Gym-like API:
- reset() -> state (int)
- step(action) -> (next_state, reward, done, info)

Grid layout (row index increases downward):
- shape: 4 x 12
- start: (3, 0)  bottom-left
- goal:  (3, 11) bottom-right
- cliff: cells (3, 1) .. (3, 10)

Actions (int):
- 0: up
- 1: right
- 2: down
- 3: left
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


Action = int
State = int


@dataclass
class CliffWalkingConfig:
	"""Configuration for the Cliff Walking environment.

	The specification for HW2 fixes the grid size to 4x12 and defines
	a single start, goal, and a cliff band between them on the bottom row.
	"""

	n_rows: int = 4
	n_cols: int = 12
	step_reward: float = -1.0
	cliff_reward: float = -100.0
	terminal_reward: float = -1.0  # or 0.0; choose and keep consistent


class CliffWalkingEnv:
	"""4x12 Cliff Walking gridworld environment.

	State is represented as a single integer in [0, n_states).
	You can convert between (row, col) and state using the helper methods
	`to_state` and `to_pos`.
	"""

	def __init__(self, config: CliffWalkingConfig | None = None, seed: int | None = None) -> None:
		self.config = config or CliffWalkingConfig()

		self.n_rows = self.config.n_rows
		self.n_cols = self.config.n_cols
		self.n_states = self.n_rows * self.n_cols
		self.n_actions = 4  # up, right, down, left

		# Coordinate convention: (row, col), row=0 at top, row=3 at bottom.
		self.start_pos = (self.n_rows - 1, 0)
		self.goal_pos = (self.n_rows - 1, self.n_cols - 1)

		# Cliff cells along bottom row between start and goal (exclusive).
		self.cliff_cells = {
			(self.n_rows - 1, c)
			for c in range(1, self.n_cols - 1)
		}

		self._rng = np.random.RandomState(seed)
		self._state: State = self.to_state(*self.start_pos)

	# ------------------------------------------------------------------
	# Public API
	# ------------------------------------------------------------------
	def reset(self) -> State:
		"""Reset environment to the start state and return it."""

		self._state = self.to_state(*self.start_pos)
		return self._state

	def step(self, action: Action) -> Tuple[State, float, bool, Dict]:
		"""Apply an action and return (next_state, reward, done, info).

		- Moves the agent according to the action.
		- If the next cell is a cliff, returns cliff reward and ends episode,
		  with the logical next state being the start state.
		- If the next cell is the goal, returns terminal reward and ends episode.
		- Otherwise, returns step reward and continues.
		"""

		row, col = self.to_pos(self._state)

		# Propose next position based on action.
		if action == 0:  # up
			row -= 1
		elif action == 1:  # right
			col += 1
		elif action == 2:  # down
			row += 1
		elif action == 3:  # left
			col -= 1
		else:
			raise ValueError(f"Invalid action: {action}")

		# If out of bounds, stay in place.
		if not (0 <= row < self.n_rows and 0 <= col < self.n_cols):
			row, col = self.to_pos(self._state)

		pos = (row, col)

		# Check cliff.
		if pos in self.cliff_cells:
			reward = self.config.cliff_reward
			done = True
			next_state = self.to_state(*pos)
			info: Dict[str, object] = {
				"terminated": True,
				"cliff": True,
				"reset_state": self.to_state(*self.start_pos),
			}
			self._state = next_state
			return next_state, float(reward), done, info

		# Check goal.
		if pos == self.goal_pos:
			reward = self.config.terminal_reward
			done = True
			next_state = self.to_state(*pos)
			info = {"terminated": True, "goal": True}
			self._state = next_state
			return next_state, float(reward), done, info

		# Normal step.
		reward = self.config.step_reward
		done = False
		next_state = self.to_state(*pos)
		info = {"terminated": False}
		self._state = next_state
		return next_state, float(reward), done, info

	# ------------------------------------------------------------------
	# Helper methods
	# ------------------------------------------------------------------
	def to_state(self, row: int, col: int) -> State:
		"""Convert (row, col) to a single integer state id."""

		return row * self.n_cols + col

	def to_pos(self, state: State) -> Tuple[int, int]:
		"""Convert integer state id back to (row, col)."""

		row = state // self.n_cols
		col = state % self.n_cols
		return row, col

	def sample_action(self) -> Action:
		"""Sample a random action uniformly from the action space."""

		return int(self._rng.randint(self.n_actions))

