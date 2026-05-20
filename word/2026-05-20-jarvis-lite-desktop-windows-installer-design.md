# Jarvis Lite Windows 桌面安装器设计

> 日期：2026-05-20
> 执行者：Codex

## 目标

生成 Windows 可分发安装产物，让用户可以通过安装器把 Jarvis Lite 桌面助手安装到本机用户目录。

## 范围

- 使用 PyInstaller 生成 `JarvisLite.exe`。
- 使用 Windows 系统自带 IExpress 生成 `JarvisLiteSetup.exe`。
- 安装器内包含桌面 exe、安装脚本和卸载脚本。
- 安装路径为 `%LOCALAPPDATA%\Programs\Jarvis Lite`。
- 安装脚本创建桌面快捷方式、开始菜单快捷方式和卸载快捷方式。
- 安装脚本写入当前用户卸载注册表项。
- 二进制产物输出到项目外 `../jarvis-lite-dist/`，不提交 Git。

## 不做事项

- 不接入摄像头、麦克风或真实语音识别。
- 不做系统级管理员安装。
- 不把 exe 或安装器提交到 Git。
- 不自动运行安装器修改当前系统。

## 验证标准

- 安装脚本内容包含安装目录、快捷方式和卸载注册表项。
- IExpress SED 文件指向项目外安装器输出路径和打包 exe。
- 能实际生成 `JarvisLite.exe` 和 `JarvisLiteSetup.exe`。
- 打包后的 `JarvisLite.exe --smoke` 退出码为 0。
- 全量测试通过。
