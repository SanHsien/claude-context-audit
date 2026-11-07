# AGENTS.md

Claude Code 本機 context 與 token 稽核工具。專案指令只放在本檔（不建 `CLAUDE.md`、`GEMINI.md`）。

## 鐵律

1. **只用 Python 標準函式庫**。不加第三方依賴，不加 `requirements.txt`。
2. **稽核工具對輸入唯讀**。只有明確指定的輸出參數（`--output`、`--deny-out`）才寫檔，`--deny-out` 不覆寫既有檔；哨兵 `hook` 只寫自己的狀態檔（`--state-dir`）。
3. **`--help` 在 cp950 終端下必須正常**，且不得產生副作用。由 `tests/test_cli_help_encoding.py` 守住；新增工具要同步登記進該測試。
4. **不設 `PYTHONUTF8` 讓測試通過**。編碼問題在工具內修，CI 也不設。
5. **不放機密、不放個人路徑**。範例與測資用假資料；家目錄寫 `C:\Users\<you>` 或 `~`。
6. **不捏造**。文件只描述實際存在、實際測過的行為；外部事實要有出處，沒查證就標「未驗證」。
7. **只打自己的 repo**：PR、push、release 一律指向 `SanHsien/claude-context-audit`。
8. 後續工作的唯一來源是 [`ROADMAP.md`](ROADMAP.md)；做完要回去更新。

## 開發流程

1. 先讀對應的 `docs/` 規範與工具檔頭（判定語意與結束碼寫在那裡）。
2. 改程式一定同步改測試；修 bug 先寫會失敗的測試。
3. 全套測試（CI 矩陣跑 Python 3.11 與 3.14；本機至少跑其中一個）：

   ```
   python -m unittest discover -s tests
   ```

4. **測試全綠才 commit**，驗證與提交之間用 `&&` 串接，不可用 `;`：

   ```
   python -m unittest discover -s tests && git add -A && git commit -m "fix(tool): ..."
   ```

5. commit 訊息用英文 conventional commits（`feat`、`fix`、`docs`、`test`、`chore`）。
6. 改了工具的選項、結束碼或行為，同步更新 `README.md` 工具表與對應 `docs/`。
7. 修復 `REVIEW.md` 列出的問題時，回註修復 commit hash 與日期（目前尚無 `REVIEW.md`，第一次 review 時建立）。

## 目錄結構

```
tools/       四支 CLI 工具（各一個檔，無相依）
tests/       unittest；每支工具一份，加上 test_cli_help_encoding.py
docs/        工具的規範文件（判定依據、取捨、已知極限）
templates/   可複製到別的專案的範本
notes/       從 ai-inbox 移入的來源筆記（保留原文，不當作現行規範）
.github/workflows/ci.yml   windows-latest + ubuntu-latest × Python 3.11／3.14，unittest
ROADMAP.md   後續工作
```

## CI

`.github/workflows/ci.yml`：`permissions: contents: read`，actions 釘 commit SHA，跑 `python -m unittest discover -s tests -v`。升級 action 時換 SHA 並保留版本註解。
