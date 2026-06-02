# Jarvis Lite v50：InnerBrain 本机评估空样本引导方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v49 文件意图混淆修复建议分组，明确 `0.46.0` 的本机评估空样本引导闭环。

## 目标

`0.46.0` 在 InnerBrain 本机评估样本为空时增加只读空状态引导。用户执行 `/inner-brain-eval-local` 或 `/inner-brain-eval-local-failed` 时，如果当前没有 `data/inner-brain/evaluation/*.jsonl` 样本，输出会明确显示“本机评估样本：- 无”，并列出可用于沉淀本机 evaluation 样本的显式命令。

## 边界

- 不新增命令。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 evaluation JSONL payload、去重键或保存路径。
- 不改变 seed 评估语义。
- 不基于测试构造失败调整知识库状态/摘要样本。
- 不改变本机评估报告导出格式之外的持久化行为。

## 实现要点

- `describe_inner_brain_evaluation()` 在 `report.total_count == 0` 且评估集为 `local_evaluation` 时追加空状态提示。
- 空状态提示列出：
  - `/inner-brain-eval-add 文本 => /命令`
  - `/inner-brain-eval-label 文本 => intent [slot=value ...]`
  - `/inner-brain-eval-add-candidate 编号 => /命令`
  - `/inner-brain-eval-label-candidate 编号 => intent [slot=value ...]`
- 文案明确说明这些入口只写入本机 evaluation 样本，不自动训练。
- Agent 命令继续复用同一评估描述函数，因此 `/inner-brain-eval-local` 和 `/inner-brain-eval-local-failed` 自动获得同一空状态。

## 验证

- RED：新增 InnerBrain 空本机评估描述测试、Agent 本机失败空样本命令测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 用户沉淀真实本机 evaluation 样本后，再根据失败报告中的高频失败维度补 seed/runtime 样本、槽位补全或轻量评分补偿。
