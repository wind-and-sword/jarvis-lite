# v72 InnerBrain 本机已处理指定文件视图报告入口方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v71 本机文件视图报告入口，明确 `0.68.0` 的本机已处理指定文件视图报告入口。

## 目标

`0.68.0` 在 `/inner-brain-eval-local-resolved 文件名` 的指定文件已处理视图中，为同文件仍有待处理失败样本的场景追加可复制的按文件导出报告入口。用户查看某个 JSONL 文件的已通过样本时，可以直接进入 `/inner-brain-eval-local-report 当前文件名` 处理剩余失败。

## 范围

- `/inner-brain-eval-local-resolved 文件名` 仍只读展示当前文件已通过样本。
- 当同文件仍有待处理失败样本时，后续处理追加：
  `/inner-brain-eval-local-report 当前文件名`
- 当前文件纯通过时不追加报告入口。

## 非目标

- 不新增命令，继续复用既有 `/inner-brain-eval-local-report [文件名]`。
- 不改变 `/inner-brain-eval-local-resolved` 全量已处理候选。
- 不改变 `/inner-brain-eval-local-file 文件名` 或 `/inner-brain-eval-local-file-failed 文件名` 指定文件视图。
- 不修改本机 evaluation JSONL payload、训练路径、失败样例、已处理样例、修复建议或报告导出路径。

## 验收

- RED：新增 Agent 指定文件已处理视图报告入口断言和版本一致性测试先失败。
- GREEN：实现后目标测试通过，纯通过指定文件不出现报告入口。
- 回归：运行 Agent + ProjectMetadata 相邻测试、全量 `unittest`、桌面 smoke、安装包构建、打包后 exe smoke、静态检查、Markdown 本地链接检查和敏感信息差异扫描。
