# Jarvis Lite v40：InnerBrain 本机评估文件过滤方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v39 候选编号写入本机评估样本，明确 `0.36.0` 的本机 evaluation JSONL 文件过滤入口。

## 目标

`0.36.0` 让本机评估样本增多后，可以按 `data/inner-brain/evaluation/*.jsonl` 文件名只查看某一个来源文件的评估结果，便于把真实日志、失败复盘和运行态样本拆文件排查。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变评估样本 JSONL 的持久化字段和去重键。
- 不改变正常聊天路由、LLM fallback 或联网搜索能力。
- 本阶段只做文件名过滤，不做报告导出或失败分组。

## 实现要点

- `InnerBrainEvaluationCase` 增加只读 `source_file` 元数据，加载本机 JSONL 时记录来源文件名。
- `evaluate_inner_brain(..., source_file_filter=...)` 支持按本机 JSONL basename 过滤，用户省略 `.jsonl` 时自动补全。
- 评估报告名在过滤时显示为 `local_evaluation:<文件名>`，描述中追加 `评估文件：<文件名>`。
- 新增 `/inner-brain-eval-local-file 文件名`，只执行指定本机评估文件。
- 新增 `/inner-brain-eval-local-file-failed 文件名`，只显示指定本机评估文件中的失败样本和修复建议。
- 两个命令作为观察/治理入口处理，不污染最近路由历史。

## 验证

- RED：新增 InnerBrain 文件过滤测试、Agent 指定文件评估测试、Agent 指定文件失败视图测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain 专项、Agent/LLM/桌面/Conversation 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据本机评估文件中的失败集继续改进样本、槽位补全或轻量分类器评分。
- 当不同来源文件继续增多时，再做失败分组、报告导出或按文件汇总的治理视图。
