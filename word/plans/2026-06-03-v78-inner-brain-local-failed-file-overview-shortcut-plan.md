# v78：InnerBrain 本机失败视图失败文件分组当前文件总览入口方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v77 本机已处理指定文件视图当前文件总览入口，明确 `0.74.0` 的本机失败视图失败文件分组当前文件总览入口。

## 目标

`0.74.0` 在 `/inner-brain-eval-local-failed` 的 `失败文件：` 分组中，为每个失败来源 JSONL 文件追加 `/inner-brain-eval-local-file 当前文件名`。用户在失败总览里看到某个失败文件后，可以直接进入同文件通过/失败总览，再决定继续看待处理失败、已处理样本或导出报告。

## 范围

- 失败文件分组候选行继续保留：
  - `/inner-brain-eval-local-file-failed 当前文件名`
  - `/inner-brain-eval-local-report 当前文件名`
- 失败文件分组候选行新增：
  - `/inner-brain-eval-local-file 当前文件名`
- 指定文件失败视图、指定文件已处理视图和报告导出反馈保持既有入口。
- 不新增命令，继续复用既有 `/inner-brain-eval-local-file [文件名]`。
- 不修改评估主体、失败排序、失败修复建议、报告正文、训练样本写入或本机 evaluation JSONL payload。

## 验收

- RED：失败文件分组相关 Agent 和 InnerBrain 测试先失败，证明候选行缺少当前文件总览入口。
- GREEN：实现后目标测试通过，失败文件分组行包含 `总览：/inner-brain-eval-local-file failed-log.jsonl`。
- 回归：运行 `tests.test_agent`、`tests.test_inner_brain`、`tests.test_project_metadata` 和全量 `unittest discover`。
- 打包：构建 Windows 安装包并验证源码 smoke、打包后 exe smoke、安装脚本版本号和 Markdown 本地链接。
