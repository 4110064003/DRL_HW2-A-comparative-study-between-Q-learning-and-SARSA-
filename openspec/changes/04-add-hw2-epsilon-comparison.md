# 04 - Add HW2 Epsilon Comparison Experiment

## 1. Why
目前實驗固定使用 `epsilon=0.1`，雖可觀察 Q-learning 與 SARSA 差異，但仍不足以完整分析探索（exploration）強度對學習曲線、穩定性與策略風險的影響。

## 2. What Changes
- 新增多組 epsilon 設定的比較實驗（epsilon sweep）。
- 在相同環境與相同其餘超參數下，分別訓練 Q-learning 與 SARSA。
- 輸出各 epsilon 的平均學習曲線，並彙整最終表現指標（例如最後 N 回合平均回報）。
- 將結果更新至報告，特別補強 exploration 對結果影響的討論。

## 3. Scope
- 主要修改：`hw2/train.py`
- 文件更新：`HW2_Qlearning_vs_SARSA_Report.md`
- 新增輸出圖：epsilon 比較曲線圖（檔名由程式輸出）

## 4. Acceptance Criteria
- 可在同一流程下完成多個 epsilon 值訓練（至少 3 個值）。
- 輸出可視覺化比較圖，清楚呈現不同 epsilon 下的學習差異。
- 報告中「探索（exploration）對結果的影響」段落需依新實驗結果更新。
