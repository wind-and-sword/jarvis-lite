# v70 InnerBrain 本机已处理视图文件候选报告入口方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v69 本机评估全量视图文件候选报告入口，明确 `0.66.0` 的本机已处理视图文件候选报告入口。

## 目标

`0.66.0` 在 `/inner-brain-eval-local-resolved` 的 `可查看文件：` 候选行中，为仍有待处理失败样本的来源 JSONL 文件追加可复制的按文件导出报告入口。用户查看已处理样本总览时，可以直接从同文件候选进入 `/inner-brain-eval-local-report 当前文件名`，继续处理剩余失败。

## 范围

- `/inner-brain-eval-local-resolved` 未指定文件且存在已处理样本时，候选行继续显示文件名、已处理数量、待处理失败数量和已处理文件查看入口。
- 当同文件待处理失败数量大于 0 时，候选行保留待处理入口：
  `/inner-brain-eval-local-file-failed 当前文件名`
- 同一行追加报告入口：
  `/inner-brain-eval-local-report 当前文件名`
- 纯通过文件不追加待处理入口，也不追加报告入口。
- 候选排序继续按待处理失败数量降序、已处理数量降序、文件名升序。

## 非目标

- 不新增命令，继续复用既有 `/inner-brain-eval-local-report [文件名]`。
- 不改变 `/inner-brain-eval-local-resolved 文件名` 指定文件视图。
- 不改变 `/inner-brain-eval-local` 全量评估视图。
- 不修改本机 evaluation JSONL payload、训练路径、失败样例、已处理样例、修复建议或报告导出路径。

## 验收

- RED：更新 Agent 本机已处理视图文件候选断言和版本一致性测试先失败。
- GREEN：实现后目标测试通过，纯通过文件候选不出现报告入口。
- 回归：运行 Agent + ProjectMetadata 相邻测试、全量 `unittest`、桌面 smoke、安装包构建、打包后 exe smoke、静态检查、Markdown 本地链接检查和敏感信息差异扫描。
