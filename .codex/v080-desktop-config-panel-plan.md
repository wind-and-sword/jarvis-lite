# Jarvis Lite 0.8.0 桌面配置面板计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

把 0.7.0 的命令行配置闭环前移到桌面面板，让安装版用户可以在 UI 里写入、检查并测试 LLM 外脑和联网搜索配置，不再必须手敲 `/llm-config-set` 与 `/search-config-set`。

## 设计

- 在 `AssistantPanel` 增加 provider 配置区，包含外脑和联网搜索两组控件。
- 外脑控件：provider、model、base_url、api_key，以及写入、检查、测试连接按钮。
- 搜索控件：provider、api_key、base_url、max_results，以及写入、检查、测试连接按钮。
- 写入动作复用既有 slash command，不直接绕过 `JarvisAgent`。
- API key 输入框使用密码显示；写入时调用敏感提交路径，只在 transcript 和会话历史里显示“api_key 已隐藏”。
- 配置检查和 smoke 测试仍显示真实命令，因为这些命令不包含密钥。

## 边界

- 不新增正则自然语言识别。
- 不新增 LLM 或搜索 provider。
- 不提交真实 `config/*.local.json`。
- 不把 api_key 放入聊天面板、会话历史、Agent 响应或工具日志。

## TDD 验收

1. RED：DesktopBridge 可以用脱敏显示文本执行敏感命令。
2. RED：AssistantPanel 暴露 provider 配置控件默认值。
3. RED：桌面写入 LLM 配置能保存 key，但 transcript/history/log 不出现 key。
4. RED：桌面写入搜索配置能保存 key，但 transcript/history/log 不出现 key。
5. RED：配置检查和 smoke 按钮复用既有命令。
6. GREEN：实现最小桌面表单、命令构造和敏感提交。
7. 验证：目标测试、桌面/Agent/LLM/Search 邻近回归、全量 unittest、桌面 smoke、安装包构建和 packaged exe smoke。
