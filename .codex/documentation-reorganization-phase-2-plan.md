# Documentation Reorganization Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完成文档整理第二阶段，把第一阶段保留下来的大体量历史文档、周验证明细、旧路径引用和过时方案说明进一步收口。

**Architecture:** 正式入口保持第一阶段结构不变；验证明细从周文件拆为日文件，周文件只做索引；旧大进度文件保留原文件名但改成索引，详细内容拆到子目录；历史方案加明确的“历史版本”提示，当前方案仍以 `word/PROJECT-PLAN.md` 和 v3 为准。

**Tech Stack:** Markdown、PowerShell 批量拆分、Git。

---

### Task 1: 拆分验证记录

**Files:**
- Modify: `verification.md`
- Modify: `verification/README.md`
- Modify: `verification/2026-05/README.md`
- Modify: `verification/2026-05/week-2026-05-18.md`
- Modify: `verification/2026-05/week-2026-05-25.md`
- Create: `verification/2026-05/2026-05-18.md`
- Create: `verification/2026-05/2026-05-20.md`
- Create: `verification/2026-05/2026-05-21.md`
- Create: `verification/2026-05/2026-05-22.md`
- Create: `verification/2026-05/2026-05-23.md`
- Create: `verification/2026-05/2026-05-25.md`
- Create: `verification/2026-05/2026-05-26.md`
- Create: `verification/2026-05/2026-05-27.md`

- [ ] 按 `## 2026-05-DD` 标题拆分两个周验证文件。
- [ ] 保留 2026-05-18 周文件开头的早期综合验证记录到 `2026-05-18.md`。
- [ ] 将两个 `week-*` 文件改为周索引。
- [ ] 更新根验证入口和月份索引。

### Task 2: 拆分旧自然语言大进度

**Files:**
- Modify: `word/progress/details/2026-05-21-jarvis-lite-natural-language-brain-progress.md`
- Create: `word/progress/details/natural-language-brain/README.md`
- Create: `word/progress/details/natural-language-brain/2026-05-21-core-and-context.md`
- Create: `word/progress/details/natural-language-brain/2026-05-22-advice-context-and-recent-files.md`
- Create: `word/progress/details/natural-language-brain/2026-05-23-desktop-recent-entries.md`
- Create: `word/progress/details/natural-language-brain/2026-05-25-knowledge-summary.md`

- [ ] 将旧大文件按追加进度主题拆分。
- [ ] 原文件改为短索引，保留原路径以避免历史链接断裂。
- [ ] 更新 `word/progress/details/README.md`。

### Task 3: 清理旧引用和历史方案标注

**Files:**
- Modify: `DOCUMENTATION.md`
- Modify: `word/文档索引.md`
- Modify: `word/progress/*.md`
- Modify: `word/plans/2026-05-18-v1-overall-plan.md`
- Modify: `word/plans/2026-05-22-v2-personal-device-agent-plan.md`

- [ ] 把日进度中的验证链接从周文件改到对应日文件。
- [ ] 将 `DOCUMENTATION.md` 的验证规则改为日明细、周索引。
- [ ] 在 v1/v2 历史方案顶部加历史版本提示。
- [ ] 检查并替换残留旧路径。

### Task 4: 验证与提交

**Files:**
- Verify all changed Markdown paths.

- [ ] 运行 `git diff --check`。
- [ ] 运行 Markdown 本地链接检查。
- [ ] 运行 `python -m unittest discover -s tests -v`。
- [ ] 运行桌面 smoke。
- [ ] 记录验证结果。
- [ ] 提交并 push。
