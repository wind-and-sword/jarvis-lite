# Jarvis Lite 桌面更新检查第一版进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

实现低风险更新检查能力，让用户能看到当前版本、是否有新版本、下载地址和更新说明。该阶段不做静默自动更新。

## 已完成

- 新增 `jarvis_lite.update`：
  - `UpdateManifest`：表示更新清单。
  - `UpdateCheckResult`：表示更新检查结果。
  - `is_newer_version()`：按数字段比较版本号。
  - `load_update_manifest()`：读取本地路径或 `http/https` URL 清单。
  - `check_for_update()`：读取清单并判断是否有新版本。
  - `describe_update_status()`：生成 CLI 和桌面面板可读的更新状态文本。
- 更新清单 JSON 支持字段：
  - `version`
  - `download_url`
  - `release_notes`
  - `published_at`
- 新增 `/update-status [清单路径或URL]` 命令。
- 未显式传入清单时，会读取 `JARVIS_LITE_UPDATE_MANIFEST_URL` 环境变量。
- 未配置更新源时，会显示当前版本和配置提示。
- 桌面快捷命令新增“检查更新”。
- 桌面桥接层把 `更新检查失败：` 识别为错误状态。

## 验证结果

- RED 验证：
  - `tests.test_update` 先因 `jarvis_lite.update` 模块不存在失败。
  - `tests.test_agent` 先因 `/update-status` 未接入失败。
  - `tests.test_desktop_bridge` 先因快捷命令缺少 `/update-status` 失败。
  - `tests.test_desktop_widgets` 先因面板缺少“检查更新”按钮失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v`：64 个测试通过。
- 全量验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：162 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：未发现空白错误，仅出现 CRLF 换行提示。
- 打包验证：
  - `.venv\Scripts\python.exe scripts\build_windows_installer.py`：成功生成安装器。
  - `Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru`：退出码 `0`。

## 后续建议

- 下一阶段可以做下载体验：点击更新后打开下载页或下载到项目外 dist/runtime 目录。
- 真正静默自动更新、校验安装包和失败回滚，建议放到专业安装器替换阶段。
- 摄像头、麦克风和真实语音识别继续按用户要求暂缓。
