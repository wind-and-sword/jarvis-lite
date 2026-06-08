# v6 高频 legacy 别名迁移计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

继续把仍会命中 `legacy_fallback` 的高频自然语言别名迁移为 InnerBrain seed 样本，保持样本分类器优先。

## 范围

- 问候短句和英文问候。
- 助手身份与能力询问同义表达。
- 最近上下文、知识库、最近文件、日报、更新、经验状态的同义表达。

## 执行

1. 写 RED 测试，断言这些表达返回 `source=seed_sample`。
2. 在 `seed_training_samples()` 中补充 seed 样本，优先复用已有 intent 和 command slot。
3. 运行目标测试和 `tests.test_inner_brain tests.test_agent`。
4. 更新 v6 文档与验证记录，提交本轮变更，不 push。
