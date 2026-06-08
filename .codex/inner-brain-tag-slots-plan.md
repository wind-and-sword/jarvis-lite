# InnerBrain 标签槽位迁移计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

把标签相关高频自然语言迁移出 `legacy_fallback`，包括：

- 给当前资料或当前结果打标签。
- 给第几份资料打标签。
- 给第几条搜索结果打标签。
- 给某个标签分组的资料批量追加标签预览。
- 读取某个标签分组资料。
- 读取第几条批量标签历史影响资料。

## 设计

- `InnerBrainTrainingSample` 继续作为主识别入口。
- 标签类 signature 将可变的标签名归一为 `{tags}`，将标签分组归一为 `{tag}`，将编号归一为 `{index}`。
- 解析函数只抽结构化槽位：`tags`、`alias`、`result_index`。
- 显式文件名打标签，例如 `给 note.txt 打标签 项目`，本阶段保留为 `legacy_fallback`，因为它包含文件路径/文件名槽位。
- `JarvisAgent` 执行层不新增重复逻辑，复用现有自然语言意图处理函数。

## TDD 步骤

1. RED：新增 `test_tag_intents_use_sample_classifier_slots`，确认标签类样例不再允许返回 `legacy.*`。
2. GREEN：新增标签 seed 样本、签名归一化、槽位抽取和 `NaturalLanguageIntent` 映射。
3. 回归：运行 `tests.test_inner_brain` 和标签相关 `tests.test_agent`。
4. 收尾：运行全量 `unittest`、桌面 smoke、preview smoke、Markdown 链接检查和敏感信息差异扫描。

## 验收

- 标签类迁移样例返回 `source=seed_sample`。
- `tags`、`alias`、`result_index` 均进入 `InnerBrainResult.slots`。
- 显式文件名标签命令仍走 `legacy_fallback`。
- 全量本地测试通过。
