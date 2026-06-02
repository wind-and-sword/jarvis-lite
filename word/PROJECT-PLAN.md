# Jarvis Lite 当前项目方案

> 日期：2026-06-02
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
- InnerBrain 本地内脑：新增结构化 `InnerBrainResult`，包含 `intent`、`slots`、`confidence`、`missing`、`source`、`reason` 和策略；当前已迁移为 seed/runtime 样本分类器优先，并在字符 n-gram Dice 相似度基础上增加包含签名置信度补偿，同时提供固定 seed 评估集和本机 local evaluation JSONL，既有自然语言规则只作为 `legacy_fallback` 迁移期兼容兜底。
- InnerBrain 多轮澄清 v1：当本地内脑已识别 intent 但缺少 `source`、`items`、`path`、`query`、`result_index`、`tags`、`alias`、`experience` 等槽位时，`JarvisAgent` 会保留本轮澄清状态；用户下一句可直接补充文件路径、桌面快捷方式名称、联网搜索关键词、经验搜索/建议关键词、目录别名、经验内容、当前资料标签，或用“第二份 项目 Python”“项目 归档”这类一句式回复补齐组合槽位，Agent 补齐后继续执行原请求，用户也可用“取消补充”等表达取消。
- InnerBrain 可观察与样本闭环：`/inner-brain-status` 查看样本数量、阈值和训练目录；`/inner-brain-eval` 执行固定评估集和本机 `data/inner-brain/evaluation/*.jsonl` 评估样本，失败时给出 `/inner-brain-teach` 或 `/inner-brain-label` 显式修复建议，但不写入训练样本或运行态上下文；`/inner-brain-eval-failed` 复用同一评估集但只显示失败样例和修复建议；`/inner-brain-eval-local` 只执行本机 `local_evaluation` 样本，有样本时会提示切换到失败视图、已处理清单和文件聚焦视图，并按失败数优先列出可聚焦文件名候选及每个文件通过/失败数量，对仍有失败的文件提示同文件失败入口和按文件报告入口；`/inner-brain-eval-local-failed` 只显示本机失败样本，并按失败数优先展示失败来源文件分组，同时展示失败类型汇总、失败期望意图汇总、失败意图混淆汇总、失败文件意图混淆汇总、失败原因汇总、失败意图混淆分组修复建议、失败文件意图混淆分组修复建议和平铺修复建议；本机 evaluation 为空时，两者会提示只写 evaluation、不自动训练的添加入口；`/inner-brain-eval-local-report [文件名]` 可把本机失败评估导出为 Markdown 报告并汇总失败类型、期望意图、意图混淆方向、文件意图混淆方向、失败原因、意图混淆修复建议和文件意图混淆修复建议，导出反馈会提示继续查看失败样本、按文件聚焦和补 evaluation 样本；指定单个文件导出时会省略文件意图混淆交叉汇总和文件级修复建议分组，`/inner-brain-eval-local-file 文件名` 有样本时会提示当前文件失败视图、当前文件已处理清单和返回全部本机评估，`/inner-brain-eval-local-file-failed 文件名` 可进一步按本机 JSONL 文件过滤失败样本，`/inner-brain-eval-local-resolved [文件名]` 可只读查看当前已通过的本机 evaluation 样本；全量已处理视图按待处理失败数优先列出有通过样本的文件候选，并为仍有待处理失败的文件提示同文件失败入口；`/inner-brain-eval-add 文本 => /命令`、`/inner-brain-eval-label 文本 => intent [slot=value ...]`、`/inner-brain-eval-add-candidate 编号 => /命令` 和 `/inner-brain-eval-label-candidate 编号 => intent [slot=value ...]` 可把用户确认的真实日志或当前训练候选先写入本机 evaluation 样本，不自动训练，保存反馈会提示复跑本机评估、只看失败、聚焦 `runtime.jsonl` 和导出失败报告；`/inner-brain-preview 文本` 只预览识别结果，不执行命令或本地动作；`/inner-brain-adopt 文本` 将正确识别结果保存为运行态 JSONL 样本；`/inner-brain-label 文本 => intent [slot=value ...]` 可人工标注 unknown 或误识别样本；`/inner-brain-teach 文本 => /命令` 和“以后我说“文本”就是 /命令”可把用户口语短句教学为已知命令；`/inner-brain-candidates` 会把 fallback/澄清候选写入本地运行态统计，按出现次数优先展示，显式 teach、label 或 adopt 后移除对应候选，写入 evaluation 的候选仍保留，便于先评估再训练。
- 本地自然语言意图层，可处理常见中文表达，包括问候、助手身份/能力询问、最近上下文、最近文件、显式文件读取/导入、显式文件打标签、读取编号资料、查看/导入编号最近文件、查看编号搜索结果、查看/执行编号建议、当前资料/结果打标签、编号资料/搜索结果打标签、标签组读取与批量标签预览、知识库、常用目录打开/整理、最近目录打开/整理、日报、更新、经验记录/搜索/建议、确认/取消执行、联网搜索、联网搜索后续来源处理和明确点名的桌面 `.lnk` 快捷方式删除；InnerBrain 高置信度命中后仍由 `JarvisAgent` 执行。
- LLM 外脑 Router 第一版：provider-neutral 配置、`config/llm.local.json` 本地配置文件、fake provider 测试路径、OpenAI Responses API adapter、OpenAI-compatible 端点、`qwen`/`gemini` provider alias、完整 `/v1/responses` URL 归一化、provider 与 Agent 双层命令白名单、LLM fallback 近期上下文与最近搜索结果、LLM `clarify` 多轮澄清续聊、LLM 澄清状态运行态恢复、LLM 澄清轮数限制和过期清理、`/llm-config-init` 本地配置草稿生成、`/llm-config-set` 本地配置写入、`/llm-config-check` 本地配置只读检查、`/llm-enable` 外脑启用入口、`/llm-context-preview`、`/llm-smoke` 运行时配置验证、token usage 日志、`/llm-status` API key/网络调用诊断、`/llm-usage` 本地汇总和 `/llm-config-example` 配置模板。
- 联网搜索方案已明确为 SearchRouter 工具能力：搜索负责获取当前网页来源和摘要，LLM 外脑负责在 Agent 提供来源后做总结、比较和自然表达；两者互补，均不绕过 `JarvisAgent`。当前 `/search` 会把联网搜索结果写入最近上下文和 LLM context，`/search-summary` 与“联网查一下...并总结”会先搜索再把来源交给 LLM 总结；`/search-open`、`/search-compare`、`/search-save-summary` 和 `/search-import-summary` 负责最近联网搜索的来源查看、来源比较、摘要保存和知识库导入；`/search-config-init` 可生成本地搜索配置草稿，`/search-config-set` 可写入本地搜索配置，`/search-config-check` 可做只读配置检查，`/search-smoke` 可做不写入最近上下文的 provider 连通性测试。
- 桌面小助手、助手面板、托盘、快捷命令、主题、尺寸、开机启动和更新入口；助手面板已提供外脑和联网搜索配置区，可写入、检查和 smoke 测试 provider 配置，写入 API key 时不会把真实 key 显示到 transcript 或会话历史；面板固定展示 LLM 外脑待补充问题、澄清轮次、取消提示、外脑启用状态、最近一次 LLM 调用结果、最近一条用户输入的路由决策和路由选择依据；桌面面板和托盘快捷命令已提供“内脑候选”入口，桌面面板会根据候选列表同步 teach/label 模板按钮状态、编号上限、候选下拉选择和显式训练目标预填。
- 本地 `unittest` 验证体系。

## 下一阶段

当前已经完成 `0.66.0` 里程碑：

> InnerBrain 样本分类器优先 + InnerBrain 包含签名置信度补偿 + InnerBrain 固定评估集 + InnerBrain 本机评估 JSONL + InnerBrain 评估失败修复建议 + InnerBrain 评估失败过滤视图 + InnerBrain 本机评估过滤视图 + InnerBrain 本机评估样本显式写入 + InnerBrain 候选编号写入本机评估样本 + InnerBrain 本机评估 JSONL 文件过滤 + InnerBrain 本机失败评估按文件分组 + InnerBrain 本机失败评估 Markdown 报告导出 + InnerBrain 本机失败评估原因汇总 + InnerBrain 本机失败评估类型汇总 + InnerBrain 本机失败评估期望意图汇总 + InnerBrain 本机失败评估意图混淆汇总 + InnerBrain 本机失败评估文件意图混淆汇总 + InnerBrain 本机失败评估意图混淆修复建议分组 + InnerBrain 本机失败评估文件意图混淆修复建议分组 + InnerBrain 本机评估空样本引导 + InnerBrain 本机评估样本保存后续验证提示 + InnerBrain 本机失败报告导出后续处理提示 + InnerBrain 本机失败视图导出报告提示 + InnerBrain 本机失败视图文件聚焦提示 + InnerBrain 本机 evaluation 已处理样本只读清单 + InnerBrain 本机评估全量视图后续处理提示 + InnerBrain 本机评估全量视图文件名候选提示 + InnerBrain 本机评估全量视图文件候选状态摘要 + InnerBrain 本机评估全量视图文件候选失败优先排序 + InnerBrain 本机评估全量视图文件候选待处理入口 + InnerBrain 本机评估全量视图文件候选报告入口 + InnerBrain 本机失败视图失败文件汇总排序 + InnerBrain 本机失败视图失败文件分组聚焦入口 + InnerBrain 本机失败视图失败文件分组报告入口 + InnerBrain 本机文件失败视图已处理入口 + InnerBrain 本机已处理视图文件候选提示 + InnerBrain 本机已处理视图文件候选状态摘要 + InnerBrain 本机已处理视图文件候选待处理优先排序 + InnerBrain 本机已处理视图文件候选待处理入口 + LLM 外脑接入第一版 + Agent 联网搜索第一版 + 多轮澄清 v1 可安装闭环 + 外脑 provider 配置闭环 v1 + 运行态配置初始化 v1 + 本地配置检查 v1 + 本地配置写入 v1 + 连通性诊断 v1 + 桌面配置面板 v1 + LLM 外脑多轮澄清 v1 + LLM 澄清状态持久化 v1 + LLM 澄清轮数与过期策略 v1 + 桌面外脑待补充状态 v1 + 桌面外脑运行状态 v1 + 最近路由决策状态 v1 + 路由决策解释详情 v1 + 最近路由历史 v1 + 路由历史详情 v1 + InnerBrain 训练候选 v1 + 候选按编号教学 v1 + 候选按编号标注 v1 + 候选频次排序 v1 + 候选运行态统计 v1 + 桌面内脑候选快捷入口 v1 + 桌面候选训练模板填充 v1 + 桌面候选模板状态同步 v1 + 桌面候选选择绑定 v1 + 桌面候选目标预填 v1。

后续目标：

- 继续扩展 InnerBrain seed/runtime 样本，把用户真实日志和现有命令能力持续沉淀为 `text -> intent -> slots` 数据。
- 继续扩展 InnerBrain 固定评估集，再评估字符 n-gram、轻量 embedding 相似度或小型分类器，不从零训练通用 LLM。
- 继续扩大缺失槽位的自然语言补全范围，把更多 `missing` 场景接入多轮澄清状态，并沉淀更细的用户纠错样本；`0.2.0` 已收口文件路径、编号资料、当前资料标签、标签组+新标签、经验搜索关键词和经验建议关键词。
- 继续打磨真实 provider 的兼容端点体验、运行态本地配置体验和用量观察能力；`0.3.0` 已让 `qwen`/`gemini` 可作为 provider alias 复用 OpenAI-compatible adapter，`0.4.0` 已支持 `/llm-config-init` 与 `/search-config-init` 生成本机配置草稿，`0.5.0` 已支持 `/llm-config-check` 与 `/search-config-check` 做只读配置检查，`0.6.0` 已支持 `/llm-config-set` 与 `/search-config-set` 用显式 `key=value` 写入本机配置，`0.7.0` 已支持 `/llm-smoke` 重新读取当前本地配置和 `/search-smoke` provider 连通性测试，`0.8.0` 已把写入、检查和 smoke 入口放入桌面配置面板，`0.9.0` 已补齐 LLM `clarify` 的多轮续聊，`0.10.0` 已让 LLM 待澄清状态进入运行态上下文，`0.11.0` 已补齐连续澄清轮数和过期清理边界，`0.12.0` 已把 LLM 待补充状态固定展示到桌面面板，`0.13.0` 已把外脑启用状态和最近调用结果固定展示到桌面面板，`0.14.0` 已把最近路由决策固定展示到桌面面板，`0.15.0` 已把路由选择依据固定展示到同一段路由状态，`0.16.0` 已把最近 5 条路由历史固定展示到同一状态区，`0.17.0` 已提供 `/route-history` 路由历史详情并让 `/recent-context` 展示最近路由摘要，`0.18.0` 已提供 `/inner-brain-candidates` 从 fallback/澄清路由中列出人工训练候选，`0.19.0` 已支持 `/inner-brain-teach-candidate 编号 => /命令` 按编号教学候选，`0.20.0` 已支持 `/inner-brain-label-candidate 编号 => intent [slot=value ...]` 按编号标注候选，`0.21.0` 已让候选按出现次数优先排序，`0.22.0` 已把候选出现次数写入本地运行态统计并在训练后移除对应候选，`0.23.0` 已把“内脑候选”加入桌面面板和托盘直接快捷命令，`0.24.0` 已在桌面面板增加候选编号和 teach/label 模板填充入口，`0.25.0` 已让模板状态和编号上限随最近候选列表同步，`0.26.0` 已把候选列表单条候选绑定到桌面下拉选择，`0.27.0` 已为 teach/label 模板增加常见命令和 intent 的显式目标预填，`0.28.0` 已补齐样本包含签名置信度补偿，`0.29.0` 已提供 `/inner-brain-eval` 固定评估集，`0.30.0` 已支持本机 `data/inner-brain/evaluation/*.jsonl` 评估样本，`0.31.0` 已在评估失败时输出显式训练修复建议，`0.32.0` 已提供 `/inner-brain-eval-failed` 只看失败样本，`0.33.0` 已提供 `/inner-brain-eval-local` 和 `/inner-brain-eval-local-failed` 只看本机样本，`0.34.0` 已提供 `/inner-brain-eval-add` 和 `/inner-brain-eval-label` 显式写入本机评估样本，`0.35.0` 已提供 `/inner-brain-eval-add-candidate` 和 `/inner-brain-eval-label-candidate` 按候选编号写入本机评估样本，`0.36.0` 已提供 `/inner-brain-eval-local-file` 和 `/inner-brain-eval-local-file-failed` 按本机评估 JSONL 文件过滤，`0.37.0` 已让本机失败评估按来源 JSONL 文件分组，`0.38.0` 已支持 `/inner-brain-eval-local-report [文件名]` 导出本机失败评估 Markdown 报告，`0.39.0` 已在本机失败评估报告中加入失败原因汇总和典型样本，`0.40.0` 已在本机失败评估报告中加入失败类型汇总和典型样本，`0.41.0` 已在本机失败评估报告中加入失败期望意图汇总和典型样本，`0.42.0` 已在本机失败评估报告中加入失败意图混淆汇总和典型样本，`0.43.0` 已在本机失败评估报告中加入失败文件意图混淆交叉汇总和典型样本，`0.44.0` 已在本机失败评估报告中加入失败意图混淆修复建议分组，`0.45.0` 已在本机失败评估报告中加入失败文件意图混淆修复建议分组，`0.46.0` 已在本机 evaluation 样本为空时加入只读添加入口引导，`0.47.0` 已在本机 evaluation 样本保存反馈中加入后续验证提示，`0.48.0` 已在本机失败报告导出反馈中加入后续处理提示，`0.49.0` 已在本机失败视图中加入导出失败报告提示，`0.50.0` 已在本机失败视图中加入按文件聚焦和返回全部失败样本提示，`0.51.0` 已提供 `/inner-brain-eval-local-resolved [文件名]` 只读查看本机 evaluation 已处理样本，`0.52.0` 已在本机评估全量视图中加入失败/已处理/文件聚焦后续处理提示，`0.53.0` 已在本机评估全量视图中列出可聚焦文件名候选，`0.54.0` 已在本机评估全量视图的文件候选行中追加通过/失败数量，`0.55.0` 已让本机评估全量视图的文件候选按失败数量优先排序，`0.62.0` 已在本机评估全量视图文件候选中为仍有失败的文件追加同文件失败入口，`0.65.0` 已在本机评估全量视图文件候选中为仍有失败的文件追加按文件报告入口，`0.63.0` 已在本机失败视图的失败文件分组中为每个失败文件追加同文件失败入口，`0.64.0` 已在本机失败视图的失败文件分组中为每个失败文件追加按文件报告入口，`0.56.0` 已让本机失败视图的失败文件分组按失败数量优先排序，`0.57.0` 已在本机文件失败视图中提示查看当前文件已处理样本，`0.58.0` 已在本机已处理视图中列出可查看文件候选，`0.59.0` 已在本机已处理视图文件候选行中追加已处理/待处理失败数量，`0.60.0` 已让本机已处理视图文件候选按待处理失败数量优先排序，`0.61.0` 已在本机已处理视图文件候选中为仍有待处理失败的文件追加同文件失败入口，`0.66.0` 已在本机已处理视图文件候选中为仍有待处理失败的文件追加按文件报告入口。
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
- [v29：桌面候选模板状态同步方案](plans/2026-06-01-v29-desktop-inner-brain-candidate-template-sync-plan.md)
- [v30：桌面候选选择绑定方案](plans/2026-06-01-v30-desktop-inner-brain-candidate-selection-plan.md)
- [v31：桌面候选目标预填方案](plans/2026-06-01-v31-desktop-inner-brain-candidate-target-prefill-plan.md)
- [v32：InnerBrain 包含签名置信度补偿方案](plans/2026-06-01-v32-inner-brain-contained-signature-boost-plan.md)
- [v33：InnerBrain 固定评估集方案](plans/2026-06-01-v33-inner-brain-seed-evaluation-plan.md)
- [v34：InnerBrain 本机评估集扩展方案](plans/2026-06-01-v34-inner-brain-local-evaluation-plan.md)
- [v35：InnerBrain 评估失败修复建议方案](plans/2026-06-01-v35-inner-brain-evaluation-fix-suggestion-plan.md)
- [v36：InnerBrain 评估失败过滤视图方案](plans/2026-06-01-v36-inner-brain-evaluation-failures-only-plan.md)
- [v37：InnerBrain 本机评估过滤视图方案](plans/2026-06-01-v37-inner-brain-local-evaluation-view-plan.md)
- [v38：InnerBrain 本机评估样本显式写入方案](plans/2026-06-01-v38-inner-brain-local-evaluation-save-plan.md)
- [v39：InnerBrain 候选编号写入本机评估样本方案](plans/2026-06-01-v39-inner-brain-candidate-evaluation-save-plan.md)
- [v40：InnerBrain 本机评估 JSONL 文件过滤方案](plans/2026-06-02-v40-inner-brain-local-evaluation-file-filter-plan.md)
- [v41：InnerBrain 本机评估失败按 JSONL 文件分组方案](plans/2026-06-02-v41-inner-brain-local-evaluation-failure-group-plan.md)
- [v42：InnerBrain 本机评估失败报告导出方案](plans/2026-06-02-v42-inner-brain-local-evaluation-report-export-plan.md)
- [v43：InnerBrain 本机评估失败原因汇总方案](plans/2026-06-02-v43-inner-brain-failure-reason-summary-plan.md)
- [v44：InnerBrain 本机评估失败类型汇总方案](plans/2026-06-02-v44-inner-brain-failure-type-summary-plan.md)
- [v45：InnerBrain 本机评估失败期望意图汇总方案](plans/2026-06-02-v45-inner-brain-failure-expected-intent-summary-plan.md)
- [v46：InnerBrain 本机评估失败意图混淆汇总方案](plans/2026-06-02-v46-inner-brain-intent-confusion-summary-plan.md)
- [v47：InnerBrain 本机评估失败文件意图混淆汇总方案](plans/2026-06-02-v47-inner-brain-file-intent-confusion-summary-plan.md)
- [v48：InnerBrain 本机评估失败意图混淆修复建议分组方案](plans/2026-06-02-v48-inner-brain-intent-confusion-fix-suggestions-plan.md)
- [v49：InnerBrain 本机失败评估文件意图混淆修复建议分组方案](plans/2026-06-02-v49-inner-brain-file-intent-confusion-fix-suggestions-plan.md)
- [v50：InnerBrain 本机评估空样本引导方案](plans/2026-06-02-v50-inner-brain-local-evaluation-empty-guidance-plan.md)
- [v51：InnerBrain 本机评估样本保存后续验证提示方案](plans/2026-06-02-v51-inner-brain-local-evaluation-save-next-steps-plan.md)
- [v52：InnerBrain 本机失败评估报告导出后续处理提示方案](plans/2026-06-02-v52-inner-brain-report-export-next-steps-plan.md)
- [v53：InnerBrain 本机失败视图导出报告提示方案](plans/2026-06-02-v53-inner-brain-local-failed-report-hint-plan.md)
- [v54：InnerBrain 本机失败视图文件聚焦提示方案](plans/2026-06-02-v54-inner-brain-local-failed-file-focus-hint-plan.md)
- [v55：InnerBrain 本机 evaluation 已处理样本只读清单方案](plans/2026-06-02-v55-inner-brain-local-resolved-list-plan.md)
- [v56：InnerBrain 本机评估全量视图后续处理提示方案](plans/2026-06-02-v56-inner-brain-local-eval-next-steps-plan.md)
- [v57：InnerBrain 本机评估全量视图文件名候选提示方案](plans/2026-06-02-v57-inner-brain-local-eval-file-suggestions-plan.md)
- [v58：InnerBrain 本机评估全量视图文件候选状态摘要方案](plans/2026-06-02-v58-inner-brain-local-eval-file-status-plan.md)
- [v59：InnerBrain 本机评估全量视图文件候选失败优先排序方案](plans/2026-06-02-v59-inner-brain-local-eval-file-priority-plan.md)
- [v60：InnerBrain 本机失败视图失败文件汇总排序方案](plans/2026-06-02-v60-inner-brain-local-failed-file-priority-plan.md)
- [v61：InnerBrain 本机文件失败视图已处理入口方案](plans/2026-06-02-v61-inner-brain-local-file-failed-resolved-hint-plan.md)
- [v62：InnerBrain 本机已处理视图文件候选提示方案](plans/2026-06-02-v62-inner-brain-local-resolved-file-suggestions-plan.md)
- [v63：InnerBrain 本机已处理视图文件候选状态摘要方案](plans/2026-06-02-v63-inner-brain-local-resolved-file-status-plan.md)
- [v64：InnerBrain 本机已处理视图文件候选待处理优先排序方案](plans/2026-06-02-v64-inner-brain-local-resolved-file-priority-plan.md)
- [v65：InnerBrain 本机已处理视图文件候选待处理入口方案](plans/2026-06-02-v65-inner-brain-local-resolved-file-failed-shortcut-plan.md)
- [v66：InnerBrain 本机评估全量视图文件候选待处理入口方案](plans/2026-06-02-v66-inner-brain-local-eval-file-failed-shortcut-plan.md)
