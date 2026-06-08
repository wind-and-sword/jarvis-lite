# 最近建议执行前确认第一版计划

> 日期：2026-05-22
> 执行者：Codex

## 目标

用户获取经验建议后，可以说“执行第二条建议”，Jarvis Lite 先展示将要执行的命令并等待“确认执行”，确认后复用现有命令处理链路。

## 设计

- `intent.py` 新增三个自然语言意图：
  - `prepare_numbered_advice_suggestion_execution`
  - `confirm_pending_advice_suggestion_execution`
  - `cancel_pending_advice_suggestion_execution`
- `JarvisAgent` 新增当前实例内待确认建议命令字段，不写入运行态文件。
- 准备执行时从建议文本中提取冒号前的命令片段。
- 命令片段包含 `[]`、`...` 或常见占位词时，不进入待确认状态，提示补全参数。
- 确认执行时调用 `self.handle(command)`，让已有命令逻辑负责实际结果和错误提示。

## 验收

- “执行第二条建议”会准备 `/kb` 并提示“确认执行”。
- “确认执行”会返回 `/kb` 的知识库状态结果。
- “执行第一条建议”遇到 `/import 源文件或目录路径 [目标文件名]` 时提示需要补充参数。
- 没有待确认命令时，“确认执行”给出明确提示。
