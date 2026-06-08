# Jarvis Lite 0.5.0 本地配置检查计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

把 `0.4.0` 的“生成配置草稿”推进为“生成后可本地检查”的闭环：

- `/llm-config-check`：读取当前 `config/llm.local.json` 和环境变量覆盖，展示外脑配置状态，不发起网络请求。
- `/search-config-check`：读取当前 `config/search.local.json` 和环境变量覆盖，展示搜索配置状态，不发起网络请求。
- InnerBrain 新增“检查外脑配置”“检查联网搜索配置”样本入口。
- 版本提升到 `0.5.0`，生成可安装测试包。

## 执行步骤

1. 写失败测试：
   - `/llm-config-check` 能读取当前本地配置、显示 qwen alias adapter 和 SDK Base URL、不泄漏 API key。
   - `/llm-config-check` 能报告无效 JSON。
   - `/search-config-check` 能读取当前本地配置、不泄漏 API key。
   - 自然语言“检查外脑配置”“检查联网搜索配置”进入对应命令。
   - 元数据版本期望 `0.5.0`。
2. 实现最小功能：
   - Agent 命令分发新增 `/llm-config-check`、`/search-config-check`。
   - Help、LLM 命令白名单和 teachable intent 映射同步新增命令。
   - InnerBrain seed 样本新增配置检查表达。
   - 修复 LLM 配置错误在 `provider=off` 时被吞掉的问题。
3. 文档同步：
   - README、项目方案、计划索引、进度和验证记录同步 `0.5.0`。
   - 新增 `word/plans/2026-05-29-v9-runtime-config-check-plan.md`。
4. 验证与打包：
   - 目标测试、相关回归、全量 `unittest discover`。
   - 源码桌面 smoke。
   - Windows 安装器构建，复制 `JarvisLiteSetup-0.5.0.exe`。
   - 打包后 exe smoke。
   - `git diff --check`、Markdown 本地链接检查、敏感信息扫描、本地配置跟踪检查。

## 验收标准

- 检查命令不创建、不覆盖、不修改 local.json。
- 检查命令明确写出“不发起网络请求”。
- 输出只显示 API key 是否已配置，不显示真实 key。
- 无效 JSON 能在 `/llm-config-check` 中显示为配置问题。
- 0.5.0 安装包可生成并通过 smoke。
