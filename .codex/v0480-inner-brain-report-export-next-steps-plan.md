# 0.48.0 InnerBrain 本机失败评估报告导出后续处理提示计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

当用户执行 `/inner-brain-eval-local-report [文件名]` 导出本机失败评估报告后，响应要直接提示下一步处理入口，方便继续查看失败样本、按文件聚焦失败和补充本机 evaluation 样本。

## 边界

- 不新增命令。
- 不改变导出的 `word/inner-brain-evaluation-report.md` 内容。
- 不自动运行评估。
- 不自动训练、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 evaluation JSONL payload、去重键或保存路径。

## 任务

- [x] RED：新增报告导出响应后续处理提示测试和版本一致性测试。
- [x] GREEN：在 `_export_inner_brain_local_evaluation_report()` 追加后续处理提示。
- [x] 更新版本到 `0.48.0`，更新 update fixture 到 `0.48.1`。
- [x] 更新 README、PROJECT-PLAN、v52 方案、进度和验证记录。
- [x] 运行目标、相邻回归、全量 unittest、源码 smoke、安装包构建、打包 exe smoke、静态检查、Markdown 链接、敏感扫描。
- [x] 提交到本地仓库。
