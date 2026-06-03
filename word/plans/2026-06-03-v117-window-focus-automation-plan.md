# v117：窗口切换自动化第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v116 文本输入自动化第一阶段，继续推进 Jarvis Lite 1.0 验收线中的桌面自动化基础。

## 目标

`0.112.0` 建立窗口切换自动化第一阶段，让 Jarvis Lite 能通过显式命令 `/window-focus 编号或标题/应用名` 切换到当前已存在的可见窗口，并返回可复盘的执行结果。该阶段只做显式窗口切换，不点击、不输入、不启动应用、不接入自然语言自动切换。

## 范围

- 在 `src/jarvis_lite/window_state.py` 新增窗口切换动作：
  - 复用 `/windows` 的窗口快照和 AppRegistry 应用匹配。
  - 支持按 `/windows` 列表编号选择窗口。
  - 支持按已登记应用、窗口标题或进程名匹配窗口。
  - 匹配到多个窗口时返回候选提示，不执行切换。
  - 使用 Windows `ShowWindow` + `SetForegroundWindow` 切到目标窗口。
  - 支持执行器注入，单元测试不触发真实窗口切换。
- 在 `JarvisAgent` 增加命令 `/window-focus 编号或标题/应用名`：
  - 参数为空时返回用法。
  - 执行成功后写入工具日志。
  - 执行失败时返回 `窗口切换失败：...`。
- 更新 `/automation-status` 当前能力说明，把窗口切换列入桌面自动化基础能力。
- 更新版本、README、PROJECT-PLAN、计划索引、文档索引、进度记录和验证记录到 `0.112.0`。

## 非目标

- 不启动应用；目标窗口必须已经存在。
- 不点击、拖动、输入文本或发送快捷键。
- 不做屏幕元素目标识别。
- 不把自然语言直接映射到窗口切换执行。
- 不在单元测试中真实改变前台窗口。

## 文件计划

- 修改 `pyproject.toml`：版本提升到 `0.112.0`。
- 修改 `src/jarvis_lite/__init__.py`：版本提升到 `0.112.0`。
- 修改 `src/jarvis_lite/window_state.py`：新增窗口目标选择、执行结果和 Windows focus adapter。
- 修改 `src/jarvis_lite/agent.py`：接入 `/window-focus` 命令和帮助文案。
- 修改 `src/jarvis_lite/automation.py`：更新自动化状态能力列表。
- 修改 `tests/test_window_state.py`：覆盖编号选择、应用/标题匹配、歧义拒绝和执行器注入。
- 修改 `tests/test_agent.py`：覆盖 Agent `/window-focus` 命令、空参数、执行失败和版本更新测试夹具。
- 修改 `tests/test_project_metadata.py`：版本提升到 `0.112.0`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md`、`word/progress/2026-06-03.md`、`verification.md` 和 `verification/2026-06/*`。

## 执行步骤

1. RED：新增 `tests.test_window_state` 窗口选择、歧义拒绝和执行器注入测试，先确认缺少相关 API。
2. GREEN：实现窗口选择结果、执行器注入和 Windows focus adapter。
3. RED：新增 Agent `/window-focus` 测试，先确认命令未接入。
4. GREEN：接入 `JarvisAgent` 命令、日志和帮助文案。
5. RED/GREEN：版本一致性测试更新到 `0.112.0`。
6. 文档同步：更新当前方案、索引、README、进度和验证记录。
7. 回归：运行 `tests.test_window_state`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
8. Smoke：运行 `/automation-status` 和 `/windows` 验证能力展示；真实 `/window-focus` smoke 因会改变当前前台窗口，默认跳过并记录原因。
9. 打包验证：运行 Windows 安装包构建、版本化复制、安装脚本/SED/版本资源检查和打包后 smoke。

## 验收标准

- `/window-focus 2` 能解析为 `/windows` 列表中的第二个窗口并调用窗口切换执行器。
- `/window-focus Chrome` 这类应用或标题查询在唯一命中时切换窗口。
- 多个窗口命中同一查询时不切换，并提示使用编号或更具体标题。
- 空参数给出用法或可读失败原因，不触发执行器。
- 单元测试不真实切换窗口。
- `/automation-status` 明确展示窗口切换能力。
