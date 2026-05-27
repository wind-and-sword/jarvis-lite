# Jarvis Lite 当前项目方案

> 日期：2026-05-27
> 执行者：Codex
> 说明：本文是当前项目方案入口。历史方案版本保存在 `word/plans/`。

## 项目定位

Jarvis Lite 是一个本地优先的个人 PC Agent，目标是让 AI 逐步理解用户的文件、知识库、记忆、最近上下文和桌面工作流，并通过命令行和桌面入口帮助用户完成真实任务。

它当前不是多端平台，也不是纯聊天机器人。当前重点是把 PC 上的本地 Agent 主干做稳，再让 LLM 作为外脑增强理解、总结和规划能力。

## 当前路线

```text
PC Agent 稳定
  -> 接入 LLM 外脑
  -> 打磨 PC + LLM 核心闭环
  -> 再评估手机、手表、车机、AR 眼镜等多端入口
```

## 当前主干

```text
用户输入
  -> 命令 / 身份 / 本地自然语言意图 / 知识库问答优先
  -> 本地无法处理时进入 LLMRouter
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
- 本地自然语言意图层，可处理常见中文表达。
- LLM 外脑 Router 第一版：provider-neutral 配置、fake provider 测试路径、OpenAI Responses API adapter、OpenAI-compatible 端点、token usage 日志和 `/llm-status`。
- 桌面小助手、助手面板、托盘、快捷命令、主题、尺寸、开机启动和更新入口。
- 本地 `unittest` 验证体系。

## 下一阶段

当前已经进入并落地第一批：

> LLM 外脑接入第一版。

后续目标：

- 扩展 Gemini 和 Qwen provider adapter。
- 为真实 provider 继续补充本地配置 smoke 和用量观察能力。
- 继续打磨 LLM 结构化意图提示词和失败兜底。
- 让 LLM 生成更稳定的命令建议、资料总结、任务拆解和澄清问题。
- 继续由 `JarvisAgent` 承接工具调用、上下文更新和结果反馈。

## 暂缓方向

以下方向在 PC + LLM 核心闭环稳定前暂缓：

- 手机端。
- 手表健康数据。
- 车机入口。
- AR 眼镜入口。
- 跨设备同步。

## 方案版本

- [v1：整体方案与路线图](plans/2026-05-18-v1-overall-plan.md)
- [v2：个人设备级 Agent 融合方案](plans/2026-05-22-v2-personal-device-agent-plan.md)
- [v3：PC Agent 与 LLM 外脑优先方案](plans/2026-05-27-v3-pc-agent-llm-first-plan.md)
