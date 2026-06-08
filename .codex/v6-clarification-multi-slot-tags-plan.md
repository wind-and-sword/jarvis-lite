# v6 多轮澄清编号 + 标签补槽执行计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

让 InnerBrain 多轮澄清支持用户在一句回复里同时补齐编号和标签，例如“第二份 项目 Python”。

## 范围

- 覆盖 `document.tag_numbered_recent missing=result_index,tags`。
- 确保编号词只进入 `result_index`，不污染 `tags`。
- 优化澄清提示，把 `result_index`/`tags` 展示为“编号”/“标签”，并给出一句式补槽示例。
- 不新增独立执行层，补齐后仍复用 `NaturalLanguageIntent("tag_numbered_recent_document")`。

## 执行

1. 写 RED 测试：runtime 样本“给那份资料打标签”缺编号和标签，用户下一句“第二份 项目 Python”应只给第二份资料追加“项目、Python”。
2. 修复 `_clarification_slots_from_reply()` 的多槽位标签清理逻辑。
3. 补 Agent 澄清提示。
4. 运行目标测试、`tests.test_inner_brain tests.test_agent`、全量测试和静态检查。
5. 更新正式文档和验证记录，若产生用户可见版本则打 `0.1.9` 安装包并本地提交。
