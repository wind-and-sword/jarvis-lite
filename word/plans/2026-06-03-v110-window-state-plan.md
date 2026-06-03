# v110：只读窗口感知第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v108 Jarvis Lite 1.0 验收线和 v109 应用注册表，补齐“应用注册与窗口感知”的只读窗口快照基础。

## 目标

`0.105.0` 建立只读窗口感知第一阶段，让 Jarvis Lite 能获取当前 Windows 可见顶层窗口、前台窗口、窗口标题、进程 PID、进程名，并把窗口与 AppRegistry 中的 Chrome、QQ、微信、IntelliJ IDEA 和 Clash Verge 做基础关联。该阶段只做观察和描述，不切换窗口、不点击、不输入、不截图。

## 范围

- 新增 `src/jarvis_lite/window_state.py`：
  - 使用 Windows 原生 `user32`/`kernel32` 只读 API 枚举可见顶层窗口。
  - 记录窗口标题、句柄、PID、进程名和前台状态。
  - 基于进程名和窗口标题别名关联 AppRegistry 应用。
  - 非 Windows 或枚举失败时返回可读的不可用说明。
- 新增 `tests/test_window_state.py` 覆盖 fake 窗口快照、前台窗口识别、应用关联和不可用平台说明。
- 在 `JarvisAgent` 增加只读命令 `/windows`：查看当前窗口快照，不触发任何外部应用操作。
- 更新帮助文案、当前方案、方案索引、文档索引、进度记录、验证记录和版本号到 `0.105.0`。

## 非目标

- 不启动、切换、置顶或关闭任何窗口。
- 不发送快捷键、文本输入、点击或鼠标移动。
- 不截图，不 OCR。
- 不把窗口历史自动写入长期记忆。
- 不新增跨平台窗口自动化抽象；当前阶段只支持 Windows，只读失败时给出说明。

## 文件计划

- 新增 `src/jarvis_lite/window_state.py`：只读窗口快照和描述逻辑。
- 新增 `tests/test_window_state.py`：窗口快照单元测试。
- 修改 `src/jarvis_lite/agent.py`：接入 `/windows` 和帮助文案。
- 修改 `tests/test_agent.py`：Agent 命令回归。
- 修改 `pyproject.toml` 和 `src/jarvis_lite/__init__.py`：版本提升到 `0.105.0`。
- 修改 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md` 和 `word/progress/2026-06-03.md`：文档同步。

## TDD 步骤

1. RED：新增 `tests/test_window_state.py`，先确认缺少 `jarvis_lite.window_state` 失败。
2. GREEN：实现 fake 窗口快照构建、前台窗口识别、AppRegistry 关联和描述输出。
3. RED：新增 Agent `/windows` 测试，先确认 `describe_current_windows` 尚未接入。
4. GREEN：接入 Agent 命令、运行日志和帮助文案。
5. RED/GREEN：版本一致性测试更新到 `0.105.0`。
6. 回归：运行 `tests.test_window_state`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
7. Smoke：运行 `src\app.py --once "/windows"`、桌面源码 smoke 和打包后 smoke。

## 验收

- `/windows` 输出窗口感知状态、当前平台、可见窗口数量、前台窗口和窗口列表。
- 能显示前台窗口标题、进程名、PID 和 AppRegistry 应用匹配结果。
- 能通过进程名匹配 Chrome 等应用，通过标题别名匹配 Clash Verge 等应用。
- 非 Windows 或枚举失败时输出清晰不可用说明。
- 该阶段不启动、不切换、不点击、不输入、不截图。
