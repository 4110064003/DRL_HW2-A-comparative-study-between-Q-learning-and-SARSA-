# 02 - Add HW2 Path Marking Visualization

## 1. Why
目前 HW2 的結果圖已可顯示學習曲線與最終路徑熱度，但缺少像課堂範例圖那樣的「策略方向箭頭」與「路徑虛線框」標示，較不利於直接比較 Q-learning 與 SARSA 的策略差異與風險偏好。

## 2. What Changes
- 新增最終策略視覺化樣式：在每個非終止格顯示 greedy policy 的方向箭頭。
- 新增最終路徑標記：將從起點 rollout 的最終路徑以虛線框線標示。
- 保留懸崖區、起點、終點文字標示，讓圖與作業示意更一致。
- 同步產生 Q-learning policy 圖與 SARSA policy 圖，便於並列比較。

## 3. Scope
- 主要修改：`hw2/train.py`
- 不改動演算法更新公式（Q-learning 與 SARSA）與訓練超參數。

## 4. Acceptance Criteria
- 執行 `python -m hw2.train` 後，除學習曲線外，能顯示兩張策略圖：
  - `Q-learning policy`
  - `Sarsa policy`
- 每張策略圖需包含：
  - 每格 greedy action 的箭頭標記（終止格可不畫）
  - 起點、終點與懸崖區塊
  - 最終路徑的虛線標記
- 圖像可清楚看出 Q-learning 與 SARSA 的路徑差異。
