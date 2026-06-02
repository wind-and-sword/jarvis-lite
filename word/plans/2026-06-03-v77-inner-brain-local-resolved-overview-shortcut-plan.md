# v77：InnerBrain 本机已处理指定文件视图当前文件总览入口方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v76 本机文件失败视图当前文件总览入口，明确 `0.73.0` 的本机已处理指定文件视图当前文件总览入口。

## 目标

`0.73.0` 在 `/inner-brain-eval-local-resolved 文件名` 展示指定本机 evaluation 文件已处理样本后，直接提示 `/inner-brain-eval-local-file 当前文件名`。用户查看当前文件已通过样本后，可以回到同一 JSONL 文件的通过/失败总览，再决定继续看待处理失败或导出报告。

## 范围

- 指定文件已处理视图反馈继续保留：
  - `/inner-brain-eval-local-file-failed 当前文件名`
  - `/inner-brain-eval-local-report 当前文件名`（仅同文件仍有待处理失败时）
  - `/inner-brain-eval-local-resolved`
  - `/inner-brain-eval-local-failed`
- 指定文件已处理视图反馈新增：
  - `/inner-brain-eval-local-file 当前文件名`
- 全量已处理视图反馈保持原样，继续列出可查看文件候选和同文件待处理/报告入口。
- 不新增命令，继续复用既有 `/inner-brain-eval-local-file [文件名]`。
- 不修改评估主体、已处理样本筛选、失败修复建议、报告正文、训练样本写入或本机 evaluation JSONL payload。

## 验收

- RED：`test_inner_brain_eval_local_resolved_command_can_filter_local_file` 先失败，证明指定文件已处理视图缺少当前文件总览入口。
- GREEN：实现后目标测试通过，指定文件已处理视图包含 `/inner-brain-eval-local-file real-log.jsonl`。
- 回归：运行 `tests.test_agent`、`tests.test_project_metadata` 和全量 `unittest discover`。
- 打包：构建 Windows 安装包并验证源码 smoke、打包后 exe smoke、安装脚本版本号和 Markdown 本地链接。
