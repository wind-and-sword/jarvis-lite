import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.ocr import OcrAvailability, describe_image_ocr, describe_ocr_status


class OcrTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_describe_ocr_status_reports_unavailable_tesseract_cli(self):
        def fake_probe() -> OcrAvailability:
            return OcrAvailability(
                provider="tesseract-cli",
                available=False,
                command=None,
                version=None,
                reason="未找到 tesseract.exe",
            )

        response = describe_ocr_status(self.paths, probe=fake_probe)

        self.assertIn("OCR 状态：不可用", response)
        self.assertIn("Provider：tesseract-cli", response)
        self.assertIn("原因：未找到 tesseract.exe", response)

    def test_describe_image_ocr_reports_text_from_recognizer(self):
        image = self.paths.root / "logs" / "screenshots" / "sample.png"
        image.parent.mkdir(parents=True, exist_ok=True)
        image.write_bytes(b"fake-png")
        calls: list[tuple[Path, str]] = []

        def fake_recognizer(image_path: Path, language: str) -> str:
            calls.append((image_path, language))
            return "第一行\nSecond line"

        response = describe_image_ocr(
            self.paths,
            "logs/screenshots/sample.png",
            language="chi_sim+eng",
            recognizer=fake_recognizer,
        )

        self.assertIn("OCR 图片识别：logs/screenshots/sample.png", response)
        self.assertIn("Provider：tesseract-cli", response)
        self.assertIn("语言：chi_sim+eng", response)
        self.assertIn("第一行", response)
        self.assertEqual(calls, [(image, "chi_sim+eng")])

    def test_describe_image_ocr_reports_missing_image_and_engine_error(self):
        missing = describe_image_ocr(self.paths, "logs/screenshots/missing.png", recognizer=lambda path, lang: "")

        self.assertIn("OCR 图片识别失败：图片不存在", missing)

        image = self.paths.root / "sample.png"
        image.write_bytes(b"fake")

        def broken_recognizer(image_path: Path, language: str) -> str:
            raise RuntimeError("未找到 tesseract.exe")

        unavailable = describe_image_ocr(self.paths, "sample.png", recognizer=broken_recognizer)

        self.assertIn("OCR 图片识别失败：未找到 tesseract.exe", unavailable)


if __name__ == "__main__":
    unittest.main()
