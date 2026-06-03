# v132：任务失败复盘样本建议第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v131 任务失败复盘行动建议第一阶段，继续深化 Jarvis Lite 1.0 验收线中的失败样本反向生成。

## 目标

- 任务失败复盘中如果存在最近自动采集的显式命令事件，输出可复制的 `/inner-brain-eval-add 原始输入 => /命令` 建议。
- `/task-status` 最近失败记录持久化展示同一类样本建议摘要，便于重启后继续整理本机 evaluation 样本。
- 建议只来自已有任务事件，不自动写入 `data/inner-brain/evaluation/runtime.jsonl`，不训练、不重放失败前命令。

## 非目标

- 不自动调用 `/inner-brain-eval-add`、`/inner-brain-eval-label` 或候选固化命令。
- 不从 OCR 文本自动推断 intent 或 slots。
- 不为非命令事件生成命令评估样本建议。
- 不改变任务事件采集、任务恢复和截图/OCR 行为。

## 实施步骤

1. 在 `tests/test_task_state.py` 为带命令事件的失败复盘增加 RED 断言：输出 `样本建议：/inner-brain-eval-add ... => /命令`，运行态最近失败记录保留事件，`/task-status` 展示样本建议摘要。
2. 在 `tests/test_task_state.py` 为无命令事件或空事件增加边界断言：不输出具体样本建议，只保留泛化人工固化入口。
3. 在 `tests/test_agent.py` 扩展 `/task-fail` 自动采集上下文测试，验证 Agent 真实命令事件会输出可复制样本建议。
4. 将版本元数据测试期望提升到 `0.127.0`，验证 RED。
5. 在 `src/jarvis_lite/task_state.py` 新增任务事件到 evaluation 命令建议的格式化 helper，并在失败复盘和最近失败记录展示中复用。
6. 同步 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README、PROJECT-PLAN、方案索引、文档索引、进度与验证记录。
7. 运行目标测试、相邻回归、全量 unittest、临时项目 smoke、桌面 smoke、打包后 smoke 和静态检查。

## 验收标准

- 失败复盘包含 `样本建议：/inner-brain-eval-add /dir-add 工作区 C:/demo => /dir-add`。
- `/task-status` 最近失败记录包含同一建议摘要。
- 没有可用命令事件时不生成具体 `/inner-brain-eval-add ... => ...` 建议。
- 输出继续明确不自动写入 evaluation、不训练、不自动重新执行外部动作。
