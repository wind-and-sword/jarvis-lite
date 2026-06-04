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
    describe_task_window_context,
    describe_window_snapshot,
    describe_window_focus,
    select_window_focus_target,
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

    def test_describe_task_window_context_returns_compact_foreground_summary(self):
        snapshot = build_window_snapshot(
            self.paths,
            (
                NativeWindow(handle=100, title="Jarvis Lite - Google Chrome", process_id=10, process_name="chrome.exe"),
                NativeWindow(handle=200, title="代理面板", process_id=20, process_name="unknown.exe"),
            ),
            foreground_handle=100,
            platform_name="Windows",
        )

        description = describe_task_window_context(self.paths, snapshot=snapshot)

        self.assertEqual(
            description,
            "当前窗口：Jarvis Lite - Google Chrome | 进程：chrome.exe (PID 10) | 应用：Chrome (chrome)",
        )

    def test_select_window_focus_target_accepts_window_list_index(self):
        snapshot = build_window_snapshot(
            self.paths,
            (
                NativeWindow(handle=100, title="Jarvis Lite - Google Chrome", process_id=10, process_name="chrome.exe"),
                NativeWindow(handle=200, title="代理面板", process_id=20, process_name="Clash Verge.exe"),
            ),
            foreground_handle=100,
            platform_name="Windows",
        )

        selection = select_window_focus_target(self.paths, snapshot, "2")

        self.assertEqual(selection.window.handle, 200)
        self.assertEqual(selection.match_reason, "窗口编号：2")

    def test_select_window_focus_target_matches_registered_app_and_title(self):
        snapshot = build_window_snapshot(
            self.paths,
            (
                NativeWindow(handle=100, title="Jarvis Lite - Google Chrome", process_id=10, process_name="chrome.exe"),
                NativeWindow(handle=200, title="代理面板", process_id=20, process_name="unknown.exe"),
                NativeWindow(handle=300, title="项目 - IntelliJ IDEA", process_id=30, process_name="idea64.exe"),
            ),
            foreground_handle=100,
            platform_name="Windows",
        )

        app_selection = select_window_focus_target(self.paths, snapshot, "JetBrains IDEA")
        title_selection = select_window_focus_target(self.paths, snapshot, "面板")

        self.assertEqual(app_selection.window.handle, 300)
        self.assertEqual(app_selection.match_reason, "应用：IntelliJ IDEA (idea)")
        self.assertEqual(title_selection.window.handle, 200)
        self.assertEqual(title_selection.match_reason, "标题包含：面板")

    def test_select_window_focus_target_rejects_ambiguous_or_missing_query(self):
        snapshot = build_window_snapshot(
            self.paths,
            (
                NativeWindow(handle=100, title="Jarvis Lite - Google Chrome", process_id=10, process_name="chrome.exe"),
                NativeWindow(handle=200, title="Docs - Google Chrome", process_id=20, process_name="chrome.exe"),
            ),
            foreground_handle=100,
            platform_name="Windows",
        )

        with self.assertRaisesRegex(ValueError, "匹配到多个窗口"):
            select_window_focus_target(self.paths, snapshot, "Chrome")
        with self.assertRaisesRegex(ValueError, "没有找到可切换窗口"):
            select_window_focus_target(self.paths, snapshot, "不存在的窗口")

    def test_describe_window_focus_invokes_executor_without_real_switching(self):
        snapshot = build_window_snapshot(
            self.paths,
            (
                NativeWindow(handle=100, title="Jarvis Lite - Google Chrome", process_id=10, process_name="chrome.exe"),
                NativeWindow(handle=200, title="代理面板", process_id=20, process_name="Clash Verge.exe"),
            ),
            foreground_handle=100,
            platform_name="Windows",
        )
        calls: list[int] = []

        description = describe_window_focus(
            self.paths,
            "2",
            snapshot=snapshot,
            executor=lambda handle: calls.append(handle),
        )

        self.assertEqual(calls, [200])
        self.assertIn("窗口切换执行：代理面板", description)
        self.assertIn("匹配：窗口编号：2", description)
        self.assertIn("当前阶段只切换显式窗口", description)


if __name__ == "__main__":
    unittest.main()
