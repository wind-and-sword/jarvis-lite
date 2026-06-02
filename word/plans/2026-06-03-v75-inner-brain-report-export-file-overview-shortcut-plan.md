# v75：InnerBrain 本机失败报告导出反馈当前文件总览入口方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v74 本机失败报告导出反馈当前文件已处理入口，明确 `0.71.0` 的本机失败报告导出反馈当前文件总览入口。

## 目标

`0.71.0` 在 `/inner-brain-eval-local-report 文件名` 导出指定本机 evaluation 文件失败报告后，直接提示 `/inner-brain-eval-local-file 当前文件名`。用户看完当前文件失败报告后，可以回到同一 JSONL 文件的通过/失败总览，再决定继续看失败、看已处理或重新导出报告。

## 范围

- 指定文件报告导出反馈继续保留：
  - `/inner-brain-eval-local-file-failed 当前文件名`
  - `/inner-brain-eval-local-resolved 当前文件名`
  - `/inner-brain-eval-local-failed`
- 指定文件报告导出反馈新增：
  - `/inner-brain-eval-local-file 当前文件名`
- 全量报告导出反馈保持原样，继续提示全部失败视图和按文件失败聚焦模板。
- 不新增命令，继续复用既有 `/inner-brain-eval-local-file [文件名]`。
- 不修改 Markdown 报告正文，不写训练样本，不改变本机 evaluation JSONL payload。

## 验收

- RED：`test_inner_brain_eval_local_report_command_can_filter_local_file` 先失败，证明指定文件报告导出反馈缺少当前文件总览入口。
- GREEN：实现后目标测试通过，指定文件报告导出反馈包含 `/inner-brain-eval-local-file failed-log.jsonl`。
- 回归：运行 `tests.test_agent`、`tests.test_project_metadata` 和全量 `unittest discover`。
- 打包：构建 Windows 安装包并验证源码 smoke、打包后 exe smoke、安装脚本版本号和 Markdown 本地链接。
