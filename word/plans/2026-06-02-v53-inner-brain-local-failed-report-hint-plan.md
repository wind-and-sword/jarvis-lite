# Jarvis Lite v53：InnerBrain 本机失败视图导出报告提示方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v52 本机失败评估报告导出后续处理提示，明确 `0.49.0` 的本机失败视图导出报告提示闭环。

## 目标

`0.49.0` 在用户查看本机失败评估视图后，直接提示可导出 Markdown 报告。用户通过 `/inner-brain-eval-local-failed` 或 `/inner-brain-eval-local-file-failed 文件名` 看到失败样本和修复建议后，可以马上知道如何导出全部本机失败报告或当前文件失败报告。

## 边界

- 不新增命令。
- 不改变导出的 Markdown 报告内容。
- 不改变评估样本描述主体。
- 不自动运行报告导出。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 evaluation JSONL payload、去重键或保存路径。

## 实现要点

- 继续复用 `describe_inner_brain_evaluation()` 生成评估主体。
- 在 Agent 本机失败视图响应层追加 `后续处理：`。
- 全部本机失败视图有失败样本时提示：
  - `/inner-brain-eval-local-report`
  - `/inner-brain-eval-local-report 文件名`
- 指定文件失败视图有失败样本时提示：
  - `/inner-brain-eval-local-report <当前文件名>`
  - `/inner-brain-eval-local-report`
- 本机样本为空或没有失败样本时，不追加导出报告提示，避免遮挡已有空样本或无失败提示。

## 验证

- RED：新增 Agent 本机失败视图导出报告提示测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 用户沉淀真实本机 evaluation 样本后，再根据失败报告中的高频失败维度补 seed/runtime 样本、槽位补全或轻量评分补偿。
