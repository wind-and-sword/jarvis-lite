# 2026-06-02 0.56.0 InnerBrain 本机失败视图失败文件汇总排序计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

让 `/inner-brain-eval-local-failed` 的 `失败文件：` 分组按失败数量优先展示，和 0.55.0 的全量可聚焦文件排序保持一致。

## 约束

- 不自动训练，不写 `data/inner-brain/training/runtime.jsonl`。
- 不改变本机 evaluation JSONL payload、保存路径、去重策略或评估报告数据结构。
- 只改变失败文件汇总的展示顺序。

## 实施步骤

1. RED：新增 InnerBrain formatter 排序测试、Agent 本机失败视图排序测试和版本一致性测试。
2. GREEN：在 failures-only 的失败文件分组输出前排序，版本提升到 `0.56.0`。
3. 文档：同步 README、PROJECT-PLAN、v60 方案、方案索引、进度和验证记录。
4. 验证：运行目标测试、InnerBrain + Agent 相邻回归、全量 unittest、桌面 smoke、安装包构建、打包 exe smoke、静态/链接/敏感检查。
5. 提交：本地提交 `feat: 优先展示本机失败评估文件 0.56.0`。
