# 最近文件纳入最近上下文和日报计划

> 日期：2026-05-22  
> 执行者：Codex

## 目标

最近文件列表已经可持久化，本轮把它接入“查看最近上下文”和日报，使用户看完最近文件后能在上下文状态与每日回顾里继续追踪。

## 范围

- “查看最近上下文”展示最近文件列表数量和编号。
- 新建 `JarvisAgent` 后，恢复的最近文件列表仍能展示在最近上下文状态中。
- 日报“最近上下文”展示最近文件列表。
- 日报“下一步建议”在有最近文件时提示“查看第一份最近文件”。
- 不读取文件内容，不打开文件，不执行移动或删除。

## 实现步骤

1. 在 `tests/test_agent.py` 增加最近上下文展示最近文件列表与跨实例恢复测试。
2. 在 `tests/test_automation.py` 增加日报最近上下文和下一步建议覆盖最近文件的断言。
3. 更新 `agent.py` 的 `_recent_context_status()`，纳入 `self._recent_files`。
4. 更新 `automation.py` 的最近上下文和下一步建议生成逻辑，纳入 `RuntimeContext.recent_files`。
5. 更新 README、验证记录和方案文档。

## 验收

- 新增测试先 RED，再 GREEN。
- Agent、Automation 专项测试通过。
- 全量测试、桌面 smoke 和 `git diff --check` 通过。
