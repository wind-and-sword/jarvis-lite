# SearchRouter + LLMRouter 0.1.4 安装包计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

把已经通过验证的联网搜索总结组合流程打成新的 Windows 可安装测试包，便于用户重新安装测试。

## 范围

- 版本从 `0.1.3` 提升到 `0.1.4`。
- 安装说明标明覆盖安装行为和新版本确认方式。
- 构建 `JarvisLiteSetup.exe`，并复制版本化副本 `JarvisLiteSetup-0.1.4.exe`。
- 不提交真实 `config/llm.local.json` 或 `config/search.local.json`。
- 不推送远端。

## 任务

- [x] 修改版本一致性测试到 `0.1.4` 并确认 RED。
- [x] 更新 `pyproject.toml` 与 `jarvis_lite.__version__`。
- [x] 更新 README 安装说明。
- [x] 更新进度和验证文档。
- [x] 运行全量测试和源码桌面 smoke。
- [x] 构建 Windows 安装器。
- [x] 验证打包后 exe、安装脚本版本和完成消息。
- [x] 复制 `JarvisLiteSetup-0.1.4.exe`。
- [x] 运行静态检查、Markdown 链接检查和敏感信息扫描。
- [x] 提交发布改动。

## 验收

- `tests.test_project_metadata.ProjectMetadataTests.test_project_version_matches_release_package_version` 通过。
- 全量 `unittest discover` 通过。
- `JarvisLite.exe --smoke` 通过。
- `install.cmd` 包含 `DisplayVersion /d "0.1.4"` 和覆盖安装/保留用户数据提示。
- `JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.4 installation finished`。
- 版本化安装包副本存在且大小与主安装包一致。
