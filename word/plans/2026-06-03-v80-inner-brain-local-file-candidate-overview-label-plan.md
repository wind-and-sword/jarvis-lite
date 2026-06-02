# v80：InnerBrain 本机评估全量视图文件候选总览标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v79 本机已处理视图文件候选当前文件总览入口，明确 `0.76.0` 的本机评估全量视图文件候选总览标签。

## 目标

`0.76.0` 在 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选行中，把同文件全部样本入口从裸命令 `/inner-brain-eval-local-file 当前文件名` 调整为 `总览：/inner-brain-eval-local-file 当前文件名`。这样全量视图、失败视图和已处理视图的文件候选入口标签保持一致，用户能直接区分同文件总览、待处理失败和报告导出。

## 范围

- 全量本机评估文件候选行继续保留：
  - `总览：/inner-brain-eval-local-file 当前文件名`
  - 当同文件仍有失败时的 `待处理：/inner-brain-eval-local-file-failed 当前文件名`
  - 当同文件仍有失败时的 `报告：/inner-brain-eval-local-report 当前文件名`
- 纯通过文件只显示同文件总览入口，不追加待处理失败或报告入口。
- 候选排序继续按失败数量优先，不改变每个文件的总数、通过数和失败数统计。
- 不新增命令，继续复用既有 `/inner-brain-eval-local-file [文件名]`。
- 不修改评估主体、失败修复建议、报告正文、训练样本写入或本机 evaluation JSONL payload。

## 验收

- RED：全量本机评估文件候选相关 Agent 测试和版本一致性测试先失败，证明候选行仍使用裸 `/inner-brain-eval-local-file 当前文件名`。
- GREEN：实现后目标测试通过，候选行包含 `总览：/inner-brain-eval-local-file zzz-failed-log.jsonl`，并在有失败时继续包含待处理和报告入口。
- 回归：运行 `tests.test_agent`、`tests.test_project_metadata` 和全量 `unittest discover`。
- 打包：构建 Windows 安装包并验证源码 smoke、打包后 exe smoke、安装脚本版本号和 Markdown 本地链接。
