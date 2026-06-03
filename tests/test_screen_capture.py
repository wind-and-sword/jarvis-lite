import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.screen_capture import describe_screen_capture, describe_screen_ocr, save_screen_capture


class ScreenCaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_screen_capture_writes_png_to_logs_screenshots(self):
        def fake_capturer(target_path: Path) -> tuple[int, int]:
            target_path.write_bytes(b"\x89PNG\r\n\x1a\nfake")
            return (1920, 1080)

        result = save_screen_capture(self.paths, filename="desktop.png", capturer=fake_capturer)

        self.assertEqual(result.relative_path, "logs/screenshots/desktop.png")
        self.assertEqual(result.width, 1920)
        self.assertEqual(result.height, 1080)
        self.assertEqual(result.path.read_bytes(), b"\x89PNG\r\n\x1a\nfake")

    def test_save_screen_capture_adds_png_suffix_and_rejects_empty_filename(self):
        def fake_capturer(target_path: Path) -> tuple[int, int]:
            target_path.write_bytes(b"png")
            return (800, 600)

        result = save_screen_capture(self.paths, filename="current-screen", capturer=fake_capturer)

        self.assertEqual(result.relative_path, "logs/screenshots/current-screen.png")
        with self.assertRaises(ValueError):
            save_screen_capture(self.paths, filename="   ", capturer=fake_capturer)

    def test_describe_screen_capture_reports_path_size_and_action_boundary(self):
        def fake_capturer(target_path: Path) -> tuple[int, int]:
            target_path.write_bytes(b"png")
            return (1366, 768)

        description = describe_screen_capture(self.paths, filename="smoke", capturer=fake_capturer)

        self.assertIn("已保存屏幕截图：logs/screenshots/smoke.png", description)
        self.assertIn("尺寸：1366x768", description)
        self.assertIn("当前阶段只截图保存，不 OCR、不点击、不切换窗口", description)

    def test_describe_screen_ocr_captures_then_recognizes_saved_image(self):
        calls: list[tuple[Path, str]] = []

        def fake_capturer(target_path: Path) -> tuple[int, int]:
            target_path.write_bytes(b"png")
            return (1280, 720)

        def fake_recognizer(image_path: Path, language: str) -> str:
            calls.append((image_path, language))
            return "屏幕文字"

        description = describe_screen_ocr(
            self.paths,
            filename="screen-now",
            language="eng",
            capturer=fake_capturer,
            recognizer=fake_recognizer,
        )

        expected_path = self.paths.root / "logs" / "screenshots" / "screen-now.png"
        self.assertEqual(calls, [(expected_path, "eng")])
        self.assertIn("截图 OCR：logs/screenshots/screen-now.png", description)
        self.assertIn("尺寸：1280x720", description)
        self.assertIn("OCR 图片识别：logs/screenshots/screen-now.png", description)
        self.assertIn("语言：eng", description)
        self.assertIn("屏幕文字", description)
        self.assertIn("当前阶段只截图并识别文字，不点击、不切换窗口、不输入", description)


if __name__ == "__main__":
    unittest.main()
