# 0.2.0 InnerBrain 多轮澄清 v1 收口计划

> 日期：2026-05-29
> 执行者：Codex

## 里程碑定义

`0.2.0` 定义为：InnerBrain 样本分类器优先 + LLM/Search 外脑互补 + 多轮澄清 v1 可安装闭环。

本阶段不追求“理解所有自然语言”，而是把当前已支持 intent 的主要缺槽类型收口成稳定用户体验：看得懂提示、下一句能补齐、补齐后复用 Agent 现有执行链路。

## 收口范围

- `document.read_path missing=path`
- `document.read_numbered_recent missing=result_index`
- `document.tag_recent missing=tags`
- `tag_group.preview_tagging missing=alias,tags`
- `experience.search missing=query`
- `experience.advice missing=query`

## 执行规则

- 先写 RED 测试，再改实现。
- 正则只用于已知 intent 后的槽位清理，不用于决定自然语言主意图。
- 不新增执行层；补齐后仍走 `NaturalLanguageIntent` 和 `JarvisAgent`。
- 产物为 `JarvisLiteSetup-0.2.0.exe`，本地提交并 push。
