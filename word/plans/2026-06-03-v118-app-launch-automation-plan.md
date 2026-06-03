# v118：应用启动自动化第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v117 窗口切换自动化第一阶段，继续推进 Jarvis Lite 1.0 验收线中的常用应用打开能力。

## 目标

`0.113.0` 建立应用启动自动化第一阶段，让 Jarvis Lite 能通过显式命令 `/app-launch 应用名称或别名` 启动 AppRegistry 中已登记且有可用启动路径的应用，并返回可复盘的执行结果。该阶段只做显式应用启动，不切换窗口、不点击、不输入、不发送快捷键、不接入自然语言自动启动。

## 范围

- 在 `src/jarvis_lite/app_registry.py` 新增应用启动动作：
  - 复用既有 `match_registered_app()` 和 `RegisteredApp.launch_path`。
  - 支持 `config/apps.local.json` 的本地 path 覆盖和别名追加。
  - 未匹配应用时返回可读错误。
  - 匹配但没有可用路径时提示在 `config/apps.local.json` 配置 `path`。
  - 默认使用标准库 `subprocess.Popen()` 启动可执行文件。
  - 支持执行器注入，单元测试不启动真实桌面应用。
- 在 `JarvisAgent` 增加命令 `/app-launch 应用名称或别名`：
  - 参数为空时返回用法。
  - 执行成功后写入工具日志。
  - 执行失败时返回 `应用启动失败：...`。
- 更新 `/automation-status` 当前能力说明，把应用启动列入桌面自动化基础能力。
- 更新版本、README、PROJECT-PLAN、计划索引、文档索引、进度记录和验证记录到 `0.113.0`。

## 非目标

- 不自动切换到新启动应用窗口。
- 不点击、拖动、输入文本或发送快捷键。
- 不做屏幕元素目标识别。
- 不把自然语言直接映射到应用启动执行。
- 不在单元测试或默认 smoke 中真实启动桌面应用。

## 文件计划

- 修改 `pyproject.toml`：版本提升到 `0.113.0`。
- 修改 `src/jarvis_lite/__init__.py`：版本提升到 `0.113.0`。
- 修改 `src/jarvis_lite/app_registry.py`：新增应用启动结果、执行器注入和标准库启动 adapter。
- 修改 `src/jarvis_lite/agent.py`：接入 `/app-launch` 命令和帮助文案。
- 修改 `src/jarvis_lite/automation.py`：更新自动化状态能力列表。
- 修改 `tests/test_app_registry.py`：覆盖启动路径、执行器注入、未知应用和缺失路径。
- 修改 `tests/test_agent.py`：覆盖 Agent `/app-launch` 命令、空参数、执行失败和版本更新测试夹具。
- 修改 `tests/test_project_metadata.py`：版本提升到 `0.113.0`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md`、`word/progress/2026-06-03.md`、`verification.md` 和 `verification/2026-06/*`。

## 执行步骤

1. RED：新增 AppRegistry 启动路径、执行器注入、未知应用和缺失路径测试，先确认缺少相关 API。
2. GREEN：实现应用启动结果、执行器注入和 `subprocess.Popen()` adapter。
3. RED：新增 Agent `/app-launch` 测试，先确认命令未接入。
4. GREEN：接入 `JarvisAgent` 命令、日志和帮助文案。
5. RED/GREEN：版本一致性测试更新到 `0.113.0`。
6. 文档同步：更新当前方案、索引、README、进度和验证记录。
7. 回归：运行 `tests.test_app_registry`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
8. Smoke：运行 `/automation-status` 和 `/apps` 验证能力展示；真实 `/app-launch` smoke 因会启动本机应用，默认跳过并记录原因。
9. 打包验证：运行 Windows 安装包构建、版本化复制、安装脚本/SED/版本资源检查和打包后 smoke。

## 验收标准

- `/app-launch 我的浏览器` 能按 AppRegistry 别名命中应用，并调用启动执行器。
- 已登记应用没有可用启动路径时不启动，并提示配置 `config/apps.local.json`。
- 未登记应用给出可读失败原因。
- 空参数给出用法，不触发执行器。
- 单元测试不真实启动桌面应用。
- `/automation-status` 明确展示应用启动能力。
