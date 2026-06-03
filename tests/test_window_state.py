import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.window_state import (
    NativeWindow,
    build_unsupported_window_snapshot,
    build_window_snapshot,
    describe_window_snapshot,
)


class WindowStateTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_build_window_snapshot_matches_registered_apps_from_process_name_and_title(self):
        snapshot = build_window_snapshot(
            self.paths,
            (
                NativeWindow(handle=100, title="Jarvis Lite - Google Chrome", process_id=10, process_name="chrome.exe"),
                NativeWindow(handle=200, title="代理面板", process_id=20, process_name="unknown.exe"),
            ),
            foreground_handle=100,
            platform_name="Windows",
        )

        self.assertTrue(snapshot.supported)
        self.assertEqual(snapshot.foreground_window.title, "Jarvis Lite - Google Chrome")
        self.assertEqual(snapshot.foreground_window.app_id, "chrome")
        self.assertEqual(snapshot.foreground_window.app_display_name, "Chrome")
        self.assertEqual(snapshot.windows[1].app_id, "clash_verge")
        self.assertTrue(snapshot.windows[0].is_foreground)
        self.assertFalse(snapshot.windows[1].is_foreground)

    def test_describe_window_snapshot_lists_foreground_window_and_visible_windows_without_actions(self):
        snapshot = build_window_snapshot(
            self.paths,
            (
                NativeWindow(handle=100, title="Jarvis Lite - Google Chrome", process_id=10, process_name="chrome.exe"),
                NativeWindow(handle=200, title="代理面板", process_id=20, process_name="unknown.exe"),
            ),
            foreground_handle=100,
            platform_name="Windows",
        )

        description = describe_window_snapshot(snapshot)

        self.assertIn("窗口感知：", description)
        self.assertIn("当前阶段只做只读观察，不切换窗口、不点击、不输入", description)
        self.assertIn("前台窗口：Jarvis Lite - Google Chrome", description)
        self.assertIn("进程：chrome.exe (PID 10)", description)
        self.assertIn("已识别应用：Chrome (chrome)", description)
        self.assertIn("可见窗口：2 个", description)
        self.assertIn("2. 代理面板 | 进程：unknown.exe (PID 20) | 应用：Clash Verge (clash_verge)", description)

    def test_describe_unsupported_window_snapshot_reports_platform_reason(self):
        snapshot = build_unsupported_window_snapshot("Linux", "当前仅支持 Windows 窗口枚举。")

        description = describe_window_snapshot(snapshot)

        self.assertIn("窗口感知：不可用", description)
        self.assertIn("平台：Linux", description)
        self.assertIn("原因：当前仅支持 Windows 窗口枚举。", description)
        self.assertIn("当前阶段只做只读观察", description)


if __name__ == "__main__":
    unittest.main()
