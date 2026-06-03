import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.chrome_workflow import (
    build_chrome_search_url,
    describe_chrome_open,
    describe_chrome_search,
    describe_chrome_workflow_status,
    normalize_chrome_url,
    open_chrome_url,
)
from jarvis_lite.config import build_project_paths


class ChromeWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")
        self.chrome_path = self.paths.root / "tools" / "chrome.exe"
        self.chrome_path.parent.mkdir(parents=True)
        self.chrome_path.write_text("fake chrome", encoding="utf-8")
        (self.paths.config_dir / "apps.local.json").write_text(
            json.dumps(
                {
                    "apps": {
                        "chrome": {
                            "path": str(self.chrome_path),
                            "aliases": ["我的浏览器"],
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

    def test_normalize_chrome_url_adds_https_for_plain_domain(self):
        self.assertEqual(normalize_chrome_url("example.com/docs"), "https://example.com/docs")
        self.assertEqual(normalize_chrome_url("https://example.com/docs"), "https://example.com/docs")

    def test_normalize_chrome_url_rejects_empty_or_non_http_target(self):
        with self.assertRaisesRegex(ValueError, "URL 不能为空"):
            normalize_chrome_url("  ")
        with self.assertRaisesRegex(ValueError, "只支持 http/https"):
            normalize_chrome_url("file:///C:/temp/a.txt")

    def test_build_chrome_search_url_encodes_query(self):
        self.assertEqual(
            build_chrome_search_url("Jarvis Lite 中文"),
            "https://www.google.com/search?q=Jarvis+Lite+%E4%B8%AD%E6%96%87",
        )

    def test_open_chrome_url_uses_configured_path_and_injected_executor(self):
        calls = []

        result = open_chrome_url(self.paths, "example.com/docs", executor=lambda path, url: calls.append((path, url)))

        self.assertEqual(result.app.app_id, "chrome")
        self.assertEqual(result.alias, "chrome")
        self.assertEqual(result.path, self.chrome_path.resolve())
        self.assertEqual(result.url, "https://example.com/docs")
        self.assertEqual(calls, [(self.chrome_path.resolve(), "https://example.com/docs")])

    def test_describe_chrome_open_reports_scope_without_page_actions(self):
        response = describe_chrome_open(self.paths, "https://example.com", executor=lambda path, url: None)

        self.assertIn("Chrome 打开网页执行", response)
        self.assertIn("URL：https://example.com", response)
        self.assertIn("不读取网页、不点击页面、不输入页面内容", response)

    def test_describe_chrome_search_opens_encoded_search_url(self):
        calls = []

        response = describe_chrome_search(self.paths, "Jarvis Lite", executor=lambda path, url: calls.append(url))

        self.assertIn("Chrome 搜索执行", response)
        self.assertIn("关键词：Jarvis Lite", response)
        self.assertEqual(calls, ["https://www.google.com/search?q=Jarvis+Lite"])

    def test_open_chrome_url_reports_missing_chrome_path(self):
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
            with self.assertRaisesRegex(FileNotFoundError, "Chrome 启动路径未找到"):
                open_chrome_url(self.paths, "example.com", executor=lambda path, url: None)

    def test_describe_chrome_workflow_status_reports_first_stage_boundary(self):
        response = describe_chrome_workflow_status(self.paths)

        self.assertIn("Chrome 工作流状态：第一阶段", response)
        self.assertIn("/chrome-open URL", response)
        self.assertIn("/chrome-search 关键词", response)
        self.assertIn("不读取网页", response)


if __name__ == "__main__":
    unittest.main()
