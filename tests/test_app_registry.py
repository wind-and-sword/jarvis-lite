import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.app_registry import (
    find_registered_app,
    list_registered_apps,
    describe_registered_apps,
    describe_app_launch,
    launch_registered_app,
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
        self.assertIn("可用 /app-launch 启动已登记且有路径的应用", description)

    def test_launch_registered_app_uses_configured_path_and_injected_executor(self):
        executable = self.paths.root / "tools" / "browser.exe"
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
        launched_paths = []

        result = launch_registered_app(self.paths, "我的浏览器", executor=launched_paths.append)

        self.assertEqual(result.app.app_id, "chrome")
        self.assertEqual(result.alias, "我的浏览器")
        self.assertEqual(result.path, executable.resolve())
        self.assertEqual(launched_paths, [executable.resolve()])

    def test_describe_app_launch_reports_scope_without_window_or_input_actions(self):
        executable = self.paths.root / "tools" / "browser.exe"
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

        response = describe_app_launch(self.paths, "我的浏览器", executor=lambda path: None)

        self.assertIn("应用启动执行：Chrome (chrome)", response)
        self.assertIn("命中别名：我的浏览器", response)
        self.assertIn(f"路径：{executable.resolve()}", response)
        self.assertIn("当前阶段只启动已登记应用，不切换窗口、不点击、不输入", response)

    def test_launch_registered_app_reports_unknown_app(self):
        with self.assertRaisesRegex(ValueError, "没有找到应用：不存在的应用"):
            launch_registered_app(self.paths, "不存在的应用", executor=lambda path: None)

    def test_launch_registered_app_reports_missing_launch_path(self):
        empty_root = self.paths.root / "empty-program-files"
        empty_root.mkdir()

        with patch.dict(
            os.environ,
            {
                "ProgramFiles": str(empty_root),
                "ProgramFiles(x86)": str(empty_root),
                "LOCALAPPDATA": str(empty_root),
                "APPDATA": str(empty_root),
            },
        ):
            with self.assertRaisesRegex(FileNotFoundError, "应用启动路径未找到：Chrome"):
                launch_registered_app(self.paths, "Chrome", executor=lambda path: None)


if __name__ == "__main__":
    unittest.main()
