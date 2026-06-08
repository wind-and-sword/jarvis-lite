# 经验记忆第一版计划

> 日期：2026-05-21
> 执行者：Codex

## 目标

把“可复用流程经验”从身份/偏好长期记忆中拆出来，支持用户明确记录和查看经验，为后续让助手学习常用表达、常用流程打基础。

## 范围

- 新增 `memory/experiences.md` 作为经验记忆文件。
- 新增 `/experience 经验内容` 写入经验。
- 新增 `/experiences` 查看经验。
- 支持自然语言“记录经验：...”和“记住这个经验：...”。
- 支持自然语言“查看经验记忆”“经验记忆”。

## 非目标

- 不自动抽取所有任务日志。
- 不调用大模型总结经验。
- 不做经验搜索、评分、过期或分类。
- 不改变现有 `/remember` 和身份记忆行为。

## 验收

- 经验文件缺失时，查看经验返回清晰空状态。
- 写入经验会创建 `memory/experiences.md`，重复经验不重复写入。
- `/experience`、`/experiences` 和自然语言记录/查看都可用。
- `tests.test_memory`、`tests.test_agent`、全量 `unittest discover`、桌面 smoke 和 `git diff --check` 通过。
