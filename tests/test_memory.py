import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.memory import append_memory, find_identity, is_identity_question, parse_identity_fact, read_profile, summarize_profile


class MemoryTests(unittest.TestCase):
    def test_read_profile_returns_markdown_content(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir))
            profile = paths.memory_dir / "profile.md"
            profile.write_text("# 长期记忆\n\n- 用户偏好：中文回答\n", encoding="utf-8")

            content = read_profile(paths)

            self.assertIn("用户偏好：中文回答", content)

    def test_read_profile_returns_clear_message_when_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir))

            content = read_profile(paths)

            self.assertIn("还没有长期记忆", content)

    def test_summarize_profile_uses_first_meaningful_bullet(self):
        content = "# 长期记忆\n\n- 用户偏好：中文回答\n- 项目目标：本地助手\n"

        summary = summarize_profile(content)

        self.assertEqual(summary, "用户偏好：中文回答")

    def test_summarize_profile_skips_markdown_metadata(self):
        content = "# 长期记忆\n\n> 日期：2026-05-18\n> 执行者：Codex\n\n- 用户偏好：中文回答\n"

        summary = summarize_profile(content)

        self.assertEqual(summary, "用户偏好：中文回答")

    def test_append_memory_creates_profile_and_adds_bullet(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir))

            append_memory(paths, "用户姓名：张三")

            content = read_profile(paths)
            self.assertIn("# 长期记忆", content)
            self.assertIn("- 用户姓名：张三", content)

    def test_append_memory_does_not_duplicate_existing_fact(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir))

            append_memory(paths, "用户姓名：张三")
            append_memory(paths, "用户姓名：张三")

            content = read_profile(paths)
            self.assertEqual(content.count("用户姓名：张三"), 1)

    def test_append_memory_updates_existing_keyed_fact(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir))

            append_memory(paths, "用户姓名：张三")
            append_memory(paths, "用户姓名：李四")

            content = read_profile(paths)
            self.assertNotIn("用户姓名：张三", content)
            self.assertIn("用户姓名：李四", content)
            self.assertEqual(content.count("用户姓名："), 1)

    def test_find_identity_extracts_name_and_role(self):
        content = "# 长期记忆\n\n- 用户姓名：张三\n- 用户身份：Jarvis Lite 项目创建者\n"

        identity = find_identity(content)

        self.assertEqual(identity, "你是张三，Jarvis Lite 项目创建者。")

    def test_identity_question_about_relationship_is_not_saved_as_role(self):
        self.assertTrue(is_identity_question("我是你的什么人，你知道吗"))
        self.assertEqual(parse_identity_fact("我是你的什么人，你知道吗"), "")


if __name__ == "__main__":
    unittest.main()
