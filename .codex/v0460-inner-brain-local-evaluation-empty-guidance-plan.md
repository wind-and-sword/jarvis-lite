# 0.46.0 InnerBrain 本机评估空样本引导计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

当本机 `data/inner-brain/evaluation/*.jsonl` 为空时，`/inner-brain-eval-local` 和 `/inner-brain-eval-local-failed` 不只显示 `0/0` 与 `- 无`，还要明确提示当前没有本机评估样本，并列出只写 evaluation、不自动训练的添加入口。

## 边界

- 不新增命令。
- 不写 `data/inner-brain/training/runtime.jsonl`。
- 不自动采纳、不自动训练。
- 不改变 evaluation JSONL payload。
- 不改变 seed 评估语义。
- 不基于测试构造失败调整知识库状态/摘要 seed 样本。

## 任务

- [x] RED：新增 InnerBrain 空本机评估描述测试、Agent 本机失败空样本命令测试和版本一致性测试。
- [x] GREEN：在评估描述中为 `local_evaluation` 空结果追加本机评估样本空状态和添加入口。
- [x] 更新版本到 `0.46.0`，更新 update fixture 到 `0.46.1`。
- [x] 更新 README、PROJECT-PLAN、v50 方案、进度和验证记录。
- [x] 运行目标、相邻回归、全量 unittest、源码 smoke、安装包构建、打包 exe smoke、静态检查、Markdown 链接、敏感扫描。
- [x] 提交到本地仓库。

## 提交

- 本地提交：`8c6f8c5 feat: 引导本机评估空样本添加 0.46.0`
