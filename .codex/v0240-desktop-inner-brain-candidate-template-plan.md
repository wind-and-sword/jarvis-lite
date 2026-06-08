# 0.24.0 桌面 InnerBrain 候选模板填充计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

让桌面面板在查看 InnerBrain 候选后，可以通过候选编号把 teach 或 label 模板填入输入框，由用户显式补全并发送。

## 设计

- 在 `AssistantPanel` 增加候选编号 `QSpinBox`，范围 1-20，对齐运行态候选统计最多保留 20 条的约束。
- 增加“填教学”按钮，填入 `/inner-brain-teach-candidate N => `。
- 增加“填标注”按钮，填入 `/inner-brain-label-candidate N => intent slot=value`。
- 填充动作只修改输入框，不调用 `submit_text()`，不写 transcript，不改变路由状态。
- 不新增后端命令、不新增自然语言正则、不自动训练或自动标注。

## TDD 步骤

1. 在 `tests/test_desktop_widgets.py` 新增面板模板控件暴露测试。
2. 新增“填教学”按钮只填输入框、不提交测试。
3. 新增“填标注”按钮按候选编号填入 label 模板测试。
4. 将 `tests/test_project_metadata.py` 的 `RELEASE_VERSION` 提升为 `0.24.0`。
5. 跑目标测试确认 RED。
6. 修改 `src/jarvis_lite/desktop/widgets.py` 和版本元数据实现 GREEN。
7. 补齐 README、PROJECT-PLAN、方案索引、进度和验证记录。
8. 跑相邻回归、全量测试、桌面 smoke、安装包 smoke、静态检查、提交并推送。
