# Jarvis Lite v6：InnerBrain 样本分类器优先方案

> 日期：2026-05-28
> 执行者：Codex
> 说明：本文承接 v4 双脑架构和 v5 搜索互补方案，进一步明确 InnerBrain 不再以正则作为自然语言主识别路径。

## 核心结论

InnerBrain 的主路径改为本地样本分类器优先：

```text
用户自然语言
  -> InnerBrain seed/runtime 样本分类器
  -> intent / slots / confidence / missing
  -> 高置信：交给 JarvisAgent 执行
  -> 中置信：澄清或确认
  -> 低置信：进入本地知识库问答或 LLM fallback
  -> legacy_fallback：仅迁移期兼容复杂槽位规则
```

旧 `parse_natural_language_intent()` 不再作为高频自然语言主入口。它只保留两类用途：

- 迁移期兼容兜底：还没有迁移为样本/槽位抽取器的复杂本地动作继续可用，结果标记为 `source=legacy_fallback`。
- 槽位抽取辅助：文件名、编号、标签、桌面快捷方式名称、联网搜索 query 等结构化信息可以继续用明确的解析函数抽取。

## 已迁移的高频意图

第一批 seed 样本覆盖：

- 问候、助手身份、能力询问。
- 最近上下文、最近文件、批量标签历史。
- 知识库摘要、知识库状态、常用目录。
- 日报、检查更新、下载更新。
- 经验记忆、确认执行、取消执行。
- LLM 外脑启用、联网搜索。
- 桌面 `.lnk` 快捷方式删除。

这些输入命中后返回 `source=seed_sample` 或 `source=runtime_sample`，不再显示 `legacy_rule`。

## 当前 Agent 决策规则

- `confidence >= 0.78`：样本分类器高置信，生成 `NaturalLanguageIntent` 后由 `JarvisAgent` 执行。
- `0.58 <= confidence < 0.78`：如果 legacy fallback 能识别更具体的旧规则动作，先走 `legacy_fallback` 保持兼容；否则进入澄清。
- `< 0.58`：本地内脑低置信，交给本地知识库问答或 LLM fallback。

这个规则避免“查看最近文件”这类泛化样本误吞“查看第一份最近文件”这种更具体的编号槽位动作。

## 样本闭环

用户不需要写正则：

- `/inner-brain-adopt 文本`：采纳当前正确识别结果。
- `/inner-brain-label 文本 => intent [slot=value ...]`：人工修正 unknown 或误识别。
- `/inner-brain-teach 文本 => /命令` 或“以后我说“文本”就是 /命令”：把口语短句绑定到已知命令。

长期方向是继续把真实日志中的表达沉淀为 `text -> intent -> slots` 数据，再评估字符 n-gram、embedding 或小型分类器替换当前轻量相似度实现。

## 后续迁移重点

- 把标签、读取编号资料、读取编号最近文件、经验建议等复杂槽位能力逐步迁移出 `legacy_fallback`。
- 将搜索结果写入最近上下文，支持“查一下并总结”这类 SearchRouter + LLMRouter 组合流程。
- 优化中置信澄清文案，使用户能通过自然语言补齐缺失槽位。
