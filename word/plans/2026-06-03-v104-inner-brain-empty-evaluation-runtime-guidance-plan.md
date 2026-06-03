# v104：InnerBrain 本机空评估视图补样本写入提示方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v103 本机报告空筛选文件补样本写入提示，明确 `0.100.0` 的本机空评估视图补样本写入提示。

## 目标

`0.100.0` 在本机 evaluation 评估视图为空时追加提示说明补样本命令默认写入 `runtime.jsonl`。这样用户在 `/inner-brain-eval-local`、`/inner-brain-eval-local-failed` 或空文件筛选视图看到添加入口时，能直接理解下一步样本会落到默认本机 evaluation 文件，而不是误以为会写入任意筛选文件或训练样本。

## 范围

- 修改 `describe_inner_brain_evaluation()` 的空本机评估样本分支。
- 新增函数层和 Agent 命令层断言，覆盖空本机 evaluation 引导。
- 项目版本提升到 `0.100.0`，更新更新清单测试夹具到 `0.100.1`。
- 同步 README、PROJECT-PLAN、计划索引、进度和验证记录。

## 非目标

- 不新增按任意 JSONL 文件写入 evaluation 样本的命令。
- 不改变 `/inner-brain-eval-add`、`/inner-brain-eval-label`、候选写入命令的默认写入目标。
- 不改变报告正文、报告路径、本机 evaluation JSONL payload 或训练样本写入。

## 验收

- RED：空本机 evaluation 引导和版本一致性断言先失败。
- GREEN：实现后目标测试通过，响应包含 `提示：补样本命令默认写入 runtime.jsonl。`
- 回归：相邻回归、全量 `unittest`、源码 smoke、安装包构建、打包后 smoke、静态检查、Markdown 链接检查和 README BOM 检查通过。
