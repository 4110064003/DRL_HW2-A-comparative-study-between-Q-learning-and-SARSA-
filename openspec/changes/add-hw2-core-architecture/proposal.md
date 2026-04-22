## Why
為了實作作業二（Cliff Walking Gridworld）的核心架構，需要先在規格層面明確定義環境、演算法邏輯、實驗參數與評估指標，讓後續程式碼實作與比較 Q-learning 與 SARSA 時有一致的標準。

## What Changes
- 新增 Cliff Walking 4x12 網格環境的需求：包含起點、終點與懸崖區域定義，以及進入懸崖時給予 -100 獎勵並重置至起點的行為。
- 新增 Q-learning（off-policy）與 SARSA（on-policy）兩種 TD 演算法代理人之需求，明確規範各自的更新公式：
  - Q-learning 目標值須使用 $\max_a Q(S', a)$。
  - SARSA 目標值須使用下一步實際採取動作 $Q(S', A')$。
- 新增統一的實驗訓練參數需求：訓練至少 500 回合，並使用 $\epsilon=0.1, \, \alpha=0.1, \, \gamma=0.9$。
- 新增評估與視覺化需求：記錄每回合的累積獎勵，並能視覺化最終學得策略的路徑（最終路徑）。

## Impact
- Affected specs: hw2-core
- Affected code (預期)：
  - 環境實作模組（例如 `env.py` 或 `cliff_env.py`）。
  - 代理人實作模組（例如 `agents/q_learning_agent.py`, `agents/sarsa_agent.py`）。
  - 實驗與繪圖腳本（例如 `train.py`, `plot_results.py`），用於訓練 500+ 回合、記錄累積獎勵並顯示最終路徑。
