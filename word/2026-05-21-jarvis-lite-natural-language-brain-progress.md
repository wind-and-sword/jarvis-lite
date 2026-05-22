# Jarvis Lite 自然语言本地大脑第一版进度

> 日期：2026-05-21
> 执行者：Codex

## 当前目标

把用户安装测试日志中暴露的自然语言问题收口，让常见操作不依赖斜杠命令，并为后续语音入口和大模型外脑接入提供统一文本意图层。

## 已完成

- 新增 `jarvis_lite.intent`：
  - `NaturalLanguageIntent`：表示本地大脑识别出的意图。
  - `parse_natural_language_intent()`：把常见中文表达映射为内部命令或本地动作。
- 自然语言已支持：
  - “你现在能做什么事”
  - “查看知识库”
  - “查看常用目录”
  - “生成日报”
  - “检查更新”
  - “下载更新”
  - “打开D盘”
  - “打开项目目录”
  - “整理项目目录”
  - “打开桌面”
  - “整理桌面”
  - “给 note.txt 打标签 项目 Python”
  - “把 note.txt 标记为 私人资料”
  - “导入 C:\path\note.md 到知识库”
  - “把 C:\path\note.md 导入知识库”
  - 导入单个资料后：“给这个资料打标签 项目 Python”
- 修复身份误写入：
  - `我是你的什么人，你知道吗` 现在会作为身份问题处理。
  - 疑问句不会被 `我是...` 规则写入 `用户身份`。
- `/status` 文案更新为当前完整状态，覆盖命令行、桌面、自然语言、语音、工作台和更新能力。
- `/voice 文本` 会复用同一套 Agent 流程，因此自然语言意图层也能被语音入口复用。
- 常用目录别名可被自然语言复用：先登记 `/dir-add 项目 路径` 后，可说“打开项目目录”或“整理项目目录”。

## 验证结果

- RED 验证：
  - `tests.test_memory` 先因身份关系问句未识别失败。
  - `tests.test_agent` 先因能力询问、日报、知识库、更新和打开 D 盘自然语言都落入通用兜底失败。
- 专项 GREEN 验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v`：46 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：173 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：未发现空白错误，仅出现 CRLF 换行提示。
  - `.venv\Scripts\python.exe scripts\build_windows_installer.py`：成功生成安装器。
  - `Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru`：退出码 `0`。

## 当前交付状态

- 最新安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`
- 文件大小：`47,472,640` 字节
- 生成时间：`2026-05-21 11:17:54`
- 本地代码提交：`d115d24 feat: 增加自然语言本地意图层`

## 追加进度：常用目录别名自然语言

- 新增“打开别名目录”意图，例如“打开项目目录”。
- 新增“整理别名目录”意图，例如“整理项目目录”。
- 两类意图都复用已登记的常用目录，不新增移动或删除文件能力。
- 本地代码提交：`391516d feat: 支持常用目录自然语言别名`
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：39 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：175 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：已知桌面目录自然语言

- 未登记常用目录时，`整理桌面` 会尝试使用系统桌面目录生成文件整理预览。
- 未登记常用目录时，`打开桌面` 会尝试使用系统桌面目录写入打开请求记录。
- 已登记的常用目录仍优先于系统目录 fallback，方便用户覆盖自己的桌面路径。
- 仍然不移动、不删除文件，也不启动外部应用。
- RED 验证：
  - 新增 2 个测试先分别因找不到 `桌面` 常用目录和未写入打开记录失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_desktop_uses_known_desktop_directory tests.test_agent.AgentTests.test_natural_language_open_desktop_uses_known_desktop_directory -v`：2 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：41 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：177 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：资料标签自然语言

- 新增明确文件名的标签表达：
  - “给 note.txt 打标签 项目 Python”
  - “把 note.txt 标记为 私人资料”
- 解析结果直接复用 `/tag 文件名 标签...`，标签仍由知识库模块规范化和持久化。
- 本阶段不做“这个资料”上下文指代，不做模糊文件名搜索。
- RED 验证：
  - 新增 2 个测试先分别落入普通兜底和资料问答，未更新标签。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_mark_document_as_tags_updates_document_tags -v`：2 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：43 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：179 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：自然语言导入资料

- 新增明确路径导入表达：
  - “导入 C:\path\note.md 到知识库”
  - “把 C:\path\note.md 导入知识库”
- 路径带空格时支持加引号，例如 `把 "C:\path with space\note.md" 导入知识库`。
- 解析结果直接复用 `/import 源文件或目录路径`，文件类型、重名和错误提示仍由现有导入逻辑处理。
- 本阶段不做“这个文件”上下文指代，不做拖拽入口或文件选择器。
- RED 验证：
  - 新增 2 个测试先落入普通兜底，未导入资料。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_import_file_adds_document_to_knowledge_base tests.test_agent.AgentTests.test_natural_language_import_quoted_file_path_adds_document_to_knowledge_base -v`：2 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：45 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：181 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近资料上下文

- JarvisAgent 现在会记录最近一次成功导入的单个资料。
- 导入单个资料后，可以说“给这个资料打标签 项目 Python”，会作用到刚导入的 data 文件。
- 没有最近资料时，会提示先导入资料或指定文件名，不再把“这个资料”当成真实文件名。
- 目录批量导入不作为最近单个资料处理，避免“这个资料”指向多个文件。
- RED 验证：
  - 新增 2 个测试先把“这个资料”误当成文件名，未能更新最近导入资料。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_imported_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_tag_recent_document_requires_recent_document_context -v`：2 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：47 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：183 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近目录上下文

- JarvisAgent 现在会记录最近一次成功打开或整理预览的目录。
- 打开常用目录后，可以继续说“整理这个目录”，会作用到刚才的目录。
- 没有最近目录时，“打开这个目录”会提示先打开或整理一个目录，不再把“这个目录”当成普通目录别名。
- 最近目录上下文只保存在当前 Agent 实例内，重启后不恢复。
- RED 验证：
  - 新增 2 个测试先把“这个目录”误当成别名“这个”，未能使用最近目录或提示缺少最近目录。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_recent_directory_after_open_common_directory tests.test_agent.AgentTests.test_natural_language_open_recent_directory_requires_recent_directory_context -v`：2 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：49 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：185 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近搜索结果上下文

- `/ask 问题` 命中资料后，JarvisAgent 会把第一条命中的 data 文件记录为最近资料。
- 普通自然语言问题命中资料后，也会记录第一条命中的 data 文件。
- 现在可以在问答之后说“给这个结果打标签 运行环境”，会作用到刚才命中的资料。
- 本阶段不改变知识库检索排序、得分和回答格式，也不支持“第二条结果”这类编号选择。
- RED 验证：
  - 新增 2 个测试先把“这个结果”误当成真实文件名，未能给最近搜索命中的资料打标签。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_plain_question -v`：2 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge -v`：23 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：51 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：187 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近搜索结果编号选择

- JarvisAgent 现在会保存最近一次问答返回的资料路径列表。
- 问答返回多条结果后，可以说“给第二条结果打标签 运行环境”，会作用到回答里的第 2 条资料。
- 支持 `第二条结果` 和 `第2条结果` 这类简单序号表达。
- 没有最近搜索结果时，会提示先提问；序号超出范围时会提示当前结果数量。
- 本阶段不改变知识库检索排序、得分和回答格式，也不做跨会话持久化。
- RED 验证：
  - 新增 2 个测试先把“第二条结果”误当成真实文件名，未能选择最近搜索结果。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_requires_recent_results -v`：2 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：53 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge -v`：23 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：189 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：查看编号搜索结果

- 问答返回多条结果后，可以说“查看第二条结果”或“查看第2条结果”。
- JarvisAgent 会读取对应 data 文件，并返回 `data/...` 路径和文件内容。
- 没有最近搜索结果时，会提示先提问；序号超出范围时继续提示当前结果数量。
- 本阶段只读取 data 文件内容，不启动外部应用，也不改变知识库检索排序、过滤和回答格式。
- RED 验证：
  - 新增 2 个测试先落入长期记忆兜底，未能读取第二条资料或提示缺少最近搜索结果。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_requires_recent_results tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_requires_recent_results -v`：4 个结果编号相关测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：55 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：191 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近搜索结果持久化

- 最近搜索结果路径列表现在会写入项目外 `jarvis-lite-runtime/agent-context.json`。
- 新建 Agent 实例后，仍可继续说“查看第二条结果”，读取上一次问答命中的第二条资料。
- 读取运行态上下文时，如果文件缺失或损坏，会回退为空上下文。
- Agent 测试根目录改为临时目录下的 `jarvis-lite` 子目录，和运行态目录隔离，避免跨测试串扰。
- RED 验证：
  - 新增 1 个测试先证明新 Agent 实例无法恢复最近搜索结果。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_search_results_survive_new_agent_instance -v`：1 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：56 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：192 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近上下文状态查询

- 新增自然语言查询：
  - “查看最近上下文”
  - “最近上下文状态”
  - “你还记得刚才什么”
- 查询结果会展示最近资料、最近目录和最近搜索结果列表。
- 没有上下文时，会提示先提问、导入资料，或打开/整理目录。
- 新建 Agent 实例后，如果已恢复最近搜索结果，也能在最近上下文状态中展示对应结果列表。
- 本阶段只做状态可见性，不改变最近资料和最近目录的持久化策略。
- RED 验证：
  - 新增 3 个测试先全部落入长期记忆兜底，未返回最近上下文状态。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_empty_state tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_current_context tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_search_results -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：59 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：195 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近资料和最近目录持久化

- `RuntimeContext` 现在同时保存最近资料路径、最近目录和最近搜索结果。
- 运行态文件仍位于项目外 `jarvis-lite-runtime/agent-context.json`，损坏或缺失时继续回退为空上下文。
- 新建 Agent 实例后，可以继续说“给这个资料打标签 项目”，作用到上次导入或命中的资料。
- 新建 Agent 实例后，可以继续说“打开这个目录”，复用上次打开或整理的目录。
- 本阶段不改变 `/ask` 排序、导入流程、目录打开记录格式，也不实际启动资源管理器。
- RED 验证：
  - 新增 2 个测试先证明新 Agent 实例无法恢复最近资料和最近目录。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_imported_document_survives_new_agent_instance -v`：1 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_directory_survives_new_agent_instance -v`：1 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：61 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：197 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：经验记忆第一版

- 新增 `memory/experiences.md`，用于保存可复用流程经验。
- 新增 `/experience 经验内容`，写入经验记忆。
- 新增 `/experiences`，查看经验记忆；经验文件缺失时会返回清晰空状态。
- 新增自然语言表达：
  - “记录经验：导入资料后先打标签”
  - “记住这个经验：导入资料后先打标签”
  - “查看经验记忆”
- “记住这个经验：...” 不再误写入长期身份/偏好记忆。
- 本阶段不自动抽取任务日志，不调用大模型总结经验，不做经验搜索、评分或分类。
- RED 验证：
  - `tests.test_memory` 先因缺少 `append_experience` 和 `read_experiences` 导入失败。
  - `/experience` 和 `/experiences` 先返回未知命令。
  - “记住这个经验：...” 先被误写入长期记忆。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_memory -v`：11 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：65 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：203 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：经验引用第一版

- 新增 `list_recent_experiences()`，默认返回最近 3 条经验，最新经验排在前面。
- “你现在能做什么事”会在已有经验时展示最近经验列表。
- 日报新增“经验记忆”段，列出最近经验；没有经验时写明暂无经验记忆。
- 本阶段不改变 `/experiences` 全文查看格式，不做经验搜索、分类、评分或自动抽取。
- RED 验证：
  - `tests.test_memory` 先因缺少 `list_recent_experiences` 导入失败。
  - 能力摘要先没有展示“最近经验”。
  - 日报先没有“经验记忆”段。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent tests.test_automation -v`：83 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：205 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：经验搜索第一版

- 新增 `search_experiences()`，按关键词在 `memory/experiences.md` 中做简单包含匹配。
- 新增 `/experience-search 关键词`，按最新优先返回最多 5 条匹配经验。
- 新增自然语言表达：
  - “搜索经验 导入”
  - “查找经验：导入”
- 没有关键词时会提示用法；没有匹配项时会返回明确的空结果提示。
- 本阶段不做分词、模糊匹配、评分、分类或大模型改写，保持本地可测试的确定性行为。
- RED 验证：
  - 新增 5 个测试先分别因缺少 `search_experiences()`、`/experience-search` 未知命令和自然语言未映射失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v`：83 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：210 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：经验操作建议第一版

- 新增 `/experience-advice 关键词`，复用经验搜索结果给出操作建议。
- 新增自然语言表达：
  - “我该怎么导入资料”
  - “导入资料有什么经验”
  - “给我导入资料的建议”
- 有匹配经验时会输出“操作建议”、相关经验编号和可继续使用的 `/experience-search 关键词`。
- 没有匹配经验时会提示先用 `/experience 经验内容` 沉淀可复用流程。
- 本阶段不做开放式规划、不调用大模型、不做经验评分或分类。
- RED 验证：
  - 新增 4 个 Agent 测试先分别因 `/experience-advice` 未知命令和自然语言落入资料问答失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：74 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：214 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：经验建议命令联动第一版

- `/experience-advice 关键词` 现在会在相关经验之外追加“可执行命令”。
- 第一版按固定关键词映射现有本地命令，覆盖导入、标签、知识库、日报、目录、更新、语音和经验。
- 例如“导入资料有什么建议”会提示 `/import 源文件或目录路径 [目标文件名]`、`/kb` 和 `/tag 文件名 标签...`。
- 没有相关经验但命中已知能力时，仍会给出命令建议，并提示可先用 `/experience 经验内容` 沉淀经验。
- 本阶段不做开放式计划生成、不推断真实文件路径、不执行建议命令。
- RED 验证：
  - 新增 3 个 Agent 测试先因建议输出缺少“可执行命令”失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：77 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：217 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：经验建议引用最近上下文第一版

- `/experience-advice 这个资料` 会引用最近导入、标签更新或问答命中的资料。
- `/experience-advice 这个目录` 会引用最近打开或整理预览的目录。
- 有最近资料时，会输出 `当前资料：data/...`，并提示 `/read ...`、`/tag ... 标签...` 和 `/ask 问题`。
- 有最近目录时，会输出 `当前目录：别名 -> 路径`，并提示 `/organize-preview 别名` 和 `/dir-open 别名`。
- 缺少最近资料或目录时，会明确提示当前上下文缺失，并保留通用命令建议。
- 本阶段不自动执行建议命令，不推断路径，也不改变运行态上下文格式。
- RED 验证：
  - 新增 3 个 Agent 测试先因建议未输出当前资料、当前目录和具体命令失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：80 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：220 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近建议编号查看第一版

- `JarvisAgent` 现在会在当前实例内记录最近一次经验建议生成的命令建议列表。
- 用户获取建议后，可以继续说“查看第一条建议”或“查看第二条建议”。
- 返回内容只展示对应建议命令，不自动执行，也不持久化到运行态文件。
- 没有最近建议时，会提示先说“我该怎么导入资料”或使用 `/experience-advice 关键词`。
- RED 验证：
  - 新增 3 个 Agent 测试先全部落入普通兜底，无法查看编号建议。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：83 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：223 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近建议持久化第一版

- 最近建议列表现在会写入项目外 `jarvis-lite-runtime/agent-context.json`。
- 新建 `JarvisAgent` 实例后，仍可继续说“查看第一条建议”，读取上一次 `/experience-advice` 生成的命令建议。
- 读取运行态上下文时，缺失的 `recent_advice_suggestions` 字段会按空列表处理，兼容旧运行态文件。
- 本阶段不自动执行建议命令，不替换占位符参数，也不扩展最近上下文状态展示。
- RED 验证：
  - 新增 1 个测试先证明新 Agent 实例无法恢复最近建议。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_advice_suggestions_survive_new_agent_instance -v`：1 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：84 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：224 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近建议执行前确认第一版

- 用户获取经验建议后，可以说“执行第二条建议”，Jarvis Lite 会先展示将执行的命令并等待确认。
- 说“确认执行”后，会复用现有 `JarvisAgent.handle()` 命令路径执行待确认命令，例如 `/kb` 会返回知识库状态。
- 说“取消执行”会清空当前待确认建议命令。
- 建议命令包含占位符参数时，例如 `/import 源文件或目录路径 [目标文件名]`，不会进入待确认状态，会提示用户补全参数后手动输入。
- 待确认命令只保存在当前 Agent 实例内，不写入运行态文件。
- RED 验证：
  - 新增 3 个 Agent 测试先全部落入长期记忆兜底，无法准备执行、确认执行或提示缺少待确认命令。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice tests.test_agent.AgentTests.test_natural_language_prepare_advice_requires_completed_parameters tests.test_agent.AgentTests.test_natural_language_confirm_advice_requires_pending_command -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：87 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：227 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近建议状态展示第一版

- “查看最近上下文”现在会展示最近建议数量，并按编号列出建议文本。
- 准备执行建议后，“查看最近上下文”会展示当前待确认建议命令，例如 `/kb`。
- 新建 `JarvisAgent` 实例后，最近建议会从运行态上下文恢复并显示在最近上下文状态中；待确认命令仍然只存在当前实例内，重启后显示为无。
- 生成新的最近建议时会清空旧待确认命令，避免用户确认执行过期建议。
- RED 验证：
  - 新增 3 个 Agent 测试先证明最近上下文状态未展示最近建议、待确认命令和恢复后的最近建议。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_advice tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_advice_command tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_advice -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：90 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：230 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：建议命令参数补全草稿

- 对含占位符的最近建议说“执行第一条建议”时，不会进入待确认执行状态，而是返回可编辑命令草稿。
- 例如 `/import 源文件或目录路径 [目标文件名]` 会提示 `命令草稿：/import <源文件或目录路径> [目标文件名]`。
- 尖括号表示必须替换的占位内容，方括号参数可以按需保留或替换。
- 完整命令建议仍保持原有两步确认流程，例如“执行第二条建议”后再说“确认执行”。
- 本阶段不推断真实路径，不自动补全参数，也不执行不完整命令。
- RED 验证：
  - 新增 1 个 Agent 测试先因缺少“命令草稿”失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_prepare_advice_with_missing_parameters_returns_command_draft tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice tests.test_agent.AgentTests.test_natural_language_prepare_advice_requires_completed_parameters -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：91 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：231 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：草稿参数接收第一版

- 用户对含占位符建议说“执行第一条建议”后，Jarvis Lite 会记录当前草稿对应的命令名。
- 用户在同一 Agent 实例内输入补全后的同类命令，例如 `/import C:\path\to\draft-source.md`，不会立即执行，而是进入待确认建议命令状态。
- 用户再说“确认执行”后，才复用现有命令路径真正导入资料。
- 没有草稿上下文时，普通 `/import 路径` 保持原有直接执行行为。
- 修正建议命令文本解析，只用中文冒号拆分建议描述，避免 Windows 路径中的 `C:` 被误切断。
- 本阶段不做自然语言填槽、不推断真实路径、不持久化草稿状态。
- RED 验证：
  - 新增 1 个 Agent 测试先证明补全后的 `/import` 会直接执行，没有等待确认。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_completed_advice_command_draft_waits_for_confirmation tests.test_agent.AgentTests.test_natural_language_prepare_advice_with_missing_parameters_returns_command_draft tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：92 个测试通过。

## 追加进度：已知下载目录自然语言

- 未登记常用目录时，`整理下载目录` 会尝试使用用户主目录下的 `Downloads` 或 `下载` 目录生成文件整理预览。
- 未登记常用目录时，`打开下载目录` 会尝试使用用户主目录下的 `Downloads` 或 `下载` 目录写入打开请求记录。
- 已登记的常用目录仍优先于系统目录 fallback，方便用户覆盖自己的下载目录路径。
- 本阶段仍只做目录识别、整理预览和打开记录，不真实移动文件，也不启动外部资源管理器。
- RED 验证：
  - 新增 2 个测试先分别因找不到 `下载` 常用目录和未写入打开记录失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_downloads_uses_known_downloads_directory tests.test_agent.AgentTests.test_natural_language_open_downloads_uses_known_downloads_directory tests.test_agent.AgentTests.test_natural_language_organize_desktop_uses_known_desktop_directory tests.test_agent.AgentTests.test_natural_language_open_desktop_uses_known_desktop_directory -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：94 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：234 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：已知项目目录自然语言

- 未登记常用目录时，`整理项目目录` 会直接使用当前 Jarvis Lite 项目根目录生成文件整理预览。
- 未登记常用目录时，`打开项目目录` 会直接使用当前 Jarvis Lite 项目根目录写入打开请求记录。
- 已登记的 `项目` 常用目录仍优先于项目根目录 fallback，方便用户覆盖实际工作项目路径。
- 本阶段仍只做目录识别、整理预览和打开记录，不真实移动文件，也不启动外部资源管理器。
- RED 验证：
  - 新增 2 个测试先分别因找不到 `项目` 常用目录失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_project_uses_known_project_directory tests.test_agent.AgentTests.test_natural_language_open_project_uses_known_project_directory tests.test_agent.AgentTests.test_natural_language_open_common_directory_alias_records_request tests.test_agent.AgentTests.test_natural_language_organize_common_directory_alias_returns_preview -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：96 个测试通过。

## 追加进度：知识库问答证据增强

- `/ask` 和普通问题命中知识库时，每条结果会继续显示 `data/文件:行号` 和原始命中文本。
- 每条结果新增“命中原因：关键词匹配分数 N”，让用户知道这是规则式关键词匹配，而不是无来源生成。
- 回答末尾新增“可继续操作”，提示可以“查看第一条结果”“给这个结果打标签 标签”或 `/read 文件名`。
- 本阶段不改变搜索排序、匹配分数算法、弱相关过滤、最近搜索结果持久化和结果数量。
- RED 验证：
  - 新增 1 个 Knowledge 测试先证明回答缺少“命中原因”和“可继续操作”。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_answer_from_data_reports_match_reason_and_follow_up_actions tests.test_knowledge.KnowledgeTests.test_answer_from_data_includes_source_and_matching_content tests.test_knowledge.KnowledgeTests.test_answer_from_data_numbers_multiple_sources_after_summary tests.test_knowledge.KnowledgeTests.test_answer_from_data_can_include_multiple_sources -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge -v`：24 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：96 个测试通过。

## 追加进度：日报运行态上下文联动

- 日报新增“最近上下文”段，读取项目外 `jarvis-lite-runtime/agent-context.json`。
- 最近上下文段会展示最近资料、最近目录、最近搜索结果和最近建议。
- 没有运行态上下文时，日报会写明“暂无最近上下文”。
- 本阶段不改变运行态上下文文件格式，不改变“查看最近上下文”命令，也不改动经验记忆和工具日志段。
- RED 验证：
  - 新增 1 个 Automation 测试先证明日报缺少“最近上下文”段。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context tests.test_automation.AutomationTests.test_write_daily_report_creates_word_markdown -v`：2 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_automation -v`：6 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：96 个测试通过。

## 追加进度：日报下一步建议生成

- 日报新增“下一步建议”段，复用已有最近上下文、经验记忆和工具日志。
- 有最近资料时，日报会提示继续 `/read` 和 `/tag` 当前资料。
- 有最近目录时，日报会提示 `/organize-preview` 和 `/dir-open` 当前目录。
- 有最近建议、经验记忆或工具日志时，日报会提示查看建议、检索经验或沉淀工具流程。
- 没有任何上下文时，日报会给出导入资料、登记常用目录和记录经验的基础建议。
- 本阶段不调用大模型，不自动执行建议，也不改动运行态上下文文件格式。
- RED 验证：
  - 新增 1 个 Automation 测试先证明日报缺少“下一步建议”段。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context tests.test_automation.AutomationTests.test_write_daily_report_creates_word_markdown -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_automation -v`：7 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：96 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：239 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：读取资料写入最近上下文

- `/read 文件名` 成功读取 data 资料后，会把该文件写入最近资料上下文。
- 新建 `JarvisAgent` 实例后，也能恢复这份最近资料，继续执行“给这个资料打标签 项目”。
- 读取失败时不更新最近资料，避免把不存在的文件写入运行态上下文。
- 本阶段只处理已有 `/read` 命令，不新增自然语言读取意图，也不改变运行态上下文字段。
- RED 验证：
  - 新增 1 个 Agent 测试先证明 `/read manual.md` 后重启 Agent 仍然没有最近资料。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_read_command_sets_persistent_recent_document_context -v`：1 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：97 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：240 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：自然语言读取资料

- “读取 manual.md”“查看 note.txt”“看看 data/note.md”会映射到现有 `/read` 命令。
- 自然语言读取成功后，继续复用 `/read` 的最近资料上下文更新；后续可以说“给这个资料打标签 项目”。
- 只识别 `.md` 和 `.txt` 后缀的资料文件名，避免误判“查看知识库”“查看最近上下文”等状态查询。
- “查看第一条结果”和“查看第一条建议”仍然走编号上下文逻辑，不被文件读取意图覆盖。
- RED 验证：
  - 新增 1 个 Agent 测试先证明“读取 manual.md”落入长期记忆兜底，没有返回资料内容。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_document_updates_recent_document_context tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_first_advice_after_experience_advice -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：98 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：241 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：自然语言读取最近资料

- 有最近资料上下文时，“读取这个资料”“查看这个资料”“看看当前资料”会读取当前资料内容。
- 没有最近资料时，会提示先读取资料、导入资料或指定文件名，不再把“这个资料”交给普通知识库检索。
- 本阶段复用现有 `/read` 命令，不改变运行态上下文字段，也不改变编号结果和编号建议读取。
- RED 验证：
  - 新增 2 个 Agent 测试先证明“读取这个资料”会落入普通知识库检索，并且无上下文时没有明确提示。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_recent_document_reads_current_document tests.test_agent.AgentTests.test_natural_language_read_recent_document_requires_recent_context tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_first_advice_after_experience_advice -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：100 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：243 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近资料列表第一版

- 最近资料不再只保留单个当前资料，同时维护最近资料列表，最多保留 5 条，最新在前。
- “查看最近上下文”会展示“最近资料列表”，便于看见最近读过、导入过或问答命中过的多份资料。
- 新建 `JarvisAgent` 实例后，最近资料列表会从 `jarvis-lite-runtime/agent-context.json` 恢复。
- 日报的“最近上下文”段会展示最近资料列表，下一步建议仍以当前资料为主。
- 本阶段不扫描系统最近文件，不新增真实文件操作，也不改变“读取这个资料”的当前资料语义。
- RED 验证：
  - 新增 2 个 Agent 测试和 1 个 Automation 测试先证明最近上下文和日报只显示单个最近资料。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_document_list tests.test_agent.AgentTests.test_recent_document_list_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_read_recent_document_reads_current_document tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：102 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_automation -v`：7 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：245 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：按编号读取最近资料

- 看到最近资料列表后，可以继续说“读取第二份资料”“查看第2个文档”。
- 该能力只作用于最近资料列表，不改变“查看第二条结果”的最近搜索结果语义。
- 读取成功后复用 `/read`，被读取的资料会成为当前最近资料，并移动到最近资料列表第一位。
- 缺少最近资料列表或编号越界时，会给出明确提示。
- RED 验证：
  - 新增 3 个 Agent 测试，其中“读取第二份资料”和缺少最近资料列表提示都先落入普通知识库检索；“查看第二条结果”回归通过。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_reads_selected_document tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_requires_recent_list tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_does_not_override_search_result tests.test_agent.AgentTests.test_natural_language_read_recent_document_reads_current_document -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：105 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：248 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：按编号给最近资料打标签

- 看到最近资料列表后，可以继续说“给第二份资料打标签 项目”“给第2个文档打标签 Python”。
- 该能力只作用于最近资料列表，不改变“给第二条结果打标签”的最近搜索结果语义。
- 标签更新复用现有 `/tag`，保持知识库标签写入、工具日志和最近资料列表更新逻辑一致。
- 缺少最近资料列表或编号越界时，会给出明确提示。
- RED 验证：
  - 新增 2 个 Agent 测试先证明“给第二份资料打标签”会误走普通 `/tag` 文件名；“给第二条结果打标签”回归通过。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_updates_selected_document_tags tests.test_agent.AgentTests.test_natural_language_tag_numbered_recent_document_requires_recent_list tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_document_reads_selected_document -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：107 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：250 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：系统最近文件列表第一版

- 新增 `/recent-files` 和自然语言“查看最近文件”“最近文件列表”。
- 第一版扫描已登记常用目录，以及已知项目目录、桌面和下载目录的顶层普通文件。
- 最近文件按修改时间倒序展示最多 5 个，输出来源别名、文件名、路径和修改时间。
- 本阶段不递归扫描，不读取文件内容，不打开、不移动、不删除文件。
- RED 验证：
  - 新增 1 个 Automation 测试和 2 个 Agent 测试先证明底层函数、自然语言入口和 `/recent-files` 命令缺失。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_list_recent_files_returns_top_level_files_newest_first tests.test_agent.AgentTests.test_natural_language_recent_files_reports_known_project_files_newest_first tests.test_agent.AgentTests.test_recent_files_command_reports_empty_state -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：109 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_automation -v`：8 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：253 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：按编号查看最近文件详情

- `/recent-files` 和“查看最近文件”现在会把最近文件列表写入 `jarvis-lite-runtime/agent-context.json`。
- 看到最近文件列表后，可以继续说“查看第一份最近文件”“读取第2份最近文件”。
- 编号查看只输出文件名、来源、路径和修改时间，不读取文件内容，也不打开文件。
- 新建 `JarvisAgent` 实例后，仍可恢复最近文件列表并按编号查看详情。
- RED 验证：
  - 新增 3 个 Agent 测试先证明“查看第一份最近文件”没有意图、列表不能跨实例恢复、缺列表时没有明确提示。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_file_reports_file_metadata tests.test_agent.AgentTests.test_recent_file_list_survives_new_agent_instance tests.test_agent.AgentTests.test_natural_language_read_numbered_recent_file_requires_recent_files -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：112 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_automation -v`：8 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：256 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近文件纳入最近上下文和日报

- 执行 `/recent-files` 或“查看最近文件”后，“查看最近上下文”会展示最近文件列表数量和编号。
- 新建 `JarvisAgent` 实例后，恢复的最近文件列表也会出现在最近上下文状态中。
- 日报“最近上下文”段会展示最近文件列表，日报“下一步建议”会提示继续“查看第一份最近文件”或重新 `/recent-files`。
- 本阶段仍只展示来源和路径，不读取文件内容、不打开文件、不移动或删除文件。
- RED 验证：
  - 新增 2 个 Agent 测试和扩展 2 个 Automation 测试先证明最近文件未进入最近上下文、跨实例最近上下文和日报。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_file_list tests.test_agent.AgentTests.test_recent_file_list_survives_new_agent_instance_in_recent_context tests.test_automation.AutomationTests.test_write_daily_report_includes_runtime_recent_context tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：114 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_automation -v`：8 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：258 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：最近上下文输出下一步建议

- “查看最近上下文”现在会在上下文状态后追加“下一步建议”。
- 这批建议复用日报的确定性建议生成逻辑，不解析日报 Markdown。
- 有最近资料时提示继续 `/read` 和 `/tag`，有最近目录时提示 `/organize-preview` 和 `/dir-open`。
- 有最近文件时提示“查看第一份最近文件”和 `/recent-files`，有最近建议时提示查看/执行第一条建议。
- 本阶段只展示建议文本，不自动执行命令，也不改变确认执行流程。
- RED 验证：
  - 新增 1 个 Agent 测试先证明已有最近资料、目录、最近文件和最近建议时，“查看最近上下文”没有下一步建议。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_suggests_next_actions tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context -v`：2 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：115 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_automation -v`：8 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：259 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：桌面快捷入口补齐最近上下文和最近文件

- 桌面面板快捷命令新增“最近上下文”和“最近文件”。
- 托盘快捷命令继续复用同一套 `direct_quick_commands()`，会同步出现这两个入口。
- “最近上下文”快捷入口提交自然语言 `查看最近上下文`，复用本地意图层。
- “最近文件”快捷入口提交 `/recent-files`。
- `/organize-preview` 仍然因为需要参数而不会进入直接快捷入口。
- RED 验证：
  - 扩展桌面桥接和面板测试，先证明快捷命令缺少 `查看最近上下文`、`/recent-files`，面板无法点击“最近上下文”。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`：19 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v`：8 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：260 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 后续建议

- 后续接入大模型时，应让大模型输出结构化意图建议，再由本地大脑决定是否执行。
- 下一步可以继续做“个人设备级 Agent 电脑工作台增强”，优先围绕知识库摘要、最近文件后续操作和桌面入口细化做更稳定的上下文识别。
