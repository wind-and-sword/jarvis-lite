# Jarvis Lite v30：桌面候选选择绑定方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v29 桌面候选模板状态同步，明确 `0.26.0` 的候选选择绑定闭环。

## 目标

`0.26.0` 在桌面候选模板区增加候选下拉选择。用户执行 `/inner-brain-candidates` 后，可以直接从候选列表中选择某条候选；选择动作会同步候选编号，再点击“填教学”或“填标注”写入对应编号模板。

## 边界

- 只在桌面 UI 层解析当前候选列表的编号行。
- 不新增后端命令，不改变 `/inner-brain-candidates` 输出格式。
- 不新增自然语言正则，不改变 InnerBrain、LLM fallback、SearchRouter 或知识库路由。
- 不自动发送、不自动训练；模板按钮仍只填入输入框。
- 空候选时下拉框显示“暂无候选”并禁用。

## 实现要点

- `AssistantPanel` 增加 `innerBrainCandidateSelect` 下拉框。
- `_extract_inner_brain_candidate_options()` 从候选响应中解析 `N. 文本` 行。
- 候选下拉框 item data 保存候选编号，显示文本使用紧凑摘要。
- 用户选择候选时同步 `QSpinBox` 编号；用户改编号时同步下拉框当前项。
- “填教学”“填标注”继续复用当前编号生成 `/inner-brain-teach-candidate` 和 `/inner-brain-label-candidate` 模板。

## 验证

- RED：新增桌面测试先失败，证明候选下拉框、选项文本、选择同步和版本提升尚未实现。
- GREEN：目标测试通过。
- 回归：桌面 widget 专项、相邻桌面/Agent/LLM/InnerBrain/Conversation 回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 继续评估候选下拉框是否需要预填常见目标命令或 intent，但仍必须由用户显式确认。
- 继续评估轻量 embedding 或小型分类器方案，但不从零训练通用 LLM。
