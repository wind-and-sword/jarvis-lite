# 0.25.0 桌面候选模板状态同步计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

让桌面面板在执行 `/inner-brain-candidates` 后，根据实际候选数量同步模板控件状态，减少无效编号和误操作。

## 设计

- 初始仍允许手动填入模板，保留 0.24.0 的显式输入能力。
- 当 `/inner-brain-candidates` 返回空状态时：
  - 状态文本显示 `候选模板：暂无候选`。
  - “填教学”“填标注”禁用。
  - 候选编号上限收紧为 1。
- 当 `/inner-brain-candidates` 返回 N 条候选时：
  - 状态文本显示 `候选模板：N 条候选`。
  - 模板按钮启用。
  - 候选编号上限收紧为 N，避免填入不存在的编号。
- 同步只发生在候选列表响应后，不改变后端候选统计、排序、teach 或 label 行为。

## TDD 步骤

1. 在 `tests/test_desktop_widgets.py` 新增空候选禁用模板测试。
2. 新增有候选时同步候选数量、编号上限和填充编号测试。
3. 将 `tests/test_project_metadata.py` 的 `RELEASE_VERSION` 提升到 `0.25.0`。
4. 跑目标测试确认 RED。
5. 在 `AssistantPanel` 中新增候选模板状态 label、测试辅助方法和同步逻辑。
6. 更新版本元数据、README、PROJECT-PLAN、方案索引、进度与验证记录。
7. 跑目标 GREEN、相邻回归、全量、桌面 smoke、安装包 smoke、静态检查。
8. 提交并推送 `0.25.0`。
