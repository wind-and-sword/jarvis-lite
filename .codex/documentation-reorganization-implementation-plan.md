# Documentation Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 Jarvis Lite 的项目介绍、当前方案、方案历史、每日进度、设计文档和验证记录拆分为清晰职责边界。

**Architecture:** 根目录只保留项目入口与长期规则；`word/` 承担正式方案、设计和进度；`verification/` 承担详细验证归档，根目录 `verification.md` 只保留入口摘要。旧内容不删除，先迁移到新的可检索位置。

**Tech Stack:** Markdown、PowerShell 文件迁移、Git。

---

### Task 1: 方案文档结构

**Files:**
- Create: `word/PROJECT-PLAN.md`
- Create: `word/plans/2026-05-18-v1-overall-plan.md`
- Create: `word/plans/2026-05-22-v2-personal-device-agent-plan.md`
- Create: `word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`
- Move: `word/jarvis-lite-overall-plan.md`
- Move: `word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`

- [ ] 建立 `word/plans/`。
- [ ] 将 v1/v2 历史方案迁移到 `word/plans/`。
- [ ] 新建 v3 当前方案，明确 PC Agent -> LLM -> 多端入口的顺序。
- [ ] 新建 `word/PROJECT-PLAN.md` 作为当前方案入口。

### Task 2: 进度和设计文档目录

**Files:**
- Create: `word/progress/*.md`
- Create: `word/design/*.md`
- Move: existing `word/*progress.md`
- Move: existing design docs

- [ ] 建立 `word/progress/` 和 `word/design/`。
- [ ] 将进度文档按自然日迁移到 `word/progress/`。
- [ ] 将设计文档迁移到 `word/design/`。
- [ ] 保留原文内容，不在本阶段大幅删改历史进度。

### Task 3: 验证记录拆分

**Files:**
- Modify: `verification.md`
- Create: `verification/README.md`
- Create: `verification/2026-05/README.md`
- Create: `verification/2026-05/week-2026-05-18.md`
- Create: `verification/2026-05/week-2026-05-25.md`

- [ ] 按标题日期将既有验证记录拆成自然周文件。
- [ ] 根目录 `verification.md` 改为短入口。
- [ ] 保证历史验证命令和结论仍可追溯。

### Task 4: 项目入口和文档规则

**Files:**
- Modify: `README.md`
- Modify: `DOCUMENTATION.md`
- Modify: `word/文档索引.md`

- [ ] 将 `README.md` 重写为项目介绍和快速启动。
- [ ] 将新的目录职责写入 `DOCUMENTATION.md`。
- [ ] 将 `word/文档索引.md` 改成唯一完整索引。

### Task 5: 验证与提交

**Files:**
- Verify all changed Markdown paths.

- [ ] 运行 `git diff --check`。
- [ ] 运行 Markdown 链接存在性检查。
- [ ] 文档变更后运行本地测试或说明跳过依据。
- [ ] 提交并 push。
