import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.messaging_workflow import (
    describe_message_prepare,
    describe_messaging_focus,
    describe_messaging_open,
    describe_messaging_workflow_status,
    open_messaging_app,
    parse_message_prepare_request,
)
from jarvis_lite.window_state import NativeWindow, build_window_snapshot


class MessagingWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")
        self.qq_path = self.paths.root / "tools" / "QQ.exe"
        self.wechat_path = self.paths.root / "tools" / "WeChat.exe"
        self.qq_path.parent.mkdir(parents=True)
        self.qq_path.write_text("fake qq", encoding="utf-8")
        self.wechat_path.write_text("fake wechat", encoding="utf-8")
        (self.paths.config_dir / "apps.local.json").write_text(
            json.dumps(
                {
                    "apps": {
                        "qq": {"path": str(self.qq_path), "aliases": ["工作QQ"]},
                        "wechat": {"path": str(self.wechat_path), "aliases": ["工作微信"]},
                    }
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_describe_messaging_workflow_status_reports_first_stage_boundary(self):
        response = describe_messaging_workflow_status(self.paths)

        self.assertIn("QQ/微信准备式工作流状态：第一阶段", response)
        self.assertIn("/qq-open", response)
        self.assertIn("/wechat-prepare-message 联系人 => 消息", response)
        self.assertIn("不查找真实联系人、不点击、不输入、不发送消息", response)
        self.assertIn(str(self.qq_path.resolve()), response)
        self.assertIn(str(self.wechat_path.resolve()), response)

    def test_open_messaging_app_uses_configured_path_and_injected_executor(self):
        calls = []

        result = open_messaging_app(self.paths, "qq", executor=lambda path: calls.append(path))

        self.assertEqual(result.app.app_id, "qq")
        self.assertEqual(result.alias, "qq")
        self.assertEqual(result.path, self.qq_path.resolve())
        self.assertEqual(calls, [self.qq_path.resolve()])

    def test_describe_messaging_open_reports_scope_without_message_actions(self):
        response = describe_messaging_open(self.paths, "wechat", executor=lambda path: None)

        self.assertIn("微信打开执行：微信 (wechat)", response)
        self.assertIn("不查找联系人、不点击、不输入、不发送消息", response)

    def test_open_messaging_app_reports_missing_path(self):
        empty_root = self.paths.root / "empty-program-files"
        empty_root.mkdir()
        (self.paths.config_dir / "apps.local.json").unlink()

        with patch.dict(
            os.environ,
            {
                "ProgramFiles": str(empty_root),
                "ProgramFiles(x86)": str(empty_root),
                "LOCALAPPDATA": str(empty_root),
                "APPDATA": str(empty_root),
            },
        ):
            with self.assertRaisesRegex(FileNotFoundError, "微信启动路径未找到"):
                open_messaging_app(self.paths, "wechat", executor=lambda path: None)

    def test_describe_messaging_focus_uses_existing_window_and_injected_executor(self):
        calls = []
        snapshot = build_window_snapshot(
            self.paths,
            (NativeWindow(handle=300, title="微信", process_id=30, process_name="WeChat.exe"),),
            foreground_handle=None,
            platform_name="Windows",
        )

        response = describe_messaging_focus(
            self.paths,
            "wechat",
            snapshot=snapshot,
            executor=lambda handle: calls.append(handle),
        )

        self.assertIn("微信聚焦执行", response)
        self.assertIn("窗口切换执行：微信", response)
        self.assertIn("不点击、不输入、不发送消息", response)
        self.assertEqual(calls, [300])

    def test_describe_messaging_focus_guides_open_when_window_missing(self):
        snapshot = build_window_snapshot(self.paths, (), foreground_handle=None, platform_name="Windows")

        with self.assertRaisesRegex(ValueError, "/qq-open"):
            describe_messaging_focus(self.paths, "qq", snapshot=snapshot, executor=lambda handle: None)

    def test_parse_message_prepare_request_requires_contact_and_message(self):
        draft = parse_message_prepare_request("张三 => 明天十点开会")

        self.assertEqual(draft.contact, "张三")
        self.assertEqual(draft.message, "明天十点开会")

        with self.assertRaisesRegex(ValueError, "用法"):
            parse_message_prepare_request("张三 明天十点开会")
        with self.assertRaisesRegex(ValueError, "联系人不能为空"):
            parse_message_prepare_request("=> 明天十点开会")
        with self.assertRaisesRegex(ValueError, "消息内容不能为空"):
            parse_message_prepare_request("张三 => ")

    def test_describe_message_prepare_returns_unsent_draft(self):
        response = describe_message_prepare("qq", "张三 => 明天十点开会")

        self.assertIn("QQ 消息准备单：", response)
        self.assertIn("联系人：张三", response)
        self.assertIn("消息：明天十点开会", response)
        self.assertIn("状态：未发送", response)
        self.assertIn("不查找真实联系人、不点击、不输入、不发送消息", response)


if __name__ == "__main__":
    unittest.main()
