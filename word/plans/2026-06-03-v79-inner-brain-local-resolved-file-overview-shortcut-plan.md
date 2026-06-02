# v79：InnerBrain 本机已处理视图文件候选当前文件总览入口方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v78 本机失败视图失败文件分组当前文件总览入口，明确 `0.75.0` 的本机已处理视图文件候选当前文件总览入口。

## 目标

`0.75.0` 在 `/inner-brain-eval-local-resolved` 的 `可查看文件：` 候选行中，为每个有已处理样本的来源 JSONL 文件追加 `/inner-brain-eval-local-file 当前文件名`。用户在已处理总览里看到某个文件后，可以直接回到同文件通过/失败总览，再决定继续看已处理样本、待处理失败或导出报告。

## 范围

- 已处理文件候选行继续保留：
  - `/inner-brain-eval-local-resolved 当前文件名`
  - 当同文件仍有待处理失败时的 `/inner-brain-eval-local-file-failed 当前文件名`
  - 当同文件仍有待处理失败时的 `/inner-brain-eval-local-report 当前文件名`
- 已处理文件候选行新增：
  - `/inner-brain-eval-local-file 当前文件名`
- 纯通过文件只显示同文件总览和同文件已处理入口，不追加待处理失败或报告入口。
- 指定文件已处理视图、失败视图、文件总览和报告导出反馈保持既有入口。
- 不新增命令，继续复用既有 `/inner-brain-eval-local-file [文件名]`。
- 不修改评估主体、已处理文件排序、失败修复建议、报告正文、训练样本写入或本机 evaluation JSONL payload。

## 验收

- RED：全量已处理视图文件候选相关 Agent 测试和版本一致性测试先失败，证明候选行缺少当前文件总览入口。
- GREEN：实现后目标测试通过，候选行包含 `总览：/inner-brain-eval-local-file real-log.jsonl` 和 `已处理：/inner-brain-eval-local-resolved real-log.jsonl`。
- 回归：运行 `tests.test_agent`、`tests.test_project_metadata` 和全量 `unittest discover`。
- 打包：构建 Windows 安装包并验证源码 smoke、打包后 exe smoke、安装脚本版本号和 Markdown 本地链接。
