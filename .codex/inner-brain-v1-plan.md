# InnerBrain v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a local lightweight InnerBrain layer that outputs structured intent, slots, confidence, missing fields, source, reason, and action policy before the LLM fallback.

**Architecture:** InnerBrain v1 wraps the existing `parse_natural_language_intent()` as a compatibility source and adds a seed/training-sample similarity classifier for expression variants. `JarvisAgent` keeps all execution authority; InnerBrain only produces structured understanding and conservative policy decisions.

**Tech Stack:** Python stdlib dataclasses, JSONL loading, character n-gram Jaccard/Dice similarity, existing `NaturalLanguageIntent`, existing `unittest` test suite.

---

## File Structure

- Create `src/jarvis_lite/inner_brain.py`: schema, seed samples, JSONL loader, text normalization, similarity classifier, conversion to `NaturalLanguageIntent`.
- Modify `src/jarvis_lite/agent.py`: instantiate InnerBrain and call it after identity facts and before data/LLM fallback.
- Create `tests/test_inner_brain.py`: focused unit tests for schema, seed matching, JSONL loading, confidence policy, missing slots.
- Modify `tests/test_agent.py`: integration tests ensuring InnerBrain handles phrase variants without calling LLM and low-confidence text still reaches LLM fallback.
- Update docs: `README.md`, `word/PROJECT-PLAN.md`, `word/progress/2026-05-28.md`, `verification.md`, `verification/2026-05/2026-05-28.md`, `.codex/testing.md`, `.codex/review-report.md`.

## Task 1: InnerBrain Schema And Legacy Wrapper

- [ ] Write failing tests in `tests/test_inner_brain.py` for `InnerBrainResult` fields and legacy parser wrapping `早上好`.
- [ ] Run targeted test and verify RED.
- [ ] Create `src/jarvis_lite/inner_brain.py` with `InnerBrain`, `InnerBrainResult`, `InnerBrainTrainingSample`, `InnerBrainPolicy`.
- [ ] Implement `InnerBrain.understand(text)` so legacy parser returns confidence `1.0`, source `legacy_rule`, policy `execute`.
- [ ] Run targeted tests and verify GREEN.

## Task 2: Seed Samples And Similarity Classifier

- [ ] Add failing tests for sample variants such as `麻烦看一下知识库摘要` and `把桌面比特浏览器快捷方式删除`.
- [ ] Verify RED because no sample classifier exists.
- [ ] Add built-in seed samples for stable intents: `knowledge.summary`, `knowledge.status`, `desktop.delete_shortcut`, `assistant.identity`, `assistant.greeting`.
- [ ] Implement normalized character n-gram similarity and confidence thresholds: high `>=0.78`, medium `>=0.58`, low `<0.58`.
- [ ] Convert high-confidence samples to `NaturalLanguageIntent` or command; medium missing slots returns clarify; low returns fallback.
- [ ] Run targeted tests and verify GREEN.

## Task 3: Runtime JSONL Training Sample Loading

- [ ] Add failing tests using temp `ProjectPaths` with `data/inner-brain/training/custom.jsonl`.
- [ ] Verify RED because loader is absent.
- [ ] Implement JSONL loader with strict required fields `text`, `intent`, `slots`; ignore invalid lines with reason recorded in result only when selected samples are valid.
- [ ] Ensure runtime samples extend seed samples and can override expression variants without touching source code.
- [ ] Run targeted tests and verify GREEN.

## Task 4: Agent Integration

- [ ] Add failing Agent tests: sample variant maps to `/kb-summary` without calling LLM; low-confidence external planning prompt still calls fake LLM.
- [ ] Verify RED.
- [ ] Modify `JarvisAgent.__init__()` to accept optional InnerBrain and default to `InnerBrain(self.paths)`.
- [ ] Replace direct `parse_natural_language_intent()` dispatch with `self.inner_brain.understand(prompt)` plus conservative policy handling.
- [ ] Keep existing `_handle_natural_language_intent()` as execution bridge.
- [ ] Run targeted tests and verify GREEN.

## Task 5: Docs, Verification, Commit

- [ ] Update README and project docs to describe InnerBrain v1 as local lightweight NLU, not a self-trained small LLM.
- [ ] Update progress and verification files with exact command results.
- [ ] Run `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.
- [ ] Run `git diff --check`.
- [ ] Run markdown local-link check if docs changed.
- [ ] Commit with `feat: 引入 InnerBrain 内脑雏形` and push `origin main`.
