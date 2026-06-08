# 最近目录上下文计划

> 日期：2026-05-21
> 执行者：Codex

## 上下文扫描

- 自然语言解析集中在 `src/jarvis_lite/intent.py`，目录类表达已经支持 `打开项目目录`、`整理项目目录`、`打开桌面`、`整理桌面`。
- Agent 已有 `JarvisAgent._recent_document_path`，用于“这个资料”指代最近单个资料。
- 目录打开由 `_open_directory_path()` 记录请求；整理预览由 `_organize_preview()` 调用 `preview_file_organization()`。
- 路线文档 `word/2026-05-21-jarvis-lite-natural-language-brain-progress.md` 建议继续沉淀“最近目录”“最近搜索结果”等上下文。
- `code-index`、`sequential-thinking`、`shrimp-task-manager` 当前工具列表不可用，本轮使用 `rg`、源码阅读、`update_plan` 和本地 unittest 作为降级方案。

## 范围

- 支持用户先打开或整理某个目录后，再说“整理这个目录”“打开这个目录”。
- 最近目录上下文只保存在当前 `JarvisAgent` 实例内，不跨进程持久化。
- 最近目录包含常用目录别名或已知目录别名，以及解析出的绝对路径。
- 无上下文时给出明确提示，不再把“这个目录”误当成目录别名。

## 不做

- 不做跨会话最近目录持久化。
- 不做任意路径的自然语言整理。
- 不移动、删除或实际整理文件，仍然只生成整理预览。

## 验收

- RED：新增测试先失败，证明“这个目录”当前会被当成别名。
- GREEN：打开常用目录后，“整理这个目录”能预览同一目录。
- GREEN：无最近目录时，“打开这个目录”给出最近目录缺失提示。
- 全量 `unittest`、桌面 smoke、`git diff --check` 通过。
