# 03 - Add HW2 50-Run Averaged Learning Curves

## 1. Why
單次訓練曲線受隨機探索影響較大，波動明顯。為了更穩定地比較 Q-learning 與 SARSA 的學習表現，需要使用多次獨立訓練後的平均曲線。

## 2. What Changes
- 將訓練流程由單次 run 改為多次獨立 run（50 runs）。
- 對每個演算法（Q-learning、SARSA）記錄每個 run 的每回合累積獎勵。
- 以 episode 為單位，對 50 runs 取平均，繪製 averaged learning curve。
- 圖標題與圖例補充 averaged over 50 runs 的資訊。

## 3. Scope
- 主要修改：`hw2/train.py`
- 不改動：
  - 環境設定（4x12 cliff walking）
  - 更新公式（Q-learning / SARSA）
  - 基本超參數（epsilon=0.1, alpha=0.1, gamma=0.9）

## 4. Acceptance Criteria
- 執行 `python -m hw2.train` 時，Q-learning 與 SARSA 各自執行 50 runs。
- 學習曲線使用 50 runs 的平均值繪製，而非單次 run。
- 曲線圖標題或註記清楚標示 `averaged over 50 runs`。
- 既有策略圖（箭頭與路徑標記）仍可正常產生。
