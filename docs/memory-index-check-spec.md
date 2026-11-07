# 記憶索引檢查規範：`check_memory_index` 的判定、門檻與校準

> 對應工具：[`tools/check_memory_index.py`](../tools/check_memory_index.py)｜測試：[`tests/test_check_memory_index.py`](../tests/test_check_memory_index.py)
> 來源筆記留在 ai-inbox：[`notes/2026-10-26-ai-shared-memory-template-team-collaboration.md`](https://github.com/SanHsien/ai-inbox/blob/main/notes/2026-10-26-ai-shared-memory-template-team-collaboration.md)（本 repo 不收，內容未在此重驗）。
> 本文只描述程式實際的行為。標「作者取捨」的門檻沒有外部依據；標「回報」的數字是一次本機執行的結果，未存檔。

## 1. 它在擔心什麼

Claude Code 這類工具開場會載入一份記憶索引（`MEMORY.md`，一行一個指標），內文才按需讀取。索引與檔案一旦不同步，會出現三種問題：

| 問題 | 後果 |
| :--- | :--- |
| 索引指向不存在的檔 | 載入時讀不到，或誤以為記憶還在 |
| 記憶檔沒進索引 | 檔案存在但永遠不會被想起 |
| 索引過長或單行過長 | 開場就吃掉脈絡預算 |

工具是**唯讀**的：只讀資料夾，不改任何檔案，輸出到標準輸出。

## 2. 資料模型

```text
記憶資料夾/
├── MEMORY.md            主索引，一行一個指標：- [name.md](name.md) — 一行描述
├── INDEX-*.md           子索引：只有被主索引（或另一個已被跟隨的子索引）指到才會被讀
├── <name>.md            記憶檔，需要 frontmatter：name、description、type
└── daily-log-*.md       預設排除，不要求進索引
```

- 只看**頂層**的 `.md`；子資料夾裡的檔只在被索引指到時才檢查是否存在。
- 子索引可再指向子索引，已跟隨過的不會重複讀（防循環）。
- `--max-entries` 只算 `MEMORY.md` 自己的指標，因為開場載入的是它。
- `type` 可寫在 frontmatter 頂層，也可在 `metadata:` 底下。

## 3. 檢查項目與嚴重度

ERROR 一定讓結束碼為 1；WARN 預設只提醒，加 `--strict` 才失敗。

| 嚴重度 | 代碼 | 觸發條件 |
| :--- | :--- | :--- |
| ERROR | `no-index` | 資料夾裡沒有 `MEMORY.md`（工具直接結束，不做其他檢查） |
| ERROR | `broken-link` | 指標指向不存在的檔；大小寫不符也算（Windows 不分大小寫，Linux／macOS 分），訊息會附實際檔名 |
| ERROR | `outside-dir` | 指標是絕對路徑、磁碟機代號開頭，或含 `..` |
| ERROR | `unindexed` | 頂層 `.md` 沒出現在主索引或任何被跟隨的子索引（`daily-log-*.md` 與 `--ignore` 除外） |
| ERROR | `no-frontmatter` | 缺 frontmatter、沒有結尾的 `---`，或缺 `name`／`description`／`type` 任一欄 |
| ERROR | `unreadable` | 檔案不是合法 UTF-8，或讀取失敗 |
| WARN | `duplicate` | 同一個檔在索引中出現多次 |
| WARN | `multi-pointer` | 一行有多個指標 |
| WARN | `long-line` | 索引行（含子索引）超過 `--max-line-chars` |
| WARN | `too-many` | `MEMORY.md` 的指標數超過 `--max-entries` |
| WARN | `name-mismatch` | frontmatter 的 `name` 與檔名（去掉 `.md`）不同 |
| WARN | `unknown-type` | `type` 不在 `--types` 清單 |
| WARN | `dead-wikilink` | `[[name]]` 指向不存在的記憶；圍欄程式碼區塊與行內程式碼內的不算 |

`INDEX-*.md` 本身不要求 frontmatter。`http://` 之類帶 scheme 的連結與 `#` 開頭的錨點不當成索引指標。

## 4. 門檻

| 選項 | 預設 | 性質 |
| :--- | :--- | :--- |
| `--max-entries` | 60 | **作者取捨**，只警告，未在本 repo 量測過 |
| `--max-line-chars` | 200 | **作者取捨**，只警告，未在本 repo 量測過 |
| `--types` | `user,feedback,project,reference,insight` | 作者自己的記憶分類；別的專案用別的分類就改這個 |
| `--ignore` | `daily-log-*.md` | 可重複；`--no-default-ignore` 取消預設排除 |
| `--skip-frontmatter` | 無 | 仍須進索引，但不檢查 frontmatter |

兩個數字門檻都是 WARN，不會讓結束碼變 1（除非加 `--strict`），所以放寬它們不會藏起 ERROR。

## 5. 結束碼與輸出

| 結束碼 | 意義 |
| :--- | :--- |
| 0 | 沒有 ERROR（加 `--strict` 時也沒有 WARN） |
| 1 | 有 ERROR，或 `--strict` 且有 WARN |
| 2 | 參數錯誤或資料夾不存在（錯誤訊息印在標準錯誤） |

預設輸出每個發現一行，最後一行是摘要。`--json` 改輸出 `stats`（`index_entries`、`sub_index_entries`、`memory_files`）、`errors`、`warnings`、`by_code` 與 `findings` 陣列。

用假資料跑出來的實際輸出（三個記憶檔：一個指標指向不存在的檔、一個檔沒進索引、一個 frontmatter 的 `name`／`type` 不合）：

```text
ERROR broken-link    MEMORY.md:3  指向不存在的檔：missing.md
ERROR unindexed      orphan.md  沒有出現在 MEMORY.md 或其子索引
WARN  name-mismatch  feedback-b.md:1  name 是 wrong，檔名是 feedback-b
WARN  unknown-type   feedback-b.md:1  type 是 weird，不在 user, feedback, project, reference, insight
ERROR no-frontmatter orphan.md:1  缺 frontmatter（或沒有結尾的 ---）
WARN  dead-wikilink  user-a.md:6  [[nope]] 沒有對應的記憶檔
索引指標 3 條（子索引另 0 條）；頂層記憶檔 3 個；ERROR 3、WARN 3（broken-link=1, dead-wikilink=1, name-mismatch=1, no-frontmatter=1, unindexed=1, unknown-type=1）
```

## 6. 校準方式

預設門檻不一定適合你的資料夾。照這個順序調，不要憑感覺：

1. 先不帶任何門檻選項跑 `--json`，看 `stats.index_entries`、`by_code`。
2. ERROR 先全部清掉：它們代表索引與檔案真的不一致，不是門檻問題。
3. 看 WARN 是否集中在 `too-many`／`long-line`。若是，決定要**縮索引**（把低頻條目移到 `INDEX-*.md` 子索引，主索引只留高頻）還是**放寬門檻**；前者才真的降低開場成本，後者只是讓警告消失。
4. 子索引不計入 `--max-entries`，所以把條目搬進子索引會讓 `too-many` 消失；這是設計用途，但要確認開場真的只載入主索引。
5. 用 `--strict` 放進 CI 或排程前，先確認 WARN 為 0，否則會一直失敗。

回報（一次本機唯讀執行，未存檔；對象是作者自己的記憶資料夾）：主索引 89 條、子索引另 124 條、頂層記憶檔 209 個，ERROR 0、WARN 8（`dead-wikilink` 4、`long-line` 1、`name-mismatch` 2、`too-many` 1）。也就是說作者自己的資料夾就超過預設的 60 條，`too-many` 是否該調高或改為縮索引，尚未決定；這也是預設門檻「未量測」的具體例子。

## 7. 已知極限

- 只檢查結構與連結，不判斷記憶**內容**是否過時、重複或互相矛盾。
- `dead-wikilink` 只處理 `[[name]]`、`[[name|別名]]`、`[[name#段落]]` 三種寫法，目標只與頂層檔名及索引內的子路徑比對。
- 只認 `- ` 或 `* ` 開頭的條列行為索引行；其他格式的連結不會被當成指標。
- 不檢查 frontmatter 欄位值的語意（`description` 只要非空即可）。
