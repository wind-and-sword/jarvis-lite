# Jarvis Lite Windows 安装产物元数据设计

> 日期：2026-05-20
> 执行者：Codex

## 目标

在 Windows 安装器已经可生成的基础上，补齐桌面应用安装产物的基础元数据，让 `JarvisLite.exe` 更像一个正式桌面应用，而不是普通脚本打包产物。

## 范围

- 为 PyInstaller 构建加入 Windows `.ico` 图标。
- 为 PyInstaller 构建加入 Windows 版本资源文件。
- 版本资源包含应用名、产品名、文件说明、公司名和项目版本号。
- 安装脚本写入卸载注册表时，`DisplayVersion` 使用 `jarvis_lite.__version__`。
- `.ico` 源资产保存在项目内并提交 Git；exe、安装器和生成的版本资源继续输出到项目外构建目录。

## 实现方式

`jarvis_lite.desktop.packaging` 继续作为桌面打包配置中心，新增图标路径、版本资源路径和版本资源渲染函数。构建脚本在调用 PyInstaller 前先写入版本资源文件，再把 `--icon` 和 `--version-file` 参数交给 PyInstaller。

Windows 图标使用项目内 `packaging/windows/JarvisLite.ico`。该文件由项目脚本生成，避免依赖额外图片转换工具。

## 不做事项

- 不替换安装器工具。
- 不做代码签名。
- 不接入摄像头、麦克风或真实语音识别。
- 不提交任何 exe 或安装器二进制产物。

## 验证标准

- 构建参数中包含 Windows 图标和版本资源。
- 版本资源文本能反映当前项目版本。
- 安装脚本注册表版本号与项目版本一致。
- 全量本地测试通过。
- 重新构建后的 `JarvisLite.exe --smoke` 可正常退出。
