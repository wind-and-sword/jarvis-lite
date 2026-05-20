# Jarvis Lite 桌面安装生命周期收口进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

补齐 Windows 安装器的基础生命周期，先把卸载和覆盖安装体验收稳，为下一阶段更新机制做准备。

## 已完成

- 安装脚本在复制新 exe 前执行 `taskkill /IM JarvisLite.exe /F`，降低覆盖安装时文件被占用的概率。
- 安装脚本继续使用用户级安装目录 `%LOCALAPPDATA%\Programs\Jarvis Lite`。
- 卸载注册表增加：
  - `DisplayIcon`
  - `QuietUninstallString`
- 卸载脚本在清理文件前执行 `taskkill /IM JarvisLite.exe /F`。
- 卸载脚本会清理：
  - 桌面快捷方式 `Jarvis Lite.lnk`
  - 开始菜单快捷方式 `Jarvis Lite.lnk`
  - 开始菜单卸载快捷方式 `Uninstall Jarvis Lite.lnk`
  - 当前用户 Startup 中的 `Jarvis Lite.lnk`
  - 开始菜单目录
  - 当前用户卸载注册表项
  - 安装目录 `%LOCALAPPDATA%\Programs\Jarvis Lite`
- 卸载脚本明确保留 `%LOCALAPPDATA%\Jarvis Lite` 用户数据目录。

## 验证结果

- RED 验证：
  - `tests.test_windows_installer` 先因安装脚本缺少进程关闭步骤失败。
  - `tests.test_windows_installer` 先因安装脚本缺少 `DisplayIcon` 和 `QuietUninstallString` 失败。
  - `tests.test_windows_installer` 先因卸载脚本缺少 Startup 清理失败。
  - `tests.test_windows_installer` 先因卸载脚本缺少用户数据保留约定失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v`：7 个测试通过。
- 全量验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：157 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：未发现空白错误，仅出现 CRLF 换行提示。
- 打包验证：
  - `.venv\Scripts\python.exe scripts\build_windows_installer.py`：成功生成安装器。
  - `Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru`：退出码 `0`。

## 后续建议

- 下一阶段开始做更新机制第一版：版本清单、检查更新、更新提示和下载入口。
- 更顺滑的静默自动更新仍建议放到替换专业安装器之后。
- 摄像头、麦克风和真实语音识别继续按用户要求暂缓。
