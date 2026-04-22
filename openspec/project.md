# Project Context

## Purpose
This project studies and compares two temporal-difference reinforcement learning methods, Q-learning and SARSA, in the Cliff Walking Gridworld.
The goal is to analyze learning stability, convergence speed, and policy risk sensitivity under the same environment and hyperparameter settings.

## Tech Stack
- Python (primary implementation language)
- NumPy (numerical computation and Q-table operations)
- Matplotlib (training curve and policy visualization)
- Gymnasium (optional, for environment interoperability and benchmarking)

## Project Conventions

### Code Style
- Follow PEP 8 for formatting, naming, and module organization.
- Use object-oriented design for agent implementations (for example, a shared base agent and algorithm-specific subclasses).
- Add clear docstrings for all public modules, classes, and functions, including parameters, returns, and behavior notes.
- Prefer descriptive names (e.g., `learning_rate`, `epsilon_decay`) over abbreviations.

### Architecture Patterns
- Environment and agent are separated to keep transition logic independent from learning logic.
- Implement algorithm variants as interchangeable agent classes with a common interface (for example: `select_action`, `update`, `train_episode`).
- Keep experiment orchestration (training loop, logging, plotting) separate from core learning components.
- Centralize configuration (grid size, cliff positions, epsilon schedule, random seed) to support reproducible experiments.

### Testing Strategy
- Use deterministic seeds to validate reproducibility of training trends.
- Add unit tests for environment transitions, reward assignment, terminal-state handling, and boundary behavior.
- Add agent update-rule tests to verify Q-learning and SARSA target calculations against expected values.
- Run short smoke-training runs to verify that cumulative reward trends improve over time for both algorithms.

### Git Workflow
- Use short-lived feature branches (for example, `feature/sarsa-agent`, `feature/plot-metrics`) and merge through pull requests.
- Use concise, imperative commit messages (for example, `Add SARSA update rule test`).
- Keep commits focused by separating refactors, features, and experiment result updates when possible.

## Domain Context
- Environment: Cliff Walking Gridworld with dimensions 4x12.
- Typical setup: start at lower-left, goal at lower-right, and cliff cells along the bottom row between start and goal.
- Cliff penalty is high and resets the episode to the start state; this highlights the behavioral difference between off-policy Q-learning and on-policy SARSA.
- Key comparison dimensions: cumulative reward, episode length, convergence behavior, and policy safety near cliff cells.

## Important Constraints
- All algorithm comparisons should use aligned settings (episodes, alpha, gamma, epsilon policy) unless a specific ablation is intended.
- Keep implementation readable for coursework evaluation and reproducibility.
- Avoid introducing unnecessary dependencies beyond Python, NumPy, Matplotlib, and optional Gymnasium.
- Visual outputs should be reproducible from code (no manual post-processing assumptions).

## External Dependencies
- Python runtime and standard library
- NumPy
- Matplotlib
- Gymnasium (optional)
