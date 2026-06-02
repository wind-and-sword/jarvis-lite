import sys
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite import __version__
from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths
from jarvis_lite.llm import FakeLLMProvider, LLMIntent, LLMRouter, LLMSettings, LLMUsage, build_llm_router
from jarvis_lite.runtime_context import load_runtime_context, runtime_context_path
from jarvis_lite.search import FakeSearchProvider, SearchResult, SearchRouter, SearchSettings


class SequenceLLMProvider:
    name = "fake"

    def __init__(self, intents):
        self.intents = list(intents)
        self.calls = []

    def complete_intent(self, prompt, context):
        self.calls.append((prompt, context))
        if not self.intents:
            return None
        return self.intents.pop(0)


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 用户偏好：中文简洁回答\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "note.txt").write_text("资料内容", encoding="utf-8")
        self.agent = JarvisAgent(self.paths)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_memory_command_returns_profile_content(self):
        response = self.agent.handle("/memory")

        self.assertIn("用户偏好：中文简洁回答", response)

    def test_experiences_command_reports_empty_state(self):
        response = self.agent.handle("/experiences")

        self.assertIn("还没有经验记忆", response)

    def test_experience_command_records_experience(self):
        response = self.agent.handle("/experience 导入资料后先打标签")

        self.assertIn("已记录经验：导入资料后先打标签", response)
        self.assertIn("导入资料后先打标签", self.agent.handle("/experiences"))

    def test_experience_search_command_returns_matching_experiences(self):
        self.agent.handle("/experience 导入资料后先打标签")
        self.agent.handle("/experience 日报生成后检查最近经验")
        self.agent.handle("/experience 导入 PDF 后查看知识库")

        response = self.agent.handle("/experience-search 导入")

        self.assertIn("经验搜索：导入", response)
        self.assertIn("1. 导入 PDF 后查看知识库", response)
        self.assertIn("2. 导入资料后先打标签", response)
        self.assertNotIn("日报生成", response)

    def test_experience_search_command_reports_no_match(self):
        self.agent.handle("/experience 导入资料后先打标签")

        response = self.agent.handle("/experience-search 语音")

        self.assertIn("没有找到和“语音”相关的经验", response)

    def test_experience_search_command_requires_keyword(self):
        response = self.agent.handle("/experience-search")

        self.assertIn("用法：/experience-search 关键词", response)

    def test_experience_advice_command_returns_related_experiences(self):
        self.agent.handle("/experience 导入资料后先打标签")
        self.agent.handle("/experience 日报生成后检查最近经验")
        self.agent.handle("/experience 导入 PDF 后查看知识库")

        response = self.agent.handle("/experience-advice 导入")

        self.assertIn("操作建议：导入", response)
        self.assertIn("相关经验：", response)
        self.assertIn("1. 导入 PDF 后查看知识库", response)
        self.assertIn("2. 导入资料后先打标签", response)
        self.assertIn("/experience-search 导入", response)
        self.assertNotIn("日报生成", response)

    def test_experience_advice_command_suggests_import_commands(self):
        self.agent.handle("/experience 导入资料后先打标签")

        response = self.agent.handle("/experience-advice 导入资料")

        self.assertIn("可执行命令：", response)
        self.assertIn("/import 源文件或目录路径 [目标文件名]", response)
        self.assertIn("/kb", response)
        self.assertIn("/tag 文件名 标签...", response)

    def test_experience_advice_command_reports_no_related_experience(self):
        self.agent.handle("/experience 导入资料后先打标签")

        response = self.agent.handle("/experience-advice 语音")

        self.assertIn("还没有找到和“语音”相关的经验建议", response)
        self.assertIn("/experience 经验内容", response)

    def test_experience_advice_command_suggests_known_commands_without_experience(self):
        response = self.agent.handle("/experience-advice 生成日报")

        self.assertIn("还没有找到和“生成日报”相关的经验建议", response)
        self.assertIn("可执行命令：", response)
        self.assertIn("/daily-report [文件名]", response)

    def test_experience_advice_for_recent_document_uses_recent_document_context(self):
        source = Path(self.temp_dir.name) / "recent-advice.md"
        source.write_text("Jarvis Lite 可以给最近资料提供建议。\n", encoding="utf-8")
        self.agent.handle("/experience 资料导入后先打标签")
        self.agent.handle(f"/import {source}")

        response = self.agent.handle("/experience-advice 这个资料")

        self.assertIn("当前资料：data/recent-advice.md", response)
        self.assertIn("资料导入后先打标签", response)
        self.assertIn("/read recent-advice.md", response)
        self.assertIn("/tag recent-advice.md 标签...", response)

    def test_experience_advice_for_recent_document_requires_recent_context(self):
        response = self.agent.handle("/experience-advice 这个资料")

        self.assertIn("还没有最近资料", response)
        self.assertIn("/import 源文件或目录路径 [目标文件名]", response)

    def test_experience_advice_for_recent_directory_uses_recent_directory_context(self):
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()
        self.agent.handle(f"/dir-add 项目 {target}")
        self.agent.handle("打开项目目录")

        response = self.agent.handle("/experience-advice 这个目录")

        self.assertIn(f"当前目录：项目 -> {target.resolve()}", response)
        self.assertIn("/organize-preview 项目", response)
        self.assertIn("/dir-open 项目", response)

    def test_experience_advice_command_requires_keyword(self):
        response = self.agent.handle("/experience-advice")

        self.assertIn("用法：/experience-advice 关键词", response)

    def test_natural_language_record_experience_records_experience(self):
        response = self.agent.handle("记住这个经验：导入资料后先打标签")

        self.assertIn("已记录经验：导入资料后先打标签", response)
        self.assertIn("导入资料后先打标签", self.agent.handle("/experiences"))

    def test_natural_language_search_experience_maps_to_experience_search(self):
        self.agent.handle("/experience 导入资料后先打标签")
        self.agent.handle("/experience 日报生成后检查最近经验")

        response = self.agent.handle("搜索经验 导入")

        self.assertIn("经验搜索：导入", response)
        self.assertIn("导入资料后先打标签", response)
        self.assertNotIn("日报生成", response)

    def test_natural_language_experience_advice_uses_related_experiences(self):
        self.agent.handle("/experience 导入资料后先打标签")
        self.agent.handle("/experience 日报生成后检查最近经验")

        response = self.agent.handle("我该怎么导入资料")

        self.assertIn("操作建议：导入资料", response)
        self.assertIn("导入资料后先打标签", response)
        self.assertNotIn("日报生成", response)

    def test_natural_language_experience_advice_includes_command_suggestions(self):
        self.agent.handle("/experience 导入资料后先打标签")

        response = self.agent.handle("导入资料有什么建议")

        self.assertIn("操作建议：导入资料", response)
        self.assertIn("可执行命令：", response)
        self.assertIn("/import 源文件或目录路径 [目标文件名]", response)

    def test_natural_language_read_first_advice_after_experience_advice(self):
        self.agent.handle("/experience-advice 导入资料")

        response = self.agent.handle("查看第一条建议")

        self.assertIn("第 1 条建议：", response)
        self.assertIn("/import 源文件或目录路径 [目标文件名]", response)

    def test_natural_language_read_numbered_advice_after_experience_advice(self):
        self.agent.handle("/experience-advice 导入资料")

        response = self.agent.handle("查看第二条建议")

        self.assertIn("第 2 条建议：", response)
        self.assertIn("/kb", response)

    def test_recent_advice_suggestions_survive_new_agent_instance(self):
        self.agent.handle("/experience-advice 导入资料")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("查看第一条建议")

        self.assertIn("第 1 条建议：", response)
        self.assertIn("/import 源文件或目录路径 [目标文件名]", response)

    def test_natural_language_prepare_and_confirm_executable_advice(self):
        self.agent.handle("/experience-advice 导入资料")

        prepare_response = self.agent.handle("执行第二条建议")
        confirm_response = self.agent.handle("确认执行")

        self.assertIn("准备执行第 2 条建议", prepare_response)
        self.assertIn("命令：/kb", prepare_response)
        self.assertIn("确认执行", prepare_response)
        self.assertIn("已确认执行建议命令：/kb", confirm_response)
        self.assertIn("个人知识库状态", confirm_response)

    def test_natural_language_prepare_advice_requires_completed_parameters(self):
        self.agent.handle("/experience-advice 导入资料")

        prepare_response = self.agent.handle("执行第一条建议")
        confirm_response = self.agent.handle("确认执行")

        self.assertIn("需要补充参数", prepare_response)
        self.assertIn("/import 源文件或目录路径 [目标文件名]", prepare_response)
        self.assertIn("还没有待确认的建议命令", confirm_response)

    def test_natural_language_prepare_advice_with_missing_parameters_returns_command_draft(self):
        self.agent.handle("/experience-advice 导入资料")

        prepare_response = self.agent.handle("执行第一条建议")
        confirm_response = self.agent.handle("确认执行")

        self.assertIn("需要补充参数", prepare_response)
        self.assertIn("命令草稿：/import <源文件或目录路径> [目标文件名]", prepare_response)
        self.assertIn("方括号参数可以按需保留或替换", prepare_response)
        self.assertIn("还没有待确认的建议命令", confirm_response)

    def test_completed_advice_command_draft_waits_for_confirmation(self):
        source = Path(self.temp_dir.name) / "draft-source.md"
        source.write_text("Jarvis Lite 可以确认执行补全后的建议命令。\n", encoding="utf-8")
        self.agent.handle("/experience-advice 导入资料")
        self.agent.handle("执行第一条建议")

        prepare_response = self.agent.handle(f"/import {source}")
        confirm_response = self.agent.handle("确认执行")

        self.assertIn("已补全建议命令，等待确认执行", prepare_response)
        self.assertIn(f"命令：/import {source}", prepare_response)
        self.assertNotIn("已导入知识库", prepare_response)
        self.assertIn(f"已确认执行建议命令：/import {source}", confirm_response)
        self.assertIn("已导入知识库：data/draft-source.md", confirm_response)

    def test_natural_language_confirm_advice_requires_pending_command(self):
        response = self.agent.handle("确认执行")

        self.assertIn("还没有待确认的建议命令", response)
        self.assertIn("执行第一条建议", response)

    def test_natural_language_read_advice_requires_recent_advice(self):
        response = self.agent.handle("查看第一条建议")

        self.assertIn("还没有最近建议", response)
        self.assertIn("我该怎么导入资料", response)

    def test_natural_language_experience_memory_status_maps_to_experiences(self):
        self.agent.handle("/experience 导入资料后先打标签")

        response = self.agent.handle("查看经验记忆")

        self.assertIn("经验记忆", response)
        self.assertIn("导入资料后先打标签", response)

    def test_natural_language_morning_greeting_uses_user_name_without_memory_fallback(self):
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 用户姓名：欧阳\n- 用户偏好：中文简洁回答\n",
            encoding="utf-8",
        )

        response = self.agent.handle("早上好")

        self.assertIn("早上好，欧阳", response)
        self.assertIn("Jarvis Lite", response)
        self.assertNotIn("已读取长期记忆", response)
        self.assertNotIn("输入 /help", response)

    def test_natural_language_assistant_name_question_answers_assistant_identity(self):
        response = self.agent.handle("你叫什么名字")

        self.assertIn("我叫 Jarvis Lite", response)
        self.assertIn("本地 PC 助手", response)
        self.assertNotIn("已读取长期记忆", response)
        self.assertNotIn("输入 /help", response)

    def test_natural_language_deletes_named_desktop_shortcuts_only(self):
        fake_home = Path(self.temp_dir.name) / "home"
        desktop = fake_home / "Desktop"
        desktop.mkdir(parents=True)
        cloud_shortcut = desktop / "比特云手机.lnk"
        browser_shortcut = desktop / "比特浏览器.lnk"
        protected_file = desktop / "比特浏览器.txt"
        cloud_shortcut.write_text("shortcut", encoding="utf-8")
        browser_shortcut.write_text("shortcut", encoding="utf-8")
        protected_file.write_text("not a shortcut", encoding="utf-8")

        with patch("jarvis_lite.agent.Path.home", return_value=fake_home):
            response = self.agent.handle("帮我把桌面上的比特云手机和比特浏览器的快捷方式删掉")

        self.assertIn("已删除桌面快捷方式", response)
        self.assertIn("比特云手机.lnk", response)
        self.assertIn("比特浏览器.lnk", response)
        self.assertFalse(cloud_shortcut.exists())
        self.assertFalse(browser_shortcut.exists())
        self.assertTrue(protected_file.exists())

    def test_inner_brain_seed_variant_executes_without_llm(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("麻烦看一下知识库摘要")

        self.assertIn("知识库摘要", response)
        self.assertEqual(provider.calls, [])
        self.assertNotIn("不应使用外脑", response)

    def test_inner_brain_runtime_sample_executes_without_llm(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "请打开我的资料库",
                    "intent": "knowledge.status",
                    "slots": {"command": "/kb"},
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("请打开我的资料库")

        self.assertIn("个人知识库状态", response)
        self.assertEqual(provider.calls, [])

    def test_inner_brain_low_confidence_still_uses_llm_fallback(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"外脑处理开放问题"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("火星基地预算需要外部判断")

        self.assertIn("LLM 外脑：外脑处理开放问题", response)
        self.assertEqual(len(provider.calls), 1)

    def test_inner_brain_clarification_includes_completion_and_training_hints(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "帮我导入这份资料",
                    "intent": "knowledge.import",
                    "slots": {},
                    "missing": ["source"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("帮我导入这份资料")

        self.assertIn("意图：knowledge.import", response)
        self.assertIn("需要补充：要导入的文件或目录", response)
        self.assertIn("可直接补充：/import 源文件或目录路径 [目标文件名]", response)
        self.assertIn("/inner-brain-label 原话 => knowledge.import source=文件或目录路径", response)
        self.assertIn("/inner-brain-teach 原话 => /命令", response)
        self.assertEqual(provider.calls, [])

    def test_inner_brain_clarification_accepts_followup_source_and_executes_import(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "帮我导入这份资料",
                    "intent": "knowledge.import",
                    "slots": {},
                    "missing": ["source"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        source = Path(self.temp_dir.name) / "followup-source.md"
        source.write_text("多轮澄清可以补齐导入路径。\n", encoding="utf-8")
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        clarify_response = agent.handle("帮我导入这份资料")
        followup_response = agent.handle(str(source))

        self.assertIn("需要补充：要导入的文件或目录", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("已导入知识库：data/followup-source.md", followup_response)
        self.assertTrue((self.paths.data_dir / "followup-source.md").exists())
        self.assertEqual(provider.calls, [])

    def test_inner_brain_clarification_accepts_followup_desktop_shortcut_name(self):
        fake_home = Path(self.temp_dir.name) / "home"
        desktop = fake_home / "Desktop"
        desktop.mkdir(parents=True)
        shortcut = desktop / "比特浏览器.lnk"
        shortcut.write_text("shortcut", encoding="utf-8")

        with patch("jarvis_lite.agent.Path.home", return_value=fake_home):
            clarify_response = self.agent.handle("删除桌面快捷方式")
            followup_response = self.agent.handle("比特浏览器")

        self.assertIn("需要补充：要处理的对象名称", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("已删除桌面快捷方式", followup_response)
        self.assertFalse(shortcut.exists())

    def test_inner_brain_clarification_accepts_followup_web_search_query(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "帮我联网查一下",
                    "intent": "web.search",
                    "slots": {},
                    "missing": ["query"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python current release", "https://python.example/current", "当前版本摘要。", "fake"),
            )
        )
        llm_provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake"), llm_provider),
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        clarify_response = agent.handle("帮我联网查一下")
        followup_response = agent.handle("Python 版本")

        self.assertIn("需要补充：查询关键词", clarify_response)
        self.assertIn("可直接补充：/search 关键词", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("联网搜索：Python 版本", followup_response)
        self.assertIn("Python current release", followup_response)
        self.assertEqual(search_provider.calls, ["Python 版本"])
        self.assertEqual(llm_provider.calls, [])

    def test_inner_brain_clarification_accepts_followup_web_search_summary_query(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "帮我联网总结一下",
                    "intent": "web.search_summarize",
                    "slots": {},
                    "missing": ["query"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
            )
        )
        llm_provider = FakeLLMProvider('{"type":"answer","answer":"Python 3.13 是当前发布线。"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake"), llm_provider),
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        clarify_response = agent.handle("帮我联网总结一下")
        followup_response = agent.handle("Python 版本")

        self.assertIn("需要补充：查询关键词", clarify_response)
        self.assertIn("可直接补充：/search-summary 关键词", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("联网搜索：Python 版本", followup_response)
        self.assertIn("LLM 外脑总结：Python 3.13 是当前发布线。", followup_response)
        self.assertEqual(search_provider.calls, ["Python 版本"])
        self.assertEqual(len(llm_provider.calls), 1)

    def test_inner_brain_clarification_accepts_followup_numbered_tags_without_polluting_tags(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "给那份资料打标签",
                    "intent": "document.tag_numbered_recent",
                    "slots": {},
                    "missing": ["result_index", "tags"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "manual.md").write_text(
            "第二份最近资料可被打标签。\n",
            encoding="utf-8",
        )
        agent = JarvisAgent(self.paths)
        agent.handle("/read manual.md")
        agent.handle("/read note.txt")

        clarify_response = agent.handle("给那份资料打标签")
        followup_response = agent.handle("第二份 项目 Python")
        kb_response = agent.handle("/kb")

        self.assertIn("需要补充：编号、标签", clarify_response)
        self.assertIn("可直接补充：请直接回复编号和标签，例如“第二份 项目 Python”", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("已更新标签：data/manual.md（项目、Python）", followup_response)
        self.assertIn("标签：项目、Python", kb_response)
        self.assertNotIn("标签：第二份", kb_response)

    def test_inner_brain_clarification_accepts_followup_directory_alias(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "打开那个常用位置",
                    "intent": "directory.open_alias",
                    "slots": {},
                    "missing": ["alias"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()
        agent = JarvisAgent(self.paths)
        agent.handle(f"/dir-add 项目 {target}")

        clarify_response = agent.handle("打开那个常用位置")
        followup_response = agent.handle("目录是项目")
        transcript_path = self.paths.logs_dir / "desktop-actions.txt"

        self.assertIn("需要补充：目录别名", clarify_response)
        self.assertIn("可直接补充：请直接回复目录别名，例如“项目”", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("已记录打开目录请求：项目", followup_response)
        self.assertTrue(transcript_path.is_file())
        transcript = transcript_path.read_text(encoding="utf-8")
        self.assertIn("open_directory", transcript)
        self.assertIn(str(target.resolve()), transcript)

    def test_inner_brain_clarification_accepts_followup_experience_content(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "记住这个经验",
                    "intent": "experience.record",
                    "slots": {},
                    "missing": ["experience"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        agent = JarvisAgent(self.paths)

        clarify_response = agent.handle("记住这个经验")
        followup_response = agent.handle("经验是导入资料后先打标签")
        experiences_response = agent.handle("/experiences")

        self.assertIn("需要补充：经验内容", clarify_response)
        self.assertIn("可直接补充：请直接回复经验内容，例如“导入资料后先打标签”", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("已记录经验：导入资料后先打标签", followup_response)
        self.assertIn("导入资料后先打标签", experiences_response)
        self.assertNotIn("经验是导入资料后先打标签", experiences_response)

    def test_inner_brain_clarification_accepts_followup_document_path(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "读取那个文件",
                    "intent": "document.read_path",
                    "slots": {},
                    "missing": ["path"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "note.txt").write_text("路径补槽资料。\n", encoding="utf-8")
        agent = JarvisAgent(self.paths)

        clarify_response = agent.handle("读取那个文件")
        followup_response = agent.handle("文件是 note.txt")

        self.assertIn("需要补充：文件路径", clarify_response)
        self.assertIn("可直接补充：请直接回复文件路径，例如“note.txt”", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("路径补槽资料。", followup_response)

    def test_inner_brain_clarification_accepts_followup_result_index_for_recent_document(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "读取那份资料",
                    "intent": "document.read_numbered_recent",
                    "slots": {},
                    "missing": ["result_index"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "manual.md").write_text("第二份资料内容。\n", encoding="utf-8")
        agent = JarvisAgent(self.paths)
        agent.handle("/read manual.md")
        agent.handle("/read note.txt")

        clarify_response = agent.handle("读取那份资料")
        followup_response = agent.handle("第二份")

        self.assertIn("需要补充：编号", clarify_response)
        self.assertIn("可直接补充：请补充编号，例如“第二份”", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("第 2 份资料：data/manual.md", followup_response)
        self.assertIn("第二份资料内容。", followup_response)

    def test_inner_brain_clarification_accepts_followup_tags_for_recent_document(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "给这个资料打标签",
                    "intent": "document.tag_recent",
                    "slots": {},
                    "missing": ["tags"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        agent = JarvisAgent(self.paths)
        agent.handle("/read note.txt")

        clarify_response = agent.handle("给这个资料打标签")
        followup_response = agent.handle("标签是项目 Python")
        kb_response = agent.handle("/kb")

        self.assertIn("需要补充：标签", clarify_response)
        self.assertIn("可直接补充：请直接回复标签，例如“项目 Python”", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("已更新标签：data/note.txt（项目、Python）", followup_response)
        self.assertIn("标签：项目、Python", kb_response)

    def test_inner_brain_clarification_accepts_followup_tag_group_alias_and_tags(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "给一组资料打标签",
                    "intent": "tag_group.preview_tagging",
                    "slots": {},
                    "missing": ["alias", "tags"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        agent = JarvisAgent(self.paths)
        agent.handle("/read note.txt")
        agent.handle("给这个资料打标签 项目")

        clarify_response = agent.handle("给一组资料打标签")
        followup_response = agent.handle("项目 归档")

        self.assertIn("需要补充：标签组、标签", clarify_response)
        self.assertIn("可直接补充：请直接回复标签组和新标签，例如“项目 归档”", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("批量打标签预览：项目标签资料", followup_response)
        self.assertIn("拟追加标签：归档", followup_response)
        self.assertNotIn("拟追加标签：项目、归档", followup_response)

    def test_inner_brain_clarification_accepts_followup_experience_search_query(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "帮我搜索经验",
                    "intent": "experience.search",
                    "slots": {},
                    "missing": ["query"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        agent = JarvisAgent(self.paths)
        agent.handle("/experience 导入资料后先打标签")

        clarify_response = agent.handle("帮我搜索经验")
        followup_response = agent.handle("关键词是导入资料")

        self.assertIn("需要补充：经验关键词", clarify_response)
        self.assertIn("可直接补充：请直接回复经验关键词，例如“导入资料”", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("经验搜索：导入资料", followup_response)
        self.assertIn("导入资料后先打标签", followup_response)

    def test_inner_brain_clarification_accepts_followup_experience_advice_query(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "给我一点操作思路",
                    "intent": "experience.advice",
                    "slots": {},
                    "missing": ["query"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        agent = JarvisAgent(self.paths)
        agent.handle("/experience 导入资料后先打标签")

        clarify_response = agent.handle("给我一点操作思路")
        followup_response = agent.handle("关键词是导入资料")

        self.assertIn("需要补充：经验关键词", clarify_response)
        self.assertIn("可直接补充：请直接回复经验关键词，例如“导入资料”", clarify_response)
        self.assertIn("已补齐缺失信息，继续执行。", followup_response)
        self.assertIn("操作建议：导入资料", followup_response)
        self.assertIn("导入资料后先打标签", followup_response)

    def test_inner_brain_clarification_can_be_cancelled(self):
        fake_home = Path(self.temp_dir.name) / "home"
        desktop = fake_home / "Desktop"
        desktop.mkdir(parents=True)
        shortcut = desktop / "比特浏览器.lnk"
        shortcut.write_text("shortcut", encoding="utf-8")

        with patch("jarvis_lite.agent.Path.home", return_value=fake_home):
            clarify_response = self.agent.handle("删除桌面快捷方式")
            cancel_response = self.agent.handle("取消补充")
            followup_response = self.agent.handle("比特浏览器")

        self.assertIn("需要补充：要处理的对象名称", clarify_response)
        self.assertIn("已取消这次补充", cancel_response)
        self.assertNotIn("已删除桌面快捷方式", followup_response)
        self.assertTrue(shortcut.exists())

    def test_natural_language_desktop_shortcut_delete_reports_missing_names(self):
        fake_home = Path(self.temp_dir.name) / "home"
        desktop = fake_home / "Desktop"
        desktop.mkdir(parents=True)
        existing_shortcut = desktop / "比特云手机.lnk"
        existing_shortcut.write_text("shortcut", encoding="utf-8")

        with patch("jarvis_lite.agent.Path.home", return_value=fake_home):
            response = self.agent.handle("删除桌面上的比特云手机和不存在的快捷方式")

        self.assertIn("已删除桌面快捷方式", response)
        self.assertIn("比特云手机.lnk", response)
        self.assertIn("未找到：不存在.lnk", response)
        self.assertFalse(existing_shortcut.exists())

    def test_natural_language_deletes_object_first_desktop_shortcut_expression(self):
        fake_home = Path(self.temp_dir.name) / "home"
        desktop = fake_home / "Desktop"
        desktop.mkdir(parents=True)
        shortcut = desktop / "比特浏览器.lnk"
        shortcut.write_text("shortcut", encoding="utf-8")
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        with patch("jarvis_lite.agent.Path.home", return_value=fake_home):
            response = agent.handle("把桌面快捷方式比特浏览器删掉")

        self.assertIn("已删除桌面快捷方式", response)
        self.assertIn("比特浏览器.lnk", response)
        self.assertFalse(shortcut.exists())
        self.assertEqual(provider.calls, [])

    def test_status_command_reports_current_capabilities(self):
        response = self.agent.handle("/status")

        self.assertIn("Jarvis Lite 当前状态", response)
        self.assertIn("长期记忆", response)
        self.assertIn("个人知识库", response)
        self.assertIn("工具日志", response)
        self.assertIn("自然语言", response)
        self.assertIn("桌面能力", response)
        self.assertIn("memory/profile.md", response)

    def test_help_command_lists_llm_usage_command(self):
        response = self.agent.handle("/help")

        self.assertIn("/llm-usage：查看 LLM token 用量汇总", response)
        self.assertIn("/llm-smoke [prompt]：强制调用 LLM 做一次配置验证", response)
        self.assertIn("/llm-context-preview：预览 LLM fallback 上下文，不调用 provider", response)
        self.assertIn("/llm-config-example [provider]：查看 LLM 环境变量配置模板", response)
        self.assertIn("/inner-brain-status：查看 InnerBrain 本地内脑状态", response)
        self.assertIn("/inner-brain-preview 文本：预览 InnerBrain 识别结果，不执行动作", response)
        self.assertIn("/inner-brain-adopt 文本：采纳 InnerBrain 识别结果为运行态样本", response)
        self.assertIn("/inner-brain-label 文本 => intent [slot=value ...]：人工标注 InnerBrain runtime 样本", response)
        self.assertIn("/inner-brain-teach 文本 => /命令：把自然语言短句教学为已知命令", response)
        self.assertIn("/llm-enable：查看外脑启用状态和本地配置路径", response)
        self.assertIn("/search-status：查看联网搜索 provider 状态", response)
        self.assertIn("/search 关键词：联网搜索并返回来源", response)

    def test_search_status_command_reports_default_disabled_state(self):
        response = self.agent.handle("/search-status")

        self.assertIn("联网搜索：未启用", response)
        self.assertIn("Provider：off", response)
        self.assertIn("网络调用：否（联网搜索未启用）", response)

    def test_search_command_returns_fake_provider_results(self):
        provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
            )
        )
        agent = JarvisAgent(
            self.paths,
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), provider),
        )

        response = agent.handle("/search Python 版本")

        self.assertIn("联网搜索：Python 版本", response)
        self.assertIn("1. Python 3.13 release", response)
        self.assertIn("URL：https://python.example/3-13", response)
        self.assertIn("摘要：Python 3.13 发布摘要。", response)
        self.assertEqual(provider.calls, ["Python 版本"])

    def test_search_command_reports_disabled_provider(self):
        response = self.agent.handle("/search Python 版本")

        self.assertIn("联网搜索未启用", response)
        self.assertIn("/search-enable", response)

    def test_search_smoke_command_reloads_local_config_without_recent_context(self):
        local_config = self.paths.config_dir / "search.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_results": [
                        {
                            "title": "Python current release",
                            "url": "https://python.example/current",
                            "snippet": "当前版本摘要。",
                        }
                    ],
                    "max_results": 5,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle("/search-smoke Python 版本")
        open_response = self.agent.handle("/search-open 1")
        context_response = self.agent.handle("查看最近上下文")

        self.assertIn("联网搜索 smoke：Python 版本", response)
        self.assertIn("这是一次 provider 连通性测试，可能发起真实网络调用。", response)
        self.assertIn("调用结果：成功，返回 1 条来源。", response)
        self.assertIn("1. Python current release", response)
        self.assertIn("URL：https://python.example/current", response)
        self.assertIn("摘要：当前版本摘要。", response)
        self.assertIn("smoke 不会写入最近联网搜索上下文。", response)
        self.assertIn("还没有最近联网搜索", open_response)
        self.assertNotIn("最近联网搜索：Python 版本", context_response)

    def test_search_smoke_command_reports_disabled_provider(self):
        response = self.agent.handle("/search-smoke Python 版本")

        self.assertIn("联网搜索 smoke：Python 版本", response)
        self.assertIn("调用结果：失败", response)
        self.assertIn("联网搜索未启用", response)
        self.assertIn("/search-config-check", response)

    def test_natural_language_web_search_uses_inner_brain_entry_without_llm(self):
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python current release", "https://python.example/current", "当前版本摘要。", "fake"),
            )
        )
        llm_provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake"), llm_provider),
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        response = agent.handle("联网查一下 Python 版本")

        self.assertIn("联网搜索：Python 版本", response)
        self.assertIn("Python current release", response)
        self.assertEqual(search_provider.calls, ["Python 版本"])
        self.assertEqual(llm_provider.calls, [])

    def test_search_command_records_web_results_in_recent_context_and_llm_context(self):
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
                SearchResult("Python downloads", "https://python.example/downloads", "Python 下载页。", "fake"),
            )
        )
        agent = JarvisAgent(
            self.paths,
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        search_response = agent.handle("/search Python 版本")
        recent_response = agent.handle("查看最近上下文")
        llm_context = agent.handle("/llm-context-preview")
        restarted_agent = JarvisAgent(self.paths)
        restarted_context = restarted_agent.handle("/llm-context-preview")

        self.assertIn("联网搜索：Python 版本", search_response)
        self.assertIn("最近联网搜索：Python 版本", recent_response)
        self.assertIn("Python 3.13 release", recent_response)
        self.assertIn("https://python.example/3-13", recent_response)
        self.assertIn("最近联网搜索：Python 版本", llm_context)
        self.assertIn("Python 3.13 发布摘要。", llm_context)
        self.assertIn("最近联网搜索：Python 版本", restarted_context)
        self.assertIn("https://python.example/downloads", restarted_context)

    def test_natural_language_web_search_summary_uses_search_results_as_llm_context(self):
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
            )
        )
        llm_provider = FakeLLMProvider('{"type":"answer","answer":"Python 3.13 是当前发布线。"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake"), llm_provider),
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        response = agent.handle("联网查一下 Python 版本并总结")

        self.assertIn("联网搜索：Python 版本", response)
        self.assertIn("Python 3.13 release", response)
        self.assertIn("LLM 外脑总结：Python 3.13 是当前发布线。", response)
        self.assertEqual(search_provider.calls, ["Python 版本"])
        self.assertEqual(len(llm_provider.calls), 1)
        llm_prompt, llm_context = llm_provider.calls[0]
        self.assertIn("总结", llm_prompt)
        self.assertIn("最近联网搜索：Python 版本", "\n".join(llm_context))
        self.assertIn("https://python.example/3-13", "\n".join(llm_context))

    def test_search_summary_reports_llm_disabled_without_crashing(self):
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
            )
        )
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="off")),
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        response = agent.handle("/search-summary Python 版本")

        self.assertIn("联网搜索：Python 版本", response)
        self.assertIn("Python 3.13 release", response)
        self.assertIn("LLM 外脑未返回总结", response)
        self.assertIn("/llm-status", response)
        self.assertEqual(search_provider.calls, ["Python 版本"])

    def test_natural_language_opens_numbered_recent_web_search_source_without_browser_launch(self):
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
                SearchResult("Python downloads", "https://python.example/downloads", "Python 下载页。", "fake"),
            )
        )
        agent = JarvisAgent(
            self.paths,
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        agent.handle("/search Python 版本")
        response = agent.handle("打开第二条联网搜索结果")

        self.assertIn("联网搜索来源 2：Python downloads", response)
        self.assertIn("URL：https://python.example/downloads", response)
        self.assertIn("当前不会启动浏览器", response)

    def test_search_compare_recent_sources_uses_llm_context(self):
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
                SearchResult("Python downloads", "https://python.example/downloads", "Python 下载页。", "fake"),
            )
        )
        llm_provider = FakeLLMProvider('{"type":"answer","answer":"第一个来源偏发布信息，第二个来源偏下载入口。"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake"), llm_provider),
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        agent.handle("/search Python 版本")
        response = agent.handle("比较一下这些联网来源")

        self.assertIn("LLM 外脑比较：第一个来源偏发布信息，第二个来源偏下载入口。", response)
        self.assertEqual(len(llm_provider.calls), 1)
        llm_prompt, llm_context = llm_provider.calls[0]
        self.assertIn("比较", llm_prompt)
        self.assertIn("最近联网搜索：Python 版本", "\n".join(llm_context))

    def test_search_save_summary_writes_word_summary_from_recent_web_search(self):
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
            )
        )
        llm_provider = FakeLLMProvider('{"type":"answer","answer":"Python 3.13 是当前发布线。"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake"), llm_provider),
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        agent.handle("/search Python 版本")
        response = agent.handle("/search-save-summary python-version")

        summary_path = self.paths.word_dir / "python-version.md"
        self.assertIn("已保存联网搜索摘要：word/python-version.md", response)
        self.assertTrue(summary_path.is_file())
        content = summary_path.read_text(encoding="utf-8")
        self.assertIn("Python 3.13 是当前发布线。", content)
        self.assertIn("https://python.example/3-13", content)

    def test_search_import_summary_writes_data_document_and_updates_recent_document(self):
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
            )
        )
        llm_provider = FakeLLMProvider('{"type":"answer","answer":"Python 3.13 是当前发布线。"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake"), llm_provider),
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        agent.handle("/search Python 版本")
        response = agent.handle("导入这个搜索摘要到知识库")
        read_response = agent.handle("读取这个资料")

        self.assertIn("已导入联网搜索摘要：data/web-search-python-版本.md", response)
        self.assertTrue((self.paths.data_dir / "web-search-python-版本.md").is_file())
        self.assertIn("联网搜索摘要：Python 版本", read_response)
        self.assertIn("Python 3.13 是当前发布线。", read_response)

    def test_search_enable_command_reports_local_config_path_without_api_key(self):
        local_config = self.paths.config_dir / "search.local.json"
        local_config.write_text(
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
        agent = JarvisAgent(self.paths)

        response = agent.handle("/search-enable")

        self.assertIn("联网搜索启用入口", response)
        self.assertIn("联网搜索：已启用", response)
        self.assertIn("配置文件：config/search.local.json", response)
        self.assertIn("模板文件：config/search.example.json", response)
        self.assertIn("API key：已配置", response)
        self.assertNotIn("secret-search-key", response)

    def test_search_config_init_creates_tavily_local_config_draft_without_api_key(self):
        response = self.agent.handle("/search-config-init tavily")

        local_config = self.paths.config_dir / "search.local.json"
        payload = json.loads(local_config.read_text(encoding="utf-8"))
        enable_response = self.agent.handle("/search-enable")

        self.assertIn("已生成联网搜索本地配置草稿：config/search.local.json", response)
        self.assertIn("Provider：tavily", response)
        self.assertIn("下一步：填入 api_key 后执行 /search-enable", response)
        self.assertEqual(payload["provider"], "tavily")
        self.assertEqual(payload["api_key"], "")
        self.assertEqual(payload["base_url"], "")
        self.assertEqual(payload["max_results"], 5)
        self.assertEqual(payload["fake_results"], [])
        self.assertIn("缺少 JARVIS_LITE_SEARCH_API_KEY", enable_response)
        self.assertIn("网络调用：否（配置未完成）", enable_response)

    def test_search_config_check_reads_current_local_config_without_api_key_or_network(self):
        local_config = self.paths.config_dir / "search.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "tavily",
                    "api_key": "secret-search-key",
                    "base_url": "https://search.example/api",
                    "max_results": 3,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle("/search-config-check")

        self.assertIn("联网搜索配置检查：", response)
        self.assertIn("配置文件：config/search.local.json", response)
        self.assertIn("本地配置：存在", response)
        self.assertIn("联网搜索：已启用", response)
        self.assertIn("Provider：tavily", response)
        self.assertIn("Max results：3", response)
        self.assertIn("API key：已配置", response)
        self.assertIn("检查方式：只读取本地配置和环境变量，不发起网络请求。", response)
        self.assertIn("结果：配置完整，可执行 /search-enable 或 /search 关键词。", response)
        self.assertNotIn("secret-search-key", response)

    def test_search_config_set_writes_local_config_without_leaking_api_key(self):
        response = self.agent.handle("/search-config-set provider=tavily api_key=secret-search-key max_results=3")

        local_config = self.paths.config_dir / "search.local.json"
        payload = json.loads(local_config.read_text(encoding="utf-8"))
        check_response = self.agent.handle("/search-config-check")
        log_text = self.paths.log_path.read_text(encoding="utf-8")

        self.assertIn("已写入联网搜索本地配置：config/search.local.json", response)
        self.assertIn("变更字段：provider、api_key、max_results", response)
        self.assertIn("/search-config-check", response)
        self.assertEqual(payload["provider"], "tavily")
        self.assertEqual(payload["api_key"], "secret-search-key")
        self.assertEqual(payload["max_results"], 3)
        self.assertIn("联网搜索：已启用", check_response)
        self.assertIn("API key：已配置", check_response)
        self.assertIn("结果：配置完整，可执行 /search-enable 或 /search 关键词。", check_response)
        self.assertNotIn("secret-search-key", response)
        self.assertNotIn("secret-search-key", check_response)
        self.assertNotIn("secret-search-key", log_text)

    def test_search_config_set_rejects_invalid_max_results_without_partial_write(self):
        response = self.agent.handle("/search-config-set provider=tavily max_results=0")

        self.assertIn("max_results 必须是大于 0 的整数", response)
        self.assertFalse((self.paths.config_dir / "search.local.json").exists())

    def test_agent_reads_llm_local_config_file_on_startup(self):
        local_config = self.paths.config_dir / "llm.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_response": "{\"type\":\"answer\",\"answer\":\"本地配置外脑已接入\"}",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        agent = JarvisAgent(self.paths)
        response = agent.handle("这句话需要外脑理解")

        self.assertIn("LLM 外脑：本地配置外脑已接入", response)

    def test_llm_enable_command_reports_local_config_path_without_api_key(self):
        local_config = self.paths.config_dir / "llm.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "openai-compatible",
                    "model": "compatible-model",
                    "base_url": "https://compatible.example/v1/responses",
                    "api_key": "secret-local-key",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        agent = JarvisAgent(self.paths)

        response = agent.handle("/llm-enable")

        self.assertIn("LLM 外脑：已启用", response)
        self.assertIn("配置文件：config/llm.local.json", response)
        self.assertIn("API key：已配置", response)
        self.assertIn("/llm-smoke", response)
        self.assertNotIn("secret-local-key", response)

    def test_llm_config_init_creates_qwen_local_config_draft_without_api_key(self):
        response = self.agent.handle("/llm-config-init qwen")

        local_config = self.paths.config_dir / "llm.local.json"
        payload = json.loads(local_config.read_text(encoding="utf-8"))
        enable_response = self.agent.handle("/llm-enable")

        self.assertIn("已生成外脑本地配置草稿：config/llm.local.json", response)
        self.assertIn("Provider：qwen", response)
        self.assertIn("Adapter：openai-compatible", response)
        self.assertIn("下一步：填入 model、base_url、api_key 后执行 /llm-enable", response)
        self.assertEqual(payload["provider"], "qwen")
        self.assertEqual(payload["model"], "")
        self.assertEqual(payload["base_url"], "")
        self.assertEqual(payload["api_key"], "")
        self.assertEqual(payload["fake_response"], "")
        self.assertIn("缺少 JARVIS_LITE_LLM_MODEL", enable_response)
        self.assertIn("缺少 JARVIS_LITE_LLM_API_KEY", enable_response)
        self.assertIn("缺少 JARVIS_LITE_LLM_BASE_URL", enable_response)
        self.assertIn("网络调用：否（配置未完成）", enable_response)

    def test_llm_config_check_reads_current_local_config_without_api_key_or_network(self):
        local_config = self.paths.config_dir / "llm.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "qwen",
                    "model": "qwen-test",
                    "base_url": "https://qwen.example/v1/responses",
                    "api_key": "secret-existing-key",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle("/llm-config-check")

        self.assertIn("外脑配置检查：", response)
        self.assertIn("配置文件：config/llm.local.json", response)
        self.assertIn("本地配置：存在", response)
        self.assertIn("LLM 外脑：已启用", response)
        self.assertIn("Provider：qwen", response)
        self.assertIn("Adapter：openai-compatible", response)
        self.assertIn("Model：qwen-test", response)
        self.assertIn("SDK Base URL：https://qwen.example/v1", response)
        self.assertIn("API key：已配置", response)
        self.assertIn("检查方式：只读取本地配置和环境变量，不发起网络请求。", response)
        self.assertIn("结果：配置完整，可执行 /llm-enable 或 /llm-smoke。", response)
        self.assertNotIn("secret-existing-key", response)

    def test_llm_config_set_writes_local_config_without_leaking_api_key(self):
        response = self.agent.handle(
            "/llm-config-set "
            "provider=qwen "
            "model=qwen-plus "
            "base_url=https://qwen.example/v1/responses "
            "api_key=secret-existing-key"
        )

        local_config = self.paths.config_dir / "llm.local.json"
        payload = json.loads(local_config.read_text(encoding="utf-8"))
        check_response = self.agent.handle("/llm-config-check")
        log_text = self.paths.log_path.read_text(encoding="utf-8")

        self.assertIn("已写入外脑本地配置：config/llm.local.json", response)
        self.assertIn("变更字段：provider、model、base_url、api_key", response)
        self.assertIn("/llm-config-check", response)
        self.assertEqual(payload["provider"], "qwen")
        self.assertEqual(payload["model"], "qwen-plus")
        self.assertEqual(payload["base_url"], "https://qwen.example/v1/responses")
        self.assertEqual(payload["api_key"], "secret-existing-key")
        self.assertIn("LLM 外脑：已启用", check_response)
        self.assertIn("Provider：qwen", check_response)
        self.assertIn("Adapter：openai-compatible", check_response)
        self.assertIn("Model：qwen-plus", check_response)
        self.assertIn("API key：已配置", check_response)
        self.assertIn("结果：配置完整，可执行 /llm-enable 或 /llm-smoke。", check_response)
        self.assertNotIn("secret-existing-key", response)
        self.assertNotIn("secret-existing-key", check_response)
        self.assertNotIn("secret-existing-key", log_text)

    def test_llm_config_set_preserves_unspecified_existing_fields(self):
        local_config = self.paths.config_dir / "llm.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "qwen",
                    "model": "old-model",
                    "base_url": "https://qwen.example/v1/responses",
                    "api_key": "secret-existing-key",
                    "fake_response": "",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle("/llm-config-set model=qwen-max")
        payload = json.loads(local_config.read_text(encoding="utf-8"))

        self.assertIn("变更字段：model", response)
        self.assertEqual(payload["provider"], "qwen")
        self.assertEqual(payload["model"], "qwen-max")
        self.assertEqual(payload["base_url"], "https://qwen.example/v1/responses")
        self.assertEqual(payload["api_key"], "secret-existing-key")
        self.assertNotIn("secret-existing-key", response)

    def test_llm_config_set_rejects_invalid_provider_without_partial_write(self):
        local_config = self.paths.config_dir / "llm.local.json"
        original_payload = {
            "provider": "qwen",
            "model": "qwen-test",
            "base_url": "https://qwen.example/v1/responses",
            "api_key": "secret-existing-key",
        }
        local_config.write_text(json.dumps(original_payload, ensure_ascii=False), encoding="utf-8")

        response = self.agent.handle("/llm-config-set provider=unknown")
        payload = json.loads(local_config.read_text(encoding="utf-8"))

        self.assertIn("暂不支持 LLM provider：unknown", response)
        self.assertEqual(payload, original_payload)
        self.assertNotIn("secret-existing-key", response)

    def test_llm_config_check_reports_invalid_json(self):
        local_config = self.paths.config_dir / "llm.local.json"
        local_config.write_text("{invalid-json", encoding="utf-8")

        response = self.agent.handle("/llm-config-check")

        self.assertIn("外脑配置检查：", response)
        self.assertIn("本地配置：存在", response)
        self.assertIn("不是有效 JSON", response)
        self.assertIn("结果：配置未完成，修正后执行 /llm-enable。", response)

    def test_llm_config_init_does_not_overwrite_existing_local_config_or_leak_key(self):
        local_config = self.paths.config_dir / "llm.local.json"
        original_payload = {
            "provider": "qwen",
            "model": "qwen-test",
            "base_url": "https://qwen.example/v1/responses",
            "api_key": "secret-existing-key",
        }
        local_config.write_text(json.dumps(original_payload, ensure_ascii=False), encoding="utf-8")

        response = self.agent.handle("/llm-config-init gemini")
        payload = json.loads(local_config.read_text(encoding="utf-8"))

        self.assertEqual(payload, original_payload)
        self.assertIn("外脑本地配置已存在：config/llm.local.json", response)
        self.assertIn("未覆盖已有配置", response)
        self.assertIn("/llm-enable", response)
        self.assertNotIn("secret-existing-key", response)

    def test_natural_language_config_init_uses_inner_brain_entries(self):
        llm_response = self.agent.handle("生成外脑配置")
        search_response = self.agent.handle("生成联网搜索配置")

        self.assertTrue((self.paths.config_dir / "llm.local.json").is_file())
        self.assertTrue((self.paths.config_dir / "search.local.json").is_file())
        self.assertIn("已生成外脑本地配置草稿", llm_response)
        self.assertIn("已生成联网搜索本地配置草稿", search_response)

    def test_natural_language_config_check_uses_inner_brain_entries(self):
        llm_response = self.agent.handle("检查外脑配置")
        search_response = self.agent.handle("检查联网搜索配置")

        self.assertIn("外脑配置检查：", llm_response)
        self.assertIn("联网搜索配置检查：", search_response)
        self.assertIn("检查方式：只读取本地配置和环境变量，不发起网络请求。", llm_response)
        self.assertIn("检查方式：只读取本地配置和环境变量，不发起网络请求。", search_response)

    def test_natural_language_config_set_uses_inner_brain_entries_for_usage(self):
        llm_response = self.agent.handle("设置外脑配置")
        search_response = self.agent.handle("设置联网搜索配置")

        self.assertIn("用法：/llm-config-set key=value ...", llm_response)
        self.assertIn("用法：/search-config-set key=value ...", search_response)
        self.assertFalse((self.paths.config_dir / "llm.local.json").exists())
        self.assertFalse((self.paths.config_dir / "search.local.json").exists())

    def test_natural_language_enable_llm_uses_inner_brain_entry(self):
        response = self.agent.handle("开启外脑")

        self.assertIn("外脑启用入口", response)
        self.assertIn("配置文件：config/llm.local.json", response)
        self.assertIn("模板文件：config/llm.example.json", response)
        self.assertIn("/llm-status", response)
        self.assertNotIn("已读取长期记忆", response)

    def test_enable_llm_reloads_local_config_during_running_session(self):
        local_config = self.paths.config_dir / "llm.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_response": "{\"type\":\"answer\",\"answer\":\"运行中已重新接入外脑\"}",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        enable_response = self.agent.handle("开启外脑")
        llm_response = self.agent.handle("这句话需要外脑判断")

        self.assertIn("LLM 外脑：已启用", enable_response)
        self.assertIn("Provider：fake", enable_response)
        self.assertIn("再次执行 /llm-enable", enable_response)
        self.assertIn("LLM 外脑：运行中已重新接入外脑", llm_response)

    def test_enable_llm_reports_qwen_alias_adapter_from_local_config(self):
        local_config = self.paths.config_dir / "llm.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "qwen",
                    "model": "qwen-test",
                    "base_url": "https://qwen.example/v1/responses",
                    "api_key": "secret-qwen-key",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle("/llm-enable")

        self.assertIn("LLM 外脑：已启用", response)
        self.assertIn("Provider：qwen", response)
        self.assertIn("Adapter：openai-compatible", response)
        self.assertIn("SDK Base URL：https://qwen.example/v1", response)
        self.assertIn("网络调用：是", response)
        self.assertNotIn("secret-qwen-key", response)

    def test_inner_brain_status_command_reports_samples_and_thresholds(self):
        response = self.agent.handle("/inner-brain-status")

        self.assertIn("InnerBrain 状态", response)
        self.assertIn("样本分类器：启用（优先）", response)
        self.assertIn("legacy_fallback：启用（仅迁移期兼容）", response)
        self.assertNotIn("legacy_rule：启用", response)
        self.assertRegex(response, r"seed_sample：\d+ 条")
        self.assertIn("高置信阈值：0.78", response)

    def test_inner_brain_eval_command_reports_repeatable_seed_baseline(self):
        response = self.agent.handle("/inner-brain-eval")

        self.assertIn("InnerBrain 评估", response)
        self.assertIn("评估集：seed_evaluation", response)
        self.assertRegex(response, r"通过：\d+/\d+")
        self.assertIn("失败：0", response)
        self.assertIn("帮我看一下知识库状态 -> knowledge.status", response)
        self.assertNotIn("未知命令", response)

    def test_inner_brain_eval_command_includes_local_evaluation_cases_without_training(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "real-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval")

        self.assertIn("评估集：seed_evaluation+local_evaluation", response)
        self.assertIn("local_evaluation：1 条", response)
        self.assertIn("请看看资料库状态 -> knowledge.status", response)
        self.assertIn("失败：0", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_command_suggests_explicit_training_for_failed_local_cases(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval")

        self.assertIn("失败：1", response)
        self.assertIn("失败修复建议：", response)
        self.assertIn("请看看资料库状态：/inner-brain-teach 请看看资料库状态 => /kb-summary", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_failed_command_lists_only_failed_cases(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval-failed")

        self.assertIn("失败样例：", response)
        self.assertNotIn("PASS 早上好", response)
        self.assertNotIn("早上好 -> assistant.greeting", response)
        self.assertIn("FAIL 请看看资料库状态 -> knowledge.status", response)
        self.assertIn("失败修复建议：", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_local_command_lists_only_local_cases(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "real-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval-local")

        self.assertIn("评估集：local_evaluation", response)
        self.assertIn("local_evaluation：1 条", response)
        self.assertIn("请看看资料库状态 -> knowledge.status", response)
        self.assertNotIn("seed_evaluation：", response)
        self.assertNotIn("早上好 -> assistant.greeting", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_local_failed_command_guides_empty_local_evaluation_samples(self):
        response = self.agent.handle("/inner-brain-eval-local-failed")

        self.assertIn("评估集：local_evaluation", response)
        self.assertIn("本机评估样本：", response)
        self.assertIn("- 无", response)
        self.assertIn("添加本机评估样本：", response)
        self.assertIn("- /inner-brain-eval-add 文本 => /命令", response)
        self.assertIn("- /inner-brain-eval-label 文本 => intent [slot=value ...]", response)
        self.assertIn("说明：这些命令只写入本机 evaluation 样本，不自动训练。", response)
        self.assertNotIn("导出本机失败报告", response)
        self.assertNotIn("按文件聚焦失败", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_local_failed_command_lists_only_failed_local_cases(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval-local-failed")

        self.assertIn("评估集：local_evaluation", response)
        self.assertIn("失败样例：", response)
        self.assertNotIn("PASS 早上好", response)
        self.assertNotIn("早上好 -> assistant.greeting", response)
        self.assertIn("FAIL 请看看资料库状态 -> knowledge.status", response)
        self.assertIn("失败修复建议：", response)
        self.assertIn("后续处理：", response)
        self.assertIn("- 按文件聚焦失败：/inner-brain-eval-local-file-failed 文件名", response)
        self.assertIn("- 导出本机失败报告：/inner-brain-eval-local-report", response)
        self.assertIn("- 按文件导出失败报告：/inner-brain-eval-local-report 文件名", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_local_failed_command_groups_failures_by_local_file(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "real-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval-local-failed")

        self.assertIn("失败文件：", response)
        self.assertIn("- failed-log.jsonl：1 条", response)
        self.assertNotIn("- real-log.jsonl：", response)
        self.assertIn("FAIL 请看看资料库状态 -> knowledge.status", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_local_file_command_lists_only_selected_local_file_cases(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "real-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval-local-file real-log.jsonl")

        self.assertIn("评估集：local_evaluation:real-log.jsonl", response)
        self.assertIn("评估文件：real-log.jsonl", response)
        self.assertIn("通过：1/1", response)
        self.assertIn("请看看资料库状态 -> knowledge.status", response)
        self.assertNotIn("FAIL 请看看资料库状态", response)
        self.assertNotIn("seed_evaluation：", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "real-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval-local-file-failed failed-log.jsonl")

        self.assertIn("评估集：local_evaluation:failed-log.jsonl", response)
        self.assertIn("评估文件：failed-log.jsonl", response)
        self.assertIn("失败样例：", response)
        self.assertIn("FAIL 请看看资料库状态 -> knowledge.status", response)
        self.assertNotIn("PASS 请看看资料库状态", response)
        self.assertIn("失败修复建议：", response)
        self.assertIn("后续处理：", response)
        self.assertIn("- 查看全部本机失败样本：/inner-brain-eval-local-failed", response)
        self.assertIn("- 导出当前文件失败报告：/inner-brain-eval-local-report failed-log.jsonl", response)
        self.assertIn("- 导出全部本机失败报告：/inner-brain-eval-local-report", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval-local-report")

        report_path = self.paths.word_dir / "inner-brain-evaluation-report.md"
        self.assertIn("已导出 InnerBrain 本机评估失败报告。", response)
        self.assertIn("报告文件：word/inner-brain-evaluation-report.md", response)
        self.assertIn("失败样本：1", response)
        self.assertIn("后续处理：", response)
        self.assertIn("- 查看本机失败样本：/inner-brain-eval-local-failed", response)
        self.assertIn("- 按文件聚焦失败：/inner-brain-eval-local-file-failed 文件名", response)
        self.assertIn("- 补命令评估样本：/inner-brain-eval-add 文本 => /命令", response)
        self.assertIn("- 补意图评估样本：/inner-brain-eval-label 文本 => intent [slot=value ...]", response)
        content = report_path.read_text(encoding="utf-8")
        self.assertIn("失败文件：", content)
        self.assertIn("- failed-log.jsonl：1 条", content)
        self.assertIn("失败类型汇总：", content)
        self.assertIn("- 命令不匹配：1 条", content)
        self.assertIn("- 意图不匹配：1 条", content)
        self.assertIn("失败期望意图汇总：", content)
        self.assertIn("- knowledge.summary：1 条", content)
        self.assertIn("失败意图混淆汇总：", content)
        self.assertIn("- knowledge.summary -> knowledge.status：1 条", content)
        self.assertIn("失败文件意图混淆汇总：", content)
        self.assertIn("- failed-log.jsonl：knowledge.summary -> knowledge.status：1 条", content)
        self.assertIn("失败意图混淆修复建议：", content)
        self.assertIn("  - 请看看资料库状态：/inner-brain-teach 请看看资料库状态 => /kb-summary", content)
        self.assertIn("失败文件意图混淆修复建议：", content)
        self.assertIn("- failed-log.jsonl：knowledge.summary -> knowledge.status：1 条", content)
        self.assertIn("失败原因汇总：", content)
        self.assertIn("意图期望 knowledge.summary，实际 knowledge.status；命令期望 /kb-summary，实际 /kb：1 条", content)
        self.assertIn("FAIL 请看看资料库状态 -> knowledge.status", content)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_local_report_command_can_filter_local_file(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "real-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/inner-brain-eval-local-report failed-log")

        report_path = self.paths.word_dir / "inner-brain-evaluation-report.md"
        self.assertIn("已导出 InnerBrain 本机评估失败报告。", response)
        self.assertIn("评估文件：failed-log.jsonl", response)
        self.assertIn("后续处理：", response)
        self.assertIn("- 复查当前文件失败样本：/inner-brain-eval-local-file-failed failed-log.jsonl", response)
        self.assertIn("- 查看全部本机失败样本：/inner-brain-eval-local-failed", response)
        self.assertTrue(report_path.exists())
        content = report_path.read_text(encoding="utf-8")
        self.assertIn("评估文件：failed-log.jsonl", content)
        self.assertIn("FAIL 请看看资料库状态 -> knowledge.status", content)
        self.assertNotIn("- real-log.jsonl：", content)
        self.assertNotIn("失败文件意图混淆修复建议：", content)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_add_command_saves_local_evaluation_case_without_training(self):
        response = self.agent.handle("/inner-brain-eval-add 请看看资料库状态 => /kb")

        self.assertIn("已保存 InnerBrain 本机评估样本", response)
        self.assertIn("样本文件：data/inner-brain/evaluation/runtime.jsonl", response)
        self.assertIn("目标命令：/kb", response)
        self.assertIn("后续验证：", response)
        self.assertIn("- 复跑本机评估：/inner-brain-eval-local", response)
        self.assertIn("- 只看失败样本：/inner-brain-eval-local-failed", response)
        self.assertIn("- 聚焦样本文件：/inner-brain-eval-local-file runtime.jsonl", response)
        self.assertIn("- 导出失败报告：/inner-brain-eval-local-report", response)
        sample_file = self.paths.data_dir / "inner-brain" / "evaluation" / "runtime.jsonl"
        payload = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertEqual(payload["text"], "请看看资料库状态")
        self.assertEqual(payload["expected_intent"], "knowledge.status")
        self.assertEqual(payload["expected_command"], "/kb")
        local_eval_response = self.agent.handle("/inner-brain-eval-local")
        self.assertIn("评估集：local_evaluation", local_eval_response)
        self.assertIn("请看看资料库状态 -> knowledge.status", local_eval_response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_label_command_saves_local_evaluation_case_without_training(self):
        response = self.agent.handle("/inner-brain-eval-label 请看看资料库状态 => knowledge.status command=/kb")

        self.assertIn("已保存 InnerBrain 本机评估样本", response)
        self.assertIn("意图：knowledge.status", response)
        self.assertIn("目标命令：/kb", response)
        sample_file = self.paths.data_dir / "inner-brain" / "evaluation" / "runtime.jsonl"
        payload = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertEqual(payload["text"], "请看看资料库状态")
        self.assertEqual(payload["expected_intent"], "knowledge.status")
        self.assertEqual(payload["expected_command"], "/kb")
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_eval_add_rejects_unknown_command_without_writing_case(self):
        response = self.agent.handle("/inner-brain-eval-add 打开未知工具 => /unknown-command")

        self.assertIn("教学目标不是已知命令：/unknown-command", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "evaluation" / "runtime.jsonl").exists())
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_preview_command_reports_result_without_execution(self):
        response = self.agent.handle("/inner-brain-preview 麻烦看一下知识库摘要")

        self.assertIn("InnerBrain 预览", response)
        self.assertIn("意图：knowledge.summary", response)
        self.assertIn("命令：/kb-summary", response)
        self.assertIn("说明：这里只预览识别结果，不执行命令。", response)
        self.assertNotIn("资料文件：", response)

    def test_inner_brain_preview_does_not_delete_desktop_shortcut(self):
        fake_home = Path(self.temp_dir.name) / "home"
        desktop = fake_home / "Desktop"
        desktop.mkdir(parents=True)
        shortcut = desktop / "比特浏览器.lnk"
        shortcut.write_text("shortcut", encoding="utf-8")

        with patch("jarvis_lite.agent.Path.home", return_value=fake_home):
            response = self.agent.handle("/inner-brain-preview 把桌面比特浏览器快捷方式删除")

        self.assertIn("InnerBrain 预览", response)
        self.assertIn("意图：desktop.delete_shortcut", response)
        self.assertIn("对象：比特浏览器", response)
        self.assertTrue(shortcut.exists())

    def test_inner_brain_adopt_command_saves_runtime_sample_and_refreshes_status(self):
        response = self.agent.handle("/inner-brain-adopt 帮我看看资料库状态")
        status = self.agent.handle("/inner-brain-status")
        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())

        self.assertIn("已保存 InnerBrain runtime 样本", response)
        self.assertIn("意图：knowledge.status", response)
        self.assertIn("样本文件：data/inner-brain/training/runtime.jsonl", response)
        self.assertIn("runtime_sample：1 条", status)
        self.assertEqual(saved_sample["text"], "帮我看看资料库状态")
        self.assertEqual(saved_sample["intent"], "knowledge.status")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})

    def test_inner_brain_adopt_command_skips_duplicate_sample(self):
        self.agent.handle("/inner-brain-adopt 帮我看看资料库状态")

        response = self.agent.handle("/inner-brain-adopt 帮我看看资料库状态")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        self.assertIn("样本已存在", response)
        self.assertEqual(len(sample_file.read_text(encoding="utf-8").splitlines()), 1)

    def test_inner_brain_adopt_command_rejects_unknown_result(self):
        response = self.agent.handle("/inner-brain-adopt 火星基地预算需要外部判断")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        self.assertIn("无法保存 InnerBrain 样本", response)
        self.assertIn("unknown", response)
        self.assertFalse(sample_file.exists())

    def test_inner_brain_adopt_does_not_delete_desktop_shortcut(self):
        fake_home = Path(self.temp_dir.name) / "home"
        desktop = fake_home / "Desktop"
        desktop.mkdir(parents=True)
        shortcut = desktop / "比特浏览器.lnk"
        shortcut.write_text("shortcut", encoding="utf-8")

        with patch("jarvis_lite.agent.Path.home", return_value=fake_home):
            response = self.agent.handle("/inner-brain-adopt 把桌面比特浏览器快捷方式删除")

        saved_sample = json.loads(
            (self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").read_text(encoding="utf-8").strip()
        )
        self.assertIn("已保存 InnerBrain runtime 样本", response)
        self.assertIn("意图：desktop.delete_shortcut", response)
        self.assertEqual(saved_sample["slots"], {"items": ["比特浏览器"]})
        self.assertTrue(shortcut.exists())

    def test_inner_brain_label_command_saves_unknown_prompt_and_refreshes_current_agent(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        label_response = agent.handle("/inner-brain-label 可以看看资料库吗 => knowledge.status command=/kb")
        status = agent.handle("/inner-brain-status")
        followup = agent.handle("可以看看资料库吗")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 人工标注样本", label_response)
        self.assertIn("意图：knowledge.status", label_response)
        self.assertIn("槽位 command：/kb", label_response)
        self.assertIn("runtime_sample：1 条", status)
        self.assertEqual(saved_sample["text"], "可以看看资料库吗")
        self.assertEqual(saved_sample["intent"], "knowledge.status")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})
        self.assertIn("个人知识库状态", followup)
        self.assertEqual(provider.calls, [])

    def test_inner_brain_label_command_requires_arrow_and_intent(self):
        response = self.agent.handle("/inner-brain-label 可以看看资料库吗 knowledge.status command=/kb")

        self.assertIn("用法：/inner-brain-label 文本 => intent [slot=value ...]", response)

    def test_inner_brain_label_command_rejects_invalid_slot_assignment(self):
        response = self.agent.handle("/inner-brain-label 可以看看资料库吗 => knowledge.status command")

        self.assertIn("标注参数错误", response)
        self.assertIn("slot 必须使用 key=value", response)

    def test_inner_brain_label_does_not_delete_desktop_shortcut(self):
        fake_home = Path(self.temp_dir.name) / "home"
        desktop = fake_home / "Desktop"
        desktop.mkdir(parents=True)
        shortcut = desktop / "比特浏览器.lnk"
        shortcut.write_text("shortcut", encoding="utf-8")

        with patch("jarvis_lite.agent.Path.home", return_value=fake_home):
            response = self.agent.handle(
                "/inner-brain-label 随手删掉这个快捷方式 => desktop.delete_shortcut items=比特浏览器"
            )

        saved_sample = json.loads(
            (self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").read_text(encoding="utf-8").strip()
        )
        self.assertIn("已保存 InnerBrain 人工标注样本", response)
        self.assertEqual(saved_sample["slots"], {"items": ["比特浏览器"]})
        self.assertTrue(shortcut.exists())

    def test_inner_brain_teach_command_saves_command_sample_and_refreshes_current_agent(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        teach_response = agent.handle("/inner-brain-teach 可以看看资料库吗 => /kb")
        status = agent.handle("/inner-brain-status")
        followup = agent.handle("可以看看资料库吗")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 教学样本", teach_response)
        self.assertIn("目标命令：/kb", teach_response)
        self.assertIn("说明：这里只保存教学样本，不执行命令。", teach_response)
        self.assertIn("runtime_sample：1 条", status)
        self.assertEqual(saved_sample["text"], "可以看看资料库吗")
        self.assertEqual(saved_sample["intent"], "knowledge.status")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})
        self.assertIn("个人知识库状态", followup)
        self.assertEqual(provider.calls, [])

    def test_inner_brain_teach_natural_sentence_saves_command_sample(self):
        response = self.agent.handle("以后我说“看看资料库”就是 /kb")
        followup = self.agent.handle("看看资料库")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 教学样本", response)
        self.assertEqual(saved_sample["text"], "看看资料库")
        self.assertEqual(saved_sample["intent"], "knowledge.status")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})
        self.assertIn("个人知识库状态", followup)

    def test_inner_brain_teach_does_not_execute_target_command_when_saving(self):
        response = self.agent.handle("/inner-brain-teach 每天收尾 => /daily-report")

        self.assertIn("已保存 InnerBrain 教学样本", response)
        self.assertIn("目标命令：/daily-report", response)
        self.assertNotIn("已生成日报", response)
        self.assertEqual(list(self.paths.word_dir.glob("*.md")), [])

    def test_inner_brain_teach_rejects_unknown_target_command(self):
        response = self.agent.handle("/inner-brain-teach 打开未知工具 => /unknown-command")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        self.assertIn("教学目标不是已知命令", response)
        self.assertIn("/unknown-command", response)
        self.assertFalse(sample_file.exists())

    def test_inner_brain_teach_search_summary_uses_search_summary_intent(self):
        search_provider = FakeSearchProvider(
            (
                SearchResult("Python 3.13 release", "https://python.example/3-13", "Python 3.13 发布摘要。", "fake"),
            )
        )
        llm_provider = FakeLLMProvider('{"type":"answer","answer":"教学后的搜索总结。"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake"), llm_provider),
            search_router=SearchRouter(SearchSettings(provider="fake", max_results=5), search_provider),
        )

        teach_response = agent.handle("/inner-brain-teach 查版本 => /search-summary Python 版本")
        followup = agent.handle("查版本")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 教学样本", teach_response)
        self.assertEqual(saved_sample["intent"], "web.search_summarize")
        self.assertEqual(saved_sample["slots"], {"command": "/search-summary Python 版本"})
        self.assertIn("LLM 外脑总结：教学后的搜索总结。", followup)
        self.assertEqual(search_provider.calls, ["Python 版本"])

    def test_inner_brain_candidates_reports_empty_state_without_polluting_route_history(self):
        self.agent.handle("早上好")

        response = self.agent.handle("/inner-brain-candidates")
        status = self.agent.route_status_text()

        self.assertIn("InnerBrain 训练候选：暂无。", response)
        self.assertIn("最近输入都已经由命令、本地内脑或知识库稳定处理", response)
        self.assertIn("最近路由：inner-brain / assistant.greeting", status)
        self.assertNotIn("command / /inner-brain-candidates", status)

    def test_inner_brain_candidates_lists_llm_and_memory_fallback_prompts(self):
        self.agent.handle("火星基地预算需要外部判断")
        provider = FakeLLMProvider(
            '{"type":"answer","answer":"外脑处理开放问题","reason":"需要开放判断"}'
        )
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider),
        )
        agent.handle("这句话需要外脑判断")

        response = agent.handle("/inner-brain-candidates")

        self.assertIn("InnerBrain 训练候选：", response)
        self.assertIn("1. 这句话需要外脑判断", response)
        self.assertIn("当前路由：llm-fallback / answer", response)
        self.assertIn("结果：LLM 外脑处理", response)
        self.assertIn("依据：provider=fake model=intent-test source=fallback type=answer", response)
        self.assertIn("/inner-brain-teach 这句话需要外脑判断 => /命令", response)
        self.assertIn("/inner-brain-label 这句话需要外脑判断 => intent slot=value", response)
        self.assertIn("2. 火星基地预算需要外部判断", response)
        self.assertIn("当前路由：memory-fallback / profile", response)
        self.assertNotIn("command / /inner-brain-candidates", response)

    def test_inner_brain_candidates_restore_on_startup(self):
        self.agent.handle("火星基地预算需要外部判断")

        restarted_agent = JarvisAgent(self.paths)
        response = restarted_agent.handle("brain-candidates")

        self.assertIn("InnerBrain 训练候选：", response)
        self.assertIn("1. 火星基地预算需要外部判断", response)
        self.assertIn("当前路由：memory-fallback / profile", response)
        self.assertNotIn("command / brain-candidates", response)

    def test_inner_brain_candidates_prioritize_repeated_fallback_prompts(self):
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("木星基地预算需要外部判断")

        response = self.agent.handle("/inner-brain-candidates")

        self.assertIn("1. 火星基地预算需要外部判断", response)
        self.assertIn("出现次数：2", response)
        self.assertIn("2. 木星基地预算需要外部判断", response)
        self.assertLess(
            response.index("1. 火星基地预算需要外部判断"),
            response.index("2. 木星基地预算需要外部判断"),
        )

    def test_inner_brain_candidates_keep_persistent_counts_after_recent_history_rotation(self):
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("火星基地预算需要外部判断")
        for index in range(1, 6):
            self.agent.handle(f"第{index}个新候选需要外部判断")

        runtime_context = load_runtime_context(self.paths)
        response = self.agent.handle("/inner-brain-candidates")

        recent_prompts = {decision.prompt for decision in runtime_context.recent_route_decisions}
        self.assertNotIn("火星基地预算需要外部判断", recent_prompts)
        self.assertIn("1. 火星基地预算需要外部判断", response)
        self.assertIn("出现次数：3", response)
        self.assertLess(
            response.index("1. 火星基地预算需要外部判断"),
            response.index("2. 第5个新候选需要外部判断"),
        )

    def test_inner_brain_teach_candidate_saves_selected_candidate_command(self):
        self.agent.handle("火星基地预算需要外部判断")

        teach_response = self.agent.handle("/inner-brain-teach-candidate 1 => /kb")
        status_after_teach = self.agent.route_status_text()
        followup = self.agent.handle("火星基地预算需要外部判断")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 教学样本", teach_response)
        self.assertIn("目标命令：/kb", teach_response)
        self.assertEqual(saved_sample["text"], "火星基地预算需要外部判断")
        self.assertEqual(saved_sample["intent"], "knowledge.status")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})
        self.assertIn("最近路由：memory-fallback / profile", status_after_teach)
        self.assertNotIn("command / /inner-brain-teach-candidate", status_after_teach)
        self.assertIn("个人知识库状态", followup)

    def test_inner_brain_teach_candidate_uses_frequency_ranked_candidate(self):
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("木星基地预算需要外部判断")

        teach_response = self.agent.handle("/inner-brain-teach-candidate 1 => /kb")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 教学样本", teach_response)
        self.assertEqual(saved_sample["text"], "火星基地预算需要外部判断")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})

    def test_inner_brain_teach_candidate_uses_persistent_rank_after_recent_history_rotation(self):
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("火星基地预算需要外部判断")
        for index in range(1, 6):
            self.agent.handle(f"第{index}个新候选需要外部判断")

        teach_response = self.agent.handle("/inner-brain-teach-candidate 1 => /kb")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 教学样本", teach_response)
        self.assertEqual(saved_sample["text"], "火星基地预算需要外部判断")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})

    def test_inner_brain_teach_candidate_removes_trained_persistent_candidate(self):
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("火星基地预算需要外部判断")

        self.agent.handle("/inner-brain-teach-candidate 1 => /kb")
        response = self.agent.handle("/inner-brain-candidates")

        self.assertNotIn("火星基地预算需要外部判断", response)
        self.assertIn("InnerBrain 训练候选：暂无。", response)

    def test_inner_brain_teach_candidate_reports_missing_candidate(self):
        self.agent.handle("火星基地预算需要外部判断")

        response = self.agent.handle("/inner-brain-teach-candidate 2 => /kb")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        self.assertIn("没有第 2 条 InnerBrain 训练候选", response)
        self.assertIn("/inner-brain-candidates", response)
        self.assertFalse(sample_file.exists())

    def test_inner_brain_teach_candidate_rejects_unknown_target_command(self):
        self.agent.handle("火星基地预算需要外部判断")

        response = self.agent.handle("/inner-brain-teach-candidate 1 => /unknown-command")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        self.assertIn("教学目标不是已知命令", response)
        self.assertIn("/unknown-command", response)
        self.assertFalse(sample_file.exists())

    def test_inner_brain_label_candidate_saves_selected_candidate_label(self):
        agent = self.agent
        agent.handle("火星基地预算需要外部判断")

        label_response = agent.handle("/inner-brain-label-candidate 1 => knowledge.status command=/kb")
        status_after_label = agent.route_status_text()
        followup = agent.handle("火星基地预算需要外部判断")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 人工标注样本", label_response)
        self.assertIn("意图：knowledge.status", label_response)
        self.assertIn("槽位 command：/kb", label_response)
        self.assertEqual(saved_sample["text"], "火星基地预算需要外部判断")
        self.assertEqual(saved_sample["intent"], "knowledge.status")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})
        self.assertIn("最近路由：memory-fallback / profile", status_after_label)
        self.assertNotIn("command / /inner-brain-label-candidate", status_after_label)
        self.assertIn("个人知识库状态", followup)

    def test_inner_brain_label_candidate_uses_frequency_ranked_candidate(self):
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("火星基地预算需要外部判断")
        self.agent.handle("木星基地预算需要外部判断")

        label_response = self.agent.handle("/inner-brain-label-candidate 1 => knowledge.status command=/kb")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 人工标注样本", label_response)
        self.assertEqual(saved_sample["text"], "火星基地预算需要外部判断")
        self.assertEqual(saved_sample["intent"], "knowledge.status")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})

    def test_inner_brain_label_candidate_reports_missing_candidate(self):
        self.agent.handle("火星基地预算需要外部判断")

        response = self.agent.handle("/inner-brain-label-candidate 2 => knowledge.status command=/kb")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        self.assertIn("没有第 2 条 InnerBrain 训练候选", response)
        self.assertIn("/inner-brain-candidates", response)
        self.assertFalse(sample_file.exists())

    def test_inner_brain_label_candidate_rejects_invalid_slot_assignment(self):
        self.agent.handle("火星基地预算需要外部判断")

        response = self.agent.handle("/inner-brain-label-candidate 1 => knowledge.status command")

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        self.assertIn("标注参数错误", response)
        self.assertIn("slot 必须使用 key=value", response)
        self.assertFalse(sample_file.exists())

    def test_inner_brain_eval_add_candidate_saves_selected_candidate_command_without_training(self):
        self.agent.handle("火星基地预算需要外部判断")

        response = self.agent.handle("/inner-brain-eval-add-candidate 1 => /kb")
        status_after_save = self.agent.route_status_text()
        candidates_after_save = self.agent.handle("/inner-brain-candidates")

        sample_file = self.paths.data_dir / "inner-brain" / "evaluation" / "runtime.jsonl"
        self.assertTrue(sample_file.exists())
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 本机评估样本", response)
        self.assertIn("用户说法：火星基地预算需要外部判断", response)
        self.assertIn("目标命令：/kb", response)
        self.assertIn("后续验证：", response)
        self.assertIn("- 聚焦样本文件：/inner-brain-eval-local-file runtime.jsonl", response)
        self.assertIn("- 导出失败报告：/inner-brain-eval-local-report", response)
        self.assertEqual(saved_sample["text"], "火星基地预算需要外部判断")
        self.assertEqual(saved_sample["expected_intent"], "knowledge.status")
        self.assertEqual(saved_sample["expected_command"], "/kb")
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())
        self.assertIn("1. 火星基地预算需要外部判断", candidates_after_save)
        self.assertIn("最近路由：memory-fallback / profile", status_after_save)
        self.assertNotIn("command / /inner-brain-eval-add-candidate", status_after_save)

    def test_inner_brain_eval_label_candidate_saves_selected_candidate_label_without_training(self):
        self.agent.handle("火星基地预算需要外部判断")

        response = self.agent.handle("/inner-brain-eval-label-candidate 1 => knowledge.status command=/kb")
        candidates_after_save = self.agent.handle("/inner-brain-candidates")

        sample_file = self.paths.data_dir / "inner-brain" / "evaluation" / "runtime.jsonl"
        self.assertTrue(sample_file.exists())
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertIn("已保存 InnerBrain 本机评估样本", response)
        self.assertIn("意图：knowledge.status", response)
        self.assertIn("目标命令：/kb", response)
        self.assertEqual(saved_sample["text"], "火星基地预算需要外部判断")
        self.assertEqual(saved_sample["expected_intent"], "knowledge.status")
        self.assertEqual(saved_sample["expected_command"], "/kb")
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())
        self.assertIn("1. 火星基地预算需要外部判断", candidates_after_save)

    def test_inner_brain_eval_add_candidate_reports_missing_candidate_without_writing_case(self):
        self.agent.handle("火星基地预算需要外部判断")

        response = self.agent.handle("/inner-brain-eval-add-candidate 2 => /kb")

        self.assertIn("没有第 2 条 InnerBrain 训练候选", response)
        self.assertIn("/inner-brain-candidates", response)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "evaluation" / "runtime.jsonl").exists())
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_llm_status_command_reports_router_state(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"状态测试"}')
        router = LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider)
        agent = JarvisAgent(self.paths, llm_router=router)

        response = agent.handle("/llm-status")

        self.assertIn("LLM 外脑：已启用", response)
        self.assertIn("Provider：fake", response)
        self.assertIn("Model：intent-test", response)

    def test_llm_status_command_reports_missing_configuration(self):
        agent = JarvisAgent(self.paths, llm_router=build_llm_router(LLMSettings(provider="openai")))

        response = agent.handle("/llm-status")

        self.assertIn("配置问题：", response)
        self.assertIn("缺少 JARVIS_LITE_LLM_MODEL", response)
        self.assertIn("缺少 JARVIS_LITE_LLM_API_KEY", response)

    def test_llm_activity_status_records_recent_answer_fallback(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"外脑处理开放问题"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider),
        )

        response = agent.handle("这句话需要外脑判断")
        status = agent.llm_activity_status_text()
        runtime_context = load_runtime_context(self.paths)

        self.assertIn("LLM 外脑：外脑处理开放问题", response)
        self.assertIn("外脑运行状态：已启用", status)
        self.assertIn("Provider：fake", status)
        self.assertIn("Model：intent-test", status)
        self.assertIn("最近调用：fallback / answer", status)
        self.assertIn("输入：这句话需要外脑判断", status)
        self.assertIn("结果：外脑处理开放问题", status)
        self.assertIsNotNone(runtime_context.recent_llm_call)

    def test_llm_activity_status_restores_recent_call_on_startup(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"外脑处理开放问题"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider),
        )
        agent.handle("这句话需要外脑判断")
        restarted_agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider),
        )

        status = restarted_agent.llm_activity_status_text()

        self.assertIn("外脑运行状态：已启用", status)
        self.assertIn("最近调用：fallback / answer", status)
        self.assertIn("结果：外脑处理开放问题", status)

    def test_route_status_records_inner_brain_greeting_without_llm(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("早上好")
        status = agent.route_status_text()

        self.assertIn("Jarvis Lite", response)
        self.assertIn("最近路由：inner-brain / assistant.greeting", status)
        self.assertIn("输入：早上好", status)
        self.assertIn("结果：本地内脑命中", status)
        self.assertEqual(provider.calls, [])

    def test_route_status_explains_inner_brain_decision(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        agent.handle("早上好")
        status = agent.route_status_text()

        self.assertIn("最近路由：inner-brain / assistant.greeting", status)
        self.assertIn("依据：", status)
        self.assertIn("source=seed_sample", status)
        self.assertIn("confidence=1.00", status)
        self.assertIn("reason=最相似样本：早上好", status)
        self.assertEqual(provider.calls, [])

    def test_route_status_explains_inner_brain_clarification(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "帮我导入这份资料",
                    "intent": "knowledge.import",
                    "slots": {},
                    "missing": ["source"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        agent.handle("帮我导入这份资料")
        status = agent.route_status_text()

        self.assertIn("最近路由：inner-brain-clarify / knowledge.import", status)
        self.assertIn("依据：", status)
        self.assertIn("source=runtime_sample", status)
        self.assertIn("confidence=1.00", status)
        self.assertIn("missing=source", status)
        self.assertIn("reason=最相似样本：帮我导入这份资料", status)
        self.assertEqual(provider.calls, [])

    def test_route_status_explanation_restores_on_startup(self):
        self.agent.handle("早上好")

        restarted_agent = JarvisAgent(self.paths)
        status = restarted_agent.route_status_text()

        self.assertIn("最近路由：inner-brain / assistant.greeting", status)
        self.assertIn("依据：", status)
        self.assertIn("source=seed_sample", status)
        self.assertIn("reason=最相似样本：早上好", status)

    def test_route_status_tracks_recent_route_history(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"外脑处理开放问题"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider),
        )

        agent.handle("早上好")
        agent.handle("这句话需要外脑判断")
        status = agent.route_status_text()

        self.assertIn("最近路由：llm-fallback / answer", status)
        self.assertIn("最近路由历史：", status)
        self.assertIn("1. llm-fallback / answer | 输入：这句话需要外脑判断 | 结果：LLM 外脑处理", status)
        self.assertIn("2. inner-brain / assistant.greeting | 输入：早上好 | 结果：本地内脑命中", status)

    def test_route_status_history_restores_on_startup(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"外脑处理开放问题"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))
        agent.handle("早上好")
        agent.handle("这句话需要外脑判断")

        restarted_agent = JarvisAgent(self.paths)
        status = restarted_agent.route_status_text()
        runtime_context = load_runtime_context(self.paths)

        self.assertIn("最近路由：llm-fallback / answer", status)
        self.assertIn("最近路由历史：", status)
        self.assertIn("1. llm-fallback / answer | 输入：这句话需要外脑判断", status)
        self.assertIn("2. inner-brain / assistant.greeting | 输入：早上好", status)
        self.assertEqual(len(runtime_context.recent_route_decisions), 2)

    def test_route_status_history_keeps_five_latest_entries(self):
        for prompt in ("/status", "/kb", "/dirs", "/tools", "/memory", "早上好"):
            self.agent.handle(prompt)

        status = self.agent.route_status_text()
        runtime_context = load_runtime_context(self.paths)

        self.assertEqual(len(runtime_context.recent_route_decisions), 5)
        self.assertIn("1. inner-brain / assistant.greeting | 输入：早上好", status)
        self.assertIn("5. command / /kb | 输入：/kb", status)
        self.assertNotIn("command / /status | 输入：/status", status)

    def test_route_history_command_reports_empty_state(self):
        response = self.agent.handle("/route-history")
        status = self.agent.route_status_text()

        self.assertIn("路由历史：还没有记录。", response)
        self.assertIn("先输入一个问题或命令", response)
        self.assertEqual(status, "最近路由：无")

    def test_route_history_command_reports_recent_decisions_with_explanations(self):
        provider = FakeLLMProvider(
            '{"type":"answer","answer":"外脑处理开放问题","reason":"需要开放判断"}'
        )
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider),
        )

        agent.handle("早上好")
        agent.handle("这句话需要外脑判断")
        response = agent.handle("/route-history")

        self.assertIn("路由历史：", response)
        self.assertIn("1. llm-fallback / answer", response)
        self.assertIn("输入：这句话需要外脑判断", response)
        self.assertIn("结果：LLM 外脑处理", response)
        self.assertIn("依据：provider=fake model=intent-test source=fallback type=answer", response)
        self.assertIn("reason=需要开放判断", response)
        self.assertIn("2. inner-brain / assistant.greeting", response)
        self.assertIn("输入：早上好", response)
        self.assertIn("依据：source=seed_sample confidence=1.00", response)
        self.assertNotIn("command / /route-history", response)

    def test_route_history_command_restores_on_startup(self):
        self.agent.handle("早上好")

        restarted_agent = JarvisAgent(self.paths)
        response = restarted_agent.handle("route-history")

        self.assertIn("路由历史：", response)
        self.assertIn("1. inner-brain / assistant.greeting", response)
        self.assertIn("输入：早上好", response)
        self.assertNotIn("command / route-history", response)

    def test_recent_context_includes_recent_route_history(self):
        self.agent.handle("早上好")

        response = self.agent.handle("/recent-context")

        self.assertIn("- 最近路由：inner-brain / assistant.greeting", response)
        self.assertIn("  1. inner-brain / assistant.greeting | 输入：早上好 | 结果：本地内脑命中", response)
        self.assertNotIn("command / /recent-context", response)

    def test_route_status_records_llm_fallback(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"外脑处理开放问题"}')
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider),
        )

        response = agent.handle("这句话需要外脑判断")
        status = agent.route_status_text()

        self.assertIn("LLM 外脑：外脑处理开放问题", response)
        self.assertIn("最近路由：llm-fallback / answer", status)
        self.assertIn("输入：这句话需要外脑判断", status)
        self.assertIn("结果：LLM 外脑处理", status)

    def test_route_status_explains_llm_fallback(self):
        provider = FakeLLMProvider(
            '{"type":"answer","answer":"外脑处理开放问题","reason":"需要开放判断"}'
        )
        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider),
        )

        agent.handle("这句话需要外脑判断")
        status = agent.route_status_text()

        self.assertIn("最近路由：llm-fallback / answer", status)
        self.assertIn("依据：", status)
        self.assertIn("provider=fake", status)
        self.assertIn("model=intent-test", status)
        self.assertIn("source=fallback", status)
        self.assertIn("type=answer", status)
        self.assertIn("summary=外脑处理开放问题", status)
        self.assertIn("reason=需要开放判断", status)

    def test_route_status_records_identity_memory_answer(self):
        self.agent.handle("我叫张三")

        response = self.agent.handle("我是谁")
        status = self.agent.route_status_text()

        self.assertIn("你是张三", response)
        self.assertIn("最近路由：memory-fallback / identity", status)
        self.assertIn("输入：我是谁", status)
        self.assertIn("结果：长期记忆命中", status)

    def test_llm_usage_command_summarizes_local_usage_log(self):
        self.paths.log_path.write_text(
            "\n".join(
                [
                    "2026-05-27T12:00:00\trecord_log\t"
                    "LLM 外脑用量：provider=openai model=gpt-test input_tokens=12 output_tokens=5 total_tokens=17",
                    "2026-05-27T12:01:00\trecord_log\t"
                    "LLM 外脑用量：provider=openai-compatible model=qwen-test input_tokens=7 output_tokens=3 total_tokens=10",
                ]
            ),
            encoding="utf-8",
        )

        response = self.agent.handle("/llm-usage")

        self.assertIn("LLM 用量汇总：2 次调用", response)
        self.assertIn("总计：input_tokens=19 output_tokens=8 total_tokens=27", response)
        self.assertIn("openai / gpt-test：1 次", response)
        self.assertIn("openai-compatible / qwen-test：1 次", response)

    def test_llm_config_example_command_reports_provider_templates(self):
        response = self.agent.handle("/llm-config-example")

        self.assertIn("LLM 配置模板", response)
        self.assertIn('$env:JARVIS_LITE_LLM_PROVIDER = "openai"', response)
        self.assertIn('$env:JARVIS_LITE_LLM_PROVIDER = "openai-compatible"', response)
        self.assertIn("不会读取或保存真实 API key", response)

    def test_llm_config_example_command_can_filter_provider(self):
        response = self.agent.handle("/llm-config-example openai-compatible")

        self.assertIn("OpenAI-compatible 端点", response)
        self.assertIn("JARVIS_LITE_LLM_BASE_URL", response)
        self.assertNotIn("Fake provider", response)

    def test_llm_config_example_command_maps_model_hub_alias(self):
        response = self.agent.handle("/llm-config-example qwen")

        self.assertIn("qwen 使用 OpenAI-compatible adapter", response)
        self.assertIn('$env:JARVIS_LITE_LLM_PROVIDER = "qwen"', response)

    def test_llm_smoke_command_reports_disabled_router(self):
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="off")))

        response = agent.handle("/llm-smoke")

        self.assertIn("LLM smoke：LLM 外脑未启用", response)
        self.assertIn("/llm-status", response)
        self.assertIn("/llm-config-example openai-compatible", response)

    def test_llm_smoke_command_reloads_local_config_during_running_session(self):
        local_config = self.paths.config_dir / "llm.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_response": "{\"type\":\"answer\",\"answer\":\"smoke 已重新读取本地配置\"}",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle("/llm-smoke 测试连接")

        self.assertIn("LLM smoke：type=answer", response)
        self.assertIn("回答：smoke 已重新读取本地配置", response)

    def test_llm_smoke_command_returns_answer_without_normal_fallback(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"smoke 正常"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider))

        response = agent.handle("/llm-smoke 只测试连接")

        self.assertIn("LLM smoke：type=answer", response)
        self.assertIn("回答：smoke 正常", response)
        self.assertEqual(provider.calls[0][0], "只测试连接")
        self.assertIn("LLM smoke 配置验证", provider.calls[0][1][0])

    def test_llm_smoke_command_does_not_execute_command_intent(self):
        provider = FakeLLMProvider('{"type":"command","command":"/kb-summary","reason":"需要看摘要"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), provider))

        response = agent.handle("/llm-smoke 测试命令建议")

        self.assertIn("LLM smoke：type=command", response)
        self.assertIn("命令建议：/kb-summary", response)
        self.assertIn("smoke 不会自动执行命令建议", response)
        self.assertNotIn("知识库摘要", response)

    def test_llm_smoke_command_records_usage(self):
        class UsageProvider:
            name = "fake"

            def complete_intent(self, prompt, context):
                return LLMIntent(
                    type="answer",
                    answer="带用量的 smoke",
                    usage=LLMUsage(
                        provider="fake",
                        model="intent-test",
                        input_tokens=11,
                        output_tokens=4,
                        total_tokens=15,
                    ),
                )

        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), UsageProvider()),
        )

        response = agent.handle("/llm-smoke usage test")

        log_content = (self.paths.logs_dir / "jarvis.log").read_text(encoding="utf-8")
        self.assertIn("回答：带用量的 smoke", response)
        self.assertIn(
            "LLM 外脑用量：provider=fake model=intent-test input_tokens=11 output_tokens=4 total_tokens=15",
            log_content,
        )

    def test_natural_language_llm_smoke_uses_inner_brain_entry(self):
        local_config = self.paths.config_dir / "llm.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_response": "{\"type\":\"answer\",\"answer\":\"外脑连接可用\"}",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle("测试外脑连接")

        self.assertIn("LLM smoke：type=answer", response)
        self.assertIn("回答：外脑连接可用", response)

    def test_natural_language_search_smoke_uses_inner_brain_entry(self):
        local_config = self.paths.config_dir / "search.local.json"
        local_config.write_text(
            json.dumps(
                {
                    "provider": "fake",
                    "fake_results": [
                        {
                            "title": "Python current release",
                            "url": "https://python.example/current",
                            "snippet": "当前版本摘要。",
                        }
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle("测试联网搜索连接")

        self.assertIn("联网搜索 smoke：Python 版本", response)
        self.assertIn("调用结果：成功，返回 1 条来源。", response)
        self.assertIn("Python current release", response)

    def test_llm_context_preview_reports_context_without_calling_provider(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"不应调用 provider"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )

        agent.handle("/ask Jarvis Lite 使用什么？")
        response = agent.handle("/llm-context-preview")

        self.assertIn("LLM context preview", response)
        self.assertIn("不会调用 provider", response)
        self.assertIn("记忆摘要：", response)
        self.assertIn("最近搜索结果：2 条", response)
        self.assertIn("1. data/memory.md", response)
        self.assertIn("2. data/runtime.md", response)
        self.assertEqual(provider.calls, [])

    def test_knowledge_status_command_reports_data_index(self):
        response = self.agent.handle("/kb")

        self.assertIn("个人知识库状态", response)
        self.assertIn("资料文件：1 个", response)
        self.assertIn("可检索文本行：1 行", response)
        self.assertIn("data/note.txt", response)

    def test_knowledge_summary_command_reports_document_previews(self):
        response = self.agent.handle("/kb-summary")

        self.assertIn("知识库摘要：", response)
        self.assertIn("资料文件：1 个", response)
        self.assertIn("1. data/note.txt（1 行）", response)
        self.assertIn("摘要：资料内容", response)

    def test_knowledge_summary_command_suggests_numbered_followups(self):
        response = self.agent.handle("/kb-summary")

        self.assertIn("可继续操作：读取第一份资料；给第一份资料打标签 标签；/ask 关键词", response)

    def test_knowledge_summary_command_suggests_tagged_ask_followups(self):
        self.agent.handle("/tag note.txt 项目 助手")

        response = self.agent.handle("/kb-summary")

        self.assertIn("按标签提问：/ask 助手；/ask 项目", response)

    def test_knowledge_summary_command_suggests_tagged_read_followups(self):
        self.agent.handle("/tag note.txt 项目 助手")

        response = self.agent.handle("/kb-summary")

        self.assertIn("按标签读取：读取助手标签资料；读取项目标签资料", response)

    def test_knowledge_summary_command_sets_recent_document_list_for_numbered_followups(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份摘要资料。\n", encoding="utf-8")
        self.agent.handle("/kb-summary")

        response = self.agent.handle("读取第二份资料")

        self.assertIn("第 2 份资料：data/zeta.md", response)
        self.assertIn("第二份摘要资料", response)

    def test_knowledge_summary_document_list_survives_new_agent_instance(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份持久摘要资料。\n", encoding="utf-8")
        self.agent.handle("/kb-summary")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("读取第二份资料")

        self.assertIn("第 2 份资料：data/zeta.md", response)
        self.assertIn("第二份持久摘要资料", response)

    def test_natural_language_read_tagged_documents_sets_recent_document_list(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目")
        self.agent.handle("/tag zeta.md 项目")

        response = self.agent.handle("读取项目标签资料")
        followup = self.agent.handle("读取第二份资料")

        self.assertIn("标签资料：项目", response)
        self.assertIn("1. data/note.txt（1 行，标签：项目）", response)
        self.assertIn("2. data/zeta.md（1 行，标签：项目）", response)
        self.assertIn("可继续操作：读取第一份资料；给第一份资料打标签 标签；/ask 项目", response)
        self.assertIn("第 2 份资料：data/zeta.md", followup)
        self.assertIn("第二份项目标签资料", followup)

    def test_natural_language_read_tagged_documents_reports_no_match(self):
        response = self.agent.handle("查看缺失标签资料")

        self.assertIn("没有找到标签为“缺失”的资料", response)
        self.assertIn("/kb-summary", response)

    def test_natural_language_preview_tagged_documents_tagging_sets_recent_document_list_without_mutation(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目")
        self.agent.handle("/tag zeta.md 项目")

        response = self.agent.handle("给项目标签资料都打标签 归档")
        followup = self.agent.handle("读取第二份资料")
        knowledge_status = self.agent.handle("/kb")

        self.assertIn("批量打标签预览：项目标签资料", response)
        self.assertIn("拟追加标签：归档", response)
        self.assertIn("1. data/note.txt（当前标签：项目；预览标签：项目、归档）", response)
        self.assertIn("2. data/zeta.md（当前标签：项目；预览标签：项目、归档）", response)
        self.assertIn("说明：这里只生成预览，不会修改资料标签。", response)
        self.assertIn("可继续操作：给第一份资料打标签 项目 归档；给第二份资料打标签 项目 归档", response)
        self.assertIn("第 2 份资料：data/zeta.md", followup)
        self.assertIn("第二份项目标签资料", followup)
        self.assertIn("data/note.txt（1 行，标签：项目）", knowledge_status)
        self.assertIn("data/zeta.md（1 行，标签：项目）", knowledge_status)
        self.assertNotIn("标签：项目、归档", knowledge_status)

    def test_natural_language_preview_tagged_documents_tagging_reports_no_match(self):
        response = self.agent.handle("给缺失标签资料都打标签 归档")

        self.assertIn("没有找到标签为“缺失”的资料", response)
        self.assertIn("/kb-summary", response)

    def test_natural_language_confirm_tagged_documents_tagging_applies_previewed_tags(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目")
        self.agent.handle("/tag zeta.md 项目")
        self.agent.handle("给项目标签资料都打标签 归档")

        response = self.agent.handle("确认执行")
        knowledge_status = self.agent.handle("/kb")
        second_confirm = self.agent.handle("确认执行")

        self.assertIn("已确认执行批量打标签：项目标签资料", response)
        self.assertIn("追加标签：归档", response)
        self.assertIn("1. data/note.txt（项目、归档）", response)
        self.assertIn("2. data/zeta.md（项目、归档）", response)
        self.assertIn("data/note.txt（1 行，标签：项目、归档）", knowledge_status)
        self.assertIn("data/zeta.md（1 行，标签：项目、归档）", knowledge_status)
        self.assertIn("还没有待确认的建议命令", second_confirm)

    def test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目 助手")
        self.agent.handle("/tag zeta.md 项目")
        self.agent.handle("给项目标签资料都打标签 归档")

        response = self.agent.handle("确认执行")
        restore_response = self.agent.handle("给第一份资料打标签 项目 助手")

        self.assertIn("操作记录：本次已更新 2 份资料。", response)
        self.assertIn(
            "恢复提示：如需撤销本次追加，可逐份执行：给第一份资料打标签 项目 助手；给第二份资料打标签 项目",
            response,
        )
        self.assertIn("已更新标签：data/note.txt（项目、助手）", restore_response)

    def test_natural_language_cancel_tagged_documents_tagging_clears_preview(self):
        self.agent.handle("/tag note.txt 项目")
        self.agent.handle("给项目标签资料都打标签 归档")

        cancel_response = self.agent.handle("取消执行")
        confirm_response = self.agent.handle("确认执行")
        knowledge_status = self.agent.handle("/kb")

        self.assertIn("已取消待执行批量打标签：项目标签资料", cancel_response)
        self.assertIn("还没有待确认的建议命令", confirm_response)
        self.assertIn("data/note.txt（1 行，标签：项目）", knowledge_status)
        self.assertNotIn("标签：项目、归档", knowledge_status)

    def test_voice_status_command_reports_voice_entry(self):
        with patch.dict(os.environ, {"JARVIS_LITE_VOICE_ENGINE": "transcript"}):
            response = self.agent.handle("/voice-status")

        self.assertIn("语音入口状态", response)
        self.assertIn("当前引擎：transcript", response)

    def test_automation_status_command_reports_workspace_automation(self):
        response = self.agent.handle("/automation-status")

        self.assertIn("阶段 4 自动化状态", response)
        self.assertIn("常用目录", response)

    def test_update_status_command_reports_available_update_from_manifest(self):
        manifest = Path(self.temp_dir.name) / "update.json"
        manifest.write_text(
            json.dumps(
                {
                        "version": "0.50.1",
                        "download_url": "https://example.com/JarvisLiteSetup.exe",
                        "release_notes": "新增更新检查。",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle(f"/update-status {manifest}")

        self.assertIn("发现新版本：0.50.1", response)
        self.assertIn(f"当前版本：{__version__}", response)
        self.assertIn("https://example.com/JarvisLiteSetup.exe", response)

    def test_update_download_command_downloads_package_to_runtime_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            paths = build_project_paths(root / "jarvis-lite")
            agent = JarvisAgent(paths)
            package = root / "JarvisLiteSetup.exe"
            package.write_bytes(b"installer")
            manifest = root / "update.json"
            manifest.write_text(
                json.dumps(
                    {
                        "version": "0.50.1",
                        "download_url": str(package),
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            response = agent.handle(f"/update-download {manifest}")
            downloaded = root / "jarvis-lite-runtime" / "updates" / "JarvisLiteSetup.exe"

            self.assertIn("已下载更新安装包", response)
            self.assertIn(str(downloaded), response)
            self.assertEqual(downloaded.read_bytes(), b"installer")

    def test_natural_language_identity_question_does_not_pollute_memory(self):
        self.agent.handle("我叫欧阳")

        response = self.agent.handle("我是你的什么人，你知道吗")
        content = self.paths.profile_path.read_text(encoding="utf-8")

        self.assertIn("你是欧阳", response)
        self.assertNotIn("用户身份：你的什么人", content)

    def test_natural_language_capability_question_returns_capability_summary(self):
        response = self.agent.handle("你现在能做什么事")

        self.assertIn("我现在可以", response)
        self.assertIn("记忆", response)
        self.assertIn("知识库", response)
        self.assertIn("日报", response)

    def test_natural_language_capability_question_reports_recent_experiences(self):
        self.agent.handle("/experience 导入资料后先打标签")

        response = self.agent.handle("你现在能做什么事")

        self.assertIn("最近经验", response)
        self.assertIn("导入资料后先打标签", response)

    def test_natural_language_daily_report_generates_report(self):
        response = self.agent.handle("生成日报")

        self.assertIn("已生成日报：word/", response)

    def test_natural_language_knowledge_status_maps_to_kb(self):
        response = self.agent.handle("查看知识库")

        self.assertIn("个人知识库状态", response)

    def test_natural_language_knowledge_summary_maps_to_summary(self):
        response = self.agent.handle("总结知识库")

        self.assertIn("知识库摘要：", response)
        self.assertIn("data/note.txt", response)
        self.assertIn("摘要：资料内容", response)

    def test_natural_language_update_status_maps_to_update_status(self):
        response = self.agent.handle("检查更新")

        self.assertIn("更新状态", response)
        self.assertIn("更新源：未配置", response)

    def test_natural_language_tag_document_updates_document_tags(self):
        response = self.agent.handle("给 note.txt 打标签 项目 Python")

        self.assertIn("已更新标签：data/note.txt（项目、Python）", response)
        self.assertIn("标签：项目、Python", self.agent.handle("/kb"))

    def test_natural_language_mark_document_as_tags_updates_document_tags(self):
        response = self.agent.handle("把 note.txt 标记为 私人资料")

        self.assertIn("已更新标签：data/note.txt（私人资料）", response)
        self.assertIn("标签：私人资料", self.agent.handle("/kb"))

    def test_natural_language_tag_recent_imported_document_updates_document_tags(self):
        source = Path(self.temp_dir.name) / "recent.md"
        source.write_text("Jarvis Lite 可以记住最近导入的资料。\n", encoding="utf-8")
        self.agent.handle(f"/import {source}")

        response = self.agent.handle("给这个资料打标签 项目 Python")

        self.assertIn("已更新标签：data/recent.md（项目、Python）", response)
        self.assertIn("标签：项目、Python", self.agent.handle("/kb"))

    def test_natural_language_tag_recent_document_requires_recent_document_context(self):
        response = self.agent.handle("给这个资料打标签 项目")

        self.assertIn("还没有最近资料", response)
        self.assertIn("先导入资料", response)

    def test_natural_language_tag_numbered_recent_document_updates_selected_document_tags(self):
        (self.paths.data_dir / "manual.md").write_text(
            "第二份最近资料可被打标签。\n",
            encoding="utf-8",
        )
        self.agent.handle("/read manual.md")
        self.agent.handle("/read note.txt")

        response = self.agent.handle("给第二份资料打标签 项目 Python")

        self.assertIn("已更新标签：data/manual.md（项目、Python）", response)
        self.assertIn("manual.md", self.agent.handle("/kb"))
        self.assertIn("标签：项目、Python", self.agent.handle("/kb"))

    def test_natural_language_tag_numbered_recent_document_marks_missing_document(self):
        manual_path = self.paths.data_dir / "manual.md"
        manual_path.write_text("第二份最近资料可被打标签。\n", encoding="utf-8")
        self.agent.handle("/read manual.md")
        self.agent.handle("/read note.txt")
        manual_path.unlink()

        response = self.agent.handle("给第二份资料打标签 项目")

        self.assertIn("第 2 份资料：data/manual.md（资料缺失）", response)
        self.assertIn("你可以先查看 /kb，或重新导入资料。", response)

    def test_natural_language_tag_numbered_recent_document_requires_recent_list(self):
        response = self.agent.handle("给第二份资料打标签 项目")

        self.assertIn("还没有最近资料列表", response)
        self.assertIn("先读取资料", response)

    def test_read_command_sets_persistent_recent_document_context(self):
        (self.paths.data_dir / "manual.md").write_text(
            "Jarvis Lite 读取资料后应更新最近资料上下文。\n",
            encoding="utf-8",
        )

        read_response = self.agent.handle("/read manual.md")
        restarted_agent = JarvisAgent(self.paths)
        tag_response = restarted_agent.handle("给这个资料打标签 项目")

        self.assertIn("读取资料后应更新最近资料上下文", read_response)
        self.assertIn("已更新标签：data/manual.md（项目）", tag_response)
        self.assertIn("标签：项目", restarted_agent.handle("/kb"))

    def test_natural_language_read_document_updates_recent_document_context(self):
        (self.paths.data_dir / "manual.md").write_text(
            "Gamma payload 42.\nSecond line without query words.\n",
            encoding="utf-8",
        )

        read_response = self.agent.handle("读取 manual.md")
        tag_response = self.agent.handle("给这个资料打标签 项目")

        self.assertIn("Gamma payload 42", read_response)
        self.assertIn("Second line without query words", read_response)
        self.assertIn("已更新标签：data/manual.md（项目）", tag_response)
        self.assertIn("标签：项目", self.agent.handle("/kb"))

    def test_natural_language_read_recent_document_reads_current_document(self):
        (self.paths.data_dir / "manual.md").write_text(
            "Recent document payload.\nSecond recent document line.\n",
            encoding="utf-8",
        )
        self.agent.handle("读取 manual.md")

        response = self.agent.handle("读取这个资料")

        self.assertIn("Recent document payload", response)
        self.assertIn("Second recent document line", response)

    def test_natural_language_read_recent_document_requires_recent_context(self):
        response = self.agent.handle("读取这个资料")

        self.assertIn("还没有最近资料", response)
        self.assertIn("先读取资料", response)

    def test_natural_language_read_numbered_recent_document_reads_selected_document(self):
        (self.paths.data_dir / "manual.md").write_text(
            "Second recent document payload.\n",
            encoding="utf-8",
        )
        self.agent.handle("/read manual.md")
        self.agent.handle("/read note.txt")

        response = self.agent.handle("读取第二份资料")

        self.assertIn("第 2 份资料：data/manual.md", response)
        self.assertIn("Second recent document payload", response)

    def test_natural_language_read_numbered_recent_document_marks_missing_document(self):
        manual_path = self.paths.data_dir / "manual.md"
        manual_path.write_text("Second recent document payload.\n", encoding="utf-8")
        self.agent.handle("/read manual.md")
        self.agent.handle("/read note.txt")
        manual_path.unlink()

        response = self.agent.handle("读取第二份资料")

        self.assertIn("第 2 份资料：data/manual.md（资料缺失）", response)
        self.assertIn("你可以先查看 /kb，或重新导入资料。", response)

    def test_natural_language_read_numbered_recent_document_requires_recent_list(self):
        response = self.agent.handle("读取第二份资料")

        self.assertIn("还没有最近资料列表", response)
        self.assertIn("先读取资料", response)

    def test_natural_language_read_numbered_recent_document_does_not_override_search_result(self):
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        self.agent.handle("/ask Jarvis Lite 使用什么？")

        response = self.agent.handle("查看第二条结果")

        self.assertIn("第 2 条结果：data/runtime.md", response)
        self.assertIn("Python 3.13", response)

    def test_natural_language_import_file_adds_document_to_knowledge_base(self):
        source = Path(self.temp_dir.name) / "outside-natural.md"
        source.write_text("Jarvis Lite 可以用自然语言导入资料。\n", encoding="utf-8")

        response = self.agent.handle(f"导入 {source} 到知识库")

        self.assertIn("已导入知识库", response)
        self.assertIn("data/outside-natural.md", response)
        self.assertIn("自然语言导入资料", self.agent.handle("/ask 自然语言导入资料"))

    def test_natural_language_import_quoted_file_path_adds_document_to_knowledge_base(self):
        source = Path(self.temp_dir.name) / "outside natural.md"
        source.write_text("Jarvis Lite 可以导入带空格路径的资料。\n", encoding="utf-8")

        response = self.agent.handle(f'把 "{source}" 导入知识库')

        self.assertIn("已导入知识库", response)
        self.assertIn("data/outside natural.md", response)
        self.assertIn("带空格路径", self.agent.handle("/ask 带空格路径"))

    def test_natural_language_open_windows_drive_records_request(self):
        drive = Path("D:/")
        if not drive.is_dir():
            self.skipTest("本机没有 D 盘，跳过自然语言打开 D 盘验证。")

        response = self.agent.handle("打开D盘")
        transcript = (self.paths.logs_dir / "desktop-actions.txt").read_text(encoding="utf-8")

        self.assertIn("已记录打开目录请求：D盘", response)
        self.assertIn("open_directory", transcript)
        self.assertIn(str(drive.resolve()), transcript)

    def test_natural_language_open_common_directory_alias_records_request(self):
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()
        self.agent.handle(f"/dir-add 项目 {target}")

        response = self.agent.handle("打开项目目录")
        transcript = (self.paths.logs_dir / "desktop-actions.txt").read_text(encoding="utf-8")

        self.assertIn("已记录打开目录请求：项目", response)
        self.assertIn("open_directory", transcript)
        self.assertIn(str(target.resolve()), transcript)

    def test_natural_language_organize_common_directory_alias_returns_preview(self):
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()
        (target / "notes.md").write_text("笔记", encoding="utf-8")
        self.agent.handle(f"/dir-add 项目 {target}")

        response = self.agent.handle("整理项目目录")

        self.assertIn("文件整理预览：项目", response)
        self.assertIn("notes.md", response)
        self.assertIn("不会移动或删除文件", response)

    def test_natural_language_organize_project_uses_known_project_directory(self):
        project_note = self.paths.root / "project-note.md"
        project_note.write_text("项目说明", encoding="utf-8")

        response = self.agent.handle("整理项目目录")

        self.assertIn("文件整理预览：项目", response)
        self.assertIn("project-note.md", response)
        self.assertIn("不会移动或删除文件", response)

    def test_natural_language_open_project_uses_known_project_directory(self):
        response = self.agent.handle("打开项目目录")

        transcript_path = self.paths.logs_dir / "desktop-actions.txt"
        self.assertIn("已记录打开目录请求：项目", response)
        self.assertTrue(transcript_path.is_file())
        transcript = transcript_path.read_text(encoding="utf-8")
        self.assertIn("open_directory", transcript)
        self.assertIn(str(self.paths.root.resolve()), transcript)

    def test_natural_language_organize_recent_directory_after_open_common_directory(self):
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()
        (target / "notes.md").write_text("笔记", encoding="utf-8")
        self.agent.handle(f"/dir-add 项目 {target}")
        self.agent.handle("打开项目目录")

        response = self.agent.handle("整理这个目录")

        self.assertIn("文件整理预览：项目", response)
        self.assertIn("notes.md", response)
        self.assertIn("不会移动或删除文件", response)

    def test_natural_language_open_recent_directory_requires_recent_directory_context(self):
        response = self.agent.handle("打开这个目录")

        self.assertIn("还没有最近目录", response)
        self.assertIn("先打开或整理一个目录", response)

    def test_natural_language_organize_desktop_uses_known_desktop_directory(self):
        desktop = Path(self.temp_dir.name) / "Desktop"
        desktop.mkdir()
        (desktop / "todo.txt").write_text("待办", encoding="utf-8")

        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            response = self.agent.handle("整理桌面")

        self.assertIn("文件整理预览：桌面", response)
        self.assertIn("todo.txt", response)
        self.assertIn("不会移动或删除文件", response)

    def test_natural_language_organize_downloads_uses_known_downloads_directory(self):
        downloads = Path(self.temp_dir.name) / "Downloads"
        downloads.mkdir()
        (downloads / "invoice.pdf").write_text("发票", encoding="utf-8")

        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            response = self.agent.handle("整理下载目录")

        self.assertIn("文件整理预览：下载", response)
        self.assertIn("invoice.pdf", response)
        self.assertIn("不会移动或删除文件", response)

    def test_natural_language_open_desktop_uses_known_desktop_directory(self):
        desktop = Path(self.temp_dir.name) / "Desktop"
        desktop.mkdir()

        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            response = self.agent.handle("打开桌面")

        transcript = (self.paths.logs_dir / "desktop-actions.txt").read_text(encoding="utf-8")
        self.assertIn("已记录打开目录请求：桌面", response)
        self.assertIn("open_directory", transcript)
        self.assertIn(str(desktop.resolve()), transcript)

    def test_natural_language_open_downloads_uses_known_downloads_directory(self):
        downloads = Path(self.temp_dir.name) / "Downloads"
        downloads.mkdir()

        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            response = self.agent.handle("打开下载目录")

        transcript_path = self.paths.logs_dir / "desktop-actions.txt"
        self.assertIn("已记录打开目录请求：下载", response)
        self.assertTrue(transcript_path.is_file())
        transcript = transcript_path.read_text(encoding="utf-8")
        self.assertIn("open_directory", transcript)
        self.assertIn(str(downloads.resolve()), transcript)

    def test_natural_language_recent_files_reports_known_project_files_newest_first(self):
        old_file = self.paths.root / "old-note.txt"
        new_file = self.paths.root / "new-note.md"
        nested = self.paths.root / "nested"
        nested.mkdir()
        nested_file = nested / "nested-note.txt"
        old_file.write_text("旧项目文件", encoding="utf-8")
        new_file.write_text("新项目文件", encoding="utf-8")
        nested_file.write_text("不扫描子目录", encoding="utf-8")
        os.utime(old_file, (100, 100))
        os.utime(new_file, (200, 200))
        os.utime(nested_file, (300, 300))

        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            response = self.agent.handle("查看最近文件")

        self.assertIn("最近文件", response)
        self.assertIn("项目", response)
        self.assertLess(response.index("new-note.md"), response.index("old-note.txt"))
        self.assertNotIn("nested-note.txt", response)

    def test_recent_files_command_reports_empty_state(self):
        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            response = self.agent.handle("/recent-files")

        self.assertIn("最近文件", response)
        self.assertIn("没有找到", response)
        self.assertIn("项目目录、桌面或下载目录", response)

    def test_natural_language_read_numbered_recent_file_reports_file_metadata(self):
        recent_file = self.paths.root / "recent-report.md"
        recent_file.write_text("最近文件内容不应被读取。\n", encoding="utf-8")
        os.utime(recent_file, (200, 200))
        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            self.agent.handle("查看最近文件")

        response = self.agent.handle("查看第一份最近文件")

        self.assertIn("第 1 份最近文件：recent-report.md", response)
        self.assertIn("来源：项目", response)
        self.assertIn(f"路径：{recent_file.resolve()}", response)
        self.assertIn("修改时间：", response)
        self.assertIn("不会读取或打开文件", response)
        self.assertNotIn("最近文件内容不应被读取", response)

    def test_recent_file_list_survives_new_agent_instance(self):
        recent_file = self.paths.root / "persistent-recent.txt"
        recent_file.write_text("最近文件列表应跨实例恢复。\n", encoding="utf-8")
        os.utime(recent_file, (200, 200))
        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            self.agent.handle("/recent-files")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("查看第一份最近文件")

        self.assertIn("第 1 份最近文件：persistent-recent.txt", response)
        self.assertIn(f"路径：{recent_file.resolve()}", response)

    def test_natural_language_read_numbered_recent_file_requires_recent_files(self):
        response = self.agent.handle("查看第一份最近文件")

        self.assertIn("还没有最近文件列表", response)
        self.assertIn("先查看最近文件", response)

    def test_natural_language_import_numbered_recent_file_adds_document_to_knowledge_base(self):
        recent_file = self.paths.root / "recent-source.md"
        recent_file.write_text("最近文件可以导入知识库。\n", encoding="utf-8")
        os.utime(recent_file, (200, 200))
        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            self.agent.handle("/recent-files")

        response = self.agent.handle("导入第一份最近文件到知识库")

        self.assertIn("已导入知识库", response)
        self.assertIn("data/recent-source.md", response)
        ask_response = self.agent.handle("/ask 最近文件可以导入什么？")
        self.assertIn("data/recent-source.md", ask_response)
        self.assertIn("最近文件可以导入知识库", ask_response)

    def test_natural_language_import_numbered_recent_file_requires_recent_files(self):
        response = self.agent.handle("导入第一份最近文件到知识库")

        self.assertIn("还没有最近文件列表", response)
        self.assertIn("先查看最近文件", response)

    def test_natural_language_import_numbered_recent_file_reports_out_of_range(self):
        recent_file = self.paths.root / "only-recent.md"
        recent_file.write_text("只有一份最近文件。\n", encoding="utf-8")
        os.utime(recent_file, (200, 200))
        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            self.agent.handle("查看最近文件")

        response = self.agent.handle("把第2份最近文件导入知识库")

        self.assertIn("最近文件列表只有 1 条", response)
        self.assertIn("不能选择第 2 份", response)

    def test_dir_add_and_dirs_commands_manage_common_directories(self):
        target = Path(self.temp_dir.name) / "projects"
        target.mkdir()

        add_response = self.agent.handle(f"/dir-add 项目 {target}")
        list_response = self.agent.handle("/dirs")

        self.assertIn("已登记常用目录：项目", add_response)
        self.assertIn("项目", list_response)
        self.assertIn(str(target.resolve()), list_response)

    def test_daily_report_command_writes_report_to_word_dir(self):
        response = self.agent.handle("/daily-report today.md")

        self.assertIn("已生成日报：word/today.md", response)
        self.assertTrue((self.paths.word_dir / "today.md").is_file())

    def test_organize_preview_command_reports_plan_for_common_directory(self):
        target = Path(self.temp_dir.name) / "desktop"
        target.mkdir()
        (target / "notes.md").write_text("笔记", encoding="utf-8")
        (target / "todo.txt").write_text("待办", encoding="utf-8")
        self.agent.handle(f"/dir-add 桌面 {target}")

        response = self.agent.handle("/organize-preview 桌面")

        self.assertIn("文件整理预览：桌面", response)
        self.assertIn("不会移动或删除文件", response)
        self.assertIn("md/", response)
        self.assertIn("notes.md", response)
        self.assertIn("txt/", response)
        self.assertIn("todo.txt", response)

    def test_dir_open_command_records_dry_run_request(self):
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()
        self.agent.handle(f"/dir-add 项目 {target}")

        response = self.agent.handle("/dir-open 项目")

        transcript = (self.paths.logs_dir / "desktop-actions.txt").read_text(encoding="utf-8")
        self.assertIn("已记录打开目录请求：项目", response)
        self.assertIn("当前不会启动外部应用", response)
        self.assertIn("open_directory", transcript)
        self.assertIn(str(target.resolve()), transcript)

    def test_speak_command_records_transcript(self):
        with patch.dict(os.environ, {"JARVIS_LITE_VOICE_ENGINE": "transcript"}):
            response = self.agent.handle("/speak 你好 Jarvis")

        self.assertIn("已记录语音播报文本", response)
        self.assertIn("你好 Jarvis", (self.paths.logs_dir / "voice-output.txt").read_text(encoding="utf-8"))

    def test_voice_command_handles_recognized_text_and_speaks_response(self):
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 推荐使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )

        with patch.dict(os.environ, {"JARVIS_LITE_VOICE_ENGINE": "transcript"}):
            response = self.agent.handle("/voice Jarvis Lite 推荐使用什么 Python 版本？")

        transcript = (self.paths.logs_dir / "voice-output.txt").read_text(encoding="utf-8")
        self.assertIn("识别文本：Jarvis Lite 推荐使用什么 Python 版本？", response)
        self.assertIn("Python 3.13", response)
        self.assertIn("Python 3.13", transcript)

    def test_tag_command_updates_document_tags(self):
        response = self.agent.handle("/tag note.txt 项目 Python")

        self.assertIn("已更新标签：data/note.txt（项目、Python）", response)
        self.assertIn("标签：项目、Python", self.agent.handle("/kb"))

    def test_tag_command_requires_filename_and_tags(self):
        response = self.agent.handle("/tag note.txt")

        self.assertIn("用法：/tag 文件名 标签...", response)

    def test_ask_command_can_find_document_by_tag(self):
        self.agent.handle("/tag note.txt 私人资料")

        response = self.agent.handle("/ask 私人资料")

        self.assertIn("data/note.txt:1", response)

    def test_natural_language_tag_recent_search_result_after_ask_command(self):
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 推荐使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        self.agent.handle("/ask Python 3.13")

        response = self.agent.handle("给这个结果打标签 运行环境")

        self.assertIn("已更新标签：data/runtime.md（运行环境）", response)
        self.assertIn("标签：运行环境", self.agent.handle("/kb"))

    def test_natural_language_tag_recent_search_result_after_plain_question(self):
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 推荐使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        self.agent.handle("Jarvis Lite 推荐使用什么 Python 版本？")

        response = self.agent.handle("给这个结果打标签 运行环境")

        self.assertIn("已更新标签：data/runtime.md（运行环境）", response)
        self.assertIn("标签：运行环境", self.agent.handle("/kb"))

    def test_natural_language_tag_numbered_search_result_after_ask_command(self):
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )

        search_response = self.agent.handle("/ask Jarvis Lite 使用什么？")
        response = self.agent.handle("给第二条结果打标签 运行环境")

        self.assertIn("1. 根据 data/memory.md:1", search_response)
        self.assertIn("2. 根据 data/runtime.md:1", search_response)
        self.assertIn("已更新标签：data/runtime.md（运行环境）", response)
        self.assertIn("标签：运行环境", self.agent.handle("/kb"))

    def test_natural_language_tag_numbered_search_result_requires_recent_results(self):
        response = self.agent.handle("给第二条结果打标签 运行环境")

        self.assertIn("还没有最近搜索结果", response)
        self.assertIn("先提问", response)

    def test_natural_language_read_numbered_search_result_after_ask_command(self):
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        self.agent.handle("/ask Jarvis Lite 使用什么？")

        response = self.agent.handle("查看第二条结果")

        self.assertIn("data/runtime.md", response)
        self.assertIn("Python 3.13", response)

    def test_natural_language_read_numbered_search_result_requires_recent_results(self):
        response = self.agent.handle("查看第二条结果")

        self.assertIn("还没有最近搜索结果", response)
        self.assertIn("先提问", response)

    def test_recent_search_results_survive_new_agent_instance(self):
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        self.agent.handle("/ask Jarvis Lite 使用什么？")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("查看第二条结果")

        self.assertIn("data/runtime.md", response)
        self.assertIn("Python 3.13", response)

    def test_recent_imported_document_survives_new_agent_instance(self):
        source = Path(self.temp_dir.name) / "recent-persistent.md"
        source.write_text("Jarvis Lite 可以跨 Agent 实例记住最近资料。\n", encoding="utf-8")
        self.agent.handle(f"/import {source}")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("给这个资料打标签 项目")

        self.assertIn("已更新标签：data/recent-persistent.md（项目）", response)
        self.assertIn("标签：项目", restarted_agent.handle("/kb"))

    def test_recent_directory_survives_new_agent_instance(self):
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()
        self.agent.handle(f"/dir-add 项目 {target}")
        self.agent.handle("打开项目目录")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("打开这个目录")

        self.assertIn("已记录打开目录请求：项目", response)
        self.assertIn(str(target.resolve()), response)

    def test_natural_language_recent_context_status_reports_empty_state(self):
        response = self.agent.handle("查看最近上下文")

        self.assertIn("最近上下文", response)
        self.assertIn("还没有记录", response)
        self.assertIn("先提问", response)

    def test_natural_language_recent_context_status_reports_current_context(self):
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )

        self.agent.handle("/ask Jarvis Lite 使用什么？")
        self.agent.handle(f"/dir-add 项目 {target}")
        self.agent.handle("打开项目目录")
        response = self.agent.handle("你还记得刚才什么")

        self.assertIn("最近上下文", response)
        self.assertIn("最近资料：data/memory.md", response)
        self.assertIn(f"最近目录：项目 -> {target.resolve()}", response)
        self.assertIn("最近搜索结果：2 条", response)
        self.assertIn("1. data/memory.md", response)
        self.assertIn("2. data/runtime.md", response)

    def test_natural_language_recent_context_status_reports_recent_document_list(self):
        (self.paths.data_dir / "manual.md").write_text(
            "第一份最近资料。\n",
            encoding="utf-8",
        )
        self.agent.handle("/read manual.md")
        self.agent.handle("/read note.txt")

        response = self.agent.handle("查看最近上下文")

        self.assertIn("最近资料：data/note.txt", response)
        self.assertIn("最近资料列表：2 条", response)
        self.assertIn("1. data/note.txt", response)
        self.assertIn("2. data/manual.md", response)

    def test_natural_language_recent_context_status_reports_recent_file_list(self):
        older_file = self.paths.root / "older-report.md"
        newer_file = self.paths.root / "newer-report.md"
        older_file.write_text("旧文件内容不应进入上下文状态。\n", encoding="utf-8")
        newer_file.write_text("新文件内容不应进入上下文状态。\n", encoding="utf-8")
        os.utime(older_file, (200, 200))
        os.utime(newer_file, (300, 300))
        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            self.agent.handle("查看最近文件")

        response = self.agent.handle("查看最近上下文")

        self.assertIn("最近文件列表：2 条", response)
        self.assertIn(f"1. 项目 -> {newer_file.resolve()}", response)
        self.assertIn(f"2. 项目 -> {older_file.resolve()}", response)
        self.assertNotIn("新文件内容不应进入上下文状态", response)

    def test_natural_language_recent_context_status_suggests_next_actions(self):
        target = Path(self.temp_dir.name) / "project"
        target.mkdir()
        recent_file = self.paths.root / "recent-task.txt"
        recent_file.write_text("最近文件内容不应进入建议。\n", encoding="utf-8")
        os.utime(recent_file, (200, 200))
        self.agent.handle("/read note.txt")
        self.agent.handle(f"/dir-add 项目 {target}")
        self.agent.handle("打开项目目录")
        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            self.agent.handle("/recent-files")
        self.agent.handle("/experience-advice 导入资料")

        response = self.agent.handle("查看最近上下文")

        self.assertIn("下一步建议：", response)
        self.assertIn("继续处理最近资料：/read note.txt；/tag note.txt 标签...", response)
        self.assertIn("继续处理最近目录：/organize-preview 项目；/dir-open 项目", response)
        self.assertIn("继续处理最近文件：查看第一份最近文件；导入第一份最近文件到知识库；/recent-files", response)
        self.assertIn("继续最近建议：查看第一条建议；执行第一条建议", response)
        self.assertNotIn("最近文件内容不应进入建议", response)

    def test_recent_document_list_survives_new_agent_instance(self):
        (self.paths.data_dir / "manual.md").write_text(
            "第一份持久化最近资料。\n",
            encoding="utf-8",
        )
        self.agent.handle("/read manual.md")
        self.agent.handle("/read note.txt")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("最近上下文状态")

        self.assertIn("最近资料列表：2 条", response)
        self.assertIn("1. data/note.txt", response)
        self.assertIn("2. data/manual.md", response)

    def test_recent_file_list_survives_new_agent_instance_in_recent_context(self):
        recent_file = self.paths.root / "restored-recent.txt"
        recent_file.write_text("恢复后的最近文件内容不应被读取。\n", encoding="utf-8")
        os.utime(recent_file, (200, 200))
        with patch("jarvis_lite.agent.Path.home", return_value=Path(self.temp_dir.name)):
            self.agent.handle("/recent-files")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("最近上下文状态")

        self.assertIn("最近文件列表：1 条", response)
        self.assertIn(f"1. 项目 -> {recent_file.resolve()}", response)
        self.assertNotIn("恢复后的最近文件内容不应被读取", response)

    def test_natural_language_recent_context_status_reports_recent_advice(self):
        self.agent.handle("/experience-advice 导入资料")

        response = self.agent.handle("查看最近上下文")

        self.assertIn("最近上下文", response)
        self.assertIn("最近建议：3 条", response)
        self.assertIn("1. /import 源文件或目录路径 [目标文件名]", response)
        self.assertIn("待确认建议命令：无", response)

    def test_natural_language_recent_context_status_reports_pending_advice_command(self):
        self.agent.handle("/experience-advice 导入资料")
        self.agent.handle("执行第二条建议")

        response = self.agent.handle("查看最近上下文")

        self.assertIn("最近建议：3 条", response)
        self.assertIn("待确认建议命令：/kb", response)

    def test_natural_language_recent_context_status_reports_pending_tagged_documents_tagging(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目")
        self.agent.handle("/tag zeta.md 项目")
        self.agent.handle("给项目标签资料都打标签 归档")

        response = self.agent.handle("查看最近上下文")
        self.agent.handle("确认执行")
        after_confirm_response = self.agent.handle("查看最近上下文")

        self.assertIn("待确认批量打标签：项目标签资料 -> 追加标签：归档，2 份", response)
        self.assertIn("待确认建议命令：无", response)
        self.assertIn("待确认批量打标签：无", after_confirm_response)

    def test_natural_language_recent_context_status_reports_recent_tagged_documents_operation(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目 助手")
        self.agent.handle("/tag zeta.md 项目")
        self.agent.handle("给项目标签资料都打标签 归档")
        self.agent.handle("确认执行")

        response = self.agent.handle("查看最近上下文")

        self.assertIn("最近批量打标签：项目标签资料 -> 追加标签：归档，已更新 2 份", response)
        self.assertIn("恢复提示：给第一份资料打标签 项目 助手；给第二份资料打标签 项目", response)
        self.assertIn("待确认批量打标签：无", response)

    def test_recent_tagged_documents_operation_survives_new_agent_instance(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目 助手")
        self.agent.handle("/tag zeta.md 项目")
        self.agent.handle("给项目标签资料都打标签 归档")
        self.agent.handle("确认执行")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("最近上下文状态")

        self.assertIn("最近批量打标签：项目标签资料 -> 追加标签：归档，已更新 2 份", response)
        self.assertIn("恢复提示：给第一份资料打标签 项目 助手；给第二份资料打标签 项目", response)

    def test_tagged_documents_history_command_survives_new_agent_instance(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目 助手")
        self.agent.handle("/tag zeta.md 项目")
        self.agent.handle("给项目标签资料都打标签 归档")
        self.agent.handle("确认执行")
        self.agent.handle("给归档标签资料都打标签 已审")
        self.agent.handle("确认执行")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("/tag-history")
        natural_response = restarted_agent.handle("查看批量标签历史")
        recent_context = restarted_agent.handle("查看最近上下文")

        self.assertIn("批量打标签历史：", response)
        self.assertIn("1. 归档标签资料 -> 追加标签：已审，已更新 2 份", response)
        self.assertIn("2. 项目标签资料 -> 追加标签：归档，已更新 2 份", response)
        self.assertLess(
            response.find("1. 归档标签资料"),
            response.find("2. 项目标签资料"),
        )
        self.assertIn("恢复提示：给第一份资料打标签 项目 助手 归档；给第二份资料打标签 项目 归档", response)
        self.assertIn("批量打标签历史：", natural_response)
        self.assertIn("最近批量打标签：归档标签资料 -> 追加标签：已审，已更新 2 份", recent_context)

    def test_read_tagged_documents_history_documents_sets_recent_document_list(self):
        (self.paths.data_dir / "zeta.md").write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目 助手")
        self.agent.handle("/tag zeta.md 项目")
        self.agent.handle("给项目标签资料都打标签 归档")
        self.agent.handle("确认执行")
        self.agent.handle("给归档标签资料都打标签 已审")
        self.agent.handle("确认执行")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("读取第一条标签历史资料")
        followup = restarted_agent.handle("读取第二份资料")

        self.assertIn("第 1 条批量标签历史影响资料：归档标签资料 -> 追加标签：已审", response)
        self.assertIn("1. data/note.txt", response)
        self.assertIn("2. data/zeta.md", response)
        self.assertIn("恢复提示：给第一份资料打标签 项目 助手 归档；给第二份资料打标签 项目 归档", response)
        self.assertIn("可继续操作：读取第一份资料；给第一份资料打标签 标签；/tag-history", response)
        self.assertIn("第 2 份资料：data/zeta.md", followup)
        self.assertIn("第二份项目标签资料", followup)

    def test_read_tagged_documents_history_documents_marks_missing_documents(self):
        zeta_path = self.paths.data_dir / "zeta.md"
        zeta_path.write_text("第二份项目标签资料。\n", encoding="utf-8")
        self.agent.handle("/tag note.txt 项目 助手")
        self.agent.handle("/tag zeta.md 项目")
        self.agent.handle("给项目标签资料都打标签 归档")
        self.agent.handle("确认执行")
        restarted_agent = JarvisAgent(self.paths)
        zeta_path.unlink()

        response = restarted_agent.handle("读取第一条标签历史资料")

        self.assertIn("1. data/note.txt", response)
        self.assertIn("2. data/zeta.md（资料缺失）", response)
        self.assertIn("恢复提示：给第一份资料打标签 项目 助手；给第二份资料打标签 项目", response)
        self.assertIn("可继续操作：读取第一份资料；给第一份资料打标签 标签；/tag-history", response)

    def test_natural_language_recent_context_status_reports_restored_search_results(self):
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        self.agent.handle("/ask Jarvis Lite 使用什么？")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("最近上下文状态")

        self.assertIn("最近上下文", response)
        self.assertIn("最近资料：data/memory.md", response)
        self.assertIn("最近搜索结果：2 条", response)
        self.assertIn("1. data/memory.md", response)
        self.assertIn("2. data/runtime.md", response)

    def test_natural_language_recent_context_status_reports_restored_advice(self):
        self.agent.handle("/experience-advice 导入资料")
        restarted_agent = JarvisAgent(self.paths)

        response = restarted_agent.handle("最近上下文状态")

        self.assertIn("最近上下文", response)
        self.assertIn("最近建议：3 条", response)
        self.assertIn("1. /import 源文件或目录路径 [目标文件名]", response)
        self.assertIn("待确认建议命令：无", response)

    def test_import_command_adds_text_file_to_knowledge_base(self):
        source = Path(self.temp_dir.name) / "outside.md"
        source.write_text("Jarvis Lite 可以导入外部资料。\n", encoding="utf-8")

        response = self.agent.handle(f"/import {source}")

        self.assertIn("已导入知识库", response)
        self.assertIn("data/outside.md", response)
        self.assertIn("外部资料", self.agent.handle("/ask Jarvis Lite 可以导入什么？"))

    def test_import_command_reports_missing_argument(self):
        response = self.agent.handle("/import")

        self.assertIn("用法：/import", response)

    def test_import_command_can_import_directory(self):
        source_dir = Path(self.temp_dir.name) / "batch"
        source_dir.mkdir()
        (source_dir / "alpha.md").write_text("Jarvis Lite 可以批量导入资料。\n", encoding="utf-8")
        (source_dir / "skip.png").write_text("跳过", encoding="utf-8")

        response = self.agent.handle(f"/import {source_dir}")

        self.assertIn("已导入知识库：2 个文件", response)
        self.assertIn("成功 1 个", response)
        self.assertIn("跳过 1 个", response)
        self.assertIn("批量导入资料", self.agent.handle("/ask Jarvis Lite 可以批量导入什么？"))

    def test_import_command_can_import_chat_json(self):
        source = Path(self.temp_dir.name) / "chat.json"
        source.write_text(
            json.dumps([{"role": "assistant", "content": "Jarvis Lite 可以导入聊天记录。"}], ensure_ascii=False),
            encoding="utf-8",
        )

        response = self.agent.handle(f"/import {source}")

        self.assertIn("已导入知识库", response)
        self.assertIn("data/chat.md", response)
        self.assertIn("聊天记录", self.agent.handle("/ask 聊天记录"))

    def test_list_command_uses_data_tool(self):
        response = self.agent.handle("/list")

        self.assertIn("note.txt", response)
        self.assertIn("list_data", (self.paths.logs_dir / "jarvis.log").read_text(encoding="utf-8"))

    def test_plain_message_mentions_loaded_memory_summary(self):
        response = self.agent.handle("随便聊聊")

        self.assertIn("Jarvis Lite", response)
        self.assertIn("用户偏好：中文简洁回答", response)

    def test_greeting_does_not_use_plain_memory_summary_fallback(self):
        response = self.agent.handle("你好")

        self.assertIn("Jarvis Lite", response)
        self.assertNotIn("已读取长期记忆", response)
        self.assertNotIn("用户偏好：中文简洁回答", response)

    def test_plain_message_does_not_duplicate_punctuation(self):
        (self.paths.memory_dir / "profile.md").write_text(
            "# 长期记忆\n\n- 项目目标：本地助手。\n",
            encoding="utf-8",
        )

        response = self.agent.handle("你好")

        self.assertNotIn("。。", response)

    def test_plain_question_uses_matching_data_document(self):
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 推荐使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )

        response = self.agent.handle("Jarvis Lite 推荐使用什么 Python 版本？")

        self.assertIn("根据 data/runtime.md:1", response)
        self.assertIn("Python 3.13", response)

    def test_local_natural_language_intent_does_not_call_llm(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("总结知识库")

        self.assertIn("知识库摘要", response)
        self.assertEqual(provider.calls, [])
        self.assertNotIn("不应使用外脑", response)

    def test_data_answer_does_not_call_llm(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"不应使用外脑"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 推荐使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )

        response = agent.handle("Jarvis Lite 推荐使用什么 Python 版本？")

        self.assertIn("Python 3.13", response)
        self.assertEqual(provider.calls, [])

    def test_llm_command_intent_is_executed_by_agent(self):
        provider = FakeLLMProvider('{"type":"command","command":"/kb-summary","reason":"用户想看资料摘要"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("请判断跨星际预算优先级")

        self.assertIn("知识库摘要", response)
        self.assertEqual(len(provider.calls), 1)
        self.assertEqual(provider.calls[0][0], "请判断跨星际预算优先级")

    def test_llm_command_intent_rejects_unknown_command_before_agent_execution(self):
        provider = FakeLLMProvider('{"type":"command","command":"/unknown","reason":"错误命令"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("请判断跨星际预算优先级")

        self.assertIn("LLM 外脑拒绝执行未列入白名单的命令：/unknown", response)
        self.assertNotIn("未知命令：/unknown", response)
        self.assertEqual(len(provider.calls), 1)

    def test_llm_fallback_context_includes_recent_next_actions(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"可以继续处理最近资料"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        agent.handle("/read note.txt")
        response = agent.handle("请规划一个外部判断任务")

        self.assertIn("LLM 外脑：可以继续处理最近资料", response)
        self.assertEqual(len(provider.calls), 1)
        context = provider.calls[0][1]
        self.assertIn("最近资料：data/note.txt", context)
        self.assertIn("下一步建议：继续处理最近资料：/read note.txt；/tag note.txt 标签...", context)

    def test_llm_fallback_context_includes_recent_search_results(self):
        provider = FakeLLMProvider('{"type":"answer","answer":"可以基于最近搜索结果规划"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )

        ask_response = agent.handle("/ask Jarvis Lite 使用什么？")
        response = agent.handle("请判断跨星际预算优先级")

        self.assertIn("data/memory.md", ask_response)
        self.assertIn("data/runtime.md", ask_response)
        self.assertIn("LLM 外脑：可以基于最近搜索结果规划", response)
        self.assertEqual(len(provider.calls), 1)
        context = provider.calls[0][1]
        self.assertIn("最近搜索结果：2 条", context)
        self.assertIn("1. data/memory.md", context)
        self.assertIn("2. data/runtime.md", context)

    def test_llm_clarification_intent_asks_without_execution(self):
        provider = FakeLLMProvider('{"type":"clarify","clarification":"你想整理哪个目录？"}')
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("火星基地预算需要外部判断")

        self.assertIn("LLM 外脑需要补充信息：你想整理哪个目录？", response)
        self.assertEqual(len(provider.calls), 1)

    def test_llm_clarification_followup_reuses_original_prompt_and_executes_final_command(self):
        provider = SequenceLLMProvider(
            [
                LLMIntent(type="clarify", clarification="你想看知识库还是最近文件？"),
                LLMIntent(type="command", command="/kb-summary", reason="用户补充了知识库"),
            ]
        )
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        first_response = agent.handle("帮我判断下一步")
        second_response = agent.handle("知识库")

        self.assertIn("LLM 外脑需要补充信息：你想看知识库还是最近文件？", first_response)
        self.assertIn("已补齐外脑需要的信息，继续处理。", second_response)
        self.assertIn("LLM 外脑建议执行命令：/kb-summary", second_response)
        self.assertIn("知识库摘要", second_response)
        self.assertEqual(len(provider.calls), 2)
        second_prompt, second_context = provider.calls[1]
        self.assertIn("原始问题：帮我判断下一步", second_prompt)
        self.assertIn("外脑澄清问题：你想看知识库还是最近文件？", second_prompt)
        self.assertIn("用户补充：知识库", second_prompt)
        self.assertIn("LLM 澄清补充：知识库", second_context)

    def test_llm_clarification_followup_can_return_answer(self):
        provider = SequenceLLMProvider(
            [
                LLMIntent(type="clarify", clarification="你想让我从哪个方向判断？"),
                LLMIntent(type="answer", answer="建议先整理知识库，再补充搜索来源。"),
                LLMIntent(type="answer", answer="新的外脑回答"),
            ]
        )
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        first_response = agent.handle("帮我判断下一步")
        second_response = agent.handle("从资料完整性判断")
        third_response = agent.handle("再判断一次")

        self.assertIn("LLM 外脑需要补充信息：你想让我从哪个方向判断？", first_response)
        self.assertIn("已补齐外脑需要的信息，继续处理。", second_response)
        self.assertIn("LLM 外脑：建议先整理知识库，再补充搜索来源。", second_response)
        self.assertIn("LLM 外脑：新的外脑回答", third_response)
        self.assertEqual(len(provider.calls), 3)
        self.assertEqual(provider.calls[2][0], "再判断一次")

    def test_llm_clarification_can_be_cancelled_without_second_provider_call(self):
        provider = SequenceLLMProvider([LLMIntent(type="clarify", clarification="你想整理哪个目录？")])
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        first_response = agent.handle("帮我判断下一步")
        second_response = agent.handle("取消补充")

        self.assertIn("LLM 外脑需要补充信息：你想整理哪个目录？", first_response)
        self.assertIn("已取消这次外脑补充", second_response)
        self.assertEqual(len(provider.calls), 1)

    def test_llm_clarification_pending_survives_new_agent_instance(self):
        provider = SequenceLLMProvider(
            [
                LLMIntent(type="clarify", clarification="你想看知识库还是最近文件？"),
                LLMIntent(type="command", command="/kb-summary", reason="用户补充了知识库"),
            ]
        )
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        first_response = agent.handle("帮我判断下一步")
        restarted_agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))
        second_response = restarted_agent.handle("知识库")

        self.assertIn("LLM 外脑需要补充信息：你想看知识库还是最近文件？", first_response)
        self.assertIn("已补齐外脑需要的信息，继续处理。", second_response)
        self.assertIn("LLM 外脑建议执行命令：/kb-summary", second_response)
        self.assertEqual(len(provider.calls), 2)
        second_prompt, second_context = provider.calls[1]
        self.assertIn("原始问题：帮我判断下一步", second_prompt)
        self.assertIn("外脑澄清问题：你想看知识库还是最近文件？", second_prompt)
        self.assertIn("用户补充：知识库", second_prompt)
        self.assertIn("LLM 澄清补充：知识库", second_context)

    def test_recent_context_reports_pending_llm_clarification_without_consuming_it(self):
        provider = SequenceLLMProvider(
            [
                LLMIntent(type="clarify", clarification="你想看知识库还是最近文件？"),
                LLMIntent(type="answer", answer="建议先看知识库。"),
            ]
        )
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        agent.handle("帮我判断下一步")
        context_response = agent.handle("/recent-context")
        followup_response = agent.handle("知识库")

        self.assertIn("待补充外脑问题：你想看知识库还是最近文件？", context_response)
        self.assertIn("外脑原始问题：帮我判断下一步", context_response)
        self.assertIn("可回复缺失信息继续，或回复“取消补充”。", context_response)
        self.assertIn("LLM 外脑：建议先看知识库。", followup_response)
        self.assertEqual(len(provider.calls), 2)

    def test_llm_clarification_cancel_clears_persisted_pending(self):
        provider = SequenceLLMProvider([LLMIntent(type="clarify", clarification="你想整理哪个目录？")])
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        agent.handle("帮我判断下一步")
        restarted_agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))
        cancel_response = restarted_agent.handle("取消补充")
        new_provider = SequenceLLMProvider([LLMIntent(type="answer", answer="新的外脑判断")])
        after_cancel_agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), new_provider))
        after_cancel_response = after_cancel_agent.handle("火星基地预算需要外部判断")

        self.assertIn("已取消这次外脑补充", cancel_response)
        self.assertIn("LLM 外脑：新的外脑判断", after_cancel_response)
        self.assertEqual(new_provider.calls[0][0], "火星基地预算需要外部判断")

    def test_llm_clarification_reclarify_preserves_original_prompt_and_reports_round(self):
        provider = SequenceLLMProvider(
            [
                LLMIntent(type="clarify", clarification="你想看知识库还是最近文件？"),
                LLMIntent(type="clarify", clarification="还需要哪个时间范围？"),
                LLMIntent(type="answer", answer="建议先看最近一周的知识库。"),
            ]
        )
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        first_response = agent.handle("帮我判断下一步")
        second_response = agent.handle("知识库")
        context_response = agent.handle("/recent-context")
        third_response = agent.handle("最近一周")

        self.assertIn("LLM 外脑需要补充信息：你想看知识库还是最近文件？", first_response)
        self.assertIn("LLM 外脑仍需要补充信息（第 2/3 轮）：还需要哪个时间范围？", second_response)
        self.assertIn("澄清轮次：2/3", context_response)
        self.assertIn("LLM 外脑：建议先看最近一周的知识库。", third_response)
        self.assertEqual(len(provider.calls), 3)
        third_prompt, third_context = provider.calls[2]
        self.assertIn("原始问题：帮我判断下一步", third_prompt)
        self.assertNotIn("原始问题：原始问题：", third_prompt)
        self.assertIn("外脑澄清问题：还需要哪个时间范围？", third_prompt)
        self.assertIn("LLM 澄清补充：最近一周", third_context)

    def test_llm_clarification_max_rounds_clears_pending(self):
        provider = SequenceLLMProvider(
            [
                LLMIntent(type="clarify", clarification="第一轮问题？"),
                LLMIntent(type="clarify", clarification="第二轮问题？"),
                LLMIntent(type="clarify", clarification="第三轮问题？"),
                LLMIntent(type="clarify", clarification="第四轮问题？"),
            ]
        )
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        agent.handle("帮我判断下一步")
        agent.handle("补充一")
        agent.handle("补充二")
        limit_response = agent.handle("补充三")
        new_provider = SequenceLLMProvider([LLMIntent(type="answer", answer="新的外脑判断")])
        restarted_agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), new_provider))
        after_limit_response = restarted_agent.handle("新的问题")

        self.assertIn("LLM 外脑连续追问过多，已结束这次外脑补充。", limit_response)
        self.assertIsNone(load_runtime_context(self.paths).pending_llm_clarification)
        self.assertIn("LLM 外脑：新的外脑判断", after_limit_response)
        self.assertEqual(new_provider.calls[0][0], "新的问题")

    def test_expired_llm_clarification_pending_is_cleared_on_startup(self):
        context_path = runtime_context_path(self.paths)
        context_path.parent.mkdir(parents=True, exist_ok=True)
        context_path.write_text(
            json.dumps(
                {
                    "pending_llm_clarification": {
                        "original_prompt": "旧问题",
                        "clarification": "旧澄清",
                        "context": ["旧上下文"],
                        "created_at": "2000-01-01T00:00:00",
                        "clarification_count": 1,
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        provider = SequenceLLMProvider([LLMIntent(type="answer", answer="新的外脑判断")])
        agent = JarvisAgent(self.paths, llm_router=LLMRouter(LLMSettings(provider="fake"), provider))

        response = agent.handle("新的问题")

        self.assertIn("LLM 外脑：新的外脑判断", response)
        self.assertEqual(provider.calls[0][0], "新的问题")
        self.assertIsNone(load_runtime_context(self.paths).pending_llm_clarification)

    def test_llm_usage_is_recorded_when_provider_returns_usage(self):
        class UsageProvider:
            name = "fake"

            def complete_intent(self, prompt, context):
                return LLMIntent(
                    type="answer",
                    answer="带用量的回答",
                    usage=LLMUsage(
                        provider="fake",
                        model="intent-test",
                        input_tokens=10,
                        output_tokens=3,
                        total_tokens=13,
                    ),
                )

        agent = JarvisAgent(
            self.paths,
            llm_router=LLMRouter(LLMSettings(provider="fake", model="intent-test"), UsageProvider()),
        )

        response = agent.handle("火星基地预算需要外部判断")

        log_content = (self.paths.logs_dir / "jarvis.log").read_text(encoding="utf-8")
        self.assertIn("LLM 外脑：带用量的回答", response)
        self.assertIn(
            "LLM 外脑用量：provider=fake model=intent-test input_tokens=10 output_tokens=3 total_tokens=13",
            log_content,
        )

    def test_ask_command_reports_no_match(self):
        response = self.agent.handle("/ask 今天晚饭吃什么？")

        self.assertIn("没有在 data 目录找到", response)

    def test_ask_command_returns_multiple_data_sources(self):
        (self.paths.data_dir / "runtime.md").write_text(
            "Jarvis Lite 使用 Python 3.13 系列运行。\n",
            encoding="utf-8",
        )
        (self.paths.data_dir / "memory.md").write_text(
            "Jarvis Lite 使用 memory/profile.md 保存长期记忆。\n",
            encoding="utf-8",
        )

        response = self.agent.handle("/ask Jarvis Lite 使用什么？")

        self.assertIn("data/memory.md:1", response)
        self.assertIn("data/runtime.md:1", response)

    def test_remember_command_appends_long_term_memory(self):
        response = self.agent.handle("/remember 用户姓名：张三")

        self.assertIn("已记住", response)
        self.assertIn("用户姓名：张三", (self.paths.memory_dir / "profile.md").read_text(encoding="utf-8"))

    def test_plain_identity_statement_is_saved_to_memory(self):
        response = self.agent.handle("我叫张三")

        self.assertIn("已记住", response)
        self.assertIn("用户姓名：张三", (self.paths.memory_dir / "profile.md").read_text(encoding="utf-8"))

    def test_plain_role_statement_is_saved_to_memory(self):
        response = self.agent.handle("我是Jarvis Lite项目创建者")

        self.assertIn("已记住", response)
        self.assertIn("用户身份：Jarvis Lite项目创建者", (self.paths.memory_dir / "profile.md").read_text(encoding="utf-8"))

    def test_identity_question_uses_long_term_memory(self):
        self.agent.handle("我叫张三")
        self.agent.handle("我是Jarvis Lite项目创建者")

        response = self.agent.handle("你知道我是谁吗")

        self.assertIn("你是张三", response)
        self.assertIn("Jarvis Lite项目创建者", response)

    def test_identity_update_replaces_old_name(self):
        self.agent.handle("我叫张三")
        self.agent.handle("我叫李四")

        response = self.agent.handle("我是谁")
        content = (self.paths.memory_dir / "profile.md").read_text(encoding="utf-8")

        self.assertIn("你是李四", response)
        self.assertNotIn("用户姓名：张三", content)
        self.assertEqual(content.count("用户姓名："), 1)


if __name__ == "__main__":
    unittest.main()
