# 桌面知识库摘要快捷入口计划

> 日期：2026-05-25
> 执行者：Codex

## 目标

把已稳定的 `/kb-summary` 暴露到桌面面板和托盘的无参数快捷入口中，让用户不用记命令也能查看知识库摘要。

## 实现设计

- `quick_commands()` 在“知识库”后新增 `QuickCommand("知识库摘要", "/kb-summary")`。
- `DIRECT_QUICK_COMMAND_PROMPTS` 增加 `/kb-summary`，因为它不需要额外参数。
- 面板和托盘继续复用 `direct_quick_commands()`，不分别维护列表。
- 继续排除 `/organize-preview` 等需要参数的命令。

## 验收标准

- Desktop bridge 测试覆盖 quick/direct 列表包含知识库摘要。
- Desktop widgets 测试覆盖面板按钮展示知识库摘要。
- 全量测试、桌面 smoke 和 `git diff --check` 通过。
