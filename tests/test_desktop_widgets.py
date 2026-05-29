import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "minimal")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from jarvis_lite.config import build_project_paths
from jarvis_lite.desktop.bridge import DesktopBridge
from jarvis_lite.desktop.settings import (
    DesktopSettings,
    desktop_settings_path,
    load_desktop_settings,
    save_desktop_settings,
)
from jarvis_lite.desktop.state import DesktopState
from jarvis_lite.desktop.widgets import AssistantPanel, DesktopPetWindow


class DesktopWidgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv[:1])

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "jarvis-lite"
        self.paths = build_project_paths(self.project_root)
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 用户偏好：中文回答\n",
            encoding="utf-8",
        )
        self.bridge = DesktopBridge(self.paths)
        self.panel = AssistantPanel(self.bridge)
        self.pet = DesktopPetWindow(self.panel, self.paths)

    def tearDown(self):
        self.panel.close()
        self.pet.close()
        self.temp_dir.cleanup()

    def test_pet_window_starts_floating_and_keeps_panel_hidden(self):
        flags = self.pet.windowFlags()

        self.assertFalse(self.panel.isVisible())
        self.assertTrue(bool(flags & Qt.WindowType.WindowStaysOnTopHint))
        self.assertTrue(bool(flags & Qt.WindowType.FramelessWindowHint))
        self.assertEqual(self.pet.objectName(), "desktopPetWindow")

    def test_pet_window_toggles_panel_visibility(self):
        self.pet.toggle_panel()
        QApplication.processEvents()

        self.assertTrue(self.panel.isVisible())

        self.pet.toggle_panel()
        QApplication.processEvents()

        self.assertFalse(self.panel.isVisible())

    def test_panel_can_send_text_through_desktop_bridge(self):
        self.panel.submit_text("/memory")

        self.assertIn("用户：/memory", self.panel.transcript_text())
        self.assertIn("用户偏好：中文回答", self.panel.transcript_text())
        self.assertIn("状态：success", self.panel.status_text())
        self.assertEqual(self.panel.llm_pending_status_text(), "外脑待补充：无")
        self.assertIn("最近调用：无", self.panel.llm_activity_status_text())
        self.assertIn("最近路由：command / /memory", self.panel.route_status_text())

    def test_panel_shows_llm_pending_status_and_refreshes_after_cancel(self):
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
        self.panel.close()
        self.pet.close()
        self.bridge = DesktopBridge(self.paths)
        self.panel = AssistantPanel(self.bridge)
        self.pet = DesktopPetWindow(self.panel, self.paths)

        self.panel.submit_text("帮我判断下一步")
        pending_text = self.panel.llm_pending_status_text()

        self.assertIn("外脑待补充（1/3）：你想看知识库还是最近文件？", pending_text)
        self.assertIn("回复缺失信息继续，或输入“取消补充”。", pending_text)

        self.panel.submit_text("取消补充")

        self.assertEqual(self.panel.llm_pending_status_text(), "外脑待补充：无")

    def test_panel_restores_persisted_llm_pending_status_on_startup(self):
        self.paths.config_dir.mkdir(parents=True, exist_ok=True)
        (self.paths.config_dir / "llm.local.json").write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_response": {
                        "type": "clarify",
                        "clarification": "需要哪个时间范围？",
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        self.bridge = DesktopBridge(self.paths)
        self.bridge.send("帮我判断下一步")
        self.panel.close()
        self.pet.close()

        self.bridge = DesktopBridge(self.paths)
        self.panel = AssistantPanel(self.bridge)
        self.pet = DesktopPetWindow(self.panel, self.paths)

        self.assertIn("外脑待补充（1/3）：需要哪个时间范围？", self.panel.llm_pending_status_text())

    def test_panel_shows_llm_activity_status_after_answer(self):
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
        self.panel.close()
        self.pet.close()
        self.bridge = DesktopBridge(self.paths)
        self.panel = AssistantPanel(self.bridge)
        self.pet = DesktopPetWindow(self.panel, self.paths)

        self.panel.submit_text("帮我判断下一步")
        activity_text = self.panel.llm_activity_status_text()

        self.assertIn("外脑运行状态：已启用", activity_text)
        self.assertIn("最近调用：fallback / answer", activity_text)
        self.assertIn("结果：外脑处理开放问题", activity_text)

    def test_panel_shows_route_status_after_inner_brain_reply(self):
        self.panel.submit_text("早上好")

        route_text = self.panel.route_status_text()

        self.assertIn("最近路由：inner-brain / assistant.greeting", route_text)
        self.assertIn("输入：早上好", route_text)

    def test_panel_exposes_only_direct_quick_command_buttons(self):
        self.assertEqual(
            self.panel.quick_command_texts(),
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

    def test_panel_quick_command_button_submits_prompt(self):
        self.panel.quick_command_button("知识库").click()
        QApplication.processEvents()

        self.assertIn("用户：/kb", self.panel.transcript_text())
        self.assertIn("Jarvis：", self.panel.transcript_text())
        self.assertIn("状态：success", self.panel.status_text())

    def test_panel_recent_context_quick_command_submits_natural_language_prompt(self):
        self.panel.quick_command_button("最近上下文").click()
        QApplication.processEvents()

        self.assertIn("用户：查看最近上下文", self.panel.transcript_text())
        self.assertIn("最近上下文", self.panel.transcript_text())
        self.assertIn("状态：success", self.panel.status_text())

    def test_panel_tag_history_quick_command_submits_tag_history_command(self):
        self.panel.quick_command_button("标签历史").click()
        QApplication.processEvents()

        self.assertIn("用户：/tag-history", self.panel.transcript_text())
        self.assertIn("批量打标签历史：还没有记录。", self.panel.transcript_text())
        self.assertIn("状态：success", self.panel.status_text())

    def test_panel_tracks_last_result_after_submission(self):
        self.panel.submit_text("/memory")

        self.assertIn("用户：/memory", self.panel.last_result_text())
        self.assertIn("Jarvis：", self.panel.last_result_text())
        self.assertIn("用户偏好：中文回答", self.panel.last_result_text())

    def test_pet_caption_tracks_panel_state(self):
        self.pet.toggle_panel()
        self.panel.submit_text("/not-found")

        self.assertEqual(self.pet.caption_text(), "错误")
        self.assertEqual(self.pet.current_asset_name(), "error.svg")

        self.panel.submit_text("/memory")

        self.assertEqual(self.pet.caption_text(), "完成")
        self.assertEqual(self.pet.current_asset_name(), "success.svg")

    def test_pet_window_starts_with_idle_asset(self):
        self.assertEqual(self.pet.current_asset_name(), "idle.svg")

        self.pet.set_state(DesktopState.WORKING)

        self.assertEqual(self.pet.current_asset_name(), "working.svg")

    def test_pet_window_uses_state_animation_profile(self):
        self.assertEqual(self.pet.current_animation_name(), "idle-breathing")
        self.assertEqual(self.pet.animation_interval_ms(), 1200)

        self.pet.set_state(DesktopState.THINKING)

        self.assertEqual(self.pet.current_animation_name(), "thinking-pulse")
        self.assertEqual(self.pet.animation_interval_ms(), 360)

    def test_pet_window_advances_animation_frame_without_changing_asset(self):
        self.pet.set_state(DesktopState.WORKING)
        first_frame = self.pet.animation_frame()

        self.pet.advance_animation_frame()

        self.assertNotEqual(self.pet.animation_frame(), first_frame)
        self.assertEqual(self.pet.current_asset_name(), "working.svg")

    def test_pet_window_persists_position_to_runtime_directory(self):
        self.pet.move(240, 180)
        self.pet.persist_position()

        settings = load_desktop_settings(self.paths)
        self.assertEqual(settings.position_x, 240)
        self.assertEqual(settings.position_y, 180)
        self.assertEqual(desktop_settings_path(self.paths).parent, self.project_root.parent / "jarvis-lite-runtime")

    def test_pet_window_restores_desktop_preferences_on_startup(self):
        self.panel.close()
        self.pet.close()
        save_desktop_settings(
            self.paths,
            DesktopSettings(
                position_x=120,
                position_y=90,
                always_on_top=False,
                opacity_percent=74,
                pet_size=184,
                theme_name="daylight",
            ),
        )

        self.panel = AssistantPanel(self.bridge)
        self.pet = DesktopPetWindow(self.panel, self.paths)

        self.assertFalse(self.pet.is_always_on_top())
        self.assertEqual(self.pet.current_opacity_percent(), 74)
        self.assertEqual(self.pet.current_pet_size(), 184)
        self.assertEqual(self.pet.current_theme_name(), "daylight")
        self.assertEqual(self.pet.width(), 184)

    def test_pet_window_applies_and_persists_desktop_preferences(self):
        save_desktop_settings(
            self.paths,
            DesktopSettings(panel_width=560, panel_height=700),
        )

        self.pet.apply_preferences(always_on_top=False, opacity_percent=82, pet_size=176)

        settings = load_desktop_settings(self.paths)
        self.assertFalse(self.pet.is_always_on_top())
        self.assertEqual(self.pet.current_opacity_percent(), 82)
        self.assertEqual(self.pet.current_pet_size(), 176)
        self.assertEqual(settings.position_x, self.pet.x())
        self.assertEqual(settings.position_y, self.pet.y())
        self.assertFalse(settings.always_on_top)
        self.assertEqual(settings.opacity_percent, 82)
        self.assertEqual(settings.pet_size, 176)
        self.assertEqual(settings.theme_name, "midnight")
        self.assertEqual(settings.panel_width, 560)
        self.assertEqual(settings.panel_height, 700)

    def test_pet_window_applies_and_persists_theme_preference(self):
        self.pet.apply_preferences(always_on_top=True, opacity_percent=90, pet_size=168, theme_name="daylight")

        settings = load_desktop_settings(self.paths)
        self.assertEqual(settings.theme_name, "daylight")
        self.assertEqual(self.pet.current_theme_name(), "daylight")
        self.assertIn("#ecfeff", self.pet.styleSheet())

    def test_panel_exposes_desktop_settings_controls(self):
        panel = AssistantPanel(
            self.bridge,
            DesktopSettings(always_on_top=False, opacity_percent=70, pet_size=180, launch_at_login=True, theme_name="daylight"),
        )
        self.addCleanup(panel.close)

        settings = panel.settings_values()

        self.assertFalse(settings.always_on_top)
        self.assertEqual(settings.opacity_percent, 70)
        self.assertEqual(settings.pet_size, 180)
        self.assertTrue(settings.launch_at_login)
        self.assertEqual(settings.theme_name, "daylight")
        self.assertIn("#f8fafc", panel.styleSheet())

    def test_panel_exposes_provider_config_controls(self):
        values = self.panel.provider_config_values()

        self.assertEqual(values["llm"]["provider"], "openai-compatible")
        self.assertEqual(values["llm"]["model"], "")
        self.assertEqual(values["llm"]["base_url"], "")
        self.assertEqual(values["llm"]["api_key"], "")
        self.assertEqual(values["search"]["provider"], "tavily")
        self.assertEqual(values["search"]["base_url"], "")
        self.assertEqual(values["search"]["api_key"], "")
        self.assertEqual(values["search"]["max_results"], 5)

    def test_panel_writes_llm_config_without_showing_api_key_in_transcript_or_history(self):
        secret = "secret-desktop-llm-key"
        self.panel.change_llm_provider_config(
            provider="qwen",
            model="qwen-plus",
            base_url="https://qwen.example/v1/responses",
            api_key=secret,
        )

        response = self.panel.write_llm_provider_config()
        payload = json.loads((self.paths.config_dir / "llm.local.json").read_text(encoding="utf-8"))
        transcript = self.panel.transcript_text()
        history = self.bridge.session.handle("/history")
        log_text = self.paths.log_path.read_text(encoding="utf-8")

        self.assertEqual(response.state, DesktopState.SUCCESS)
        self.assertEqual(payload["provider"], "qwen")
        self.assertEqual(payload["model"], "qwen-plus")
        self.assertEqual(payload["base_url"], "https://qwen.example/v1/responses")
        self.assertEqual(payload["api_key"], secret)
        self.assertIn("用户：写入外脑配置（api_key 已隐藏）", transcript)
        self.assertIn("已写入外脑本地配置：config/llm.local.json", transcript)
        self.assertNotIn(secret, transcript)
        self.assertNotIn(secret, history)
        self.assertNotIn(secret, log_text)

    def test_panel_writes_search_config_without_showing_api_key_in_transcript_or_history(self):
        secret = "secret-desktop-search-key"
        self.panel.change_search_provider_config(
            provider="tavily",
            api_key=secret,
            base_url="https://search.example/api",
            max_results=3,
        )

        response = self.panel.write_search_provider_config()
        payload = json.loads((self.paths.config_dir / "search.local.json").read_text(encoding="utf-8"))
        transcript = self.panel.transcript_text()
        history = self.bridge.session.handle("/history")
        log_text = self.paths.log_path.read_text(encoding="utf-8")

        self.assertEqual(response.state, DesktopState.SUCCESS)
        self.assertEqual(payload["provider"], "tavily")
        self.assertEqual(payload["api_key"], secret)
        self.assertEqual(payload["base_url"], "https://search.example/api")
        self.assertEqual(payload["max_results"], 3)
        self.assertIn("用户：写入联网搜索配置（api_key 已隐藏）", transcript)
        self.assertIn("已写入联网搜索本地配置：config/search.local.json", transcript)
        self.assertNotIn(secret, transcript)
        self.assertNotIn(secret, history)
        self.assertNotIn(secret, log_text)

    def test_panel_config_check_and_smoke_buttons_submit_existing_commands(self):
        (self.paths.config_dir / "llm.local.json").write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_response": "{\"type\":\"answer\",\"answer\":\"桌面外脑 smoke 正常\"}",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (self.paths.config_dir / "search.local.json").write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_results": [
                        {
                            "title": "Python current release",
                            "url": "https://python.example/release",
                            "snippet": "桌面搜索 smoke 正常",
                        }
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        self.panel.check_llm_provider_config()
        self.panel.smoke_llm_provider()
        self.panel.check_search_provider_config()
        self.panel.smoke_search_provider()
        transcript = self.panel.transcript_text()

        self.assertIn("用户：/llm-config-check", transcript)
        self.assertIn("外脑配置检查：", transcript)
        self.assertIn("用户：/llm-smoke 请用一句话确认连接可用", transcript)
        self.assertIn("回答：桌面外脑 smoke 正常", transcript)
        self.assertIn("用户：/search-config-check", transcript)
        self.assertIn("联网搜索配置检查：", transcript)
        self.assertIn("用户：/search-smoke Python 版本", transcript)
        self.assertIn("Python current release", transcript)

    def test_panel_restores_saved_panel_size(self):
        panel = AssistantPanel(
            self.bridge,
            DesktopSettings(panel_width=560, panel_height=700),
        )
        self.addCleanup(panel.close)

        self.assertEqual(panel.width(), 560)
        self.assertEqual(panel.height(), 700)
        self.assertEqual(panel.settings_values().panel_width, 560)
        self.assertEqual(panel.settings_values().panel_height, 700)

    def test_panel_resize_persists_panel_size_to_runtime_settings(self):
        self.panel.show()
        QApplication.processEvents()

        self.panel.resize(560, 700)
        QApplication.processEvents()

        settings = load_desktop_settings(self.paths)
        self.assertEqual(settings.panel_width, 560)
        self.assertEqual(settings.panel_height, 700)

    def test_panel_settings_change_notifies_listener(self):
        changes = []
        self.panel.set_settings_listener(changes.append)

        self.panel.change_settings(always_on_top=False, opacity_percent=78, pet_size=172, launch_at_login=True, theme_name="daylight")

        self.assertEqual(len(changes), 1)
        self.assertFalse(changes[0].always_on_top)
        self.assertEqual(changes[0].opacity_percent, 78)
        self.assertEqual(changes[0].pet_size, 172)
        self.assertTrue(changes[0].launch_at_login)
        self.assertEqual(changes[0].theme_name, "daylight")


if __name__ == "__main__":
    unittest.main()
