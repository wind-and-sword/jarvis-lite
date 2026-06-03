# v106：InnerBrain README 已处理空视图概要同步方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v105 本机已处理空视图行动提示，明确 `0.102.0` 的 README 顶部概要同步。

## 目标

`0.102.0` 把本机已处理空视图行动提示同步到 README 顶部“当前能力”的 InnerBrain 样本闭环概要。这样用户先读 README 能看到 `/inner-brain-eval-local-resolved [文件名]` 在暂无已处理样本时会说明这里只显示已通过样本，并引导查看待处理失败或补充本机 evaluation 样本。

## 范围

- 修改 README 顶部 InnerBrain 样本闭环概要。
- 新增 README 概要一致性测试，限定检查该 bullet，避免安装说明长段误判。
- 项目版本提升到 `0.102.0`，更新更新清单测试夹具到 `0.102.1`。
- 同步 PROJECT-PLAN、计划索引、进度和验证记录。

## 非目标

- 不改变 `/inner-brain-eval-local-resolved [文件名]` 的运行时输出。
- 不改变已处理样本筛选、排序、文件候选、报告入口或后续处理链接。
- 不改变本机 evaluation JSONL payload、报告正文、报告路径或训练样本写入。

## 验收

- RED：README 顶部概要同步断言和版本一致性断言先失败。
- GREEN：实现后目标测试通过，README 顶部概要包含本机已处理空视图行动提示摘要。
- 回归：相邻回归、全量 `unittest`、源码 smoke、安装包构建、打包后 smoke、静态检查、Markdown 链接检查和 README BOM 检查通过。
