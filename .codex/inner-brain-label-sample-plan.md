# InnerBrain Label Sample Implementation Plan

> 日期：2026-05-28
> 执行者：Codex
> 目标：新增人工标注/纠错入口，让 `unknown` 或误识别表达也能沉淀为 InnerBrain runtime 样本。

## 任务 1：InnerBrain 标注保存 API

- [x] 在 `tests/test_inner_brain.py` 增加失败测试，覆盖人工 label 写入、列表 slot 保存和重载执行。
- [x] RED 验证。
- [x] 在 `inner_brain.py` 增加 `save_labeled_runtime_training_sample()`，复用 runtime JSONL 写入和去重逻辑。
- [x] GREEN 验证。

## 任务 2：Agent 命令

- [x] 在 `tests/test_agent.py` 增加失败测试，覆盖 `/inner-brain-label 文本 => intent slot=value...`、help、无效格式、保存后当前 Agent 立即生效、保存不执行本地动作。
- [x] RED 验证。
- [x] 在 `JarvisAgent` 增加命令解析、slot 解析、保存反馈和刷新。
- [x] GREEN 验证。

## 任务 3：文档与验证

- [x] 更新 README、项目计划、今日进度和验证记录。
- [x] 运行专项、全量、smoke、diff/link/sensitive 验证。
- [x] 更新 `.codex/testing.md`、`.codex/review-report.md`、`.codex/operations-log.md`。
- [x] 提交并推送。
