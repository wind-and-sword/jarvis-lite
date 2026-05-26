# Jarvis Lite 2026-05-26 进度补充记录

> 日期：2026-05-26  
> 执行者：Codex

## 当前目标

继续完善知识库标签工作流。昨天已经完成 `/kb-summary` 标签分组、按标签读取资料组和摘要页按标签读取建议；今天补上标签组批量操作前预览和确认闭环，让用户能先看影响范围，再决定确认或取消。

## 已完成

- 标签组批量打标签前预览：
  - `intent.py` 支持“给项目标签资料都打标签 归档”这类表达。
  - `agent.py` 新增标签组批量打标签预览逻辑，复用 `build_knowledge_index()` 按标签筛选资料。
  - 输出每份资料的当前标签和预览标签，明确说明“这里只生成预览，不会修改资料标签”。
  - 预览命中资料会写入最近资料列表，后续可继续“读取第二份资料”或按输出建议逐份执行“给第一份资料打标签 项目 归档”。
  - 标签组不存在时返回明确提示，并建议先查看 `/kb-summary`。
- 标签组批量打标签确认闭环：
  - 预览后，同一会话内说“确认执行”会逐份追加预览标签。
  - 预览后说“取消执行”会清空待确认状态，不修改资料标签。
  - 确认或取消后再次“确认执行”不会重复写入。
  - 准备执行经验建议命令时会清空标签组待确认状态，避免两个待确认任务争用同一个确认入口。
- 标签组待确认状态接入最近上下文：
  - 批量打标签预览后，“查看最近上下文”会显示待确认批量打标签、追加标签和影响资料数量。
  - 确认执行后再次查看最近上下文，会显示待确认批量打标签为无。
  - 待确认建议命令展示保持独立，不会把批量标签任务误写成建议命令。
- 标签组批量操作恢复提示：
  - 确认执行后会追加 `操作记录：本次已更新 N 份资料。`
  - 确认执行后会给出逐份恢复命令，例如“给第一份资料打标签 项目 助手”。
  - 恢复提示只基于确认前标签生成，不新增持久化撤销栈。
- 标签组批量操作摘要接入最近上下文：
  - 确认执行后，“查看最近上下文”会显示最近一次批量打标签摘要。
  - 摘要包含标签组、追加标签、成功更新数量和恢复提示。
  - 本轮只保存当前 Agent 会话内最近一次操作，不新增持久化历史结构。
- 最近批量标签操作摘要持久化：
  - `RuntimeContext` 新增最近批量标签操作摘要字段。
  - `agent-context.json` 会保存标签组、追加标签、成功更新数量和恢复命令。
  - 新 `JarvisAgent` 实例执行“最近上下文状态”时可恢复最近批量打标签摘要。
- 批量标签操作历史命令：
  - `RuntimeContext` 新增最近批量标签操作历史列表，并兼容旧的单条摘要字段。
  - 确认执行批量打标签后会把本次操作插入历史首位，最多保留 5 条。
  - `/tag-history` 和“查看批量标签历史”会按新到旧列出标签组、追加标签、更新数量和恢复提示。
- 桌面批量标签历史快捷入口：
  - 桌面面板和托盘快捷命令新增“标签历史”入口。
  - “标签历史”直接执行 `/tag-history`，复用 Agent 已有历史输出。
  - 该入口加入无参数直接快捷命令集合，不影响仍需参数的“整理预览”。
- 批量标签历史影响资料读取：
  - `RuntimeTaggedDocumentsOperationContext` 新增受影响资料路径列表，旧历史缺少路径时仍可展示摘要。
  - 确认执行批量打标签后会把影响资料路径写入历史记录。
  - “读取第一条标签历史资料”会恢复该历史的资料列表，并支持继续“读取第二份资料”。

## 验证结果

- 标签组批量打标签前预览：
  - 2 个 Agent 目标测试先失败后通过。
  - 普通自然语言打标签、按编号给最近资料打标签、按标签读取资料组和摘要按标签读取建议回归通过。
  - `tests.test_knowledge`：28 个测试通过。
- 标签组批量打标签确认闭环：
  - 2 个 Agent 目标测试先失败后通过。
  - 经验建议确认、经验建议草稿确认、普通打标签和标签预览回归通过。
  - `tests.test_knowledge`：28 个测试通过。
- 标签组待确认状态接入最近上下文：
  - 1 个 Agent 目标测试先失败后通过。
  - 最近上下文待确认建议、最近建议、空状态、标签组确认和取消回归通过。
- 标签组批量操作恢复提示：
  - 1 个 Agent 目标测试先失败后通过。
  - 标签组确认、取消、最近上下文、普通打标签和编号资料打标签回归通过。
- 标签组批量操作摘要接入最近上下文：
  - 1 个 Agent 目标测试先失败后通过。
  - 最近上下文待确认批量标签、空状态、标签组确认、恢复提示和取消回归通过。
- 最近批量标签操作摘要持久化：
  - 1 个 Agent 跨实例恢复目标测试先失败后通过。
  - 最近资料列表、最近文件列表、最近建议、当前批量摘要、确认恢复提示和取消回归通过。
- 批量标签操作历史命令：
  - 1 个 Agent 跨实例历史目标测试先失败后通过。
  - 最近批量摘要、标签组确认、恢复提示和取消回归通过。
- 桌面批量标签历史快捷入口：
  - 2 个桌面桥接测试和 2 个桌面面板测试先失败后通过。
  - 桌面桥接、面板和托盘专项 32 个测试通过。
- 批量标签历史影响资料读取：
  - 1 个 Agent 跨实例目标测试先失败后通过。
  - 批量标签历史、最近批量摘要、最近资料列表和恢复提示回归通过。
- 收尾验证：
  - 全量测试：287 个通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 当前交付状态

- 本轮新增：
  - 标签组批量打标签前预览
  - 标签组批量打标签确认闭环
  - 标签组待确认状态接入最近上下文
  - 标签组批量操作恢复提示
  - 标签组批量操作摘要接入最近上下文
  - 最近批量标签操作摘要持久化
  - 批量标签操作历史命令
  - 桌面批量标签历史快捷入口
  - 批量标签历史影响资料读取
- 对应 `.codex/` 留痕：
  - `.codex/context-scan-tagged-documents-tag-preview.json`
  - `.codex/tagged-documents-tag-preview-plan.md`
  - `.codex/context-scan-confirm-tagged-documents-tagging.json`
  - `.codex/confirm-tagged-documents-tagging-plan.md`
  - `.codex/context-scan-pending-tagged-documents-recent-context.json`
  - `.codex/pending-tagged-documents-recent-context-plan.md`
  - `.codex/context-scan-tagged-documents-undo-hints.json`
  - `.codex/tagged-documents-undo-hints-plan.md`
  - `.codex/context-scan-tagged-documents-operation-summary.json`
  - `.codex/tagged-documents-operation-summary-plan.md`
  - `.codex/context-scan-persistent-tagged-documents-operation.json`
  - `.codex/persistent-tagged-documents-operation-plan.md`
  - `.codex/context-scan-batch-tag-history.json`
  - `.codex/batch-tag-history-plan.md`
  - `.codex/context-scan-desktop-tag-history-entry.json`
  - `.codex/desktop-tag-history-entry-plan.md`
  - `.codex/context-scan-tag-history-document-list.json`
  - `.codex/tag-history-document-list-plan.md`
  - `.codex/testing.md`
  - `.codex/review-report.md`

## 后续建议

- 可以继续把标签组预览结果接入桌面摘要展示，让面板中更容易扫读多资料影响范围。
- 可以继续给批量标签历史增加按编号恢复单份资料标签的辅助提示。
