# 01 - HW2 Core Architecture: Cliff Walking + Q-learning & SARSA

## 1. Proposal Summary (Why / What / Impact)

### 1.1 Why
為了實作作業二（Cliff Walking Gridworld）的核心架構，需要先在規格層面明確定義環境、演算法邏輯、實驗參數與評估指標，讓後續程式碼實作與比較 Q-learning 與 SARSA 時有一致的標準。

### 1.2 What Changes
- 新增 Cliff Walking 4x12 網格環境的需求：包含起點、終點與懸崖區域定義，以及進入懸崖時給予 -100 獎勵並重置至起點的行為。
- 新增 Q-learning（off-policy）與 SARSA（on-policy）兩種 TD 演算法代理人之需求，明確規範各自的更新公式：
  - Q-learning 目標值須使用 $\max_a Q(S', a)$。
  - SARSA 目標值須使用下一步實際採取動作 $Q(S', A')$。
- 新增統一的實驗訓練參數需求：訓練至少 500 回合，並使用 $\epsilon=0.1, \, \alpha=0.1, \, \gamma=0.9$。
- 新增評估與視覺化需求：記錄每回合的累積獎勵，並能視覺化最終學得策略的路徑（最終路徑）。

### 1.3 Impact
- Affected specs: hw2-core
- Affected code (預期)：
  - 環境實作模組（例如 `env.py` 或 `cliff_env.py`）。
  - 代理人實作模組（例如 `agents/q_learning_agent.py`, `agents/sarsa_agent.py`）。
  - 實驗與繪圖腳本（例如 `train.py`, `plot_results.py`），用於訓練 500+ 回合、記錄累積獎勵並顯示最終路徑。

---

## 2. Implementation Tasks Overview

### 2.1 環境實作
- [ ] 1.1 實作 4x12 Cliff Walking 網格環境（包含狀態空間、動作空間）。
- [ ] 1.2 定義起點、終點與懸崖區域位置（典型為底列起點與終點之間皆為懸崖）。
- [ ] 1.3 實作轉移與獎勵邏輯：
  - [ ] 1.3.1 一般格子步移獎勵為 -1。
  - [ ] 1.3.2 進入懸崖時給予 -100 獎勵並將代理人重置回起點，同時結束該回合。
  - [ ] 1.3.3 抵達終點時結束該回合。

### 2.2 演算法實作
- [ ] 2.1 實作 Q-learning 代理人（off-policy）：
  - [ ] 2.1.1 定義 $Q(s,a)$ 資料結構（例如 NumPy 陣列）。
  - [ ] 2.1.2 實作 $\epsilon$-greedy 策略選擇動作，$\epsilon=0.1$。
  - [ ] 2.1.3 更新規則：
    - $Q(S, A) \leftarrow Q(S, A) + \alpha \bigl[ R + \gamma \max_a Q(S', a) - Q(S, A) \bigr]$。
- [ ] 2.2 實作 SARSA 代理人（on-policy）：
  - [ ] 2.2.1 共用或類似的 $Q(s,a)$ 結構。
  - [ ] 2.2.2 同樣使用 $\epsilon$-greedy 策略選擇動作，$\epsilon=0.1$。
  - [ ] 2.2.3 更新規則：
    - $Q(S, A) \leftarrow Q(S, A) + \alpha \bigl[ R + \gamma Q(S', A') - Q(S, A) \bigr]$，其中 $A'$ 為下一步實際採取的動作。

### 2.3 實驗與評估流程
- [ ] 3.1 建立訓練流程，對 Q-learning 與 SARSA 各訓練至少 500 回合。
- [ ] 3.2 於訓練過程中記錄每回合的累積獎勵（episode return）。
- [ ] 3.3 使用 Matplotlib 對累積獎勵曲線進行視覺化（可分別繪製 Q-learning 與 SARSA）。
- [ ] 3.4 由最終學得的 $Q$ 值或策略，從起點沿著 greedy 策略產生最終路徑並將其視覺化（例如以網格圖標示路徑、懸崖與終點）。

### 2.4 驗證與整理
- [ ] 4.1 使用固定隨機種子驗證結果可重現性（趨勢類似即可）。
- [ ] 4.2 檢查 Q-learning 與 SARSA 在懸崖附近的行為差異，確認 off-policy 與 on-policy 行為有預期的風險偏好差異。
- [ ] 4.3 更新/補充實驗報告或 README，說明環境設定、超參數與主要觀察結果（選做）。

---

## 3. Requirements (Spec Summary: hw2-core)

> 下列內容為 hw2-core delta spec 的彙整，作為作業二核心架構的需求說明。

### 3.1 HW2 Cliff Walking Environment
作業二的 Cliff Walking 環境 SHALL 滿足以下條件：
- 狀態空間為一個 4x12 的離散網格，每個格子代表一個狀態。
- 起點位於網格左下角，終點位於網格右下角。
- 起點與終點之間的底行格子（不含起點與終點）皆為懸崖區域（cliff）。
- 每個時間步移動到非終點且非懸崖的合法格子時，獎勵為 -1。
- 當代理人進入任何懸崖格子時：
  - 立即給予獎勵 -100。
  - 該回合立刻結束，並在下一回合重置代理人到起點。
- 當代理人到達終點格子時，該回合結束，獎勵為 -1（或 0，實作時須明確固定並於程式中註記）。
- 動作空間至少包含向上、向下、向左、向右四種移動；超出邊界的動作應有明確處理（例如保持在原狀態並持續給予 -1 獎勵）。

**Scenario: 一般步移**
- WHEN 代理人從非終點、非懸崖的合法格子採取一個動作，且結果仍在網格內且非懸崖、非終點
- THEN 代理人移動到新格子並得到獎勵 -1，回合持續進行

**Scenario: 進入懸崖**
- WHEN 代理人從任一合法格子採取動作後進入懸崖區域格子
- THEN 該步獲得獎勵 -100，該回合結束，下一回合從起點重新開始

**Scenario: 抵達終點**
- WHEN 代理人從任一合法格子採取動作後進入終點格子
- THEN 回合立即結束，獎勵為事先定義的終點獎勵（-1 或 0）

---

### 3.2 Q-learning Agent (Off-policy)
系統 SHALL 提供一個基於 Q-learning（off-policy）的代理人，符合以下條件：
- 使用 $Q(s,a)$ 表示狀態—動作值函數，可使用 NumPy 陣列或同等結構實作。
- 採用 $\epsilon$-greedy 策略選擇動作，$\epsilon$ 固定為 0.1。
- 學習率 $\alpha$ 固定為 0.1，折扣因子 $\gamma$ 固定為 0.9。
- 在每一步更新時，其 TD 目標值 MUST 使用下一狀態的最大 Q 值 $\max_a Q(S', a)$（off-policy）。

更新公式：
- $Q(S, A) \leftarrow Q(S, A) + \alpha \bigl[ R + \gamma \max_a Q(S', a) - Q(S, A) \bigr]$。

**Scenario: 一般轉移更新（非終點、非懸崖）**
- WHEN 代理人在非終點、非懸崖狀態 $S$ 採取動作 $A$，收到獎勵 $R$ 並轉移到新狀態 $S'$（且回合未結束）
- THEN 系統使用 $R + \gamma \max_a Q(S', a)$ 作為 TD 目標，依上述 Q-learning 公式更新 $Q(S, A)$

**Scenario: 終止狀態更新**
- WHEN 代理人因進入懸崖或終點導致回合結束
- THEN 系統應使用終止狀態的 TD 目標（通常為僅含即時獎勵的形式），並在更新後不再從終止狀態延伸 $\max_a Q(S', a)$

---

### 3.3 SARSA Agent (On-policy)
系統 SHALL 提供一個基於 SARSA（on-policy）的代理人，符合以下條件：
- 使用同樣的 $Q(s,a)$ 結構表示狀態—動作值。
- 採用 $\epsilon$-greedy 策略選擇動作，$\epsilon$ 固定為 0.1。
- 學習率 $\alpha$ 固定為 0.1，折扣因子 $\gamma$ 固定為 0.9。
- 在每一步更新時，其 TD 目標值 MUST 使用下一步實際採取的動作 $A'$ 對應的 $Q(S', A')$（on-policy）。

更新公式：
- $Q(S, A) \leftarrow Q(S, A) + \alpha \bigl[ R + \gamma Q(S', A') - Q(S, A) \bigr]$。

**Scenario: 一般轉移更新（非終點、非懸崖）**
- WHEN 代理人在非終點、非懸崖狀態 $S$ 採取動作 $A$，收到獎勵 $R$ 並轉移到新狀態 $S'$，接著依 $\epsilon$-greedy 政策選出下一動作 $A'$
- THEN 系統使用 $R + \gamma Q(S', A')$ 作為 TD 目標，依上述 SARSA 公式更新 $Q(S, A)$

**Scenario: 終止狀態更新**
- WHEN 代理人因進入懸崖或終點導致回合結束
- THEN 系統在該步更新時不再選取下一動作 $A'$，並使用終止狀態適當的 TD 目標（通常僅含即時獎勵）

---

### 3.4 Training Configuration
系統 SHALL 支援以下統一的訓練設定，以利比較 Q-learning 與 SARSA：
- 每種演算法至少訓練 500 回合（episodes）以上。
- 使用固定的超參數：
  - 探索率 $\epsilon = 0.1$（固定 $\epsilon$-greedy，無遞減）。
  - 學習率 $\alpha = 0.1$。
  - 折扣因子 $\gamma = 0.9$。
- 每回合結束時 MUST 計算並記錄該回合的累積獎勵（episode return）。

**Scenario: 訓練過程記錄**
- WHEN 系統對 Q-learning 或 SARSA 進行訓練
- THEN 對每一回合記錄一次累積獎勵，形成長度至少為 500 的序列，以便後續繪圖與分析

---

### 3.5 Evaluation and Visualization
系統 SHALL 提供對訓練結果的評估與視覺化能力：
- 能以折線圖或類似方式繪製「回合索引 vs 累積獎勵」曲線，分別呈現 Q-learning 與 SARSA 的學習過程。
- 能從最終學得的策略中，從起點狀態開始沿 greedy 策略（對每個狀態選取 $\arg\max_a Q(s,a)$）產生一條最終路徑，直到到達終點或達到最大步數上限。
- 能在 4x12 網格上視覺化最終路徑，例如：
  - 將網格畫出並標示起點、終點與懸崖。
  - 在網格上用特殊標記或顏色顯示代理人最終策略走過的路徑。

**Scenario: 累積獎勵曲線繪圖**
- WHEN 完成 Q-learning 與 SARSA 至少 500 回合的訓練並保存每回合累積獎勵
- THEN 系統能產生對應的學習曲線圖，以便比較兩種演算法的學習穩定性與收斂速度

**Scenario: 最終路徑視覺化**
- WHEN 訓練完成且取得最終的 Q 表或策略
- THEN 系統能從起點出發，依 greedy 策略生成一條到達終點的路徑，並在 4x12 網格上將該路徑與懸崖、終點一併視覺化顯示
