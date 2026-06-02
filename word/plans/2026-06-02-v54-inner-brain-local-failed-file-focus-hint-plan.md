# Jarvis Lite v54：InnerBrain 本机失败视图文件聚焦提示方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v53 本机失败视图导出报告提示，明确 `0.50.0` 的本机失败视图文件聚焦提示闭环。

## 目标

`0.50.0` 在用户查看本机失败评估视图后，直接提示可按来源 JSONL 文件聚焦失败样本。用户通过 `/inner-brain-eval-local-failed` 看到失败文件分组后，可以马上知道如何执行 `/inner-brain-eval-local-file-failed 文件名`；用户通过 `/inner-brain-eval-local-file-failed 文件名` 聚焦单个文件后，也可以马上回到 `/inner-brain-eval-local-failed` 查看全部本机失败样本。

## 边界

- 不新增命令。
- 不改变导出的 Markdown 报告内容。
- 不改变评估样本描述主体。
- 不自动运行报告导出。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 evaluation JSONL payload、去重键或保存路径。

## 实现要点

- 继续复用 `JarvisAgent._describe_inner_brain_local_failed_evaluation()` 作为本机失败视图后续处理出口。
- 全部本机失败视图有失败样本时提示 `/inner-brain-eval-local-file-failed 文件名`。
- 指定文件失败视图有失败样本时提示 `/inner-brain-eval-local-failed`。
- 本机样本为空或没有失败样本时，不追加文件聚焦提示，避免遮挡已有空样本或无失败提示。

## 验证

- RED：新增 Agent 本机失败视图文件聚焦提示测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 用户沉淀真实本机 evaluation 样本后，再根据失败报告中的高频失败维度补 seed/runtime 样本、槽位补全或轻量评分补偿。
