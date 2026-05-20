import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths


class ConfigTests(unittest.TestCase):
    def test_build_project_paths_creates_expected_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            paths = build_project_paths(root)

            self.assertEqual(paths.root, root)
            self.assertTrue(paths.memory_dir.is_dir())
            self.assertTrue(paths.data_dir.is_dir())
            self.assertTrue(paths.logs_dir.is_dir())
            self.assertTrue(paths.word_dir.is_dir())

    def test_frozen_app_uses_local_app_data_as_default_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            local_app_data = Path(temp_dir) / "LocalAppData"

            with patch.dict("os.environ", {"LOCALAPPDATA": str(local_app_data)}), patch.object(sys, "frozen", True, create=True):
                paths = build_project_paths()

            self.assertEqual(paths.root, local_app_data / "Jarvis Lite")
            self.assertTrue(paths.memory_dir.is_dir())
            self.assertTrue(paths.data_dir.is_dir())


if __name__ == "__main__":
    unittest.main()
