# 阶段 2 知识库标签实现计划

> 日期：2026-05-19
> 执行者：Codex

## 目标

为 `data/` 知识库资料增加简单标签能力，方便用户按主题分类资料，并让标签参与 `/kb` 展示和 `/ask` 检索。

## 接口契约

- 新增 `set_document_tags(paths, relative_path, tags)`：给已存在的 `.md` 或 `.txt` 资料设置标签。
- `KnowledgeDocument` 增加 `tags` 字段，默认空元组。
- `build_knowledge_index` 和 `describe_knowledge_base` 读取标签元数据。
- `search_data` 在文本命中之外，把文档标签作为轻量检索信号。
- 新增 CLI 命令 `/tag 文件名 标签...`。

## 存储方案

使用 `data/.knowledge-tags.json` 保存元数据。该文件位于知识库根目录，使用标准库 `json` 读写，不引入数据库或第三方依赖。

## 实施步骤

1. 新增 `tests/test_knowledge.py` 红灯测试：设置标签后 `build_knowledge_index` 可读回标签。
2. 新增红灯测试：`describe_knowledge_base` 显示资料标签。
3. 新增红灯测试：`search_data` 可通过标签命中文档内容。
4. 新增 `tests/test_agent.py` 红灯测试：`/tag 文件名 标签...` 可更新标签，缺参时提示用法。
5. 实现 JSON 元数据读写、标签规范化、文档存在校验和 `/tag` 命令。
6. 运行全量 `unittest` 和 CLI 冒烟验证。
7. 更新 README、`word/` 进度文档、`verification.md` 和 `.codex` 记录。

## 风险

- 当前标签只服务于本地单机知识库，不处理多设备冲突。
- 标签检索仍属于规则式关键词匹配，不提供语义分类。
