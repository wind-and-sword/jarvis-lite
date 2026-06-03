import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.app_registry import (
    find_registered_app,
    list_registered_apps,
    describe_registered_apps,
)
from jarvis_lite.config import build_project_paths


class AppRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_builtin_registry_contains_first_five_apps(self):
        apps = list_registered_apps(self.paths)

        self.assertEqual([app.app_id for app in apps], ["chrome", "qq", "wechat", "idea", "clash_verge"])
        self.assertEqual([app.display_name for app in apps], ["Chrome", "QQ", "微信", "IntelliJ IDEA", "Clash Verge"])

    def test_find_registered_app_matches_common_chinese_and_english_aliases(self):
        self.assertEqual(find_registered_app(self.paths, "谷歌浏览器").app_id, "chrome")
        self.assertEqual(find_registered_app(self.paths, "google chrome").app_id, "chrome")
        self.assertEqual(find_registered_app(self.paths, "微信").app_id, "wechat")
        self.assertEqual(find_registered_app(self.paths, "idea").app_id, "idea")
        self.assertEqual(find_registered_app(self.paths, "代理面板").app_id, "clash_verge")
        self.assertIsNone(find_registered_app(self.paths, "不存在的应用"))

    def test_local_config_overrides_path_and_adds_aliases(self):
        executable = self.paths.root / "tools" / "chrome.exe"
        executable.parent.mkdir(parents=True)
        executable.write_text("fake executable", encoding="utf-8")
        (self.paths.config_dir / "apps.local.json").write_text(
            json.dumps(
                {
                    "apps": {
                        "chrome": {
                            "path": str(executable),
                            "aliases": ["我的浏览器"],
                        }
                    }
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        app = find_registered_app(self.paths, "我的浏览器")
        description = describe_registered_apps(self.paths)

        self.assertEqual(app.app_id, "chrome")
        self.assertEqual(app.configured_path, executable.resolve())
        self.assertEqual(app.launch_path, executable.resolve())
        self.assertIn("我的浏览器", app.aliases)
        self.assertIn(f"路径：{executable.resolve()}", description)


if __name__ == "__main__":
    unittest.main()
