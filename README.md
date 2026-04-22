# DRL HW2: Q-learning vs SARSA (Cliff Walking)

本專案比較兩種 TD 控制方法在 Cliff Walking 環境中的表現：
- Q-learning（Off-policy）
- SARSA（On-policy）

核心目標是比較三件事：
- 學習表現（每回合累積獎勵曲線）
- 最終策略行為（路徑是否貼近懸崖）
- 穩定性（訓練波動與 exploration 影響）

## Environment
- Grid: `4 x 12`
- Start: 左下角
- Goal: 右下角
- Cliff: 底列起點與終點之間
- Reward:
  - 一般步移：`-1`
  - 進入懸崖：`-100`

## Training Setup
- Baseline setting:
  - `episodes = 500`
  - `runs = 50`（取平均）
  - `epsilon = 0.1`
  - `alpha = 0.1`
  - `gamma = 0.9`
- Epsilon comparison:
  - `epsilon in [0.01, 0.1, 0.3]`
  - 額外做輕量 sweep 比較 exploration 影響

## Project Structure

- `hw2/`：核心程式碼（環境、代理人、訓練流程）
- `assets/images/`：實驗結果圖片
- `docs/reports/`：報告 PDF / MD
- `docs/transcripts/`：對話整理檔
- `scripts/`：startup / ending 腳本

## Results (PNG)

### 1. Baseline reward curve (50-run average)
![Reward Curve 50-run Average](assets/images/reward_curve_50runAverage.png)

說明：
- 兩種方法都能隨訓練提升回報。
- Q-learning 與 SARSA 收斂速度接近，但波動特性不同。

### 2. Final policy: Q-learning
![Q-learning Policy](assets/images/Q_learning_policy.png)

說明：
- Q-learning 常學到較貼近懸崖的短路徑。
- 在有探索時可能承擔較高風險。

### 3. Final policy: SARSA
![SARSA Policy](assets/images/Sarsa_policy.png)

說明：
- SARSA 傾向保守路徑，與懸崖保持更安全距離。
- 在持續探索下通常更穩健。

### 4. Epsilon comparison
![Epsilon Comparison](assets/images/reward_curve_epsilon_comparison.png)

說明：
- `epsilon` 增大時（探索更強），兩者回報都下降。
- 中高探索下，SARSA 通常比 Q-learning 更穩定。

## Key Takeaways
- Q-learning（Off-policy）
  - 更新使用 `max_a Q(S', a)`。
  - 傾向理論最優，但高探索時可能較冒險。
- SARSA（On-policy）
  - 更新使用實際下一動作 `Q(S', A')`。
  - 會反映探索策略影響，通常較保守、較穩定。

## How To Run
在專案根目錄執行：

```bash
python -m hw2.train
```

執行後會產生/更新：
- `assets/images/reward_curve_50runAverage.png`
- `assets/images/Q_learning_policy.png`
- `assets/images/Sarsa_policy.png`
- `assets/images/reward_curve_epsilon_comparison.png`

## Report
完整分析請見：
- `docs/reports/HW2_Qlearning_vs_SARSA_Report.md`
- `docs/reports/HW2_Qlearning_vs_SARSA_Report.pdf`

對話整理：
- `docs/transcripts/conversation_transcript.md`
- `docs/transcripts/conversation_transcript.pdf`

## Scripts
- `scripts/startup.cmd` / `scripts/startup.ps1`: 抓取或更新專案內容
- `scripts/ending.cmd` / `scripts/ending.ps1`: 快速 commit + push（可自訂 commit message）

### ending.cmd 使用方式

建議直接傳入 commit message：

```bat
scripts\ending.cmd "新增AI chat紀錄、歸檔整理"
```

若使用標籤式寫法，也可：

```bat
scripts\ending.cmd "CommitMessage" "新增AI chat紀錄、歸檔整理"
```

注意：第二種寫法的兩個引號之間要有空白，不能寫成連在一起的 `"CommitMessage""新增..."`。
