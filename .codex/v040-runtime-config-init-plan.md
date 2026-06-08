# 0.4.0 运行态配置初始化计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

让用户安装后不需要手动复制模板，也能通过命令或自然语言生成本机 `local.json` 配置草稿：

- `/llm-config-init [provider]`：生成 `config/llm.local.json`，默认 `openai-compatible`，支持 `qwen`、`gemini` 等现有 provider。
- `/search-config-init [provider]`：生成 `config/search.local.json`，默认 `tavily`。
- 草稿不写真实 API key；`api_key`、`model`、`base_url` 保持空值，避免误触发真实网络调用。
- 已存在配置时不覆盖，并且不打印已有 API key。
- InnerBrain 增加“生成外脑配置”“生成联网搜索配置”等自然语言入口，仍由 `JarvisAgent` 执行。

## 验收契约

- 新命令创建本地配置文件，并在响应里给出相对路径、provider、下一步命令。
- LLM alias provider 初始化时显示实际 adapter。
- 已存在本地配置时返回“已存在/未覆盖”，文件内容不变，响应不泄漏 key。
- 搜索配置初始化后 `/search-enable` 可读取该草稿并报告缺少 API key，不触发网络调用。
- 帮助文案、README、方案文档、验证记录同步到 `0.4.0`。

## TDD 顺序

1. Agent 测试：LLM qwen 配置草稿创建。
2. Agent 测试：LLM 已有配置不覆盖且不泄漏 key。
3. Agent 测试：Search tavily 配置草稿创建。
4. Agent 测试：自然语言配置初始化入口。
5. 版本一致性测试提升到 `0.4.0`。
6. 实现代码、跑专项、全量、桌面 smoke、打包 smoke 和静态验证。
