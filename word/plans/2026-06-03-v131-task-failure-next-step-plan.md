# v131：任务失败复盘行动建议第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v130 任务执行结果摘要采集第一阶段，继续深化 Jarvis Lite 1.0 验收线中的任务状态和失败复盘。

## 目标

- 普通 `/task-fail 失败原因` 记录失败时，如果尚未采集屏幕/OCR 上下文，下一步建议明确提示可执行 `/task-fail-capture 失败原因` 补充截图和 OCR。
- 已通过 `/task-fail-capture` 显式采集截图/OCR 的失败记录，不再反复提示同一采集命令，而是保留恢复、取消或重开任务建议。
- `/task-status` 的最近失败记录持久化展示同一下一步建议，便于重启后继续处理。

## 非目标

- 不自动截图、不自动 OCR、不自动重新执行外部动作。
- 不在失败后自动调用 `/task-fail-capture`，只给出可复制的显式入口。
- 不新增任务编排器，不自动重放失败前命令。
- 不从失败复盘自动写入 InnerBrain 样本、联系人、授权规则或长期配置。

## 实施步骤

1. 扩展 `tests/test_task_state.py`，先验证普通失败记录会提示 `/task-fail-capture 失败原因`，且状态视图持久化该建议。
2. 扩展 `tests/test_task_state.py`，验证已采集截图/OCR 的失败记录不再提示同一采集命令。
3. 扩展 `tests/test_agent.py`，验证 Agent `/task-fail` 输出和重启后的 `/task-status` 都展示补充截图/OCR 建议。
4. 将版本元数据测试期望提升到 `0.126.0`，验证 RED。
5. 扩展 `src/jarvis_lite/task_state.py`，按屏幕/OCR 上下文生成动态下一步建议并写入失败记录。
6. 同步 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README、PROJECT-PLAN、方案索引、文档索引、进度与验证记录。
7. 运行目标测试、相邻回归、全量 unittest、临时项目 smoke、桌面 smoke、打包后 smoke 和静态检查。

## 验收标准

- `/task-fail 目标测试失败` 输出 `补充截图/OCR：/task-fail-capture 目标测试失败`。
- 重启后 `/task-status` 的最近失败记录仍展示该建议。
- `/task-fail-capture 打包后 smoke 失败` 的失败记录不再提示 `/task-fail-capture 打包后 smoke 失败`。
- 输出继续明确“不自动截图、不自动 OCR、不自动重新执行外部动作”。
