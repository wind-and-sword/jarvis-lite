# v135：任务失败复盘窗口与授权摘要第一阶段实施计划

> 日期：2026-06-04
> 执行者：Codex
> 说明：本文承接 v132 任务失败复盘样本建议第一阶段和 v108 Jarvis Lite 1.0 验收线，补齐失败复盘中当前窗口、路由和授权摘要的可读上下文。

## 目标

- `/task-fail 失败原因` 记录失败时，保存当前只读窗口摘要。
- `/task-fail-capture 失败原因 [lang=chi_sim+eng]` 继续保存截图/OCR 失败上下文，同时也保存当前只读窗口摘要。
- 失败复盘正文展示路由摘要、授权摘要和窗口上下文。
- `/task-status` 的最近失败记录展示同一批复盘上下文，便于任务中断后恢复判断。

## 非目标

- 不切换窗口、不点击、不输入、不自动重新执行外部动作。
- 不自动截图或自动 OCR 普通 `/task-fail`。
- 不接入自然语言自动任务编排。
- 不改变已有 `recent_task_failures` 历史数据的读取兼容性。

## 实施步骤

1. 在 `tests/test_window_state.py` 增加 RED：只读窗口快照可格式化为任务失败复盘使用的紧凑前台窗口摘要。
2. 在 `tests/test_task_state.py` 增加 RED：`record_task_failure()` 接收并持久化 `window_context`，失败复盘和状态页展示路由、授权和窗口上下文。
3. 在 `tests/test_agent.py` 增加 RED：Agent `/task-fail` 调用只读窗口摘要并写入失败复盘；`/task-fail-capture` 调用失败记录时也传入窗口上下文。
4. 将版本一致性目标提升到 `0.130.0` 并确认 RED。
5. 在 `window_state.py` 增加 `describe_task_window_context()`，复用现有窗口快照，不新增窗口枚举实现。
6. 在 `RuntimeTaskFailureContext` 增加可选 `window_context` 字段，并更新 JSON 读写。
7. 在 `task_state.py` 和 `agent.py` 接入窗口上下文展示和传递。
8. 同步版本、README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
9. 运行目标测试、相邻回归、全量 unittest、命令行 smoke、源码桌面 smoke、安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 任务失败复盘正文包含 `窗口上下文：当前窗口：...`。
- `/task-status` 最近失败记录包含 `路由：...`、`授权：...` 和 `窗口：...`。
- 旧运行态失败记录缺少 `window_context` 时仍能正常读取。
- 当前阶段仍只做只读窗口观察，不切换窗口、不点击、不输入、不重放外部动作。
