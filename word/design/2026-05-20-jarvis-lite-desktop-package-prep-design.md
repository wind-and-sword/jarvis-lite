# Jarvis Lite 桌面打包前准备设计

> 日期：2026-05-20
> 执行者：Codex

## 目标

让桌面助手具备可重复打包条件，避免把 PyInstaller 命令、输出目录和冻结运行态路径散落在临时命令中。

## 范围

- 冻结后的应用默认把用户数据放到 `%LOCALAPPDATA%\Jarvis Lite`。
- 新增桌面打包路径模型，统一管理 PyInstaller 输出目录。
- 新增 PyInstaller 参数生成函数。
- 新增桌面打包 launcher，用于冻结桌面入口。
- 新增 `scripts/build_desktop_exe.py`，统一执行 PyInstaller。
- 新增 `desktop-build` 可选依赖组。
- 不生成安装器，不接入开机自启动，不接入摄像头、麦克风或真实语音识别。

## 输出目录

打包输出默认放到项目外：

```text
../jarvis-lite-dist/
  desktop-exe/
  pyinstaller-build/
  pyinstaller-spec/
```

## 验证标准

- 普通源码运行仍使用项目根目录作为数据根。
- 冻结运行时默认使用 `%LOCALAPPDATA%\Jarvis Lite`。
- PyInstaller 参数可由代码稳定生成。
- 打包输出目录位于项目外。
- 本地测试和桌面 smoke 通过。
