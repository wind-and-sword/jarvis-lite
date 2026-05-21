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

## 后续建议

- 下一步可以继续沉淀“最近目录”“最近搜索结果”等上下文，扩大省略指代表达的覆盖范围。
- 后续接入大模型时，应让大模型输出结构化意图建议，再由本地大脑决定是否执行。
- 可以把成功任务沉淀为“经验记忆”，让助手逐步学习用户常用表达和常用流程。
