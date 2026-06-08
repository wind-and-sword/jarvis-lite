# 0.100.0 InnerBrain 本机空评估视图补样本写入提示计划

> 日期：2026-06-03
> 执行者：Codex

## 目标

在本机 evaluation 样本为空时，让 `/inner-brain-eval-local`、`/inner-brain-eval-local-failed` 和空文件筛选视图的评估描述明确提示：补样本命令默认写入 `runtime.jsonl`。

## 设计

- 复用 `describe_inner_brain_evaluation()` 现有 `report.total_count == 0 and report.name.startswith("local_evaluation")` 分支。
- 在“不自动训练”说明后追加 `提示：补样本命令默认写入 runtime.jsonl。`
- 不新增命令，不支持任意文件写入，不改变 `/inner-brain-eval-add`、`/inner-brain-eval-label`、候选写入命令的保存目标。
- 项目版本提升到 `0.100.0`，更新更新清单测试夹具到 `0.100.1`。

## TDD

- RED：先在 InnerBrain 函数层和 Agent 命令层断言新增提示，并把版本一致性测试更新到 `0.100.0`，确认失败点来自缺少提示和旧版本。
- GREEN：实现提示和升版后，目标测试通过。
- 回归：运行 Agent + InnerBrain + ProjectMetadata 相邻回归、全量 unittest、源码 smoke、安装包构建、打包后 smoke、静态检查和文档链接检查。

## 约束

- 不改变训练样本写入路径。
- 不改变 evaluation JSONL payload。
- 不改变报告正文、报告路径或报告导出反馈。
- 不修改 README 之外的无关功能文案。
