# v6 多轮澄清 query 槽位执行计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

把多轮澄清从文件路径和桌面快捷方式对象扩展到联网搜索 query，让“帮我查一下”之后直接回复“Python 版本”可以继续执行搜索。

## 范围

- 覆盖 `web.search missing=query`。
- 覆盖 `web.search_summarize missing=query`。
- 更新澄清提示，使 query 显示为“查询关键词”并给出对应补全命令。
- 不改变 SearchRouter/LLMRouter 分工：SearchRouter 获取来源，LLMRouter 只在 summary 场景基于来源总结。

## 执行

1. 写 RED 测试：
   - `web.search missing=query` 后下一句 query 调用 fake SearchRouter。
   - `web.search_summarize missing=query` 后下一句 query 先搜索，再调用 fake LLM 总结。
   - 澄清提示包含“查询关键词”和 `/search 关键词`。
2. 修复 `_sample_to_natural_language_intent()` 对 `web.search` 和 `web.search_summarize` 的 slots.query 使用。
3. 更新澄清提示 action hint 和 missing label。
4. 运行目标测试、相关回归、全量测试和静态检查。
5. 更新正式文档和验证记录，本地提交，不 push。
