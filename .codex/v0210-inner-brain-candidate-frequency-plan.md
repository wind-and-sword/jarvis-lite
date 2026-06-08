# 0.21.0 InnerBrain 候选频次排序计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

让 `/inner-brain-candidates` 优先展示重复出现的 fallback 候选，帮助用户先训练高频自然语言缺口。

## 边界

- 只统计最近 5 条路由历史中的候选，不新增长期统计存储。
- 只按完全相同的 prompt 聚合，不做相似文本聚类。
- 不自动训练，不自动推断命令或 intent。
- `/inner-brain-teach-candidate` 和 `/inner-brain-label-candidate` 使用聚合排序后的编号。

## 验收

- 重复候选显示 `出现次数：N`。
- 重复候选即使不是最新输入，也排在单次候选前。
- 按编号教学和按编号标注都能选中频次排序后的第 1 条候选。
- 项目版本、README、PROJECT-PLAN、验证记录和安装包同步到 `0.21.0`。
