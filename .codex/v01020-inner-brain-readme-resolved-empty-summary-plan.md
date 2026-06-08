# 0.102.0 InnerBrain README 已处理空视图概要同步实施计划

> 日期：2026-06-03
> 执行者：Codex
> 依据：`.codex/context-scan-v01020-inner-brain-readme-resolved-empty-summary.json`

## 目标

把 `0.101.0` 的本机已处理空视图行动提示同步到 README 顶部“当前能力”里的 InnerBrain 样本闭环概要，避免只有安装说明长段记录该能力。

## 设计

- 推荐方案：在 `tests/test_project_metadata.py` 抽取 README 的 `- InnerBrain 样本闭环：` bullet，并断言其中包含“暂无已处理样本时会提示这里只显示已通过样本”摘要。然后只改 README 顶部概要和版本文档。
- 备选方案一：只更新 README 不加测试。缺点是后续概要容易再次落后。
- 备选方案二：修改运行时代码或命令反馈。缺点是 0.101.0 已完成运行时行为，本轮不需要扩大范围。

## 执行步骤

1. 新增 README 顶部能力概要一致性测试，确认 RED。
2. 将 `RELEASE_VERSION` 提升到 `0.102.0`，更新更新清单测试夹具到 `0.102.1`。
3. 修改 README 顶部 InnerBrain 样本闭环 bullet，补充已处理空视图行动提示摘要，并保持 README BOM。
4. 将 `pyproject.toml` 和 `src/jarvis_lite/__init__.py` 提升到 `0.102.0`。
5. 同步 README 安装版本、PROJECT-PLAN、计划索引、进度、文档索引和验证记录。
6. 执行目标测试、相邻回归、全量回归、源码 smoke、安装包构建、版本化安装包、打包后 smoke、静态检查、Markdown 链接、密钥扫描、README BOM、本地配置和临时报告检查。
7. 写入 `.codex/testing.md`、`.codex/review-report.md`、`.codex/operations-log.md`，只暂存公开文件并本地提交。

## 验收

- RED：README 顶部概要同步断言和版本一致性断言先失败。
- GREEN：实现后目标测试通过，README 顶部 InnerBrain 样本闭环概要包含已处理空视图行动提示摘要。
- 回归：相邻回归、全量 `unittest`、源码 smoke、安装包构建、打包后 smoke、静态检查、Markdown 链接检查和 README BOM 检查通过。
