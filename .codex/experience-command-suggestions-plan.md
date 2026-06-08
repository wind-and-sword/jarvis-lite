# 经验建议命令联动第一版计划

> 日期：2026-05-22
> 执行者：Codex

## 目标

让 `/experience-advice 关键词` 在引用经验之外，给出可直接执行的下一步命令，减少用户在 `/help` 中查找命令的成本。

## 方案

- 在 `JarvisAgent` 内新增私有方法，根据关键词返回固定命令建议。
- 第一版只覆盖现有能力：导入、标签、知识库、日报、目录、更新、语音、经验。
- 不新增命令解析器、不新增配置文件、不调用大模型。

## 验收

- `/experience-advice 导入资料` 输出 `/import`、`/kb`、`/tag` 建议。
- 没有相关经验但有已知命令时，仍输出命令建议。
- “导入资料有什么建议”复用同一输出。
- RED/GREEN 过程记录到 `.codex/testing.md` 和 `verification.md`。
- 全量 unittest、桌面 smoke、`git diff --check` 通过。
