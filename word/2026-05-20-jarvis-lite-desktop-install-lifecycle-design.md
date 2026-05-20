# Jarvis Lite 桌面安装生命周期收口设计

> 日期：2026-05-20
> 执行者：Codex

## 目标

补齐 Windows 安装器的卸载生命周期，让安装、覆盖安装和卸载行为更接近正式桌面应用，并为后续更新机制打基础。

## 范围

- 安装脚本在复制新 exe 前尝试关闭正在运行的 `JarvisLite.exe`，避免覆盖安装时文件被占用。
- 卸载脚本清理桌面快捷方式、开始菜单快捷方式、开始菜单目录、卸载注册表和当前用户 Startup 中的 `Jarvis Lite.lnk`。
- 卸载脚本尝试关闭正在运行的 `JarvisLite.exe`，避免安装目录清理失败。
- 卸载默认保留用户数据目录 `%LOCALAPPDATA%\Jarvis Lite`，包括记忆、知识库、日志和桌面运行态设置。
- 卸载注册表增加 `DisplayIcon` 和 `QuietUninstallString`，让 Windows 应用列表和卸载入口更完整。

## 设计边界

本阶段仍使用 IExpress 产物，不替换安装器技术栈。IExpress 能覆盖安装，但不适合做完整的静默自动更新、差分更新或失败回滚，所以更新机制会在下一阶段单独设计。

卸载默认保留用户数据。删除用户数据需要单独的“清除个人数据”能力，避免卸载时误删记忆和知识库。

## 不做事项

- 不接入摄像头、麦克风或真实语音识别。
- 不做自动更新下载器。
- 不替换为 Inno Setup、NSIS 或 Squirrel.Windows。
- 不做代码签名。
- 不删除 `%LOCALAPPDATA%\Jarvis Lite` 用户数据。

## 验证标准

- 安装脚本包含运行进程关闭步骤。
- 安装脚本写入 `DisplayIcon` 和 `QuietUninstallString`。
- 卸载脚本包含运行进程关闭步骤。
- 卸载脚本清理 Startup 开机启动快捷方式。
- 卸载脚本明确保留用户数据目录。
- 安装器测试、全量测试、源码桌面 smoke、安装器构建和打包 exe smoke 通过。
