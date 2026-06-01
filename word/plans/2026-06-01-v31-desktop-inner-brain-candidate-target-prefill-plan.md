# Jarvis Lite v31：桌面候选目标预填方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v30 桌面候选选择绑定，明确 `0.27.0` 的候选训练目标预填闭环。

## 目标

`0.27.0` 在桌面候选训练区增加显式目标预填。用户执行 `/inner-brain-candidates` 后，可以先选择候选，再选择常见教学命令或常见标注 intent 模板；点击“填教学”或“填标注”时，只把对应完整模板写入输入框，方便用户继续编辑并手动发送。

## 边界

- 不新增后端命令，不改变 `/inner-brain-candidates`、`/inner-brain-teach-candidate` 或 `/inner-brain-label-candidate` 的协议。
- 不新增自然语言正则，不让桌面 UI 猜测用户真实意图。
- 不自动发送、不自动训练；所有训练仍必须由用户检查输入框内容后显式提交。
- 教学目标复用 Agent 当前允许教学的已知命令集合，避免 UI 预填后端不接受的命令。
- 标注目标只提供常见 `intent slot=value` 模板，用户仍可在发送前修改槽位值。

## 实现要点

- `AssistantPanel` 增加教学目标下拉框，默认保持“手动填写命令”，保证旧的空目标模板不变。
- 教学目标下拉框从 `TEACHABLE_INNER_BRAIN_COMMAND_INTENTS` 生成，优先展示常用命令，再展示剩余可教学命令。
- `AssistantPanel` 增加标注目标下拉框，默认 `intent slot=value`，并提供搜索、资料、目录、经验、标签和桌面快捷方式等常见 intent 模板。
- “填教学”根据当前候选编号和教学目标生成 `/inner-brain-teach-candidate 编号 => /命令`。
- “填标注”根据当前候选编号和标注模板生成 `/inner-brain-label-candidate 编号 => intent slot=value`。

## 验证

- RED：新增桌面测试先失败，证明目标下拉框 helper、教学目标预填、标注目标预填和版本提升尚未实现。
- GREEN：目标测试通过。
- 回归：桌面 widget 专项、相邻桌面/Agent/LLM/InnerBrain/Conversation 回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 继续观察真实候选标注时最常用的 intent 模板，再决定是否扩展或重排模板列表。
- 继续评估轻量 embedding 或小型分类器方案，但不从零训练通用 LLM。
