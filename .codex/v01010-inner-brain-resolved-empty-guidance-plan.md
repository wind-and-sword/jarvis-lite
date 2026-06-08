# 0.101.0 InnerBrain 本机已处理空视图行动提示实施计划

> 日期：2026-06-03
> 执行者：Codex
> 依据：`.codex/context-scan-v01010-inner-brain-resolved-empty-guidance.json`

## 目标

在 `/inner-brain-eval-local-resolved [文件名]` 或全量已处理视图没有任何已通过样本时，除 `- 无` 外追加行动提示，说明该视图只显示已通过样本，并引导用户先查看待处理失败样本或补充本机 evaluation 样本。

## 设计

- 推荐方案：在 `describe_inner_brain_resolved_evaluation()` 的 `not report.passed_case_results` 分支追加提示文案。优点是函数层和 Agent 命令层共享同一结果，范围最小。
- 备选方案一：在 `JarvisAgent._inner_brain_local_resolved_evaluation()` 里根据报告状态追加提示。缺点是函数层描述和命令层输出不一致。
- 备选方案二：改写后续处理链接。缺点是会影响已有入口排序和报告入口覆盖，不符合本轮小步收口目标。

## 执行步骤

1. 在 `tests/test_inner_brain.py` 的空已处理样本测试中新增提示断言。
2. 在 `tests/test_agent.py` 的 `/inner-brain-eval-local-resolved failed-log.jsonl` 空已处理样本测试中新增提示断言。
3. 将 `tests/test_project_metadata.py` 的 `RELEASE_VERSION` 提升到 `0.101.0`，将更新清单夹具提升到 `0.101.1`。
4. 运行目标测试确认 RED，失败原因应为缺少提示和版本仍为 `0.100.0`。
5. 在 `src/jarvis_lite/inner_brain.py` 空已处理样本分支追加：`提示：这里只显示已通过样本；暂无已处理样本时，请先查看待处理失败样本或补充本机 evaluation 样本。`
6. 将 `pyproject.toml` 和 `src/jarvis_lite/__init__.py` 提升到 `0.101.0`。
7. 同步 README、`word/PROJECT-PLAN.md`、计划索引、进度、文档索引和验证记录。
8. 执行目标测试、相邻回归、全量回归、源码 smoke、安装包构建、版本化安装包、打包后 smoke、静态检查、Markdown 链接、密钥扫描、README BOM、本地配置和临时报告检查。
9. 写入 `.codex/testing.md`、`.codex/review-report.md`、`.codex/operations-log.md`，只暂存公开文件并本地提交。

## 验收

- RED：新增提示断言和版本一致性测试先失败。
- GREEN：目标测试通过，响应包含 `提示：这里只显示已通过样本；暂无已处理样本时，请先查看待处理失败样本或补充本机 evaluation 样本。`
- 回归：相邻回归、全量 `unittest`、源码 smoke、安装包构建、打包后 smoke、静态检查、Markdown 链接检查、密钥扫描和 README BOM 检查通过。
