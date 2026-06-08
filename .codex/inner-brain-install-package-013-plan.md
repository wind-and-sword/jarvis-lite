# InnerBrain 0.1.3 Install Package Plan

> 日期：2026-05-28
> 执行者：Codex
> 目标：把 InnerBrain v1、样本采纳、人工标注和口语教学入口收口为 `0.1.3` 可安装测试版。

## 任务 1：版本 TDD

- [x] 增加失败测试，要求 `pyproject.toml` 与 `jarvis_lite.__version__` 一致且为 `0.1.3`。
- [x] RED 验证。
- [x] 更新 `pyproject.toml` 与 `src/jarvis_lite/__init__.py`。
- [x] GREEN 验证。

## 任务 2：文档与验证口径

- [x] 更新 README 当前版本和安装完成提示。
- [x] 更新今日进度、验证入口、月索引和日验证明细。
- [x] 更新 `.codex/testing.md`、`.codex/review-report.md`、`.codex/operations-log.md`。

## 任务 3：构建安装包

- [x] 刷新 editable 安装，使入口点使用 `0.1.3`。
- [x] 运行全量测试、源码桌面 smoke、打包脚本。
- [x] 验证打包后 `JarvisLite.exe --smoke`。
- [x] 验证 `install.cmd`、SED 完成消息和版本化安装包副本。
- [x] 静态检查、Markdown 链接检查、敏感信息扫描。
- [x] 提交并推送。
