import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.authorization import (
    authorize_intent_execution,
    describe_authorization_status,
    is_desktop_action_command,
)


class AuthorizationTests(unittest.TestCase):
    def test_desktop_action_command_detection_uses_command_name(self):
        self.assertTrue(is_desktop_action_command("/hotkey ctrl+l"))
        self.assertTrue(is_desktop_action_command("/mouse-click 100 200"))
        self.assertTrue(is_desktop_action_command("/type-text Hello Jarvis"))
        self.assertTrue(is_desktop_action_command("/window-focus Chrome"))
        self.assertTrue(is_desktop_action_command("/app-launch Chrome"))
        self.assertTrue(is_desktop_action_command("/chrome-open https://example.com"))
        self.assertTrue(is_desktop_action_command("/chrome-search Jarvis Lite"))
        self.assertTrue(is_desktop_action_command("/clash-open"))
        self.assertTrue(is_desktop_action_command("/clash-focus"))
        self.assertTrue(is_desktop_action_command("/qq-open"))
        self.assertTrue(is_desktop_action_command("/qq-focus"))
        self.assertTrue(is_desktop_action_command("/wechat-open"))
        self.assertTrue(is_desktop_action_command("/wechat-focus"))
        self.assertFalse(is_desktop_action_command("/qq-prepare-message 张三 => 你好"))
        self.assertFalse(is_desktop_action_command("/kb-summary"))
        self.assertFalse(is_desktop_action_command("hotkey ctrl+l"))

    def test_explicit_desktop_command_can_execute_directly(self):
        decision = authorize_intent_execution(
            intent_name="desktop.hotkey",
            command="/hotkey ctrl+l",
            source="explicit_command",
            confidence=1.0,
        )

        self.assertEqual(decision.action, "direct_execute")
        self.assertFalse(decision.requires_confirmation)
        self.assertIn("显式命令", decision.reason)

    def test_natural_language_desktop_action_prepares_confirmation(self):
        decision = authorize_intent_execution(
            intent_name="desktop.hotkey",
            command="/hotkey ctrl+l",
            source="natural_language",
            confidence=0.96,
        )

        self.assertEqual(decision.action, "prepare_confirmation")
        self.assertTrue(decision.requires_confirmation)
        self.assertIn("桌面动作", decision.reason)
        self.assertIn("确认执行", decision.next_step)

    def test_confirmed_advice_desktop_action_can_execute(self):
        decision = authorize_intent_execution(
            intent_name="desktop.hotkey",
            command="/hotkey ctrl+l",
            source="advice_confirmation",
            confirmed=True,
            confidence=1.0,
        )

        self.assertEqual(decision.action, "direct_execute")
        self.assertFalse(decision.requires_confirmation)
        self.assertIn("已确认", decision.reason)

    def test_missing_slots_ask_for_clarification_before_action_risk(self):
        decision = authorize_intent_execution(
            intent_name="desktop.apps.launch",
            command="/app-launch",
            source="natural_language",
            confidence=0.95,
            missing=("app",),
        )

        self.assertEqual(decision.action, "clarify")
        self.assertTrue(decision.requires_clarification)
        self.assertIn("缺少槽位", decision.reason)
        self.assertIn("app", decision.next_step)

    def test_llm_desktop_action_is_downgraded_without_execution(self):
        decision = authorize_intent_execution(
            intent_name="desktop.hotkey",
            command="/hotkey ctrl+l",
            source="llm",
            confidence=0.91,
        )

        self.assertEqual(decision.action, "downgrade")
        self.assertFalse(decision.requires_confirmation)
        self.assertIn("LLM 外脑", decision.reason)
        self.assertIn("显式输入", decision.next_step)

    def test_low_risk_natural_language_command_can_execute_directly(self):
        decision = authorize_intent_execution(
            intent_name="knowledge.summary",
            command="/kb-summary",
            source="natural_language",
            confidence=0.94,
        )

        self.assertEqual(decision.action, "direct_execute")
        self.assertFalse(decision.requires_confirmation)
        self.assertIn("低风险", decision.reason)

    def test_low_confidence_requires_clarification(self):
        decision = authorize_intent_execution(
            intent_name="knowledge.summary",
            command="/kb-summary",
            source="natural_language",
            confidence=0.51,
        )

        self.assertEqual(decision.action, "clarify")
        self.assertTrue(decision.requires_clarification)
        self.assertIn("置信度", decision.reason)

    def test_authorization_status_describes_first_stage_policy(self):
        status = describe_authorization_status()

        self.assertIn("意图授权层状态", status)
        self.assertIn("直接执行", status)
        self.assertIn("准备后确认", status)
        self.assertIn("追问补充", status)
        self.assertIn("降级", status)
        self.assertIn("/hotkey", status)
        self.assertIn("/app-launch", status)
        self.assertIn("/chrome-open", status)
        self.assertIn("/clash-open", status)
        self.assertIn("/qq-open", status)
        self.assertIn("/wechat-open", status)


if __name__ == "__main__":
    unittest.main()
