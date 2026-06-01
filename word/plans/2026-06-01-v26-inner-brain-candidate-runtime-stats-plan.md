# Jarvis Lite v26：InnerBrain 候选运行态统计方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v25 InnerBrain 候选频次排序，明确 `0.22.0` 的候选运行态统计闭环。

## 核心结论

`0.22.0` 将 InnerBrain 训练候选从“最近 5 条路由内聚合”升级为“写入本地运行态候选统计”。当用户多次输入同一句 fallback 或澄清候选时，Jarvis Lite 会累计候选出现次数；即使该输入被后续 5 条路由挤出最近路由历史，`/inner-brain-candidates` 仍会优先展示这个高频缺口。

```text
最近路由：A、A、A、B、C、D、E、F
  -> A 已不在最近 5 条路由
  -> /inner-brain-candidates
  -> 1. A（出现次数：3）
  -> 2. F（出现次数：1）
```

## 设计边界

- 不新增自然语言正则规则。
- 不自动推断目标命令、intent 或 slot。
- 不自动把候选写入训练样本；仍必须由用户显式 teach、label 或 adopt。
- 只记录候选观察统计，不记录真实 API key 或本地 provider 配置。
- 统计保存在本地运行态上下文中，作为短中期训练辅助，不作为长期知识库。

## 0.22.0 收口内容

- 新增 `RuntimeInnerBrainCandidateContext`，保存候选文本、最近路由、摘要、依据、出现次数和首次/最近观察时间。
- `JarvisAgent` 在记录 `llm-fallback`、`memory-fallback` 和 `inner-brain-clarify` 路由时同步更新候选统计。
- `/inner-brain-candidates` 优先读取运行态候选统计，并按出现次数降序展示。
- `/inner-brain-teach-candidate` 和 `/inner-brain-label-candidate` 复用同一候选统计编号。
- 显式 teach、label 或 adopt 后移除对应候选，避免已训练文本继续出现在候选列表。
- 项目版本同步到 `0.22.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 在桌面面板上提供候选快捷复制或填充入口，减少手输命令成本。
- 继续评估轻量 embedding 或小型分类器，但不从零训练通用 LLM。
