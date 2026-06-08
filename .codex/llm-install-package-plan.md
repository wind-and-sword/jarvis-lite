# LLM 调用收口与新版打包计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

补齐 LLM 外脑第一版进入用户测试前的小任务，并构建一个新的 Windows 安装包。

## 实施步骤

1. RED：补 Agent 测试，覆盖 `/llm-context-preview`、LLM command 硬白名单拒绝未知命令、help 展示新命令。
2. RED：补 LLM 测试，覆盖 `/llm-status` API key/网络调用诊断、OpenAI provider 401/429 等错误可读化且不泄露 key。
3. RED：补安装器测试，覆盖覆盖安装文案和用户数据保留提示。
4. GREEN：抽出 LLM 可执行命令白名单，Provider instructions 和 Agent 执行校验共用同一来源。
5. GREEN：新增 `/llm-context-preview`，只展示 fallback context，不调用 provider。
6. GREEN：增强 `LLMRouter.describe()` 和 `OpenAIResponsesProvider` 错误格式化。
7. GREEN：安装脚本补充覆盖安装和用户数据保留提示，版本号提升到 `0.1.1`。
8. 文档：更新 README、项目计划、5 月 28 日进度和验证记录，明确已安装用户默认覆盖安装。
9. 验证：专项测试、全量 unittest、桌面 smoke、diff/link/敏感信息检查。
10. 打包：运行 Windows 安装器构建脚本，验证 exe smoke 和安装器产物路径。
11. 收尾：生成审查/测试留痕，提交并推送。
