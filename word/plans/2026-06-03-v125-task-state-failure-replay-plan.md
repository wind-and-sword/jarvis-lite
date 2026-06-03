# v125：任务状态与失败复盘第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v124 IDEA 项目状态第一阶段，进入 Jarvis Lite 1.0 验收路线的任务状态、中断恢复和失败复盘主线。

## 背景

`0.119.0` 已完成首批常用应用第一阶段工作流：Chrome、Clash Verge、QQ、微信和 IntelliJ IDEA 均有显式状态、打开、聚焦或准备式入口。桌面动作仍只由显式 slash command 触发，不把自然语言直接映射为键鼠执行。

下一步需要让 Jarvis Lite 能记录一个多步骤任务当前执行到哪里、失败在哪一步，并在中断后给出继续、取消或重新开始的入口。第一阶段先做显式任务状态命令和运行态持久化，不自动截图、不自动 OCR、不自动恢复执行外部动作。

## 目标

- 新增任务状态模块，复用现有 `jarvis-lite-runtime/agent-context.json` 运行态上下文。
- 新增命令：`/task-status`、`/task-start 任务名称`、`/task-step 步骤说明`、`/task-fail 失败原因`、`/task-resume`、`/task-complete`、`/task-cancel`。
- `/task-status` 展示当前任务、当前步骤、已完成步骤、失败状态、最近失败记录和下一步建议。
- `/task-fail` 记录失败原因、失败步骤、用户原始任务、路由摘要、授权摘要占位和当前屏幕/OCR 占位说明。
- 任务状态可跨 Agent 重启恢复。

## 非目标

- 不自动启动、切换、点击、输入或重新执行失败动作。
- 不自动截图或 OCR；第一阶段只记录“未采集，后续接入截图/OCR”。
- 不自动写入 InnerBrain training/evaluation 样本，只提示后续可人工固化。
- 不接入自然语言自动任务编排；本阶段只支持显式 slash command。

## 实施步骤

1. 新增 `tests/test_task_state.py`，先验证空状态、开始任务、记录步骤、失败记录、恢复、完成、取消和运行态恢复。
2. 在 `tests/test_agent.py` 增加 `/task-status`、`/task-start`、`/task-step`、`/task-fail`、`/task-resume`、`/task-complete`、`/task-cancel` 命令、帮助、`/status` 和 `/recent-context` 断言。
3. 将版本元数据测试期望提升到 `0.120.0`，验证 RED。
4. 扩展 `src/jarvis_lite/runtime_context.py`，增加当前任务和最近失败记录的可序列化上下文。
5. 新增 `src/jarvis_lite/task_state.py`，实现任务状态读写、步骤推进、失败复盘和状态文案。
6. 将新命令接入 `JarvisAgent`、`TEACHABLE_INNER_BRAIN_COMMAND_INTENTS`、`/help`、`/status` 和 `/recent-context`。
7. 同步版本、README、PROJECT-PLAN、方案索引、文档索引、进度与验证记录。
8. 运行目标测试、相邻回归、全量 unittest、smoke、打包和静态检查。

## 验收标准

- `/task-status` 空状态提示还没有当前任务，并说明可用 `/task-start 任务名称`。
- `/task-start` 后 `/task-step` 能记录当前步骤，前一个进行中步骤自动归入已完成步骤。
- `/task-fail` 会将当前任务标记为失败，记录最近失败复盘，并提示 `/task-resume`、`/task-cancel` 和人工固化入口。
- 重启 `JarvisAgent` 后任务状态和最近失败记录仍可通过 `/task-status` 查看。
- `/task-resume` 可把失败任务恢复为进行中，`/task-complete` 和 `/task-cancel` 会结束当前任务。
- 本阶段输出明确“不自动截图、不自动 OCR、不自动重新执行外部动作”。
