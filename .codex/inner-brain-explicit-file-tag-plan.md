# InnerBrain 显式文件名标签槽位迁移计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

把 `给 note.txt 打标签 项目`、`把 data/note.txt 标记为 项目 Python` 这类显式文件名标签表达从 `legacy_fallback` 迁移到 InnerBrain 样本分类器。

## 约束

- 样本分类器负责自然语言主识别。
- 正则只抽 `path` 和 `tags` 槽位。
- Agent 执行层继续复用 `/tag`，不新增平行标签实现。
- 仅覆盖知识库支持的 `.md`、`.txt` 资料文件。

## 任务

- [x] 改写 InnerBrain 回归测试，先确认显式文件名标签仍走 legacy。
- [x] 新增 `document.tag_path` seed 样本。
- [x] 新增 tag path 签名归一化。
- [x] 新增 `path` 与 `tags` 槽位抽取。
- [x] 映射为 `/tag "path" tags...`。
- [x] 跑目标 InnerBrain 和 Agent 标签回归。
- [x] 更新文档和验证记录。
- [x] 运行全量回归和静态检查。
- [ ] 提交改动。

## 验收

- `InnerBrain.understand("给 note.txt 打标签 项目")` 返回 `source=seed_sample`。
- `InnerBrain.understand("把 data/note.txt 标记为 项目 Python")` 抽取 `path=note.txt` 和两个标签。
- `JarvisAgent.handle("给 note.txt 打标签 项目 Python")` 仍更新 `data/note.txt` 标签。
