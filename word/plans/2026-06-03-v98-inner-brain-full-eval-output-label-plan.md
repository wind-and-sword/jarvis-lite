# v98：InnerBrain 全量评估输出固定与本机评估集标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v97 全量评估运行日志固定与本机评估集标签，明确 `0.94.0` 的评估输出正文标签。

## 目标

`0.94.0` 把 InnerBrain 评估响应正文里的内部评估集名称改成用户可读标签：固定 seed 评估显示为“固定评估集”，本机 `data/inner-brain/evaluation/*.jsonl` 样本显示为“本机评估集”。这样 `/inner-brain-eval` 的输出正文和运行日志都能明确区分“固定+本机”和只看本机样本。

## 范围

- `/inner-brain-eval` 无本机样本时，输出 `评估集：固定评估集`。
- `/inner-brain-eval` 有本机样本时，输出 `评估集：固定评估集+本机评估集`，来源计数显示 `固定评估集：N 条` 与 `本机评估集：N 条`。
- `/inner-brain-eval-local` 继续只评估本机样本，但正文显示 `评估集：本机评估集`；指定文件时保留文件名上下文。
- 不改变 `report.name` 内部值、source key、评估样本读取、筛选、排序、失败报告、训练写入、命令集合或运行日志。

## 验证

- RED：InnerBrain 评估描述和 Agent `/inner-brain-eval` 响应先失败，证明仍输出 `seed_evaluation` / `local_evaluation` 内部名。
- GREEN：实现后目标测试通过，覆盖固定评估、固定+本机评估和本机评估输出标签。
- 回归：运行 InnerBrain + Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
