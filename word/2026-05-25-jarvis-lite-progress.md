# Jarvis Lite 2026-05-25 进度补充记录

> 日期：2026-05-25  
> 执行者：Codex

## 当前目标

在最近文件连续操作之后，补齐建议链路和知识库摘要能力，让最近文件可以被引导导入知识库，知识库内容可以被快速概览并继续按编号操作。

## 已完成

- 最近文件导入进入下一步建议：
  - `automation.py` 的 `suggest_next_actions_from_context()` 会把最近文件建议扩展为“查看第一份最近文件；导入第一份最近文件到知识库；/recent-files”。
  - “查看最近上下文”和日报下一步建议都复用同一建议文本。
  - 本阶段只更新建议，不自动执行导入。
- 知识库摘要增强：
  - `knowledge.py` 新增 `summarize_knowledge_base()`。
  - `/kb-summary` 和 `/knowledge-summary` 可输出资料总数、可检索行数、标签和首条可检索文本预览。
  - `intent.py` 支持“总结知识库”“知识库摘要”“总结资料库”“资料库摘要”等自然语言入口。
  - 空知识库会返回明确空状态。
- 知识库摘要联动最近资料上下文：
  - `agent.py` 新增 `_knowledge_summary()`。
  - 查看摘要后，摘要资料列表会写入运行态最近资料上下文。
  - 用户可继续说“读取第一份资料”“给第二份资料打标签 项目”，新 `JarvisAgent` 实例也可恢复该列表。
  - 摘要末尾追加“可继续操作：读取第一份资料；给第一份资料打标签 标签；/ask 关键词”。
- 知识库摘要长预览截断：
  - `knowledge.py` 新增 `SUMMARY_PREVIEW_MAX_CHARS = 80` 和 `_summary_preview()`。
  - 单份资料首条文本过长时，摘要预览会截断并追加 `...`，避免输出难以扫读。
- 知识库摘要按标签分组：
  - `/kb-summary` 在逐份资料概览前新增“标签分组”段。
  - 有标签资料会按标签聚合，多标签资料可出现在多个标签组。
  - 无标签资料会进入“未标签”组，方便先扫资料类型再按编号继续操作。
  - 该阶段不改变最近资料编号顺序，不改变 `/kb`、`/ask`、导入和标签写入逻辑。
- 知识库摘要按标签后续建议：
  - `/kb-summary` 保留“读取第一份资料；给第一份资料打标签 标签；/ask 关键词”的通用提示。
  - 当知识库存在标签时，摘要末尾会额外提示 `按标签提问：/ask 标签A；/ask 标签B`。
  - 标签建议去重后按名称排序，最多展示 3 个，避免提示过长。
- 文档与进度记录审计：
  - 发现 `word/` 独立日期文档停留在 2026-05-22，后续进度散落在 2026-05-21 和 2026-05-22 的长文档中。
  - 已补充 2026-05-23 与 2026-05-25 两份进度总账，并更新 `word/文档索引.md`。

## 验证结果

- 最近文件导入建议：
  - 最近上下文和日报最近文件建议 2 个目标测试通过。
  - `tests.test_agent`：118 个测试通过。
  - `tests.test_automation`：8 个测试通过。
  - 全量测试：263 个通过。
- 知识库摘要增强：
  - 4 个目标测试通过。
  - `tests.test_knowledge`：26 个测试通过。
  - `tests.test_agent`：120 个测试通过。
  - 全量测试：267 个通过。
- 知识库摘要上下文联动：
  - 3 个目标测试通过。
  - `tests.test_agent`：123 个测试通过。
  - `tests.test_knowledge`：26 个测试通过。
  - 全量测试：270 个通过。
- 知识库摘要长预览截断：
  - 1 个目标测试通过。
  - `tests.test_knowledge`：27 个测试通过。
  - 全量测试：271 个通过。
- 知识库摘要按标签分组：
  - 1 个目标测试先失败后通过。
  - `tests.test_knowledge`：28 个测试通过。
  - `tests.test_agent`：123 个测试通过。
- 知识库摘要按标签后续建议：
  - 1 个目标测试先失败后通过。
  - 编号后续建议和最近资料上下文 2 个回归测试通过。
  - `tests.test_agent`：124 个测试通过。
  - `tests.test_knowledge`：28 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 当前交付状态

- 已提交并推送：
  - `df6e8f9 feat: 最近文件建议支持导入入口`
  - `75f6899 feat: 支持知识库摘要`
  - `4368ce8 feat: 摘要结果联动最近资料`
  - `a94e5a9 feat: 截断知识库摘要预览`
- 本轮新增：
  - 知识库摘要按标签分组
  - 知识库摘要按标签后续建议
- 对应 `.codex/` 留痕：
  - `.codex/context-scan-recent-file-import-suggestions.json`
  - `.codex/recent-file-import-suggestions-plan.md`
  - `.codex/context-scan-knowledge-summary.json`
  - `.codex/knowledge-summary-plan.md`
  - `.codex/context-scan-knowledge-summary-context.json`
  - `.codex/knowledge-summary-context-plan.md`
  - `.codex/context-scan-knowledge-summary-preview.json`
  - `.codex/knowledge-summary-preview-plan.md`
  - `.codex/context-scan-kb-summary-grouping.json`
  - `.codex/kb-summary-grouping-plan.md`
  - `.codex/context-scan-kb-summary-tag-suggestions.json`
  - `.codex/kb-summary-tag-suggestions-plan.md`
  - `.codex/testing.md`
  - `.codex/review-report.md`

## 后续建议

- 继续做知识库摘要的分组展示，例如按标签或资料来源聚合。
- 继续细化摘要后的下一步建议，例如按资料类型提示读取、打标签、提问或导入相关资料。
- 桌面入口可继续补摘要快捷入口，但应保持无参数命令优先，避免把需要用户补参的动作放入直接按钮。
