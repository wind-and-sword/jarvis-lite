# v71 InnerBrain 本机文件视图报告入口方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v70 本机已处理视图文件候选报告入口，明确 `0.67.0` 的本机文件视图报告入口。

## 目标

`0.67.0` 在 `/inner-brain-eval-local-file 文件名` 的指定文件总览中，为当前文件仍有失败样本的场景追加可复制的按文件导出报告入口。用户从单个 JSONL 文件总览查看通过/失败混合结果时，可以直接进入 `/inner-brain-eval-local-report 当前文件名`。

## 范围

- `/inner-brain-eval-local-file 文件名` 仍显示当前文件评估结果、后续处理、待处理失败入口、已处理样本入口和返回全部本机评估入口。
- 当当前文件存在失败样本时，后续处理追加：
  `/inner-brain-eval-local-report 当前文件名`
- 当前文件纯通过时不追加报告入口。

## 非目标

- 不新增命令，继续复用既有 `/inner-brain-eval-local-report [文件名]`。
- 不改变 `/inner-brain-eval-local-file-failed 文件名` 指定文件失败视图。
- 不改变 `/inner-brain-eval-local` 全量评估视图、全量文件候选排序或已处理视图。
- 不修改本机 evaluation JSONL payload、训练路径、失败样例、已处理样例、修复建议或报告导出路径。

## 验收

- RED：新增 Agent 指定文件总览报告入口断言和版本一致性测试先失败。
- GREEN：实现后目标测试通过，纯通过指定文件不出现报告入口。
- 回归：运行 Agent + ProjectMetadata 相邻测试、全量 `unittest`、桌面 smoke、安装包构建、打包后 exe smoke、静态检查、Markdown 本地链接检查和敏感信息差异扫描。
