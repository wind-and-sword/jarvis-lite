# v111：屏幕截图保存第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v108 Jarvis Lite 1.0 验收线、v109 应用注册表和 v110 只读窗口感知，补齐“看懂屏幕”路线的截图保存基础。

## 目标

`0.106.0` 建立屏幕截图保存第一阶段，让 Jarvis Lite 能通过 `/screenshot [文件名]` 保存当前主屏幕截图到 `logs/screenshots/`，并返回相对路径和图片尺寸。该阶段只做截图落盘，不 OCR、不点击、不切换窗口、不锁定目标窗口。

## 范围

- 新增 `src/jarvis_lite/screen_capture.py`：
  - 使用既有 PySide6 依赖获取当前主屏幕。
  - 将截图保存为 PNG 到 `logs/screenshots/`。
  - 支持显式文件名，缺省时使用时间戳文件名。
  - 返回保存路径、宽高和只截图不操作的边界说明。
- 在 `JarvisAgent` 增加命令 `/screenshot [文件名]`：
  - 文件名可选，省略时自动生成时间戳。
  - 显式文件名自动补 `.png` 后缀。
  - 截图失败时返回可读失败原因。
- 新增 `tests/test_screen_capture.py` 覆盖路径生成、PNG 后缀、空文件名错误和描述输出。
- 更新帮助文案、当前方案、方案索引、文档索引、进度记录、验证记录和版本号到 `0.106.0`。

## 非目标

- 不做 OCR、图片识别或屏幕元素解析。
- 不枚举、切换、置顶或聚焦目标窗口。
- 不发送快捷键、文本输入、点击或鼠标移动。
- 不把截图内容自动写入长期记忆或知识库。
- 不新增截图历史管理、隐私分类或长期图片索引。

## 文件计划

- 新增 `src/jarvis_lite/screen_capture.py`：截图保存和描述逻辑。
- 新增 `tests/test_screen_capture.py`：截图保存单元测试。
- 修改 `src/jarvis_lite/agent.py`：接入 `/screenshot` 和帮助文案。
- 修改 `tests/test_agent.py`：Agent 命令回归。
- 修改 `pyproject.toml` 和 `src/jarvis_lite/__init__.py`：版本提升到 `0.106.0`。
- 修改 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md` 和 `word/progress/2026-06-03.md`：文档同步。

## TDD 步骤

1. RED：新增 `tests/test_screen_capture.py`，先确认缺少 `jarvis_lite.screen_capture` 失败。
2. GREEN：实现截图保存路径、PNG 后缀、空文件名校验和描述输出。
3. RED：新增 Agent `/screenshot` 测试，先确认 `describe_screen_capture` 尚未接入。
4. GREEN：接入 Agent 命令、运行日志和帮助文案。
5. RED/GREEN：版本一致性测试更新到 `0.106.0`。
6. 回归：运行 `tests.test_screen_capture`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
7. Smoke：运行 `src\app.py --once "/screenshot smoke-0.106.0"`、桌面源码 smoke 和打包后 smoke。

## 验收

- `/screenshot` 能保存当前主屏幕截图到 `logs/screenshots/`。
- `/screenshot manual` 能生成 `logs/screenshots/manual.png`。
- 输出包含截图相对路径和图片尺寸。
- 空白显式文件名返回可读错误。
- 该阶段不 OCR、不点击、不切换窗口、不输入。
