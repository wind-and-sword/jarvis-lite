import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.conversation import ConversationSession


class ConversationSessionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name))
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 用户偏好：中文简洁回答\n",
            encoding="utf-8",
        )
        self.session = ConversationSession(self.paths)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_session_records_user_and_assistant_turns(self):
        response = self.session.handle("你好")

        self.assertIn("Jarvis Lite", response)
        self.assertEqual(len(self.session.turns), 1)
        self.assertEqual(self.session.turns[0].user, "你好")
        self.assertIn("用户偏好：中文简洁回答", self.session.turns[0].assistant)

    def test_history_command_outputs_recorded_turns_without_recording_itself(self):
        self.session.handle("你好")

        history = self.session.handle("/history")

        self.assertIn("用户：你好", history)
        self.assertIn("助手：", history)
        self.assertEqual(len(self.session.turns), 1)

    def test_save_summary_writes_conversation_markdown_to_word_dir(self):
        self.session.handle("你好")

        response = self.session.handle("/save-summary today")

        summary_file = self.paths.word_dir / "today.md"
        self.assertIn("已写入会话总结", response)
        self.assertTrue(summary_file.is_file())
        content = summary_file.read_text(encoding="utf-8")
        self.assertIn("# today", content)
        self.assertIn("用户：你好", content)
        self.assertIn("助手：", content)

    def test_save_summary_requires_existing_turns(self):
        response = self.session.handle("/save-summary empty")

        self.assertIn("当前会话还没有可总结的内容", response)
        self.assertFalse((self.paths.word_dir / "empty.md").exists())

    def test_clear_command_removes_session_history(self):
        self.session.handle("你好")

        response = self.session.handle("/clear")

        self.assertIn("已清空当前会话", response)
        self.assertEqual(self.session.turns, [])


if __name__ == "__main__":
    unittest.main()
