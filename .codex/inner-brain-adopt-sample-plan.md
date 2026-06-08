# InnerBrain Adopt Sample Implementation Plan

> 日期：2026-05-28
> 执行者：Codex
> 目标：把 InnerBrain preview 的正确识别结果沉淀为运行态训练样本，形成“预览 -> 采纳 -> 复用”的闭环。

## 任务 1：样本写入 API

- [ ] 在 `tests/test_inner_brain.py` 增加失败测试，覆盖保存 runtime JSONL、重复样本不重复写、unknown 不保存。
- [ ] RED 验证。
- [ ] 在 `src/jarvis_lite/inner_brain.py` 增加样本写入函数和保存结果数据结构。
- [ ] GREEN 验证。

## 任务 2：Agent 命令

- [ ] 在 `tests/test_agent.py` 增加失败测试，覆盖 `/inner-brain-adopt 文本`、`/help`、采纳桌面删除表达不执行删除、保存后 status 刷新。
- [ ] RED 验证。
- [ ] 在 `JarvisAgent` 增加命令路由、日志和输出文案。
- [ ] GREEN 验证。

## 任务 3：文档与验证

- [ ] 更新 README、项目计划、今日进度和验证记录。
- [ ] 运行专项、全量、smoke、diff/link/sensitive 验证。
- [ ] 更新 `.codex/testing.md` 和 `.codex/review-report.md`。
- [ ] 提交并按用户既有要求推送。
