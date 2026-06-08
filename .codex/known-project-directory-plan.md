# 已知项目目录上下文增强计划

> 日期：2026-05-22  
> 执行者：Codex

## 目标

让未登记常用目录时的“打开项目目录”和“整理项目目录”可以直接指向当前 Jarvis Lite 项目根目录。

## 约束

- 用户通过 `/dir-add 项目 路径` 登记的目录仍优先于 fallback。
- 不真实启动外部应用，只沿用现有目录打开记录。
- 不移动或删除文件，只沿用现有整理预览。
- 不新增自研目录索引系统，复用 `ProjectPaths.root`。

## 实施步骤

1. 新增两个 Agent 测试：
   - `test_natural_language_open_project_uses_known_project_directory`
   - `test_natural_language_organize_project_uses_known_project_directory`
2. 先运行新增测试，确认未实现时失败。
3. 在 `JarvisAgent._known_directory()` 中增加项目根目录 fallback。
4. 运行 targeted tests、`tests.test_agent`、全量测试、桌面 smoke 和 `git diff --check`。
5. 更新 README、进度文档、方案文档、验证记录和本地 `.codex` 留痕。
