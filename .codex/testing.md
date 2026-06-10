# 测试记录

> 日期：2026-05-18
> 执行者：Codex

## 测试策略

本阶段使用 Python 标准库 `unittest`，不引入第三方测试依赖。

## TDD 红灯记录

### 初始模块缺失

命令：

```powershell
python -m unittest discover -s tests -v
```

结果：

- 4 个测试模块导入失败。
- 失败原因：`ModuleNotFoundError: No module named 'jarvis_lite'`。
- 判定：符合预期，测试先定义了尚未实现的包接口。

### data 目录占位文件外露

命令：

```powershell
python -m unittest tests.test_tools.ToolRegistryTests.test_list_data_hides_project_placeholder_files -v
```

结果：

- 失败原因：`list_data` 输出 `.gitkeep`。
- 修复：目录列表跳过点文件。

### 记忆摘要误取 Markdown 元信息

命令：

```powershell
python -m unittest tests.test_memory.MemoryTests.test_summarize_profile_skips_markdown_metadata -v
```

结果：

- 失败原因：摘要返回 `> 日期：2026-05-18`。
- 修复：摘要提取跳过 Markdown 引用元信息。

### 普通回复重复标点

命令：

```powershell
python -m unittest tests.test_agent.AgentTests.test_plain_message_does_not_duplicate_punctuation -v
```

结果：

- 失败原因：回复中出现 `。。`。
- 修复：统一句子结尾处理。

### 阶段状态路径分隔符

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_status_command_reports_phase_one_capabilities -v
```

结果：

- 失败原因：`/status` 在 Windows 上输出 `memory\profile.md`，不符合文档中统一使用的项目相对路径格式。
- 修复：状态页路径统一使用 `Path.as_posix()` 输出。

### 阶段 2 知识库索引缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_build_knowledge_index_counts_supported_documents_and_searchable_lines -v
```

结果：

- 失败原因：`knowledge.py` 尚未提供 `build_knowledge_index`。
- 修复：新增 `KnowledgeIndex`、`KnowledgeDocument` 和 `build_knowledge_index`。

### 阶段 2 知识库状态命令缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_knowledge_status_command_reports_data_index -v
```

结果：

- 失败原因：Agent 尚未识别 `/kb`，返回未知命令。
- 修复：新增 `/kb` 和 `/knowledge` 命令，输出个人知识库状态。

### 阶段 2 资料导入函数缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_import_knowledge_file_copies_supported_text_into_data -v
```

结果：

- 失败原因：`knowledge.py` 尚未提供 `import_knowledge_file`。
- 修复：新增 Markdown/txt 导入函数，导入到 `data/` 并返回可检索行数。

### 阶段 2 资料导入命令缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_import_command_adds_text_file_to_knowledge_base -v
```

结果：

- 失败原因：Agent 尚未识别 `/import`，返回未知命令。
- 修复：新增 `/import 源文件路径 [目标文件名]` 命令。

### 阶段 2 目录批量导入缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_import_knowledge_path_imports_supported_files_from_directory -v
```

结果：

- 失败原因：`knowledge.py` 尚未提供 `import_knowledge_path`。
- 修复：新增路径导入分发，支持递归导入目录中的 Markdown/txt。

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_import_command_can_import_directory -v
```

结果：

- 失败原因：`/import` 把目录当作文件处理。
- 修复：`/import` 改为调用 `import_knowledge_path`，并输出批量导入摘要。

### 阶段 2 /ask 具体版本排序不足

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_search_data_prioritizes_specific_version_term_over_generic_terms -v
```

结果：

- 失败原因：泛化资料和包含 `3.13` 的具体资料分数相同，现有排序按文件名把 `alpha.md` 放在 `zeta.md` 前面。
- 修复：包含数字或版本号的查询词命中权重提高，具体版本资料优先。

### 阶段 2 /ask 回答缺少摘要编号

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_answer_from_data_numbers_multiple_sources_after_summary -v
```

结果：

- 失败原因：回答直接输出来源片段，没有命中数量摘要和编号。
- 修复：`answer_from_data` 输出 `我在 data 目录找到 N 条相关资料：`，并按序号列出来源。

### 阶段 2 知识库标签 API 缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_set_document_tags_persists_normalized_tags_in_index -v
```

结果：

- 失败原因：`knowledge.py` 尚未提供 `set_document_tags`。
- 修复：新增 `data/.knowledge-tags.json` 元数据读写、标签规范化和 `KnowledgeDocument.tags`。

### 阶段 2 标签命令缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_tag_command_updates_document_tags -v
```

结果：

- 失败原因：Agent 尚未识别 `/tag`，返回未知命令。
- 修复：新增 `/tag 文件名 标签...` 命令，写入资料标签并记录日志。

### 阶段 2 PDF 导入缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_import_knowledge_file_converts_pdf_to_markdown_document -v
```

结果：

- 失败原因：`import_knowledge_file` 只支持 `.md` 和 `.txt`，拒绝 `.pdf`。
- 修复：新增 `pypdf>=6,<7` 依赖，PDF 导入时抽取文本并转换成同名 Markdown。

### 阶段 2 JSON 聊天记录导入缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_import_knowledge_file_converts_chat_json_to_markdown_document -v
```

结果：

- 失败原因：`import_knowledge_file` 拒绝 `.json`。
- 修复：新增聊天记录 JSON 转 Markdown，支持列表格式和 `messages` 对象格式。

### 阶段 2 目录批量导入 PDF/JSON 目标名错误

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_import_knowledge_path_imports_pdf_and_json_from_directory -v
```

结果：

- 失败原因：目录导入把 `manual.pdf` 作为目标名传入后没有转换成 `manual.md`。
- 修复：对 PDF/JSON 目录导入目标名统一改为 Markdown 后缀。

### 阶段 3 语音模块缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_voice.VoiceTests.test_speak_text_records_transcript_in_transcript_engine -v
```

结果：

- 失败原因：尚未提供 `jarvis_lite.voice` 模块。
- 修复：新增 `voice.py`，支持 `describe_voice`、`speak_text` 和 transcript 播报记录。

### 阶段 3 语音命令缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_voice_status_command_reports_voice_entry -v
```

结果：

- 失败原因：Agent 尚未识别 `/voice-status`，返回未知命令。
- 修复：新增 `/voice-status`、`/speak 文本` 和 `/voice 已识别的语音文本`。

### 阶段 4 工作台自动化模块缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_add_common_directory_persists_alias_and_path -v
```

结果：

- 失败原因：尚未提供 `jarvis_lite.automation` 模块。
- 修复：新增 `automation.py`，支持常用目录登记、列表和日报生成。

### 阶段 4 自动化命令缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_automation_status_command_reports_workspace_automation -v
```

结果：

- 失败原因：Agent 尚未识别 `/automation-status`，返回未知命令。
- 修复：新增 `/automation-status`、`/dir-add`、`/dirs` 和 `/daily-report`。

## 最终验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 80 个测试全部通过。

命令：

```powershell
python src/app.py --once "/memory"
python src/app.py --once "/list"
python src/app.py --once "你好"
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe src/app.py --once "/status"
.\.venv\Scripts\python.exe src/app.py --once "/kb"
.\.venv\Scripts\python.exe src/app.py --once "/import .codex/import-smoke.md import-smoke.md"
.\.venv\Scripts\python.exe src/app.py --once "/import .codex/import-smoke-dir"
.\.venv\Scripts\python.exe src/app.py --once "/ask Jarvis Lite 使用什么 Python 版本？"
.\.venv\Scripts\python.exe src/app.py --once "Jarvis Lite 当前可以读取什么？"
.\.venv\Scripts\python.exe src/app.py --once "/ask Jarvis Lite 当前可以什么？"
@'
hello
/history
/save-summary cli-smoke
/exit
'@ | .\.venv\Scripts\python.exe -X utf8 src/app.py
@'
我叫测试用户
我是Jarvis Lite测试者
你知道我是谁吗
/exit
'@ | .\.venv\Scripts\python.exe -X utf8 src/app.py
```

结果：

- `/memory` 输出 `memory/profile.md`。
- `/list` 输出 `data 目录为空。`。
- 普通输入输出 Jarvis Lite 记忆摘要。
- `logs/jarvis.log` 记录了 `list_data` 工具调用。
- 项目虚拟环境使用 Python 3.13.2。
- `/status` 输出阶段 1 状态、长期记忆、data 文本问答和工具日志位置。
- `/kb` 输出个人知识库状态、支持格式、资料文件数量和可检索行数。
- `/import` 可以导入 Markdown/txt 文件或目录到 `data/`，导入后可被 `/kb` 和 `/ask` 使用。
- `/ask` 可以基于 `data/jarvis-lite.md` 返回带来源的回答。
- `/ask` 回答包含命中数量摘要和编号。
- 包含数字或版本号的查询词可以优先命中更具体资料。
- `/tag` 可以给资料设置标签，`/kb` 可以展示标签，`/ask` 可以通过标签命中资料。
- `/import` 可以把 PDF 和 JSON 聊天记录转换为 Markdown 后进入知识库。
- `/voice-status`、`/speak` 和 `/voice` 覆盖阶段 3 第一批语音入口能力；自动化验证使用 transcript 引擎。
- `/automation-status`、`/dir-add`、`/dirs` 和 `/daily-report` 覆盖阶段 4 第一批非硬件工作台自动化能力。
- 普通问题可以自动命中 `data/` 资料。
- 多片段问题可以返回多个强相关来源，并过滤弱相关片段。
- 交互式 CLI 可以记录当前会话、查看历史并保存会话总结。
- 长期记忆写入和身份问答通过 CLI 冒烟验证；测试后恢复原始 `memory/profile.md`。
- 同 key 长期记忆更新测试通过，身份改名后回答使用新姓名。

## 2026-05-19 阶段 4 推送前复验

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 80 个测试全部通过。

命令：

```powershell
@'
import tempfile
from pathlib import Path
from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths

with tempfile.TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)
    paths = build_project_paths(root)
    project_dir = root / "project"
    project_dir.mkdir()
    agent = JarvisAgent(paths)
    print(agent.handle("/automation-status"))
    print(agent.handle(f"/dir-add 项目 {project_dir}"))
    print(agent.handle("/dirs"))
    print(agent.handle("/daily-report today.md"))
    report_path = paths.word_dir / "today.md"
    print(f"REPORT_EXISTS={report_path.is_file()}")
'@ | .\.venv\Scripts\python.exe -X utf8 -
```

结果：

- `/automation-status` 输出阶段 4 状态，并明确摄像头、麦克风暂缓。
- `/dir-add 项目 <临时目录>` 可登记常用目录。
- `/dirs` 可列出刚登记的目录。
- `/daily-report today.md` 生成 `word/today.md`，`REPORT_EXISTS=True`。

## 2026-05-19 文件整理预览验证

### RED：核心函数缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_preview_file_organization_groups_files_by_extension -v
```

结果：

- 失败原因：`jarvis_lite.automation` 尚未提供 `preview_file_organization`。
- 修复：新增整理预览数据结构和 `preview_file_organization`，按扩展名分组并跳过子目录。

### RED：Agent 命令缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_organize_preview_command_reports_plan_for_common_directory -v
```

结果：

- 失败原因：Agent 尚未识别 `/organize-preview`。
- 修复：接入 `/organize-preview 常用目录别名`，复用常用目录登记数据输出整理预览。

### 最终验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 82 个测试全部通过。

命令：

```powershell
@'
import tempfile
from pathlib import Path
from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths

with tempfile.TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)
    paths = build_project_paths(root)
    project_dir = root / "project"
    project_dir.mkdir()
    (project_dir / "notes.md").write_text("笔记", encoding="utf-8")
    (project_dir / "todo.txt").write_text("待办", encoding="utf-8")
    (project_dir / "README").write_text("无后缀", encoding="utf-8")
    (project_dir / "nested").mkdir()
    agent = JarvisAgent(paths)
    print(agent.handle("/automation-status"))
    print(agent.handle(f"/dir-add 项目 {project_dir}"))
    print(agent.handle("/dirs"))
    print(agent.handle("/daily-report today.md"))
    print(agent.handle("/organize-preview 项目"))
    print(f"REPORT_EXISTS={(paths.word_dir / 'today.md').is_file()}")
'@ | .\.venv\Scripts\python.exe -X utf8 -
```

结果：

- `/organize-preview 项目` 输出 3 个文件的整理预览，按 `md/`、`txt/` 和 `no-extension/` 分组。
- 整理预览显示跳过 1 个子目录。
- 输出明确说明只生成预览，不会移动或删除文件。

## 2026-05-19 常用目录打开记录验证

### RED：记录函数缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_record_directory_open_request_writes_transcript -v
```

结果：

- 失败原因：`jarvis_lite.automation` 尚未提供 `record_directory_open_request`。
- 修复：新增 `DirectoryOpenRecord` 和 transcript 写入函数，写入 `logs/desktop-actions.txt`。

### RED：Agent 命令缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_dir_open_command_records_dry_run_request -v
```

结果：

- 失败原因：Agent 尚未接入 `/dir-open`，因此没有生成 `logs/desktop-actions.txt`。
- 修复：新增 `/dir-open 常用目录别名`，复用常用目录登记数据并记录打开目录请求。

### 最终验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 84 个测试全部通过。

命令：

```powershell
@'
import tempfile
from pathlib import Path
from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths

with tempfile.TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)
    paths = build_project_paths(root)
    project_dir = root / "project"
    project_dir.mkdir()
    (project_dir / "notes.md").write_text("笔记", encoding="utf-8")
    (project_dir / "todo.txt").write_text("待办", encoding="utf-8")
    (project_dir / "README").write_text("无后缀", encoding="utf-8")
    (project_dir / "nested").mkdir()
    agent = JarvisAgent(paths)
    print(agent.handle("/automation-status"))
    print(agent.handle(f"/dir-add 项目 {project_dir}"))
    print(agent.handle("/dirs"))
    print(agent.handle("/daily-report today.md"))
    print(agent.handle("/organize-preview 项目"))
    print(agent.handle("/dir-open 项目"))
    print(f"REPORT_EXISTS={(paths.word_dir / 'today.md').is_file()}")
    print((paths.logs_dir / "desktop-actions.txt").read_text(encoding="utf-8"))
'@ | .\.venv\Scripts\python.exe -X utf8 -
```

结果：

- `/dir-open 项目` 输出记录文件位置和当前不会启动外部应用。
- `logs/desktop-actions.txt` 包含 `open_directory`、常用目录别名和目标路径。

## 2026-05-19 桌面助手素材、运行态设置和状态动效验证

### RED：运行态设置文件损坏

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
```

结果：

- 新增 `test_load_settings_falls_back_to_defaults_when_runtime_file_is_invalid` 后失败。
- 失败原因：`load_desktop_settings()` 对损坏 JSON 直接抛出 `JSONDecodeError`。
- 修复：读取运行态设置时捕获解析错误并回退默认位置。

### RED：状态动效缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
```

结果：

- 新增状态动效 profile 和帧推进测试后失败。
- 失败原因：`DesktopPetWindow` 还没有 `current_animation_name()`、`animation_interval_ms()`、`animation_frame()` 和 `advance_animation_frame()`。
- 修复：使用 `QTimer` 和状态动效 profile 驱动角色素材轻量缩放。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_assets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
```

结果：

- 桌面素材测试 2 个通过。
- 桌面设置测试 3 个通过。
- 桌面 widget 测试 8 个通过。
- 全量测试 103 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。

## 2026-05-19 桌面助手托盘生命周期验证

### RED：托盘模块缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
```

结果：

- 失败原因：`ModuleNotFoundError: No module named 'jarvis_lite.desktop.tray'`。
- 修复：新增 `DesktopTrayController`，提供托盘菜单、显示助手、隐藏助手和退出应用。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
```

结果：

- 桌面入口测试 3 个通过。
- 桌面托盘测试 3 个通过；Qt minimal 插件在窗口可见性测试中输出 `This plugin does not support raise()`，但命令退出码为 0。
- 全量测试 106 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。

## 2026-05-19 桌面助手设置面板验证

### RED：运行态偏好设置缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
```

结果：

- 失败原因：`save_desktop_preferences` 尚不存在，`DesktopSettings` 也没有置顶、透明度和小助手尺寸字段。
- 修复：扩展 `DesktopSettings`，新增偏好保存读取，并让保存位置时保留已有偏好。

### RED：设置面板和小助手设置应用接口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
```

结果：

- 失败原因：`AssistantPanel` 尚不接受初始设置，没有设置回调；`DesktopPetWindow` 缺少 `apply_preferences()`、`is_always_on_top()` 等接口。
- 修复：面板新增置顶复选框、透明度滑块和尺寸滑块；小助手启动时恢复设置，变更时立即应用并写入运行态文件。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 桌面设置测试 6 个通过。
- 桌面 widget 测试 12 个通过。
- 桌面入口测试 3 个通过。
- 桌面托盘测试 3 个通过；Qt minimal 插件仍会输出 `This plugin does not support raise()`，退出码为 0。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 全量测试 113 个通过。

## 2026-05-19 桌面托盘快捷命令验证

### RED：托盘快捷命令接口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
```

结果：

- 失败原因：`DesktopTrayController` 缺少 `quick_command_texts()` 和 `quick_command_action()`。
- 修复：托盘菜单新增状态、知识库、常用目录和生成日报 4 个快捷命令 action。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 桌面托盘测试 5 个通过；Qt minimal 插件仍会输出 `This plugin does not support raise()`，退出码为 0。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 全量测试 115 个通过。

## 2026-05-20 桌面托盘最近结果验证

### RED：面板最近结果接口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_tracks_last_result_after_submission -v
```

结果：

- 失败原因：`AssistantPanel` 缺少 `last_result_text()`。
- 修复：`AssistantPanel.submit_text()` 保存本轮用户输入和助手输出，并返回 `DesktopResponse`。

### RED：托盘最近结果入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
```

结果：

- 失败原因：`DesktopTrayController` 缺少 `recent_result_action` 和 `recent_result_text()`。
- 修复：托盘菜单新增“最近结果”入口，快捷命令执行后更新运行态最近结果；点击最近结果只显示面板，不重复执行命令。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 桌面 widget 测试 13 个通过。
- 桌面托盘测试 8 个通过；Qt minimal 插件仍会输出 `This plugin does not support raise()`，退出码为 0。
- 全量测试 119 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误。

## 2026-05-20 桌面面板尺寸持久化验证

### RED：运行态设置缺少面板宽高

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
```

结果：

- 失败原因：`save_desktop_panel_size` 不存在，`DesktopSettings` 缺少 `panel_width` 和 `panel_height`。
- 修复：`DesktopSettings` 新增面板宽高字段，运行态 JSON 读写包含面板宽高，并新增 `save_desktop_panel_size()`。

### RED：面板未恢复或保存宽高

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
```

结果：

- 失败原因：`AssistantPanel` 初始化仍使用 Qt 默认宽高，resize 后没有写入运行态设置；`DesktopPetWindow.apply_preferences()` 会把面板宽高重置为默认值。
- 修复：`AssistantPanel` 按设置恢复宽高，并在 resize/close 时保存尺寸；小助手偏好保存时保留已有面板宽高。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 桌面设置测试 8 个通过。
- 桌面 widget 测试 15 个通过。
- 桌面入口测试 3 个通过。
- 全量测试 123 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误。

## 2026-05-20 桌面体验收口验证

### RED：应用图标和应用身份缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_assets tests.test_desktop_app tests.test_desktop_tray -v
```

结果：

- 失败原因：`desktop_app_icon_path()` 不存在，应用名仍是默认 `python`。
- 修复：新增应用图标素材、应用图标路径函数，并在桌面 app、面板、小助手窗口和托盘中使用统一图标。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_assets tests.test_desktop_app tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 桌面资产、入口和托盘测试合计 15 个通过。
- 全量测试 125 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误。

## 2026-05-20 桌面打包前准备验证

### RED：冻结运行态和打包参数缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_config tests.test_desktop_packaging -v
```

结果：

- 失败原因：冻结运行态仍指向源码根目录，`jarvis_lite.desktop.packaging` 模块不存在。
- 修复：冻结运行态默认使用 `%LOCALAPPDATA%\Jarvis Lite`；新增 PyInstaller 参数生成、桌面 launcher、打包脚本和 `desktop-build` 可选依赖。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_config tests.test_desktop_packaging -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 配置和桌面打包准备测试合计 5 个通过。
- 全量测试 129 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误。

## 2026-05-20 Windows 桌面安装器验证

### RED：安装器脚本和 SED 生成缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v
```

结果：

- 失败原因：`jarvis_lite.desktop.windows_installer` 模块不存在。
- 修复：新增安装脚本、卸载脚本、IExpress SED 文件生成和 `scripts/build_windows_installer.py`。

### 构建命令

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[desktop-build]"
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
```

结果：

- PyInstaller 6.20.0 安装成功。
- 构建生成 `E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe`。
- IExpress 构建生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- Windows 安装器测试 3 个通过。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。
- 全量测试 132 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误。

## 2026-05-20 Windows 安装产物元数据验证

### RED：Windows 图标、版本资源和安装器版本串联缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_packaging -v
.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v
```

结果：

- `tests.test_desktop_packaging` 失败原因：`render_windows_version_info` 等版本资源函数不存在。
- `tests.test_windows_installer` 失败原因：`render_install_script()` 不支持传入 `version` 参数。
- 修复：新增 Windows `.ico` 图标、版本资源生成、PyInstaller 元数据参数和安装脚本版本号参数。

### 构建命令

```powershell
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
```

结果：

- 构建生成 `E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe`。
- 构建生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- PyInstaller 日志包含 `Copying icon to EXE` 和 `Copying version information to EXE`。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_packaging -v
.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
git diff --check
```

结果：

- 桌面打包测试 7 个通过。
- Windows 安装器测试 4 个通过。
- 全量测试 137 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。
- `JarvisLite.exe` 的 `FileDescription` 为 `Jarvis Lite desktop assistant`，`ProductName` 为 `Jarvis Lite`，`FileVersion` 和 `ProductVersion` 均为 `0.1.0`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。

## 2026-05-20 桌面开机自启动验证

### 现状审查

命令：

```powershell
git status --short --branch
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- `main...origin/main`，无未提交变更。
- 全量测试 137 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。
- 未发现必须先修的回归问题。

### RED：开机启动模块、设置字段和面板开关缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_autostart -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
```

结果：

- `tests.test_desktop_autostart` 失败原因：`jarvis_lite.desktop.autostart` 模块不存在。
- `tests.test_desktop_settings` 失败原因：`DesktopSettings` 缺少 `launch_at_login`。
- `tests.test_desktop_widgets` 失败原因：面板设置值和 `change_settings()` 不支持 `launch_at_login`。
- `tests.test_desktop_app` 失败原因：缺少 `apply_panel_settings`。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_autostart -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- 桌面开机启动测试 7 个通过。
- 桌面设置测试 8 个通过。
- 桌面 widget 测试 15 个通过。
- 桌面入口测试 6 个通过。
- 全量测试 146 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-20 桌面主题预设验证

### RED：主题 API 和运行态主题字段缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_style -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
```

结果：

- `tests.test_desktop_style` 先因 `jarvis_lite.desktop.app_style` 缺少主题 API 失败。
- `tests.test_desktop_settings` 先因 `DesktopSettings` 缺少 `theme_name` 失败。
- `tests.test_desktop_widgets` 先因面板设置值和小助手偏好不支持主题失败。
- `tests.test_desktop_app` 先因 `apply_panel_settings()` 不传递 `theme_name` 失败。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_style -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- 桌面主题样式测试 3 个通过。
- 桌面设置测试 9 个通过。
- 桌面 widget 测试 16 个通过。
- 桌面入口测试 6 个通过。
- 全量测试 151 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-20 桌面面板快捷命令收口验证

### RED：无参数快捷命令筛选和面板入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v
```

结果：

- `tests.test_desktop_bridge` 先因缺少 `direct_quick_commands()` 失败。
- `tests.test_desktop_widgets` 先因 `AssistantPanel` 缺少 `quick_command_texts()` 和 `quick_command_button()` 失败。
- `tests.test_desktop_tray` 先因无法导入无参数快捷命令集合失败。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- 桌面桥接层、widget 和托盘专项测试共 30 个通过。
- 全量测试 154 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-20 桌面安装生命周期收口验证

### RED：卸载生命周期和覆盖安装前置处理缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v
```

结果：

- `test_install_script_prepares_for_cover_install_and_complete_uninstall_metadata` 先因安装脚本缺少进程关闭、`DisplayIcon` 和 `QuietUninstallString` 失败。
- `test_uninstall_script_removes_startup_shortcut_and_stops_running_app` 先因卸载脚本缺少 Startup 清理和运行进程关闭失败。
- `test_uninstall_script_preserves_user_data_directory` 先因卸载脚本缺少用户数据保留约定失败。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- Windows 安装器专项测试 7 个通过。
- 全量测试 157 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-20 桌面更新检查第一版验证

### RED：更新模块、命令和桌面入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v
```

结果：

- `tests.test_update` 先因 `jarvis_lite.update` 模块不存在失败。
- `tests.test_agent` 先因 `/update-status` 未接入失败。
- `tests.test_desktop_bridge` 先因快捷命令缺少 `/update-status` 失败。
- `tests.test_desktop_widgets` 先因面板快捷按钮缺少“检查更新”失败。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- 更新模块、Agent、桌面桥接、widget 和托盘专项测试共 64 个通过。
- 全量测试 162 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-21 桌面更新下载体验验证

### RED：更新下载函数、命令和桌面入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets -v
```

结果：

- `tests.test_update` 先因缺少 `describe_update_download` 和 `download_update` 导致导入失败。
- `tests.test_agent` 先因 `/update-download` 返回未知命令失败。
- `tests.test_desktop_bridge` 先因快捷命令缺少 `/update-download` 失败。
- `tests.test_desktop_widgets` 先因面板快捷按钮缺少“下载更新”失败。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets -v
```

结果：

- 更新模块、Agent、桌面桥接和 widget 专项测试共 60 个通过。
- 过程中发现 Windows 本地路径 `C:\...` 会被 `urlparse` 识别为 `c` 协议，已通过优先识别 Windows 路径修复。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- 全量测试 166 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。
- 安装器重新生成成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-21 自然语言本地大脑第一版验证

### RED：自然语言常用意图缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v
```

结果：

- `tests.test_memory` 先因 `我是你的什么人，你知道吗` 未识别为身份问题失败。
- `tests.test_agent` 先因自然语言能力询问、生成日报、查看知识库、检查更新和打开 D 盘都落入通用兜底失败。
- `/status` 旧断言仍要求“阶段 1 状态”，与当前完整状态不一致。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v
```

结果：

- 记忆和 Agent 专项测试共 46 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 173 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。

## 2026-05-21 常用目录别名自然语言验证

### RED：打开和整理常用目录别名缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- `打开项目目录` 先未记录打开目录请求。
- `整理项目目录` 先落入通用兜底，未返回文件整理预览。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 39 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 175 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 已知桌面目录自然语言验证

### RED：整理桌面和打开桌面缺少系统目录 fallback

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_desktop_uses_known_desktop_directory tests.test_agent.AgentTests.test_natural_language_open_desktop_uses_known_desktop_directory -v
```

结果：

- `整理桌面` 先返回 `没有找到常用目录：桌面`。
- `打开桌面` 先没有写入 `logs/desktop-actions.txt`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_desktop_uses_known_desktop_directory tests.test_agent.AgentTests.test_natural_language_open_desktop_uses_known_desktop_directory -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 已知桌面目录新增 2 个测试通过。
- Agent 专项测试 41 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 177 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 资料标签自然语言验证

### RED：自然语言标签表达未映射到 /tag

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_mark_document_as_tags_updates_document_tags -v
```

结果：

- `给 note.txt 打标签 项目 Python` 先落入普通兜底，没有更新标签。
- `把 note.txt 标记为 私人资料` 先被当作资料问答，没有更新标签。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_mark_document_as_tags_updates_document_tags -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 自然语言资料标签新增 2 个测试通过。
- Agent 专项测试 43 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 179 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 自然语言导入资料验证

### RED：自然语言导入表达未映射到 /import

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_import_file_adds_document_to_knowledge_base tests.test_agent.AgentTests.test_natural_language_import_quoted_file_path_adds_document_to_knowledge_base -v
```

结果：

- `导入 <路径> 到知识库` 先落入普通兜底，没有导入资料。
- `把 "<带空格路径>" 导入知识库` 先落入普通兜底，没有导入资料。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_import_file_adds_document_to_knowledge_base tests.test_agent.AgentTests.test_natural_language_import_quoted_file_path_adds_document_to_knowledge_base -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 自然语言导入资料新增 2 个测试通过。
- Agent 专项测试 45 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 181 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近资料上下文验证

### RED：这个资料无法指向最近导入资料

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_imported_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_tag_recent_document_requires_recent_document_context -v
```

结果：

- 导入单个资料后，`给这个资料打标签 项目 Python` 先把 `这个资料` 当成真实文件名，标签更新失败。
- 未导入资料时，`给这个资料打标签 项目` 先把 `这个资料` 当成真实文件名，未给出最近资料缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_imported_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_tag_recent_document_requires_recent_document_context -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近资料上下文新增 2 个测试通过。
- Agent 专项测试 47 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 183 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近目录上下文验证

### RED：这个目录无法指向最近目录

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_recent_directory_after_open_common_directory tests.test_agent.AgentTests.test_natural_language_open_recent_directory_requires_recent_directory_context -v
```

结果：

- 打开 `项目` 常用目录后，`整理这个目录` 先把 `这个` 当成常用目录别名，提示没有找到常用目录。
- 未打开或整理目录时，`打开这个目录` 先把 `这个` 当成常用目录别名，未给出最近目录缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_recent_directory_after_open_common_directory tests.test_agent.AgentTests.test_natural_language_open_recent_directory_requires_recent_directory_context -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近目录上下文新增 2 个测试通过。
- Agent 专项测试 49 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 185 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近搜索结果上下文验证

### RED：这个结果无法指向最近搜索命中

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_plain_question -v
```

结果：

- `/ask Python 3.13` 命中 `data/runtime.md` 后，`给这个结果打标签 运行环境` 先把 `这个结果` 当成真实文件名，标签更新失败。
- 普通问题命中 `data/runtime.md` 后，`给这个结果打标签 运行环境` 同样先把 `这个结果` 当成真实文件名，标签更新失败。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_plain_question -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近搜索结果上下文新增 2 个测试通过。
- Knowledge 专项测试 23 个通过。
- Agent 专项测试 51 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 187 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近搜索结果编号选择验证

### RED：无法选择第二条搜索结果

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_requires_recent_results -v
```

结果：

- `/ask Jarvis Lite 使用什么？` 返回两条资料后，`给第二条结果打标签 运行环境` 先把 `第二条结果` 当成真实文件名，标签更新失败。
- 未提问时，`给第二条结果打标签 运行环境` 同样先把 `第二条结果` 当成真实文件名，未给出最近搜索结果缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_requires_recent_results -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 最近搜索结果编号选择新增 2 个测试通过。
- Agent 专项测试 53 个通过。
- Knowledge 专项测试 23 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 189 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 查看编号搜索结果验证

### RED：无法查看第二条搜索结果

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_requires_recent_results -v
```

结果：

- `/ask Jarvis Lite 使用什么？` 返回两条资料后，`查看第二条结果` 先落入长期记忆兜底，没有读取第二条资料。
- 未提问时，`查看第二条结果` 先落入长期记忆兜底，未给出最近搜索结果缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_requires_recent_results tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_requires_recent_results -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 查看编号搜索结果新增 2 个测试通过。
- 编号搜索结果相关 4 个测试通过。
- Agent 专项测试 55 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 191 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近搜索结果持久化验证

### RED：新 Agent 实例无法恢复最近搜索结果

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_search_results_survive_new_agent_instance -v
```

结果：

- 第一个 Agent 执行 `/ask Jarvis Lite 使用什么？` 后，新建第二个 Agent 再说 `查看第二条结果`，先提示还没有最近搜索结果。

### 根因与修复

- 根因：最近搜索结果列表只保存在 `JarvisAgent` 实例内。
- 修复：新增 `runtime_context.py`，把最近搜索结果路径列表写入项目外 `jarvis-lite-runtime/agent-context.json`，并在 Agent 初始化时恢复。
- 测试隔离：Agent 测试根目录改为临时目录下的 `jarvis-lite` 子目录，避免运行态文件写到系统临时目录的公共父级而串扰测试。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_search_results_survive_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近搜索结果持久化新增 1 个测试通过。
- Agent 专项测试 56 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 192 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近上下文状态查询验证

### RED：自然语言最近上下文查询缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_empty_state tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_current_context tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_search_results -v
```

结果：

- `查看最近上下文` 先落入长期记忆兜底，没有输出最近上下文空状态。
- `你还记得刚才什么` 先落入长期记忆兜底，没有展示最近资料、最近目录和最近搜索结果。
- `最近上下文状态` 在新 Agent 实例中也先落入长期记忆兜底，没有展示已恢复的搜索结果。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_empty_state tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_current_context tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_search_results -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近上下文状态新增 3 个测试通过。
- Agent 专项测试 59 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 195 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近资料和最近目录持久化验证

### RED：新 Agent 实例无法恢复最近资料和最近目录

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_imported_document_survives_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_directory_survives_new_agent_instance -v
```

结果：

- 最近资料测试先失败：重启后响应为“还没有最近资料”。
- 最近目录测试先失败：重启后响应为“还没有最近目录”。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_imported_document_survives_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_directory_survives_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近资料持久化新增 1 个测试通过。
- 最近目录持久化新增 1 个测试通过。
- Agent 专项测试 61 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 197 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 经验记忆第一版验证

### RED：缺少独立经验记忆入口

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experiences_command_reports_empty_state tests.test_agent.AgentTests.test_experience_command_records_experience tests.test_agent.AgentTests.test_natural_language_record_experience_records_experience tests.test_agent.AgentTests.test_natural_language_experience_memory_status_maps_to_experiences -v
```

结果：

- `tests.test_memory` 先因缺少 `append_experience` 和 `read_experiences` 导入失败。
- `/experience` 和 `/experiences` 先返回未知命令。
- “记住这个经验：...” 先被误写入长期记忆。
- “查看经验记忆” 先落入长期记忆兜底。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Memory 专项测试 11 个通过。
- Agent 专项测试 65 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 203 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 经验引用第一版验证

### RED：能力摘要和日报未引用经验

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory.MemoryTests.test_list_recent_experiences_returns_latest_items_first -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_capability_question_reports_recent_experiences -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_write_daily_report_creates_word_markdown -v
```

结果：

- `tests.test_memory` 先因缺少 `list_recent_experiences` 导入失败。
- 能力摘要先没有“最近经验”内容。
- 日报先没有“经验记忆”段。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent tests.test_automation -v
```

结果：

- Memory、Agent、Automation 专项测试共 83 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 205 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 经验搜索第一版验证

### RED：经验关键词检索入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory.MemoryTests.test_search_experiences_returns_matching_items_latest_first -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experience_search_command_returns_matching_experiences tests.test_agent.AgentTests.test_experience_search_command_reports_no_match tests.test_agent.AgentTests.test_experience_search_command_requires_keyword tests.test_agent.AgentTests.test_natural_language_search_experience_maps_to_experience_search -v
```

结果：

- `tests.test_memory` 先因缺少 `search_experiences` 导入失败。
- `/experience-search` 先返回未知命令。
- “搜索经验 导入”先未映射到经验搜索命令。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v
```

结果：

- Memory 和 Agent 专项测试共 83 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 210 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 经验操作建议第一版验证

### RED：经验建议入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experience_advice_command_returns_related_experiences tests.test_agent.AgentTests.test_experience_advice_command_reports_no_related_experience tests.test_agent.AgentTests.test_experience_advice_command_requires_keyword tests.test_agent.AgentTests.test_natural_language_experience_advice_uses_related_experiences -v
```

结果：

- `/experience-advice` 相关 3 个测试先返回未知命令。
- “我该怎么导入资料”先落入资料问答，没有引用经验建议。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 74 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 214 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 经验建议命令联动第一版验证

### RED：经验建议缺少可执行命令

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experience_advice_command_suggests_import_commands tests.test_agent.AgentTests.test_experience_advice_command_suggests_known_commands_without_experience tests.test_agent.AgentTests.test_natural_language_experience_advice_includes_command_suggestions -v
```

结果：

- `/experience-advice 导入资料` 先只有相关经验，没有“可执行命令”。
- `/experience-advice 生成日报` 先只提示缺少经验，没有 `/daily-report [文件名]`。
- “导入资料有什么建议”先没有输出 `/import 源文件或目录路径 [目标文件名]`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 77 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 217 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 经验建议引用最近上下文第一版验证

### RED：经验建议无法引用最近资料和目录

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experience_advice_for_recent_document_uses_recent_document_context tests.test_agent.AgentTests.test_experience_advice_for_recent_document_requires_recent_context tests.test_agent.AgentTests.test_experience_advice_for_recent_directory_uses_recent_directory_context -v
```

结果：

- `/experience-advice 这个资料` 先只按字面输出通用资料命令，没有当前资料和具体 `/read`、`/tag`。
- 缺少最近资料时先没有“还没有最近资料”的明确提示。
- `/experience-advice 这个目录` 先只输出通用目录命令，没有当前目录和具体 `/organize-preview 项目`、`/dir-open 项目`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 80 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 220 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近建议编号查看第一版验证

### RED：无法查看编号建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_first_advice_after_experience_advice tests.test_agent.AgentTests.test_natural_language_read_numbered_advice_after_experience_advice tests.test_agent.AgentTests.test_natural_language_read_advice_requires_recent_advice -v
```

结果：

- “查看第一条建议”先落入普通兜底，没有读取最近建议。
- “查看第二条建议”同样落入普通兜底。
- 没有最近建议时没有明确提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 83 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 223 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近建议持久化第一版验证

### RED：新 Agent 无法恢复最近建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_advice_suggestions_survive_new_agent_instance -v
```

结果：

- 新增测试先失败，新建 `JarvisAgent` 后返回“还没有最近建议”，无法读取上一轮 `/experience-advice` 的建议。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_advice_suggestions_survive_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近建议持久化单测通过。
- Agent 专项测试 84 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 224 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近建议执行前确认第一版验证

### RED：无法准备或确认执行建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice tests.test_agent.AgentTests.test_natural_language_prepare_advice_requires_completed_parameters tests.test_agent.AgentTests.test_natural_language_confirm_advice_requires_pending_command -v
```

结果：

- “执行第二条建议”先落入长期记忆兜底，没有准备待确认命令。
- “执行第一条建议”先落入长期记忆兜底，没有提示补充参数。
- “确认执行”先落入长期记忆兜底，没有提示缺少待确认命令。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice tests.test_agent.AgentTests.test_natural_language_prepare_advice_requires_completed_parameters tests.test_agent.AgentTests.test_natural_language_confirm_advice_requires_pending_command -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近建议执行前确认 3 个新增测试通过。
- Agent 专项测试 87 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 227 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近建议状态展示第一版验证

### RED：最近上下文不展示最近建议状态

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_advice tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_advice_command tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_advice -v
```

结果：

- 生成建议后，“查看最近上下文”仍返回“还没有记录”，没有展示最近建议。
- 准备执行建议后，“查看最近上下文”没有展示待确认建议命令。
- 新建 Agent 恢复最近建议后，“最近上下文状态”仍没有展示最近建议。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_advice tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_advice_command tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_advice -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近建议状态展示 3 个新增测试通过。
- Agent 专项测试 90 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 230 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 建议命令参数补全草稿验证

### RED：占位符建议缺少命令草稿

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_prepare_advice_with_missing_parameters_returns_command_draft -v
```

结果：

- 新增测试先失败，`执行第一条建议` 仍只提示需要补充参数，没有输出 `命令草稿：/import <源文件或目录路径> [目标文件名]`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_prepare_advice_with_missing_parameters_returns_command_draft tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice tests.test_agent.AgentTests.test_natural_language_prepare_advice_requires_completed_parameters -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 建议命令参数补全草稿新增测试通过。
- 最近建议执行相关 3 个测试通过，完整命令确认执行行为未回归。
- Agent 专项测试 91 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 231 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 草稿参数接收第一版验证

### RED：补全草稿后直接执行

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_completed_advice_command_draft_waits_for_confirmation -v
```

结果：

- 新增测试先失败，拿到 `/import` 命令草稿后输入完整 `/import 路径` 会直接返回“已导入知识库”，没有进入待确认建议命令状态。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_completed_advice_command_draft_waits_for_confirmation tests.test_agent.AgentTests.test_natural_language_prepare_advice_with_missing_parameters_returns_command_draft tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 草稿参数接收新增测试通过。
- 最近建议执行相关 3 个测试通过。
- Agent 专项测试 92 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 232 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 已知下载目录自然语言验证

### RED：下载目录缺少系统目录 fallback

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_downloads_uses_known_downloads_directory tests.test_agent.AgentTests.test_natural_language_open_downloads_uses_known_downloads_directory -v
```

结果：

- 新增测试先失败，`整理下载目录` 返回 `没有找到常用目录：下载`。
- `打开下载目录` 没有写入 `logs/desktop-actions.txt`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_downloads_uses_known_downloads_directory tests.test_agent.AgentTests.test_natural_language_open_downloads_uses_known_downloads_directory tests.test_agent.AgentTests.test_natural_language_organize_desktop_uses_known_desktop_directory tests.test_agent.AgentTests.test_natural_language_open_desktop_uses_known_desktop_directory -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 下载目录新增 2 个测试通过。
- 桌面和下载目录 fallback 相关 4 个测试通过。
- Agent 专项测试 94 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 234 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 已知项目目录自然语言验证

### RED：项目目录缺少项目根目录 fallback

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_project_uses_known_project_directory tests.test_agent.AgentTests.test_natural_language_open_project_uses_known_project_directory -v
```

结果：

- 新增测试先失败，`整理项目目录` 返回 `没有找到常用目录：项目`。
- `打开项目目录` 返回 `没有找到常用目录：项目`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_project_uses_known_project_directory tests.test_agent.AgentTests.test_natural_language_open_project_uses_known_project_directory tests.test_agent.AgentTests.test_natural_language_open_common_directory_alias_records_request tests.test_agent.AgentTests.test_natural_language_organize_common_directory_alias_returns_preview -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 项目目录新增 2 个测试通过。
- 项目目录 fallback 与用户登记项目目录优先级相关 4 个测试通过。
- Agent 专项测试 96 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 236 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 知识库问答证据增强验证

### RED：知识库回答缺少命中原因和继续操作

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_answer_from_data_reports_match_reason_and_follow_up_actions -v
```

结果：

- 新增测试先失败，回答只包含 `我在 data 目录找到 1 条相关资料` 和 `根据 data/jarvis.txt:1`，没有“命中原因”和“可继续操作”。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_answer_from_data_reports_match_reason_and_follow_up_actions tests.test_knowledge.KnowledgeTests.test_answer_from_data_includes_source_and_matching_content tests.test_knowledge.KnowledgeTests.test_answer_from_data_numbers_multiple_sources_after_summary tests.test_knowledge.KnowledgeTests.test_answer_from_data_can_include_multiple_sources -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 知识库问答证据增强新增 1 个测试通过。
- Knowledge 专项测试 24 个通过。
- Agent 专项测试 96 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 237 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 日报运行态上下文联动验证

### RED：日报缺少最近上下文

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context -v
```

结果：

- 新增测试先失败，生成的日报包含长期记忆、知识库、常用目录、经验记忆和最近工具日志，但没有 `## 最近上下文`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context tests.test_automation.AutomationTests.test_write_daily_report_creates_word_markdown -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 日报运行态上下文新增 1 个测试通过。
- Automation 专项测试 6 个通过。
- Agent 专项测试 96 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 238 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 日报下一步建议生成验证

### RED：日报缺少下一步建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context -v
```

结果：

- 新增测试先失败，生成的日报没有 `## 下一步建议`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context tests.test_automation.AutomationTests.test_write_daily_report_creates_word_markdown -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 日报下一步建议新增 1 个测试通过。
- Automation 专项测试 7 个通过。
- Agent 专项测试 96 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 239 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 读取资料写入最近上下文验证

### RED：/read 不更新最近资料

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_command_sets_persistent_recent_document_context -v
```

结果：

- 新增测试先失败，`/read manual.md` 成功后，新 Agent 实例仍然返回“还没有最近资料”。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_command_sets_persistent_recent_document_context -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 读取资料写入最近上下文新增 1 个测试通过。
- Agent 专项测试 97 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 240 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 自然语言读取资料验证

### RED：自然语言读取资料落入兜底

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_document_updates_recent_document_context -v
```

结果：

- 新增测试先失败，“读取 manual.md”返回长期记忆兜底，没有返回 `manual.md` 的文件内容。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_document_updates_recent_document_context tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_first_advice_after_experience_advice -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 自然语言读取资料新增 1 个测试通过。
- 编号搜索结果和编号建议读取回归测试通过。
- Agent 专项测试 98 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 241 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 自然语言读取最近资料验证

### RED：读取这个资料落入普通检索

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_recent_document_reads_current_document tests.test_agent.AgentTests.test_natural_language_read_recent_document_requires_recent_context -v
```

结果：

- 新增测试先失败，“读取这个资料”落入普通知识库检索并命中 `note.txt`，没有读取最近资料。
- 无最近资料时也落入普通检索，没有明确提示“还没有最近资料”。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_recent_document_reads_current_document tests.test_agent.AgentTests.test_natural_language_read_recent_document_requires_recent_context tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_first_advice_after_experience_advice -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 自然语言读取最近资料新增 2 个测试通过。
- 编号搜索结果和编号建议读取回归测试通过。
- Agent 专项测试 100 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 243 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近资料列表验证

### RED：最近上下文和日报缺少最近资料列表

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_document_list tests.test_agent.AgentTests.test_recent_document_list_survives_new_agent_instance tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context -v
```

结果：

- 新增测试先失败，“查看最近上下文”只显示单个最近资料，没有“最近资料列表：2 条”。
- 新建 Agent 实例后也只能恢复单个最近资料。
- 日报读取运行态上下文时忽略 `recent_document_paths`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_document_list tests.test_agent.AgentTests.test_recent_document_list_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_read_recent_document_reads_current_document tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation -v
```

结果：

- 最近资料列表新增 2 个 Agent 测试通过，读取当前资料回归通过，日报最近上下文测试通过。
- Agent 专项测试 102 个通过。
- Automation 专项测试 7 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 245 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 按编号读取最近资料验证

### RED：读取第二份资料落入普通检索

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_reads_selected_document tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_requires_recent_list tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_does_not_override_search_result -v
```

结果：

- 新增测试先失败，“读取第二份资料”落入普通知识库检索，没有读取最近资料列表中的第 2 份资料。
- 缺少最近资料列表时也落入普通检索，没有明确提示“还没有最近资料列表”。
- “查看第二条结果”仍然走最近搜索结果路径，回归测试通过。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_reads_selected_document tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_requires_recent_list tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_does_not_override_search_result tests.test_agent.AgentTests.test_natural_language_read_recent_document_reads_current_document -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 按编号读取最近资料新增 3 个 Agent 测试通过，当前资料读取回归通过。
- Agent 专项测试 105 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 248 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 按编号给最近资料打标签验证

### RED：给第二份资料打标签落入普通文件名

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_updates_selected_document_tags tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_requires_recent_list tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command -v
```

结果：

- 新增测试先失败，“给第二份资料打标签 项目 Python”把“第二份资料”当作普通文件名传给 `/tag`。
- 缺少最近资料列表时也没有明确提示“还没有最近资料列表”。
- “给第二条结果打标签”仍然走最近搜索结果路径，回归测试通过。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_updates_selected_document_tags tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_requires_recent_list tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_reads_selected_document -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 按编号给最近资料打标签新增 2 个 Agent 测试通过，搜索结果编号打标签和编号读取最近资料回归通过。
- Agent 专项测试 107 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 250 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 系统最近文件列表第一版验证

### RED：最近文件入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_list_recent_files_returns_top_level_files_newest_first tests.test_agent.AgentTests.test_natural_language_recent_files_reports_known_project_files_newest_first tests.test_agent.AgentTests.test_recent_files_command_reports_empty_state -v
```

结果：

- 新增 Automation 测试先因 `list_recent_files` 不存在而失败。
- “查看最近文件”先落入长期记忆兜底，没有展示最近文件。
- `/recent-files` 先返回未知命令。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_list_recent_files_returns_top_level_files_newest_first tests.test_agent.AgentTests.test_natural_language_recent_files_reports_known_project_files_newest_first tests.test_agent.AgentTests.test_recent_files_command_reports_empty_state -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation -v
```

结果：

- 最近文件列表新增 1 个 Automation 测试和 2 个 Agent 测试通过。
- Agent 专项测试 109 个通过。
- Automation 专项测试 8 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 253 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 按编号查看最近文件详情验证

### RED：第一份最近文件没有编号意图

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_file_reports_file_metadata tests.test_agent.AgentTests.test_recent_file_list_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_file_requires_recent_files -v
```

结果：

- 新增测试先失败，“查看第一份最近文件”落入长期记忆兜底。
- `/recent-files` 生成的最近文件列表不能跨 Agent 实例恢复。
- 缺少最近文件列表时没有明确提示先查看最近文件。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_file_reports_file_metadata tests.test_agent.AgentTests.test_recent_file_list_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_file_requires_recent_files -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation -v
```

结果：

- 按编号查看最近文件详情新增 3 个 Agent 测试通过。
- Agent 专项测试 112 个通过。
- Automation 专项测试 8 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 256 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近文件纳入最近上下文和日报验证

### RED：最近文件缺少上下文联动

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_file_list tests.test_agent.AgentTests.test_recent_file_list_survives_new_agent_instance_in_recent_context tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context -v
```

结果：

- “查看最近上下文”先没有展示最近文件列表。
- 新 Agent 实例恢复最近文件列表后，最近上下文状态仍未展示最近文件。
- 日报“最近上下文”和“下一步建议”先没有读取 `recent_files`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_file_list tests.test_agent.AgentTests.test_recent_file_list_survives_new_agent_instance_in_recent_context tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation -v
```

结果：

- 最近文件上下文联动新增/扩展 4 个测试通过。
- Agent 专项测试 114 个通过。
- Automation 专项测试 8 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 258 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近上下文下一步建议验证

### RED：最近上下文缺少下一步建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_suggests_next_actions -v
```

结果：

- 已准备最近资料、最近目录、最近文件和最近建议时，“查看最近上下文”先没有 `下一步建议：` 段。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_suggests_next_actions tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation -v
```

结果：

- 最近上下文下一步建议新增 1 个 Agent 测试通过。
- 日报下一步建议回归测试通过。
- Agent 专项测试 115 个通过。
- Automation 专项测试 8 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 259 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-23 桌面最近上下文和最近文件快捷入口验证

### RED：桌面快捷入口缺少最近上下文和最近文件

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_quick_commands_include_current_assistant_capabilities tests.test_desktop_bridge.DesktopBridgeTests.test_direct_quick_commands_exclude_commands_that_need_arguments -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_only_direct_quick_command_buttons tests.test_desktop_widgets.DesktopWidgetTests.test_panel_recent_context_quick_command_submits_natural_language_prompt -v
```

结果：

- 桌面桥接层快捷命令先没有 `查看最近上下文` 和 `/recent-files`。
- 面板快捷按钮先没有“最近上下文”，点击测试出现 `KeyError`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
```

结果：

- Desktop bridge 专项测试 4 个通过。
- Desktop widgets 专项测试 19 个通过。
- Desktop tray 专项测试 8 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 260 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-23 按编号导入最近文件验证

### RED：最近文件编号导入被误当成普通路径

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_import_numbered_recent_file_adds_document_to_knowledge_base tests.test_agent.AgentTests.test_natural_language_import_numbered_recent_file_requires_recent_files tests.test_agent.AgentTests.test_natural_language_import_numbered_recent_file_reports_out_of_range -v
```

结果：

- “导入第一份最近文件到知识库”先返回 `导入失败：源路径不存在：第一份最近文件`。
- 缺少最近文件列表时没有提示先查看最近文件。
- 编号越界时没有提示最近文件列表数量。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_import_numbered_recent_file_adds_document_to_knowledge_base tests.test_agent.AgentTests.test_natural_language_import_numbered_recent_file_requires_recent_files tests.test_agent.AgentTests.test_natural_language_import_numbered_recent_file_reports_out_of_range -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 按编号导入最近文件新增 3 个 Agent 测试通过。
- Agent 专项测试 118 个通过。
- Knowledge 专项测试 24 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 263 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-25 知识库摘要增强

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_reports_document_previews_with_sources tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_reports_empty_state tests.test_agent.AgentTests.test_knowledge_summary_command_reports_document_previews tests.test_agent.AgentTests.test_natural_language_knowledge_summary_maps_to_summary -v
```

结果：

- `summarize_knowledge_base` 缺失导致 Knowledge 测试导入失败。
- `/kb-summary` 返回未知命令。
- “总结知识库”落入长期记忆兜底。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_reports_document_previews_with_sources tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_reports_empty_state tests.test_agent.AgentTests.test_knowledge_summary_command_reports_document_previews tests.test_agent.AgentTests.test_natural_language_knowledge_summary_maps_to_summary -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 目标测试 4 个通过。
- Knowledge 专项测试 26 个通过。
- Agent 专项测试 120 个通过。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 267 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-25 知识库摘要联动最近资料上下文

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_numbered_followups tests.test_agent.AgentTests.test_knowledge_summary_command_sets_recent_document_list_for_numbered_followups tests.test_agent.AgentTests.test_knowledge_summary_document_list_survives_new_agent_instance -v
```

结果：

- `/kb-summary` 缺少可继续操作提示。
- 摘要后读取第二份资料失败，提示没有最近资料列表。
- 新 Agent 实例不能恢复摘要中的资料列表。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_numbered_followups tests.test_agent.AgentTests.test_knowledge_summary_command_sets_recent_document_list_for_numbered_followups tests.test_agent.AgentTests.test_knowledge_summary_document_list_survives_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 目标测试 3 个通过。
- Agent 专项测试 123 个通过。
- Knowledge 专项测试 26 个通过。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 270 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-25 知识库摘要长预览截断

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_truncates_long_document_preview -v
```

结果：

- 长预览完整输出。
- 摘要中没有 `...` 省略标记。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_truncates_long_document_preview -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 目标测试 1 个通过。
- Knowledge 专项测试 27 个通过。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 271 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-25 最近文件导入进入下一步建议验证

### RED：最近文件建议未提示导入动作

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_suggests_next_actions tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context -v
```

结果：

- “查看最近上下文”的最近文件建议仍是 `查看第一份最近文件；/recent-files`。
- 日报“下一步建议”的最近文件建议也没有提示“导入第一份最近文件到知识库”。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_suggests_next_actions tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context -v
```

结果：

- 最近上下文和日报最近文件建议 2 个测试通过。

### 专项与收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- Agent 专项测试 118 个通过。
- Automation 专项测试 8 个通过。
- 全量测试 263 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-25 文档进度同步收尾验证

### 文档与代码对应核查

命令：

```powershell
Get-Content -Raw -LiteralPath .\日志.txt
git status --short --ignored
git log --date=iso --pretty=format:"%h %ad %s" -25
rg -n "summarize_knowledge_base|SUMMARY_PREVIEW_MAX_CHARS|import_numbered_recent_file|suggest_next_actions_from_context|recent-files|最近上下文|desktopPetWindow|kb-summary|knowledge-summary|读取第一份资料|给第一份资料打标签" src tests README.md word .codex
```

结果：

- `日志.txt` 显示上次任务在写回验证和审查留痕前遇到 `503 Service Unavailable` 中断。
- `word/` 已补齐 `2026-05-23-jarvis-lite-progress.md` 和 `2026-05-25-jarvis-lite-progress.md`，并更新 `word/文档索引.md`。
- 源码和测试中存在对应实现与覆盖：`summarize_knowledge_base()`、`SUMMARY_PREVIEW_MAX_CHARS`、`import_numbered_recent_file`、`suggest_next_actions_from_context()`、`/recent-files`、`/kb-summary`、桌面 `desktopPetWindow` smoke 和最近上下文快捷入口。
- `.codex/` 中存在对应扫描、计划、测试和审查留痕；该目录被 `.gitignore` 忽略，不进入普通 git 状态。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 271 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅提示 `word/文档索引.md` 后续会从 LF 转 CRLF。

## 2026-05-25 知识库摘要按标签分组验证

### RED：摘要没有标签分组

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_groups_documents_by_tags -v
```

结果：

- 新增测试先失败，`summarize_knowledge_base()` 输出中没有 `- 标签分组：`。
- 现有摘要直接从总数进入 `- 资料概览：`，无法先按标签扫读多资料知识库。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_groups_documents_by_tags -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_reports_document_previews_with_sources tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_truncates_long_document_preview -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 标签分组新增 1 个目标测试通过。
- 摘要来源预览和长预览截断回归测试通过。
- Knowledge 专项测试 28 个通过。
- Agent 专项测试 123 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 272 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-25 知识库摘要按标签后续建议验证

### RED：摘要没有按标签提问建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_tagged_ask_followups -v
```

结果：

- 新增测试先失败，`/kb-summary` 已有“标签分组”，但末尾没有 `按标签提问：/ask 助手；/ask 项目`。
- 现有输出只保留通用 `可继续操作：读取第一份资料；给第一份资料打标签 标签；/ask 关键词`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_tagged_ask_followups -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_numbered_followups tests.test_agent.AgentTests.test_knowledge_summary_command_sets_recent_document_list_for_numbered_followups -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 标签化 `/ask` 建议新增 1 个目标测试通过。
- 编号后续建议和最近资料上下文 2 个回归测试通过。
- Agent 专项测试 124 个通过。
- Knowledge 专项测试 28 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 273 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-25 桌面知识库摘要快捷入口验证

### RED：桌面快捷入口缺少知识库摘要

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_quick_commands_include_current_assistant_capabilities tests.test_desktop_bridge.DesktopBridgeTests.test_direct_quick_commands_exclude_commands_that_need_arguments -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_only_direct_quick_command_buttons -v
```

结果：

- `quick_commands()` 中没有 `/kb-summary`。
- `direct_quick_commands()` 和面板按钮列表中没有“知识库摘要”。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_quick_commands_include_current_assistant_capabilities tests.test_desktop_bridge.DesktopBridgeTests.test_direct_quick_commands_exclude_commands_that_need_arguments -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_only_direct_quick_command_buttons -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
```

结果：

- 桌面知识库摘要快捷入口 3 个目标测试通过。
- Desktop bridge 专项测试 4 个通过。
- Desktop widgets 专项测试 19 个通过。
- Desktop tray 专项测试 8 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 273 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-25 按标签读取知识库资料组验证

### RED：读取标签资料落入普通问答

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_tagged_documents_sets_recent_document_list tests.test_agent.AgentTests.test_natural_language_read_tagged_documents_reports_no_match -v
```

结果：

- 2 个新增 Agent 测试先失败。
- “读取项目标签资料”先被当作普通问题，返回 `我在 data 目录找到 1 条相关资料`，没有 `标签资料：项目`。
- “查看缺失标签资料”先被当作普通问题，返回 `data/note.txt` 命中，没有 `没有找到标签为“缺失”的资料`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_tagged_documents_sets_recent_document_list tests.test_agent.AgentTests.test_natural_language_read_tagged_documents_reports_no_match -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 按标签读取资料组 2 个目标测试通过。
- Agent 专项测试 126 个通过。
- Knowledge 专项测试 28 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 275 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-25 知识库摘要按标签读取建议验证

### RED：摘要没有按标签读取建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_tagged_read_followups -v
```

结果：

- 新增测试先失败。
- `/kb-summary` 已有标签分组和 `按标签提问：/ask 助手；/ask 项目`，但没有 `按标签读取：读取助手标签资料；读取项目标签资料`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_tagged_read_followups tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_tagged_ask_followups -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 按标签读取建议 1 个目标测试通过。
- 标签提问建议回归测试通过。
- Agent 专项测试 127 个通过。
- Knowledge 专项测试 28 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 276 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 标签组批量打标签前预览验证

### RED：标签组批量打标签落入普通文件名

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_preview_tagged_documents_tagging_sets_recent_document_list_without_mutation tests.test_agent.AgentTests.test_natural_language_preview_tagged_documents_tagging_reports_no_match -v
```

结果：

- 2 个新增 Agent 测试先失败。
- “给项目标签资料都打标签 归档”先落入普通 `/tag` 路径，把“项目标签资料”当成文件名并返回资料格式错误。
- “给缺失标签资料都打标签 归档”同样落入普通 `/tag` 路径，没有输出标签组缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_preview_tagged_documents_tagging_sets_recent_document_list_without_mutation tests.test_agent.AgentTests.test_natural_language_preview_tagged_documents_tagging_reports_no_match -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_mark_document_as_tags_updates_document_tags tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_updates_selected_document_tags tests.test_agent.AgentTests.test_natural_language_read_tagged_documents_sets_recent_document_list tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_tagged_read_followups -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 标签组批量打标签前预览 2 个目标测试通过。
- 普通自然语言打标签、按编号给最近资料打标签、按标签读取资料组和摘要按标签读取建议回归通过。
- Knowledge 专项测试 28 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 278 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 标签组批量打标签确认闭环验证

### RED：确认执行不识别标签组预览

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_applies_previewed_tags tests.test_agent.AgentTests.test_natural_language_cancel_tagged_documents_tagging_clears_preview -v
```

结果：

- 2 个新增 Agent 测试先失败。
- 预览后说“确认执行”仍返回“还没有待确认的建议命令”，没有写入标签。
- 预览后说“取消执行”仍返回“还没有待取消的建议命令”，没有清空标签组待确认状态。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_applies_previewed_tags tests.test_agent.AgentTests.test_natural_language_cancel_tagged_documents_tagging_clears_preview -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice tests.test_agent.AgentTests.test_natural_language_prepare_advice_requires_completed_parameters tests.test_agent.AgentTests.test_completed_advice_command_draft_waits_for_confirmation tests.test_agent.AgentTests.test_natural_language_confirm_advice_requires_pending_command tests.test_agent.AgentTests.test_natural_language_preview_tagged_documents_tagging_sets_recent_document_list_without_mutation tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 标签组批量打标签确认/取消 2 个目标测试通过。
- 经验建议确认、经验建议草稿确认、普通打标签和标签组预览回归通过。
- Knowledge 专项测试 28 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 280 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 标签组待确认状态接入最近上下文验证

### RED：最近上下文不展示批量标签待确认状态

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_tagged_documents_tagging -v
```

结果：

- 1 个新增 Agent 测试先失败。
- 预览后“查看最近上下文”只有最近资料列表和“待确认建议命令：无”，没有显示待确认批量打标签任务。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_tagged_documents_tagging -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_tagged_documents_tagging tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_advice_command tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_advice tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_empty_state tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_applies_previewed_tags tests.test_agent.AgentTests.test_natural_language_cancel_tagged_documents_tagging_clears_preview -v
```

结果：

- 标签组待确认状态目标测试通过。
- 最近上下文待确认建议、最近建议、空状态、标签组确认和取消回归 6 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 281 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 标签组批量操作恢复提示验证

### RED：确认结果缺少恢复提示

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints -v
```

结果：

- 1 个新增 Agent 测试先失败。
- 确认批量打标签后只输出更新后的标签列表，没有 `操作记录` 和 `恢复提示`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_applies_previewed_tags tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints tests.test_agent.AgentTests.test_natural_language_cancel_tagged_documents_tagging_clears_preview tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_tagged_documents_tagging tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_updates_selected_document_tags -v
```

结果：

- 标签组恢复提示目标测试通过。
- 标签组确认、恢复提示、取消、最近上下文、普通打标签和编号资料打标签回归 6 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 282 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 标签组批量操作摘要接入最近上下文验证

### RED：最近上下文缺少最近批量操作摘要

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_tagged_documents_operation -v
```

结果：

- 1 个新增 Agent 测试先失败。
- 确认批量打标签后，“查看最近上下文”只显示最近资料列表和待确认批量打标签为无，没有最近批量操作摘要和恢复提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_tagged_documents_operation -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_tagged_documents_operation tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_tagged_documents_tagging tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_empty_state tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_applies_previewed_tags tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints tests.test_agent.AgentTests.test_natural_language_cancel_tagged_documents_tagging_clears_preview -v
```

结果：

- 最近批量标签操作摘要目标测试通过。
- 最近上下文待确认批量标签、空状态、标签组确认、恢复提示和取消回归 6 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 283 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 最近批量标签操作摘要持久化验证

### RED：新 Agent 无法恢复最近批量标签摘要

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_tagged_documents_operation_survives_new_agent_instance -v
```

结果：

- 1 个新增 Agent 测试先失败。
- 新 `JarvisAgent` 实例只能恢复最近资料列表，最近上下文显示“最近批量打标签：无”。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_tagged_documents_operation_survives_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_tagged_documents_operation_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_tagged_documents_operation tests.test_agent.AgentTests.test_recent_document_list_survives_new_agent_instance tests.test_agent.AgentTests.test_recent_file_list_survives_new_agent_instance_in_recent_context tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_advice tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints tests.test_agent.AgentTests.test_natural_language_cancel_tagged_documents_tagging_clears_preview -v
```

结果：

- 最近批量标签操作摘要跨 Agent 恢复目标测试通过。
- 最近资料列表、最近文件列表、最近建议、当前批量摘要、确认恢复提示和取消回归 7 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 284 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 批量标签操作历史命令验证

### RED：批量标签历史命令不存在

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_tagged_documents_history_command_survives_new_agent_instance -v
```

结果：

- 1 个新增 Agent 测试先失败。
- `/tag-history` 返回未知命令，无法查看最近批量标签操作历史。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_tagged_documents_history_command_survives_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_tagged_documents_history_command_survives_new_agent_instance tests.test_agent.AgentTests.test_recent_tagged_documents_operation_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_tagged_documents_operation tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_applies_previewed_tags tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints tests.test_agent.AgentTests.test_natural_language_cancel_tagged_documents_tagging_clears_preview -v
```

结果：

- 批量标签历史命令跨 Agent 恢复目标测试通过。
- 最近批量摘要、标签组确认、恢复提示和取消回归 6 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 285 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 桌面批量标签历史快捷入口验证

### RED：桌面快捷入口缺少标签历史

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_quick_commands_include_current_assistant_capabilities tests.test_desktop_bridge.DesktopBridgeTests.test_direct_quick_commands_exclude_commands_that_need_arguments -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_only_direct_quick_command_buttons tests.test_desktop_widgets.DesktopWidgetTests.test_panel_tag_history_quick_command_submits_tag_history_command -v
```

结果：

- 桌面桥接层快捷命令先缺少 `/tag-history`。
- 面板快捷按钮先缺少“标签历史”，点击测试出现 `KeyError`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_quick_commands_include_current_assistant_capabilities tests.test_desktop_bridge.DesktopBridgeTests.test_direct_quick_commands_exclude_commands_that_need_arguments -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_only_direct_quick_command_buttons tests.test_desktop_widgets.DesktopWidgetTests.test_panel_tag_history_quick_command_submits_tag_history_command -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v
```

结果：

- 桌面桥接和面板目标测试通过。
- 桌面桥接、面板和托盘专项 32 个测试通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 286 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 批量标签历史影响资料读取验证

### RED：标签历史无法恢复影响资料列表

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_sets_recent_document_list -v
```

结果：

- 1 个新增 Agent 测试先失败。
- “读取第一条标签历史资料”先被普通资料问答兜底，无法恢复历史影响资料列表。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_sets_recent_document_list -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_tagged_documents_history_command_survives_new_agent_instance tests.test_agent.AgentTests.test_recent_tagged_documents_operation_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_tagged_documents_operation tests.test_agent.AgentTests.test_recent_document_list_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints -v
```

结果：

- 批量标签历史影响资料读取目标测试通过。
- 批量标签历史、最近批量摘要、最近资料列表和恢复提示回归 5 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 287 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-27 LLM 兼容端点完整 Responses URL 验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_openai_compatible_provider_normalizes_responses_endpoint_url tests.test_llm.LLMTests.test_router_describes_normalized_responses_endpoint_url -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_describe_llm_config_examples_can_filter_provider -v
```

结果：

- 兼容端点目标测试先失败，SDK client 仍收到完整 `/v1/responses` URL，状态描述未展示归一化后的 SDK Base URL。
- 配置模板目标测试先失败，输出没有提示“完整 `/v1/responses` URL”。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_openai_compatible_provider_normalizes_responses_endpoint_url tests.test_llm.LLMTests.test_router_describes_normalized_responses_endpoint_url tests.test_llm.LLMTests.test_describe_llm_config_examples_can_filter_provider -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_config_example_command_can_filter_provider -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 完整 `/v1/responses` URL 归一化、`/llm-status` 展示和配置模板专项 4 个测试通过。
- `tests.test_llm` 24 个测试通过。
- `tests.test_agent` 152 个测试通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
Markdown 本地链接检查脚本
```

结果：

- `unittest`：通过，`Ran 326 tests`，结果 `OK`。
- 桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。

## 2026-05-27 LLM smoke 调用验证命令

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_llm_smoke_command_reports_disabled_router tests.test_agent.AgentTests.test_llm_smoke_command_returns_answer_without_normal_fallback tests.test_agent.AgentTests.test_llm_smoke_command_does_not_execute_command_intent tests.test_agent.AgentTests.test_llm_smoke_command_records_usage -v
```

结果：

- 目标测试先失败。
- `/help` 未列出 `/llm-smoke`。
- `/llm-smoke` 返回未知命令。
- usage 日志测试因命令未执行而没有生成日志文件。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_llm_smoke_command_reports_disabled_router tests.test_agent.AgentTests.test_llm_smoke_command_returns_answer_without_normal_fallback tests.test_agent.AgentTests.test_llm_smoke_command_does_not_execute_command_intent tests.test_agent.AgentTests.test_llm_smoke_command_records_usage -v
```

结果：

- `/llm-smoke` 目标 5 个测试通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
Markdown 本地链接检查脚本
```

结果：

- `tests.test_agent`：通过，`Ran 156 tests`，结果 `OK`。
- `tests.test_llm`：通过，`Ran 24 tests`，结果 `OK`。
- `unittest`：通过，`Ran 330 tests`，结果 `OK`。
- 桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。

## 2026-05-26 批量标签历史资料缺失提示验证

### RED：历史资料缺失会触发文件读取错误

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_marks_missing_documents -v
```

结果：

- 目标测试先失败。
- 删除历史中的第二份资料后，“读取第一条标签历史资料”触发 `FileNotFoundError`，没有输出“资料缺失”提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_marks_missing_documents -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_sets_recent_document_list tests.test_agent.AgentTests.test_tagged_documents_history_command_survives_new_agent_instance tests.test_agent.AgentTests.test_recent_tagged_documents_operation_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_tagged_documents_operation tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints -v
```

结果：

- 批量标签历史资料缺失提示目标测试通过。
- 批量标签历史资料读取、历史列表、最近批量摘要、最近上下文和确认恢复提示回归 5 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 288 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 编号最近资料缺失提示验证

### RED：读取缺失编号资料只返回底层缺失信息

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_marks_missing_document -v
```

结果：

- 目标测试先失败。
- “读取第二份资料”输出 `第 2 份资料：data/manual.md` 后接底层 `文件不存在：manual.md`，没有明确编号资料缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_marks_missing_document -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_reads_selected_document tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_requires_recent_list tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_does_not_override_search_result tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_marks_missing_documents tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_sets_recent_document_list tests.test_agent.AgentTests.test_recent_document_list_survives_new_agent_instance -v
```

结果：

- 编号最近资料缺失提示目标测试通过。
- 编号读取、历史缺失、历史资料读取和最近资料持久化回归 6 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 289 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-27 LLM 配置诊断验证

### RED：状态命令不展示配置问题

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_router_describes_openai_missing_configuration tests.test_llm.LLMTests.test_router_describes_openai_compatible_missing_base_url tests.test_llm.LLMTests.test_router_describes_unknown_provider -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_status_command_reports_missing_configuration -v
```

结果：

- 目标测试先失败。
- `LLMRouter.describe()` 只显示 provider/model，不显示配置问题。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_router_describes_openai_missing_configuration tests.test_llm.LLMTests.test_router_describes_openai_compatible_missing_base_url tests.test_llm.LLMTests.test_router_describes_unknown_provider -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_status_command_reports_missing_configuration -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 配置诊断专项 4 个测试通过。
- `tests.test_llm` 16 个测试通过。
- `tests.test_agent` 147 个测试通过。

### 收尾验证

命令：

```powershell
git diff --check
Markdown 本地链接检查脚本
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
```

结果：

- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- `unittest`：通过，`Ran 313 tests`，结果 `OK`。
- 桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。

## 2026-05-27 LLM 本地用量汇总验证

### RED：usage 汇总函数和命令未实现

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_summarize_llm_usage_groups_local_log_records tests.test_llm.LLMTests.test_summarize_llm_usage_reports_empty_log tests.test_agent.AgentTests.test_llm_usage_command_summarizes_local_usage_log -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command -v
```

结果：

- 目标测试先失败。
- `summarize_llm_usage` 尚未导出，`/llm-usage` 返回未知命令，`/help` 未列出该命令。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_summarize_llm_usage_groups_local_log_records tests.test_llm.LLMTests.test_summarize_llm_usage_reports_empty_log tests.test_agent.AgentTests.test_llm_usage_command_summarizes_local_usage_log tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 本地 usage 汇总和 `/llm-usage` 专项 4 个测试通过。
- `tests.test_llm` 18 个测试通过。
- `tests.test_agent` 149 个测试通过。

### 收尾验证

命令：

```powershell
git diff --check
Markdown 本地链接检查脚本
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
```

结果：

- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- `unittest`：通过，`Ran 317 tests`，结果 `OK`。
- 桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。

## 2026-05-27 LLM 配置模板验证

### RED：配置模板函数和命令未实现

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_describe_llm_config_examples_lists_provider_templates tests.test_llm.LLMTests.test_describe_llm_config_examples_can_filter_provider tests.test_llm.LLMTests.test_describe_llm_config_examples_reports_unknown_provider tests.test_agent.AgentTests.test_llm_config_example_command_reports_provider_templates tests.test_agent.AgentTests.test_llm_config_example_command_can_filter_provider tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command -v
```

结果：

- 目标测试先失败。
- `describe_llm_config_examples` 尚未导出，`/llm-config-example` 返回未知命令，`/help` 未列出该命令。
- `qwen` 不能映射到兼容端点模板。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_describe_llm_config_examples_lists_provider_templates tests.test_llm.LLMTests.test_describe_llm_config_examples_can_filter_provider tests.test_llm.LLMTests.test_describe_llm_config_examples_reports_unknown_provider tests.test_agent.AgentTests.test_llm_config_example_command_reports_provider_templates tests.test_agent.AgentTests.test_llm_config_example_command_can_filter_provider tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_describe_llm_config_examples_maps_model_hub_alias_to_compatible_template tests.test_agent.AgentTests.test_llm_config_example_command_maps_model_hub_alias -v
```

结果：

- LLM 配置模板专项 8 个测试通过。

### 收尾验证

命令：

```powershell
git diff --check
Markdown 本地链接检查脚本
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
```

结果：

- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- `unittest`：通过，`Ran 324 tests`，结果 `OK`。
- 桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。

## 2026-05-27 LLM OpenAI-compatible 与 usage 日志验证

### RED：usage 类型和兼容 provider 未实现

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_openai_compatible_provider_requires_base_url tests.test_llm.LLMTests.test_openai_provider_attaches_usage_from_response tests.test_llm.LLMTests.test_router_uses_openai_compatible_provider_from_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_usage_is_recorded_when_provider_returns_usage -v
```

结果：

- 目标测试先失败。
- 失败原因是 `LLMUsage` 尚未定义，`openai-compatible` 尚未接入 Router，Agent 尚未记录 usage。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_openai_compatible_provider_requires_base_url tests.test_llm.LLMTests.test_openai_provider_attaches_usage_from_response tests.test_llm.LLMTests.test_router_uses_openai_compatible_provider_from_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_usage_is_recorded_when_provider_returns_usage -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- OpenAI-compatible 和 usage 专项 4 个测试通过。
- `tests.test_llm` 13 个测试通过。
- `tests.test_agent` 146 个测试通过。

### 收尾验证

命令：

```powershell
git diff --check
Markdown 本地链接检查脚本
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
```

结果：

- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- `unittest`：通过，`Ran 309 tests`，结果 `OK`。
- 桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。

## 2026-05-27 LLM 外脑接入第一版验证

### RED：Agent 未接入 LLM Router

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_local_natural_language_intent_does_not_call_llm tests.test_agent.AgentTests.test_data_answer_does_not_call_llm tests.test_agent.AgentTests.test_llm_command_intent_is_executed_by_agent tests.test_agent.AgentTests.test_llm_clarification_intent_asks_without_execution -v
```

结果：

- 4 个目标测试先失败。
- 失败原因是 `JarvisAgent.__init__()` 不接受 `llm_router` 参数。

### RED：OpenAI provider 和状态命令未实现

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_openai_provider_without_api_key_returns_no_action tests.test_llm.LLMTests.test_openai_provider_without_sdk_returns_no_action tests.test_llm.LLMTests.test_openai_provider_parses_responses_output_text tests.test_llm.LLMTests.test_router_uses_openai_provider_from_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_status_command_reports_router_state -v
```

结果：

- LLM 测试先因缺少 `OpenAIResponsesProvider` 导入失败。
- Agent 状态命令测试先失败，`/llm-status` 返回未知命令。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- `tests.test_llm` 10 个测试通过。
- `tests.test_agent` 145 个测试通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
git diff --check
Markdown 本地链接检查脚本
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
```

结果：

- `pip install -e .`：退出 0，安装 `openai-2.38.0` 并完成 editable 安装。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- `unittest`：通过，`Ran 305 tests`，结果 `OK`。
- 桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。

## 2026-05-27 编号最近资料打标签缺失提示验证

### RED：给缺失编号资料打标签只返回底层缺失信息

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_marks_missing_document -v
```

结果：

- 目标测试先失败。
- “给第二份资料打标签 项目”对已删除资料只返回底层 `标签更新失败：资料不存在：data/manual.md`，缺少编号缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_marks_missing_document -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_updates_selected_document_tags tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_requires_recent_list tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_marks_missing_document tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_marks_missing_documents tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags -v
```

结果：

- 编号最近资料打标签缺失提示目标测试通过。
- 编号打标签、编号读取缺失、历史缺失和普通标签更新回归 6 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 290 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-26 批量标签历史资料恢复提示验证

### RED：读取历史资料缺少恢复提示

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_sets_recent_document_list -v
```

结果：

- 目标测试先失败。
- “读取第一条标签历史资料”已能列出影响资料，但缺少该历史的逐份恢复提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_tagged_documents_history_documents_sets_recent_document_list -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_tagged_documents_history_command_survives_new_agent_instance tests.test_agent.AgentTests.test_recent_tagged_documents_operation_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_tagged_documents_operation tests.test_agent.AgentTests.test_recent_document_list_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_confirm_tagged_documents_tagging_reports_restore_hints -v
```

结果：

- 批量标签历史资料恢复提示目标测试通过。
- 批量标签历史、最近批量摘要、最近资料列表和确认恢复提示回归 5 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 287 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。
## 2026-05-27 LLM provider 命令边界与 smoke 模板验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_llm.LLMTests.test_describe_llm_config_examples_lists_provider_templates -v
```

结果：

- 目标 2 个测试先失败。
- provider instructions 缺少 Jarvis Lite 命令白名单和“不返回列表之外命令”约束。
- 配置模板缺少 `/llm-smoke 请用一句话确认连接可用`。

### GREEN 与收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_llm.LLMTests.test_describe_llm_config_examples_lists_provider_templates -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
敏感信息扫描
```

结果：

- 目标 2 个测试通过。
- `tests.test_llm` 25 个通过。
- `tests.test_agent` 156 个通过。
- 全量 `unittest` 331 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- 敏感信息扫描未命中真实 API key、具体网关域名或 key 片段。

## 2026-05-28 LLM fallback 近期上下文增强验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_fallback_context_includes_recent_next_actions -v
```

结果：

- 目标测试先失败。
- fake provider 收到的 context 只有 `记忆摘要` 和 `最近资料`。
- 缺少 `下一步建议：继续处理最近资料：/read note.txt；/tag note.txt 标签...`。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_fallback_context_includes_recent_next_actions -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
```

结果：

- 目标测试通过。
- `tests.test_agent` 157 个通过。
- `tests.test_llm` 25 个通过。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
```

结果：

- 全量 `unittest` 332 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。

## 2026-05-28 InnerBrain preview/status 验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_inner_brain_status_command_reports_samples_and_thresholds tests.test_agent.AgentTests.test_inner_brain_preview_command_reports_result_without_execution tests.test_agent.AgentTests.test_inner_brain_preview_does_not_delete_desktop_shortcut -v
```

结果：

- `describe_inner_brain_result` 不存在，InnerBrain 测试导入失败。
- `/help`、`/inner-brain-status`、`/inner-brain-preview` 目标测试失败。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_inner_brain_status_command_reports_samples_and_thresholds tests.test_agent.AgentTests.test_inner_brain_preview_command_reports_result_without_execution tests.test_agent.AgentTests.test_inner_brain_preview_does_not_delete_desktop_shortcut -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- 目标 12 个测试通过。
- `tests.test_inner_brain tests.test_agent` 共 179 个通过。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-status"
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-preview 麻烦看一下知识库摘要"
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
Markdown 本地链接检查脚本
```

结果：

- 全量 `unittest` 359 个通过。
- `/inner-brain-status` 输出 seed/runtime 样本数量、阈值和训练目录。
- `/inner-brain-preview 麻烦看一下知识库摘要` 输出 `knowledge.summary`、`seed_sample`、`/kb-summary`，并说明不执行命令。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。
- 敏感信息扫描未命中真实 API key、具体网关域名或 key 片段。

## 2026-05-28 用户日志自然语言识别修复验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_morning_greeting_uses_user_name_without_memory_fallback tests.test_agent.AgentTests.test_natural_language_assistant_name_question_answers_assistant_identity tests.test_agent.AgentTests.test_natural_language_deletes_named_desktop_shortcuts_only tests.test_agent.AgentTests.test_natural_language_desktop_shortcut_delete_reports_missing_names tests.test_agent.AgentTests.test_greeting_does_not_use_plain_memory_summary_fallback tests.test_desktop_bridge.DesktopBridgeTests.test_send_routes_greeting_through_local_natural_language_brain tests.test_windows_installer.WindowsInstallerTests.test_install_script_uses_supplied_project_version tests.test_windows_installer.WindowsInstallerTests.test_iexpress_sed_points_to_external_installer_output_and_packaged_exe -v
```

结果：

- 8 个目标测试先失败。
- 失败原因符合预期：用户日志中的问候、助手身份和桌面快捷方式删除都落到长期记忆兜底；安装提示缺少版本号。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_morning_greeting_uses_user_name_without_memory_fallback tests.test_agent.AgentTests.test_natural_language_assistant_name_question_answers_assistant_identity tests.test_agent.AgentTests.test_natural_language_deletes_named_desktop_shortcuts_only tests.test_agent.AgentTests.test_natural_language_desktop_shortcut_delete_reports_missing_names tests.test_agent.AgentTests.test_greeting_does_not_use_plain_memory_summary_fallback tests.test_desktop_bridge.DesktopBridgeTests.test_send_routes_greeting_through_local_natural_language_brain tests.test_windows_installer.WindowsInstallerTests.test_install_script_uses_supplied_project_version tests.test_windows_installer.WindowsInstallerTests.test_iexpress_sed_points_to_external_installer_output_and_packaged_exe -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_desktop_bridge tests.test_windows_installer tests.test_desktop_packaging tests.test_project_metadata -v
```

结果：

- 目标 8 个测试通过。
- 相关回归 188 个测试通过。

### 收尾与打包

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "早上好"
.\.venv\Scripts\python.exe src\app.py --once "你叫什么名字"
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.1.2 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'FinishMessage|TargetName'
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.1.2.exe -Force
```

结果：

- 全量 `unittest` 345 个通过。
- 源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 命令行 `早上好` 和 `你叫什么名字` 均不再走长期记忆兜底。
- editable 安装更新为 `jarvis-lite 0.1.2`。
- 安装器生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，并复制出 `JarvisLiteSetup-0.1.2.exe`。
- `install.cmd` 显示 `DisplayVersion /d "0.1.2"`、`Jarvis Lite 0.1.2 installed to "%INSTALL_DIR%"`、覆盖安装提示和用户数据保留提示。
- IExpress 完成消息显示 `Jarvis Lite 0.1.2 installation finished. Start Jarvis Lite from desktop shortcut to use this version.`

## 2026-05-28 LLM 调用收口与 0.1.1 打包

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_llm_context_preview_reports_context_without_calling_provider tests.test_agent.AgentTests.test_llm_command_intent_rejects_unknown_command_before_agent_execution tests.test_llm.LLMTests.test_openai_provider_formats_401_error_without_leaking_api_key tests.test_llm.LLMTests.test_openai_provider_formats_429_error_as_rate_or_quota_issue tests.test_llm.LLMTests.test_router_uses_openai_provider_from_settings tests.test_llm.LLMTests.test_router_describes_openai_missing_configuration tests.test_llm.LLMTests.test_router_describes_fake_provider_as_local_no_network tests.test_windows_installer.WindowsInstallerTests.test_install_script_explains_cover_install_and_keeps_user_data -v
```

结果：

- 9 个目标测试先失败，分别证明 `/llm-context-preview`、Agent 侧 LLM 命令硬白名单、状态诊断、错误可读化和覆盖安装提示尚未实现。

### GREEN 与专项

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_llm_context_preview_reports_context_without_calling_provider tests.test_agent.AgentTests.test_llm_command_intent_rejects_unknown_command_before_agent_execution tests.test_llm.LLMTests.test_openai_provider_formats_401_error_without_leaking_api_key tests.test_llm.LLMTests.test_openai_provider_formats_429_error_as_rate_or_quota_issue tests.test_llm.LLMTests.test_router_uses_openai_provider_from_settings tests.test_llm.LLMTests.test_router_describes_openai_missing_configuration tests.test_llm.LLMTests.test_router_describes_fake_provider_as_local_no_network tests.test_windows_installer.WindowsInstallerTests.test_install_script_explains_cover_install_and_keeps_user_data -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer tests.test_desktop_packaging tests.test_project_metadata -v
```

结果：

- 目标 9 个测试通过。
- `tests.test_llm` 28 个通过。
- `tests.test_agent` 160 个通过。
- 安装器、桌面打包和项目元数据专项 18 个通过。

### 收尾与打包

命令：

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/llm-context-preview"
.\.venv\Scripts\python.exe src\app.py --once "/llm-status"
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
```

结果：

- editable 安装更新为 `jarvis-lite 0.1.1`。
- 全量 `unittest` 339 个通过。
- 源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，并复制出 `JarvisLiteSetup-0.1.1.exe`。
- `install.cmd` 显示 `DisplayVersion /d "0.1.1"`、覆盖安装提示和用户数据保留提示。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。
- 敏感信息扫描未命中真实 API key、具体网关域名或 key 片段。

## 2026-05-28 LLM fallback 最近搜索结果上下文验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_fallback_context_includes_recent_search_results -v
```

结果：

- 初次 RED 因测试提示词包含“资料”，被本地知识库弱匹配拦截，未进入 LLM fallback；调整提示词后重新执行。
- 目标测试随后按预期失败。
- fake provider 收到的 context 包含记忆摘要、最近资料和下一步建议，但缺少最近搜索结果。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_fallback_context_includes_recent_search_results -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm -v
```

结果：

- 目标测试通过。
- `tests.test_agent` 158 个通过。
- `tests.test_llm` 25 个通过。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
```

结果：

- 全量 `unittest` 333 个通过。
- 桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。
- 敏感信息扫描未命中真实 API key、具体网关域名或 key 片段。

## 2026-05-28 InnerBrain 本地内脑第一版验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_seed_variant_executes_without_llm tests.test_agent.AgentTests.test_inner_brain_runtime_sample_executes_without_llm tests.test_agent.AgentTests.test_inner_brain_low_confidence_still_uses_llm_fallback -v
```

结果：

- `tests.test_inner_brain` 先因 `jarvis_lite.inner_brain` 不存在失败。
- Agent 集成测试先失败，seed/runtime 样本表达没有进入本地内脑，分别走了 LLM 或 data 问答。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_seed_variant_executes_without_llm tests.test_agent.AgentTests.test_inner_brain_runtime_sample_executes_without_llm tests.test_agent.AgentTests.test_inner_brain_low_confidence_still_uses_llm_fallback -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- `tests.test_inner_brain` 6 个通过。
- Agent 目标 3 个通过。
- `tests.test_inner_brain tests.test_agent` 共 174 个通过。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe src\app.py --once "麻烦看一下知识库摘要"
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
Markdown 本地链接检查脚本
```

结果：

- 全量 `unittest` 354 个通过。
- `麻烦看一下知识库摘要` 输出知识库摘要。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。

## 2026-05-28 InnerBrain runtime 样本采纳验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- `tests.test_inner_brain` 因 `save_runtime_training_sample` 不存在而导入失败。
- `/help` 未列出 `/inner-brain-adopt`。
- `/inner-brain-adopt` 返回未知命令，runtime 样本文件未创建。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- `tests.test_inner_brain tests.test_agent` 共 186 个通过。
- 覆盖 JSONL 写入、重复样本跳过、`unknown` 拒绝、保存后 status 刷新，以及采纳桌面快捷方式删除表达时不删除 `.lnk` 文件。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
临时目录 /inner-brain-adopt smoke
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
```

结果：

- 全量 `unittest` 366 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 临时目录 `/inner-brain-adopt 帮我看看资料库状态` 输出已保存 runtime 样本和 `runtime_sample：1 条`，未污染当前仓库 `data/`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。
- 敏感信息扫描未命中。

## 2026-05-28 LLM 本地配置入口验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_config tests.test_llm.LLMTests.test_settings_read_local_config_file tests.test_llm.LLMTests.test_environment_overrides_local_config_file tests.test_llm.LLMTests.test_build_router_reads_local_config_file tests.test_agent.AgentTests.test_agent_reads_llm_local_config_file_on_startup tests.test_agent.AgentTests.test_llm_enable_command_reports_local_config_path_without_api_key tests.test_agent.AgentTests.test_natural_language_enable_llm_uses_inner_brain_entry -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_enable_llm_reloads_local_config_during_running_session -v
```

结果：

- `ProjectPaths.config_dir`、`llm_local_config_path()` 和本地配置读取入口不存在。
- “开启外脑”落入长期记忆兜底。
- 运行中写入 `llm.local.json` 后 `/llm-enable` 未重新加载 Router。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_config tests.test_llm.LLMTests.test_settings_read_local_config_file tests.test_llm.LLMTests.test_environment_overrides_local_config_file tests.test_llm.LLMTests.test_build_router_reads_local_config_file tests.test_agent.AgentTests.test_agent_reads_llm_local_config_file_on_startup tests.test_agent.AgentTests.test_llm_enable_command_reports_local_config_path_without_api_key tests.test_agent.AgentTests.test_natural_language_enable_llm_uses_inner_brain_entry tests.test_agent.AgentTests.test_enable_llm_reloads_local_config_during_running_session tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_inner_brain_status_command_reports_samples_and_thresholds -v
.\.venv\Scripts\python.exe -m unittest tests.test_config tests.test_llm tests.test_inner_brain tests.test_agent -v
```

结果：

- 目标 11 个测试通过。
- `tests.test_config tests.test_llm tests.test_inner_brain tests.test_agent` 共 233 个通过。
- 覆盖 `config/llm.local.json`、环境变量覆盖、Agent 启动读取、`/llm-enable`、自然语言“开启外脑”和运行中重新加载。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "开启外脑"
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
```

结果：

- 全量 `unittest` 384 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- “开启外脑”输出外脑启用入口、`config/llm.local.json` 和 `config/llm.example.json`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。
- 敏感信息扫描未命中。

## 2026-05-28 InnerBrain 0.1.3 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- 测试失败，`pyproject.toml` 中版本仍为 `0.1.2`，期望 `0.1.3`。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata tests.test_windows_installer tests.test_desktop_packaging -v
.\.venv\Scripts\python.exe -m pip install -e .
```

结果：

- 项目元数据、Windows 安装器和桌面打包专项 19 个通过。
- editable 安装从 `jarvis-lite 0.1.2` 更新到 `jarvis-lite 0.1.3`。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.1.3 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.1.3 installation finished'
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.1.3.exe -Force
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
```

结果：

- 全量 `unittest` 377 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包脚本生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 版本化副本生成成功：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.3.exe`。
- `install.cmd` 包含 `DisplayVersion /d "0.1.3"`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.3 installation finished`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。
- 敏感信息扫描未命中。

## 2026-05-28 InnerBrain 口语化教学入口验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_inner_brain_teach_command_saves_command_sample_and_refreshes_current_agent tests.test_agent.AgentTests.test_inner_brain_teach_natural_sentence_saves_command_sample tests.test_agent.AgentTests.test_inner_brain_teach_does_not_execute_target_command_when_saving tests.test_agent.AgentTests.test_inner_brain_teach_rejects_unknown_target_command -v
```

结果：

- `/help` 未列出 `/inner-brain-teach`。
- `/inner-brain-teach` 返回未知命令，runtime 样本文件未创建。
- 口语教学句式未被识别，无法保存样本。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_inner_brain_teach_command_saves_command_sample_and_refreshes_current_agent tests.test_agent.AgentTests.test_inner_brain_teach_natural_sentence_saves_command_sample tests.test_agent.AgentTests.test_inner_brain_teach_does_not_execute_target_command_when_saving tests.test_agent.AgentTests.test_inner_brain_teach_rejects_unknown_target_command -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- 目标 5 个测试通过。
- `tests.test_inner_brain tests.test_agent` 共 196 个通过。
- 覆盖 help 文案、slash 教学、口语教学、保存后立即生效、保存不执行 `/daily-report`、未知目标命令拒绝。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
临时目录 /inner-brain-teach smoke
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
```

结果：

- 全量 `unittest` 376 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 临时目录 `/inner-brain-teach 可以看看资料库吗 => /kb` 后，跟进输入 `可以看看资料库吗` 输出个人知识库状态，`runtime_sample：1 条`，未污染当前仓库 `data/`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。
- 敏感信息扫描未命中。

## 2026-05-28 InnerBrain 人工标注样本验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- `save_labeled_runtime_training_sample` 不存在导致 `tests.test_inner_brain` 导入失败。
- `/help` 未列出 `/inner-brain-label`。
- `/inner-brain-label` 返回未知命令，无法保存 unknown 或误识别输入。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- `tests.test_inner_brain tests.test_agent` 共 192 个通过。
- 覆盖人工标注写入、列表 slot 保存、保存后当前 Agent 立即刷新、无效格式提示、无效 slot 拒绝，以及标注桌面快捷方式删除表达时不删除 `.lnk` 文件。

### 收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
临时目录 /inner-brain-label smoke
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
```

结果：

- 全量 `unittest` 372 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 临时目录 `/inner-brain-label 可以看看资料库吗 => knowledge.status command=/kb` 后，跟进输入 `可以看看资料库吗` 输出个人知识库状态，`runtime_sample：1 条`，未污染当前仓库 `data/`。
- `git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查通过。
- 敏感信息扫描未命中。
## 2026-05-28 Agent 联网搜索第一版验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_search -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_search_status_command_reports_default_disabled_state tests.test_agent.AgentTests.test_search_command_returns_fake_provider_results tests.test_agent.AgentTests.test_search_command_reports_disabled_provider tests.test_agent.AgentTests.test_natural_language_web_search_uses_inner_brain_entry_without_llm tests.test_agent.AgentTests.test_search_enable_command_reports_local_config_path_without_api_key -v
```

结果：

- 失败原因符合预期：`ModuleNotFoundError: No module named 'jarvis_lite.search'`。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_search -v
.\.venv\Scripts\python.exe -m unittest tests.test_search tests.test_inner_brain tests.test_agent -v
```

结果：

- `tests.test_search`：通过，`Ran 10 tests`，结果 `OK`。
- `tests.test_search tests.test_inner_brain tests.test_agent`：通过，`Ran 215 tests`，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/search-status"
$env:JARVIS_LITE_SEARCH_PROVIDER='fake'; $env:JARVIS_LITE_SEARCH_FAKE_RESULTS='[{"title":"Python release","url":"https://python.example/release","snippet":"Python 版本摘要"}]'; .\.venv\Scripts\python.exe src\app.py --once "/search Python 版本"; Remove-Item Env:JARVIS_LITE_SEARCH_PROVIDER; Remove-Item Env:JARVIS_LITE_SEARCH_FAKE_RESULTS
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
git ls-files config/search.local.json
```

结果：

- editable 安装成功，安装 `tavily-python 0.7.24`。
- 全量 `unittest`：通过，`Ran 399 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/search-status` smoke：通过，默认 off。
- fake provider `/search Python 版本` smoke：通过，输出编号 URL 来源。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息扫描：通过，输出 `Sensitive scan OK`。
- `git ls-files config/search.local.json` 未输出 tracked 文件。

## 2026-05-28 InnerBrain 样本分类器优先迁移验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- 测试按预期失败 12 项：高频自然语言仍返回 `source=legacy_rule`，状态仍显示 `legacy_rule：启用`，复杂槽位旧规则未标记为 `legacy_fallback`。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- `tests.test_inner_brain tests.test_agent`：通过，`Ran 207 tests`，结果 `OK`。
- 全量 `unittest`：通过，`Ran 401 tests`，结果 `OK`。

### 补充样本 RED/GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_high_frequency_intents_use_sample_classifier -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- 补充 `有什么功能`、`目录列表`、`下载最新版`、`取消运行` 等回归用例后先失败，来源仍为 `legacy_fallback`。
- 扩展 seed 样本后目标测试通过。
- `tests.test_inner_brain tests.test_agent`：通过，`Ran 207 tests`，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-status"
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-preview 早上好"
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- 全量 `unittest`：通过，`Ran 401 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/inner-brain-status` smoke：通过，输出样本分类器优先、`legacy_fallback` 迁移期兼容、`seed_sample：51 条`。
- `/inner-brain-preview 早上好` smoke：通过，输出 `意图：assistant.greeting`、`来源：seed_sample`、`策略：execute`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息扫描：通过，输出 `Sensitive scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-29 InnerBrain 多轮澄清 v1 收口与 0.2.0 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_document_path tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_result_index_for_recent_document tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_tags_for_recent_document tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_tag_group_alias_and_tags tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_experience_search_query tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_experience_advice_query -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- 6 个目标测试先有 5 个失败：提示标签、编号示例、标签组+新标签拆分和经验关键词提示尚未收口。
- 版本一致性测试先失败，`pyproject.toml` 仍为 `0.1.10`，期望 `0.2.0`。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_document_path tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_result_index_for_recent_document tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_tags_for_recent_document tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_tag_group_alias_and_tags tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_experience_search_query tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_experience_advice_query -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 6 个目标测试通过，结果 `OK`。
- `tests.test_inner_brain tests.test_agent`：通过，`Ran 240 tests`，结果 `OK`。
- 版本一致性测试通过。
- 全量 `unittest discover`：通过，`Ran 434 tests`，结果 `OK`；首次全量因更新测试模拟 manifest 仍写当前版本 `0.2.0` 失败，改为模拟新版本 `0.2.1` 后复跑通过。

### 打包和静态检查

命令：

```powershell
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.2.0.exe -Force
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.2.0 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.2.0 installation finished|TargetName|AppLaunched'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.2.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `install.cmd` 包含 `DisplayVersion /d "0.2.0"`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.2.0 installation finished`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.2.0.exe` 均存在，大小均为 57,073,664 bytes。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`；首次脚本因 Git 中文路径转义报错，改用 `git -c core.quotepath=false ls-files` 后复跑通过。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-29 本地配置写入与 0.6.0 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_config_set_writes_local_config_without_leaking_api_key tests.test_agent.AgentTests.test_llm_config_set_preserves_unspecified_existing_fields tests.test_agent.AgentTests.test_llm_config_set_rejects_invalid_provider_without_partial_write tests.test_agent.AgentTests.test_search_config_set_writes_local_config_without_leaking_api_key tests.test_agent.AgentTests.test_search_config_set_rejects_invalid_max_results_without_partial_write tests.test_agent.AgentTests.test_natural_language_config_set_uses_inner_brain_entries_for_usage tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- 6 个配置写入目标测试先失败或报错，`/llm-config-set` 与 `/search-config-set` 仍是未知命令。
- 自然语言“设置外脑配置”先落入旧 `llm.config_init` 澄清，不符合本轮方案。
- 版本一致性测试先失败，`pyproject.toml` 仍为 `0.5.0`，期望 `0.6.0`。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_config_set_writes_local_config_without_leaking_api_key tests.test_agent.AgentTests.test_llm_config_set_preserves_unspecified_existing_fields tests.test_agent.AgentTests.test_llm_config_set_rejects_invalid_provider_without_partial_write tests.test_agent.AgentTests.test_search_config_set_writes_local_config_without_leaking_api_key tests.test_agent.AgentTests.test_search_config_set_rejects_invalid_max_results_without_partial_write tests.test_agent.AgentTests.test_natural_language_config_set_uses_inner_brain_entries_for_usage tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 7 个目标测试通过，结果 `OK`。
- `tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search`：通过，`Ran 299 tests`，结果 `OK`。
- 全量 `unittest discover`：通过，`Ran 452 tests`，结果 `OK`。

### Smoke、打包与静态验证

命令：

```powershell
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/llm-config-set provider=qwen model=qwen-plus base_url=https://qwen.example/v1/responses api_key=smoke-key"
.\.venv\Scripts\python.exe src\app.py --once "/llm-config-check"
.\.venv\Scripts\python.exe src\app.py --once "/search-config-set provider=tavily api_key=smoke-search-key max_results=3"
.\.venv\Scripts\python.exe src\app.py --once "/search-config-check"
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.6.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.6.0 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.6.0 installation finished|TargetName|AppLaunched'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.6.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/llm-config-set` + `/llm-config-check` CLI smoke：通过，输出配置完整，响应未显示真实 key。
- `/search-config-set` + `/search-config-check` CLI smoke：通过，输出配置完整，响应未显示真实 key。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `install.cmd` 包含 `taskkill`、`DisplayVersion /d "0.6.0"`、`Jarvis Lite 0.6.0 installed`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.6.0 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe` 和 `AppLaunched=install.cmd`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.6.0.exe` 均存在，大小均为 57,081,856 bytes。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件；`Test-Path` 均为 `False`。

## 2026-05-29 本地配置检查与 0.5.0 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_search_config_check_reads_current_local_config_without_api_key_or_network tests.test_agent.AgentTests.test_llm_config_check_reads_current_local_config_without_api_key_or_network tests.test_agent.AgentTests.test_llm_config_check_reports_invalid_json tests.test_agent.AgentTests.test_natural_language_config_check_uses_inner_brain_entries tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- 4 个 Agent 目标测试先失败，配置检查命令未知，自然语言“检查外脑配置”未进入检查命令。
- 版本一致性测试先失败，`pyproject.toml` 仍为 `0.4.0`，期望 `0.5.0`。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_search_config_check_reads_current_local_config_without_api_key_or_network tests.test_agent.AgentTests.test_llm_config_check_reads_current_local_config_without_api_key_or_network tests.test_agent.AgentTests.test_llm_config_check_reports_invalid_json tests.test_agent.AgentTests.test_natural_language_config_check_uses_inner_brain_entries tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search -v
```

结果：

- 5 个目标测试通过，结果 `OK`。
- `tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search`：首次因测试清单版本仍为 `0.4.1` 失败，改为 `0.5.1` 后复跑通过，`Ran 293 tests`，结果 `OK`。

### 全量、smoke 与打包

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/llm-config-check"
.\.venv\Scripts\python.exe src\app.py --once "/search-config-check"
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.5.0.exe -Force
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.5.0 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.5.0 installation finished|TargetName|AppLaunched'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.5.0.exe
```

结果：

- 全量 `unittest discover`：通过，`Ran 446 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/llm-config-check` CLI smoke：通过，输出外脑配置检查、本地配置未创建、检查方式不发起网络请求。
- `/search-config-check` CLI smoke：通过，输出联网搜索配置检查、本地配置未创建、检查方式不发起网络请求。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `install.cmd` 包含 `taskkill`、`DisplayVersion /d "0.5.0"`、`Jarvis Lite 0.5.0 installed`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.5.0 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe` 和 `AppLaunched=install.cmd`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.5.0.exe` 均存在，大小均为 57,077,760 bytes。

## 2026-05-28 InnerBrain 编号槽位迁移验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_numbered_object_intents_use_sample_classifier_slots -v
```

结果：

- 目标测试按预期失败。
- 8 个样例仍返回 `legacy.*` 意图，说明测试锁定了本阶段要迁移的缺口。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_numbered_object_intents_use_sample_classifier_slots -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 目标测试通过。
- `tests.test_inner_brain`：通过，`Ran 16 tests`，结果 `OK`。
- `tests.test_agent`：通过，`Ran 192 tests`，结果 `OK`。

### 全量与 smoke

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-status"
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-preview 读取第二份资料"
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- 全量 `unittest`：通过，`Ran 402 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/inner-brain-status`：通过，输出 `seed_sample：66 条`。
- `/inner-brain-preview 读取第二份资料`：通过，输出 `意图：document.read_numbered_recent`、`来源：seed_sample`、`编号：2`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-29 0.4.0 接手后最终复验

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.4.0.exe -Force
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- 全量 `unittest discover`：通过，`Ran 442 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制生成 `JarvisLiteSetup-0.4.0.exe`，大小 57,073,664 bytes。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息扫描：通过，输出 `Sensitive scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-29 外脑 provider 配置闭环与 0.3.0 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_router_uses_qwen_alias_with_openai_compatible_adapter tests.test_llm.LLMTests.test_gemini_alias_requires_openai_compatible_base_url tests.test_llm.LLMTests.test_describe_llm_config_examples_maps_model_hub_alias_to_compatible_template tests.test_llm.LLMTests.test_describe_llm_config_examples_maps_gemini_alias_to_compatible_template tests.test_agent.AgentTests.test_enable_llm_reports_qwen_alias_adapter_from_local_config -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- provider alias 目标测试先失败，`qwen`/`gemini` 尚未作为有效 provider alias 完成构建、诊断和模板展示。
- 版本一致性测试先失败，`pyproject.toml` 仍为 `0.2.0`，期望 `0.3.0`。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_llm.LLMTests.test_router_uses_qwen_alias_with_openai_compatible_adapter tests.test_llm.LLMTests.test_gemini_alias_requires_openai_compatible_base_url tests.test_llm.LLMTests.test_describe_llm_config_examples_maps_model_hub_alias_to_compatible_template tests.test_llm.LLMTests.test_describe_llm_config_examples_maps_gemini_alias_to_compatible_template tests.test_agent.AgentTests.test_enable_llm_reports_qwen_alias_adapter_from_local_config -v
.\.venv\Scripts\python.exe -m unittest tests.test_llm tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory -v
```

结果：

- 5 个 provider alias 目标测试通过，结果 `OK`。
- `tests.test_llm tests.test_agent`：通过，`Ran 251 tests`，结果 `OK`。
- 版本一致性和更新命令专项测试通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.3.0.exe -Force
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.3.0 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.3.0 installation finished|TargetName|AppLaunched'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.3.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- 全量 `unittest discover`：通过，`Ran 438 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `install.cmd` 包含 `taskkill`、`DisplayVersion /d "0.3.0"`、`Jarvis Lite 0.3.0 installed`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.3.0 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe` 和 `AppLaunched=install.cmd`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.3.0.exe` 均存在，大小均为 57,069,568 bytes。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息扫描：通过，未命中常见 API key 模式。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-29 运行态配置初始化与 0.4.0 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_config_init_creates_qwen_local_config_draft_without_api_key tests.test_agent.AgentTests.test_llm_config_init_does_not_overwrite_existing_local_config_or_leak_key tests.test_agent.AgentTests.test_search_config_init_creates_tavily_local_config_draft_without_api_key tests.test_agent.AgentTests.test_natural_language_config_init_uses_inner_brain_entries tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- `/llm-config-init` 与 `/search-config-init` 目标测试先失败，命令尚不存在且自然语言入口未生成配置。
- 版本一致性测试先失败，`pyproject.toml` 仍为 `0.3.0`，期望 `0.4.0`。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_config_init_creates_qwen_local_config_draft_without_api_key tests.test_agent.AgentTests.test_llm_config_init_does_not_overwrite_existing_local_config_or_leak_key tests.test_agent.AgentTests.test_search_config_init_creates_tavily_local_config_draft_without_api_key tests.test_agent.AgentTests.test_natural_language_config_init_uses_inner_brain_entries tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search -v
```

结果：

- 5 个目标测试通过，结果 `OK`。
- `tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search`：通过，`Ran 289 tests`，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.4.0.exe -Force
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.4.0 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.4.0 installation finished|TargetName|AppLaunched'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.4.0.exe
```

结果：

- 全量 `unittest discover`：通过，`Ran 442 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `install.cmd` 包含 `taskkill`、`DisplayVersion /d "0.4.0"`、`Jarvis Lite 0.4.0 installed`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.4.0 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe` 和 `AppLaunched=install.cmd`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.4.0.exe` 均存在，大小均为 57,073,664 bytes。

## 2026-05-29 InnerBrain 目录别名和经验内容补槽与 0.1.10 安装包验证

### RED/GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_directory_alias tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_experience_content -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v
```

结果：

- 目标测试先失败，澄清文案显示原始 `alias`/`experience`，缺少中文缺槽名和补槽示例。
- 修复后 2 个目标测试通过，结果 `OK`。
- `tests.test_inner_brain tests.test_agent`：通过，`Ran 234 tests`，结果 `OK`。
- 版本一致性测试先因 `pyproject.toml` 仍为 `0.1.9` 失败；同步到 `0.1.10` 后通过。

### 全量与打包

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.1.10.exe -Force
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.1.10 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.1.10 installation finished|TargetName|AppLaunched'
```

结果：

- 全量 `unittest discover`：通过，`Ran 428 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `install.cmd` 包含 `DisplayVersion /d "0.1.10"`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.10 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe` 和 `AppLaunched=install.cmd`。

### 提交前收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- 全量 `unittest discover`：通过，`Ran 428 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-29 InnerBrain 编号+标签联合补槽与 0.1.9 安装包验证

### RED/GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_numbered_tags_without_polluting_tags -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v
```

结果：

- 目标测试先失败，澄清文案显示原始 `result_index、tags`，缺少编号+标签一句式提示。
- 修复后目标测试通过，结果 `OK`。
- `tests.test_inner_brain tests.test_agent`：通过，`Ran 232 tests`，结果 `OK`。
- 版本一致性测试先因 `pyproject.toml` 仍为 `0.1.8` 失败；同步到 `0.1.9` 后通过。

### 全量与打包

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.1.9.exe -Force
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.1.9 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.1.9 installation finished|TargetName|AppLaunched'
```

结果：

- 全量 `unittest discover`：通过，`Ran 426 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `install.cmd` 包含 `DisplayVersion /d "0.1.9"`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.9 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe` 和 `AppLaunched=install.cmd`。

### 提交前收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- 全量 `unittest discover`：通过，`Ran 426 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-29 InnerBrain 多轮澄清 query 补槽与 0.1.8 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_web_search_query tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_web_search_summary_query -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- query 补槽目标测试先失败，澄清文案只显示原始 `query`，没有 `/search 关键词` 或 `/search-summary 关键词`。
- 版本一致性测试先失败，`pyproject.toml` 仍为 `0.1.7`。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_web_search_query tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_web_search_summary_query -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- query 补槽 2 项通过。
- `tests.test_inner_brain tests.test_agent`：通过，`Ran 231 tests`，结果 `OK`。
- 版本一致性测试通过，项目元数据同步为 `0.1.8`。

### 打包

命令：

```powershell
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.1.8.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
```

结果：

- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.1.8.exe` 均存在，大小均为 57,069,568 bytes。
- 提交前全量 `unittest discover`：通过，`Ran 425 tests`，结果 `OK`。
- 提交前源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 提交前打包后 `JarvisLite.exe --smoke`：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-29 InnerBrain 多轮澄清状态与 0.1.7 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_source_and_executes_import tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_desktop_shortcut_name tests.test_agent.AgentTests.test_inner_brain_clarification_can_be_cancelled -v
```

结果：

- 目标测试先失败，路径补充未继续导入，桌面快捷方式名称补充未继续删除，取消补充未清空 pending。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_source_and_executes_import tests.test_agent.AgentTests.test_inner_brain_clarification_accepts_followup_desktop_shortcut_name tests.test_agent.AgentTests.test_inner_brain_clarification_can_be_cancelled tests.test_agent.AgentTests.test_inner_brain_clarification_includes_completion_and_training_hints -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
```

结果：

- 澄清专项 4 项通过。
- `tests.test_inner_brain tests.test_agent`：通过，`Ran 229 tests`，结果 `OK`。

### 版本、全量与打包

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.1.7.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
```

结果：

- 版本一致性测试按 TDD 先失败后通过。
- 全量 `unittest discover`：通过，`Ran 423 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.1.7.exe` 均存在，大小均为 57,069,568 bytes。
- 提交前复跑全量 `unittest discover`：通过，`Ran 423 tests`，结果 `OK`。
- 提交前源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 提交前打包后 `JarvisLite.exe --smoke`：退出码 0。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-28 v6 高频 legacy 别名迁移与 0.1.6 安装包

### RED/GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_legacy_high_frequency_aliases_use_seed_samples -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_numbered_object_intents_use_sample_classifier_slots -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- 高频别名测试先失败，29 个代表表达仍返回 `source=legacy_fallback`；扩展 seed 样本后通过。
- `请帮我导入第二份最近文件到资料库` 先返回 `legacy.import_numbered_recent_file`；扩展编号最近文件导入签名后通过。
- 版本一致性测试先失败，`pyproject.toml` 仍为 `0.1.5`；同步项目元数据到 `0.1.6` 后通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
代表句脚本扫描 InnerBrain 输出 source
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe ..\jarvis-lite-dist\JarvisLiteSetup-0.1.6.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.1.6 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.1.6 installation finished|TargetName|AppLaunched'
```

结果：

- `tests.test_inner_brain tests.test_agent`：通过，`Ran 226 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 全量 `unittest discover`：通过，`Ran 420 tests`，结果 `OK`。
- 代表句复扫：通过，输出 `legacy=0 unknown=0`。首次脚本引用不存在的 `jarvis_lite.paths` 失败，修正为 `build_project_paths` 后通过。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.1.6.exe` 均存在，大小均为 57,065,472 bytes。
- 打包后 `JarvisLite.exe --smoke`：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `install.cmd` 包含 `taskkill`、`DisplayVersion /d "0.1.6"`、`Jarvis Lite 0.1.6 installed`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.6 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe` 和 `AppLaunched=install.cmd`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-28 v6 搜索后续动作与 0.1.5 安装包

### RED/GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_web_search_followup_intents_use_sample_classifier_slots tests.test_agent.AgentTests.test_natural_language_opens_numbered_recent_web_search_source_without_browser_launch tests.test_agent.AgentTests.test_search_compare_recent_sources_uses_llm_context tests.test_agent.AgentTests.test_search_save_summary_writes_word_summary_from_recent_web_search tests.test_agent.AgentTests.test_search_import_summary_writes_data_document_and_updates_recent_document -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_desktop_shortcut_object_first_variants_use_sample_classifier_slots tests.test_agent.AgentTests.test_natural_language_deletes_object_first_desktop_shortcut_expression -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_clarification_includes_completion_and_training_hints -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- 搜索后续 5 项测试先失败后通过。
- 桌面快捷方式宾语前置表达 2 项测试先失败后通过。
- InnerBrain 澄清提示测试先失败后通过。
- `0.1.5` 版本一致性测试先失败后通过。

### 全量、smoke 和打包

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-preview 打开第一条联网搜索结果"
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-preview 把桌面快捷方式比特浏览器删掉"
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- `tests.test_inner_brain tests.test_agent`：通过，`Ran 225 tests`，结果 `OK`。
- 全量 `unittest discover`：通过，`Ran 419 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包：生成并复制 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.5.exe`，大小 57,065,472 bytes。
- 打包 exe smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装脚本版本：`DisplayVersion /d "0.1.5"`；IExpress 完成提示：`Jarvis Lite 0.1.5 installation finished`。
- InnerBrain 预览：`打开第一条联网搜索结果` 输出 `web_search.open_numbered` 和 `/search-open 1`；`把桌面快捷方式比特浏览器删掉` 输出 `desktop.delete_shortcut` 和 `对象：比特浏览器`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-28 InnerBrain 标签槽位迁移验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_tag_intents_use_sample_classifier_slots -v
```

结果：

- 目标测试按预期失败。
- 7 个样例仍返回 `legacy.*` 意图，说明测试锁定了本阶段要迁移的缺口。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_tag_intents_use_sample_classifier_slots -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 目标测试通过。
- `tests.test_inner_brain`：通过，`Ran 17 tests`，结果 `OK`。
- `tests.test_agent`：通过，`Ran 192 tests`，结果 `OK`。

### 全量与 smoke

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-status"
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-preview 给第二份资料打标签 项目 Python"
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- 全量 `unittest`：通过，`Ran 403 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/inner-brain-status`：通过，输出 `seed_sample：75 条`。
- `/inner-brain-preview 给第二份资料打标签 项目 Python`：通过，输出 `意图：document.tag_numbered_recent`、`来源：seed_sample`、`标签：项目、Python`、`编号：2`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-28 InnerBrain 文件路径、目录和经验槽位迁移验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_file_path_intents_use_sample_classifier_slots -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_directory_intents_use_sample_classifier_slots -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_experience_intents_use_sample_classifier_slots -v
```

结果：

- 三个目标测试按预期先失败。
- 文件读取/导入、目录打开/整理、经验记录/搜索/建议样例仍返回 `legacy.*` 或 `command`/`legacy_fallback`。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_file_path_intents_use_sample_classifier_slots -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_directory_intents_use_sample_classifier_slots -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_experience_intents_use_sample_classifier_slots -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 三个目标测试通过。
- `tests.test_inner_brain`：通过，`Ran 20 tests`，结果 `OK`。
- `tests.test_inner_brain tests.test_agent`：通过，`Ran 212 tests`，结果 `OK`。
- 全量 `unittest`：通过，`Ran 406 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/inner-brain-status`：通过，输出 `seed_sample：90 条`。
- `/inner-brain-preview 导入 E:/docs/manual.pdf 到资料库`：通过，输出 `knowledge.import` 和 `/import "E:/docs/manual.pdf"`。
- `/inner-brain-preview 打开项目目录`：通过，输出 `directory.open_alias` 和 `别名：项目`。
- `/inner-brain-preview 我该怎么导入资料`：通过，输出 `experience.advice` 和 `/experience-advice 导入资料`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`；首次脚本因根目录 Markdown parent path 为空失败，修正后复跑通过。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-28 SearchRouter + LLMRouter 搜索总结组合验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_web_search_summary_uses_sample_classifier_slot -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_search_command_records_web_results_in_recent_context_and_llm_context tests.test_agent.AgentTests.test_natural_language_web_search_summary_uses_search_results_as_llm_context -v
```

结果：

- InnerBrain 目标测试先失败，`联网查一下 Python 版本并总结` 返回 `web.search`，没有映射为 `/search-summary`。
- Agent 目标测试先失败，`/search` 不写入最近联网搜索上下文，`/llm-context-preview` 不含搜索来源。
- Agent 目标测试先失败，明确“并总结”的自然语言只返回普通搜索结果，没有 `LLM 外脑总结`。

### GREEN 与专项回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_web_search_summary_uses_sample_classifier_slot -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_search_command_records_web_results_in_recent_context_and_llm_context tests.test_agent.AgentTests.test_natural_language_web_search_summary_uses_search_results_as_llm_context -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_search_summary_reports_llm_disabled_without_crashing tests.test_agent.AgentTests.test_inner_brain_teach_search_summary_uses_search_summary_intent tests.test_inner_brain.InnerBrainTests.test_web_search_summary_uses_sample_classifier_slot -v
```

结果：

- `web.search_summarize` 样本、槽位和 `/search-summary` 映射通过。
- `/search` 结果进入最近联网搜索上下文，并在 Agent 重启后保留到 `/llm-context-preview`。
- `/search-summary` 组合流程把搜索来源放进 LLM context，并展示 `LLM 外脑总结：...`。
- LLM 关闭时 `/search-summary` 不再崩溃，返回搜索来源和 `/llm-status`、`/llm-enable` 提示。
- `/inner-brain-teach 查版本 => /search-summary Python 版本` 保存为 `web.search_summarize`，followup 会执行教学目标。
- 追加目标测试：3 项通过，结果 `OK`。

### 全量与 smoke

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-status"
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-preview 联网查一下 Python 版本并总结"
.\.venv\Scripts\python.exe src\app.py --once "/search-summary Python 版本"
fake 搜索 + fake LLM 环境变量 smoke：联网查一下 Python 版本并总结
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- `tests.test_inner_brain tests.test_agent`：通过，`Ran 217 tests`，结果 `OK`。
- 全量 `unittest discover`：通过，`Ran 411 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/inner-brain-status`：通过，输出 `seed_sample：92 条`。
- `/inner-brain-preview 联网查一下 Python 版本并总结`：通过，输出 `意图：web.search_summarize`、`来源：seed_sample`、`命令：/search-summary Python 版本`。
- 默认 `/search-summary Python 版本`：通过，搜索关闭时输出联网搜索未启用、`/search-status` 和 `/search-enable`。
- fake 搜索 + fake LLM 自然语言 smoke：通过，输出 `联网搜索：Python 版本`、URL 来源和 `LLM 外脑总结：Python 3.13 是当前发布线。`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-28 SearchRouter + LLMRouter 0.1.4 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- 目标测试按预期失败，`pyproject.toml` 为 `0.1.3`，期望 `0.1.4`。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- 1 项通过，结果 `OK`。
- `pyproject.toml` 与 `jarvis_lite.__version__` 已更新为 `0.1.4`。

### 全量、源码 smoke 与打包验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'Jarvis Lite 0.1.4 installed|DisplayVersion|Existing app files|User data kept|taskkill'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0.1.4 installation finished|TargetName'
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.1.4.exe -Force
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.1.4.exe
```

结果：

- 全量 `unittest discover`：通过，`Ran 411 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `install.cmd` 包含 `taskkill`、`DisplayVersion /d "0.1.4"`、`Jarvis Lite 0.1.4 installed`、覆盖安装提示和用户数据保留提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.4 installation finished` 和 `TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.1.4.exe` 均存在，大小均为 57,057,280 bytes。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。

## 2026-05-28 InnerBrain 显式文件名标签槽位迁移验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_explicit_file_tag_intents_use_sample_classifier_slots -v
```

结果：

- 目标测试按预期失败，`给 note.txt 打标签 项目` 和 `把 data/note.txt 标记为 项目 Python` 均返回 `command`/`legacy_fallback`。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_explicit_file_tag_intents_use_sample_classifier_slots tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_mark_document_as_tags_updates_document_tags -v
```

结果：

- 3 项通过，结果 `OK`。
- 两个显式文件名标签样例均返回 `document.tag_path`、`source=seed_sample`，并映射到 `/tag`。

### 全量与 smoke

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-preview 给 note.txt 打标签 项目"
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
```

结果：

- `tests.test_inner_brain tests.test_agent`：通过，`Ran 217 tests`，结果 `OK`。
- 全量 `unittest discover`：通过，`Ran 411 tests`，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/inner-brain-preview 给 note.txt 打标签 项目`：通过，输出 `意图：document.tag_path`、`来源：seed_sample`、`命令：/tag "note.txt" 项目`、`标签：项目`、`路径：note.txt`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。
## 2026-05-29 连通性诊断与 0.7.0 安装包验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_smoke_command_reloads_local_config_during_running_session tests.test_agent.AgentTests.test_search_smoke_command_reloads_local_config_without_recent_context tests.test_agent.AgentTests.test_search_smoke_command_reports_disabled_provider tests.test_agent.AgentTests.test_natural_language_llm_smoke_uses_inner_brain_entry tests.test_agent.AgentTests.test_natural_language_search_smoke_uses_inner_brain_entry tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：

- 6 项按预期失败，原因分别为 `/llm-smoke` 未重读运行中写入的本地配置、`/search-smoke` 未实现、自然语言 smoke 样本未接入和项目版本仍为 `0.6.0`。

### GREEN 与回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_smoke_command_reloads_local_config_during_running_session tests.test_agent.AgentTests.test_search_smoke_command_reloads_local_config_without_recent_context tests.test_agent.AgentTests.test_search_smoke_command_reports_disabled_provider tests.test_agent.AgentTests.test_natural_language_llm_smoke_uses_inner_brain_entry tests.test_agent.AgentTests.test_natural_language_search_smoke_uses_inner_brain_entry tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

- 目标 6 项通过，结果 `OK`。
- 相邻回归 `tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search`：通过，`Ran 304 tests`，结果 `OK`。
- 全量 `unittest discover`：通过，`Ran 457 tests`，结果 `OK`。

### Smoke、打包与静态检查

命令：

```powershell
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe src\app.py --once "/llm-config-set provider=fake"
.\.venv\Scripts\python.exe src\app.py --once "/llm-smoke CLI smoke"
.\.venv\Scripts\python.exe src\app.py --once "/search-config-set provider=fake max_results=1"
.\.venv\Scripts\python.exe src\app.py --once "/search-smoke Python 版本"
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.7.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `/llm-smoke` CLI smoke：通过，输出 `LLM smoke：type=answer` 和 `回答：本地 fake 外脑已启用`。
- `/search-smoke` CLI smoke：通过，输出 `调用结果：成功，返回 1 条来源。` 和 `smoke 不会写入最近联网搜索上下文。`
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制生成 `JarvisLiteSetup-0.7.0.exe`，大小 57,081,856 bytes。
- 打包后 `JarvisLite.exe --smoke`：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `install.cmd` 包含 `DisplayVersion /d "0.7.0"`、`Jarvis Lite 0.7.0 installed`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.7.0 installation finished`。
- `git diff --check`：退出 0，仅提示 LF/CRLF 工作区换行警告。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 和 `config/search.local.json` 未被 Git 跟踪，CLI smoke 后 `Test-Path` 均为 `False`。
## 2026-05-29 0.8.0 桌面配置面板验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_send_sensitive_executes_real_command_but_records_redacted_input tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_provider_config_controls tests.test_desktop_widgets.DesktopWidgetTests.test_panel_writes_llm_config_without_showing_api_key_in_transcript_or_history tests.test_desktop_widgets.DesktopWidgetTests.test_panel_writes_search_config_without_showing_api_key_in_transcript_or_history tests.test_desktop_widgets.DesktopWidgetTests.test_panel_config_check_and_smoke_buttons_submit_existing_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：5 个桌面目标测试因缺少 `send_sensitive` 和配置面板 API 报错，版本测试因仍为 `0.7.0` 失败，符合 RED 预期。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_send_sensitive_executes_real_command_but_records_redacted_input tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_provider_config_controls tests.test_desktop_widgets.DesktopWidgetTests.test_panel_writes_llm_config_without_showing_api_key_in_transcript_or_history tests.test_desktop_widgets.DesktopWidgetTests.test_panel_writes_search_config_without_showing_api_key_in_transcript_or_history tests.test_desktop_widgets.DesktopWidgetTests.test_panel_config_check_and_smoke_buttons_submit_existing_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_search -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
git diff --check
```

结果：

- 目标测试：6 项通过。
- 邻近回归：316 项通过。
- 全量测试：462 项通过。
- 源码桌面 smoke：通过。
- 安装包构建：生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制为 `JarvisLiteSetup-0.8.0.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。

## 2026-05-29 0.9.0 LLM 外脑多轮澄清验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_clarification_followup_reuses_original_prompt_and_executes_final_command tests.test_agent.AgentTests.test_llm_clarification_followup_can_return_answer tests.test_agent.AgentTests.test_llm_clarification_can_be_cancelled_without_second_provider_call tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：失败 4 项，符合预期。

- `test_llm_clarification_followup_reuses_original_prompt_and_executes_final_command`：第二句“知识库”被 InnerBrain 当作新请求处理，未进入 LLM 澄清续聊。
- `test_llm_clarification_followup_can_return_answer`：第二句被 data 检索当作新问题处理，未进入 LLM 澄清续聊。
- `test_llm_clarification_can_be_cancelled_without_second_provider_call`：取消短语被普通 fallback 处理，未清空 LLM 待澄清。
- `test_project_version_matches_release_package_version`：当前项目版本仍为 `0.8.0`，期望 `0.9.0`。

### TARGET GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_clarification_followup_reuses_original_prompt_and_executes_final_command tests.test_agent.AgentTests.test_llm_clarification_followup_can_return_answer tests.test_agent.AgentTests.test_llm_clarification_can_be_cancelled_without_second_provider_call tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：4 项通过，`Ran 4 tests`，结果 `OK`。

### 回归、打包与静态检查

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation tests.test_desktop_bridge tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.9.0.exe -Force
Start-Process -FilePath ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe -ArgumentList '--smoke' -Wait -PassThru -WindowStyle Hidden
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.9\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.9\.0 installation finished'
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 邻近回归：332 项通过，结果 `OK`。
- 全量测试：465 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- 安装包复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.9.0.exe`，大小 57,090,048 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.9.0"` 和 `Jarvis Lite 0.9.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.9.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，未发现真实 API key。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在。

## 2026-05-29 0.10.0 LLM 外脑澄清状态持久化验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_clarification_pending_survives_new_agent_instance tests.test_agent.AgentTests.test_recent_context_reports_pending_llm_clarification_without_consuming_it tests.test_agent.AgentTests.test_llm_clarification_cancel_clears_persisted_pending tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：失败 4 项，符合预期。

- `test_llm_clarification_pending_survives_new_agent_instance`：重启 Agent 后没有恢复 LLM pending，用户补充被 InnerBrain 当作新输入。
- `test_recent_context_reports_pending_llm_clarification_without_consuming_it`：`/recent-context` 尚不存在，无法查看待补充外脑问题。
- `test_llm_clarification_cancel_clears_persisted_pending`：重启 Agent 后取消补充落到普通 fallback，说明 pending 未持久化。
- `test_project_version_matches_release_package_version`：当前项目版本仍为 `0.9.0`，期望 `0.10.0`。

### TARGET GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_clarification_pending_survives_new_agent_instance tests.test_agent.AgentTests.test_recent_context_reports_pending_llm_clarification_without_consuming_it tests.test_agent.AgentTests.test_llm_clarification_cancel_clears_persisted_pending tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：4 项通过，`Ran 4 tests`，结果 `OK`。

### 回归、打包与静态检查

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation tests.test_desktop_bridge tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.10.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.10\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.10\.0 installation finished'
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 邻近回归：335 项通过，结果 `OK`。
- 全量 `unittest discover`：468 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：命令退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.10.0.exe` 均存在，大小均为 57,085,952 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.10.0"` 和 `Jarvis Lite 0.10.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.10.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

## 2026-06-01 0.21.0 InnerBrain 候选频次排序验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_candidates_prioritize_repeated_fallback_prompts tests.test_agent.AgentTests.test_inner_brain_teach_candidate_uses_frequency_ranked_candidate tests.test_agent.AgentTests.test_inner_brain_label_candidate_uses_frequency_ranked_candidate tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：符合预期，3 个候选频次测试失败，版本一致性测试失败。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_candidates_prioritize_repeated_fallback_prompts tests.test_agent.AgentTests.test_inner_brain_teach_candidate_uses_frequency_ranked_candidate tests.test_agent.AgentTests.test_inner_brain_label_candidate_uses_frequency_ranked_candidate tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：4 项通过，结果 `OK`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：381 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.21.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.21\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.21\.0 installation finished'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.21.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：508 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；构建日志包含既有 `tzdata` hidden import warning，但命令退出码为 0。
- 打包后 `JarvisLite.exe --smoke`：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.21.0.exe` 均存在，大小均为 57,102,336 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.21.0"` 和 `Jarvis Lite 0.21.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.21.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

## 2026-06-01 0.20.0 InnerBrain 候选按编号标注验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_label_candidate_saves_selected_candidate_label tests.test_agent.AgentTests.test_inner_brain_label_candidate_reports_missing_candidate tests.test_agent.AgentTests.test_inner_brain_label_candidate_rejects_invalid_slot_assignment tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：符合预期，3 个候选标注测试失败或错误，版本一致性测试失败。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_label_candidate_saves_selected_candidate_label tests.test_agent.AgentTests.test_inner_brain_label_candidate_reports_missing_candidate tests.test_agent.AgentTests.test_inner_brain_label_candidate_rejects_invalid_slot_assignment tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：4 项通过，结果 `OK`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：378 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.20.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.20\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.20\.0 installation finished'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.20.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：505 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；构建日志包含既有 `tzdata` hidden import warning，但命令退出码为 0。
- 打包后 `JarvisLite.exe --smoke`：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.20.0.exe` 均存在，大小均为 57,102,336 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.20.0"` 和 `Jarvis Lite 0.20.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.20.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

## 2026-05-29 0.18.0 InnerBrain 训练候选验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_candidates_reports_empty_state_without_polluting_route_history tests.test_agent.AgentTests.test_inner_brain_candidates_lists_llm_and_memory_fallback_prompts tests.test_agent.AgentTests.test_inner_brain_candidates_restore_on_startup -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v
```

结果：3 个训练候选测试按预期失败，版本一致性测试按预期失败。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_candidates_reports_empty_state_without_polluting_route_history tests.test_agent.AgentTests.test_inner_brain_candidates_lists_llm_and_memory_fallback_prompts tests.test_agent.AgentTests.test_inner_brain_candidates_restore_on_startup tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：4 项通过，结果 `OK`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：372 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.18.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.18\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.18\.0 installation finished'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.18.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：499 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；构建日志包含既有 `tzdata` hidden import warning，但命令退出码为 0。
- 打包后 `JarvisLite.exe --smoke`：退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.18.0.exe` 均存在，大小均为 57,102,336 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.18.0"` 和 `Jarvis Lite 0.18.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.18.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

## 2026-05-29 0.11.0 LLM 外脑澄清轮数与过期策略验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_clarification_reclarify_preserves_original_prompt_and_reports_round tests.test_agent.AgentTests.test_llm_clarification_max_rounds_clears_pending tests.test_agent.AgentTests.test_expired_llm_clarification_pending_is_cleared_on_startup tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：失败 4 项，符合预期。连续澄清未报告轮次，超过上限未清理，过期 pending 仍消耗新输入，版本仍为 `0.10.0`。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_clarification_reclarify_preserves_original_prompt_and_reports_round tests.test_agent.AgentTests.test_llm_clarification_max_rounds_clears_pending tests.test_agent.AgentTests.test_expired_llm_clarification_pending_is_cleared_on_startup tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：4 项通过，结果 `OK`。

### 回归与收尾

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation tests.test_desktop_bridge tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.11.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
```

结果：

- 邻近回归：338 项通过。
- 全量 `unittest discover`：471 项通过。
- 源码桌面 smoke 和打包后 exe smoke 均通过。
- 安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.11.0.exe` 已生成，大小 57,090,048 bytes。
- `install.cmd` 和 `JarvisLiteSetup.sed` 均显示 `0.11.0`。
- `git diff --check`、Markdown 本地链接检查、敏感信息差异扫描均通过；本地 LLM/Search 配置未被跟踪且文件不存在。

## 2026-05-29 0.12.0 桌面外脑待补充状态验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_llm_pending_status_after_clarification tests.test_desktop_widgets.DesktopWidgetTests.test_panel_can_send_text_through_desktop_bridge tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_llm_pending_status_and_refreshes_after_cancel tests.test_desktop_widgets.DesktopWidgetTests.test_panel_restores_persisted_llm_pending_status_on_startup tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：失败 5 项，符合预期。`DesktopResponse`、`DesktopBridge` 和 `AssistantPanel` 尚未暴露或展示 LLM pending 状态，版本仍为 `0.11.0`。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_llm_pending_status_after_clarification tests.test_desktop_widgets.DesktopWidgetTests.test_panel_can_send_text_through_desktop_bridge tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_llm_pending_status_and_refreshes_after_cancel tests.test_desktop_widgets.DesktopWidgetTests.test_panel_restores_persisted_llm_pending_status_on_startup tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：5 项通过，结果 `OK`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：347 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.12.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.12\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.12\.0 installation finished'
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：474 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.12.0.exe` 均存在，大小均为 57,094,144 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.12.0"` 和 `Jarvis Lite 0.12.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.12.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

## 2026-05-29 0.13.0 桌面外脑运行状态验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_activity_status_records_recent_answer_fallback tests.test_agent.AgentTests.test_llm_activity_status_restores_recent_call_on_startup tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_llm_activity_status_after_answer tests.test_desktop_widgets.DesktopWidgetTests.test_panel_can_send_text_through_desktop_bridge tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_llm_activity_status_after_answer tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：失败 6 项，符合预期。`JarvisAgent.llm_activity_status_text()`、`DesktopResponse.llm_activity_status_text`、`DesktopBridge.llm_activity_status_text()` 和 `AssistantPanel.llm_activity_status_text()` 尚不存在，版本仍为 `0.12.0`。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_llm_activity_status_records_recent_answer_fallback tests.test_agent.AgentTests.test_llm_activity_status_restores_recent_call_on_startup tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_llm_activity_status_after_answer tests.test_desktop_widgets.DesktopWidgetTests.test_panel_can_send_text_through_desktop_bridge tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_llm_activity_status_after_answer tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：6 项通过，结果 `OK`。

## 2026-06-01 0.19.0 InnerBrain 候选按编号教学验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_teach_candidate_saves_selected_candidate_command tests.test_agent.AgentTests.test_inner_brain_teach_candidate_reports_missing_candidate tests.test_agent.AgentTests.test_inner_brain_teach_candidate_rejects_unknown_target_command -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v
```

结果：符合预期。

- 3 个候选教学测试失败或错误，`/inner-brain-teach-candidate` 尚未实现。
- 版本一致性测试失败，`pyproject.toml` 仍为 `0.18.0`，期望 `0.19.0`。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_teach_candidate_saves_selected_candidate_command tests.test_agent.AgentTests.test_inner_brain_teach_candidate_reports_missing_candidate tests.test_agent.AgentTests.test_inner_brain_teach_candidate_rejects_unknown_target_command tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：4 项通过，结果 `OK`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：375 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.19.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.19\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.19\.0 installation finished'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.19.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：502 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；构建日志包含既有 `tzdata` hidden import warning，但命令退出码为 0。
- 打包后 `JarvisLite.exe --smoke`：退出码 0。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.19.0.exe` 均存在，大小均为 57,102,336 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.19.0"` 和 `Jarvis Lite 0.19.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.19.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

## 2026-05-29 0.17.0 路由历史详情验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_route_history_command_reports_empty_state tests.test_agent.AgentTests.test_route_history_command_reports_recent_decisions_with_explanations tests.test_agent.AgentTests.test_route_history_command_restores_on_startup tests.test_agent.AgentTests.test_recent_context_includes_recent_route_history -v
.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v
```

结果：4 个路由历史详情测试按预期失败，版本一致性测试按预期失败。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_route_history_command_reports_empty_state tests.test_agent.AgentTests.test_route_history_command_reports_recent_decisions_with_explanations tests.test_agent.AgentTests.test_route_history_command_restores_on_startup tests.test_agent.AgentTests.test_recent_context_includes_recent_route_history tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：5 项通过，结果 `OK`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：369 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.17.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.17\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.17\.0 installation finished'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.17.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：496 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；构建日志包含既有 `tzdata` hidden import warning，但命令退出码为 0。
- 打包后 `JarvisLite.exe --smoke`：退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.17.0.exe` 均存在，大小均为 57,102,336 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.17.0"` 和 `Jarvis Lite 0.17.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.17.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：365 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.16.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.16\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.16\.0 installation finished'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.16.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：492 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；构建日志包含既有 `tzdata` hidden import warning，但命令退出码为 0。
- 打包后 `JarvisLite.exe --smoke`：退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.16.0.exe` 均存在，大小均为 57,098,240 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.16.0"` 和 `Jarvis Lite 0.16.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.16.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：351 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.13.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.13\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.13\.0 installation finished'
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：478 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.13.0.exe` 均存在，大小均为 57,094,144 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.13.0"` 和 `Jarvis Lite 0.13.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.13.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

## 2026-05-29 0.14.0 最近路由决策状态验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_route_status_records_inner_brain_greeting_without_llm tests.test_agent.AgentTests.test_route_status_records_llm_fallback tests.test_agent.AgentTests.test_route_status_records_identity_memory_answer tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_route_status_for_inner_brain_reply tests.test_desktop_widgets.DesktopWidgetTests.test_panel_can_send_text_through_desktop_bridge tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_route_status_after_inner_brain_reply tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：先失败 6 项，符合预期。`JarvisAgent.route_status_text()`、`DesktopResponse.route_status_text`、`DesktopBridge.route_status_text()` 和 `AssistantPanel.route_status_text()` 尚不存在，版本仍为 `0.13.0`。追加身份记忆路由测试后新增 1 项失败，证明身份记忆早返回分支会保留旧状态。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_route_status_records_inner_brain_greeting_without_llm tests.test_agent.AgentTests.test_route_status_records_llm_fallback tests.test_agent.AgentTests.test_route_status_records_identity_memory_answer tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_route_status_for_inner_brain_reply tests.test_desktop_widgets.DesktopWidgetTests.test_panel_can_send_text_through_desktop_bridge tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_route_status_after_inner_brain_reply tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：7 项通过，结果 `OK`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：356 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.14.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.14\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.14\.0 installation finished'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.14.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：483 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 `JarvisLite.exe --smoke`：退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.14.0.exe` 均存在，大小均为 57,098,240 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.14.0"` 和 `Jarvis Lite 0.14.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.14.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

## 2026-05-29 0.15.0 路由解释详情验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_route_status_records_inner_brain_greeting_without_llm tests.test_agent.AgentTests.test_route_status_explains_inner_brain_decision tests.test_agent.AgentTests.test_route_status_explains_inner_brain_clarification tests.test_agent.AgentTests.test_route_status_explanation_restores_on_startup tests.test_agent.AgentTests.test_route_status_records_llm_fallback tests.test_agent.AgentTests.test_route_status_explains_llm_fallback tests.test_agent.AgentTests.test_route_status_records_identity_memory_answer tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_route_status_for_inner_brain_reply tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_route_status_after_inner_brain_reply tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：10 项中 7 项失败，符合预期。

- `route_status_text()` 尚无 `依据：` 行。
- InnerBrain 执行、InnerBrain 澄清、LLM fallback 和运行态恢复均缺少解释详情。
- 桌面 Bridge/Panel 只能透传旧路由状态。
- 项目版本仍为 `0.14.0`，期望 `0.15.0`。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_route_status_records_inner_brain_greeting_without_llm tests.test_agent.AgentTests.test_route_status_explains_inner_brain_decision tests.test_agent.AgentTests.test_route_status_explains_inner_brain_clarification tests.test_agent.AgentTests.test_route_status_explanation_restores_on_startup tests.test_agent.AgentTests.test_route_status_records_llm_fallback tests.test_agent.AgentTests.test_route_status_explains_llm_fallback tests.test_agent.AgentTests.test_route_status_records_identity_memory_answer tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_route_status_for_inner_brain_reply tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_route_status_after_inner_brain_reply tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：10 项通过，结果 `OK`。

### 邻近回归

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v
```

结果：360 项通过，结果 `OK`。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Copy-Item -LiteralPath ..\jarvis-lite-dist\JarvisLiteSetup.exe -Destination ..\jarvis-lite-dist\JarvisLiteSetup-0.15.0.exe -Force
..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke
Select-String -Path ..\jarvis-lite-dist\windows-installer-stage\install.cmd -Pattern 'DisplayVersion|Jarvis Lite 0\.15\.0 installed'
Select-String -Path ..\jarvis-lite-dist\JarvisLiteSetup.sed -Pattern 'Jarvis Lite 0\.15\.0 installation finished'
Get-Item ..\jarvis-lite-dist\JarvisLiteSetup.exe, ..\jarvis-lite-dist\JarvisLiteSetup-0.15.0.exe
git diff --check
Markdown 本地链接检查脚本
敏感信息差异扫描
git ls-files config/llm.local.json config/search.local.json
Test-Path .\config\llm.local.json
Test-Path .\config\search.local.json
```

结果：

- 全量 `unittest discover`：487 项通过，结果 `OK`。
- 源码桌面 smoke：通过，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装器构建成功，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；构建日志包含既有 `tzdata` hidden import warning，但命令退出码为 0。
- 打包后 `JarvisLite.exe --smoke`：退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.15.0.exe` 均存在，大小均为 57,098,240 bytes。
- `install.cmd` 包含 `DisplayVersion /d "0.15.0"` 和 `Jarvis Lite 0.15.0 installed`。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.15.0 installation finished`。
- `git diff --check`：退出 0，仅 LF/CRLF 工作区换行提示。
- Markdown 本地链接检查：通过，输出 `Markdown local links OK`。
- 敏感信息差异扫描：通过，输出 `Sensitive diff scan OK`。
- `config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪，工作区本地配置文件不存在，`Test-Path` 均为 `False`。

## 2026-05-29 0.16.0 最近路由历史验证

### RED

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_route_status_tracks_recent_route_history tests.test_agent.AgentTests.test_route_status_history_restores_on_startup tests.test_agent.AgentTests.test_route_status_history_keeps_five_latest_entries tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_recent_route_history tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_recent_route_history tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：6 项中 5 项失败、1 项错误，符合预期。

- `RuntimeContext` 尚无 `recent_route_decisions`。
- `route_status_text()` 尚无“最近路由历史”。
- 桌面 Bridge/Panel 只能展示最新路由。
- 项目版本仍为 `0.15.0`，期望 `0.16.0`。

### GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_route_status_tracks_recent_route_history tests.test_agent.AgentTests.test_route_status_history_restores_on_startup tests.test_agent.AgentTests.test_route_status_history_keeps_five_latest_entries tests.test_desktop_bridge.DesktopBridgeTests.test_send_exposes_recent_route_history tests.test_desktop_widgets.DesktopWidgetTests.test_panel_shows_recent_route_history tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v
```

结果：6 项通过，结果 `OK`。
## 2026-06-01 0.22.0 InnerBrain 候选运行态统计

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_candidates_keep_persistent_counts_after_recent_history_rotation tests.test_agent.AgentTests.test_inner_brain_teach_candidate_uses_persistent_rank_after_recent_history_rotation tests.test_agent.AgentTests.test_inner_brain_teach_candidate_removes_trained_persistent_candidate tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项按预期失败。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v`，384 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，511 项 OK。
- 桌面 smoke：源码与打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.22.0.exe`，大小 `57,106,432` 字节。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查、敏感信息差异扫描、本地配置跟踪检查均通过。

## 2026-06-01 0.23.0 桌面内脑候选快捷入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_quick_commands_include_current_assistant_capabilities tests.test_desktop_bridge.DesktopBridgeTests.test_direct_quick_commands_exclude_commands_that_need_arguments tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_only_direct_quick_command_buttons tests.test_desktop_widgets.DesktopWidgetTests.test_panel_inner_brain_candidates_quick_command_submits_candidates_command tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，5 项按预期失败。
- GREEN：同一目标命令通过，5 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v`，385 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，512 项 OK。
- 桌面 smoke：源码 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；打包后窗口版 exe smoke 退出码 0。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.23.0.exe`，大小 `57,106,432` 字节。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查、敏感信息差异扫描、本地配置跟踪检查均通过。

## 2026-06-01 0.24.0 桌面候选训练模板填充

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_inner_brain_candidate_template_controls tests.test_desktop_widgets.DesktopWidgetTests.test_panel_inner_brain_teach_template_button_fills_input_without_submitting tests.test_desktop_widgets.DesktopWidgetTests.test_panel_inner_brain_label_template_button_fills_label_template_for_selected_candidate tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 个桌面测试报 `AttributeError`，版本测试失败，符合预期。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v`，388 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，515 项 OK。
- 桌面 smoke：源码 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；打包后窗口版 exe smoke 退出码 0。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.24.0.exe`，大小 `57,110,528` 字节。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查、敏感信息差异扫描、本地配置跟踪检查均通过。

## 2026-06-01 0.25.0 桌面候选模板状态同步

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_empty_inner_brain_candidates_disables_candidate_template_buttons tests.test_desktop_widgets.DesktopWidgetTests.test_panel_inner_brain_candidates_result_limits_template_index_to_candidate_count tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 个桌面测试缺少候选模板状态同步方法，版本测试失败，符合预期。
- GREEN：同一目标命令通过，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v`，390 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，517 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.25.0.exe`，大小 `57,110,528` 字节。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查、敏感信息差异扫描、本地配置跟踪检查均通过。

## 2026-06-01 0.26.0 桌面候选选择绑定

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_empty_inner_brain_candidates_disables_candidate_selector tests.test_desktop_widgets.DesktopWidgetTests.test_panel_inner_brain_candidate_selector_binds_selected_candidate_to_templates tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 个桌面测试报 `AttributeError`，版本测试失败，符合预期。
- GREEN：同一目标命令通过，3 项 OK。
- 桌面 widget 专项：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`，37 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v`，355 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，519 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.26.0.exe`，大小 `57,110,528` 字节。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查、敏感信息差异扫描、本地配置跟踪检查均通过。

## 2026-06-01 0.27.0 桌面候选目标预填

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_exposes_inner_brain_candidate_template_controls tests.test_desktop_widgets.DesktopWidgetTests.test_panel_inner_brain_teach_template_can_prefill_known_target_command tests.test_desktop_widgets.DesktopWidgetTests.test_panel_inner_brain_label_template_can_prefill_known_intent_template tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 个桌面测试报缺少目标预填 helper，版本测试失败，符合预期。
- GREEN：同一目标命令通过，4 项 OK。
- 桌面 widget 专项：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`，39 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation -v`，355 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，521 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.27.0.exe`，大小 `57,114,624` 字节。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (116 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；本地配置跟踪检查通过。

## 2026-06-01 0.28.0 InnerBrain 样本包含签名置信度补偿

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_sample_classifier_boosts_contained_sample_signature tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期失败；自然语言长句只进入 `CLARIFY`，版本测试仍期望 `0.28.0`。
- GREEN：同一目标命令通过，2 项 OK。
- InnerBrain 专项：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v`，25 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，395 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，522 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.28.0.exe`，大小 `57,114,624` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.28.0"` 和 `Jarvis Lite 0.28.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.28.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (266 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；本地配置跟踪检查通过。

## 2026-06-01 0.29.0 InnerBrain 固定评估集

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_evaluation_reports_repeatable_seed_baseline tests.test_agent.AgentTests.test_inner_brain_eval_command_reports_repeatable_seed_baseline tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，评估 API 导入失败、`/inner-brain-eval` 返回未知命令、版本测试失败，符合预期。
- GREEN：同一目标命令通过，3 项 OK。
- InnerBrain 专项：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v`，26 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，397 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，524 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.29.0.exe`，大小 `57,114,624` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.29.0"` 和 `Jarvis Lite 0.29.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.29.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (268 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；本地配置跟踪检查通过。

## 2026-06-01 0.30.0 InnerBrain 本机评估集扩展

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_evaluation_loads_local_jsonl_cases tests.test_agent.AgentTests.test_inner_brain_eval_command_includes_local_evaluation_cases_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，`load_evaluation_cases` 导入失败、`/inner-brain-eval` 未合并本机评估样本、版本测试失败，符合预期。
- GREEN：同一目标命令通过，3 项 OK。
- InnerBrain 专项：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v`，27 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，399 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，526 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.30.0.exe`，大小 `57,118,720` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.30.0"` 和 `Jarvis Lite 0.30.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.30.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (119 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；本地配置跟踪检查通过。

## 2026-06-01 0.31.0 InnerBrain 评估失败修复建议

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_evaluation_describes_failed_cases_with_training_suggestions tests.test_agent.AgentTests.test_inner_brain_eval_command_suggests_explicit_training_for_failed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，失败建议缺失、Agent 命令失败建议缺失、版本测试失败，符合预期。
- GREEN：同一目标命令通过，3 项 OK。
- InnerBrain 专项：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v`，28 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，401 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，528 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.31.0.exe`，大小 `57,118,720` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.31.0"` 和 `Jarvis Lite 0.31.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.31.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (120 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；本地配置跟踪检查通过。

## 2026-06-01 0.32.0 InnerBrain 评估失败过滤视图

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_evaluation_can_describe_failed_cases_only tests.test_agent.AgentTests.test_inner_brain_eval_failed_command_lists_only_failed_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，`failures_only` 参数缺失、`/inner-brain-eval-failed` 未知命令、版本测试失败，符合预期。
- GREEN：同一目标命令通过，3 项 OK。
- InnerBrain 专项：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v`，29 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，403 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，530 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.32.0.exe`，大小 `57,118,720` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.32.0"` 和 `Jarvis Lite 0.32.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.32.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (121 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；本地配置跟踪检查通过。

## 2026-06-01 0.33.0 InnerBrain 本机评估过滤视图

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_evaluation_can_filter_local_evaluation_source tests.test_agent.AgentTests.test_inner_brain_eval_local_command_lists_only_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_lists_only_failed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，`source_filter` 参数缺失、`/inner-brain-eval-local` 未知、`/inner-brain-eval-local-failed` 未知、版本测试失败，符合预期。
- GREEN：同一目标命令通过，4 项 OK。
- InnerBrain 专项：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v`，30 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，406 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，533 项 OK；提交前重新执行同一全量命令，533 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.33.0.exe`，大小 `57,118,720` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.33.0"` 和 `Jarvis Lite 0.33.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.33.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (122 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；本地配置跟踪检查通过。

## 2026-06-01 0.34.0 InnerBrain 本机评估样本写入

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_save_local_evaluation_case_writes_reloadable_jsonl_without_training tests.test_agent.AgentTests.test_inner_brain_eval_add_command_saves_local_evaluation_case_without_training tests.test_agent.AgentTests.test_inner_brain_eval_label_command_saves_local_evaluation_case_without_training tests.test_agent.AgentTests.test_inner_brain_eval_add_rejects_unknown_command_without_writing_case tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，`save_local_evaluation_case` 导入失败、两个 eval 写入命令未知、未知命令拒绝路径仍返回未知命令、版本测试失败，符合预期。
- GREEN：同一目标命令通过，5 项 OK。
- InnerBrain 专项：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain -v`，31 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，410 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，537 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.34.0.exe`，大小 `57,122,816` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.34.0"` 和 `Jarvis Lite 0.34.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.34.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (276 checked across 123 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在。

## 2026-06-02 0.35.0 InnerBrain 候选编号写入本机评估样本

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_add_candidate_saves_selected_candidate_command_without_training tests.test_agent.AgentTests.test_inner_brain_eval_label_candidate_saves_selected_candidate_label_without_training tests.test_agent.AgentTests.test_inner_brain_eval_add_candidate_reports_missing_candidate_without_writing_case tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项按预期失败；新命令未知、评估文件未写出、版本仍为 `0.34.0`。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，413 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，540 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.35.0.exe`，大小 `57,122,816` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.35.0"` 和 `Jarvis Lite 0.35.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.35.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (278 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在。

## 2026-06-02 0.36.0 InnerBrain 本机评估 JSONL 文件过滤

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_evaluation_can_filter_local_evaluation_file tests.test_agent.AgentTests.test_inner_brain_eval_local_file_command_lists_only_selected_local_file_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，1 项 ERROR、3 项 FAIL；`source_file_filter` API 缺失、两个 eval local file 命令未知、版本仍为 `0.35.0`，符合预期。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，416 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，543 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.36.0.exe`，大小 `57,122,816` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.36.0"` 和 `Jarvis Lite 0.36.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.36.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接检查输出 `Markdown local links OK (288 checked across 126 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在。

## 2026-06-02 0.37.0 InnerBrain 本机评估失败文件分组

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_groups_local_failures_by_file tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_groups_failures_by_local_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项按预期 FAIL；失败视图缺少 `失败文件：`，仍混入通过文件 `real-log.jsonl` 的来源计数，版本仍为 `0.36.0`。
- GREEN：同一目标命令通过，3 项 OK。
- 目标复跑：同一目标命令在收尾前复跑通过，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_llm tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_conversation -v`，418 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，545 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.37.0.exe`，大小 `57,126,912` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.37.0"` 和 `Jarvis Lite 0.37.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.37.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (291 checked across 30 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.38.0 InnerBrain 本机评估失败报告导出

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_can_filter_local_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项按预期 FAIL；导出 API 缺失、`/inner-brain-eval-local-report` 未知、版本仍为 `0.37.0`。
- GREEN：同一目标命令通过，4 项 OK。
- 目标复跑：同一目标命令在收尾前复跑通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，327 项 OK；首次失败的更新检测 fixture 已从 `0.37.1` 同步为 `0.38.1` 后复跑通过。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，548 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.38.0.exe`，大小 `57,126,912` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.38.0"` 和 `Jarvis Lite 0.38.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.38.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (294 checked across 30 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.39.0 InnerBrain 本机评估失败原因汇总

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_summarizes_failure_reasons tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，1 项 ERROR、3 项 FAIL；`failed_reason_counts` 缺失、报告缺少 `失败原因汇总：`、版本仍为 `0.38.0`。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归首次：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，1 项失败；根因是更新检测测试断言仍为 `0.38.1`，fixture 已为 `0.39.1`。
- 相邻回归复跑：同一命令通过，328 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，549 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.39.0.exe`，大小 `57,126,912` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.39.0"` 和 `Jarvis Lite 0.39.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.39.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (297 checked across 130 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.40.0 InnerBrain 本机评估失败类型汇总

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_summarizes_failure_reason_categories tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，1 项 ERROR、3 项 FAIL；`failed_reason_category_counts` 缺失、报告缺少 `失败类型汇总：`、版本仍为 `0.39.0`。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，329 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，550 项 OK。
- 桌面 smoke：源码输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`；打包后 exe 复跑输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.40.0.exe`，大小 `57,126,912` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.40.0"` 和 `Jarvis Lite 0.40.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.40.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (300 checked across 131 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.41.0 InnerBrain 本机评估失败期望意图汇总

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_summarizes_failed_expected_intents tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，1 项 ERROR、3 项 FAIL；`failed_expected_intent_counts` 缺失、报告缺少 `失败期望意图汇总：`、版本仍为 `0.40.0`。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，330 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，551 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.41.0.exe`，大小 `57,126,912` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.41.0"` 和 `Jarvis Lite 0.41.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.41.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (303 checked across 132 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.42.0 InnerBrain 本机评估失败意图混淆汇总

- RED 首次命令误用了旧测试类名 `InnerBrainEvaluationTests` / `JarvisAgentTests`，出现测试加载错误；修正为 `InnerBrainTests` / `AgentTests` 后复跑。
- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_summarizes_failed_intent_confusions tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，1 项 ERROR、3 项 FAIL；`failed_intent_confusion_counts` 缺失、报告缺少 `失败意图混淆汇总：`、版本仍为 `0.41.0`。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，331 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，552 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.42.0.exe`，大小 `57,126,912` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.42.0"` 和 `Jarvis Lite 0.42.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.42.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (306 checked across 132 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.43.0 InnerBrain 本机评估失败文件意图混淆汇总

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_summarizes_failed_file_intent_confusions tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，1 项 ERROR、3 项 FAIL；`failed_source_file_intent_confusion_counts` 缺失、报告缺少 `失败文件意图混淆汇总：`、版本仍为 `0.42.0`。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，332 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，553 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.43.0.exe`，大小 `57,131,008` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.43.0"` 和 `Jarvis Lite 0.43.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.43.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (309 checked across 133 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.44.0 InnerBrain 本机评估失败意图混淆修复建议分组

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_groups_fix_suggestions_by_intent_confusion tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项 FAIL；失败视图和报告缺少 `失败意图混淆修复建议：`，版本仍为 `0.43.0`。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，333 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，554 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.44.0.exe`，大小 `57,131,008` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.44.0"` 和 `Jarvis Lite 0.44.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.44.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (312 checked across 135 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.45.0 InnerBrain 本机失败评估文件意图混淆修复建议分组

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_groups_fix_suggestions_by_file_intent_confusion tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项 FAIL；失败视图和报告缺少 `失败文件意图混淆修复建议：`，版本仍为 `0.44.0`。
- GREEN：补强单文件过滤负向断言后目标命令通过，5 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，334 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，555 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.45.0.exe`，大小 `57,131,008` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.45.0"` 和 `Jarvis Lite 0.45.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.45.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (315 checked across 136 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.46.0 InnerBrain 本机评估空样本引导

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_local_evaluation_empty_state_suggests_evaluation_sample_commands tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_guides_empty_local_evaluation_samples tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项按预期 FAIL；空本机评估描述缺少样本添加命令引导，版本仍为 `0.45.0`。
- GREEN：同一目标命令通过，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，336 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，557 项 OK。
- 实际空本机评估命令：`.\.venv\Scripts\python.exe src\app.py --once "/inner-brain-eval-local-failed"` 输出本机评估样本为空、四个 evaluation 样本添加入口和不自动训练说明。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.46.0.exe`，大小 `57,131,008` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.46.0"` 和 `Jarvis Lite 0.46.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.46.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (318 checked across 136 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.47.0 InnerBrain 本机评估样本保存后续验证提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_add_command_saves_local_evaluation_case_without_training tests.test_agent.AgentTests.test_inner_brain_eval_add_candidate_saves_selected_candidate_command_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项按预期 FAIL；保存反馈缺少 `后续验证：`，版本仍为 `0.46.0`。
- GREEN：同一目标命令通过，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，336 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，557 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.47.0.exe`，大小 `57,131,008` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.47.0"` 和 `Jarvis Lite 0.47.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.47.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (321 checked across 137 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.48.0 InnerBrain 本机失败报告导出后续处理提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_can_filter_local_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项按预期 FAIL；报告导出响应缺少 `后续处理：`，版本仍为 `0.47.0`。
- GREEN：同一目标命令通过，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，336 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，557 项 OK。
- 桌面 smoke：源码和打包后 exe 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.48.0.exe`，大小 `57,131,008` 字节。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.48.0"` 和 `Jarvis Lite 0.48.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.48.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (324 checked across 138 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.51.0 InnerBrain 本机 evaluation 已处理样本只读清单

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_resolved_evaluation_lists_only_passed_local_cases tests.test_inner_brain.InnerBrainTests.test_inner_brain_resolved_evaluation_reports_empty_passed_list tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_lists_only_passed_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_can_filter_local_file tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_reports_empty_passed_list tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，6 项按预期失败或错误；新描述函数未导出，Agent 返回未知命令，版本仍为 `0.50.0`。
- GREEN：同一目标命令通过，6 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，341 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，562 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.51.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0；窗口版 exe 未回显 stdout。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.51.0"` 和 `Jarvis Lite 0.51.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.51.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.51.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (332 checked across 309 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。
## 2026-06-02 0.49.0 InnerBrain 本机失败视图导出报告提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_guides_empty_local_evaluation_samples tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_lists_only_failed_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项中 3 项按预期 FAIL；本机失败视图缺少 `后续处理：`，版本仍为 `0.48.0`；空样本负向断言通过。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，336 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，557 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.49.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.49.0"` 和 `Jarvis Lite 0.49.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.49.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.49.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (327 checked across 140 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.50.0 InnerBrain 本机失败视图文件聚焦提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_guides_empty_local_evaluation_samples tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_lists_only_failed_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项中 3 项按预期 FAIL；本机失败视图缺少文件聚焦/查看全部失败样本提示，版本仍为 `0.49.0`；空样本负向断言通过。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，336 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，557 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.50.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.50.0"` 和 `Jarvis Lite 0.50.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.50.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.50.0.exe` 均为 `57,126,912` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (330 checked across 141 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.52.0 InnerBrain 本机评估全量视图后续处理提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_command_lists_only_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_guides_empty_local_evaluation_samples tests.test_agent.AgentTests.test_inner_brain_eval_local_file_command_lists_only_selected_local_file_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项中 3 项按预期 FAIL；本机全量评估和文件全量评估响应缺少 `后续处理：`，版本仍为 `0.51.0`；空样本负向断言通过。
- GREEN：同一目标命令通过，4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，341 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，562 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.52.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.52.0"` 和 `Jarvis Lite 0.52.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.52.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.52.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (334 checked across 30 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.53.0 InnerBrain 本机评估全量视图文件名候选提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_command_lists_only_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_file_command_lists_only_selected_local_file_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项中 2 项按预期 FAIL；本机全量评估缺少 `可聚焦文件：` 与具体文件命令，版本仍为 `0.52.0`；文件过滤视图未回归。
- GREEN：同一目标命令通过，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，341 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，562 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.53.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.53.0"` 和 `Jarvis Lite 0.53.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.53.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.53.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (339 checked across 30 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.54.0 InnerBrain 本机评估全量视图文件候选状态摘要

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_command_lists_only_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_file_command_lists_only_selected_local_file_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项中 2 项按预期 FAIL；本机全量评估文件候选行缺少 `通过 N 条，失败 N 条`，版本仍为 `0.53.0`；文件过滤视图未回归。
- GREEN：同一目标命令通过，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，341 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，562 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.54.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.54.0"` 和 `Jarvis Lite 0.54.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.54.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.54.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (341 checked across 145 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.55.0 InnerBrain 本机评估全量视图文件候选失败优先排序

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_command_lists_only_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_file_command_lists_only_selected_local_file_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项中 2 项按预期 FAIL；本机全量评估文件候选仍按来源文件名顺序展示，失败文件未排到纯通过文件前，版本仍为 `0.54.0`；文件过滤视图未回归。
- GREEN：同一目标命令通过，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，341 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，562 项 OK；提交前复跑同一全量命令仍为 562 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.55.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.55.0"` 和 `Jarvis Lite 0.55.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.55.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.55.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (343 checked across 146 files)`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.56.0 InnerBrain 本机失败视图失败文件汇总排序

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_sorts_failure_files_by_failed_count tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_sorts_failure_files_by_failed_count tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项按预期 FAIL；失败文件仍按原顺序展示，版本仍为 `0.55.0`。
- GREEN：同一目标命令通过，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent -v`，343 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.56.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.56.0"` 和 `Jarvis Lite 0.56.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.56.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.56.0.exe` 均为 `57,135,104` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (348 checked across markdown files)`；敏感信息差异扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.57.0 InnerBrain 本机文件失败视图已处理入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；当前文件失败视图缺少 `- 查看当前文件已处理样本：/inner-brain-eval-local-resolved failed-log.jsonl`，版本仍为 `0.56.0`。
- GREEN：同一目标命令通过，2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，302 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.57.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.57.0"` 和 `Jarvis Lite 0.57.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.57.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.57.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (351 checked across 148 files)`；敏感信息差异扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.58.0 InnerBrain 本机已处理视图文件候选提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_lists_only_passed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；全量已处理视图缺少 `可查看文件：`，版本仍为 `0.57.0`。
- GREEN：同一目标命令通过，2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，302 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.58.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.58.0"` 和 `Jarvis Lite 0.58.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.58.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.58.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 354 checked across 328 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.59.0 InnerBrain 本机已处理视图文件候选状态摘要

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_lists_only_passed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；全量已处理视图候选行缺少 `已处理 1 条，待处理失败 1 条`，版本仍为 `0.58.0`。
- GREEN：同一目标命令通过，2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，302 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.59.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.59.0"` 和 `Jarvis Lite 0.59.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.59.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.59.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 357 checked across 329 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 未被 Git 跟踪且当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.60.0 InnerBrain 本机已处理视图文件候选待处理优先排序

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_lists_only_passed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；`clean-log.jsonl` 因通过数更多排在仍有待处理失败的 `real-log.jsonl` 前，版本仍为 `0.59.0`。
- GREEN：同一目标命令通过，2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，302 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.60.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.60.0"` 和 `Jarvis Lite 0.60.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.60.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.60.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 360 checked across 330 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.61.0 InnerBrain 本机已处理视图文件候选待处理入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_lists_only_passed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；候选行缺少 `待处理：/inner-brain-eval-local-file-failed real-log.jsonl`，版本仍为 `0.60.0`。
- GREEN：同一目标命令通过，2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，302 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.61.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.61.0"` 和 `Jarvis Lite 0.61.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.61.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.61.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 363 checked across 331 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.62.0 InnerBrain 本机评估全量视图文件候选待处理入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_command_lists_only_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；候选行缺少 `待处理：/inner-brain-eval-local-file-failed zzz-failed-log.jsonl`，版本仍为 `0.61.0`。
- GREEN：同一目标命令通过，2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，302 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.62.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`install.cmd` 包含 `DisplayVersion /d "0.62.0"` 和 `Jarvis Lite 0.62.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.62.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.62.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 366 checked across 332 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.63.0 InnerBrain 本机失败视图失败文件分组聚焦入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_groups_local_failures_by_file tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_sorts_failure_files_by_failed_count tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_groups_failures_by_local_file tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_sorts_failure_files_by_failed_count tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，5 项按预期 FAIL；失败文件行缺少 `/inner-brain-eval-local-file-failed failed-log.jsonl`，版本仍为 `0.62.0`。
- GREEN：同一目标命令通过，5 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_project_metadata -v`，347 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.63.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.63.0"` 和 `Jarvis Lite 0.63.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.63.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.63.0.exe` 均为 `57,135,104` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 367 checked across 153 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.64.0 InnerBrain 本机失败视图失败文件分组报告入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_groups_local_failures_by_file tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_sorts_failure_files_by_failed_count tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_groups_failures_by_local_file tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_sorts_failure_files_by_failed_count tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，5 项按预期 FAIL；失败文件行缺少 `报告：/inner-brain-eval-local-report failed-log.jsonl`，版本仍为 `0.63.0`。
- GREEN：同一目标命令通过，5 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain tests.test_agent tests.test_project_metadata -v`，347 项 OK。
- 全量：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.64.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.64.0"` 和 `Jarvis Lite 0.64.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.64.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.64.0.exe` 均为 `57,135,104` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 368 checked across 155 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。
## 2026-06-02 0.65.0 InnerBrain 本机评估全量视图文件候选报告入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_command_lists_only_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；候选行缺少 `报告：/inner-brain-eval-local-report zzz-failed-log.jsonl`，版本仍为 `0.64.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，302 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.65.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.65.0"` 和 `Jarvis Lite 0.65.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.65.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.65.0.exe` 均为 `57,135,104` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 369 checked across 156 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.66.0 InnerBrain 本机已处理视图文件候选报告入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_lists_only_passed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；候选行缺少 `报告：/inner-brain-eval-local-report real-log.jsonl`，版本仍为 `0.65.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，302 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，564 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.66.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.66.0"` 和 `Jarvis Lite 0.66.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.66.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.66.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 374 checked across 157 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.67.0 InnerBrain 本机文件视图报告入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_file_command_lists_only_selected_local_file_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_file_command_suggests_report_for_failed_selected_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项中 2 项按预期 FAIL；指定文件总览缺少 `导出当前文件失败报告：/inner-brain-eval-local-report failed-log.jsonl`，版本仍为 `0.66.0`，纯通过指定文件负向断言已通过。
- GREEN：同一目标命令 3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，303 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，565 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.67.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.67.0"` 和 `Jarvis Lite 0.67.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.67.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.67.0.exe` 均为 `57,135,104` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 376 checked across 158 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-02 0.68.0 InnerBrain 本机已处理指定文件视图报告入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_can_filter_local_file tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_suggests_report_for_file_with_pending_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项中 2 项按预期 FAIL；指定文件已处理视图缺少 `导出当前文件失败报告：/inner-brain-eval-local-report real-log.jsonl`，版本仍为 `0.67.0`，纯通过指定文件负向断言已通过。
- GREEN：同一目标命令 3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.68.0.exe`。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 复跑输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.68.0"` 和 `Jarvis Lite 0.68.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.68.0 installation finished`。
- 安装包大小：`JarvisLiteSetup.exe` 与 `JarvisLiteSetup-0.68.0.exe` 均为 `57,131,008` 字节。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 378 checked across 159 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.69.0 InnerBrain 本机 evaluation 保存反馈按文件报告入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_add_command_saves_local_evaluation_case_without_training tests.test_agent.AgentTests.test_inner_brain_eval_label_command_saves_local_evaluation_case_without_training tests.test_agent.AgentTests.test_inner_brain_eval_add_candidate_saves_selected_candidate_command_without_training tests.test_agent.AgentTests.test_inner_brain_eval_label_candidate_saves_selected_candidate_label_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，5 项按预期 FAIL；四条保存反馈仍输出全局 `/inner-brain-eval-local-report`，版本仍为 `0.68.0`。
- GREEN：同一目标命令 5 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.69.0.exe`，大小 `57,131,008` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.69.0"` 和 `Jarvis Lite 0.69.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.69.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 394 checked across 334 files`；敏感信息差异扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.70.0 InnerBrain 本机失败报告导出反馈当前文件已处理入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_can_filter_local_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；文件级报告导出反馈缺少 `/inner-brain-eval-local-resolved failed-log.jsonl`，版本仍为 `0.69.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.70.0.exe`，大小 `57,131,008` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.70.0"` 和 `Jarvis Lite 0.70.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.70.0 installation finished`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 398 checked across 335 files`；敏感信息差异扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.71.0 InnerBrain 本机失败报告导出反馈当前文件总览入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_can_filter_local_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；文件级报告导出反馈缺少 `/inner-brain-eval-local-file failed-log.jsonl`，版本仍为 `0.70.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.71.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.71.0"` 和 `Jarvis Lite 0.71.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.71.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 401 checked across 336 files`；敏感信息差异扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.72.0 InnerBrain 本机文件失败视图当前文件总览入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；指定文件失败视图缺少 `/inner-brain-eval-local-file failed-log.jsonl`，版本仍为 `0.71.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.72.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.72.0"` 和 `Jarvis Lite 0.72.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.72.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 404 checked across 337 files`；敏感信息差异扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.73.0 InnerBrain 本机已处理指定文件视图当前文件总览入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_can_filter_local_file tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_suggests_report_for_file_with_pending_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项按预期 FAIL；指定文件已处理视图缺少 `/inner-brain-eval-local-file real-log.jsonl`，版本仍为 `0.72.0`。
- GREEN：同一目标命令 3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.73.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.73.0"` 和 `Jarvis Lite 0.73.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.73.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 407 checked across 338 files`；敏感信息差异扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.74.0 InnerBrain 本机失败视图失败文件分组当前文件总览入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_groups_failures_by_local_file tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_sorts_failure_files_by_failed_count tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_sorts_failure_files_by_failed_count tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项按预期 FAIL；失败文件分组缺少 `总览：/inner-brain-eval-local-file ...`，版本仍为 `0.73.0`。
- GREEN：同一目标命令 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_project_metadata -v`，349 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.74.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.74.0"` 和 `Jarvis Lite 0.74.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.74.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 410 checked across 339 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。
- 备注：SED 目标路径检查首次使用 `Select-String -Pattern` 导致 Windows 反斜杠正则解析失败，改用 `-SimpleMatch` 复验通过。

## 2026-06-03 0.75.0 InnerBrain 本机已处理视图文件候选当前文件总览入口

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_lists_only_passed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；全量已处理视图文件候选缺少 `总览：/inner-brain-eval-local-file ...`，版本仍为 `0.74.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.75.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.75.0"` 和 `Jarvis Lite 0.75.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.75.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 413 checked across 340 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.76.0 InnerBrain 本机评估全量视图文件候选总览标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_command_lists_only_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；全量本机评估文件候选仍使用裸 `/inner-brain-eval-local-file ...`，版本仍为 `0.75.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.76.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.76.0"` 和 `Jarvis Lite 0.76.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.76.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 416 checked across 348 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.77.0 InnerBrain 本机文件失败视图当前文件总览标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；指定文件失败视图仍输出旧的 `查看当前文件全部样本：...`，版本仍为 `0.76.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.77.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.77.0"` 和 `Jarvis Lite 0.77.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.77.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 419 checked across 169 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。
- 备注：安装脚本和 SED 首次按错误仓库内路径检查失败；按系统化调试定位到构建产物真实路径后复验通过。Markdown 链接检查使用 Git 跟踪的 Markdown 文件范围，未把 `.codex` 忽略留痕文件计入提交验证范围。

## 2026-06-03 0.78.0 InnerBrain 本机已处理指定文件视图当前文件总览标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_can_filter_local_file tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_suggests_report_for_file_with_pending_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项按预期 FAIL；指定文件已处理视图仍输出旧的 `查看当前文件全部样本：...`，版本仍为 `0.77.0`。
- GREEN：同一目标命令 3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.78.0.exe`，大小 `57,131,008` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，未发现残留 `JarvisLite*` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.78.0"` 和 `Jarvis Lite 0.78.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.78.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 422 checked across 170 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.79.0 InnerBrain 本机失败报告导出反馈当前文件总览标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_can_filter_local_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；指定文件报告导出反馈仍输出旧的 `查看当前文件全部样本：...`，版本仍为 `0.78.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.79.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，等待后未发现残留 `JarvisLite.exe` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.79.0"` 和 `Jarvis Lite 0.79.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.79.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 425 checked across 169 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。
- 调试备注：SED 路径检查首次使用 `Select-String -Pattern` 导致反斜杠正则解析失败，改用 `-SimpleMatch` 后复验通过；打包后 smoke 首次并行检查时短暂看到 `JarvisLite` 进程，等待 3 秒后自动退出，复跑确认输出和无残留进程。

## 2026-06-03 0.80.0 InnerBrain 本机失败报告导出反馈当前文件待处理失败标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_can_filter_local_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；指定文件报告导出反馈仍输出旧的 `复查当前文件失败样本：...`，版本仍为 `0.79.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.80.0.exe`，大小 `57,131,008` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式检查确认无残留 `JarvisLite.exe` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.80.0"` 和 `Jarvis Lite 0.80.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.80.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 428 checked across 172 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。
- 调试备注：打包后 smoke 与进程检查合并命令首次因 `Get-Process` 无结果产生非零退出；按系统化调试确认根因为检查命令写法后，改用显式分支复验无残留进程。

## 2026-06-03 0.81.0 InnerBrain 本机当前文件反馈全部待处理失败标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_can_filter_local_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项按预期 FAIL；指定文件失败视图和报告导出反馈仍输出旧的 `查看全部本机失败样本：...`，版本仍为 `0.80.0`。
- GREEN：同一目标命令 3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.81.0.exe`，大小 `57,131,008` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式检查确认无残留 `JarvisLite.exe` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.81.0"` 和 `Jarvis Lite 0.81.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.81.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 431 checked across 174 files`；敏感信息差异扫描输出 `Sensitive diff scan OK`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.82.0 InnerBrain 本机失败报告导出反馈全量待处理失败标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；全量报告导出反馈仍输出旧的 `查看本机失败样本：...`，版本仍为 `0.81.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.82.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式检查确认无残留 `JarvisLite.exe` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.82.0"` 和 `Jarvis Lite 0.82.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.82.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (175 files).`；敏感信息差异扫描输出 `Sensitive diff scan OK`；过期标记扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。
- 备注：Markdown 链接检查首次脚本正则未正确转义 Windows 盘符反斜杠，按系统化调试替换为 `Path.IsPathFullyQualified()` 后复验通过。

## 2026-06-03 0.83.0 InnerBrain 本机文件失败视图全部待处理失败报告标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；指定文件失败视图仍输出旧的 `导出全部本机失败报告：...`，版本仍为 `0.82.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.83.0.exe`，大小 `57,131,008` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式检查确认无残留 `JarvisLite.exe` 进程。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.83.0"` 和 `Jarvis Lite 0.83.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.83.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK (176 files).`；敏感信息差异扫描输出 `Sensitive diff scan OK`；当前文档过期标记扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.84.0 InnerBrain 本机失败视图待处理失败报告标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_lists_only_failed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；全量失败视图仍输出旧的 `导出本机失败报告：...`，版本仍为 `0.83.0`。
- 附加 RED：打包后 `..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 首次在 2 秒检查点残留 `JarvisLite.exe`；新增桌面 smoke 清理断言后，当前实现仍保留本次 smoke 创建的 `desktopPetWindow` 顶层 widget。
- GREEN：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_lists_only_failed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version tests.test_desktop_app.DesktopAppTests.test_smoke_mode_creates_desktop_pet_window -v`，3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata tests.test_desktop_app -v`，310 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.84.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `ProcessCount=0`。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.84.0"` 和 `Jarvis Lite 0.84.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.84.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 440 checked across 177 files`；敏感信息差异扫描无命中；旧文案和过期版本扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.85.0 InnerBrain 本机失败视图按文件待处理失败报告标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_lists_only_failed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，2 项按预期 FAIL；全量失败视图仍输出旧的 `按文件导出失败报告：...`，版本仍为 `0.84.0`。
- GREEN：同一目标命令 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.85.0.exe`，大小 `57,135,104` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `ProcessCount=0`。
- 安装脚本：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.85.0"` 和 `Jarvis Lite 0.85.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.85.0 installation finished`，`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 443 checked across 178 files`；敏感信息差异扫描无命中；旧文案和过期版本扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。
## 2026-06-03 0.86.0 InnerBrain 本机当前文件待处理失败报告标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_file_command_suggests_report_for_failed_selected_file tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_suggests_report_for_file_with_pending_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败，三个当前文件反馈仍输出旧的 `导出当前文件失败报告：...`，版本仍为 `0.85.0`。
- GREEN：同一目标命令 4 项通过。
- 相邻回归：首次因更新测试 manifest 夹具仍为 `0.85.1` 且断言未同步而失败；更新到 `0.86.1` 后复跑 `.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项通过。
- 源码 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.86.0.exe`，大小 `57,135,104` 字节。
- 安装脚本与 SED：包含 `DisplayVersion /d "0.86.0"`、`Jarvis Lite 0.86.0 installed`、`Jarvis Lite 0.86.0 installation finished` 和 `TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`；显式进程复查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 437 checked across 175 files`；敏感信息差异扫描、旧文案扫描和过期版本扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。
## 2026-06-03 0.87.0 InnerBrain 本机评估样本保存反馈待处理失败标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_add_command_saves_local_evaluation_case_without_training tests.test_agent.AgentTests.test_inner_brain_eval_label_command_saves_local_evaluation_case_without_training tests.test_agent.AgentTests.test_inner_brain_eval_add_candidate_saves_selected_candidate_command_without_training tests.test_agent.AgentTests.test_inner_brain_eval_label_candidate_saves_selected_candidate_label_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败，四个保存反馈仍输出旧的 `只看失败样本` 和 `导出样本文件失败报告`，版本仍为 `0.86.0`。
- GREEN：同一目标命令 5 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项通过。
- 源码 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.87.0.exe`，大小 `57,135,104` 字节。
- 安装脚本与 SED：包含 `DisplayVersion /d "0.87.0"`、`Jarvis Lite 0.87.0 installed`、`Jarvis Lite 0.87.0 installation finished` 和 `TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包后 smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`；显式进程复查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 440 checked across 176 files`；严格密钥形态扫描、旧文案扫描和过期版本扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.88.0 InnerBrain 本机文件候选待处理报告标签

- RED：修正测试名后运行 `.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_groups_local_failures_by_file tests.test_inner_brain.InnerBrainTests.test_inner_brain_failed_evaluation_sorts_failure_files_by_failed_count tests.test_agent.AgentTests.test_inner_brain_eval_local_command_lists_only_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_groups_failures_by_local_file tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_sorts_failure_files_by_failed_count tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_lists_only_passed_local_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败，7 项均为预期失败；文件候选/失败文件分组仍输出旧的 `报告` 短标签，项目版本仍为 `0.87.0`。
- GREEN：同一目标命令 7 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_project_metadata -v`，349 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.88.0.exe`，大小 `57,131,008` 字节。
- 打包后 exe smoke：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `ProcessCount=0`。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.88.0"`、`Jarvis Lite 0.88.0 installed`、`Jarvis Lite 0.88.0 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，`JarvisLite.version.txt` 的 `FileVersion` 与 `ProductVersion` 均为 `0.88.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 452 checked across 353 files`；严格密钥形态扫描、旧短标签扫描和过期版本扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.89.0 InnerBrain 本机报告导出待处理失败标题

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_can_filter_local_file tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，4 项按预期 FAIL；导出反馈和 Markdown H1 仍为旧的“本机评估失败报告”，版本仍为 `0.88.0`。
- GREEN：同一目标命令 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_project_metadata -v`，349 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.89.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.89.0"`、`Jarvis Lite 0.89.0 installed`、`Jarvis Lite 0.89.0 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，`JarvisLite.version.txt` 的 `FileVersion` 与 `ProductVersion` 均为 `0.89.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 455 checked across 354 files`；严格密钥形态扫描、旧标题/旧反馈扫描、过期版本扫描和当前文档过期标记扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.90.0 InnerBrain 本机失败帮助待处理标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_lists_only_failed_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_file_failed_command_lists_only_selected_file_failures tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；帮助和运行日志仍输出旧的“失败样本/失败评估报告”描述，版本仍为 `0.89.0`。
- GREEN：同一目标命令 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.90.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.90.0"`、`Jarvis Lite 0.90.0 installed`、`Jarvis Lite 0.90.0 installation finished`、`TargetName=E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，`JarvisLite.version.txt` 的 `FileVersion` 与 `ProductVersion` 均为 `0.90.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 458 checked across 181 files`；严格密钥形态扫描、旧帮助/旧日志扫描、过期版本扫描和当前文档过期标记扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.91.0 InnerBrain 本机报告导出反馈待处理失败计数标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_can_filter_local_file tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；报告导出成功反馈仍输出旧的 `失败样本：1`，版本仍为 `0.90.0`。
- GREEN：同一目标命令 3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.91.0.exe`，大小 `57,131,008` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.91.0"`、`Jarvis Lite 0.91.0 installed`、`Jarvis Lite 0.91.0 installation finished`，`JarvisLite.version.txt` 的 `FileVersion` 与 `ProductVersion` 均为 `0.91.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 461 checked across 356 files`；严格密钥形态扫描、旧反馈/旧断言/旧 manifest 夹具扫描和当前文档过期标记扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.92.0 InnerBrain 本机全量反馈按文件聚焦待处理失败标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_lists_only_failed_local_cases tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_exports_failed_markdown_without_training tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；两个全量反馈仍输出旧的 `按文件聚焦失败：...`，版本仍为 `0.91.0`。
- GREEN：同一目标命令 3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.92.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.92.0"`、`Jarvis Lite 0.92.0 installed`、`Jarvis Lite 0.92.0 installation finished`，`JarvisLite.version.txt` 的 `FileVersion` 与 `ProductVersion` 均为 `0.92.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 464 checked across 184 files`；严格密钥形态扫描、旧标签/旧 manifest 夹具扫描和当前文档过期标记扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.93.0 InnerBrain 全量评估运行日志固定与本机评估集标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_command_includes_local_evaluation_cases_without_training tests.test_agent.AgentTests.test_inner_brain_eval_failed_command_lists_only_failed_cases tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；两个全量评估运行日志仍输出旧的“本地评估集”，项目版本仍为 `0.92.0`。
- GREEN：同一目标命令 3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.93.0.exe`，大小 `57,131,008` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.93.0"`、`Jarvis Lite 0.93.0 installed`、`Jarvis Lite 0.93.0 installation finished`，`JarvisLite.version.txt` 的 `FileVersion` 与 `ProductVersion` 均为 `0.93.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 467 checked across 185 files`；严格密钥形态扫描、旧全量评估日志/旧 manifest 夹具扫描和当前文档过期标记扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.94.0 InnerBrain 全量评估输出固定与本机评估集标签

- RED：目标命令 7 项先失败；失败点为评估正文仍输出 `seed_evaluation`、`seed_evaluation+local_evaluation`、`local_evaluation` 内部名，版本仍为 `0.93.0`。
- 补充 RED：`describe_inner_brain_resolved_evaluation()` 两个函数层用例先失败，确认已处理样本视图仍输出 `local_evaluation`。
- GREEN：目标命令 7 项 OK；补充 resolved 函数层 2 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_project_metadata -v`，349 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.94.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.94.0"`、`Jarvis Lite 0.94.0 installed`、`Jarvis Lite 0.94.0 installation finished`，`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.94.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，显式进程检查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 470 checked across 186 files`；严格密钥形态扫描无命中；旧内部评估集显示名扫描仅剩测试负断言和内部 source key 断言；`config/llm.local.json` 与 `config/search.local.json` 当前不存在，`Test-Path` 均为 `False`。

## 2026-06-03 0.95.0 InnerBrain 全量评估帮助固定与本机评估集标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；帮助仍输出旧的泛化“评估集/评估失败样本”说明，版本仍为 `0.94.0`。
- GREEN：同一目标命令 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，304 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.95.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.95.0"`、`Jarvis Lite 0.95.0 installed`、`Jarvis Lite 0.95.0 installation finished`，`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.95.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，显式进程检查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 472 checked across 187 tracked files`；严格密钥形态扫描无命中；旧全量评估帮助文案扫描仅剩测试负断言；README BOM 保留；`config/llm.local.json` 与 `config/search.local.json` 当前不存在。

## 2026-06-03 0.96.0 InnerBrain 本机报告处理边界待处理失败标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 修正测试名后先失败；报告仍输出旧的“需要修复失败样本时”，版本仍为 `0.95.0`。
- GREEN：同一目标命令 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_project_metadata -v`，349 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，566 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.96.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.96.0"`、`Jarvis Lite 0.96.0 installed`、`Jarvis Lite 0.96.0 installation finished`；`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.96.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，显式进程检查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 474 checked across 188 tracked files`；严格密钥形态扫描无命中；旧报告处理边界提示和过期版本扫描无命中；README BOM 保留；`config/llm.local.json` 与 `config/search.local.json` 当前不存在。

## 2026-06-03 0.97.0 InnerBrain 本机失败视图文档待处理失败标签

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_current_docs_use_pending_failure_language_for_local_failed_view tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；README 仍输出旧的“只看失败”，PROJECT-PLAN 仍输出旧的“本机失败样本”，版本仍为 `0.96.0`。
- GREEN：扩展后的目标命令 `.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_current_docs_use_pending_failure_language_for_local_failed_view tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory -v` 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，305 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，567 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.97.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.97.0"`、`Jarvis Lite 0.97.0 installed`、`Jarvis Lite 0.97.0 installation finished`；`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.97.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，显式进程检查输出 `ProcessCount=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 479 checked across 189 tracked files`；严格密钥形态扫描无命中；活动公开文档旧标签、更新清单旧夹具和安装产物旧版本标记扫描无命中；README BOM 保留；`config/llm.local.json` 与 `config/search.local.json` 当前不存在。

## 2026-06-03 0.98.0 InnerBrain 本机报告指定文件样本计数提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_marks_empty_filtered_file_sample_count tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；指定文件报告反馈缺少 `当前文件样本：0`，版本仍为 `0.97.0`。
- GREEN：扩展后的目标命令 `.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_marks_empty_filtered_file_sample_count tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory -v` 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，306 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，568 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.98.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.98.0"`、`Jarvis Lite 0.98.0 installed`、`Jarvis Lite 0.98.0 installation finished`；`JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.98.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，显式进程检查输出 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 482 checked across 191 tracked files`；严格密钥形态扫描无命中；README BOM 保留；`config/llm.local.json` 与 `config/search.local.json` 当前不存在。

## 2026-06-03 0.99.0 InnerBrain 本机报告空筛选文件补样本写入提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_marks_empty_filtered_file_sample_count tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；指定文件空报告反馈缺少 `提示：当前筛选文件暂无本机 evaluation 样本；补样本命令默认写入 runtime.jsonl。`，版本仍为 `0.98.0`。
- GREEN：扩展后的目标命令 `.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_inner_brain_eval_local_report_command_marks_empty_filtered_file_sample_count tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory -v` 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，306 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，568 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.99.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.99.0"`、`Jarvis Lite 0.99.0 installed`、`Jarvis Lite 0.99.0 installation finished`；`JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.99.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，输出包含 `Jarvis Lite` 与 `desktopPetWindow`，显式进程检查输出 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 484 checked across 192 tracked/untracked files`；严格密钥形态扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在；`word/inner-brain-evaluation-report.md` 当前不存在；README BOM 保留。

## 2026-06-03 0.100.0 InnerBrain 本机空评估视图补样本写入提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_local_evaluation_empty_state_suggests_evaluation_sample_commands tests.test_agent.AgentTests.test_inner_brain_eval_local_command_guides_empty_local_evaluation_sample_target tests.test_agent.AgentTests.test_inner_brain_eval_local_failed_command_guides_empty_local_evaluation_samples tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory -v` 先失败；三处空本机 evaluation 视图缺少 `提示：补样本命令默认写入 runtime.jsonl。`，版本仍为 `0.99.0`。
- GREEN：同一目标命令 6 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_project_metadata -v`，352 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，569 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.100.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.100.0"`、`Jarvis Lite 0.100.0 installed`、`Jarvis Lite 0.100.0 installation finished`；`JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.100.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，输出包含 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 488 checked across 193 tracked/untracked files`；严格密钥形态扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在；`word/inner-brain-evaluation-report.md` 当前不存在；README BOM 保留。

## 2026-06-03 0.101.0 InnerBrain 本机已处理空视图行动提示

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_inner_brain.InnerBrainTests.test_inner_brain_resolved_evaluation_reports_empty_passed_list tests.test_agent.AgentTests.test_inner_brain_eval_local_resolved_command_reports_empty_passed_list tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory -v` 先失败；函数层和命令层缺少 `提示：这里只显示已通过样本；暂无已处理样本时，请先查看待处理失败样本或补充本机 evaluation 样本。`，版本仍为 `0.100.0`。
- GREEN：同一目标命令 5 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_inner_brain tests.test_project_metadata -v`，352 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，569 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.101.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.101.0"`、`Jarvis Lite 0.101.0 installed`、`Jarvis Lite 0.101.0 installation finished`；`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.101.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，输出包含 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，显式进程检查输出 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 490 checked across 194 tracked/untracked files`；严格密钥形态扫描无命中；更新清单旧夹具和公开旧版本扫描无命中；`config/llm.local.json` 与 `config/search.local.json` 当前不存在；`word/inner-brain-evaluation-report.md` 当前不存在；README BOM 保留。

## 2026-06-03 0.102.0 InnerBrain README 已处理空视图概要同步

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_readme_inner_brain_summary_mentions_empty_resolved_guidance tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory -v` 先失败；README 顶部概要缺少 `暂无已处理样本时会提示这里只显示已通过样本`，版本仍为 `0.101.0`。
- GREEN：同一目标命令 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，308 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，570 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.102.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：`windows-installer-stage\install.cmd` 包含 `DisplayVersion /d "0.102.0"` 和 `Jarvis Lite 0.102.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.102.0 installation finished`；`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.102.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，输出包含 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`；即时进程检查短暂显示 `RunningJarvisAfterSmoke=1`，延迟 3 秒复查为 `RunningJarvisAfterDelay=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 492 checked across 195 tracked/untracked files`；严格密钥形态扫描无命中；当前范围旧版本扫描无命中，v105 历史方案中的旧更新清单夹具描述保留为历史记录；README BOM 为 `EF-BB-BF`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在；`word/inner-brain-evaluation-report.md` 当前不存在。

## 2026-06-03 0.103.0 InnerBrain PROJECT-PLAN 已处理空视图主干同步

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata.ProjectMetadataTests.test_project_plan_inner_brain_summary_mentions_empty_resolved_guidance tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version tests.test_agent.AgentTests.test_update_status_command_reports_available_update_from_manifest tests.test_agent.AgentTests.test_update_download_command_downloads_package_to_runtime_directory -v` 先失败；PROJECT-PLAN 主干概要缺少 `暂无已处理样本时会提示这里只显示已通过样本`，版本仍为 `0.102.0`。
- GREEN：同一目标命令 4 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_project_metadata -v`，309 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，571 项 OK。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.103.0.exe`，大小 `57,135,104` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.103.0"`、`Jarvis Lite 0.103.0 installed`、`Jarvis Lite 0.103.0 installation finished`；`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.103.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，输出包含 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`；延迟 3 秒复查输出 `JarvisLite process count: 0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 494 checked across 196 tracked/untracked files`；严格密钥形态扫描无命中；当前范围旧版本扫描无命中；README BOM 为 `EF-BB-BF`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在；`word/inner-brain-evaluation-report.md` 当前不存在。

## 2026-06-03 0.108.0 截图 OCR 串联第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_screen_capture.ScreenCaptureTests.test_describe_screen_ocr_captures_then_recognizes_saved_image tests.test_agent.AgentTests.test_screen_ocr_command_captures_then_recognizes_current_screen tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；缺少 `describe_screen_ocr`，Agent 未接入 `describe_screen_ocr`，版本仍为 `0.107.0`。
- GREEN：同一目标命令 3 项 OK。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_agent tests.test_screen_capture tests.test_ocr tests.test_window_state tests.test_app_registry tests.test_project_metadata -v`，330 项 OK。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，592 项 OK。
- 命令行截图 OCR smoke：`.\.venv\Scripts\python.exe src\app.py --once "/screen-ocr smoke-0.108.0 lang=eng"` 输出 `截图 OCR：logs/screenshots/smoke-0.108.0.png`、`尺寸：1920x1080` 和 Tesseract CLI 不可用诊断；截图大小 `195,407` 字节，验证后已删除。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅出现既有可选 `Hidden import "tzdata" not found!` 警告。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.108.0.exe`，大小 `57,155,584` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.108.0"`、`Jarvis Lite 0.108.0 installed`、`Jarvis Lite 0.108.0 installation finished`；`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.108.0`。
- 打包后 exe smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 `0`，输出包含 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`；延迟 3 秒复查输出 `JarvisLite process count: 0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 372 checked across 201 tracked/untracked files`；严格密钥形态扫描无命中；README BOM 为 `EF-BB-BF`；`config/llm.local.json` 与 `config/search.local.json` 当前不存在；`word/inner-brain-evaluation-report.md` 当前不存在。
- 审查降级：`superpowers:requesting-code-review` 要求派发 reviewer 子代理，但当前多代理工具声明只有用户显式要求代理/委派时才能 spawn；本轮未派发子代理，改做本地自审并记录到 `.codex/review-report.md`。
- 调试留痕：首次将 `JarvisLite.version.txt` 误按单行版本文件检查导致失败；根因确认该文件是 PyInstaller 版本资源脚本，改按既有验证口径检查 `FileVersion` 与 `ProductVersion` 后通过。

## 2026-06-03 0.109.0 快捷键自动化第一阶段

- 目标测试：`.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_parse_hotkey_sequence_normalizes_multiple_combinations tests.test_automation.AutomationTests.test_parse_hotkey_sequence_rejects_empty_or_incomplete_combinations tests.test_automation.AutomationTests.test_describe_hotkey_automation_invokes_executor_with_each_combination tests.test_agent.AgentTests.test_hotkey_command_sends_explicit_keyboard_shortcut tests.test_agent.AgentTests.test_hotkey_command_requires_explicit_shortcut tests.test_agent.AgentTests.test_hotkey_command_reports_execution_failure tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，7 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_automation tests.test_agent tests.test_project_metadata -v`，331 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，598 项通过。
- 命令行 smoke：`.\.venv\Scripts\python.exe src\app.py --once "/automation-status"` 输出当前能力包含 `/hotkey`；真实 `/hotkey` smoke 因会向当前焦点窗口发送键盘事件跳过。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅有既有可选 `tzdata` hidden import 警告和 `pyautogui` 依赖侧无阻塞 SyntaxWarning。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.109.0.exe`，大小 `60,383,232` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.109.0"`、`Jarvis Lite 0.109.0 installed`、`Jarvis Lite 0.109.0 installation finished`；`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.109.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，输出包含 `Jarvis Lite` 与 `desktopPetWindow`；延迟 3 秒复查 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 376 checked across 202 tracked/untracked files`；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.110.0 鼠标点击自动化第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_parse_mouse_click_request_defaults_left_button tests.test_automation.AutomationTests.test_parse_mouse_click_request_accepts_explicit_button_and_negative_coordinates tests.test_automation.AutomationTests.test_parse_mouse_click_request_rejects_incomplete_coordinates_or_unknown_button tests.test_automation.AutomationTests.test_describe_mouse_click_automation_invokes_executor_with_coordinates tests.test_agent.AgentTests.test_mouse_click_command_executes_explicit_coordinate_click tests.test_agent.AgentTests.test_mouse_click_command_requires_coordinates tests.test_agent.AgentTests.test_mouse_click_command_reports_execution_failure tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；缺少 `describe_mouse_click_automation`、Agent patch 目标不存在，版本仍为 `0.109.0`。
- 目标 GREEN：同一目标命令 8 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_automation tests.test_agent tests.test_project_metadata -v`，338 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，605 项通过。
- 命令行 smoke：`.\.venv\Scripts\python.exe src\app.py --once "/automation-status"` 输出当前能力包含 `/mouse-click`；真实 `/mouse-click` smoke 因会向当前桌面发送鼠标事件跳过。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅有既有可选 `tzdata` hidden import 警告和 `pyautogui` 依赖侧无阻塞 SyntaxWarning。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.110.0.exe`，大小 `60,383,232` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.110.0"`、`Jarvis Lite 0.110.0 installed`、`Jarvis Lite 0.110.0 installation finished`；`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.110.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，输出包含 `Jarvis Lite` 与 `desktopPetWindow`；延迟 3 秒复查 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 379 checked across 203 tracked/untracked files`；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.115.0 自动记忆与配置管家第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_memory_config_manager tests.test_agent.AgentTests.test_config_manager_status_command_reports_memory_and_config_without_secrets tests.test_agent.AgentTests.test_status_command_reports_current_capabilities tests.test_agent.AgentTests.test_help_command_lists_llm_usage_command tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；缺少 `jarvis_lite.memory_config_manager`，Agent 未接入 `/config-manager-status`，版本仍为 `0.114.0`。
- 目标 GREEN：同一目标命令 6 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_memory_config_manager tests.test_agent tests.test_project_metadata tests.test_llm tests.test_search tests.test_app_registry tests.test_automation -v`，406 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，639 项通过。
- 命令行 smoke：`/config-manager-status` 与 `/memory-config-status` 输出记忆与配置管家状态，包含 API key 脱敏说明。
- 源码桌面 smoke：输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 打包：`JarvisLiteSetup-0.115.0.exe` 生成，大小 `60,399,616` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.115.0`。
- 打包后 smoke：退出码 0，输出包含 `desktopPetWindow`，延迟复查 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 549 项通过；严格真实密钥形态扫描 19 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.111.0 文本输入自动化第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_parse_text_input_request_preserves_explicit_text tests.test_automation.AutomationTests.test_parse_text_input_request_rejects_empty_text tests.test_automation.AutomationTests.test_describe_text_input_automation_invokes_executor_without_real_typing tests.test_agent.AgentTests.test_type_text_command_inputs_explicit_text tests.test_agent.AgentTests.test_type_text_command_requires_text tests.test_agent.AgentTests.test_type_text_command_reports_execution_failure tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；缺少 `describe_text_input_automation`、Agent patch 目标不存在，版本仍为 `0.110.0`。
- 目标 GREEN：同一目标命令 7 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_automation tests.test_agent tests.test_project_metadata -v`，344 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，611 项通过。
- 命令行 smoke：`.\.venv\Scripts\python.exe src\app.py --once "/automation-status"` 输出当前能力包含 `/type-text`；真实 `/type-text` smoke 因会向当前焦点输入文本并改写剪贴板跳过。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`；PyInstaller 仅有既有可选 `tzdata` hidden import 警告和 `pyautogui` 依赖侧无阻塞 SyntaxWarning。
- 版本化安装包：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.111.0.exe`，大小 `60,387,328` 字节。
- 安装脚本、SED 与版本资源：包含 `DisplayVersion /d "0.111.0"`、`Jarvis Lite 0.111.0 installed`、`Jarvis Lite 0.111.0 installation finished`；`JarvisLite.version.txt` 与 `JarvisLite.exe` 的 `FileVersion` 与 `ProductVersion` 均为 `0.111.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，输出包含 `Jarvis Lite` 与 `desktopPetWindow`；延迟 3 秒复查 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查输出 `Markdown local links OK: 533 checked across markdown files`；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。
## 2026-06-03 0.112.0 窗口切换自动化第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_window_state tests.test_agent.AgentTests.test_window_focus_command_switches_explicit_target tests.test_agent.AgentTests.test_window_focus_command_requires_target tests.test_agent.AgentTests.test_window_focus_command_reports_execution_failure tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为缺少窗口切换 API、Agent 未接入 `describe_window_focus`、项目版本仍为 `0.111.0`。
- GREEN：同一目标命令 11 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_window_state tests.test_agent tests.test_project_metadata -v`，336 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，618 项通过。
- Smoke：`.\.venv\Scripts\python.exe src\app.py --once "/automation-status"` 输出当前能力包含 `/window-focus`；`.\.venv\Scripts\python.exe src\app.py --once "/windows"` 输出窗口感知状态和 11 个可见窗口；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；真实 `/window-focus` smoke 因会改变前台窗口跳过。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.112.0.exe`，大小 `60,387,328` 字节；安装脚本、SED、版本资源和打包后 smoke 均为 `0.112.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接复跑通过，`537` 项；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.113.0 应用启动自动化第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_app_registry tests.test_agent.AgentTests.test_app_launch_command_launches_registered_app tests.test_agent.AgentTests.test_app_launch_command_requires_query tests.test_agent.AgentTests.test_app_launch_command_reports_failure tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；缺少 `describe_app_launch`、`launch_registered_app`、Agent patch 目标不存在，版本仍为 `0.112.0`。
- GREEN：同一目标扩展到 `/apps`、`/app-find` 相邻断言后 13 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_app_registry tests.test_agent tests.test_project_metadata -v`，339 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，625 项通过。
- 命令行 smoke：`/automation-status` 输出当前能力包含 `/app-launch`；`/apps` 输出应用注册表，当前机器识别 Chrome 路径；真实 `/app-launch` smoke 因会启动本机应用跳过。
- 源码桌面 smoke：输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 打包：`JarvisLiteSetup-0.113.0.exe` 生成，大小 `60,387,328` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源为 `0.113.0`。
- 打包后 smoke：退出码 0，输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`；延迟复查 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 541 项通过；严格密钥形态扫描 18 个公开变更文件无命中；本地敏感配置不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.116.0 Chrome 低风险工作流第一阶段

- RED：Chrome 工作流目标命令 19 项先失败，符合预期。
- GREEN：同一目标命令 26 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_chrome_workflow tests.test_agent tests.test_authorization tests.test_project_metadata tests.test_llm tests.test_app_registry tests.test_automation -v`，417 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，653 项通过。
- Smoke：`.\.venv\Scripts\python.exe src\app.py --once "/chrome-workflow-status"` 输出 Chrome 工作流状态；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `desktopPetWindow`；真实 `/chrome-open` 与 `/chrome-search` 跳过。
- 打包：`JarvisLiteSetup-0.116.0.exe` 生成，大小 `60,403,712` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.116.0`；打包后 exe smoke 退出码 0 且无残留进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 552 项通过；严格真实密钥形态扫描 22 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.117.0 Clash Verge 低风险工作流第一阶段

- RED：Clash Verge 工作流目标命令 20 项先失败，符合预期。
- GREEN：同一目标命令 25 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_clash_workflow tests.test_agent tests.test_authorization tests.test_project_metadata tests.test_llm tests.test_app_registry tests.test_window_state tests.test_automation -v`，429 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，666 项通过。
- Smoke：`.\.venv\Scripts\python.exe src\app.py --once "/clash-workflow-status"` 输出 Clash Verge 工作流状态；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `desktopPetWindow`；真实 `/clash-open` 与 `/clash-focus` 跳过。
- 打包：`JarvisLiteSetup-0.117.0.exe` 生成，大小 `60,403,712` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.117.0`；打包后 exe smoke 退出码 0 且无残留进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 554 项通过；严格真实密钥形态扫描 22 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.118.0 QQ/微信准备式工作流第一阶段

- RED：QQ/微信准备式工作流目标命令先失败，符合预期；失败点包括缺少 `jarvis_lite.messaging_workflow`、Agent 未接入命令、授权层和 LLM 白名单未同步，版本仍为 `0.117.0`。
- GREEN：目标命令 29 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_messaging_workflow tests.test_agent tests.test_authorization tests.test_project_metadata tests.test_llm tests.test_app_registry tests.test_window_state tests.test_automation -v`，440 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，683 项通过。
- Smoke：`.\.venv\Scripts\python.exe src\app.py --once "/messaging-workflow-status"` 输出 QQ/微信准备式工作流状态；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `desktopPetWindow`；真实 QQ/微信打开和聚焦命令因会启动或切换本机应用跳过。
- 打包：`JarvisLiteSetup-0.118.0.exe` 生成，大小 `60,411,904` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.118.0`；打包后 exe smoke 退出码 0，stdout 包含 `desktopPetWindow`，无残留 `JarvisLite.exe` 进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 652 项通过；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.119.0 IDEA 项目状态第一阶段

- RED：IDEA 工作流目标命令先失败，符合预期；失败点包括缺少 `jarvis_lite.idea_workflow`、Agent 未接入命令、授权层和 LLM 白名单未同步，版本仍为 `0.118.0`。
- GREEN：目标命令 24 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_idea_workflow tests.test_agent tests.test_authorization tests.test_project_metadata tests.test_llm tests.test_app_registry tests.test_window_state tests.test_automation -v`，451 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，702 项通过。
- Smoke：`.\.venv\Scripts\python.exe src\app.py --once "/idea-workflow-status"` 输出 IDEA 工作流状态；`.\.venv\Scripts\python.exe src\app.py --once "/idea-project-status"` 只读识别当前仓库 `.idea`、`.git` 与 `pyproject.toml`；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `desktopPetWindow`；真实 IDEA 打开、聚焦和打开项目命令因会启动或切换本机应用跳过。
- 打包：`JarvisLiteSetup-0.119.0.exe` 生成，大小 `60,416,000` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.119.0`；打包后 exe smoke 退出码 0，stdout 包含 `desktopPetWindow`，无残留 `JarvisLite.exe` 进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接检查改用 `git ls-files -z` 复跑通过，559 项通过；严格真实密钥形态扫描排除测试假值前缀后无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.120.0 任务状态与失败复盘第一阶段

- RED：任务状态目标命令先失败，符合预期；失败点包括缺少 `jarvis_lite.task_state`、Agent 未接入任务命令，版本仍为 `0.119.0`。
- 目标 GREEN：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state tests.test_agent.AgentTests.test_task_status_command_reports_empty_state tests.test_agent.AgentTests.test_task_commands_record_failure_and_restore_on_startup tests.test_agent.AgentTests.test_task_resume_complete_and_cancel_commands tests.test_agent.AgentTests.test_task_commands_require_arguments_and_are_listed tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，9 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state tests.test_agent tests.test_project_metadata tests.test_llm tests.test_automation -v`，425 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，710 项通过。
- 命令行 smoke：`/task-status` 输出空任务状态和 `/task-start 任务名称` 入口；当前仓库 `/task-start 发布 0.120.0` 后 `/task-cancel` 可清理当前任务；临时项目 start/step/fail/status smoke 验证失败复盘可持久化。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 打包：`JarvisLiteSetup-0.120.0.exe` 生成，大小 `60,424,192` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.120.0`。
- 打包后 smoke：`JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，`RunningJarvisAfterSmoke=0`；中文 stdout 在重定向下出现编码显示问题，不影响 smoke 结论。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 562 项通过；严格密钥形态扫描 15 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.121.0 任务失败截图 OCR 复盘第一阶段

- RED：`0.121.0` 任务失败截图 OCR 复盘核心、Agent `/task-fail-capture`、帮助、状态、LLM 白名单边界和版本一致性测试先失败；失败点为缺少 `record_task_failure_with_screen_ocr`、Agent 未接入 `/task-fail-capture`、项目元数据仍为 `0.120.0`。
- GREEN：`0.121.0` 目标命令 9 项通过，覆盖截图/OCR 成功写入、OCR 不可用诊断写入、Agent 命令参数、帮助、状态、LLM 白名单和版本一致性。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state tests.test_agent tests.test_project_metadata tests.test_llm tests.test_screen_capture tests.test_ocr tests.test_automation -v`，435 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，713 项通过。
- 命令行 smoke：`.\.venv\Scripts\python.exe src\app.py --once "/task-status"` 输出空任务状态和 `/task-start 任务名称` 入口；真实 `/task-fail-capture` smoke 因会保存当前屏幕截图跳过，改用截图和 OCR 注入单元测试覆盖采集契约。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.121.0.exe`，大小 `60,424,192` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.121.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，`RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 565 项通过；严格密钥形态扫描 12 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.122.0 记忆与配置候选池第一阶段

- RED：目标测试先失败；失败点为缺少 `jarvis_lite.memory_config_candidates`、Agent 未接入 `/config-candidate-add` 等候选池命令，版本仍为 `0.121.0`。
- GREEN：`.\.venv\Scripts\python.exe -m unittest tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent.AgentTests.test_config_candidate_commands_record_restore_and_dismiss_candidates tests.test_agent.AgentTests.test_config_candidate_commands_require_arguments_and_are_listed tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，9 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，411 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，718 项通过。
- 命令行 smoke：`.\.venv\Scripts\python.exe src\app.py --once "/config-candidates"` 输出空候选池和候选添加/忽略入口；`.\.venv\Scripts\python.exe src\app.py --once "/config-manager-status"` 输出候选统计和 `/config-candidates` 入口。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.122.0.exe`，大小 `60,432,384` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.122.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0；GUI exe 未回传 stdout，延迟复查无残留 `JarvisLite*` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 569 项通过；严格真实密钥形态扫描 16 个公开变更文件无命中；本地敏感配置文件不存在。

## 0.123.0 记忆与配置候选固化第一阶段

- RED：目标测试先失败，缺少 `apply_memory_config_candidate`、Agent 未接入 `/config-candidate-apply`，版本仍为 `0.122.0`；候选列表固化入口提示断言也先失败。
- GREEN：目标测试 11 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，417 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，724 项通过。
- 命令 smoke：临时项目内 `/config-candidate-apply` 可固化 memory、experience、directory 候选；contact_alias 返回暂不支持并保持活跃。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.123.0.exe`，大小 `60,436,480` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.123.0`。
- 打包后 smoke：`Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，复查无残留 `JarvisLite*` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 415 项通过；严格真实密钥形态扫描 15 个公开变更文件无命中；本地敏感配置文件不存在。

## 0.124.0 任务状态自动采集第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state.TaskStateTests.test_task_route_events_persist_and_feed_failure_replay tests.test_agent.AgentTests.test_task_failure_replay_includes_auto_captured_command_context tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为缺少 `record_task_route_event`、失败复盘缺少“自动采集上下文”、版本仍为 `0.123.0`。
- GREEN：同一目标集 3 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state tests.test_agent tests.test_llm tests.test_project_metadata -v`，417 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，726 项通过。
- 临时项目命令 smoke：`/task-start` 后执行 `/dir-add`，再执行 `/task-fail` 和 `/task-status`；失败复盘与状态均展示 `command / /dir-add` 自动采集上下文。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.124.0.exe`，大小 `60,436,480` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.124.0`。
- 打包后 smoke：`Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，复查无残留 `JarvisLite*` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 419 项通过；严格真实密钥形态扫描排除测试假值前缀后 17 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.125.0 任务执行结果摘要采集第一阶段

- RED：目标测试先失败，缺少 `record_task_event_result`，失败复盘仍显示 `结果：显式命令`，版本仍为 `0.124.0`。
- GREEN：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state.TaskStateTests.test_task_route_event_result_updates_latest_matching_event tests.test_agent.AgentTests.test_task_failure_replay_includes_auto_captured_command_context tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，3 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state tests.test_agent tests.test_llm tests.test_project_metadata -v`，418 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，727 项通过。
- 临时项目命令 smoke：`/task-start` 后执行 `/dir-add`，再执行 `/task-fail` 和 `/task-status`；失败复盘和状态均展示 `结果：已登记常用目录：工作区 ->`，`/task-fail` 自身不进入自动采集段。首次 smoke 断言误用 `/task-fail` 标题检查 `/task-status`，修正断言后复跑通过。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.125.0.exe`，大小 `60,436,480` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.125.0`。
- 打包后 smoke：`Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，复查无残留 `JarvisLite*` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 583 项通过；严格真实密钥形态扫描 17 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.126.0 任务失败复盘行动建议第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state.TaskStateTests.test_task_step_failure_and_status_persist_to_runtime_context tests.test_task_state.TaskStateTests.test_task_failure_with_screen_ocr_records_capture_context tests.test_agent.AgentTests.test_task_commands_record_failure_and_restore_on_startup tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；普通失败复盘和任务状态缺少 `/task-fail-capture 失败原因` 补充截图/OCR 建议，版本仍为 `0.125.0`。
- GREEN：同一目标命令 4 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state tests.test_agent tests.test_llm tests.test_project_metadata -v`，418 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，727 项通过；当前会话复跑结果为 `Ran 727 tests in 18.140s`，`OK`。
- 临时项目 smoke：普通 `/task-fail 验证失败` 响应和 `/task-status` 最近失败记录均提示 `补充截图/OCR：/task-fail-capture 验证失败`；截图/OCR 分支使用 fake capturer 与 fake OCR 调用 `record_task_failure_with_screen_ocr()`，最新失败记录不重复包含 `/task-fail-capture` 建议。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.126.0.exe`，大小 `60,436,480` 字节；版本资源均为 `0.126.0`。
- 打包后 smoke：`Start-Process E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stderr 为空，无残留 `JarvisLite*` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 588 项通过；严格真实密钥形态扫描 16 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.127.0 任务失败复盘样本建议第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state.TaskStateTests.test_task_step_failure_and_status_persist_to_runtime_context tests.test_task_state.TaskStateTests.test_task_route_events_persist_and_feed_failure_replay tests.test_task_state.TaskStateTests.test_task_route_event_result_updates_latest_matching_event tests.test_agent.AgentTests.test_task_failure_replay_includes_auto_captured_command_context tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为显式命令事件失败复盘缺少 `/inner-brain-eval-add 原始输入 => /命令` 样本建议，版本仍为 `0.126.0`。
- GREEN：同一目标命令 5 项通过；临时项目 smoke 发现 `/task-status` 缺少样本建议边界后，补充 `test_task_route_events_persist_and_feed_failure_replay` RED 断言并复跑单测确认失败，再复用样本建议行 helper 修复。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state tests.test_agent tests.test_llm tests.test_project_metadata -v`，418 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，727 项通过。
- 临时项目 smoke：`/task-start` 后执行 `/dir-add`，再执行 `/task-fail` 和 `/task-status`；失败复盘和状态均包含 `样本建议：/inner-brain-eval-add /dir-add 工作区 ... => /dir-add` 与“不自动写入 evaluation、不训练”边界，未生成 evaluation/training runtime 样本。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.127.0.exe`，大小 `60,440,576` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.127.0`。
- 打包后 smoke：`Start-Process E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stderr 为空，无残留 `JarvisLite*` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 593 项通过；严格真实密钥形态扫描 16 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.128.0 记忆与配置候选恢复第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_memory_config_candidates tests.test_agent.AgentTests.test_config_candidate_restore_command_reactivates_history_candidates tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为缺少 `describe_memory_config_candidate_history` 和 `restore_memory_config_candidate`、Agent 未接入 `/config-candidate-history`、版本仍为 `0.127.0`。
- GREEN：同一目标命令 11 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，421 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，730 项通过。
- 临时项目 smoke：`/config-candidate-history` 可查看已忽略和已固化候选，`/config-candidate-restore 1` 可恢复为活跃候选；恢复已固化 memory/directory 后，`memory/profile.md` 和常用目录仍保留，未生成 `llm.local.json`、`search.local.json`、`apps.local.json` 或 `authorization.local.json`。首次 smoke 断言误把 `CommonDirectory.path` 当字符串比较，修正为 `Path(...)` 后复跑通过。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.128.0.exe`，大小 `60,440,576` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.128.0`。
- 打包后 smoke：`Start-Process E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stderr 为空，无残留 `JarvisLite*` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 598 项通过；严格真实密钥形态扫描 18 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.129.0 高风险记忆与配置候选确认草稿第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_memory_config_candidates tests.test_agent.AgentTests.test_config_candidate_apply_command_keeps_unsupported_candidate_active tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为高风险候选仍输出旧“暂不支持”文案，版本仍为 `0.128.0`。
- GREEN：同一目标命令 12 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，422 项通过。首次因更新 manifest 测试夹具仍为 `0.128.1` 失败，提升到 `0.129.1` 后复跑通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，731 项通过。
- 临时项目 smoke：联系人别名、授权规则、应用别名和偏好候选执行 `/config-candidate-apply 编号` 均输出确认草稿、撤销入口和不写入长期配置边界；`/config-candidates` 仍保留 4 条 active 候选，未生成联系人、授权、应用别名、偏好、LLM 或 search 本地配置文件。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.129.0.exe`，大小 `60,440,576` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.129.0`。
- 打包后 smoke：`Start-Process E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stderr 为空，无残留 `JarvisLite*` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 603 项通过；严格真实密钥形态扫描 16 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.130.0 任务失败复盘窗口与授权摘要第一阶段

- RED：目标命令先失败，失败点为缺少 `describe_task_window_context()`、`record_task_failure()` 尚不接收 `window_context`、Agent 尚未传递窗口上下文、版本仍为 `0.129.0`。
- GREEN：`.\.venv\Scripts\python.exe -m unittest tests.test_window_state.WindowStateTests.test_describe_task_window_context_returns_compact_foreground_summary tests.test_task_state.TaskStateTests.test_task_failure_records_window_route_and_authorization_context tests.test_agent.AgentTests.test_task_fail_command_records_window_context_in_replay tests.test_agent.AgentTests.test_task_fail_capture_command_records_screen_ocr_context tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 通过；当前会话复验 `Ran 5 tests in 0.203s`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_task_state tests.test_agent tests.test_window_state tests.test_llm tests.test_project_metadata -v`，429 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，734 项通过。
- 命令行 smoke：临时项目内 `/task-start`、`/task-fail`、`/task-status` 均通过；失败复盘和状态页展示窗口、路由和授权上下文，运行态 `window_context` 以 `当前窗口：` 开头。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.130.0.exe`，大小 `60,440,576` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.130.0`。
- 打包后 smoke：`Start-Process E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无新增残留 `JarvisLite` 进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 612 项通过；严格真实密钥形态扫描 20 个公开变更/新增文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.131.0 联系人别名确认固化与撤销第一阶段

- RED：目标命令先失败，失败点为缺少 `jarvis_lite.contacts`、Agent 未接入 `/config-candidate-confirm` 和 `/config-candidate-undo`、确认草稿缺少确认固化入口、版本仍为 `0.130.0`。
- GREEN：`.\.venv\Scripts\python.exe -m unittest tests.test_contacts tests.test_memory_config_candidates.MemoryConfigCandidateTests.test_confirm_contact_alias_candidate_persists_and_undo_removes_alias tests.test_memory_config_candidates.MemoryConfigCandidateTests.test_confirm_only_supports_contact_alias_in_first_stage tests.test_memory_config_candidates.MemoryConfigCandidateTests.test_apply_high_risk_candidates_returns_confirmation_draft_without_writing_config tests.test_memory_config_manager.MemoryConfigManagerTests.test_describe_memory_config_manager_reports_empty_storage tests.test_memory_config_manager.MemoryConfigManagerTests.test_describe_memory_config_manager_masks_provider_api_keys tests.test_agent.AgentTests.test_config_candidate_commands_require_arguments_and_are_listed tests.test_agent.AgentTests.test_config_candidate_apply_command_keeps_unsupported_candidate_active tests.test_agent.AgentTests.test_config_candidate_confirm_and_undo_contact_alias tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 通过；复验 `Ran 12 tests in 0.429s`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_contacts tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，428 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，739 项通过。
- 临时项目 smoke：联系人别名候选可先生成确认草稿，再确认写入 `contacts.local.json`、历史展示、撤销删除并恢复活跃候选。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.131.0.exe`，大小 `60,448,768` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.131.0`。
- 打包后 smoke：`Start-Process -Wait E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 616 项通过；严格真实密钥形态扫描 21 个公开变更/新增文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.132.0 应用别名确认固化与撤销第一阶段

- RED：目标命令先失败，失败点为缺少应用别名解析/写入/删除 helper、候选确认暂不支持 `app_alias`、Agent 尚未接入应用别名确认/撤销、版本仍为 `0.131.0`。
- GREEN：`.\.venv\Scripts\python.exe -m unittest tests.test_app_registry.AppRegistryTests.test_app_alias_store_writes_matches_and_removes_alias_without_deleting_path tests.test_app_registry.AppRegistryTests.test_app_alias_candidate_requires_alias_and_registered_app_query tests.test_memory_config_candidates.MemoryConfigCandidateTests.test_confirm_app_alias_candidate_persists_and_undo_removes_alias tests.test_memory_config_candidates.MemoryConfigCandidateTests.test_confirm_supports_only_confirmed_high_risk_candidate_types tests.test_agent.AgentTests.test_config_candidate_confirm_and_undo_app_alias tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 通过；复验 `Ran 6 tests in 0.349s`，`OK`。
- 调试复验：临时 smoke 暴露应用本地配置读取变量遮蔽后，修复 `_read_local_registry_payload()` 并复跑 `tests.test_app_registry.AppRegistryTests.test_app_alias_store_writes_matches_and_removes_alias_without_deleting_path -v`，1 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_app_registry tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，437 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，743 项通过。
- 临时项目 smoke：应用别名候选可先生成确认草稿，再确认写入 `apps.local.json`，`/app-find 晨会入口` 命中 Chrome，撤销删除别名并恢复活跃候选。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：最终源码变更后重跑 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 时，工具包装在 IExpress 阶段超时；等待后台 `iexpress`/`makecab` 完成后，版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.132.0.exe` 已刷新，大小 `60,448,768` 字节，时间戳 `2026/6/4 14:11:28`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.132.0`。
- 打包后 smoke：`Start-Process -Wait E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 620 项通过；严格真实密钥形态扫描 19 个公开变更/新增文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.133.0 授权规则确认固化与撤销第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_authorization tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent.AgentTests.test_config_candidate_confirm_and_undo_authorization_rule tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为缺少 `jarvis_lite.authorization_rules`、候选确认暂不支持 `authorization_rule`、Agent 仍返回暂不支持、版本仍为 `0.132.0`。
- GREEN：同一目标命令 27 项通过；复验结果为 `Ran 27 tests in 0.897s`，`OK`。
- 追加 RED/GREEN：配置管家授权规则管理入口先断言失败，再新增 `/authorization-status` 管理入口后目标断言通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_authorization tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，440 项通过。首次因更新 manifest 夹具仍为 `0.132.1` 失败，提升到 `0.133.1` 后复跑通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，当前会话复验 `Ran 746 tests in 20.672s`，`OK`。
- 命令行 smoke：临时项目内执行 `/config-candidate-add authorization_rule 微信发消息前需要确认`、`/config-candidate-confirm 1`、`/authorization-status`、`/config-manager-status`、`/config-candidate-history`、`/config-candidate-undo 1`、`/config-candidates`；确认写入 `authorization.local.json`，撤销后文件内容为 `{"rules":[]}`，候选恢复活跃；复验输出 `authorization-rule-smoke OK`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.133.0.exe`，大小 `60,452,864` 字节，时间戳 `2026/6/5 10:26:50`。
- 安装包元数据：`install.cmd` 包含 `DisplayVersion /d "0.133.0"` 和 `Jarvis Lite 0.133.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.133.0 installation finished`；`JarvisLite.version.txt` 的 `filevers/prodvers` 为 `(0, 133, 0, 0)`；`desktop-exe\JarvisLite.exe` 的 `FileVersion/ProductVersion` 均为 `0.133.0`。
- 打包后 smoke：`Start-Process -Wait E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 630 项通过；严格真实密钥形态扫描 23 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.134.0 偏好确认固化与撤销第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent.AgentTests.test_config_candidate_confirm_and_undo_preference tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为缺少 `jarvis_lite.preferences`、候选确认暂不支持 `preference`、版本仍为 `0.133.0`。
- GREEN：同一目标命令 20 项通过；复验结果为 `Ran 20 tests in 0.983s`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，434 项通过。首次因更新 manifest 夹具仍为 `0.133.1` 失败，提升到 `0.134.1` 后复跑通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，提交前复验 `Ran 750 tests in 23.472s`，`OK`。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，7 项通过。
- 命令行 smoke：临时项目内执行 `/config-candidate-add preference 回答尽量简洁`、`/config-candidate-confirm 1`、`/config-manager-status`、`/config-candidate-history`、`/config-candidate-undo 1`、`/config-candidates`；确认写入 `preferences.local.json`，配置管家展示 `偏好：1 条`，撤销后文件内容为 `{"preferences":[]}`，候选恢复活跃；复验输出 `preference-smoke OK`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.134.0.exe`，大小 `60,461,056` 字节，时间戳 `2026/6/5 11:46:55`。
- 安装包元数据：`install.cmd` 包含 `DisplayVersion /d "0.134.0"` 和 `Jarvis Lite 0.134.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.134.0 installation finished`；`JarvisLite.version.txt` 的 `filevers/prodvers` 为 `(0, 134, 0, 0)`；`desktop-exe\JarvisLite.exe` 的 `FileVersion/ProductVersion` 均为 `0.134.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 308 项通过；严格真实密钥形态扫描 20 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.135.0 偏好显式启用与停用第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent.AgentTests.test_config_candidate_confirm_and_undo_preference tests.test_agent.AgentTests.test_preference_status_enable_and_disable_commands_manage_saved_preferences tests.test_memory_config_manager tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为缺少 `set_preference_enabled`、`Preference.enabled`、`/preference-status` 命令、配置管家偏好入口和版本仍为 `0.134.0`。
- GREEN：同一目标命令 10 项通过；复验结果为 `Ran 10 tests in 0.491s`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，437 项通过。首次因更新 manifest 夹具仍为 `0.134.1` 失败，提升到 `0.135.1` 后复跑通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，提交前复验 `Ran 753 tests in 21.719s`，`OK`。
- 命令行 smoke：临时项目内执行偏好候选新增、确认、状态查看、启用、停用和配置管家状态；确认偏好默认未启用，启用后 `enabled=true`，停用后 `enabled=false`，配置管家提示 `/preference-status`；复验输出 `preference-enable-smoke OK`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.135.0.exe`，大小 `60,461,056` 字节，时间戳 `2026/6/5 13:02:31`。
- 安装包元数据：`install.cmd` 包含 `DisplayVersion /d "0.135.0"` 和 `Jarvis Lite 0.135.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.135.0 installation finished`；`JarvisLite.version.txt` 的 `filevers/prodvers` 为 `(0, 135, 0, 0)`；`desktop-exe\JarvisLite.exe` 的 `FileVersion/ProductVersion` 均为 `0.135.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，`Ran 7 tests in 0.002s`，`OK`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 494 项通过；严格真实密钥形态扫描 20 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.136.0 偏好应用预览第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent.AgentTests.test_preference_preview_command_reports_enabled_preferences_without_applying tests.test_memory_config_manager tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为缺少 `describe_preference_preview`、`/preference-preview` 命令、配置管家偏好预览入口和版本仍为 `0.135.0`。
- GREEN：同一目标命令 11 项通过；复验结果为 `Ran 11 tests in 0.352s`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，440 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，提交前复验 `Ran 756 tests in 22.471s`，`OK`。
- 命令行 smoke：临时项目内执行偏好候选新增、确认、预览、启用、再次预览、状态和配置管家状态；确认无启用偏好时提示先启用，启用后预览展示输入、已启用偏好和不自动改变回复/LLM/路由/执行决策边界；复验输出 `preference-preview-smoke OK`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.136.0.exe`，大小 `60,465,152` 字节，时间戳 `2026/6/5 14:43:18`。
- 安装包元数据：`install.cmd` 包含 `DisplayVersion /d "0.136.0"` 和 `Jarvis Lite 0.136.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.136.0 installation finished`；`JarvisLite.version.txt` 的 `filevers/prodvers` 为 `(0, 136, 0, 0)`；`desktop-exe\JarvisLite.exe` 的 `FileVersion/ProductVersion` 均为 `0.136.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，`Ran 7 tests in 0.004s`，`OK`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 498 项通过；严格真实密钥形态扫描 20 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.137.0 偏好稳定 ID 与冲突提示第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent.AgentTests.test_config_candidate_confirm_and_undo_preference tests.test_agent.AgentTests.test_preference_status_enable_and_disable_commands_manage_saved_preferences tests.test_agent.AgentTests.test_preference_preview_command_reports_enabled_preferences_without_applying tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v` 先失败；失败点为缺少 `Preference.preference_id`、存储缺少 `id`、命令仍只接受数字编号、状态/预览缺少 ID 与冲突提示、版本仍为 `0.136.0`。
- GREEN：同一目标命令 13 项通过；复验结果为 `Ran 13 tests in 0.589s`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，442 项通过。首次因更新 manifest 测试夹具仍为 `0.136.1` 失败，提升到 `0.137.1` 后复跑通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，当前会话复验 `Ran 758 tests in 21.858s`，`OK`。
- 命令行 smoke：临时项目内执行两个偏好候选新增、确认、按 ID 启用、状态查看、预览和按 ID 停用；确认状态和预览展示 ID，简洁/详细偏好同时启用时展示 `偏好冲突提示` 和 `只提示冲突，不自动裁决优先级`；复验输出 `preference-id-conflict-smoke OK`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.137.0.exe`，大小 `60,465,152` 字节，时间戳 `2026/6/5 16:05:57`。
- 安装包元数据：`install.cmd` 包含 `DisplayVersion /d "0.137.0"` 和 `Jarvis Lite 0.137.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.137.0 installation finished`；`JarvisLite.version.txt` 的 `filevers/prodvers` 为 `(0, 137, 0, 0)`；`desktop-exe\JarvisLite.exe` 的 `FileVersion/ProductVersion` 均为 `0.137.0`。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，`Ran 7 tests in 0.004s`，`OK`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 646 项通过；严格真实密钥形态扫描 15 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.138.0 偏好应用确认草稿第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v` 先失败；失败点为缺少 `describe_preference_application_draft`、Agent `/preference-apply-draft` 返回未知命令、版本仍为 `0.137.0`。
- GREEN：同一目标命令 429 项通过；复验结果为 `Ran 429 tests in 16.953s`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，445 项通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，当前会话复验 `Ran 761 tests in 22.423s`，`OK`。
- 命令行 smoke：临时项目内执行偏好候选新增、确认、无启用草稿、启用、再次生成草稿和配置管家状态；确认草稿展示输入、启用偏好、不真正应用偏好和不改变回复/LLM/路由/执行决策边界；复验输出 `preference-apply-draft-smoke OK`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.138.0.exe`，大小 `60,465,152` 字节，时间戳 `2026/6/5 17:10:33`。
- 安装包元数据：`install.cmd` 包含 `DisplayVersion /d "0.138.0"` 和 `Jarvis Lite 0.138.0 installed`；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.138.0 installation finished`；`JarvisLite.version.txt` 的 `filevers/prodvers` 为 `(0, 138, 0, 0)`；`desktop-exe\JarvisLite.exe` 的 `FileVersion/ProductVersion` 均为 `0.138.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 重定向复验退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，`Ran 7 tests in 0.002s`，`OK`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 650 项通过；严格真实密钥形态扫描 16 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.139.0 偏好应用确认命令第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_memory_config_manager tests.test_llm tests.test_project_metadata -v` 先失败；失败点为缺少 `describe_confirmed_preference_application`、Agent `/preference-apply-confirm` 返回未知命令、配置管家入口缺失、版本仍为 `0.138.0`。
- GREEN：同一目标命令通过；接手后用相邻回归复验 449 项通过。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，`Ran 449 tests in 19.271s`，`OK`。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 765 tests in 24.771s`，`OK`。
- 命令行 smoke：临时项目内执行偏好候选新增、确认、无启用确认、启用、确认、再新增冲突偏好并启用、冲突确认；输出 `preference-apply-confirm smoke OK`，覆盖无启用拒绝、单次确认和冲突拒绝。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.139.0.exe`，大小 `60,469,248` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.139.0`。
- 打包后 smoke：`E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 重定向复验退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 654 项通过；严格真实密钥形态扫描 17 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.140.0 偏好应用确认记录与撤销第一阶段

- RED：目标测试先失败，失败点为缺少偏好应用确认历史 helper、Agent `/preference-apply-history` 和 `/preference-apply-undo` 返回未知命令、版本仍为 `0.139.0`。
- GREEN：目标实现写入运行态 `recent_preference_applications`，新增历史查看和撤销命令；相邻回归 `Ran 453 tests`，`OK`。
- 断线恢复：`日志.txt` 尾部显示上次在命令行 smoke 使用不存在的 `load_preferences` 导入后断线；本轮改用 `save_preference`、`set_preference_enabled`、`read_preferences` 和 Agent 命令复跑。
- 追加 RED：`tests.test_preferences.PreferenceTests.test_confirmed_preference_application_keeps_same_second_duplicate_history` 先失败，固定同一时间戳连续两次相同确认后历史只有 1 条。
- 追加 GREEN：确认 ID 生成在已有历史存在同 ID 时追加序号参与哈希；单测通过，同秒重复确认保留两条不同 `prefapp-...` 记录。
- 目标复验：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v`，`Ran 438 tests`，`OK`。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 770 tests`，`OK`。
- 命令行 smoke：临时项目执行保存偏好、启用偏好、确认、历史、编号撤销、同秒重复确认和按确认 ID 撤销；输出 `preference-apply-audit-smoke OK`，两条同秒确认 ID 为 `prefapp-eef3c515fe` 和 `prefapp-8e505eac4e`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.140.0.exe`，大小 `59,715,584` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.140.0`。
- 打包后 smoke：`E:\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 重定向复验退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 断线恢复最终复验：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 770 tests in 11.525s`，`OK`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 666 项通过；严格真实密钥形态扫描 25 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.141.0 偏好进入普通回复上下文第一阶段

- RED：新增目标测试先失败，失败点为缺少 `describe_preference_reply_context()`、`/llm-context-preview` 不展示有效偏好确认上下文、普通 LLM fallback 未收到偏好确认上下文、版本仍为 `0.140.0`。
- GREEN：实现有效确认记录选择和 Agent `_llm_context_lines()` 接入；目标命令 `.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent.AgentTests.test_llm_context_preview_includes_confirmed_preference_application tests.test_agent.AgentTests.test_llm_fallback_receives_confirmed_preference_context_until_undone tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，`Ran 23 tests`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_memory_config_candidates tests.test_memory_config_manager tests.test_agent tests.test_llm tests.test_project_metadata -v`，`Ran 458 tests in 6.834s`，`OK`。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 774 tests in 8.623s`，`OK`。
- 命令行 smoke：临时项目保存并启用偏好，确认前 preview 无确认上下文，确认后 preview 和普通 LLM fallback context 均包含 `prefapp-...` 与偏好文本，撤销后 preview 和普通 LLM fallback context 均移除确认上下文；输出 `preference-reply-context-smoke OK`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.141.0.exe`，大小 `59,711,488` 字节。
- 安装包元数据：`install.cmd`、`JarvisLiteSetup.sed`、`JarvisLite.version.txt` 和 `desktop-exe\JarvisLite.exe` 均为 `0.141.0`。
- 打包后 smoke：`E:\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 671 项通过；严格真实密钥形态扫描 14 个公开变更/新增文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 0.142.0 偏好格式化本地回答第一阶段

- RED：目标测试先失败；失败点为缺少 `describe_preference_local_answer_note()`、本地知识库 `/ask` 回答不展示 `已确认偏好格式化：prefapp-...`、长期记忆兜底不展示该附注、版本仍为 `0.141.0`。
- GREEN：新增本地回答偏好附注 helper，接入 `_answer_from_data()` 和长期记忆兜底；目标命令 `.\.venv\Scripts\python.exe -m unittest tests.test_preferences.PreferenceTests.test_preference_local_answer_note_requires_enabled_preferences_to_match_confirmation tests.test_agent.AgentTests.test_local_data_answer_includes_confirmed_preference_note_until_undone tests.test_agent.AgentTests.test_memory_fallback_includes_confirmed_preference_note_until_undone tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，`Ran 5 tests`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v`，`Ran 445 tests in 6.577s`，`OK`。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 777 tests in 8.625s`，`OK`。
- 命令行 smoke：临时项目保存并启用偏好，确认前本地知识库和长期记忆兜底无附注，确认后两者展示 `已确认偏好格式化：prefapp-...`，撤销后两者移除附注；输出 `preference-local-answer-format-smoke OK`。首次 smoke 失败根因为脚本误判长期记忆兜底不会先调用 LLM fallback，修正断言后通过。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.142.0.exe`，大小 `59,715,584` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `desktop-exe\JarvisLite.exe` 版本资源均为 `0.142.0`。
- 打包后 smoke：`E:\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，`Ran 7 tests`，`OK`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 674 项通过；严格真实密钥形态扫描 722 个文本文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.143.0 偏好应用撤销提示第一阶段

- RED：目标测试先失败；失败点为确认输出、本地知识库附注和长期记忆兜底附注未展示按确认 ID 撤销的精确命令，普通 LLM fallback context 有泄漏风险，版本仍为 `0.142.0`。
- GREEN：新增内部格式化 helper，并接入确认输出、本地知识库命中回答附注和长期记忆兜底附注；目标命令 `.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v`，`Ran 11 tests`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v` 之后再跑相关回归，`Ran 445 tests`，`OK`。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 777 tests`，`OK`。
- 命令行 smoke：`preference-undo-hints-smoke OK`，确认输出、本地 `/ask` 附注和长期记忆兜底附注均展示 `撤销确认：/preference-apply-undo prefapp-...`，普通 LLM fallback context 不包含该命令。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；生成基础 `E:\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，并复制版本化安装包 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.143.0.exe`，大小 `59,715,584` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.143.0`。
- 打包后 smoke：`Start-Process -Wait -PassThru -RedirectStandardOutput -RedirectStandardError E:\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 静态检查：`git diff --check` 退出码 0；Markdown 本地链接 677 项通过，覆盖 423 个 Markdown 文件；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 0.144.0 偏好本地回答附注范围第一阶段

- RED：目标测试先失败；失败点为 `describe_preference_local_answer_note(paths, "knowledge")` 旧签名不接受 answer type、本地知识库 `/ask` 输出缺少 `回答类型：本地知识库回答`、长期记忆兜底输出缺少 `回答类型：长期记忆兜底回答`、版本仍为 `0.143.0`。
- GREEN：目标命令 `.\.venv\Scripts\python.exe -m unittest tests.test_preferences.PreferenceTests.test_preference_local_answer_note_requires_enabled_preferences_to_match_confirmation tests.test_preferences.PreferenceTests.test_preference_local_answer_note_uses_answer_type_scope tests.test_agent.AgentTests.test_llm_fallback_receives_confirmed_preference_context_until_undone tests.test_agent.AgentTests.test_local_data_answer_includes_confirmed_preference_note_until_undone tests.test_agent.AgentTests.test_memory_fallback_includes_confirmed_preference_note_until_undone tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，`Ran 6 tests`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v`，`Ran 446 tests in 6.578s`，`OK`；首次因更新 manifest 夹具仍为 `0.143.1` 失败，提升到 `0.144.1` 后复跑通过。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 778 tests in 9.049s`，`OK`。
- 命令行 smoke：`preference-local-answer-scope-smoke OK`，覆盖本地知识库回答类型标签、长期记忆兜底回答类型标签、撤销后失效，以及 LLM context 不泄漏本地回答标签或撤销命令。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；生成基础 `E:\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，并复制版本化安装包 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.144.0.exe`，大小 `59,715,584` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.144.0`。
- 打包后 smoke：`Start-Process -Wait -PassThru -RedirectStandardOutput -RedirectStandardError E:\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 文档收紧后最终复验：全量 `unittest` 重新执行，`Ran 778 tests in 8.882s`，`OK`；`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 675 项通过，覆盖 424 个 Markdown 文件；严格真实 key 形态扫描无命中；本地敏感配置文件不存在；README 108 行，根 `verification.md` 19 行。

## 0.145.0 偏好本地回答类型开关第一阶段

- RED：目标命令先失败；失败点为 `tests/test_preferences.py` 无法导入 `describe_preference_local_answer_type_settings`，Agent `/preference-answer-types` 返回未知命令，停用 knowledge 后 `/ask` 仍展示 `已确认偏好格式化：prefapp-...`，项目版本仍为 `0.144.0`。
- GREEN：目标命令 `.\.venv\Scripts\python.exe -m unittest tests.test_preferences.PreferenceTests.test_preference_local_answer_type_settings_default_to_knowledge_and_memory tests.test_preferences.PreferenceTests.test_preference_local_answer_note_respects_answer_type_settings tests.test_preferences.PreferenceTests.test_preference_local_answer_type_setting_rejects_unknown_without_writing tests.test_agent.AgentTests.test_preference_answer_type_commands_manage_local_answer_note_scope tests.test_agent.AgentTests.test_local_answer_type_disable_hides_only_that_answer_type_note tests.test_llm.LLMTests.test_openai_provider_instructions_list_supported_agent_commands tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version -v`，`Ran 7 tests`，`OK`。
- 相邻回归：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v`，`Ran 451 tests in 7.182s`，`OK`。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 783 tests in 9.632s`，`OK`。
- 命令行 smoke：`preference-local-answer-type-settings-smoke OK`，覆盖默认双开、停用 knowledge、停用 memory、重新启用两类类型和 LLM context 不泄漏本地回答标签或撤销命令。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；生成基础 `E:\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，并复制版本化安装包 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.145.0.exe`，大小 `59,719,680` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.145.0`。
- 打包后 smoke：`E:\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 文档后最终复验：全量 `unittest` 重新执行，`Ran 783 tests`，`OK`；`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 683 项通过；严格真实 key 形态扫描无命中；本地敏感配置文件不存在；README 108 行，根 `verification.md` 21 行。

## 0.146.0 偏好普通回复上下文开关第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v` 先失败；失败点为缺少 `describe_preference_reply_context_settings` / `set_preference_reply_context_enabled`，Agent 返回未知命令，停用普通回复上下文后 `/llm-context-preview` 仍展示 `已确认偏好应用：prefapp-...`，版本仍为 `0.145.0`。
- GREEN：同一目标命令复跑通过，`Ran 455 tests in 7.065s`，`OK`。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 787 tests in 9.338s`，`OK`。
- 命令行 smoke：临时项目内执行 `/preference-reply-context`、偏好候选确认、偏好启用、偏好应用确认、`/llm-context-preview`、本地知识库回答、`/preference-reply-context-disable`、再次预览和本地知识库回答、`/preference-reply-context-enable`；输出 `preference-reply-context-settings-smoke OK`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，stdout 包含 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；生成基础 `E:\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，并复制版本化安装包 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.146.0.exe`，大小 `59,719,680` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.146.0`。
- 打包后 smoke：`E:\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 长度 0，无残留 `JarvisLite` 进程。
- 文档索引补齐后最终复验：全量 `unittest` 重新执行，`Ran 787 tests in 8.766s`，`OK`；`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 689 项通过，覆盖 428 个 tracked/untracked Markdown 文件；严格真实 key 形态扫描无命中；`config/llm.local.json`、`config/search.local.json` 和 `word/inner-brain-evaluation-report.md` 不存在。

## 0.147.0 偏好应用状态解释第一阶段

- RED：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v` 先失败；失败点为缺少 `describe_preference_application_status`、Agent `/preference-apply-status` 返回未知命令、项目版本仍为 `0.146.0`。
- GREEN：同一目标命令复跑通过，`Ran 458 tests in 6.984s`，`OK`。
- 全量回归：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 790 tests in 9.454s`，`OK`。
- 命令行 smoke：临时项目内执行偏好候选确认、启用、偏好应用确认、默认 `/preference-apply-status`、停用普通回复上下文、停用 `knowledge`、按确认 ID 查询和未知引用查询；输出 `preference-application-status-explain-smoke OK`。
- 源码桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 退出码 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 安装包构建：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`。
- 版本化安装包：`E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.147.0.exe` 生成，大小 `59,719,680` 字节，时间戳 `2026/6/10 11:52:58`。
- 安装包元数据：`install.cmd` 包含 `DisplayVersion /d "0.147.0"`；`JarvisLite.version.txt` 的 `filevers/prodvers` 为 `(0, 147, 0, 0)`；`desktop-exe\JarvisLite.exe` 的 `FileVersion/ProductVersion` 均为 `0.147.0`。
- 打包后 smoke：`Start-Process -Wait -PassThru -RedirectStandardOutput -RedirectStandardError E:\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 退出码 0，stdout 包含 `desktopPetWindow`，stderr 为空，无残留 `JarvisLite` 进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 696 项通过，覆盖 429 个 tracked/untracked Markdown 文件；严格真实 key 形态扫描无命中；`config/llm.local.json`、`config/search.local.json` 和 `word/inner-brain-evaluation-report.md` 不存在。
- 文档同步后最终复验：全量 `unittest` 重新执行，`Ran 790 tests in 9.193s`，`OK`；`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 696 项通过，覆盖 429 个 tracked/untracked Markdown 文件；严格真实 key 形态扫描无命中；本地敏感配置文件不存在；README 108 行，根 `verification.md` 23 行。
