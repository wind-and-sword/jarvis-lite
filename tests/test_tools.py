import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.tools import ToolNotAllowedError, ToolRegistry


class ToolRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name))
        self.registry = ToolRegistry(self.paths)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_registry_exposes_only_first_stage_tools(self):
        self.assertEqual(
            self.registry.allowed_tool_names,
            {
                "list_data",
                "read_data_file",
                "write_note",
                "write_summary",
                "record_log",
            },
        )

    def test_list_data_hides_project_placeholder_files(self):
        (self.paths.data_dir / ".gitkeep").write_text("", encoding="utf-8")

        result = self.registry.run("list_data")

        self.assertTrue(result.success)
        self.assertEqual(result.output, "data 目录为空。")

    def test_unknown_tool_is_rejected(self):
        with self.assertRaises(ToolNotAllowedError):
            self.registry.run("delete_file", path="important.txt")

    def test_read_data_file_returns_content_and_records_log(self):
        data_file = self.paths.data_dir / "hello.txt"
        data_file.write_text("hello jarvis", encoding="utf-8")

        result = self.registry.run("read_data_file", path="hello.txt")

        self.assertTrue(result.success)
        self.assertEqual(result.output, "hello jarvis")
        self.assertIn("read_data_file", (self.paths.logs_dir / "jarvis.log").read_text(encoding="utf-8"))

    def test_read_data_file_rejects_path_outside_data_dir(self):
        with self.assertRaises(ValueError):
            self.registry.run("read_data_file", path="../README.md")

    def test_write_note_creates_markdown_note_and_records_log(self):
        result = self.registry.run("write_note", title="today", content="开始 Jarvis Lite")

        note_file = self.paths.memory_dir / "notes" / "today.md"
        self.assertTrue(result.success)
        self.assertTrue(note_file.is_file())
        self.assertIn("开始 Jarvis Lite", note_file.read_text(encoding="utf-8"))
        self.assertIn("write_note", (self.paths.logs_dir / "jarvis.log").read_text(encoding="utf-8"))

    def test_write_summary_creates_user_readable_summary(self):
        result = self.registry.run("write_summary", filename="summary.md", content="阶段总结")

        summary_file = self.paths.word_dir / "summary.md"
        self.assertTrue(result.success)
        self.assertTrue(summary_file.is_file())
        self.assertIn("阶段总结", summary_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
