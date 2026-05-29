# Jarvis Lite v12：桌面配置面板方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v11 连通性诊断方案，明确 `0.8.0` 的桌面端外脑与联网搜索配置体验。

## 核心结论

`0.8.0` 的主线是把命令行配置闭环搬到桌面面板：

```text
用户在桌面面板填写 provider / model / base_url / api_key
  -> 点击“写入外脑”或“写入搜索”
  -> AssistantPanel 构造既有 /llm-config-set 或 /search-config-set 命令
  -> DesktopBridge 以敏感提交方式执行真实命令
  -> transcript 与会话历史只显示“api_key 已隐藏”
  -> JarvisAgent 继续负责配置写入、校验、日志和后续检查/测试
```

检查与 smoke 仍复用已有命令：

```text
外脑：/llm-config-check、/llm-smoke 请用一句话确认连接可用
联网搜索：/search-config-check、/search-smoke Python 版本
```

## 设计边界

- 不新增 LLM provider adapter，不新增搜索 provider。
- 不把自然语言配置改成正则猜测；敏感值由用户在表单中显式填写。
- 不绕过 `JarvisAgent` 直接写配置文件，桌面层只提供表单和脱敏提交。
- API key 输入框使用密码显示；留空时不覆盖已有 key。
- API key 不进入桌面 transcript、会话历史、Agent 响应或工具日志。

## 0.8.0 收口内容

- `AssistantPanel` 增加“外脑”和“联网搜索”配置区。
- 外脑配置区支持 provider、model、base_url、api_key，以及写入、检查、测试按钮。
- 联网搜索配置区支持 provider、api_key、base_url、max_results，以及写入、检查、测试按钮。
- `DesktopBridge.send_sensitive()` 执行真实命令，但只把脱敏后的显示文本写入会话历史。
- 桌面配置写入复用 `/llm-config-set` 和 `/search-config-set`，检查和连通性测试复用已有命令。
- 项目版本同步到 `0.8.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 如果桌面配置区在真实屏幕上过于拥挤，再拆成面板 tab 或独立设置窗口。
- 如果真实 provider smoke 错误仍不可读，继续增强错误解释。
- 继续把开放式自然语言理解交给 LLM 外脑，把工具执行和本地状态更新保留在 `JarvisAgent`。
