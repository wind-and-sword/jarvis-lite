# 0.40.0 InnerBrain 本机评估失败类型汇总 Implementation Plan

> 日期：2026-06-02
> 执行者：Codex
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and superpowers:verification-before-completion. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在本机失败评估视图和 Markdown 报告中增加轻量“失败类型汇总”，帮助先按意图、命令、策略维度处理高频失败。

**Architecture:** 沿用 `InnerBrainEvaluationReport` 的只读派生属性模式，从现有失败 `reason` 文本识别类型并计数。`describe_inner_brain_evaluation(..., failures_only=True)` 在失败文件和失败原因之间输出类型汇总，报告导出继续复用同一描述。

**Tech Stack:** Python 3.13、标准库 `unittest`、本地 Markdown 文档、现有 Windows 打包脚本。

---

### Task 1: RED 测试

**Files:**
- Modify: `tests/test_inner_brain.py`
- Modify: `tests/test_agent.py`
- Modify: `tests/test_project_metadata.py`

- [ ] 新增 `test_inner_brain_failed_evaluation_summarizes_failure_reason_categories`，构造同时出现意图、命令、策略差异的本机评估样本，断言 `failed_reason_category_counts` 和 `失败类型汇总：`。
- [ ] 扩展报告导出测试，断言 Markdown 包含 `失败类型汇总：` 与类型计数。
- [ ] 扩展 Agent 本机报告测试，断言 `/inner-brain-eval-local-report` 导出的 Markdown 包含类型汇总。
- [ ] 将版本测试期望改为 `0.40.0`，先运行目标测试并确认失败原因是新接口/新展示缺失和版本未提升。

### Task 2: GREEN 实现

**Files:**
- Modify: `src/jarvis_lite/inner_brain.py`
- Modify: `pyproject.toml`
- Modify: `src/jarvis_lite/__init__.py`
- Modify: `tests/test_agent.py`

- [ ] 在 `InnerBrainEvaluationReport` 增加 `failed_reason_category_counts` 派生属性。
- [ ] 新增内部 helper，把 reason 中的 `意图期望`、`命令期望`、`策略期望` 映射为 `意图不匹配`、`命令不匹配`、`策略不匹配`。
- [ ] 在 failures-only 描述中输出 `失败类型汇总：`，按数量降序、名称升序稳定排序，并列出典型样本。
- [ ] 版本提升到 `0.40.0`，更新更新检测 fixture 为 `0.40.1`。
- [ ] 复跑目标测试至通过。

### Task 3: 文档与验证

**Files:**
- Modify: `README.md`
- Modify: `word/PROJECT-PLAN.md`
- Add: `word/plans/2026-06-02-v44-inner-brain-failure-type-summary-plan.md`
- Modify: `word/plans/README.md`
- Modify: `word/文档索引.md`
- Modify: `word/progress/2026-06-02.md`
- Modify: `verification.md`
- Modify: `verification/2026-06/*.md`
- Modify: `.codex/testing.md`
- Modify: `.codex/review-report.md`
- Modify: `.codex/operations-log.md`

- [ ] 同步用户文档，明确 0.40.0 只读展示失败类型，不训练、不改 JSONL。
- [ ] 运行 InnerBrain + Agent 相邻回归和全量 unittest。
- [ ] 运行源码桌面 smoke、构建 Windows 安装包、复制 `JarvisLiteSetup-0.40.0.exe`、运行打包后 exe smoke。
- [ ] 执行 `git diff --check`、Markdown 本地链接检查、敏感信息差异扫描和本地配置跟踪检查。
- [ ] 生成审查报告，提交并 push 到 `origin/main`。
