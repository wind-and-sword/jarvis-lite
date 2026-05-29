# Jarvis Lite v22：InnerBrain 训练候选方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v21 路由历史详情，明确 `0.18.0` 的训练候选收口。

## 核心结论

`0.18.0` 开始把“看见路由问题”推进为“沉淀训练闭环前置”。本阶段新增只读候选入口：

```text
最近路由历史
  -> 筛选 llm-fallback / memory-fallback / inner-brain-clarify
  -> /inner-brain-candidates 展示候选输入、当前路由、结果、依据
  -> 给出 /inner-brain-teach 与 /inner-brain-label 示例
```

它不会自动训练，因为 LLM fallback 可能是开放问题，memory fallback 也可能只是没有资料。候选列表只帮助用户判断哪些表达应固定为本地内脑样本。

## 设计边界

- 不新增自然语言正则规则。
- 不自动写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 InnerBrain、知识库、LLM fallback 或联网搜索执行顺序。
- 候选来源只使用最近 5 条路由历史，不新增长期审计日志。
- `/inner-brain-candidates` 是只读诊断入口，不污染路由历史。

## 0.18.0 收口内容

- 新增 `/inner-brain-candidates`、`inner-brain-candidates`、`/brain-candidates`、`brain-candidates`。
- 候选包含 LLM fallback、记忆兜底和 InnerBrain 澄清路由。
- 每条候选展示输入、当前路由、结果、依据和人工训练示例。
- 项目版本同步到 `0.18.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 增加“采纳第 N 条候选为教学样本”的显式命令，但必须由用户指定目标命令或 intent。
- 对候选做去重和频次统计，优先处理重复出现的低置信度或 fallback 输入。
