# Desktop Tray Recent Result Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 给桌面托盘快捷命令补一个稳定的最近结果入口，让用户从托盘执行命令后能重新打开最近一次结果，而不会重复执行命令。

**Architecture:** `AssistantPanel` 负责记录最近一次提交的完整结果文本，并继续复用 `DesktopBridge`。`DesktopTrayController` 负责把托盘命令标签、执行结果和菜单动作关联起来，新增“最近结果”动作，只显示已有面板内容，不再次调用命令。该阶段不做系统通知、不做真实硬件入口、不做打包。

**Tech Stack:** Python 3.13、PySide6、标准库 `unittest`、现有 `jarvis_lite.desktop` 包。

---

### Task 1: AssistantPanel 记录最近提交结果

**Files:**
- Modify: `tests/test_desktop_widgets.py`
- Modify: `src/jarvis_lite/desktop/widgets.py`

- [x] **Step 1: Write the failing test**

在 `tests/test_desktop_widgets.py` 增加测试：提交 `/memory` 后，`AssistantPanel.last_result_text()` 包含 `用户：/memory`、`Jarvis：` 和记忆内容。

- [x] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_tracks_last_result_after_submission -v`

Expected: FAIL，原因是 `AssistantPanel` 还没有 `last_result_text()`。

- [x] **Step 3: Write minimal implementation**

在 `AssistantPanel.__init__` 中初始化 `_last_result_text = ""`。在 `submit_text()` 收到 `DesktopResponse` 后，把本轮两行对话保存为最近结果，并让 `submit_text()` 返回 response；空输入返回 `None`。

- [x] **Step 4: Run test to verify it passes**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets.DesktopWidgetTests.test_panel_tracks_last_result_after_submission -v`

Expected: PASS。

### Task 2: 托盘菜单增加最近结果入口

**Files:**
- Modify: `tests/test_desktop_tray.py`
- Modify: `src/jarvis_lite/desktop/tray.py`

- [x] **Step 1: Write failing tray tests**

增加测试覆盖：
- 初始“最近结果（暂无）”动作不可用。
- 托盘快捷命令执行后，最近结果文本、动作文案和 tooltip 更新。
- 点击最近结果只显示窗口和面板，不重复提交命令。

- [x] **Step 2: Run tests to verify they fail**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v`

Expected: FAIL，原因是托盘控制器还没有最近结果动作和结果状态。

- [x] **Step 3: Write minimal implementation**

在 `DesktopTrayController` 增加 `recent_result_action`、`recent_result_text()`、`_show_recent_result()`、`_update_recent_result()`。托盘快捷命令连接时同时传入 label 和 prompt；执行后根据 `AssistantPanel.submit_text()` 返回值更新最近结果。点击最近结果只调用显示逻辑，不再次执行命令。

- [x] **Step 4: Run tray tests to verify they pass**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v`

Expected: PASS。

### Task 3: 文档和全量验证

**Files:**
- Modify: `README.md`
- Modify: `verification.md`
- Modify: `word/2026-05-19-jarvis-lite-desktop-app-progress.md`
- Modify: `word/文档索引.md`
- Modify: `.codex/testing.md`
- Modify: `.codex/operations-log.md`

- [x] **Step 1: Update docs**

记录托盘最近结果入口、测试命令和当前阶段进度。用户可读进度继续放 `word/`，Codex 本地验证记录放 `.codex/`。

- [x] **Step 2: Run focused verification**

Run:
`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v`
`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`

Expected: PASS。

- [x] **Step 3: Run full verification**

Run:
`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`
`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`
`git diff --check`

Expected: PASS / exit 0。

- [x] **Step 4: Commit and push**

Run:
`git add ...`
`git commit -m "feat: 增加托盘最近结果入口"`
`git -c http.sslBackend=openssl push origin main`
