# Jarvis Lite 桌面更新下载体验进度

> 日期：2026-05-21
> 执行者：Codex

## 当前目标

在“检查更新”之后补齐手动下载体验，让用户能把更新清单中的安装包保存到项目外运行态目录，再自行覆盖安装。

## 已完成

- 新增 `UpdateDownloadResult`，记录当前版本、最新版本、下载地址、保存路径和写入字节数。
- 新增 `update_download_dir(project_root)`，下载目录为 `../jarvis-lite-runtime/updates/`。
- 新增 `download_update()`：
  - 先复用 `check_for_update()` 判断是否有新版本。
  - 当前已是最新版本时不创建下载目录。
  - 有新版本时支持从本地路径、`file://`、`http://` 或 `https://` 下载/复制安装包。
  - 修正 Windows 本地路径被识别为 URL scheme 的问题。
- 新增 `describe_update_download()`，返回命令行和桌面面板可读的下载结果。
- 新增 `/update-download [清单路径或URL]` 命令。
- 桌面面板和托盘快捷命令新增“下载更新”。
- 桌面桥接层把 `更新下载失败：` 识别为错误状态。

## 验证结果

- RED 验证：
  - `tests.test_update` 先因缺少 `describe_update_download` 和 `download_update` 失败。
  - `tests.test_agent` 先因 `/update-download` 返回未知命令失败。
  - `tests.test_desktop_bridge` 先因缺少 `/update-download` 快捷命令失败。
  - `tests.test_desktop_widgets` 先因面板缺少“下载更新”按钮失败。
- 专项 GREEN 验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets -v`：60 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：166 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：未发现空白错误，仅出现 CRLF 换行提示。
  - `.venv\Scripts\python.exe scripts\build_windows_installer.py`：成功生成安装器。
  - `Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru`：退出码 `0`。

## 后续建议

- 下一步可以继续做“更新清单发布约定”：生成示例 manifest、把安装器路径和版本号输出成可发布清单。
- 真正静默自动更新、安装包校验和失败回滚，仍建议放到专业安装器替换阶段。
- 摄像头、麦克风和真实语音识别继续按用户要求暂缓。
