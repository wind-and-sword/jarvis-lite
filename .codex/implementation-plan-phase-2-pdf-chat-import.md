# 阶段 2 PDF 与聊天记录导入实现计划

> 日期：2026-05-19
> 执行者：Codex

## 目标

让 `/import` 支持更多个人知识库来源：PDF 文件和通用 JSON 聊天记录。导入后仍落地为 `data/` 下的 Markdown 文档，继续复用 `/kb`、`/tag` 和 `/ask`。

## 方案取舍

1. PDF 使用主流库 `pypdf` 抽取文本，不自研 PDF 解析器。
2. PDF 不保存原文件到 `data/`，而是生成 `.md` 文本资料；当前阶段不做大模型摘要，只做可检索文本转换。
3. 聊天记录支持常见 JSON 结构：列表形式或包含 `messages` 的对象；每条消息读取 `role`/`speaker`/`from` 和 `content`/`text`/`message`。
4. 目录导入扩展为扫描 `.md`、`.txt`、`.pdf`、`.json`，其中 `.pdf` 和 `.json` 会转换成 Markdown。

## 接口契约

- `import_knowledge_path(paths, source_path, target_name=None)` 继续作为唯一导入入口。
- 单个 `.pdf` 默认导入为同名 `.md`。
- 单个 `.json` 默认导入为同名 `.md`。
- 显式 `target_name` 对 PDF/JSON 只允许 Markdown 或无后缀目标名。
- 导入结果继续返回 `KnowledgeImportSummary` / `KnowledgeDocument`。

## 验证

- 新增单测覆盖 PDF 转 Markdown、JSON 聊天记录转 Markdown、目录批量导入跳过/成功统计。
- 全量运行 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`。
- CLI 冒烟使用临时目录执行 `/import sample.json` 和 `/ask`。
