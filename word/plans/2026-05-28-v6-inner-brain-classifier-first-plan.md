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
- 读取当前资料、读取编号资料、查看/导入编号最近文件、查看编号搜索结果、查看/执行编号经验建议。
- 给当前资料/结果打标签、给编号资料/搜索结果打标签、读取标签资料、标签组批量打标签预览、读取编号标签历史影响资料。

这些输入命中后返回 `source=seed_sample` 或 `source=runtime_sample`，不再显示 `legacy_rule`。

## 编号槽位迁移约定

第一批复杂槽位动作已迁移为“样本签名 + 槽位抽取”：

- 样本负责识别语义，例如 `读取第{index}份资料`、`查看第{index}条结果`、`执行第{index}条建议`。
- 签名归一化只把编号位置标准化为 `{index}`，让 `第一`、`第二`、`2` 等表达命中同一个样本。
- 槽位抽取只负责产出 `result_index`，不负责决定意图。
- `JarvisAgent` 继续复用既有执行函数，例如 `read_numbered_recent_document`、`read_numbered_search_result` 和 `prepare_numbered_advice_suggestion_execution`。

这一步保证“查看第二条结果”这类表达不再靠 legacy parser 判定自然语言主意图，同时保留编号这种结构化信息的可审计抽取。

## 标签槽位迁移约定

第二批复杂槽位动作已迁移为“样本签名 + 标签槽位抽取”：

- `给这个资料打标签 项目 Python` -> `document.tag_recent`，抽取 `tags=("项目", "Python")`。
- `给第二份资料打标签 项目 Python` -> `document.tag_numbered_recent`，抽取 `result_index=2` 和 `tags`。
- `给第二条结果打标签 运行环境` -> `search_result.tag_numbered`，抽取 `result_index=2` 和 `tags`。
- `给项目标签资料都打标签 归档` -> `tag_group.preview_tagging`，抽取 `alias="项目"` 和 `tags`。
- `读取项目标签资料` -> `tag_group.read`，抽取 `alias="项目"`。
- `读取第一条标签历史资料` -> `tag_history.read_numbered`，抽取 `result_index=1`。

显式文件名或路径型标签命令，例如 `给 note.txt 打标签 项目`，本阶段仍保留为 `legacy_fallback`，因为它属于文件名/路径槽位迁移，不和标签组、最近上下文槽位混在一起处理。

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

- 把显式文件名/路径导入、目录别名等剩余复杂槽位能力逐步迁移出 `legacy_fallback`。
- 将搜索结果写入最近上下文，支持“查一下并总结”这类 SearchRouter + LLMRouter 组合流程。
- 优化中置信澄清文案，使用户能通过自然语言补齐缺失槽位。
