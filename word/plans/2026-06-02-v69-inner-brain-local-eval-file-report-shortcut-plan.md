# v69 InnerBrain 本机评估全量视图文件候选报告入口方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v68 本机失败视图失败文件分组报告入口，明确 `0.65.0` 的本机评估全量视图文件候选报告入口。

## 目标

`0.65.0` 在 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选行中，为仍有失败样本的来源 JSONL 文件追加可复制的按文件导出报告入口。用户查看全部本机 evaluation 样本时，可以直接从总览进入 `/inner-brain-eval-local-report 当前文件名`，不再手动拼接报告命令。

## 范围

- `/inner-brain-eval-local` 未指定文件且存在本机样本时，候选行继续显示文件名、总样本数、通过数量、失败数量和文件聚焦入口。
- 当同文件失败数量大于 0 时，候选行保留待处理入口：
  `/inner-brain-eval-local-file-failed 当前文件名`
- 同一行追加报告入口：
  `/inner-brain-eval-local-report 当前文件名`
- 纯通过文件不追加待处理入口，也不追加报告入口。
- 候选排序继续按失败数量降序、总样本数降序、文件名升序。

## 非目标

- 不新增命令，继续复用既有 `/inner-brain-eval-local-report [文件名]`。
- 不改变 `/inner-brain-eval-local-file 文件名` 指定文件视图。
- 不改变 `/inner-brain-eval-local-failed` 失败视图分组。
- 不修改本机 evaluation JSONL payload、训练路径、失败样例、修复建议或报告导出路径。

## 验收

- RED：更新 Agent 本机全量评估文件候选断言和版本一致性测试先失败。
- GREEN：实现后目标测试通过，纯通过文件候选不出现报告入口。
- 回归：运行 Agent + ProjectMetadata 相邻测试、全量 `unittest`、桌面 smoke、安装包构建、打包后 exe smoke、静态检查、Markdown 本地链接检查和敏感信息差异扫描。
