# InnerBrain Teach Command Implementation Plan

> 日期：2026-05-28
> 执行者：Codex
> 目标：新增口语化教学入口，让用户无需理解 intent/slot 也能把自然语言短句映射到已知命令。

## 方案

推荐方案：新增 `/inner-brain-teach 文本 => /命令`，并支持“以后我说“文本”就是 /命令”“把“文本”记成 /命令”。内部复用 `save_labeled_runtime_training_sample()`，把目标命令转换成 `intent + command slot` 后写入 runtime JSONL。

取舍：

- 相比继续扩展 `/inner-brain-label`，教学入口更符合普通用户心智。
- 相比做完整 UI 纠错向导，本轮 CLI/面板输入都可直接复用，验证成本低。
- 相比让 LLM 自动猜标签，本轮先要求用户明确给出目标命令，样本质量更稳定。

## 任务 1：失败测试

- [x] Agent help 列出 `/inner-brain-teach`。
- [x] `/inner-brain-teach 可以看看资料库吗 => /kb` 保存 runtime 样本并刷新当前 Agent。
- [x] `以后我说“可以看看资料库吗”就是 /kb` 保存后跟进输入可执行 `/kb`。
- [x] 教学动作本身不执行目标命令。
- [x] 未知目标命令不写入样本。

## 任务 2：实现

- [x] 增加可教学命令到 intent 的映射。
- [x] 增加 slash 教学命令解析。
- [x] 增加口语教学句式解析。
- [x] 复用人工标注保存与反馈格式。

## 任务 3：文档与验证

- [x] 更新 README、项目计划、今日进度和验证记录。
- [x] 更新 `.codex/testing.md`、`.codex/review-report.md`、`.codex/operations-log.md`。
- [x] 运行专项、全量、smoke、diff/link/sensitive 验证。
- [x] 提交并推送。
