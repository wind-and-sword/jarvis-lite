# Jarvis Lite 桌面更新检查第一版执行计划

> 日期：2026-05-20
> 执行者：Codex

## 目标

实现第 5 阶段更新机制第一版：版本清单解析、手动检查更新、桌面快捷入口和下载地址提示。

## 文件范围

- 新增 `src/jarvis_lite/update.py`：版本比较、清单解析、更新检查、状态文案。
- 新增 `tests/test_update.py`：更新模块单元测试。
- 修改 `src/jarvis_lite/agent.py`：接入 `/update-status [清单路径或URL]`。
- 修改 `tests/test_agent.py`：覆盖更新命令。
- 修改 `src/jarvis_lite/desktop/bridge.py`：快捷命令增加“检查更新”，错误状态识别更新失败。
- 修改 `tests/test_desktop_bridge.py`、`tests/test_desktop_widgets.py`、`tests/test_desktop_tray.py`：更新快捷命令断言。
- 更新 `README.md`、`verification.md`、`word/文档索引.md`。
- 新增 `word/2026-05-20-jarvis-lite-desktop-update-check-progress.md`。
- 更新 `.codex/testing.md` 和 `.codex/operations-log.md`，本地留痕不提交。

## TDD 步骤

1. 新增 `tests/test_update.py`：
   - `is_newer_version("0.10.0", "0.2.0")` 为真。
   - 无更新源返回“更新源：未配置”。
   - 本地 JSON 清单版本更高时返回更新可用和下载地址。
   - 当前版本已是最新时返回无需更新。
2. 扩展 `tests/test_agent.py`：
   - `/update-status <manifest.json>` 返回发现新版本和下载地址。
3. 扩展桌面测试：
   - `quick_commands()` 和 `direct_quick_commands()` 包含 `/update-status`。
   - 面板快捷命令文本包含“检查更新”。
   - 托盘快捷命令文本来自同一组 direct commands。
4. 运行 RED，确认失败。
5. 实现 `update.py`、Agent 命令和桌面快捷命令。
6. 运行专项测试，确认 GREEN。
7. 更新正式文档和验证记录。
8. 运行全量测试、源码桌面 smoke、安装器构建、打包 exe smoke、`git diff --check`。
9. 单独提交并 push 本阶段。
