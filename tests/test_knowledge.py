import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.knowledge import answer_from_data, search_data


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_search_data_returns_matching_text_with_source(self):
        (self.paths.data_dir / "profile.md").write_text(
            "# 项目资料\n\nJarvis Lite 第一阶段使用 Python 3.13 作为运行环境。\n",
            encoding="utf-8",
        )

        results = search_data(self.paths, "Python 3.13")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].relative_path, "profile.md")
        self.assertIn("Python 3.13", results[0].text)

    def test_search_data_ignores_hidden_and_unsupported_files(self):
        (self.paths.data_dir / ".secret.md").write_text("Python 3.13", encoding="utf-8")
        (self.paths.data_dir / "raw.bin").write_text("Python 3.13", encoding="utf-8")

        results = search_data(self.paths, "Python")

        self.assertEqual(results, [])

    def test_answer_from_data_includes_source_and_matching_content(self):
        (self.paths.data_dir / "jarvis.txt").write_text(
            "Jarvis Lite 可以读取 data 目录里的文本资料。\n",
            encoding="utf-8",
        )

        answer = answer_from_data(self.paths, "Jarvis Lite 可以读取什么资料？")

        self.assertIn("根据 data/jarvis.txt:1", answer)
        self.assertIn("读取 data 目录里的文本资料", answer)

    def test_answer_from_data_returns_empty_string_without_match(self):
        (self.paths.data_dir / "jarvis.txt").write_text("Jarvis Lite 使用 Python。\n", encoding="utf-8")

        answer = answer_from_data(self.paths, "今天晚饭吃什么？")

        self.assertEqual(answer, "")


if __name__ == "__main__":
    unittest.main()
