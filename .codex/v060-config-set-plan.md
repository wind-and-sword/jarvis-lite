# Jarvis Lite 0.6.0 本地配置写入计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

把 `0.4.0` 的“生成配置草稿”和 `0.5.0` 的“只读配置检查”推进为“可在 Jarvis Lite 内写入本地配置”的闭环：

- `/llm-config-set key=value ...`：写入 `config/llm.local.json`，支持 `provider`、`model`、`base_url`、`api_key`、`fake_response`。
- `/search-config-set key=value ...`：写入 `config/search.local.json`，支持 `provider`、`api_key`、`base_url`、`max_results`、`fake_results`。
- 命令输出只展示变更字段和下一步，不回显真实 API key。
- InnerBrain 新增“设置/修改外脑配置”“设置/修改联网搜索配置”入口，映射到无参命令用法，不猜测敏感值。
- 版本提升到 `0.6.0`，生成可安装测试包。

## 执行步骤

1. 写失败测试：
   - `/llm-config-set provider=qwen model=qwen-plus base_url=... api_key=...` 能创建并写入本地配置，响应不泄漏 key，随后 `/llm-config-check` 显示配置完整。
   - 已有 LLM 配置只改 `model` 时保留未指定字段。
   - `/search-config-set provider=tavily api_key=... max_results=3` 能创建并写入本地配置，响应不泄漏 key，随后 `/search-config-check` 显示配置完整。
   - 无效 key/provider/max_results 可读报错，并且不写入部分坏配置。
   - 自然语言“设置外脑配置”“设置联网搜索配置”返回配置写入用法。
   - 元数据版本期望 `0.6.0`。
2. 实现最小功能：
   - LLM/Search 模块新增结构化配置写入 helper。
   - Agent 命令分发新增 `/llm-config-set`、`/search-config-set`。
   - Help、LLM command 白名单、teachable intent 映射和 InnerBrain seed 样本同步新增命令。
   - 写入日志只记录字段名，不记录字段值。
3. 文档同步：
   - README、项目方案、计划索引、进度和验证记录同步 `0.6.0`。
   - 新增 `word/plans/2026-05-29-v10-runtime-config-set-plan.md`。
4. 验证与打包：
   - 目标测试、相关回归、全量 `unittest discover`。
   - 源码桌面 smoke。
   - `/llm-config-set`、`/search-config-set`、对应 check 的 CLI smoke。
   - Windows 安装器构建，复制 `JarvisLiteSetup-0.6.0.exe`。
   - 打包后 exe smoke。
   - `git diff --check`、Markdown 本地链接检查、敏感信息扫描、本地配置跟踪检查。

## 验收标准

- 写入命令可创建缺失的 `local.json`，也可保留已有未指定字段。
- 写入命令拒绝未知字段、未知 provider、非法 `max_results` 和损坏 JSON，不产生部分写入。
- 输出和日志不包含真实 API key。
- 检查命令能读取写入后的配置并显示配置完整。
- 自然语言入口只引导用户使用显式 `key=value` 命令，不通过正则猜测用户秘密。
- 0.6.0 安装包可生成并通过 smoke。
