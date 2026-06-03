# v114：快捷键自动化第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v108 Jarvis Lite 1.0 验收线和 v113 截图 OCR 串联，启动键鼠自动化基础层的第一个可执行动作。

## 目标

`0.109.0` 建立快捷键发送第一阶段，让 Jarvis Lite 能通过显式命令 `/hotkey key1+key2 [...]` 发送一个或多个键盘快捷键组合，并返回可复盘的执行结果。该阶段只做快捷键，不点击、不输入文本、不切换窗口、不启动应用、不接入自然语言自动执行。

## 范围

- 在 `src/jarvis_lite/automation.py` 新增快捷键动作：
  - 新增动作结果数据结构，记录动作类型、组合键、执行时间和说明。
  - 新增快捷键参数解析，支持 `ctrl+l`、`ctrl+shift+esc`、`alt+tab` 等组合。
  - 使用成熟生态 `pyautogui` 作为真实执行 adapter。
  - 支持执行器注入，单元测试不触发真实键盘。
- 在 `JarvisAgent` 增加命令 `/hotkey key1+key2 [...]`：
  - 参数为空时返回用法。
  - 执行成功后写入工具日志。
  - 执行失败时返回可读失败原因。
- 更新 `/automation-status` 当前能力说明，把快捷键列入桌面自动化基础能力。
- 更新版本、README、PROJECT-PLAN、计划索引、文档索引、进度记录和验证记录到 `0.109.0`。

## 非目标

- 不做鼠标点击、拖动或移动。
- 不做文本输入。
- 不做窗口切换或目标窗口定位。
- 不做应用启动。
- 不把自然语言直接映射到快捷键执行。
- 不新增免确认规则或长期授权配置。

## 文件计划

- 修改 `pyproject.toml`：增加 `pyautogui>=0.9,<1` 运行时依赖，版本提升到 `0.109.0`。
- 修改 `src/jarvis_lite/__init__.py`：版本提升到 `0.109.0`。
- 修改 `src/jarvis_lite/automation.py`：新增快捷键动作、解析和真实 adapter。
- 修改 `src/jarvis_lite/agent.py`：接入 `/hotkey` 命令和帮助文案。
- 修改 `tests/test_automation.py`：覆盖快捷键解析、执行器注入、空参数和执行失败。
- 修改 `tests/test_agent.py`：覆盖 Agent `/hotkey` 命令和版本更新测试夹具。
- 修改 `tests/test_project_metadata.py`：版本提升到 `0.109.0`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md`、`word/progress/2026-06-03.md`、`verification.md` 和 `verification/2026-06/*`。

## 执行步骤

1. RED：新增 `tests.test_automation` 快捷键解析和执行器注入测试，先确认缺少相关 API。
2. GREEN：实现快捷键组合解析、执行结果和 pyautogui adapter。
3. RED：新增 Agent `/hotkey` 测试，先确认命令未接入。
4. GREEN：接入 `JarvisAgent` 命令、日志和帮助文案。
5. RED/GREEN：版本一致性测试更新到 `0.109.0`。
6. 文档同步：更新当前方案、索引、README、进度和验证记录。
7. 回归：运行 `tests.test_automation`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
8. Smoke：运行 `/automation-status` 验证新能力展示；真实 `/hotkey` smoke 只选择低风险组合，若当前桌面环境不适合发送真实按键，则在验证记录中标注原因。
9. 打包验证：运行 Windows 安装包构建、版本化复制、安装脚本/SED/版本资源检查和打包后 smoke。

## 验收标准

- `/hotkey ctrl+l` 能解析为 `("ctrl", "l")` 并调用快捷键执行器。
- `/hotkey ctrl+shift+esc alt+tab` 能按顺序执行多个组合。
- 空参数给出用法，不触发执行器。
- 执行器异常能返回 `快捷键执行失败：...`。
- 单元测试不真实发送快捷键。
- `/automation-status` 明确展示快捷键能力。
