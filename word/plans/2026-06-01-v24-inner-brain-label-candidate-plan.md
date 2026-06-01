# Jarvis Lite v24：InnerBrain 候选按编号标注方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v23 InnerBrain 候选按编号教学，明确 `0.20.0` 的非命令型候选标注闭环。

## 核心结论

`0.20.0` 补齐候选训练闭环的另一半：当候选不是固定命令，而是需要明确 `intent` 和 `slot` 时，用户可以直接按编号标注。

```text
/inner-brain-candidates
  -> 用户看到第 N 条候选
  -> /inner-brain-label-candidate N => intent slot=value
  -> Agent 保存 text -> intent -> slots runtime 样本
  -> 重新加载 InnerBrain
```

## 设计边界

- 不新增自然语言正则规则。
- 不自动推断 intent 或 slot。
- 不自动写入候选，必须显式执行 `/inner-brain-label-candidate 编号 => intent [slot=value ...]`。
- 不执行标注出来的本地动作。
- 不改变 InnerBrain、知识库、LLM fallback 或联网搜索执行顺序。

## 0.20.0 收口内容

- 新增 `/inner-brain-label-candidate 编号 => intent [slot=value ...]`。
- 复用 `/inner-brain-candidates` 的候选筛选顺序。
- 复用 `/inner-brain-label` 的 slot 解析、runtime 样本保存和当前 Agent 刷新逻辑。
- 候选标注命令不记录自身路由，避免改变候选编号。
- 项目版本同步到 `0.20.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 对候选做频次统计，优先处理重复出现的 fallback 输入。
- 在桌面面板上提供候选快捷复制或填充入口，减少手输命令成本。
