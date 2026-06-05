import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.authorization_rules import save_authorization_rule
from jarvis_lite.automation import add_common_directory
from jarvis_lite.config import build_project_paths
from jarvis_lite.contacts import save_contact_alias
from jarvis_lite.memory import append_experience, append_memory
from jarvis_lite.memory_config_candidates import record_memory_config_candidate
from jarvis_lite.memory_config_manager import describe_memory_config_manager
from jarvis_lite.preferences import save_preference


class MemoryConfigManagerTests(unittest.TestCase):
    def test_describe_memory_config_manager_reports_empty_storage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            response = describe_memory_config_manager(paths)

            self.assertIn("记忆与配置管家：", response)
            self.assertIn("长期记忆：0 条", response)
            self.assertIn("经验记忆：0 条", response)
            self.assertIn("常用目录：0 个", response)
            self.assertIn("联系人别名：0 个", response)
            self.assertIn("授权规则：0 条", response)
            self.assertIn("偏好：0 条", response)
            self.assertIn("应用本地覆盖：0 个", response)
            self.assertIn("LLM 本地配置：未创建", response)
            self.assertIn("联网搜索本地配置：未创建", response)
            self.assertIn("记忆与配置候选：0 条活跃，0 条已忽略", response)
            self.assertIn("本阶段只做只读盘点", response)
            self.assertIn("/remember 记忆内容", response)
            self.assertIn("/authorization-status", response)
            self.assertIn("/preference-status", response)
            self.assertIn("/preference-preview", response)
            self.assertIn("/config-candidates", response)

    def test_describe_memory_config_manager_masks_provider_api_keys(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            target = Path(temp_dir) / "project"
            target.mkdir()
            append_memory(paths, "用户姓名：欧阳")
            append_memory(paths, "用户偏好：中文回答")
            append_experience(paths, "导入资料后先打标签")
            add_common_directory(paths, "项目", target)
            save_contact_alias(paths, "小王", "微信联系人王工", source="test")
            save_authorization_rule(paths, "微信发消息前需要确认", source="test")
            save_preference(paths, "回答尽量简洁", source="test")
            record_memory_config_candidate(paths, "app_alias", "代理面板 = Clash Verge")
            (paths.config_dir / "apps.local.json").write_text(
                json.dumps(
                    {
                        "apps": {
                            "chrome": {
                                "path": str(target / "chrome.exe"),
                                "aliases": ["工作浏览器"],
                            }
                        }
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (paths.config_dir / "llm.local.json").write_text(
                json.dumps(
                    {
                        "provider": "qwen",
                        "model": "qwen-plus",
                        "base_url": "https://qwen.example/v1/responses",
                        "api_key": "secret-llm-key",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (paths.config_dir / "search.local.json").write_text(
                json.dumps(
                    {
                        "provider": "tavily",
                        "api_key": "secret-search-key",
                        "max_results": 3,
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            response = describe_memory_config_manager(paths)

            self.assertIn("长期记忆：2 条", response)
            self.assertIn("经验记忆：1 条", response)
            self.assertIn("常用目录：1 个", response)
            self.assertIn("目录别名：项目", response)
            self.assertIn("联系人别名：1 个", response)
            self.assertIn("授权规则：1 条", response)
            self.assertIn("偏好：1 条", response)
            self.assertIn("应用本地覆盖：1 个", response)
            self.assertIn("记忆与配置候选：1 条活跃，0 条已忽略", response)
            self.assertIn("LLM 本地配置：存在", response)
            self.assertIn("Provider：qwen", response)
            self.assertIn("Model：qwen-plus", response)
            self.assertIn("API key：已配置", response)
            self.assertIn("联网搜索本地配置：存在", response)
            self.assertIn("Max results：3", response)
            self.assertNotIn("secret-llm-key", response)
            self.assertNotIn("secret-search-key", response)


if __name__ == "__main__":
    unittest.main()
