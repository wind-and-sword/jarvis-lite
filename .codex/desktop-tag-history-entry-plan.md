# 桌面批量标签历史入口计划

日期：2026-05-26  
执行者：Codex

## 目标

让桌面面板和托盘直接显示“标签历史”快捷入口，点击后执行 `/tag-history`，方便查看最近批量标签操作摘要。

## 步骤

1. 在 `tests/test_desktop_bridge.py` 扩展快捷命令测试，要求 `quick_commands()` 和 `direct_quick_commands()` 包含 `/tag-history`。
2. 在 `tests/test_desktop_widgets.py` 扩展面板快捷按钮测试，并新增点击“标签历史”按钮的行为测试。
3. 运行目标测试确认 RED。
4. 修改 `src/jarvis_lite/desktop/bridge.py`，把 `/tag-history` 加入直接快捷命令白名单和快捷命令列表。
5. 运行目标测试和桌面相关回归。
6. 更新 README、进度文档和验证记录。

## 验收

- 桌面 direct quick commands 包含“标签历史”。
- 面板点击“标签历史”会提交 `/tag-history`。
- 无历史时输出“批量打标签历史：还没有记录。”，状态为 success。
- 全量测试、桌面 smoke、`git diff --check` 通过。
