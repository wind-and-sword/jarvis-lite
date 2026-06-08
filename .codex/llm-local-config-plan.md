# LLM 外脑本地配置计划

> 日期：2026-05-28  
> 执行者：Codex

## 目标

- 让 Jarvis Lite 从 `config/llm.local.json` 读取外脑 provider、model、base_url、api_key。
- 保留环境变量覆盖能力，方便临时调试。
- 新增可提交的 `config/llm.example.json`，真实 `config/llm.local.json` 由 `.gitignore` 忽略。
- 让“开启外脑”进入外脑配置引导或状态说明，不再落入长期记忆摘要。

## 实现步骤

1. RED：新增配置目录、本地配置读取、环境变量覆盖、Agent 自动读取配置和“开启外脑”入口测试。
2. GREEN：扩展 `ProjectPaths.config_dir`、`LLMSettings.from_sources()`、`build_llm_router(paths=...)` 和 Agent `/llm-enable` 引导。
3. 文档：更新 README、项目计划、当天进度和验证记录，说明安装版配置路径和真实密钥处理方式。
4. 验证：运行目标测试、全量 unittest、桌面 smoke、diff check、Markdown 链接检查和敏感信息扫描。

## 决策

- 不把真实 API key 写入 Git。即使仓库是私有仓库，密钥进入 Git 历史后仍会出现在备份、日志、远端历史和后续复制包里。
- Git 中提交的是结构、模板和加载逻辑；真实值放在本地 `config/llm.local.json`。
