# v116：文本输入自动化第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v115 鼠标点击自动化第一阶段，继续推进 Jarvis Lite 1.0 验收线中的键鼠自动化基础。

## 目标

`0.111.0` 建立文本输入自动化第一阶段，让 Jarvis Lite 能通过显式命令 `/type-text 文本` 向当前焦点输入文本，并返回可复盘的执行结果。该阶段只做显式文本输入，不点击目标、不切换窗口、不启动应用、不接入自然语言自动输入。

## 范围

- 在 `src/jarvis_lite/automation.py` 新增文本输入动作：
  - 解析显式文本内容，拒绝空文本。
  - 记录输入字符数和执行时间。
  - 使用 `pyperclip` 写入剪贴板，再通过既有 `pyautogui` 发送粘贴快捷键，优先支持 Unicode 文本。
  - 支持执行器注入，单元测试不触发真实文本输入。
- 在 `JarvisAgent` 增加命令 `/type-text 文本`：
  - 参数为空时返回用法。
  - 执行成功后写入工具日志。
  - 执行失败时返回 `文本输入失败：...`。
- 更新 `/automation-status` 当前能力说明，把文本输入列入桌面自动化基础能力。
- 更新版本、README、PROJECT-PLAN、计划索引、文档索引、进度记录和验证记录到 `0.111.0`。

## 非目标

- 不做目标输入框识别。
- 不做点击、拖动、窗口切换或应用启动。
- 不把自然语言直接映射到文本输入执行。
- 不在单元测试中真实输入文本。
- 不承诺恢复用户剪贴板内容；当前阶段优先建立显式输入能力。

## 文件计划

- 修改 `pyproject.toml`：版本提升到 `0.111.0`，新增 `pyperclip` 运行时依赖。
- 修改 `src/jarvis_lite/__init__.py`：版本提升到 `0.111.0`。
- 修改 `src/jarvis_lite/automation.py`：新增文本输入解析、结果和真实 adapter。
- 修改 `src/jarvis_lite/agent.py`：接入 `/type-text` 命令和帮助文案。
- 修改 `tests/test_automation.py`：覆盖文本解析、空文本拒绝和执行器注入。
- 修改 `tests/test_agent.py`：覆盖 Agent `/type-text` 命令、空参数、执行失败和版本更新测试夹具。
- 修改 `tests/test_project_metadata.py`：版本提升到 `0.111.0`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md`、`word/progress/2026-06-03.md`、`verification.md` 和 `verification/2026-06/*`。

## 执行步骤

1. RED：新增 `tests.test_automation` 文本输入解析、空文本拒绝和执行器注入测试，先确认缺少相关 API。
2. GREEN：实现文本输入请求、执行结果和 pyperclip + pyautogui adapter。
3. RED：新增 Agent `/type-text` 测试，先确认命令未接入。
4. GREEN：接入 `JarvisAgent` 命令、日志和帮助文案。
5. RED/GREEN：版本一致性测试更新到 `0.111.0`。
6. 文档同步：更新当前方案、索引、README、进度和验证记录。
7. 回归：运行 `tests.test_automation`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
8. Smoke：运行 `/automation-status` 验证新能力展示；真实 `/type-text` smoke 因会影响当前焦点输入和剪贴板，默认跳过并记录原因。
9. 打包验证：运行 Windows 安装包构建、版本化复制、安装脚本/SED/版本资源检查和打包后 smoke。

## 验收标准

- `/type-text Hello Jarvis` 能解析为文本 `Hello Jarvis` 并调用文本执行器。
- 空参数给出用法或可读失败原因，不触发执行器。
- 执行失败返回 `文本输入失败：...`。
- 单元测试不真实输入文本。
- `/automation-status` 明确展示文本输入能力。
