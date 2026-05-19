import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "minimal")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtWidgets import QApplication

from jarvis_lite.config import build_project_paths
from jarvis_lite.desktop.bridge import DesktopBridge
from jarvis_lite.desktop.tray import DesktopTrayController
from jarvis_lite.desktop.widgets import AssistantPanel, DesktopPetWindow


class DesktopTrayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv[:1])

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")
        self.bridge = DesktopBridge(self.paths)
        self.panel = AssistantPanel(self.bridge)
        self.pet = DesktopPetWindow(self.panel, self.paths)

    def tearDown(self):
        if hasattr(self.pet, "allow_application_close"):
            self.pet.allow_application_close()
        self.panel.close()
        self.pet.close()
        self.app.setQuitOnLastWindowClosed(True)
        self.temp_dir.cleanup()

    def test_tray_controller_exposes_lifecycle_actions(self):
        controller = DesktopTrayController(self.app, self.pet)

        self.assertEqual(controller.action_texts(), ("显示助手", "隐藏助手", "退出"))
        self.assertFalse(self.app.quitOnLastWindowClosed())
        self.assertTrue(self.pet.is_close_to_tray_enabled())

    def test_pet_close_hides_to_tray_when_tray_controller_is_enabled(self):
        DesktopTrayController(self.app, self.pet)
        self.pet.show()
        QApplication.processEvents()

        close_accepted = self.pet.close()
        QApplication.processEvents()

        self.assertFalse(close_accepted)
        self.assertFalse(self.pet.isVisible())
        self.assertFalse(self.panel.isVisible())

    def test_tray_controller_can_show_hide_and_quit_application(self):
        controller = DesktopTrayController(self.app, self.pet)

        controller.show_assistant()
        QApplication.processEvents()

        self.assertTrue(self.pet.isVisible())

        self.pet.toggle_panel()
        QApplication.processEvents()
        self.assertTrue(self.panel.isVisible())

        controller.hide_assistant()
        QApplication.processEvents()

        self.assertFalse(self.pet.isVisible())
        self.assertFalse(self.panel.isVisible())

        controller.quit_application()
        QApplication.processEvents()

        self.assertTrue(controller.is_quit_requested())
        self.assertFalse(self.pet.is_close_to_tray_enabled())


if __name__ == "__main__":
    unittest.main()
