# 最近建议编号查看第一版计划

> 日期：2026-05-22
> 执行者：Codex

## 目标

让用户在获得经验建议后，可以继续说“查看第一条建议”，明确拿到对应命令文本。

## 设计

- `JarvisAgent` 新增当前实例内 `_recent_advice_suggestions`。
- `_experience_advice()` 每次生成命令建议后更新该列表；没有命令建议时清空。
- `intent.py` 新增 `read_numbered_advice_suggestion` 意图。
- Agent 读取第 N 条建议时只返回命令文本，不自动执行。

## 非目标

- 不持久化最近建议。
- 不支持自动执行建议。
- 不解析建议参数，也不替换占位符。
