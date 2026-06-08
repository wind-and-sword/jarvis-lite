# 0.44.0 InnerBrain 本机评估失败意图混淆修复建议分组 Implementation Plan

> 日期：2026-06-02
> 执行者：Codex
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and superpowers:verification-before-completion. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在本机失败评估视图和 Markdown 报告中增加“失败意图混淆修复建议”，把同一 `expected -> actual` 混淆方向下的显式 teach/label 建议集中展示。

**Architecture:** 沿用 `describe_inner_brain_evaluation(..., failures_only=True)` 的只读派生展示模式，从 `failed_case_results` 中筛选 expected intent 与 actual intent 不一致的失败样本，并复用 `_inner_brain_evaluation_fix_suggestion()` 生成建议。不新增命令、不写训练样本、不改变 evaluation JSONL payload。

**Tech Stack:** Python 3.13、标准库 `unittest`、本地 Markdown 文档、现有 Windows 打包脚本。

---

### Task 1: RED 测试

**Files:**
- Modify: `tests/test_inner_brain.py`
- Modify: `tests/test_agent.py`
- Modify: `tests/test_project_metadata.py`

- [x] 新增 InnerBrain 描述测试，构造两个 `knowledge.summary -> knowledge.status` 失败样本和一个意图一致的策略失败。
- [x] 断言 failures-only 描述包含 `失败意图混淆修复建议：`、混淆方向、数量和该方向下的两条显式修复建议。
- [x] 断言意图一致失败不进入意图混淆修复建议分组。
- [x] 扩展 Markdown 导出测试和 Agent 本机报告测试，断言未指定单个文件的报告包含分组修复建议。
- [x] 将版本测试期望改为 `0.44.0`，更新检测 fixture 改为 `0.44.1`，先运行目标测试并确认失败原因是新展示缺失和版本未提升。

### Task 2: GREEN 实现

**Files:**
- Modify: `src/jarvis_lite/inner_brain.py`
- Modify: `pyproject.toml`
- Modify: `src/jarvis_lite/__init__.py`
- Modify: `tests/test_agent.py`

- [x] 在 `describe_inner_brain_evaluation(..., failures_only=True)` 中构建意图混淆到修复建议的映射。
- [x] 输出 `失败意图混淆修复建议：`，按失败数量降序、混淆方向升序稳定排序。
- [x] 每个混淆方向输出数量和该方向下的显式修复建议。
- [x] 保留现有 `失败修复建议：` 平铺列表，覆盖意图一致的策略或命令失败。
- [x] 版本提升到 `0.44.0`，更新更新检测 fixture 为 `0.44.1`。
- [x] 复跑目标测试至通过。

### Task 3: 文档与验证

**Files:**
- Modify: `README.md`
- Modify: `word/PROJECT-PLAN.md`
- Add: `word/plans/2026-06-02-v48-inner-brain-intent-confusion-fix-suggestions-plan.md`
- Modify: `word/plans/README.md`
- Modify: `word/文档索引.md`
- Modify: `word/progress/2026-06-02.md`
- Modify: `verification.md`
- Modify: `verification/2026-06/*.md`
- Modify: `.codex/testing.md`
- Modify: `.codex/review-report.md`
- Modify: `.codex/operations-log.md`

- [x] 同步用户文档，明确 0.44.0 只读展示按意图混淆方向分组的修复建议，不训练、不改 JSONL。
- [x] 运行 InnerBrain + Agent 相邻回归和全量 unittest。
- [x] 运行源码桌面 smoke、构建 Windows 安装包、复制 `JarvisLiteSetup-0.44.0.exe`、运行打包后 exe smoke。
- [x] 执行 `git diff --check`、Markdown 本地链接检查、敏感信息差异扫描和本地配置跟踪检查。
- [x] 生成审查报告。
- [ ] 提交并 push 到 `origin/main`。
