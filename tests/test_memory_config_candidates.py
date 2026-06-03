import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.memory_config_candidates import (
    apply_memory_config_candidate,
    describe_memory_config_candidates,
    dismiss_memory_config_candidate,
    record_memory_config_candidate,
)
from jarvis_lite.automation import list_common_directories
from jarvis_lite.memory import read_experiences, read_profile
from jarvis_lite.runtime_context import load_runtime_context


class MemoryConfigCandidateTests(unittest.TestCase):
    def test_describe_memory_config_candidates_reports_empty_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            response = describe_memory_config_candidates(paths)

            self.assertIn("记忆与配置候选：暂无。", response)
            self.assertIn("不会自动写入长期记忆或配置", response)
            self.assertIn("/config-candidate-add 类型 内容", response)
            self.assertIn("/config-candidate-apply 编号", response)

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
            self.assertIn("/config-candidate-apply 编号", response)
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

    def test_apply_memory_and_experience_candidates_persist_and_mark_applied(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            record_memory_config_candidate(paths, "memory", "项目简称：Jarvis Lite")
            record_memory_config_candidate(paths, "experience", "失败复盘后先补本机 evaluation 样本")

            memory_response = apply_memory_config_candidate(paths, 1)
            experience_response = apply_memory_config_candidate(paths, 1)
            list_response = describe_memory_config_candidates(paths)
            runtime_context = load_runtime_context(paths)

            self.assertIn("已固化记忆与配置候选 1：长期记忆", memory_response)
            self.assertIn("memory/profile.md", memory_response)
            self.assertIn("- 项目简称：Jarvis Lite", read_profile(paths))
            self.assertIn("已固化记忆与配置候选 1：经验记忆", experience_response)
            self.assertIn("memory/experiences.md", experience_response)
            self.assertIn("- 失败复盘后先补本机 evaluation 样本", read_experiences(paths))
            self.assertIn("记忆与配置候选：暂无。", list_response)
            self.assertEqual(
                [candidate.status for candidate in runtime_context.memory_config_candidates],
                ["applied", "applied"],
            )

    def test_apply_directory_candidate_registers_common_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            target_dir = Path(temp_dir) / "work"
            target_dir.mkdir()
            record_memory_config_candidate(paths, "directory", f"工作区 => {target_dir}")

            response = apply_memory_config_candidate(paths, 1)
            directories = list_common_directories(paths)

            self.assertIn("已固化记忆与配置候选 1：常用目录", response)
            self.assertIn("memory/directories.json", response)
            self.assertEqual(len(directories), 1)
            self.assertEqual(directories[0].alias, "工作区")
            self.assertEqual(directories[0].path, target_dir.resolve())

    def test_apply_rejects_unsupported_or_invalid_candidates_without_hiding_them(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            record_memory_config_candidate(paths, "contact_alias", "小王 => 微信联系人王工")
            record_memory_config_candidate(paths, "directory", "缺少路径")

            unsupported_response = apply_memory_config_candidate(paths, 1)
            invalid_directory_response = apply_memory_config_candidate(paths, 2)
            list_response = describe_memory_config_candidates(paths)
            runtime_context = load_runtime_context(paths)

            self.assertIn("暂不支持固化联系人别名候选", unsupported_response)
            self.assertIn("不会写入长期配置", unsupported_response)
            self.assertIn("目录候选格式", invalid_directory_response)
            self.assertIn("联系人别名：小王 => 微信联系人王工", list_response)
            self.assertIn("常用目录：缺少路径", list_response)
            self.assertEqual(
                [candidate.status for candidate in runtime_context.memory_config_candidates],
                ["active", "active"],
            )


if __name__ == "__main__":
    unittest.main()
