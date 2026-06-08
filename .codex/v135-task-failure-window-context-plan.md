# v135：任务失败复盘窗口与授权摘要第一阶段实施计划

> 日期：2026-06-04
> 执行者：Codex

## 目标

- `/task-fail` 与 `/task-fail-capture` 记录失败时，保存当前只读窗口摘要。
- 失败复盘正文和 `/task-status` 最近失败记录展示路由摘要、授权摘要和窗口上下文。
- 运行态读取兼容旧数据；旧失败记录没有窗口字段时按空值处理。

## 非目标

- 不切换窗口、不点击、不输入、不自动重新执行外部动作。
- 不把窗口感知变成自然语言自动任务编排。
- 不变更截图/OCR 的真实采集边界。

## 实施步骤

1. RED：补 `task_state`、`agent`、`window_state` 和版本一致性测试，确认当前缺少窗口上下文与版本更新。
2. GREEN：在 `window_state.py` 增加紧凑前台窗口摘要 helper。
3. GREEN：在 `RuntimeTaskFailureContext` 增加 `window_context` 可选字段，并更新 JSON 读写。
4. GREEN：让 `record_task_failure()` 和 `record_task_failure_with_screen_ocr()` 接收并展示 `window_context`。
5. GREEN：Agent 显式失败命令调用只读窗口摘要 helper。
6. 同步版本、README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
7. 运行目标测试、相邻回归、全量 unittest、smoke、打包和静态检查。

## 验收标准

- 普通失败复盘包含 `窗口上下文：当前窗口：...`。
- `/task-status` 最近失败记录包含 `路由：...`、`授权：...` 和 `窗口：...`。
- `/task-fail-capture` 继续记录截图/OCR，同时也携带窗口上下文。
- `0.130.0` 的目标测试、相邻回归、全量回归和安装包 smoke 通过。
