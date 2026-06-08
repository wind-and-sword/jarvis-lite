# InnerBrain 编号槽位迁移计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

把第一批编号/对象槽位动作从 `legacy_fallback` 迁移到 `seed_sample` 样本分类器主路径：

- 读取这个资料。
- 读取第几份资料。
- 查看/读取第几份最近文件。
- 导入第几份最近文件到知识库。
- 查看/读取第几条搜索结果。
- 查看/读取第几条建议。
- 执行/运行第几条建议。

## 设计

- 自然语言主识别仍由 `InnerBrainTrainingSample` 和相似度分类完成。
- 新增 intent-specific signature，把 `第一`、`第二`、`2` 等编号归一为 `{index}`，使样本能覆盖编号变体。
- 正则只用于结构化槽位抽取：从已命中的编号动作中抽取 `result_index`。
- 不改 `JarvisAgent` 执行层，继续复用现有 `NaturalLanguageIntent` 名称和处理函数。
- 未迁移的标签、路径、批量标签历史等复杂动作继续保留 `legacy_fallback`。

## TDD 步骤

1. RED：新增 `tests.test_inner_brain.InnerBrainTests.test_numbered_object_intents_use_sample_classifier_slots`，确认第一批动作不再允许返回 `legacy_fallback`。
2. GREEN：扩展 seed 样本、签名归一化、槽位抽取和 `NaturalLanguageIntent` 映射。
3. 回归：运行 `tests.test_inner_brain`、`tests.test_agent` 和全量 `unittest discover`。
4. Smoke：运行桌面 smoke、`/inner-brain-status` 和 `/inner-brain-preview 读取第二份资料`。

## 验收

- 第一批编号动作返回 `source=seed_sample`。
- 编号动作写入 `slots["result_index"]`，并映射到对应 `NaturalLanguageIntent.result_index`。
- `给 note.txt 打标签 项目` 这类尚未迁移动作仍返回 `legacy_fallback`。
- 全量本地测试通过。
