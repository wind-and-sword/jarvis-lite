import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.memory_config_candidates import (
    describe_memory_config_candidates,
    dismiss_memory_config_candidate,
    record_memory_config_candidate,
)
from jarvis_lite.runtime_context import load_runtime_context


class MemoryConfigCandidateTests(unittest.TestCase):
    def test_describe_memory_config_candidates_reports_empty_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            response = describe_memory_config_candidates(paths)

            self.assertIn("记忆与配置候选：暂无。", response)
            self.assertIn("不会自动写入长期记忆或配置", response)
            self.assertIn("/config-candidate-add 类型 内容", response)

    def test_record_memory_config_candidate_merges_duplicates_and_persists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            first = record_memory_config_candidate(paths, "memory", "以后称这个项目为 Jarvis Lite")
            second = record_memory_config_candidate(paths, "记忆", "以后称这个项目为 Jarvis Lite")
            response = describe_memory_config_candidates(paths)
            runtime_context = load_runtime_context(paths)

            self.assertIn("已记录记忆与配置候选：长期记忆", first)
            self.assertIn("出现次数：2", second)
            self.assertIn("1. 长期记忆：以后称这个项目为 Jarvis Lite", response)
            self.assertIn("出现次数：2", response)
            self.assertEqual(len(runtime_context.memory_config_candidates), 1)
            self.assertEqual(runtime_context.memory_config_candidates[0].count, 2)
            self.assertFalse(paths.profile_path.exists())
            self.assertFalse((paths.config_dir / "apps.local.json").exists())

    def test_dismiss_memory_config_candidate_hides_active_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            record_memory_config_candidate(paths, "memory", "以后称这个项目为 Jarvis Lite")
            record_memory_config_candidate(paths, "directory", "把 E:/work 记成工作区")

            dismiss_response = dismiss_memory_config_candidate(paths, 1)
            response = describe_memory_config_candidates(paths)
            runtime_context = load_runtime_context(paths)

            self.assertIn("已忽略候选 1", dismiss_response)
            self.assertNotIn("以后称这个项目为 Jarvis Lite", response)
            self.assertIn("常用目录：把 E:/work 记成工作区", response)
            self.assertEqual(
                [candidate.status for candidate in runtime_context.memory_config_candidates],
                ["dismissed", "active"],
            )


if __name__ == "__main__":
    unittest.main()
