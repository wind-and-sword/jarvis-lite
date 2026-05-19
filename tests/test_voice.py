import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.voice import describe_voice, speak_text


class VoiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_speak_text_records_transcript_in_transcript_engine(self):
        result = speak_text(self.paths, "Jarvis Lite 语音播报", engine="transcript")

        transcript = self.paths.logs_dir / "voice-output.txt"
        self.assertTrue(result.success)
        self.assertIn("已记录语音播报文本", result.message)
        self.assertIn("Jarvis Lite 语音播报", transcript.read_text(encoding="utf-8"))

    def test_speak_text_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            speak_text(self.paths, "   ", engine="transcript")

    def test_describe_voice_reports_transcript_path(self):
        description = describe_voice(self.paths, engine="transcript")

        self.assertIn("语音入口状态", description)
        self.assertIn("当前引擎：transcript", description)
        self.assertIn("logs/voice-output.txt", description)


if __name__ == "__main__":
    unittest.main()
