# Jarvis Lite v51：InnerBrain 本机评估样本保存后续验证提示方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v50 本机评估空样本引导，明确 `0.47.0` 的本机 evaluation 样本保存后续验证提示闭环。

## 目标

`0.47.0` 在用户显式保存本机 evaluation 样本后，直接提示下一步验证命令。用户通过 `/inner-brain-eval-add`、`/inner-brain-eval-label`、`/inner-brain-eval-add-candidate` 或 `/inner-brain-eval-label-candidate` 写入样本后，可以马上看到如何复跑本机评估、只看失败样本、聚焦当前 `runtime.jsonl` 文件和导出失败报告。

## 边界

- 不新增命令。
- 不自动运行评估。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 evaluation JSONL payload、去重键或保存路径。
- 不改变候选写入 evaluation 后仍保留的语义。

## 实现要点

- 继续复用 `_describe_inner_brain_evaluation_case_save()` 作为四条 evaluation 保存路径的统一反馈出口。
- 在保存反馈末尾追加 `后续验证：`。
- 后续验证提示列出：
  - `/inner-brain-eval-local`
  - `/inner-brain-eval-local-failed`
  - `/inner-brain-eval-local-file runtime.jsonl`
  - `/inner-brain-eval-local-report`
- 既有 `样本文件`、`用户说法`、`意图`、`期望策略`、`目标命令` 和“不训练”说明保持不变。

## 验证

- RED：新增 Agent 保存反馈后续验证提示测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 用户沉淀真实本机 evaluation 样本后，再根据失败报告中的高频失败维度补 seed/runtime 样本、槽位补全或轻量评分补偿。
