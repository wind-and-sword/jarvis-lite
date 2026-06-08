# 最近建议持久化第一版计划

> 日期：2026-05-22
> 执行者：Codex

## 目标

让用户生成经验建议后，即使重新创建 `JarvisAgent` 实例，也可以继续说“查看第一条建议”，读取上一轮建议中的命令文本。

## 设计

- `RuntimeContext` 增加 `recent_advice_suggestions: tuple[str, ...]`。
- `load_runtime_context()` 读取可选 JSON 列表，缺失、类型错误或损坏文件继续回退为空上下文。
- `save_runtime_context()` 写出 `recent_advice_suggestions`，保持和已有最近资料、目录、搜索结果同一个运行态文件。
- `JarvisAgent.__init__()` 从运行态上下文恢复 `_recent_advice_suggestions`。
- `_remember_recent_advice_suggestions()` 写入内存字段后调用 `_save_runtime_context()`。
- `_save_runtime_context()` 写入完整 `RuntimeContext`，避免最近建议更新时丢失其他最近上下文。

## 验收

- 新增测试证明 `/experience-advice 导入资料` 后，新建 Agent 仍可处理“查看第一条建议”。
- 保持没有最近建议时的现有提示。
- 运行 Agent 专项测试、全量 unittest、桌面 smoke 和 `git diff --check`。

## 非目标

- 不自动执行建议命令。
- 不替换建议中的占位符参数。
- 不在最近上下文状态中展示最近建议数量。
