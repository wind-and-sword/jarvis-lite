# 0.23.0 桌面内脑候选快捷入口计划

> 日期：2026-06-01
> 执行者：Codex

## 验收契约

- `quick_commands()` 包含 `QuickCommand("内脑候选", "/inner-brain-candidates")`。
- `direct_quick_commands()` 包含该命令。
- 桌面面板显示“内脑候选”按钮。
- 点击按钮执行 `/inner-brain-candidates` 并刷新 transcript/status。
- 不新增自然语言正则，不自动训练，不改变候选后端规则。

## 执行步骤

1. RED：新增桌面 bridge、widgets 和版本测试。
2. GREEN：补充快捷命令和版本号。
3. 文档：同步 README、PROJECT-PLAN、方案索引、进度和验证记录。
4. 验证：运行目标测试、相邻回归、全量 unittest、桌面 smoke、安装包构建与静态检查。
