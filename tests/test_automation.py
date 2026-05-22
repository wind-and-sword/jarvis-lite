import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.automation import (
    add_common_directory,
    describe_automation,
    list_common_directories,
    preview_file_organization,
    record_directory_open_request,
    write_daily_report,
)
from jarvis_lite.config import build_project_paths
from jarvis_lite.memory import append_experience
from jarvis_lite.runtime_context import RuntimeContext, RuntimeDirectoryContext, save_runtime_context


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
        append_experience(self.paths, "导入资料后先打标签")
        self.paths.log_path.write_text("2026-05-19T12:00:00\trecord_log\t测试日志\n", encoding="utf-8")

        report = write_daily_report(self.paths, "daily.md")

        content = report.path.read_text(encoding="utf-8")
        self.assertEqual(report.relative_path, "word/daily.md")
        self.assertIn("Jarvis Lite 日报", content)
        self.assertIn("用户偏好：中文回答", content)
        self.assertIn("知识库资料：1 个", content)
        self.assertIn("经验记忆", content)
        self.assertIn("导入资料后先打标签", content)
        self.assertIn("测试日志", content)

    def test_write_daily_report_includes_runtime_recent_context(self):
        project_dir = Path(self.temp_dir.name) / "project"
        project_dir.mkdir()
        save_runtime_context(
            self.paths,
            RuntimeContext(
                recent_document_path="note.md",
                recent_directory=RuntimeDirectoryContext(alias="项目", path=str(project_dir.resolve())),
                recent_search_result_paths=("note.md", "manual.md"),
                recent_advice_suggestions=("/read note.md：读取当前资料",),
            ),
        )

        report = write_daily_report(self.paths, "context-daily.md")

        content = report.path.read_text(encoding="utf-8")
        self.assertIn("## 最近上下文", content)
        self.assertIn("最近资料：data/note.md", content)
        self.assertIn(f"最近目录：项目 -> {project_dir.resolve()}", content)
        self.assertIn("最近搜索结果：2 条", content)
        self.assertIn("1. data/note.md", content)
        self.assertIn("最近建议：1 条", content)
        self.assertIn("/read note.md：读取当前资料", content)

    def test_preview_file_organization_groups_files_by_extension(self):
        target = Path(self.temp_dir.name) / "desktop"
        target.mkdir()
        (target / "notes.md").write_text("笔记", encoding="utf-8")
        (target / "todo.TXT").write_text("待办", encoding="utf-8")
        (target / "README").write_text("无后缀", encoding="utf-8")
        (target / "nested").mkdir()

        preview = preview_file_organization(target)

        self.assertEqual(preview.directory, target.resolve())
        self.assertEqual(preview.file_count, 3)
        self.assertEqual(preview.skipped_directory_count, 1)
        groups = {group.extension_label: group for group in preview.groups}
        self.assertEqual(groups[".md"].target_folder, "md")
        self.assertEqual(groups[".txt"].target_folder, "txt")
        self.assertEqual(groups["无后缀"].target_folder, "no-extension")
        self.assertEqual(groups[".md"].files, ("notes.md",))
        self.assertEqual(groups[".txt"].files, ("todo.TXT",))
        self.assertEqual(groups["无后缀"].files, ("README",))

    def test_record_directory_open_request_writes_transcript(self):
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()

        record = record_directory_open_request(self.paths, "项目", target)

        content = record.path.read_text(encoding="utf-8")
        self.assertEqual(record.relative_path, "logs/desktop-actions.txt")
        self.assertIn("open_directory", content)
        self.assertIn("项目", content)
        self.assertIn(str(target.resolve()), content)


if __name__ == "__main__":
    unittest.main()
