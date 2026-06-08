# 0.103.0 InnerBrain PROJECT-PLAN 已处理空视图主干同步实施计划

> 日期：2026-06-03
> 执行者：Codex
> 依据：`.codex/context-scan-v01030-inner-brain-project-plan-resolved-empty-summary.json`

## 目标

把 `0.101.0` 的本机已处理空视图行动提示同步到 `word/PROJECT-PLAN.md` 的“InnerBrain 可观察与样本闭环”主干描述，和 `0.102.0` 的 README 顶部概要保持一致。

## 设计

- 推荐方案：在 `tests/test_project_metadata.py` 抽取 PROJECT-PLAN 的 `- InnerBrain 可观察与样本闭环：` bullet，并断言其中包含“暂无已处理样本时会提示这里只显示已通过样本”和“引导查看待处理失败或补充本机 evaluation 样本”。然后只改 PROJECT-PLAN 主干文档和版本文档。
- 备选方案一：只更新 PROJECT-PLAN 不加测试。缺点是后续主干描述容易再次落后。
- 备选方案二：修改运行时代码或命令反馈。缺点是 0.101.0 已完成运行时行为，本轮不需要扩大范围。

## 执行步骤

1. 新增 PROJECT-PLAN 主干概要一致性测试，确认 RED。
2. 将 `RELEASE_VERSION` 提升到 `0.103.0`，更新更新清单测试夹具到 `0.103.1`。
3. 修改 `word/PROJECT-PLAN.md` 的 InnerBrain 可观察与样本闭环 bullet，补充已处理空视图行动提示摘要。
4. 将 `pyproject.toml` 和 `src/jarvis_lite/__init__.py` 提升到 `0.103.0`。
5. 同步 README 安装版本、PROJECT-PLAN 里程碑、计划索引、进度、文档索引和验证记录。
6. 执行目标测试、相邻回归、全量 `unittest`、源码 smoke、安装包构建、版本化安装包、打包后 smoke、静态检查、Markdown 链接、密钥扫描、README BOM、本地配置和临时报告检查。
7. 写入 `.codex/testing.md`、`.codex/review-report.md`、`.codex/operations-log.md`，只暂存公开文件并本地提交。

## 验收

- RED：PROJECT-PLAN 主干概要同步断言和版本一致性断言先失败。
- GREEN：实现后目标测试通过，PROJECT-PLAN 主干 InnerBrain 可观察与样本闭环概要包含已处理空视图行动提示摘要。
- 回归：相邻回归、全量 `unittest`、源码 smoke、安装包构建、打包后 smoke、静态检查、Markdown 链接检查和 README BOM 检查通过。
