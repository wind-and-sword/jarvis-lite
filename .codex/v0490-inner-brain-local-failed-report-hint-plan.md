# 0.49.0 InnerBrain 本机失败视图导出报告提示计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

当用户查看本机失败评估视图时，如果当前视图确实包含失败样本，响应要直接提示可导出 Markdown 失败报告，方便从列表视图切到更完整的报告治理入口。

## 边界

- 不新增命令。
- 不改变导出的 `word/inner-brain-evaluation-report.md` 内容。
- 不改变评估样本描述主体。
- 不自动运行报告导出。
- 不自动训练、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 evaluation JSONL payload、去重键或保存路径。

## 任务

- [x] RED：新增本机失败视图导出报告提示测试和版本一致性测试。
- [x] GREEN：在本机失败视图响应中追加导出报告提示。
- [x] 更新版本到 `0.49.0`，更新 update fixture 到 `0.49.1`。
- [x] 更新 README、PROJECT-PLAN、v53 方案、进度和验证记录。
- [x] 运行目标、相邻回归、全量 unittest、源码 smoke、安装包构建、打包 exe smoke、静态检查、Markdown 链接、敏感扫描。
- [x] 提交到本地仓库。
