# claude-context-audit

Claude Code 本機的 context 與 token 稽核工具：從 transcript 與記憶檔找出多餘的工具定義、壓縮後遺失的事實、以及長對話該交接的時機。全部只用 Python 標準函式庫，沒有第三方依賴。

```
transcript (JSONL) ──┬─> audit_agent_tool_pruning ──────> 從沒用過的工具 -> 建議 permissions.deny
                     ├─> audit_session_memory_compression ─> 記憶壓縮後事實／決策因果遺失率
                     └─> verify_session_token_sentinel ───> token 達門檻 -> 提示交接（UserPromptSubmit hook）

記憶資料夾 (MEMORY.md + INDEX-*.md + 記憶檔) ──> check_memory_index ──> 索引與實際檔案是否一致
```

三支稽核工具對輸入唯讀（只有明確指定的 `--output`／`--deny-out` 會寫檔，`--deny-out` 不覆寫既有檔）；哨兵的 `hook` 子命令會在 `--state-dir`（預設系統暫存）記錄已提示的級距。

## 工具

| 指令 | 用途 | 結束碼 |
|------|------|--------|
| `python tools/audit_agent_tool_pruning.py S1.jsonl S2.jsonl --catalog catalog.json` | 統計工具呼叫頻率，找出整批 transcript 都沒用過的工具，建議加進 `permissions.deny` | 0 完成（含沒有建議）；2 輸入或參數有問題 |
| `python tools/audit_session_memory_compression.py --transcript T.jsonl --memory M.md` | 檢查 session 壓縮成記憶後，關鍵事實與決策因果有沒有遺失 | 0 PASS；1 FAIL；2 輸入或參數有問題 |
| `python tools/verify_session_token_sentinel.py <check\|simulate\|classify\|title\|cost\|hook> ...` | 長對話 token 哨兵：量測、模擬、判定，以及可直接當 UserPromptSubmit hook 的 `hook` 子命令 | 0 通過；1 驗證失敗或量不到（`hook` 絕不回 2）；2 其他子命令的參數錯誤 |
| `python tools/check_memory_index.py <記憶資料夾>` | 檢查 `MEMORY.md` 及其指向的 `INDEX-*.md` 子索引與實際記憶檔是否一致 | 0 通過；1 有 ERROR（加 `--strict` 則 WARN 也算）；2 參數或資料夾錯誤 |

各工具的完整選項看 `--help`；判定語意與取捨寫在檔頭與對應文件：

| 工具 | 文件 |
|------|------|
| `audit_agent_tool_pruning` | [`docs/token-economizer-cost-control-spec.md`](docs/token-economizer-cost-control-spec.md)、[筆記](notes/2026-10-31-microsoft-tokeneconomizer-experience-driven-cost-control.md) |
| `audit_session_memory_compression` | [`docs/claude-code-cross-session-memory-evaluation-guide.md`](docs/claude-code-cross-session-memory-evaluation-guide.md)、[`templates/cross-session-memory-curation-spec.md`](templates/cross-session-memory-curation-spec.md)、[筆記](notes/2026-10-31-claude-code-cross-session-memory-claudemem-vs-claudemd.md) |
| `verify_session_token_sentinel` | [`docs/long-chat-session-handoff-spec.md`](docs/long-chat-session-handoff-spec.md)、[`templates/session-handoff-brief-prompt.md`](templates/session-handoff-brief-prompt.md)、[筆記](notes/2026-11-02-littlehole-claude-saver-long-chat-session-handoff.md) |
| `check_memory_index` | [`docs/memory-index-check-spec.md`](docs/memory-index-check-spec.md)；對應筆記留在 ai-inbox：[`notes/2026-10-26-ai-shared-memory-template-team-collaboration.md`](https://github.com/SanHsien/ai-inbox/blob/main/notes/2026-10-26-ai-shared-memory-template-team-collaboration.md) |

## 快速開始

需要 Python 3.11 以上，不必安裝任何套件。

```
git clone https://github.com/SanHsien/claude-context-audit.git
cd claude-context-audit
python -m unittest discover -s tests
python tools/check_memory_index.py <你的記憶資料夾>
python tools/verify_session_token_sentinel.py simulate --tokens 100000,150000,160000,199999,200000,250000 --expect silent,notify,inject,inject,notify,notify
```

把哨兵接成 hook 的設定範例見 [`docs/long-chat-session-handoff-spec.md`](docs/long-chat-session-handoff-spec.md)。

## 與 ai-inbox 的關係

這些檔案原本在 [`SanHsien/ai-inbox`](https://github.com/SanHsien/ai-inbox)（收文章、拆任務的收件匣），用 git-filter-repo 切出來；獨立後歷史已壓縮成單一 commit，拆出前的歷史留在 ai-inbox。`notes/` 的三篇筆記保留原文，任務表與狀態停在移出當時（2026-11-02）；筆記內提到的 `build_index.py`、`task_cli.py` 等指令和其他筆記是 ai-inbox 專用，已改成指向 ai-inbox 的連結或原樣保留。

## 授權

MIT，見 [`LICENSE`](LICENSE)。後續工作見 [`ROADMAP.md`](ROADMAP.md)；開發規則見 [`AGENTS.md`](AGENTS.md)。
