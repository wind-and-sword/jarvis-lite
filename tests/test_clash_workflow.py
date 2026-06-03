import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.clash_workflow import (
    describe_clash_focus,
    describe_clash_open,
    describe_clash_workflow_status,
    open_clash_verge,
)
from jarvis_lite.config import build_project_paths
from jarvis_lite.window_state import NativeWindow, build_window_snapshot


class ClashWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")
        self.clash_path = self.paths.root / "tools" / "Clash Verge.exe"
        self.clash_path.parent.mkdir(parents=True)
        self.clash_path.write_text("fake clash", encoding="utf-8")
        (self.paths.config_dir / "apps.local.json").write_text(
            json.dumps(
                {
                    "apps": {
                        "clash_verge": {
                            "path": str(self.clash_path),
                            "aliases": ["我的代理面板"],
                        }
                    }
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_describe_clash_workflow_status_reports_first_stage_boundary(self):
        response = describe_clash_workflow_status(self.paths)

        self.assertIn("Clash Verge 工作流状态：第一阶段", response)
        self.assertIn("/clash-open", response)
        self.assertIn("/clash-focus", response)
        self.assertIn("不切换节点", response)
        self.assertIn(str(self.clash_path.resolve()), response)

    def test_open_clash_verge_uses_configured_path_and_injected_executor(self):
        calls = []

        result = open_clash_verge(self.paths, executor=lambda path: calls.append(path))

        self.assertEqual(result.app.app_id, "clash_verge")
        self.assertEqual(result.alias, "clash_verge")
        self.assertEqual(result.path, self.clash_path.resolve())
        self.assertEqual(calls, [self.clash_path.resolve()])

    def test_describe_clash_open_reports_scope_without_proxy_changes(self):
        response = describe_clash_open(self.paths, executor=lambda path: None)

        self.assertIn("Clash Verge 打开代理面板执行", response)
        self.assertIn("不切换节点、不开关系统代理、不修改配置", response)

    def test_open_clash_verge_reports_missing_path(self):
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
            with self.assertRaisesRegex(FileNotFoundError, "Clash Verge 启动路径未找到"):
                open_clash_verge(self.paths, executor=lambda path: None)

    def test_describe_clash_focus_uses_existing_window_and_injected_executor(self):
        calls = []
        snapshot = build_window_snapshot(
            self.paths,
            (NativeWindow(handle=200, title="代理面板", process_id=20, process_name="Clash Verge.exe"),),
            foreground_handle=None,
            platform_name="Windows",
        )

        response = describe_clash_focus(self.paths, snapshot=snapshot, executor=lambda handle: calls.append(handle))

        self.assertIn("Clash Verge 聚焦执行", response)
        self.assertIn("窗口切换执行：代理面板", response)
        self.assertIn("不点击、不输入、不切换节点、不修改系统代理", response)
        self.assertEqual(calls, [200])

    def test_describe_clash_focus_guides_open_when_window_missing(self):
        snapshot = build_window_snapshot(self.paths, (), foreground_handle=None, platform_name="Windows")

        with self.assertRaisesRegex(ValueError, "/clash-open"):
            describe_clash_focus(self.paths, snapshot=snapshot, executor=lambda handle: None)


if __name__ == "__main__":
    unittest.main()
