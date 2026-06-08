# Jarvis Lite 桌面更新下载体验执行计划

> 日期：2026-05-21
> 执行者：Codex

## 目标

实现更新下载体验第一版：基于已有更新清单，把新版本安装包下载或复制到项目外运行态目录，并在命令行、桌面面板和托盘提供入口。

## 文件范围

- 修改 `src/jarvis_lite/update.py`：新增下载目录、下载结果、下载执行和状态文案。
- 修改 `src/jarvis_lite/agent.py`：新增 `/update-download [清单路径或URL]`。
- 修改 `src/jarvis_lite/desktop/bridge.py`：新增“下载更新”快捷命令和下载失败状态识别。
- 修改 `tests/test_update.py`：覆盖本地包复制、最新版本跳过下载和下载状态文案。
- 修改 `tests/test_agent.py`：覆盖 `/update-download`。
- 修改 `tests/test_desktop_bridge.py`、`tests/test_desktop_widgets.py`：覆盖桌面快捷命令。
- 更新 `README.md`、`verification.md`、`word/文档索引.md`。
- 新增 `word/2026-05-21-jarvis-lite-desktop-update-download-progress.md`。
- 更新 `.codex/testing.md`、`.codex/operations-log.md`、`.codex/review-report.md`。

## TDD 步骤

1. 在 `tests/test_update.py` 增加下载行为测试。
2. 运行专项测试，确认因缺少 `download_update()` 或 `describe_update_download()` 失败。
3. 在 `src/jarvis_lite/update.py` 实现最小下载能力。
4. 运行 `tests.test_update`，确认通过。
5. 在 `tests/test_agent.py` 增加 `/update-download` 命令测试。
6. 运行 Agent 专项测试，确认命令缺失失败。
7. 在 `src/jarvis_lite/agent.py` 接入命令和工具日志。
8. 运行 Agent 专项测试，确认通过。
9. 扩展桌面桥接和 widget 测试，确认“下载更新”入口缺失失败。
10. 更新 `src/jarvis_lite/desktop/bridge.py`，让面板和托盘复用新入口。
11. 运行桌面专项测试，确认通过。
12. 更新 README、正式进度文档、文档索引和验证记录。
13. 运行全量测试、桌面 smoke、安装器构建、打包 exe smoke 和 `git diff --check`。
