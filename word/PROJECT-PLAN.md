# Jarvis Lite 当前项目方案

> 日期：2026-05-29
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
  -> 记录最近路由决策
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
- InnerBrain 多轮澄清 v1：当本地内脑已识别 intent 但缺少 `source`、`items`、`path`、`query`、`result_index`、`tags`、`alias`、`experience` 等槽位时，`JarvisAgent` 会保留本轮澄清状态；用户下一句可直接补充文件路径、桌面快捷方式名称、联网搜索关键词、经验搜索/建议关键词、目录别名、经验内容、当前资料标签，或用“第二份 项目 Python”“项目 归档”这类一句式回复补齐组合槽位，Agent 补齐后继续执行原请求，用户也可用“取消补充”等表达取消。
- InnerBrain 可观察与样本闭环：`/inner-brain-status` 查看样本数量、阈值和训练目录；`/inner-brain-preview 文本` 只预览识别结果，不执行命令或本地动作；`/inner-brain-adopt 文本` 将正确识别结果保存为运行态 JSONL 样本；`/inner-brain-label 文本 => intent [slot=value ...]` 可人工标注 unknown 或误识别样本；`/inner-brain-teach 文本 => /命令` 和“以后我说“文本”就是 /命令”可把用户口语短句教学为已知命令；`/inner-brain-candidates` 会把 fallback/澄清候选写入本地运行态统计，按出现次数优先展示，显式 teach、label 或 adopt 后移除对应候选。
- 本地自然语言意图层，可处理常见中文表达，包括问候、助手身份/能力询问、最近上下文、最近文件、显式文件读取/导入、显式文件打标签、读取编号资料、查看/导入编号最近文件、查看编号搜索结果、查看/执行编号建议、当前资料/结果打标签、编号资料/搜索结果打标签、标签组读取与批量标签预览、知识库、常用目录打开/整理、最近目录打开/整理、日报、更新、经验记录/搜索/建议、确认/取消执行、联网搜索、联网搜索后续来源处理和明确点名的桌面 `.lnk` 快捷方式删除；InnerBrain 高置信度命中后仍由 `JarvisAgent` 执行。
- LLM 外脑 Router 第一版：provider-neutral 配置、`config/llm.local.json` 本地配置文件、fake provider 测试路径、OpenAI Responses API adapter、OpenAI-compatible 端点、`qwen`/`gemini` provider alias、完整 `/v1/responses` URL 归一化、provider 与 Agent 双层命令白名单、LLM fallback 近期上下文与最近搜索结果、LLM `clarify` 多轮澄清续聊、LLM 澄清状态运行态恢复、LLM 澄清轮数限制和过期清理、`/llm-config-init` 本地配置草稿生成、`/llm-config-set` 本地配置写入、`/llm-config-check` 本地配置只读检查、`/llm-enable` 外脑启用入口、`/llm-context-preview`、`/llm-smoke` 运行时配置验证、token usage 日志、`/llm-status` API key/网络调用诊断、`/llm-usage` 本地汇总和 `/llm-config-example` 配置模板。
- 联网搜索方案已明确为 SearchRouter 工具能力：搜索负责获取当前网页来源和摘要，LLM 外脑负责在 Agent 提供来源后做总结、比较和自然表达；两者互补，均不绕过 `JarvisAgent`。当前 `/search` 会把联网搜索结果写入最近上下文和 LLM context，`/search-summary` 与“联网查一下...并总结”会先搜索再把来源交给 LLM 总结；`/search-open`、`/search-compare`、`/search-save-summary` 和 `/search-import-summary` 负责最近联网搜索的来源查看、来源比较、摘要保存和知识库导入；`/search-config-init` 可生成本地搜索配置草稿，`/search-config-set` 可写入本地搜索配置，`/search-config-check` 可做只读配置检查，`/search-smoke` 可做不写入最近上下文的 provider 连通性测试。
- 桌面小助手、助手面板、托盘、快捷命令、主题、尺寸、开机启动和更新入口；助手面板已提供外脑和联网搜索配置区，可写入、检查和 smoke 测试 provider 配置，写入 API key 时不会把真实 key 显示到 transcript 或会话历史；面板固定展示 LLM 外脑待补充问题、澄清轮次、取消提示、外脑启用状态、最近一次 LLM 调用结果、最近一条用户输入的路由决策和路由选择依据；桌面面板和托盘快捷命令已提供“内脑候选”入口。
- 本地 `unittest` 验证体系。

## 下一阶段

当前已经完成 `0.24.0` 里程碑：

> InnerBrain 样本分类器优先 + LLM 外脑接入第一版 + Agent 联网搜索第一版 + 多轮澄清 v1 可安装闭环 + 外脑 provider 配置闭环 v1 + 运行态配置初始化 v1 + 本地配置检查 v1 + 本地配置写入 v1 + 连通性诊断 v1 + 桌面配置面板 v1 + LLM 外脑多轮澄清 v1 + LLM 澄清状态持久化 v1 + LLM 澄清轮数与过期策略 v1 + 桌面外脑待补充状态 v1 + 桌面外脑运行状态 v1 + 最近路由决策状态 v1 + 路由决策解释详情 v1 + 最近路由历史 v1 + 路由历史详情 v1 + InnerBrain 训练候选 v1 + 候选按编号教学 v1 + 候选按编号标注 v1 + 候选频次排序 v1 + 候选运行态统计 v1 + 桌面内脑候选快捷入口 v1 + 桌面候选训练模板填充 v1。

后续目标：

- 继续扩展 InnerBrain seed/runtime 样本，把用户真实日志和现有命令能力持续沉淀为 `text -> intent -> slots` 数据。
- 继续评估字符 n-gram、轻量 embedding 相似度或小型分类器，不从零训练通用 LLM。
- 继续扩大缺失槽位的自然语言补全范围，把更多 `missing` 场景接入多轮澄清状态，并沉淀更细的用户纠错样本；`0.2.0` 已收口文件路径、编号资料、当前资料标签、标签组+新标签、经验搜索关键词和经验建议关键词。
- 继续打磨真实 provider 的兼容端点体验、运行态本地配置体验和用量观察能力；`0.3.0` 已让 `qwen`/`gemini` 可作为 provider alias 复用 OpenAI-compatible adapter，`0.4.0` 已支持 `/llm-config-init` 与 `/search-config-init` 生成本机配置草稿，`0.5.0` 已支持 `/llm-config-check` 与 `/search-config-check` 做只读配置检查，`0.6.0` 已支持 `/llm-config-set` 与 `/search-config-set` 用显式 `key=value` 写入本机配置，`0.7.0` 已支持 `/llm-smoke` 重新读取当前本地配置和 `/search-smoke` provider 连通性测试，`0.8.0` 已把写入、检查和 smoke 入口放入桌面配置面板，`0.9.0` 已补齐 LLM `clarify` 的多轮续聊，`0.10.0` 已让 LLM 待澄清状态进入运行态上下文，`0.11.0` 已补齐连续澄清轮数和过期清理边界，`0.12.0` 已把 LLM 待补充状态固定展示到桌面面板，`0.13.0` 已把外脑启用状态和最近调用结果固定展示到桌面面板，`0.14.0` 已把最近路由决策固定展示到桌面面板，`0.15.0` 已把路由选择依据固定展示到同一段路由状态，`0.16.0` 已把最近 5 条路由历史固定展示到同一状态区，`0.17.0` 已提供 `/route-history` 路由历史详情并让 `/recent-context` 展示最近路由摘要，`0.18.0` 已提供 `/inner-brain-candidates` 从 fallback/澄清路由中列出人工训练候选，`0.19.0` 已支持 `/inner-brain-teach-candidate 编号 => /命令` 按编号教学候选，`0.20.0` 已支持 `/inner-brain-label-candidate 编号 => intent [slot=value ...]` 按编号标注候选，`0.21.0` 已让候选按出现次数优先排序，`0.22.0` 已把候选出现次数写入本地运行态统计并在训练后移除对应候选，`0.23.0` 已把“内脑候选”加入桌面面板和托盘直接快捷命令，`0.24.0` 已在桌面面板增加候选编号和 teach/label 模板填充入口。
- 如果兼容端点无法覆盖真实使用，再评估 Gemini 和 Qwen 原生 provider adapter。
- 继续打磨 LLM 结构化意图提示词、命令参数澄清、provider 错误可读化和失败兜底。
- 让 LLM 生成更稳定的命令建议、资料总结、任务拆解、澄清问题和澄清后的最终回答。
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
- [v7：外脑 Provider 配置闭环方案](plans/2026-05-29-v7-llm-provider-config-closure-plan.md)
- [v8：运行态配置初始化方案](plans/2026-05-29-v8-runtime-config-init-plan.md)
- [v9：运行态配置检查方案](plans/2026-05-29-v9-runtime-config-check-plan.md)
- [v10：运行态配置写入方案](plans/2026-05-29-v10-runtime-config-set-plan.md)
- [v11：连通性诊断方案](plans/2026-05-29-v11-smoke-diagnostics-plan.md)
- [v12：桌面配置面板方案](plans/2026-05-29-v12-desktop-config-panel-plan.md)
- [v13：LLM 外脑多轮澄清方案](plans/2026-05-29-v13-llm-clarification-plan.md)
- [v14：LLM 外脑澄清状态持久化方案](plans/2026-05-29-v14-llm-clarification-runtime-plan.md)
- [v15：LLM 外脑澄清轮数与过期策略](plans/2026-05-29-v15-llm-clarification-guard-plan.md)
- [v16：桌面外脑待补充状态方案](plans/2026-05-29-v16-desktop-llm-pending-status-plan.md)
- [v17：桌面外脑运行状态方案](plans/2026-05-29-v17-desktop-llm-activity-status-plan.md)
- [v18：最近路由决策状态方案](plans/2026-05-29-v18-route-decision-status-plan.md)
- [v19：路由决策解释详情方案](plans/2026-05-29-v19-route-decision-explanation-plan.md)
- [v20：最近路由历史方案](plans/2026-05-29-v20-route-history-plan.md)
- [v21：路由历史详情方案](plans/2026-05-29-v21-route-history-detail-plan.md)
- [v22：InnerBrain 训练候选方案](plans/2026-05-29-v22-inner-brain-candidates-plan.md)
- [v23：InnerBrain 候选按编号教学方案](plans/2026-06-01-v23-inner-brain-teach-candidate-plan.md)
- [v24：InnerBrain 候选按编号标注方案](plans/2026-06-01-v24-inner-brain-label-candidate-plan.md)
- [v25：InnerBrain 候选频次排序方案](plans/2026-06-01-v25-inner-brain-candidate-frequency-plan.md)
- [v26：InnerBrain 候选运行态统计方案](plans/2026-06-01-v26-inner-brain-candidate-runtime-stats-plan.md)
- [v27：桌面内脑候选快捷入口方案](plans/2026-06-01-v27-desktop-inner-brain-candidate-shortcut-plan.md)
- [v28：桌面候选训练模板填充方案](plans/2026-06-01-v28-desktop-inner-brain-candidate-template-plan.md)
