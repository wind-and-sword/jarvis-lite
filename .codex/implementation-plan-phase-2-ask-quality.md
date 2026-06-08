# 阶段 2 /ask 排序与摘要质量实现计划

> 日期：2026-05-19
> 执行者：Codex

## 目标

在不引入第三方依赖、不改变 `/ask` 命令调用方式的前提下，让知识库回答优先返回更具体的资料，并让回答格式更容易阅读。

## 接口契约

- `search_data(paths, query, limit=3)` 继续返回 `list[DataMatch]`。
- `answer_from_data(paths, question)` 继续返回字符串；无命中时仍返回空字符串。
- `/ask 问题` 与普通问题继续复用 `answer_from_data`。

## 实施步骤

1. 在 `tests/test_knowledge.py` 中新增排序测试：当泛化资料和包含版本号的具体资料得分接近时，包含具体版本号的资料应优先。
2. 运行该单测，确认当前实现按路径排序导致失败。
3. 在 `tests/test_knowledge.py` 中新增回答摘要格式测试：有命中时输出命中数量摘要和编号。
4. 运行该单测，确认当前实现缺少摘要头导致失败。
5. 修改 `src/jarvis_lite/knowledge.py`：为包含数字或版本号的查询词增加权重，保持其他关键词规则稳定。
6. 修改 `answer_from_data`：增加命中数量摘要和编号，保留 `根据 data/...` 来源格式。
7. 运行知识库相关单测和全量 `unittest`。
8. 更新 `.codex/testing.md`、`verification.md`、阶段 2 进度文档和 README 当前状态。

## 风险

- 规则式检索仍不是语义检索，只能改善明确关键词、版本号、编号类问题的排序。
- 输出格式新增摘要头，已有调用方只依赖纯文本，不涉及结构化解析。
