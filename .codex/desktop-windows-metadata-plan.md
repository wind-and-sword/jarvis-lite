# Jarvis Lite Windows 安装产物元数据执行计划

> 日期：2026-05-20
> 执行者：Codex

## 目标

在已能生成 `JarvisLite.exe` 和 `JarvisLiteSetup.exe` 的基础上，补齐 Windows 桌面应用安装产物的识别信息：

- `JarvisLite.exe` 使用项目内 Windows `.ico` 图标。
- PyInstaller 构建时写入 Windows 版本资源。
- 安装脚本卸载注册表里的 `DisplayVersion` 使用 `jarvis_lite.__version__`。
- 二进制构建产物仍输出到项目外 `../jarvis-lite-dist/`。

## 不做事项

- 不接入摄像头、麦克风或真实语音识别。
- 不替换 IExpress 为 Inno Setup 或 NSIS。
- 不做代码签名。
- 不把 exe 或安装器提交到 Git。

## TDD 步骤

1. 扩展 `tests/test_desktop_packaging.py`：
   - 断言默认构建路径包含 Windows 图标路径和版本资源路径。
   - 断言 `.ico` 文件存在且有标准 ICO 文件头。
   - 断言 PyInstaller 参数包含 `--icon` 和 `--version-file`。
   - 断言版本号能转换为 Windows 四段版本。
   - 断言版本资源文本包含应用名称、产品名和版本号。
2. 扩展 `tests/test_windows_installer.py`：
   - 断言安装脚本 `DisplayVersion` 来自 `jarvis_lite.__version__`。
3. 运行专项测试，确认失败。
4. 实现：
   - 新增可复现生成 `.ico` 的脚本。
   - 生成 `packaging/windows/JarvisLite.ico`。
   - 扩展桌面打包路径、版本资源生成函数和 PyInstaller 参数。
   - 构建 exe 前写入版本资源文件。
   - 安装脚本串联项目版本号。
5. 运行专项测试、全量测试、桌面 smoke、打包 exe smoke 和 `git diff --check`。
6. 更新 `word/` 文档、`README.md`、`verification.md` 和 `.codex/testing.md`。
7. 单独提交并 push 本阶段。

## 验收标准

- `tests.test_desktop_packaging` 和 `tests.test_windows_installer` 通过。
- 全量 `unittest` 通过。
- 源码桌面 smoke 输出窗口标题和对象名。
- 重新构建后的 `JarvisLite.exe --smoke` 退出码为 0。
- `JarvisLite.exe` 构建命令包含图标和版本资源。
