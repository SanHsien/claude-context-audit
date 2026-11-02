"""每支 tools/*.py 的 --help 在 cp950 環境下都要輸出合法 UTF-8，且不得產生副作用。

Windows 管線預設用系統編碼（cp950）。工具若在 argparse 之後才把輸出改成 UTF-8，
--help 會在改之前就印出來，Agent 讀到的是亂碼；沒有 argparse 的工具甚至會把 --help 當成檔名。
副作用檢查：在空的暫存工作目錄執行 --help，結束後目錄必須仍是空的。
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
EXPECTED = {
    "audit_agent_tool_pruning.py",
    "audit_session_memory_compression.py",
    "check_memory_index.py",
    "verify_session_token_sentinel.py",
}


class CliHelpEncodingTest(unittest.TestCase):
    def test_all_four_tools_are_covered(self):
        self.assertEqual({p.name for p in TOOLS.glob("*.py")}, EXPECTED)

    def test_every_tool_help_is_utf8_under_cp950_without_side_effects(self):
        env = {**os.environ, "PYTHONIOENCODING": "cp950", "PYTHONUTF8": "0"}
        for name in sorted(EXPECTED):
            with self.subTest(tool=name), tempfile.TemporaryDirectory() as cwd:
                proc = subprocess.run(
                    [sys.executable, str(TOOLS / name), "--help"],
                    capture_output=True, env=env, cwd=cwd, timeout=60,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace")[-300:])
                text = proc.stdout.decode("utf-8")  # 不是 UTF-8 會在這裡丟 UnicodeDecodeError
                self.assertIn("usage", text)
                self.assertEqual(list(Path(cwd).iterdir()), [], "--help 不應在工作目錄建立任何檔案")


if __name__ == "__main__":
    unittest.main()
