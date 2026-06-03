# v107：InnerBrain PROJECT-PLAN 已处理空视图主干同步方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v106 README 已处理空视图概要同步，明确 `0.103.0` 的 PROJECT-PLAN 主干同步。

## 目标

`0.103.0` 把本机已处理空视图行动提示同步到 `word/PROJECT-PLAN.md` 的“InnerBrain 可观察与样本闭环”主干描述。这样项目方案入口本身也能说明 `/inner-brain-eval-local-resolved [文件名]` 在暂无已处理样本时会提示这里只显示已通过样本，并引导查看待处理失败或补充本机 evaluation 样本。

## 范围

- 修改 `word/PROJECT-PLAN.md` 的 InnerBrain 可观察与样本闭环主干描述。
- 新增 PROJECT-PLAN 主干概要一致性测试，限定检查该 bullet，避免只由 README 或历史里程碑长段覆盖。
- 项目版本提升到 `0.103.0`，更新更新清单测试夹具到 `0.103.1`。
- 同步 README 安装版本、PROJECT-PLAN、计划索引、进度和验证记录。

## 非目标

- 不改变 `/inner-brain-eval-local-resolved [文件名]` 的运行时输出。
- 不改变已处理样本筛选、排序、文件候选、报告入口或后续处理链接。
- 不改变本机 evaluation JSONL payload、报告正文、报告路径或训练样本写入。

## 验收

- RED：PROJECT-PLAN 主干概要同步断言和版本一致性断言先失败。
- GREEN：实现后目标测试通过，PROJECT-PLAN 主干概要包含本机已处理空视图行动提示摘要。
- 回归：相邻回归、全量 `unittest`、源码 smoke、安装包构建、打包后 smoke、静态检查、Markdown 链接检查和 README BOM 检查通过。
