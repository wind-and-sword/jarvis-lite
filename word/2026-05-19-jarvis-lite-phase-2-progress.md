# Jarvis Lite 阶段 2 进度记录

> 日期：2026-05-19
> 执行者：Codex

## 今日恢复点

根据 `日志.txt` 和 `word/2026-05-18-jarvis-lite-phase-2-progress.md`，昨日暂停点为：

- 阶段 1 已推送到 GitHub：`998f67a`。
- 阶段 2 第一批功能和暂停点文档本地领先远程 2 个提交。
- 今日已先推送本地提交，当前 `main` 与 `origin/main` 同步后再继续开发。

## 当前目标

继续阶段 2 个人知识库能力，优先完成 Markdown/txt 资料导入，让外部文本资料能进入 `data/`，随后被 `/kb` 统计并被 `/ask` 检索回答。

## 已完成

- 新增 `import_knowledge_file`，支持把外部 `.md` 或 `.txt` 文件导入 `data/`。
- 新增 `/import 源文件路径 [目标文件名]` 命令。
- 支持指定目标文件名；未指定时沿用源文件名。
- 导入时拒绝不支持的文件格式。
- 导入时拒绝覆盖 `data/` 中已存在的目标文件。
- 导入成功后记录到 `logs/jarvis.log`。
- 导入后的资料可立即被 `/kb` 统计，并可通过 `/ask` 命中。
- `/import` 现在也支持目录路径，会递归导入目录中的 `.md` 和 `.txt` 文件。
- 目录导入会保留相对目录结构，例如 `projects/notes.txt` 会写入 `data/projects/notes.txt`。
- 目录导入会跳过隐藏目录和不支持格式，并输出扫描、成功、跳过和可检索行数摘要。
- `/ask` 排序增加具体词权重：包含数字或版本号的查询词命中优先级更高，减少泛化资料靠文件名排序抢在具体资料前面的情况。
- `/ask` 和普通问题的资料回答增加命中数量摘要和编号，继续保留 `data/文件:行号` 来源格式。

## 验证结果

- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：58 个测试通过。
- `.venv\Scripts\python.exe src/app.py --once "/import .codex/import-smoke.md import-smoke.md"`：可以导入 Markdown 测试资料。
- `.venv\Scripts\python.exe src/app.py --once "/import .codex/import-smoke-dir"`：可以批量导入目录中的 Markdown 和 txt 资料。
- `.venv\Scripts\python.exe src/app.py --once "/ask Jarvis Lite 可以导入什么？"`：可以基于导入资料返回来源回答。
- `.venv\Scripts\python.exe src/app.py --once "/ask Jarvis Lite 使用什么 Python 版本？"`：可以返回带命中数量摘要、编号和来源的回答。

## 下一步

继续增强知识库导入体验：

1. 支持对导入资料做简单标签或分类。
2. 评估 PDF 摘要和聊天记录导入。
3. 再评估云数据库是否用于跨设备同步或结构化检索。
