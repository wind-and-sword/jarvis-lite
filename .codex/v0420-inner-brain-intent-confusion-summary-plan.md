# 0.42.0 InnerBrain 本机评估失败意图混淆汇总 Implementation Plan

> 日期：2026-06-02
> 执行者：Codex
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and superpowers:verification-before-completion. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在本机失败评估视图和 Markdown 报告中增加“失败意图混淆汇总”，帮助定位 expected intent 被识别成 actual intent 的高频方向。

**Architecture:** 沿用 `InnerBrainEvaluationReport` 的只读派生属性模式，从失败样本的 `case.expected_intent` 和 `result.intent` 计算 `expected -> actual` 计数。`describe_inner_brain_evaluation(..., failures_only=True)` 在失败期望意图汇总后输出混淆方向，报告导出继续复用同一描述。

**Tech Stack:** Python 3.13、标准库 `unittest`、本地 Markdown 文档、现有 Windows 打包脚本。

---

### Task 1: RED 测试

**Files:**
- Modify: `tests/test_inner_brain.py`
- Modify: `tests/test_agent.py`
- Modify: `tests/test_project_metadata.py`

- [ ] 新增 `test_inner_brain_failed_evaluation_summarizes_failed_intent_confusions`，构造两条 `knowledge.summary -> knowledge.status` 意图不匹配失败、一条意图一致的策略失败和一条通过样本。
- [ ] 断言 `report.failed_intent_confusion_counts == {"knowledge.summary -> knowledge.status": 2}`。
- [ ] 断言 failures-only 描述包含 `失败意图混淆汇总：`、`- knowledge.summary -> knowledge.status：2 条` 和典型样本。
- [ ] 扩展 InnerBrain Markdown 导出测试和 Agent 本机报告测试，断言报告包含混淆汇总。
- [ ] 将版本测试期望改为 `0.42.0`，更新检测 fixture 改为 `0.42.1`，先运行目标测试并确认失败原因是新接口/新展示缺失和版本未提升。

### Task 2: GREEN 实现

**Files:**
- Modify: `src/jarvis_lite/inner_brain.py`
- Modify: `pyproject.toml`
- Modify: `src/jarvis_lite/__init__.py`
- Modify: `tests/test_agent.py`

- [ ] 在 `InnerBrainEvaluationReport` 增加 `failed_intent_confusion_counts` 派生属性。
- [ ] 在 failures-only 描述中输出 `失败意图混淆汇总：`，按数量降序、pair 名称升序稳定排序，并列出典型样本。
- [ ] 只统计 `case.expected_intent != result.intent` 的失败样本，避免策略或命令问题污染意图混淆汇总。
- [ ] 版本提升到 `0.42.0`，更新更新检测 fixture 为 `0.42.1`。
- [ ] 复跑目标测试至通过。

### Task 3: 文档与验证

**Files:**
- Modify: `README.md`
- Modify: `word/PROJECT-PLAN.md`
- Add: `word/plans/2026-06-02-v46-inner-brain-intent-confusion-summary-plan.md`
- Modify: `word/plans/README.md`
- Modify: `word/文档索引.md`
- Modify: `word/progress/2026-06-02.md`
- Modify: `verification.md`
- Modify: `verification/2026-06/*.md`
- Modify: `.codex/testing.md`
- Modify: `.codex/review-report.md`
- Modify: `.codex/operations-log.md`

- [ ] 同步用户文档，明确 0.42.0 只读展示失败意图混淆方向，不训练、不改 JSONL。
- [ ] 运行 InnerBrain + Agent 相邻回归和全量 unittest。
- [ ] 运行源码桌面 smoke、构建 Windows 安装包、复制 `JarvisLiteSetup-0.42.0.exe`、运行打包后 exe smoke。
- [ ] 执行 `git diff --check`、Markdown 本地链接检查、敏感信息差异扫描和本地配置跟踪检查。
- [ ] 生成审查报告，提交并 push 到 `origin/main`。
