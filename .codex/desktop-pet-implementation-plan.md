# 桌面虚拟助手第一版 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把现有命令行核心逐步包装成桌面虚拟助手应用，第一步先提供 GUI 可调用的 bridge 层。

**Architecture:** 保留 `JarvisAgent` 和 `ConversationSession` 作为核心，不重写命令处理。新增 `jarvis_lite.desktop` 包，先实现纯 Python 的 `DesktopBridge`、状态枚举和快捷命令定义；后续 PySide6 UI 只调用 bridge。

**Tech Stack:** Python 3.13、标准库 `dataclasses`、`unittest`，后续 GUI 层再引入 PySide6。

---

## File Structure

- Create: `src/jarvis_lite/desktop/__init__.py`
- Create: `src/jarvis_lite/desktop/state.py`
- Create: `src/jarvis_lite/desktop/bridge.py`
- Create: `tests/test_desktop_bridge.py`
- Create: `word/2026-05-19-jarvis-lite-desktop-app-progress.md`
- Modify: `word/文档索引.md`
- Modify: `verification.md`

## Task 1: Desktop Bridge

**Files:**
- Create: `tests/test_desktop_bridge.py`
- Create: `src/jarvis_lite/desktop/__init__.py`
- Create: `src/jarvis_lite/desktop/state.py`
- Create: `src/jarvis_lite/desktop/bridge.py`

- [ ] **Step 1: Write failing test for basic bridge send**

```python
def test_send_returns_desktop_response_from_conversation_session(self):
    response = self.bridge.send("/memory")
    self.assertEqual(response.state, DesktopState.SUCCESS)
    self.assertIn("用户偏好：中文回答", response.assistant_text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge.DesktopBridgeTests.test_send_returns_desktop_response_from_conversation_session -v`
Expected: FAIL because `jarvis_lite.desktop` does not exist.

- [ ] **Step 3: Implement minimal bridge and state**

Implement `DesktopBridge.send(text)` by delegating to `ConversationSession.handle(text)` and returning immutable `DesktopResponse`.

- [ ] **Step 4: Verify bridge test passes**

Run the same single test. Expected: PASS.

- [ ] **Step 5: Add state/error and quick command tests**

Cover unknown command => `DesktopState.ERROR`; quick command list includes `/status`, `/kb`, `/dirs`, `/daily-report`, `/organize-preview`.

- [ ] **Step 6: Implement missing behavior**

Add error classification and `quick_commands()`.

- [ ] **Step 7: Run desktop bridge tests**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v`
Expected: PASS.

## Task 2: Documentation and Verification

**Files:**
- Create: `word/2026-05-19-jarvis-lite-desktop-app-progress.md`
- Modify: `word/文档索引.md`
- Modify: `verification.md`

- [ ] **Step 1: Document current desktop app progress**

Record that only bridge layer is implemented; PySide6 window and visual assets are next.

- [ ] **Step 2: Update verification record**

Add desktop bridge test command and final test count.

- [ ] **Step 3: Run full verification**

Run: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 4: Commit and push**

Commit message: `feat: 增加桌面助手桥接层`
