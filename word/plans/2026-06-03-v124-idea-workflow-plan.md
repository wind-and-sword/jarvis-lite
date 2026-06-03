# v124：IDEA 项目状态第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v123 QQ/微信准备式工作流第一阶段，继续推进 Jarvis Lite 1.0 验收线中的 IntelliJ IDEA 项目打开与状态识别。

## 背景

`0.118.0` 已完成 QQ/微信准备式工作流第一阶段。按照 v108 推荐落地顺序，下一步进入 IntelliJ IDEA 项目打开与状态识别。

IDEA 涉及项目目录、窗口状态、构建工具和后续测试运行。第一阶段只建立显式边界：可以显式打开 IDEA、聚焦已有 IDEA 窗口、显式用 IDEA 打开本地项目目录，并只读检查项目目录状态；不运行测试、不打开终端、不点击 IDE、不编辑项目文件，也不接入自然语言自动执行。

## 目标

- 新增 `/idea-workflow-status`，展示 IDEA 工作流第一阶段边界。
- 新增 `/idea-open`，只显式打开 IDEA 应用。
- 新增 `/idea-focus`，只聚焦当前已经存在的 IDEA 窗口；无窗口时提示先显式打开。
- 新增 `/idea-open-project 项目路径`，只显式用 IDEA 打开已存在的本地项目目录。
- 新增 `/idea-project-status [项目路径]`，默认检查当前 Jarvis Lite 项目，也可检查显式目录；只读输出项目标记和建议下一步。
- 将 IDEA 打开、聚焦和打开项目纳入授权层桌面动作集合；LLM 只允许建议状态命令，不允许直接建议打开或聚焦。

## 非目标

- 不运行 IDEA 内部测试、构建、调试或终端。
- 不读取或修改 `.idea` 配置内容。
- 不点击 IDE，不输入代码，不切换工具窗口。
- 不推断用户未给出的项目路径。
- 不在单元测试或默认 smoke 中真实启动 IDEA 或切换窗口。

## 文件计划

- 新增 `src/jarvis_lite/idea_workflow.py`：IDEA 状态、打开、聚焦、打开项目和只读项目状态。
- 新增 `tests/test_idea_workflow.py`：覆盖 IDEA 工作流核心契约。
- 修改 `src/jarvis_lite/agent.py`：接入 `/idea-workflow-status`、`/idea-open`、`/idea-focus`、`/idea-open-project` 和 `/idea-project-status`，补充帮助和 `/status`。
- 修改 `src/jarvis_lite/authorization.py`：把 IDEA 打开、聚焦和打开项目纳入桌面动作集合。
- 修改 `src/jarvis_lite/automation.py`：让 `/automation-status` 展示 IDEA 显式动作。
- 修改 `src/jarvis_lite/llm.py`：只把 `/idea-workflow-status` 加入 LLM 允许命令。
- 修改版本与文档：`pyproject.toml`、`src/jarvis_lite/__init__.py`、`tests/test_project_metadata.py`、README、PROJECT-PLAN、方案索引、文档索引、进度和验证记录。

## 执行步骤

1. RED：新增 `tests/test_idea_workflow.py`，验证 IDEA 状态、打开、聚焦、打开项目和只读项目状态，先确认模块不存在。
2. RED：扩展 Agent、授权层、LLM 白名单和版本测试，确认命令尚未接入。
3. GREEN：实现 `idea_workflow.py`，复用 AppRegistry、WindowState 和可注入执行器。
4. GREEN：接入 Agent 命令、帮助、状态、授权层、自动化状态、LLM 白名单和版本。
5. 文档：同步 README、PROJECT-PLAN、方案索引、文档索引、进度和验证记录。
6. 验证：运行目标测试、相邻回归和全量 `unittest`。
7. Smoke：运行 `/idea-workflow-status` 和 `/idea-project-status`；真实 `/idea-open`、`/idea-focus` 与 `/idea-open-project` 因会启动或切换本机应用，默认跳过并记录原因。
8. 打包：构建 Windows 安装包、复制 `JarvisLiteSetup-0.119.0.exe`、校验安装脚本/SED/版本资源，运行打包后 smoke。

## 验收标准

- `/idea-workflow-status` 输出 IDEA 工作流第一阶段边界。
- `/idea-open` 可通过注入执行器验证会调用 IDEA 路径。
- `/idea-focus` 可通过注入窗口快照验证会聚焦 IDEA 窗口；无窗口时提示 `/idea-open`。
- `/idea-open-project 项目路径` 只接受已存在目录，并通过注入执行器验证传入 IDEA 路径和项目目录。
- `/idea-project-status [项目路径]` 只读检查本地目录，输出路径、是否存在、`.idea`、`.git`、常见构建/项目标记和边界说明。
- IDEA 打开、聚焦和打开项目属于授权层桌面动作命令；LLM 只允许建议 `/idea-workflow-status`。
- 本阶段不运行测试、不打开终端、不点击、不输入、不编辑项目文件，不接入自然语言自动执行。
