# Jarvis Lite v28：桌面候选训练模板填充方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v27 桌面内脑候选快捷入口，明确 `0.24.0` 的候选 teach/label 模板填充闭环。

## 核心结论

`0.24.0` 在桌面面板增加候选编号和 teach/label 模板填充按钮。用户查看 InnerBrain 训练候选后，可以选择候选编号，把 `/inner-brain-teach-candidate` 或 `/inner-brain-label-candidate` 模板填入输入框，再由用户显式补全并发送。

## 设计边界

- 不新增自然语言正则规则。
- 不自动发送、不自动训练、不自动标注。
- 不改变 `/inner-brain-candidates`、候选统计、排序、teach 或 label 的后端规则。
- 不在托盘实现模板填充，因为托盘没有输入框上下文。

## 0.24.0 收口内容

- 桌面面板新增候选编号 stepper，默认编号为 1。
- 桌面面板新增“填教学”按钮，填入 `/inner-brain-teach-candidate 编号 => `。
- 桌面面板新增“填标注”按钮，填入 `/inner-brain-label-candidate 编号 => intent slot=value`。
- 填充动作只修改输入框和焦点，不写入 transcript，不改变最近路由状态。
- 项目版本同步到 `0.24.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 继续评估是否把候选列表中的编号和模板填充做成更紧凑的桌面交互。
- 继续评估轻量 embedding 或小型分类器方案，但不从零训练通用 LLM。
