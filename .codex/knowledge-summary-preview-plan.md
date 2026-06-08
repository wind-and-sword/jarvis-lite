# 知识库摘要长预览截断计划

> 日期：2026-05-25  
> 执行者：Codex

## 目标

让 `/kb-summary` 在资料首行很长时仍保持可扫读，摘要预览只展示固定长度并追加省略标记。

## 范围

- 更新 `summarize_knowledge_base()` 的预览格式。
- 不改变 `build_knowledge_index()`、`search_data()`、`/ask` 和 `/read`。
- 不引入 LLM 或额外依赖。

## 验收

- 长预览会被截断，输出不包含超长尾部。
- 短预览保持原样。
- 全量测试、桌面 smoke 和空白检查通过。
