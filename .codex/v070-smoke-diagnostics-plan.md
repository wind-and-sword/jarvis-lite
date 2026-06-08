# Jarvis Lite 0.7.0 连通性诊断计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

把 `0.6.0` 的“本地配置写入”推进为“写入后可直接测试 provider 连通性”的闭环：

- `/llm-smoke [prompt]`：执行前重新读取当前本地配置，减少桌面运行中手动改配置后还要显式 `/llm-enable` 的摩擦。
- `/search-smoke [query]`：对当前 SearchRouter 做一次可控连通性测试，默认查询 `Python 版本`，不写入最近搜索上下文。
- InnerBrain 新增“测试外脑连接”“测试联网搜索连接”入口。
- 版本提升到 `0.7.0`，生成可安装测试包。

## 执行步骤

1. 写失败测试：
   - `/llm-smoke` 在 Agent 已启动后能读取随后写入的 `config/llm.local.json`。
   - `/search-smoke` 在 Agent 已启动后能读取随后写入的 `config/search.local.json`，返回调用成功和来源预览。
   - `/search-smoke` 不污染最近联网搜索上下文。
   - 自然语言“测试外脑连接”“测试联网搜索连接”进入对应 smoke 命令。
   - 元数据版本期望 `0.7.0`。
2. 实现最小功能：
   - Agent 的 `/llm-smoke` 在非注入 router 时重新构建 LLMRouter。
   - Agent 新增 `/search-smoke [query]` 命令和格式化输出。
   - Help、LLM command 白名单、teachable intent 映射和 InnerBrain seed 样本同步新增 smoke 入口。
3. 文档同步：
   - README、项目方案、计划索引、进度和验证记录同步 `0.7.0`。
   - 新增 `word/plans/2026-05-29-v11-smoke-diagnostics-plan.md`。
4. 验证与打包：
   - 目标测试、相关回归、全量 `unittest discover`。
   - 源码桌面 smoke。
   - `/llm-smoke`、`/search-smoke` CLI smoke。
   - Windows 安装器构建，复制 `JarvisLiteSetup-0.7.0.exe`。
   - 打包后 exe smoke。
   - `git diff --check`、Markdown 本地链接检查、敏感信息扫描、本地配置跟踪检查。

## 验收标准

- LLM smoke 每次读取最新本地配置，但注入 router 的测试场景不被重建破坏。
- Search smoke 会明确提示这是 provider 调用，并在成功时展示前几条来源，在失败时展示可读错误。
- Search smoke 不更新最近联网搜索上下文，不影响 `/search-open`、`/search-compare` 等后续动作。
- 输出不显示真实 API key。
- 0.7.0 安装包可生成并通过 smoke。
