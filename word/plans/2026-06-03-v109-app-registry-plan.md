# v109：应用注册表第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v108 Jarvis Lite 1.0 验收线，明确第一批应用注册与只读匹配能力。

## 目标

`0.104.0` 建立 AppRegistry 第一阶段，让 Jarvis Lite 有统一位置记录和识别 Chrome、QQ、微信、IntelliJ IDEA 和 Clash Verge。该阶段先做只读注册、别名匹配、本地路径覆盖和 Agent 查看入口，不直接启动外部应用。

## 范围

- 新增 `src/jarvis_lite/app_registry.py`：
  - 内置五个应用定义。
  - 支持中文、英文和常用简称别名。
  - 支持 `config/apps.local.json` 覆盖应用路径和追加别名。
  - 提供 `list_registered_apps()`、`find_registered_app()` 和 `describe_registered_apps()`。
- 新增 `tests/test_app_registry.py` 覆盖注册表、别名匹配和本地配置覆盖。
- 在 `JarvisAgent` 增加只读命令：
  - `/apps`：查看已登记应用。
  - `/app-find 名称`：按自然语言名称或别名查找应用。
- 更新帮助文案、当前方案、方案索引、文档索引、进度记录和版本号到 `0.104.0`。

## 非目标

- 不启动外部应用。
- 不做窗口枚举、前台窗口识别、截图或 OCR。
- 不写入用户长期记忆或自动学习别名。
- 不把应用注册入口放进桌面面板。
- 不新增远程同步或跨设备配置。

## 文件计划

- 新增 `src/jarvis_lite/app_registry.py`：应用注册表和描述逻辑。
- 新增 `tests/test_app_registry.py`：注册表单元测试。
- 修改 `src/jarvis_lite/agent.py`：接入 `/apps` 和 `/app-find`。
- 修改 `tests/test_agent.py`：Agent 命令回归。
- 修改 `pyproject.toml` 和 `src/jarvis_lite/__init__.py`：版本提升到 `0.104.0`。
- 修改 `word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md` 和 `word/progress/2026-06-03.md`：文档同步。

## TDD 步骤

1. RED：新增 AppRegistry 内置五应用和别名匹配测试，先确认缺少模块失败。
2. GREEN：实现 `app_registry.py`，让内置注册与别名匹配通过。
3. RED：新增本地 `config/apps.local.json` 覆盖路径和追加别名测试。
4. GREEN：实现本地配置读取和路径候选描述。
5. RED：新增 Agent `/apps` 与 `/app-find 名称` 测试。
6. GREEN：接入 Agent 命令和帮助文案。
7. RED/GREEN：版本一致性测试更新到 `0.104.0`。
8. 回归：运行 `tests.test_app_registry`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。

## 验收

- `/apps` 输出五个首批应用及其已配置/未配置状态。
- `/app-find 谷歌浏览器` 命中 Chrome。
- `/app-find 代理面板` 命中 Clash Verge。
- `config/apps.local.json` 可覆盖路径并追加用户别名。
- 不存在的查询返回可读的未找到提示。
- 该阶段不启动任何外部应用。
