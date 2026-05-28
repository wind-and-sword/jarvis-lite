# Jarvis Lite v3：PC Agent 与 LLM 外脑优先方案

> 日期：2026-05-27
> 执行者：Codex
> 说明：本文是当前方案版本，修正 v2 中多端入口推进过早的问题，将后续路线明确为先完善 PC Agent，再接入 LLM 外脑，最后再评估手机、手表、车机和 AR 眼镜等入口。

## 1. 当前定位

Jarvis Lite 是一个本地优先的个人 PC Agent。它的核心不是“聊天”，而是把自然语言、个人记忆、知识库、最近上下文、桌面入口和本机工具组织成可持续扩展的执行系统。

当前主线：

```text
用户输入
  -> 本地意图层
  -> JarvisAgent
  -> 记忆 / 知识库 / 最近上下文
  -> 本机工具与桌面入口
  -> 结果反馈 / 下一步建议 / 确认执行
```

这一层稳定后，LLM 才作为外脑接入，而不是替代本地执行层。

## 2. 路线调整

v2 方案已经提出“个人设备级 Agent”，但手机、手表等设备入口在当前阶段不应过早展开。更合理的顺序是：

```text
阶段 1：PC Agent 稳定
阶段 2：接入 LLM 外脑
阶段 3：打磨 PC + LLM 核心闭环
阶段 4：评估手机、手表、车机、AR 眼镜等多端入口
```

这样做的原因：

- PC 是当前代码和使用场景最完整的承载端。
- LLM 的价值主要体现在复杂理解、总结、规划和结构化意图生成，应该尽早服务 PC 主线。
- 手机、手表、车机和 AR 眼镜更像入口或数据源，过早投入会分散核心 Agent 能力。
- 多端能力需要稳定的本地执行层和上下文系统支撑，否则会变成多个不完整入口。

## 3. 当前已具备的基础

截至 2026-05-27，项目已经具备：

- 命令行入口和桌面入口。
- 长期记忆、经验记忆和个人知识库。
- 本地自然语言意图层。
- 最近资料、最近文件、最近目录、最近搜索结果、最近建议和批量标签历史。
- 知识库导入、问答、摘要、标签、按标签读取资料组和批量打标签确认闭环。
- 桌面小助手、助手面板、托盘、快捷命令、主题、尺寸和更新入口。
- 本地 `unittest` 验证体系和持续追加的验证记录。

这些能力说明项目已经具备 PC Agent 主干，下一步不应立即转向多端，而应把 LLM 接入点接到现有主干上。

## 4. LLM 接入原则

LLM 作为外脑，主要承担：

- 复杂自然语言理解。
- 多步骤任务拆解。
- 对知识库资料进行更自然的总结和推理。
- 将用户表达转换为结构化意图或工具建议。
- 在不确定时给出澄清问题或下一步候选方案。

LLM 不直接替代：

- `JarvisAgent` 的执行入口。
- 本地命令和工具调用约定。
- 运行态上下文写入。
- 本地测试和验证流程。

推荐链路：

```text
用户输入
  -> 本地意图层优先判断
  -> 本地可处理：直接进入 JarvisAgent
  -> 本地不确定：调用 LLMRouter 生成结构化 LLMIntent
  -> JarvisAgent 解析 LLMIntent
  -> 进入既有工具、上下文和反馈流程
```

截至 2026-05-28，第一版已经落地 provider-neutral 的 `LLMRouter` / `LLMProvider` / `LLMIntent` 分层，并具备 `off`、`fake`、OpenAI Responses API provider、OpenAI-compatible Responses 端点、`config/llm.local.json` 本地配置文件、完整 `/v1/responses` URL 归一化、provider 与 Agent 双层命令白名单、LLM fallback 近期上下文与最近搜索结果、`/llm-enable` 外脑启用入口、`/llm-context-preview`、`/llm-smoke` 配置验证、token usage 日志、`/llm-status` API key/网络调用诊断、provider 错误可读化、`/llm-usage` 本地汇总和 `/llm-config-example` 配置模板。Gemini、Qwen provider 后续应作为 adapter 接入，不让 `JarvisAgent` 直接感知厂商细节。

## 5. 下一阶段建议

下一阶段主题建议继续围绕：

> LLM 外脑接入第一版。

已完成：

- 配置 LLM Provider 和模型参数。
- 新增结构化意图返回格式。
- 在本地命令、身份、本地自然语言意图和知识库问答之后调用 LLM。
- 让 LLM 输出可被 `JarvisAgent` 接收的命令建议，而不是自由执行。
- 增加 fake provider 测试路径、OpenAI Responses API adapter、OpenAI-compatible 端点、本地 `config/llm.local.json` 配置文件、完整 `/v1/responses` URL 归一化、provider 与 Agent 双层命令白名单、LLM fallback 近期上下文与最近搜索结果、`/llm-enable`、`/llm-context-preview`、`/llm-smoke` 配置验证、token usage 日志、`/llm-status` API key/网络调用诊断、provider 错误可读化、`/llm-usage` 本地汇总和 `/llm-config-example` 配置模板。

后续继续完成：

- 对知识库摘要、资料问答、经验建议和复杂任务拆解做第一批增强。
- 为 LLM 分支补充本地可重复测试，必要时用固定响应桩替代真实网络调用。
- 扩展 Gemini 和 Qwen adapter，并保持同一 Router 接口。

## 6. 暂缓事项

以下内容在 PC + LLM 核心闭环稳定前暂缓：

- 手机端控制或通知同步。
- 手表健康数据接入。
- 车机入口。
- AR 眼镜入口。
- 跨设备同步协议。

这些方向不取消，只是不作为当前连续开发主线。

## 7. 版本关系

- v1：`word/plans/2026-05-18-v1-overall-plan.md`，定义本地个人助手起点。
- v2：`word/plans/2026-05-22-v2-personal-device-agent-plan.md`，扩展为个人设备级 Agent 设想。
- v3：本文，明确当前优先级为 PC Agent -> LLM 外脑 -> 多端入口。
