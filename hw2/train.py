"""Training script for HW2 Cliff Walking with Q-learning and SARSA.

Usage (from project root):

	python -m hw2.train

This will:
- Train QLearningAgent and SarsaAgent for 500 episodes each
- Record per-episode returns
- Plot learning curves
- Visualize the final greedy path on the 4x12 grid for each agent
"""

from __future__ import annotations

from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from .agents import AgentConfig, QLearningAgent, SarsaAgent
from .env import CliffWalkingEnv, CliffWalkingConfig


EPISODES = 500
NUM_RUNS = 50
SEED = 0
SMOOTH_WINDOW = 20


def run_q_learning(env: CliffWalkingEnv) -> Tuple[List[float], QLearningAgent]:
	config = AgentConfig(epsilon=0.1, alpha=0.1, gamma=0.9)
	agent = QLearningAgent(env.n_states, env.n_actions, config=config, seed=SEED)

	episode_returns: List[float] = []

	for _ in range(EPISODES):
		state = env.reset()
		done = False
		total_reward = 0.0

		while not done:
			action = agent.select_action(state)
			next_state, reward, done, _ = env.step(action)
			agent.update(state, action, reward, next_state, next_action=None, done=done)
			state = next_state
			total_reward += reward

		episode_returns.append(total_reward)

	return episode_returns, agent


def run_sarsa(env: CliffWalkingEnv) -> Tuple[List[float], SarsaAgent]:
	config = AgentConfig(epsilon=0.1, alpha=0.1, gamma=0.9)
	agent = SarsaAgent(env.n_states, env.n_actions, config=config, seed=SEED)

	episode_returns: List[float] = []

	for _ in range(EPISODES):
		state = env.reset()
		action = agent.select_action(state)
		done = False
		total_reward = 0.0

		while not done:
			next_state, reward, done, _ = env.step(action)

			if not done:
				next_action = agent.select_action(next_state)
			else:
				next_action = None

			agent.update(state, action, reward, next_state, next_action=next_action, done=done)

			state = next_state
			action = next_action if next_action is not None else 0
			total_reward += reward

		episode_returns.append(total_reward)

	return episode_returns, agent


def plot_learning_curves(q_returns: List[float], sarsa_returns: List[float]) -> None:
	def moving_average(values: List[float], window: int) -> np.ndarray:
		"""Centered moving average with edge-safe denominator."""

		arr = np.asarray(values, dtype=float)
		if window <= 1:
			return arr
		kernel = np.ones(window, dtype=float)
		numer = np.convolve(arr, kernel, mode="same")
		denom = np.convolve(np.ones_like(arr), kernel, mode="same")
		return numer / np.maximum(denom, 1e-12)

	episodes = np.arange(1, len(q_returns) + 1)
	q_smooth = moving_average(q_returns, SMOOTH_WINDOW)
	sarsa_smooth = moving_average(sarsa_returns, SMOOTH_WINDOW)

	plt.figure(figsize=(8, 5))
	# Keep faint original averages for reference, and emphasize smoothed curves.
	plt.plot(episodes, q_returns, color="tab:blue", alpha=0.2, linewidth=1.0)
	plt.plot(episodes, sarsa_returns, color="tab:orange", alpha=0.2, linewidth=1.0)
	plt.plot(episodes, q_smooth, label=f"Q-learning (MA-{SMOOTH_WINDOW})", color="tab:blue", linewidth=2.2)
	plt.plot(episodes, sarsa_smooth, label=f"SARSA (MA-{SMOOTH_WINDOW})", color="tab:orange", linewidth=2.2)
	plt.xlabel("Episode")
	plt.ylabel("Return (sum of rewards)")
	plt.title(f"Cliff Walking: Episode Returns (averaged over {NUM_RUNS} runs)")
	plt.legend()
	plt.grid(True, alpha=0.3)
	plt.tight_layout()


def derive_greedy_path(env: CliffWalkingEnv, q_values: np.ndarray, max_steps: int = 100) -> List[Tuple[int, int]]:
	"""Roll out a greedy policy from the start state using Q-values.

	Returns a list of (row, col) positions visited, including start and
	(if reached) the goal.
	"""

	positions: List[Tuple[int, int]] = []
	state = env.reset()
	row, col = env.to_pos(state)
	positions.append((row, col))

	for _ in range(max_steps):
		q_row = q_values[state]
		best_action = int(np.argmax(q_row))
		next_state, _, done, _ = env.step(best_action)
		row, col = env.to_pos(next_state)
		positions.append((row, col))
		state = next_state
		if done:
			break

	return positions


def _arrow_for_action(action: int) -> str:
	if action == 0:
		return "↑"
	if action == 1:
		return "→"
	if action == 2:
		return "↓"
	return "←"


def plot_policy_with_path(
	env: CliffWalkingEnv,
	q_values: np.ndarray,
	path: List[Tuple[int, int]],
	title: str,
) -> None:
	"""Plot greedy policy arrows with a dashed final-path overlay."""

	fig, ax = plt.subplots(figsize=(11, 4.5))
	ax.set_xlim(0, env.n_cols)
	ax.set_ylim(env.n_rows, 0)
	ax.set_aspect("equal")
	ax.set_title(title, fontsize=20, weight="bold")

	# Draw cell borders.
	for x in range(env.n_cols + 1):
		ax.plot([x, x], [0, env.n_rows], color="black", linewidth=1.8)
	for y in range(env.n_rows + 1):
		ax.plot([0, env.n_cols], [y, y], color="black", linewidth=1.8)

	# Fill cliff area (bottom row between start and goal).
	for (r, c) in env.cliff_cells:
		rect = plt.Rectangle((c, r), 1, 1, facecolor="#a8c8de", edgecolor="none", zorder=0)
		ax.add_patch(rect)

	# Label start / goal / cliff.
	s_r, s_c = env.start_pos
	g_r, g_c = env.goal_pos
	ax.text(s_c + 0.5, s_r + 0.5, "Start", ha="center", va="center", fontsize=16)
	ax.text(g_c + 0.5, g_r + 0.5, "Goal", ha="center", va="center", fontsize=16)
	ax.text(env.n_cols / 2.0, s_r + 0.5, "Cliff", ha="center", va="center", fontsize=20)

	# Draw greedy action arrows for non-terminal and non-cliff cells.
	for state in range(env.n_states):
		r, c = env.to_pos(state)
		pos = (r, c)
		if pos == env.goal_pos:
			continue
		if pos in env.cliff_cells:
			continue

		action = int(np.argmax(q_values[state]))
		arrow = _arrow_for_action(action)
		ax.text(c + 0.5, r + 0.5, arrow, ha="center", va="center", fontsize=36)

	# Dashed rectangle around each unique path cell (excluding start/goal).
	path_cells = []
	for rc in path:
		if rc == env.start_pos or rc == env.goal_pos:
			continue
		if rc not in path_cells:
			path_cells.append(rc)

	for r, c in path_cells:
		rect = plt.Rectangle(
			(c + 0.08, r + 0.08),
			0.84,
			0.84,
			fill=False,
			linestyle=(0, (3, 3)),
			linewidth=2.5,
			edgecolor="#2a95d6",
		)
		ax.add_patch(rect)

	# Hide axes ticks to match assignment-style diagram.
	ax.set_xticks([])
	ax.set_yticks([])
	plt.tight_layout()


def main() -> None:
	np.random.seed(SEED)

	env_config = CliffWalkingConfig()

	q_runs: List[List[float]] = []
	sarsa_runs: List[List[float]] = []

	q_agent = None
	sarsa_agent = None

	for run_idx in range(NUM_RUNS):
		run_seed = SEED + run_idx
		env_for_q = CliffWalkingEnv(env_config, seed=run_seed)
		env_for_sarsa = CliffWalkingEnv(env_config, seed=run_seed)

		q_returns, q_agent_run = run_q_learning(env_for_q)
		sarsa_returns, sarsa_agent_run = run_sarsa(env_for_sarsa)

		q_runs.append(q_returns)
		sarsa_runs.append(sarsa_returns)

		# Keep the final run agents for policy visualization.
		q_agent = q_agent_run
		sarsa_agent = sarsa_agent_run

	q_avg_returns = np.mean(np.asarray(q_runs, dtype=float), axis=0).tolist()
	sarsa_avg_returns = np.mean(np.asarray(sarsa_runs, dtype=float), axis=0).tolist()

	plot_learning_curves(q_avg_returns, sarsa_avg_returns)

	# Derive and visualize greedy paths from final Q-values.
	if q_agent is None or sarsa_agent is None:
		raise RuntimeError("Training did not produce agents for visualization.")

	env_vis_q = CliffWalkingEnv(env_config, seed=SEED)
	q_path = derive_greedy_path(env_vis_q, q_agent.q_values)
	plot_policy_with_path(env_vis_q, q_agent.q_values, q_path, title="Q-learning policy")

	env_vis_sarsa = CliffWalkingEnv(env_config, seed=SEED)
	sarsa_path = derive_greedy_path(env_vis_sarsa, sarsa_agent.q_values)
	plot_policy_with_path(env_vis_sarsa, sarsa_agent.q_values, sarsa_path, title="Sarsa policy")

	plt.show()


if __name__ == "__main__":
	main()

