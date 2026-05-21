import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.update import (
    check_for_update,
    describe_update_download,
    describe_update_status,
    download_update,
    is_newer_version,
)


class UpdateTests(unittest.TestCase):
    def test_version_comparison_treats_numeric_segments_as_numbers(self):
        self.assertTrue(is_newer_version("0.10.0", "0.2.0"))
        self.assertFalse(is_newer_version("0.1.0", "0.1.0"))
        self.assertFalse(is_newer_version("0.1.0", "0.2.0"))

    def test_describe_update_status_reports_missing_update_source(self):
        with patch.dict("os.environ", {}, clear=True):
            response = describe_update_status(current_version="0.1.0")

        self.assertIn("当前版本：0.1.0", response)
        self.assertIn("更新源：未配置", response)
        self.assertIn("JARVIS_LITE_UPDATE_MANIFEST_URL", response)

    def test_check_for_update_reads_local_manifest_and_reports_update_available(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "update.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "version": "0.2.0",
                        "download_url": "https://example.com/JarvisLiteSetup.exe",
                        "release_notes": "新增更新检查。",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = check_for_update(str(manifest_path), current_version="0.1.0")

        self.assertTrue(result.update_available)
        self.assertEqual(result.latest_version, "0.2.0")
        self.assertEqual(result.download_url, "https://example.com/JarvisLiteSetup.exe")
        self.assertEqual(result.release_notes, "新增更新检查。")

    def test_describe_update_status_reports_current_version_is_latest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "update.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "version": "0.1.0",
                        "download_url": "https://example.com/JarvisLiteSetup.exe",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            response = describe_update_status(str(manifest_path), current_version="0.1.0")

        self.assertIn("当前已是最新版本", response)
        self.assertIn("最新版本：0.1.0", response)

    def test_download_update_copies_local_package_to_runtime_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_path = root / "JarvisLiteSetup.exe"
            package_path.write_bytes(b"installer")
            manifest_path = root / "update.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "version": "0.2.0",
                        "download_url": str(package_path),
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            downloads_dir = root / "jarvis-lite-runtime" / "updates"

            result = download_update(str(manifest_path), downloads_dir=downloads_dir, current_version="0.1.0")

            self.assertTrue(result.update_available)
            self.assertEqual(result.destination_path, downloads_dir / "JarvisLiteSetup.exe")
            self.assertEqual(result.bytes_written, len(b"installer"))
            self.assertEqual((downloads_dir / "JarvisLiteSetup.exe").read_bytes(), b"installer")

    def test_download_update_skips_when_current_version_is_latest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_path = root / "JarvisLiteSetup.exe"
            package_path.write_bytes(b"installer")
            manifest_path = root / "update.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "version": "0.1.0",
                        "download_url": str(package_path),
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            downloads_dir = root / "jarvis-lite-runtime" / "updates"

            result = download_update(str(manifest_path), downloads_dir=downloads_dir, current_version="0.1.0")

            self.assertFalse(result.update_available)
            self.assertIsNone(result.destination_path)
            self.assertEqual(result.bytes_written, 0)
            self.assertFalse(downloads_dir.exists())

    def test_describe_update_download_reports_saved_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_path = root / "JarvisLiteSetup.exe"
            package_path.write_bytes(b"installer")
            manifest_path = root / "update.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "version": "0.2.0",
                        "download_url": str(package_path),
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            downloads_dir = root / "jarvis-lite-runtime" / "updates"

            response = describe_update_download(str(manifest_path), downloads_dir=downloads_dir, current_version="0.1.0")

            self.assertIn("已下载更新安装包", response)
            self.assertIn("版本：0.2.0", response)
            self.assertIn(str(downloads_dir / "JarvisLiteSetup.exe"), response)


if __name__ == "__main__":
    unittest.main()
