import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.knowledge import (
    answer_from_data,
    build_knowledge_index,
    describe_knowledge_base,
    import_knowledge_file,
    search_data,
)


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

    def test_search_data_skips_markdown_headings(self):
        (self.paths.data_dir / "jarvis.md").write_text(
            "# Jarvis Lite 资料\n\nJarvis Lite 当前可以读取长期记忆。\n",
            encoding="utf-8",
        )

        results = search_data(self.paths, "Jarvis Lite 当前可以什么？")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].line_number, 3)

    def test_answer_from_data_filters_weak_matches_when_stronger_matches_exist(self):
        (self.paths.data_dir / "jarvis.md").write_text(
            "Jarvis Lite 当前可以读取长期记忆。\n"
            "Jarvis Lite 当前可以检索 data 文本资料。\n"
            "Jarvis Lite 第一阶段使用 Python 3.13。\n",
            encoding="utf-8",
        )

        answer = answer_from_data(self.paths, "Jarvis Lite 当前可以什么？")

        self.assertIn("data/jarvis.md:1", answer)
        self.assertIn("data/jarvis.md:2", answer)
        self.assertNotIn("data/jarvis.md:3", answer)

    def test_answer_from_data_includes_source_and_matching_content(self):
        (self.paths.data_dir / "jarvis.txt").write_text(
            "Jarvis Lite 可以读取 data 目录里的文本资料。\n",
            encoding="utf-8",
        )

        answer = answer_from_data(self.paths, "Jarvis Lite 可以读取什么资料？")

        self.assertIn("根据 data/jarvis.txt:1", answer)
        self.assertIn("读取 data 目录里的文本资料", answer)

    def test_answer_from_data_can_include_multiple_sources(self):
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "memory.txt").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )

        answer = answer_from_data(self.paths, "Jarvis Lite 使用什么？")

        self.assertIn("根据 data/memory.txt:1", answer)
        self.assertIn("根据 data/runtime.md:1", answer)
        self.assertLess(answer.index("data/memory.txt:1"), answer.index("data/runtime.md:1"))

    def test_answer_from_data_returns_empty_string_without_match(self):
        (self.paths.data_dir / "jarvis.txt").write_text("Jarvis Lite 使用 Python。\n", encoding="utf-8")

        answer = answer_from_data(self.paths, "今天晚饭吃什么？")

        self.assertEqual(answer, "")

    def test_build_knowledge_index_counts_supported_documents_and_searchable_lines(self):
        project_dir = self.paths.data_dir / "projects"
        project_dir.mkdir()
        (self.paths.data_dir / "intro.md").write_text(
            "# 标题\n\nJarvis Lite 是个人助手。\n\n第二行资料。\n",
            encoding="utf-8",
        )
        (project_dir / "jarvis.txt").write_text("阶段 2 关注个人知识库。\n", encoding="utf-8")
        (self.paths.data_dir / "image.png").write_text("不可检索", encoding="utf-8")

        index = build_knowledge_index(self.paths)

        self.assertEqual(index.document_count, 2)
        self.assertEqual(index.searchable_line_count, 3)
        self.assertEqual([document.relative_path for document in index.documents], ["intro.md", "projects/jarvis.txt"])

    def test_describe_knowledge_base_reports_empty_state(self):
        description = describe_knowledge_base(self.paths)

        self.assertIn("个人知识库状态", description)
        self.assertIn("还没有可检索资料", description)

    def test_import_knowledge_file_copies_supported_text_into_data(self):
        source = Path(self.temp_dir.name) / "outside.md"
        source.write_text("# 外部资料\n\nJarvis Lite 可以导入 Markdown。\n", encoding="utf-8")

        result = import_knowledge_file(self.paths, source)

        self.assertEqual(result.relative_path, "outside.md")
        self.assertEqual(result.searchable_line_count, 1)
        self.assertIn("导入 Markdown", (self.paths.data_dir / "outside.md").read_text(encoding="utf-8"))
        self.assertIn("outside.md", [document.relative_path for document in build_knowledge_index(self.paths).documents])

    def test_import_knowledge_file_can_use_target_name(self):
        source = Path(self.temp_dir.name) / "outside.txt"
        source.write_text("阶段 2 支持导入 txt。\n", encoding="utf-8")

        result = import_knowledge_file(self.paths, source, "notes.md")

        self.assertEqual(result.relative_path, "notes.md")
        self.assertTrue((self.paths.data_dir / "notes.md").is_file())

    def test_import_knowledge_file_rejects_unsupported_suffix(self):
        source = Path(self.temp_dir.name) / "image.png"
        source.write_text("不可导入", encoding="utf-8")

        with self.assertRaises(ValueError):
            import_knowledge_file(self.paths, source)

    def test_import_knowledge_file_rejects_existing_target(self):
        source = Path(self.temp_dir.name) / "outside.md"
        source.write_text("新资料\n", encoding="utf-8")
        (self.paths.data_dir / "outside.md").write_text("旧资料\n", encoding="utf-8")

        with self.assertRaises(FileExistsError):
            import_knowledge_file(self.paths, source)


if __name__ == "__main__":
    unittest.main()
