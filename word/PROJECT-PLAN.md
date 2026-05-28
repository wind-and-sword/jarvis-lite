# Jarvis Lite 当前项目方案

> 日期：2026-05-28
> 执行者：Codex
> 说明：本文是当前项目方案入口。历史方案版本保存在 `word/plans/`。

## 项目定位

Jarvis Lite 是一个本地优先的个人 PC Agent，目标是让 AI 逐步理解用户的文件、知识库、记忆、最近上下文和桌面工作流，并通过命令行和桌面入口帮助用户完成真实任务。

它当前不是多端平台，也不是纯聊天机器人。当前重点是把 PC 上的本地 Agent 主干做稳，再引入本地内脑增强自然语言理解和决策，让 LLM 作为外脑增强复杂理解、总结、规划和自然表达能力，并把联网搜索作为由 Agent 控制的外部资料获取工具接入。

## 当前路线

```text
PC Agent 稳定
  -> 引入本地内脑 InnerBrain
  -> 接入并打磨 LLM 外脑
  -> 接入 Agent 控制的联网搜索工具
  -> 打磨 PC + 内脑 + 外脑核心闭环
  -> 再评估手机、手表、车机、AR 眼镜等多端入口
```

## 当前主干

```text
用户输入
  -> 命令 / 身份 / 本地自然语言意图 / 知识库问答优先
  -> InnerBrain 输出 intent / slots / confidence / missing
  -> 高置信度进入 JarvisAgent；中置信度追问；低置信度进入 LLMRouter
  -> 需要当前互联网资料时由 JarvisAgent 调用 SearchRouter
  -> LLMIntent(command / answer / clarify / no_action)
  -> JarvisAgent
  -> 长期记忆 / 经验记忆 / 知识库 / 最近上下文
  -> 文件、目录、知识库、日报、更新、桌面入口等工具
  -> 结果反馈 / 下一步建议 / 确认执行
```

## 已完成基础

- 命令行助手和 PySide6 桌面助手入口。
- 长期记忆、经验记忆和个人知识库。
- Markdown、txt、PDF、JSON 聊天记录和资料目录导入。
- 知识库问答、摘要、标签、按标签读取资料组。
- 最近资料、最近文件、最近目录、最近搜索结果、最近建议和批量标签历史。
- InnerBrain 本地内脑：新增结构化 `InnerBrainResult`，包含 `intent`、`slots`、`confidence`、`missing`、`source`、`reason` 和策略；当前已迁移为 seed/runtime 样本分类器优先，既有自然语言规则只作为 `legacy_fallback` 迁移期兼容兜底。
- InnerBrain 可观察与样本闭环：`/inner-brain-status` 查看样本数量、阈值和训练目录；`/inner-brain-preview 文本` 只预览识别结果，不执行命令或本地动作；`/inner-brain-adopt 文本` 将正确识别结果保存为运行态 JSONL 样本；`/inner-brain-label 文本 => intent [slot=value ...]` 可人工标注 unknown 或误识别样本；`/inner-brain-teach 文本 => /命令` 和“以后我说“文本”就是 /命令”可把用户口语短句教学为已知命令。
- 本地自然语言意图层，可处理常见中文表达，包括问候、助手身份/能力询问、最近上下文、最近文件、显式文件读取/导入、显式文件打标签、读取编号资料、查看/导入编号最近文件、查看编号搜索结果、查看/执行编号建议、当前资料/结果打标签、编号资料/搜索结果打标签、标签组读取与批量标签预览、知识库、常用目录打开/整理、最近目录打开/整理、日报、更新、经验记录/搜索/建议、确认/取消执行、联网搜索、联网搜索后续来源处理和明确点名的桌面 `.lnk` 快捷方式删除；InnerBrain 高置信度命中后仍由 `JarvisAgent` 执行。
- LLM 外脑 Router 第一版：provider-neutral 配置、`config/llm.local.json` 本地配置文件、fake provider 测试路径、OpenAI Responses API adapter、OpenAI-compatible 端点、完整 `/v1/responses` URL 归一化、provider 与 Agent 双层命令白名单、LLM fallback 近期上下文与最近搜索结果、`/llm-enable` 外脑启用入口、`/llm-context-preview`、`/llm-smoke` 配置验证、token usage 日志、`/llm-status` API key/网络调用诊断、`/llm-usage` 本地汇总和 `/llm-config-example` 配置模板。
- 联网搜索方案已明确为 SearchRouter 工具能力：搜索负责获取当前网页来源和摘要，LLM 外脑负责在 Agent 提供来源后做总结、比较和自然表达；两者互补，均不绕过 `JarvisAgent`。当前 `/search` 会把联网搜索结果写入最近上下文和 LLM context，`/search-summary` 与“联网查一下...并总结”会先搜索再把来源交给 LLM 总结；`/search-open`、`/search-compare`、`/search-save-summary` 和 `/search-import-summary` 负责最近联网搜索的来源查看、来源比较、摘要保存和知识库导入。
- 桌面小助手、助手面板、托盘、快捷命令、主题、尺寸、开机启动和更新入口。
- 本地 `unittest` 验证体系。

## 下一阶段

当前已经进入并落地第一批：

> InnerBrain 样本分类器优先 + LLM 外脑接入第一版 + Agent 联网搜索第一版。

后续目标：

- 继续扩展 InnerBrain seed/runtime 样本，把用户真实日志和现有命令能力持续沉淀为 `text -> intent -> slots` 数据。
- 继续评估字符 n-gram、轻量 embedding 相似度或小型分类器，不从零训练通用 LLM。
- 继续打磨缺失槽位的自然语言补全、多轮澄清状态和更细的用户纠错样本沉淀。
- 扩展 Gemini 和 Qwen provider adapter。
- 继续打磨真实 provider 的兼容端点体验、运行态本地配置体验和用量观察能力。
- 继续打磨 LLM 结构化意图提示词、命令参数澄清、provider 错误可读化和失败兜底。
- 让 LLM 生成更稳定的命令建议、资料总结、任务拆解和澄清问题。
- 扩展联网搜索结果后续动作，例如按编号打开来源、保存摘要、对比多个来源和沉淀为知识库资料。
- 持续把用户真实日志里的自然语言缺口沉淀为内脑训练样本和回归测试，再交给 LLM 处理更开放的问题。
- 继续由 `JarvisAgent` 承接工具调用、上下文更新和结果反馈。

## 暂缓方向

以下方向在 PC + 内脑 + LLM 核心闭环稳定前暂缓：

- 手机端。
- 手表健康数据。
- 车机入口。
- AR 眼镜入口。
- 跨设备同步。

## 方案版本

- [v1：整体方案与路线图](plans/2026-05-18-v1-overall-plan.md)
- [v2：个人设备级 Agent 融合方案](plans/2026-05-22-v2-personal-device-agent-plan.md)
- [v3：PC Agent 与 LLM 外脑优先方案](plans/2026-05-27-v3-pc-agent-llm-first-plan.md)
- [v4：内脑与外脑双脑架构方案](plans/2026-05-28-v4-inner-brain-llm-dual-brain-plan.md)
- [v5：Agent 联网搜索与 LLM 外脑互补方案](plans/2026-05-28-v5-agent-web-search-llm-complement-plan.md)
- [v6：InnerBrain 样本分类器优先方案](plans/2026-05-28-v6-inner-brain-classifier-first-plan.md)
