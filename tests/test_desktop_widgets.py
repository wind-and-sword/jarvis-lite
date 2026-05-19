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
from jarvis_lite.desktop.widgets import AssistantPanel, DesktopPetWindow


class DesktopWidgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv[:1])

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name))
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 用户偏好：中文回答\n",
            encoding="utf-8",
        )
        self.bridge = DesktopBridge(self.paths)
        self.panel = AssistantPanel(self.bridge)
        self.pet = DesktopPetWindow(self.panel)

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

    def test_pet_caption_tracks_panel_state(self):
        self.pet.toggle_panel()
        self.panel.submit_text("/not-found")

        self.assertEqual(self.pet.caption_text(), "错误")

        self.panel.submit_text("/memory")

        self.assertEqual(self.pet.caption_text(), "完成")


if __name__ == "__main__":
    unittest.main()
