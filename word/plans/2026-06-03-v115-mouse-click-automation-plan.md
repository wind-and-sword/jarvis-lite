# v115：鼠标点击自动化第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v114 快捷键自动化第一阶段，继续推进 Jarvis Lite 1.0 验收线中的键鼠自动化基础。

## 目标

`0.110.0` 建立鼠标点击自动化第一阶段，让 Jarvis Lite 能通过显式命令 `/mouse-click x y [button=left|right|middle]` 在指定屏幕坐标执行一次鼠标点击，并返回可复盘的执行结果。该阶段只做显式坐标点击，不做目标识别、拖动、文本输入、窗口切换、应用启动或自然语言自动点击。

## 范围

- 在 `src/jarvis_lite/automation.py` 新增鼠标点击动作：
  - 解析显式坐标和可选按钮参数。
  - 支持 `left`、`right`、`middle` 三种按钮。
  - 使用既有 `pyautogui` 作为真实执行 adapter。
  - 支持执行器注入，单元测试不触发真实鼠标点击。
- 在 `JarvisAgent` 增加命令 `/mouse-click x y [button=left|right|middle]`：
  - 参数为空或不完整时返回用法或可读失败原因。
  - 执行成功后写入工具日志。
  - 执行失败时返回 `鼠标点击失败：...`。
- 更新 `/automation-status` 当前能力说明，把鼠标点击列入桌面自动化基础能力。
- 更新版本、README、PROJECT-PLAN、计划索引、文档索引、进度记录和验证记录到 `0.110.0`。

## 非目标

- 不做 OCR/窗口目标定位后的自动点击。
- 不做鼠标移动、拖动、长按或滚轮。
- 不做文本输入。
- 不做窗口切换或应用启动。
- 不把自然语言直接映射到点击执行。
- 不在单元测试中真实点击鼠标。

## 文件计划

- 修改 `pyproject.toml`：版本提升到 `0.110.0`。
- 修改 `src/jarvis_lite/__init__.py`：版本提升到 `0.110.0`。
- 修改 `src/jarvis_lite/automation.py`：新增鼠标点击解析、结果和真实 adapter。
- 修改 `src/jarvis_lite/agent.py`：接入 `/mouse-click` 命令和帮助文案。
- 修改 `tests/test_automation.py`：覆盖坐标解析、按钮参数、执行器注入和错误参数。
- 修改 `tests/test_agent.py`：覆盖 Agent `/mouse-click` 命令、空参数、执行失败和版本更新测试夹具。
- 修改 `tests/test_project_metadata.py`：版本提升到 `0.110.0`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md`、`word/progress/2026-06-03.md`、`verification.md` 和 `verification/2026-06/*`。

## 执行步骤

1. RED：新增 `tests.test_automation` 鼠标点击解析、按钮校验和执行器注入测试，先确认缺少相关 API。
2. GREEN：实现鼠标点击参数解析、执行结果和 pyautogui adapter。
3. RED：新增 Agent `/mouse-click` 测试，先确认命令未接入。
4. GREEN：接入 `JarvisAgent` 命令、日志和帮助文案。
5. RED/GREEN：版本一致性测试更新到 `0.110.0`。
6. 文档同步：更新当前方案、索引、README、进度和验证记录。
7. 回归：运行 `tests.test_automation`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
8. Smoke：运行 `/automation-status` 验证新能力展示；真实 `/mouse-click` smoke 因会影响当前桌面，默认跳过并记录原因。
9. 打包验证：运行 Windows 安装包构建、版本化复制、安装脚本/SED/版本资源检查和打包后 smoke。

## 验收标准

- `/mouse-click 100 200` 能解析为坐标 `(100, 200)` 和默认按钮 `left`。
- `/mouse-click 100 200 button=right` 能按右键点击执行器。
- 空参数或不完整坐标给出用法或可读失败原因，不触发执行器。
- 不支持的按钮返回 `鼠标点击失败：...`。
- 单元测试不真实点击鼠标。
- `/automation-status` 明确展示鼠标点击能力。
