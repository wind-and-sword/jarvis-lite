# Jarvis Lite 桌面安装生命周期收口执行计划

> 日期：2026-05-20
> 执行者：Codex

## 目标

收口 Windows 安装生命周期，重点补齐卸载清理、覆盖安装前置处理和用户数据保留约定。

## 文件范围

- 修改 `tests/test_windows_installer.py`：用 TDD 固化安装/卸载脚本行为。
- 修改 `src/jarvis_lite/desktop/windows_installer.py`：更新 install/uninstall 脚本渲染。
- 更新 `README.md`、`verification.md`、`word/文档索引.md`。
- 新增 `word/2026-05-20-jarvis-lite-desktop-install-lifecycle-progress.md`。
- 更新 `.codex/testing.md` 和 `.codex/operations-log.md`，本地留痕不提交。

## TDD 步骤

1. 扩展 `tests/test_windows_installer.py`：
   - 安装脚本包含 `taskkill /IM JarvisLite.exe /F`。
   - 安装脚本写入 `DisplayIcon` 和 `QuietUninstallString`。
   - 卸载脚本包含 Startup 目录和 `Jarvis Lite.lnk` 清理。
   - 卸载脚本包含运行进程关闭步骤。
   - 卸载脚本保留 `%LOCALAPPDATA%\Jarvis Lite` 用户数据。
2. 运行专项测试，确认 RED。
3. 更新 `render_install_script()` 和 `render_uninstall_script()`。
4. 运行专项测试，确认 GREEN。
5. 更新正式文档和验证记录。
6. 运行全量测试、源码桌面 smoke、安装器构建、打包 exe smoke、`git diff --check`。
7. 单独提交并 push 本阶段。
