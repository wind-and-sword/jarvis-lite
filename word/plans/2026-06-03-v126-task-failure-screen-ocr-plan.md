# v126：任务失败截图 OCR 复盘第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v125 任务状态与失败复盘第一阶段，进入失败上下文采集的第一步。

## 目标

- 新增显式命令 `/task-fail-capture 失败原因 [lang=chi_sim+eng]`。
- 命令在已有当前任务时保存当前主屏幕截图、尝试 OCR，并把截图路径、尺寸、OCR 文本或 OCR 失败诊断写入最近失败复盘。
- OCR 不可用时仍记录截图上下文和失败诊断。
- 继续复用 `jarvis-lite-runtime/agent-context.json`，不新增持久化文件结构。

## 非目标

- 不自动点击、输入、切换窗口、启动应用或重新执行失败动作。
- 不把自然语言自动映射到任务状态或截图 OCR 命令。
- 不自动写入 InnerBrain training/evaluation 样本，只在复盘中提示人工固化入口。

## 实施步骤

1. 在 `tests/test_task_state.py` 先新增截图 OCR 失败复盘核心测试，使用 `capturer` 和 `recognizer` 注入避免真实截图/OCR。
2. 在 `tests/test_agent.py` 新增 `/task-fail-capture` 命令测试、缺少原因用法测试、帮助和 `/status` 文案测试。
3. 将版本元数据测试期望提升到 `0.121.0`，验证 RED。
4. 扩展 `src/jarvis_lite/task_state.py`，新增 `record_task_failure_with_screen_ocr()`，复用 `save_screen_capture()` 与 `describe_image_ocr()`。
5. 将新命令接入 `JarvisAgent`、`TEACHABLE_INNER_BRAIN_COMMAND_INTENTS`、帮助、状态文案和运行日志；LLM 白名单仍只保留 `/task-status`，不开放 `/task-fail-capture`。
6. 同步版本、README、PROJECT-PLAN、方案索引、文档索引、进度与验证记录。
7. 运行目标测试、相邻回归、全量 unittest、smoke、打包和静态检查。

## 验收标准

- `/task-fail-capture 失败原因 lang=eng` 会保存截图并把 OCR 结果写入任务失败复盘。
- OCR 不可用时，失败复盘仍包含截图路径、尺寸和 OCR 失败诊断。
- 重启 `JarvisAgent` 后 `/task-status` 能看到最近失败记录中的截图/OCR 上下文。
- `/task-fail-capture` 缺少当前任务或失败原因时给出明确用法。
- 本阶段输出明确“不自动重新执行外部动作、不点击、不输入”。
