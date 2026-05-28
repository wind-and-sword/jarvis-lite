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
- 显式文件读取、显式文件/目录导入知识库。
- 打开盘符、打开/整理常用目录、打开/整理最近目录。
- 经验记录、经验搜索、经验建议。
- 联网搜索并总结组合入口。

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

## 文件路径槽位迁移约定

第三批复杂槽位动作将显式文件/路径类读写迁移为“样本签名 + 路径槽位抽取”：

- `读取 manual.md` -> `document.read_path`，抽取 `path="manual.md"`，映射为 `/read "manual.md"`。
- `查看 data/manual.txt` -> `document.read_path`，抽取时去掉 `data/` 前缀，映射为 `/read "manual.txt"`。
- `把 "C:/work/outside natural.md" 导入知识库` -> `knowledge.import`，抽取 `source="C:/work/outside natural.md"`，映射为 `/import "C:/work/outside natural.md"`。
- `导入 E:/docs/manual.pdf 到资料库` -> `knowledge.import`，抽取 `source`，映射为 `/import`。

样本负责识别“读取资料路径”和“导入知识库”语义；路径解析只负责保留文件名、相对路径、绝对路径和带空格的引号路径。编号最近文件导入仍由 `recent_file.import_numbered` 处理，避免被泛化导入样本误吞。

## 目录槽位迁移约定

第四批复杂槽位动作将目录相关自然语言迁移为样本分类：

- `打开D盘` -> `directory.open_drive`，抽取 `alias="D盘"` 和 `path="D:/"`。
- `打开项目目录` -> `directory.open_alias`，抽取 `alias="项目"`。
- `整理项目目录` -> `directory.organize_alias`，抽取 `alias="项目"`。
- `打开这个目录` -> `directory.open_recent`。
- `整理这个目录` -> `directory.organize_recent`。

目录解析只抽取别名、盘符和最近目录引用，不负责判定“打开/整理”的主语义。`JarvisAgent` 继续复用既有常用目录、项目目录、桌面/下载目录和最近目录执行链路。

## 经验槽位迁移约定

第五批复杂槽位动作将经验记忆相关表达迁移为样本分类：

- `记住这个经验：导入资料后先打标签` -> `experience.record`，抽取 `experience`，映射为 `/experience ...`。
- `搜索经验 导入`、`经验查询 日报` -> `experience.search`，抽取 `query`，映射为 `/experience-search ...`。
- `我该怎么导入资料`、`导入资料有什么建议` -> `experience.advice`，抽取 `query`，映射为 `/experience-advice ...`。

这些动作仍由现有经验记忆模块执行；InnerBrain 只负责把用户自然语言变成结构化 intent/slot。

## 联网搜索总结槽位迁移约定

第六批组合动作将“查一下并总结”迁移为样本分类：

- `联网查一下 Python 版本并总结` -> `web.search_summarize`，抽取 `query="Python 版本"`，映射为 `/search-summary Python 版本`。
- 普通 `联网查一下 Python 版本` 仍然是 `web.search`，只执行搜索并展示来源，不自动调用 LLM。

`/search-summary` 由 `JarvisAgent` 先调用 SearchRouter，把来源、URL 和摘要写入最近联网搜索上下文，再把该上下文交给 LLMRouter 总结。LLM 只基于 Agent 提供的来源表达总结，不自由浏览。

教学样本仍使用同一个 intent：`/inner-brain-teach 查版本 => /search-summary Python 版本` 会保存为 `web.search_summarize`，并通过 `command=/search-summary Python 版本` 复现用户指定命令；这避免 seed 样本和 runtime 样本出现 `web.search_summary`/`web.search_summarize` 两套名称。

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

- 继续把显式文件名标签、更多桌面快捷方式表达等剩余复杂槽位能力逐步迁移出 `legacy_fallback`。
- 扩展联网搜索后的来源处理，例如按编号打开来源、保存摘要或导入知识库。
- 优化中置信澄清文案，使用户能通过自然语言补齐缺失槽位。
