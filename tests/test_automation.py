import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.automation import (
    add_common_directory,
    describe_automation,
    list_common_directories,
    write_daily_report,
)
from jarvis_lite.config import build_project_paths


class AutomationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_common_directory_persists_alias_and_path(self):
        target = Path(self.temp_dir.name) / "projects"
        target.mkdir()

        directory = add_common_directory(self.paths, "项目", target)
        directories = list_common_directories(self.paths)

        self.assertEqual(directory.alias, "项目")
        self.assertEqual(directory.path, target.resolve())
        self.assertEqual(directories, (directory,))

    def test_list_common_directories_reports_empty_state(self):
        output = describe_automation(self.paths)

        self.assertIn("阶段 4 自动化状态", output)
        self.assertIn("常用目录：0 个", output)

    def test_write_daily_report_creates_word_markdown(self):
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 用户偏好：中文回答\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "note.md").write_text("Jarvis Lite 支持日报。\n", encoding="utf-8")
        self.paths.log_path.write_text("2026-05-19T12:00:00\trecord_log\t测试日志\n", encoding="utf-8")

        report = write_daily_report(self.paths, "daily.md")

        content = report.path.read_text(encoding="utf-8")
        self.assertEqual(report.relative_path, "word/daily.md")
        self.assertIn("Jarvis Lite 日报", content)
        self.assertIn("用户偏好：中文回答", content)
        self.assertIn("知识库资料：1 个", content)
        self.assertIn("测试日志", content)


if __name__ == "__main__":
    unittest.main()
