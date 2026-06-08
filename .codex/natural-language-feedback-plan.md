# 用户日志自然语言识别修复计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

把用户真实安装日志中暴露的自然语言缺口收敛成本地可回归能力，并生成可区分的新安装包。

## 任务

1. 补 RED 测试：`早上好`、`你好`、`你叫什么名字`、删除桌面两个指定快捷方式、缺失快捷方式提示、桌面 bridge 问候和安装完成版本提示。
2. 扩展 `NaturalLanguageIntent`：新增问候、助手身份、桌面快捷方式删除意图。
3. 扩展 `JarvisAgent`：问候直接回复，助手身份直接回复，删除动作仅处理桌面目录下明确点名的 `.lnk` 文件。
4. 更新安装器：安装脚本 echo 和 IExpress `FinishMessage` 带当前版本。
5. 版本提升到 `0.1.2`，刷新 editable 安装并重新生成 Windows 安装包。
6. 更新 README、当前方案、每日进度、验证记录和 `.codex` 本地留痕。

## 验收

- 目标 8 个测试 RED 后 GREEN。
- 相关回归 188 个测试通过。
- 全量 `unittest discover` 通过。
- 源码桌面 smoke 和打包后 exe smoke 通过。
- `JarvisLiteSetup-0.1.2.exe` 生成到项目外 `..\jarvis-lite-dist\`。
