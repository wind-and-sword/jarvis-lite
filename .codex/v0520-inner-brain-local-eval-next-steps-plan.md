# 0.52.0 InnerBrain 本机评估全量视图后续处理提示计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

让 `/inner-brain-eval-local` 和 `/inner-brain-eval-local-file 文件名` 在展示本机 evaluation 全量样本后，直接提示只看失败、只看已处理和文件聚焦入口。这样用户无需记住 0.51.0 新增的 `/inner-brain-eval-local-resolved [文件名]`，可以从全量视图自然切换到治理视图。

## 约束

- 只改变 Agent 响应文本。
- 不新增评估数据结构，不改变 `describe_inner_brain_evaluation()` 输出主体。
- 不自动训练、不写 `data/inner-brain/training/runtime.jsonl`。
- 不改变本机 evaluation JSONL payload、保存路径或报告导出内容。

## 执行步骤

1. RED：新增 `/inner-brain-eval-local` 后续处理提示测试，断言有样本时提示失败视图和已处理清单。
2. RED：新增 `/inner-brain-eval-local-file 文件名` 后续处理提示测试，断言当前文件失败和当前文件已处理命令。
3. RED：补充空样本负向断言，确保空本机 evaluation 不追加全量后续处理。
4. RED：版本一致性测试期望 `0.52.0`，更新检测 fixture 期望 `0.52.1`。
5. GREEN：新增 Agent 包装函数，`report.total_count > 0` 时追加 `后续处理：`。
6. 文档：同步 README、PROJECT-PLAN、plans README、文档索引、进度和验证记录。
7. 验证：目标测试、InnerBrain+Agent 相邻回归、全量 unittest、桌面 smoke、安装包构建、打包后 exe smoke、静态和链接检查。
8. 提交：本地提交 `feat: 提示本机评估全量视图后续处理 0.52.0`。
