# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-11-03 依 `main` 查的快照，開工前先重查。

## 現況

從 ai-inbox 以 git-filter-repo 拆出的 Claude Code 脈絡稽核工具集（public，純 Python 標準庫，無第三方依賴）。本機 `python -m unittest discover -s tests` 共 208 項測試；CI（`.github/workflows/ci.yml`）在 windows-latest 與 ubuntu-latest 以 Python 3.11 執行。獨立後歷史已壓縮成單一 commit（2026-11-03，維護者決定），拆出前的歷史留在 ai-inbox。各工具的預設門檻多為作者取捨或借自外部專案，尚未在本 repo 量測。

## 近期：可以直接動手

| 項目 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- |
| 產出 `templates/token-budget-and-loop-breaker.md`（多 Agent 專案 Token 預算上限與死循環熔斷檢核範本） | 檔案存在、內容含預算上限與熔斷條件檢核項；筆記內的路徑連結可解析；測試全綠 | Claude Sonnet | `notes/2026-10-31-microsoft-tokeneconomizer-experience-driven-cost-control.md` 該任務仍未勾選且指向不存在的檔案（ai-inbox 任務 `T-20261031-45`） |
| 補 `check_memory_index` 的規範文件 `docs/` | `docs/` 下有規範檔並從 README 連結；內容涵蓋門檻與校準方式 | Claude Sonnet | `tools/` 內該工具目前只有檔頭說明；對應筆記仍在 ai-inbox（連結見 README） |
| CI 加跑較新的 Python | `ci.yml` 矩陣含較新版本且在兩個 OS 都綠 | Claude Sonnet | `.github/workflows/ci.yml` 目前只跑 3.11；本機另以 3.14 跑過一次全套測試 |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 核對 Antigravity `agentapi` 介面說明 | 能取得廠商文件 | 對照文件更新兩份文件；查不到就移除該段落 | Claude Sonnet | `docs/long-chat-session-handoff-spec.md`、`templates/session-handoff-brief-prompt.md` 的 `agentapi` 說明只有 ai-inbox 內部紀錄佐證 |
| 同步筆記內的跨筆記連結 | ai-inbox 對應筆記的任務表或狀態變動 | 三篇移入筆記指向的 ai-inbox 網址仍符合現況 | Claude Sonnet | 三篇移入筆記的連結已改為 ai-inbox 網址，但不會自動同步 |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 引入第三方依賴 | 維持純標準庫，免依賴更新與供應鏈面 | 出現標準庫無法合理達成的需求時 |

## 維護方式

做完一項就在同一個 commit 刪掉那一列；新工作先寫在這裡再動手。測試指令見 [`AGENTS.md`](AGENTS.md)。
