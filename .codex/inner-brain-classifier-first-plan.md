# InnerBrain 样本分类器优先迁移计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

把 InnerBrain 的自然语言理解主路径从 `legacy_rule` 迁移为 seed/runtime 样本分类器优先：高频自然语言先产出 `intent / slots / confidence / missing`，再由 Agent 决策执行、澄清或交给 LLM。旧 `parse_natural_language_intent()` 仅作为迁移期兼容兜底和复杂槽位规则来源。

## 任务

1. 写 RED 测试：
   - `早上好`、`总结知识库`、`查看最近上下文`、`查看最近文件` 等常见输入不再返回 `source=legacy_rule`。
   - `/inner-brain-status` 不再宣传 `legacy_rule：启用`，而是显示样本分类器优先和 legacy fallback。
   - 搜索、桌面快捷方式删除等槽位输入继续由样本分类器命中并抽取槽位。

2. 调整 `src/jarvis_lite/inner_brain.py`：
   - `understand()` 先匹配 `_best_sample()`。
   - 样本置信度低于中阈值后再调用 legacy fallback。
   - legacy 返回 `source=legacy_fallback`，reason 明确是迁移期兼容兜底。
   - `describe_status()` 更新为当前真实路径。

3. 扩展 seed 样本：
   - 问候、身份、能力、最近上下文、最近文件、标签历史。
   - 知识库摘要/状态、常用目录、日报、更新、经验。
   - 确认/取消执行、LLM 启用、联网搜索、桌面快捷方式删除。

4. 补全样本到 `NaturalLanguageIntent` 的映射：
   - 对 command 类意图通过 `command` slot 调用 Agent。
   - 对非 command 类意图返回对应本地 intent。
   - 保留 regex 槽位抽取函数用于 search query、desktop shortcut item 等对象提取。

5. 文档同步：
   - 更新 README、`word/PROJECT-PLAN.md`、方案索引、今日进度和验证记录。
   - 记录当前阶段仍保留 legacy fallback，后续逐步迁移复杂槽位意图。

6. 验证并提交：
   - 定向 `tests.test_inner_brain tests.test_agent`。
   - 全量 `unittest discover -s tests -v`。
   - 桌面 smoke、`git diff --check`、Markdown 链接检查、敏感信息扫描。
   - 提交到本地 Git；不主动 push，除非用户明确要求。
