# Jarvis Lite v23：InnerBrain 候选按编号教学方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v22 InnerBrain 训练候选，明确 `0.19.0` 的候选教学闭环。

## 核心结论

`0.19.0` 继续推进“看见候选 -> 显式训练”的闭环，但仍不让系统自动猜意图。本阶段新增：

```text
/inner-brain-candidates
  -> 用户看到第 N 条候选
  -> /inner-brain-teach-candidate N => /明确命令
  -> Agent 保存 text -> command runtime 样本
  -> 重新加载 InnerBrain
```

这样用户不用复制整句候选文本，也不会把开放问题错误地自动塞进内脑训练集。

## 设计边界

- 不新增自然语言正则规则。
- 不自动推断目标命令。
- 不自动写入候选，必须显式执行 `/inner-brain-teach-candidate 编号 => /命令`。
- 不改变 InnerBrain、知识库、LLM fallback 或联网搜索执行顺序。
- 本阶段只做命令教学候选；复杂 `intent slot=value` 候选标注留到后续阶段。

## 0.19.0 收口内容

- 新增 `/inner-brain-teach-candidate 编号 => /命令`。
- 复用 `/inner-brain-candidates` 的候选筛选顺序。
- 目标命令复用 `/inner-brain-teach` 的白名单校验和保存逻辑。
- 候选教学命令不记录自身路由，避免改变候选编号。
- 项目版本同步到 `0.19.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 增加 `/inner-brain-label-candidate 编号 => intent slot=value`，覆盖非命令型 intent/slot 标注。
- 对候选做频次统计，优先处理重复出现的 fallback 输入。
