# 项目文档整理约定

> 日期：2026-05-27
> 执行者：Codex
> 适用范围：Jarvis Lite 项目内的正式文档、过程记录、验证记录和临时日志。

## 结论

项目文档按职责拆分，避免 README、方案、索引、进度和验证记录互相重复。

核心规则：

- `README.md` 只做项目介绍和快速启动。
- `word/PROJECT-PLAN.md` 是当前项目方案唯一入口。
- `word/文档索引.md` 是正式文档唯一完整索引。
- `word/progress/YYYY-MM-DD.md` 是每日进度入口。
- `verification.md` 只做验证入口，完整验证明细进入 `verification/`。

## 目录职责

```text
README.md                         项目介绍、当前定位、快速启动
DOCUMENTATION.md                  文档整理约定
verification.md                   验证记录短入口
verification/YYYY-MM/             按月份、自然周索引和自然日归档的完整验证记录
word/PROJECT-PLAN.md              当前项目方案
word/plans/                       方案版本历史
word/design/                      专题设计文档
word/progress/YYYY-MM-DD.md       每日进度摘要
word/progress/details/            旧阶段型和功能型进度原文
word/notes/                       学习记录和专题笔记
.codex/                           Codex 本地上下文、计划、测试和审查记录
logs/                             运行日志，不作为正式文档入口
```

## README 规则

`README.md` 只保留：

- 项目一句话介绍。
- 当前路线和核心能力摘要。
- 快速启动。
- 常用命令。
- 关键文档入口。

禁止在 README 中长期追加完整进度、完整状态清单或完整文档索引。

## 方案规则

`word/PROJECT-PLAN.md` 表示当前方案，必须能回答：

- 项目现在是什么。
- 当前路线是什么。
- 已完成基础是什么。
- 下一阶段做什么。
- 哪些方向暂缓。

方案历史进入 `word/plans/`，命名为：

```text
YYYY-MM-DD-vN-topic.md
```

当前方案变化时，应新建版本文档，并更新 `word/PROJECT-PLAN.md` 和 `word/plans/README.md`。

## 进度规则

从 2026-05-27 起，正式进度按自然日记录：

```text
word/progress/YYYY-MM-DD.md
```

每日进度只写：

- 当日目标。
- 完成事项。
- 验证摘要。
- 下一步。

旧的阶段型、功能型进度记录进入 `word/progress/details/`，保留原文用于追溯，但不作为主要阅读入口。

## 验证规则

根目录 `verification.md` 只保留最近摘要和索引。

完整验证明细进入自然日文件：

```text
verification/YYYY-MM/YYYY-MM-DD.md
```

自然周文件只作为索引：

```text
verification/YYYY-MM/week-YYYY-MM-DD.md
```

其中 `week-YYYY-MM-DD.md` 的日期是该自然周周一。若某日记录继续过大，再按主题拆到同月子目录，并在日文件中保留索引。

每次新增验证记录时，需要同步更新：

- `verification.md`
- `verification/YYYY-MM/README.md`
- 对应日文件
- 对应周索引

## 索引规则

`word/文档索引.md` 是正式文档索引。新增、迁移、重命名 `word/` 下的正式文档时，必须同步更新该索引。

README 不重复完整索引，只链接到 `word/文档索引.md`。

## 临时记录规则

- `日志.txt` 只作为临时运行日志或排障日志，可以随时清空。
- 有价值的结论必须整理进 `word/`、`verification/` 或 `.codex/`。
- `.codex/` 是 Codex 本地工作目录，默认不提交；需要长期共享的结论必须整理到正式文档。
