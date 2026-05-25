import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.desktop.bridge import DesktopBridge, direct_quick_commands, quick_commands
from jarvis_lite.desktop.state import DesktopState


class DesktopBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name))
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 用户偏好：中文回答\n",
            encoding="utf-8",
        )
        self.bridge = DesktopBridge(self.paths)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_send_returns_desktop_response_from_conversation_session(self):
        response = self.bridge.send("/memory")

        self.assertEqual(response.state, DesktopState.SUCCESS)
        self.assertEqual(response.user_input, "/memory")
        self.assertIn("用户偏好：中文回答", response.assistant_text)
        self.assertEqual(response.turn_count, 1)

    def test_send_marks_unknown_command_as_error(self):
        response = self.bridge.send("/not-found")

        self.assertEqual(response.state, DesktopState.ERROR)
        self.assertIn("未知命令：/not-found", response.assistant_text)

    def test_quick_commands_include_current_assistant_capabilities(self):
        commands = quick_commands()
        prompts = tuple(command.prompt for command in commands)

        self.assertIn("/status", prompts)
        self.assertIn("/kb", prompts)
        self.assertIn("/kb-summary", prompts)
        self.assertIn("/dirs", prompts)
        self.assertIn("查看最近上下文", prompts)
        self.assertIn("/recent-files", prompts)
        self.assertIn("/daily-report", prompts)
        self.assertIn("/update-status", prompts)
        self.assertIn("/update-download", prompts)
        self.assertIn("/organize-preview", prompts)

    def test_direct_quick_commands_exclude_commands_that_need_arguments(self):
        commands = direct_quick_commands()
        labels = tuple(command.label for command in commands)
        prompts = tuple(command.prompt for command in commands)

        self.assertEqual(labels, ("状态", "知识库", "知识库摘要", "常用目录", "最近上下文", "最近文件", "生成日报", "检查更新", "下载更新"))
        self.assertIn("/kb-summary", prompts)
        self.assertIn("查看最近上下文", prompts)
        self.assertIn("/recent-files", prompts)
        self.assertNotIn("/organize-preview", prompts)
        self.assertIn("/update-status", prompts)
        self.assertIn("/update-download", prompts)


if __name__ == "__main__":
    unittest.main()
