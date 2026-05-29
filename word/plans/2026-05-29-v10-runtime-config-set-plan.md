# Jarvis Lite v10：运行态配置写入方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v8 运行态配置初始化和 v9 本地配置检查方案，明确 `0.6.0` 的本地配置写入闭环。

## 核心结论

`0.6.0` 的主线是让用户不必手动打开 JSON，也能在 Jarvis Lite 内完成外脑和联网搜索的本地配置写入：

```text
用户输入：/llm-config-set provider=qwen model=qwen-plus base_url=https://.../v1/responses api_key=...
  -> JarvisAgent 解析 key=value 参数
  -> LLM 配置 helper 读取现有 config/llm.local.json
  -> 校验允许字段、provider 和 JSON 结构
  -> 覆盖指定字段，保留未指定字段
  -> 写回 local.json
  -> 输出变更字段、配置路径、下一步检查命令
```

联网搜索同理：

```text
用户输入：/search-config-set provider=tavily api_key=... max_results=3
  -> 结构化写入 config/search.local.json
  -> 校验 provider 和 max_results
  -> 输出 /search-config-check 与 /search-enable 下一步
```

## 设计边界

- 不从自然语言中猜测 API key、URL 或模型名；缺参数时只给出命令模板。
- 不显示真实 API key；响应和日志只记录字段名。
- 不新增 Gemini/Qwen 原生 SDK；`qwen`/`gemini` 继续作为 OpenAI-compatible alias。
- 不扩大正则自然语言解析，只增加 InnerBrain seed 样本让“设置配置”进入命令用法。
- 本地 `config/*.local.json` 继续属于运行态文件，不提交到 Git。

## 0.6.0 收口内容

- 新增 `/llm-config-set key=value ...`。
- 新增 `/search-config-set key=value ...`。
- InnerBrain seed 样本增加“设置外脑配置”“修改外脑配置”“设置联网搜索配置”“修改搜索配置”。
- README、项目方案、验证记录和版本同步到 `0.6.0`。

## 后续方向

- 如果用户测试仍觉得命令行输入复杂，再做桌面配置表单。
- 真实 provider 失败时继续增强 `/llm-smoke` 和 `/search` 的错误解释。
- 继续把用户实际表达沉淀为 InnerBrain runtime/seed 样本，但自然语言开放理解仍优先交给外脑 LLM。
