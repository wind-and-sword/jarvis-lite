# 0.47.0 InnerBrain 本机评估样本保存后续验证提示计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

当用户通过 `/inner-brain-eval-add`、`/inner-brain-eval-label`、`/inner-brain-eval-add-candidate` 或 `/inner-brain-eval-label-candidate` 保存本机 evaluation 样本后，返回信息要直接给出后续验证入口，方便用户马上复跑本机评估、只看失败、按 `runtime.jsonl` 聚焦或导出失败报告。

## 边界

- 不新增命令。
- 不自动运行评估。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 evaluation JSONL payload、去重键或保存路径。
- 不改变候选保存后仍保留的语义。

## 任务

- [x] RED：新增保存反馈后续验证命令测试和版本一致性测试。
- [x] GREEN：在 `_describe_inner_brain_evaluation_case_save()` 追加后续验证提示。
- [x] 更新版本到 `0.47.0`，更新 update fixture 到 `0.47.1`。
- [x] 更新 README、PROJECT-PLAN、v51 方案、进度和验证记录。
- [x] 运行目标、相邻回归、全量 unittest、源码 smoke、安装包构建、打包 exe smoke、静态检查、Markdown 链接、敏感扫描。
- [x] 提交到本地仓库。
