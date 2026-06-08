# Desktop Panel Size Persistence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让桌面助手面板的宽高可以随用户调整后保存，并在下次启动时恢复。

**Architecture:** `DesktopSettings` 继续作为桌面运行态设置模型，新增 `panel_width` 和 `panel_height` 字段。`settings.py` 提供保存面板尺寸的窄接口，保存时保留窗口位置、置顶、透明度和小助手尺寸。`AssistantPanel` 负责按设置恢复自身尺寸，并在用户调整面板大小或关闭面板时保存尺寸。

**Tech Stack:** Python 3.13、PySide6、标准库 `unittest`、现有 `jarvis_lite.desktop` 包。

---

### Task 1: 扩展桌面设置模型

**Files:**
- Modify: `tests/test_desktop_settings.py`
- Modify: `src/jarvis_lite/desktop/settings.py`

- [x] **Step 1: Write the failing test**

在 `tests/test_desktop_settings.py` 增加测试：
- `DesktopSettings(panel_width=560, panel_height=700)` 可以保存并读取。
- `save_desktop_panel_size(paths, 560, 700)` 会保存面板宽高，并保留已有位置和小助手偏好。

- [x] **Step 2: Run tests to verify failure**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v`

Expected: FAIL，原因是 `DesktopSettings` 缺少 `panel_width/panel_height`，且 `save_desktop_panel_size` 不存在。

- [x] **Step 3: Implement minimal settings support**

在 `DesktopSettings` 中新增默认值 `panel_width=420`、`panel_height=620`。更新 load/save/position/preferences 逻辑，新增 `save_desktop_panel_size()`。

- [x] **Step 4: Run tests to verify pass**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v`

Expected: PASS。

### Task 2: 面板恢复并保存尺寸

**Files:**
- Modify: `tests/test_desktop_widgets.py`
- Modify: `src/jarvis_lite/desktop/widgets.py`

- [x] **Step 1: Write failing widget tests**

增加测试：
- `AssistantPanel` 使用 `DesktopSettings(panel_width=560, panel_height=700)` 初始化后恢复该宽高。
- 面板 resize 后，运行态设置文件记录新的 `panel_width/panel_height`。

- [x] **Step 2: Run tests to verify failure**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`

Expected: FAIL，原因是面板尚未读取或保存尺寸。

- [x] **Step 3: Implement minimal widget support**

在 `AssistantPanel` 中定义默认、最小和最大面板尺寸；初始化时按设置恢复尺寸；`resizeEvent` 和 `closeEvent` 调用 `save_desktop_panel_size()` 保存当前尺寸。初始化恢复尺寸时暂不保存，避免创建面板就写运行态文件。

- [x] **Step 4: Run tests to verify pass**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`

Expected: PASS。

### Task 3: 文档、验证和提交

**Files:**
- Modify: `README.md`
- Modify: `verification.md`
- Modify: `word/文档索引.md`
- Create: `word/2026-05-20-jarvis-lite-desktop-panel-size-design.md`
- Create: `word/2026-05-20-jarvis-lite-desktop-panel-size-progress.md`
- Modify: `.codex/testing.md`
- Modify: `.codex/operations-log.md`

- [x] **Step 1: Update docs**

记录面板尺寸持久化的设计、进度和验证结果。

- [x] **Step 2: Run focused verification**

Run:
`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v`
`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`
`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v`

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
`git commit -m "feat: 持久化桌面面板尺寸"`
`git -c http.sslBackend=openssl push origin main`
