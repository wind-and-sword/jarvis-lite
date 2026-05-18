import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name))
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 用户偏好：中文简洁回答\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "note.txt").write_text("资料内容", encoding="utf-8")
        self.agent = JarvisAgent(self.paths)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_memory_command_returns_profile_content(self):
        response = self.agent.handle("/memory")

        self.assertIn("用户偏好：中文简洁回答", response)

    def test_list_command_uses_data_tool(self):
        response = self.agent.handle("/list")

        self.assertIn("note.txt", response)
        self.assertIn("list_data", (self.paths.logs_dir / "jarvis.log").read_text(encoding="utf-8"))

    def test_plain_message_mentions_loaded_memory_summary(self):
        response = self.agent.handle("你好")

        self.assertIn("Jarvis Lite", response)
        self.assertIn("用户偏好：中文简洁回答", response)

    def test_plain_message_does_not_duplicate_punctuation(self):
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 项目目标：本地助手。\n",
            encoding="utf-8",
        )

        response = self.agent.handle("你好")

        self.assertNotIn("。。", response)

    def test_plain_question_uses_matching_data_document(self):
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 推荐使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )

        response = self.agent.handle("Jarvis Lite 推荐使用什么 Python 版本？")

        self.assertIn("根据 data/runtime.md:1", response)
        self.assertIn("Python 3.13", response)

    def test_ask_command_reports_no_match(self):
        response = self.agent.handle("/ask 今天晚饭吃什么？")

        self.assertIn("没有在 data 目录找到", response)

    def test_ask_command_returns_multiple_data_sources(self):
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/ask Jarvis Lite 使用什么？")

        self.assertIn("data/memory.md:1", response)
        self.assertIn("data/runtime.md:1", response)


if __name__ == "__main__":
    unittest.main()
