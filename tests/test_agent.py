import sys
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths


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

    def test_status_command_reports_current_capabilities(self):
        response = self.agent.handle("/status")

        self.assertIn("Jarvis Lite 当前状态", response)
        self.assertIn("长期记忆", response)
        self.assertIn("个人知识库", response)
        self.assertIn("工具日志", response)
        self.assertIn("自然语言", response)
        self.assertIn("桌面能力", response)
        self.assertIn("memory/profile.md", response)

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
                    "version": "0.2.0",
                    "download_url": "https://example.com/JarvisLiteSetup.exe",
                    "release_notes": "新增更新检查。",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        response = self.agent.handle(f"/update-status {manifest}")

        self.assertIn("发现新版本：0.2.0", response)
        self.assertIn("当前版本：0.1.0", response)
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
                        "version": "0.2.0",
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
        response = self.agent.handle("你好")

        self.assertIn("Jarvis Lite", response)
        self.assertIn("用户偏好：中文简洁回答", response)

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
