# Jarvis Lite v42：InnerBrain 本机评估失败报告导出方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v41 本机失败评估按文件分组，明确 `0.38.0` 的本机失败评估 Markdown 报告导出入口。

## 目标

`0.38.0` 新增一个只读导出闭环：用户执行 `/inner-brain-eval-local-report [文件名]` 后，Jarvis Lite 会执行本机 `local_evaluation` 失败评估，并把结果写入 `word/inner-brain-evaluation-report.md`。报告包含评估集、失败文件分组、失败样例、失败原因和显式修复建议，便于后续按文件集中处理真实日志样本。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变评估样本 JSONL 的持久化字段和去重键。
- 不改变正常聊天路由、LLM fallback 或联网搜索能力。
- 本阶段只做 Markdown 报告导出，不改分类器评分、不补 seed 样本。

## 实现要点

- 新增报告导出结果对象，记录报告路径、相对路径、失败数和是否按文件过滤。
- 新增 `export_inner_brain_evaluation_report()`，复用 `describe_inner_brain_evaluation(report, failures_only=True)` 生成正文，并在 Markdown 顶部写入日期、执行者和只读说明。
- Agent 新增 `/inner-brain-eval-local-report [文件名]`：
  - 不带文件名时导出全部本机失败评估。
  - 带文件名时复用现有 JSONL 文件名规范化逻辑，只导出指定本机评估文件的失败项。
  - 返回报告相对路径、失败数和“不训练”说明。
- 新命令作为路由观察命令处理，不污染最近路由训练候选。

## 验证

- RED：新增 InnerBrain 报告导出测试、Agent 全量本机失败报告导出测试、Agent 指定文件报告导出测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain/Agent/LLM/桌面/Conversation 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 若报告仍不足以定位失败原因，再做按文件汇总治理视图或失败原因聚类。
- 根据报告中的高频失败样本，再扩展 seed/runtime 样本、槽位补全或轻量分类器评分。
