# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-11-08 依 `main` `2eaaa1c` 查的快照，開工前先重查。

## 現況

從 ai-inbox 以 git-filter-repo 拆出的 Claude Code 脈絡稽核工具集（public，純 Python 標準庫，無第三方依賴）。本機 `python -m unittest discover -s tests` 共 208 項測試（2026-11-08 本機以 Python 3.11.15 與 3.14.10 各跑一次，皆 `Ran 208 tests ... OK`）；CI（`.github/workflows/ci.yml`）在 windows-latest 與 ubuntu-latest 以 Python 3.11 與 3.14 矩陣執行；`2eaaa1c` 的 CI 四個 job（兩個 OS × Python 3.11／3.14）都 success（2026-11-08 `gh run list` 查）。獨立後歷史已壓縮成單一 commit（2026-11-03，維護者決定），拆出前的歷史留在 ai-inbox。各工具的預設門檻多為作者取捨或借自外部專案，尚未在本 repo 量測。

## 近期：可以直接動手

| 項目 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- |
| （目前沒有）| — | — | — |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 核對 Antigravity `agentapi` 介面說明 | 能取得廠商文件 | 對照文件更新兩份文件；查不到就移除該段落 | Claude Sonnet | `docs/long-chat-session-handoff-spec.md`、`templates/session-handoff-brief-prompt.md` 的 `agentapi` 說明只有 ai-inbox 內部紀錄佐證 |
| 同步筆記內的跨筆記連結 | ai-inbox 對應筆記的任務表或狀態變動 | 三篇移入筆記指向的 ai-inbox 網址仍符合現況 | Claude Sonnet | 三篇移入筆記的連結已改為 ai-inbox 網址，但不會自動同步 |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 引入第三方依賴 | 維持純標準庫，免依賴更新與供應鏈面 | 出現標準庫無法合理達成的需求時 |
| 產出 `templates/token-budget-and-loop-breaker.md`（Token 預算上限與死循環熔斷檢核範本） | 來源筆記的任務 `T-20261031-45` 已標「不做」：預算與熔斷的實際設定要看平台，靜態範本幫助有限；成本手冊 `docs/token-economizer-cost-control-spec.md`（第 6 節熔斷）與 `audit_agent_tool_pruning` 已涵蓋可驗證的部分。2026-11-08 沿用該決定 | 有特定平台的預算／熔斷設定項可對照官方文件逐項驗證，或手冊第 6 節被證實不夠用 |

## 維護方式

做完一項就在同一個 commit 刪掉那一列；新工作先寫在這裡再動手。測試指令見 [`AGENTS.md`](AGENTS.md)。
