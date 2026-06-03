# v105：InnerBrain 本机已处理空视图行动提示方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v104 本机空评估视图补样本写入提示，明确 `0.101.0` 的本机已处理空视图行动提示。

## 目标

`0.101.0` 在本机 evaluation 已处理样本视图为空时追加提示说明该视图只显示已通过样本，并引导用户先查看待处理失败样本或补充本机 evaluation 样本。这样用户在 `/inner-brain-eval-local-resolved [文件名]` 看到 `- 无` 时，能直接理解当前没有已通过样本，而不是误以为本机 evaluation 没有样本或命令失效。

## 范围

- 修改 `describe_inner_brain_resolved_evaluation()` 的空已处理样本分支。
- 新增函数层和 Agent 命令层断言，覆盖空已处理样本提示。
- 项目版本提升到 `0.101.0`，更新更新清单测试夹具到 `0.101.1`。
- 同步 README、PROJECT-PLAN、计划索引、进度和验证记录。

## 非目标

- 不改变 `/inner-brain-eval-local-resolved [文件名]` 的只读定位。
- 不改变已处理样本筛选、排序、文件候选、报告入口或后续处理链接。
- 不新增按任意 JSONL 文件写入 evaluation 样本的命令。
- 不改变本机 evaluation JSONL payload、报告正文、报告路径或训练样本写入。

## 验收

- RED：空已处理样本提示断言和版本一致性断言先失败。
- GREEN：实现后目标测试通过，响应包含 `提示：这里只显示已通过样本；暂无已处理样本时，请先查看待处理失败样本或补充本机 evaluation 样本。`
- 回归：相邻回归、全量 `unittest`、源码 smoke、安装包构建、打包后 smoke、静态检查、Markdown 链接检查和 README BOM 检查通过。
