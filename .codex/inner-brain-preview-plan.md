# InnerBrain Preview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add non-executing InnerBrain status and preview commands so natural-language understanding is visible before tool execution.

**Architecture:** `inner_brain.py` owns formatting of `InnerBrainResult` and status metadata. `JarvisAgent` exposes `/inner-brain-status` and `/inner-brain-preview 文本`, records logs, and never executes previewed commands.

**Tech Stack:** Python stdlib, existing `JarvisAgent`, existing `unittest` tests.

---

### Task 1: InnerBrain Formatting

**Files:**
- Modify: `src/jarvis_lite/inner_brain.py`
- Test: `tests/test_inner_brain.py`

- [ ] Add failing tests for result preview formatting and status output.
- [ ] Verify RED.
- [ ] Implement `describe_inner_brain_result()` and `InnerBrain.describe_status()`.
- [ ] Verify GREEN with `tests.test_inner_brain`.

### Task 2: Agent Commands

**Files:**
- Modify: `src/jarvis_lite/agent.py`
- Test: `tests/test_agent.py`

- [ ] Add failing tests for `/inner-brain-status`, `/inner-brain-preview 文本`, `/help`, and preview not deleting desktop shortcuts.
- [ ] Verify RED.
- [ ] Add command routing and help text.
- [ ] Verify GREEN with targeted Agent tests.

### Task 3: Documentation And Verification

**Files:**
- Modify: `README.md`
- Modify: `word/PROJECT-PLAN.md`
- Modify: `word/progress/2026-05-28.md`
- Modify: `verification.md`
- Modify: `verification/2026-05/README.md`
- Modify: `verification/2026-05/2026-05-28.md`

- [ ] Update docs with the new commands and non-execution boundary.
- [ ] Run full `unittest`, command smoke, desktop smoke, `git diff --check`, and Markdown local link check.
- [ ] Commit and push.
