import sys
import json
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
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")
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

    def test_send_routes_greeting_through_local_natural_language_brain(self):
        response = self.bridge.send("早上好")

        self.assertEqual(response.state, DesktopState.SUCCESS)
        self.assertEqual(response.user_input, "早上好")
        self.assertIn("Jarvis Lite", response.assistant_text)
        self.assertNotIn("已读取长期记忆", response.assistant_text)

    def test_send_marks_unknown_command_as_error(self):
        response = self.bridge.send("/not-found")

        self.assertEqual(response.state, DesktopState.ERROR)
        self.assertIn("未知命令：/not-found", response.assistant_text)

    def test_send_sensitive_executes_real_command_but_records_redacted_input(self):
        secret = "secret-desktop-llm-key"
        response = self.bridge.send_sensitive(
            (
                "/llm-config-set provider=qwen model=qwen-plus "
                "base_url=https://qwen.example/v1/responses "
                f"api_key={secret}"
            ),
            "写入外脑配置（api_key 已隐藏）",
        )
        payload = json.loads((self.paths.config_dir / "llm.local.json").read_text(encoding="utf-8"))
        history = self.bridge.session.handle("/history")
        log_text = self.paths.log_path.read_text(encoding="utf-8")

        self.assertEqual(response.state, DesktopState.SUCCESS)
        self.assertEqual(response.user_input, "写入外脑配置（api_key 已隐藏）")
        self.assertEqual(payload["api_key"], secret)
        self.assertIn("用户：写入外脑配置（api_key 已隐藏）", history)
        self.assertNotIn(secret, history)
        self.assertNotIn(secret, log_text)

    def test_send_exposes_llm_pending_status_after_clarification(self):
        self.paths.config_dir.mkdir(parents=True, exist_ok=True)
        (self.paths.config_dir / "llm.local.json").write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_response": {
                        "type": "clarify",
                        "clarification": "你想看知识库还是最近文件？",
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        bridge = DesktopBridge(self.paths)

        response = bridge.send("帮我判断下一步")

        self.assertIn("LLM 外脑需要补充信息：你想看知识库还是最近文件？", response.assistant_text)
        self.assertIn("外脑待补充（1/3）：你想看知识库还是最近文件？", response.llm_pending_status_text)
        self.assertIn("回复缺失信息继续，或输入“取消补充”。", response.llm_pending_status_text)
        self.assertEqual(response.llm_pending_status_text, bridge.llm_pending_status_text())

    def test_send_exposes_llm_activity_status_after_answer(self):
        self.paths.config_dir.mkdir(parents=True, exist_ok=True)
        (self.paths.config_dir / "llm.local.json").write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_response": {
                        "type": "answer",
                        "answer": "外脑处理开放问题",
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        bridge = DesktopBridge(self.paths)

        response = bridge.send("帮我判断下一步")

        self.assertIn("LLM 外脑：外脑处理开放问题", response.assistant_text)
        self.assertIn("外脑运行状态：已启用", response.llm_activity_status_text)
        self.assertIn("最近调用：fallback / answer", response.llm_activity_status_text)
        self.assertIn("结果：外脑处理开放问题", response.llm_activity_status_text)
        self.assertEqual(response.llm_activity_status_text, bridge.llm_activity_status_text())

    def test_send_exposes_route_status_for_inner_brain_reply(self):
        response = self.bridge.send("早上好")

        self.assertIn("Jarvis Lite", response.assistant_text)
        self.assertIn("最近路由：inner-brain / assistant.greeting", response.route_status_text)
        self.assertIn("依据：", response.route_status_text)
        self.assertIn("source=seed_sample", response.route_status_text)
        self.assertEqual(response.route_status_text, self.bridge.route_status_text())

    def test_quick_commands_include_current_assistant_capabilities(self):
        commands = quick_commands()
        prompts = tuple(command.prompt for command in commands)

        self.assertIn("/status", prompts)
        self.assertIn("/kb", prompts)
        self.assertIn("/kb-summary", prompts)
        self.assertIn("/dirs", prompts)
        self.assertIn("查看最近上下文", prompts)
        self.assertIn("/recent-files", prompts)
        self.assertIn("/tag-history", prompts)
        self.assertIn("/daily-report", prompts)
        self.assertIn("/update-status", prompts)
        self.assertIn("/update-download", prompts)
        self.assertIn("/organize-preview", prompts)

    def test_direct_quick_commands_exclude_commands_that_need_arguments(self):
        commands = direct_quick_commands()
        labels = tuple(command.label for command in commands)
        prompts = tuple(command.prompt for command in commands)

        self.assertEqual(
            labels,
            (
                "状态",
                "知识库",
                "知识库摘要",
                "常用目录",
                "最近上下文",
                "最近文件",
                "标签历史",
                "生成日报",
                "检查更新",
                "下载更新",
            ),
        )
        self.assertIn("/kb-summary", prompts)
        self.assertIn("查看最近上下文", prompts)
        self.assertIn("/recent-files", prompts)
        self.assertIn("/tag-history", prompts)
        self.assertNotIn("/organize-preview", prompts)
        self.assertIn("/update-status", prompts)
        self.assertIn("/update-download", prompts)


if __name__ == "__main__":
    unittest.main()
