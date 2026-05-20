# Jarvis Lite 桌面面板尺寸持久化进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

继续完善桌面虚拟助手的设置体验。本阶段实现助手面板宽高的保存和恢复，让用户调整面板大小后，下次启动仍能保持同样尺寸。

## 当前取舍

- 面板尺寸保存到项目外 `../jarvis-lite-runtime/desktop-settings.json`，不进入 Git。
- 面板尺寸属于运行态偏好，不新增命令行参数。
- 本阶段不做主题切换、安装包、开机自启动、摄像头、麦克风或真实语音识别。

## 已完成

- `DesktopSettings` 新增 `panel_width` 和 `panel_height`，默认值为 `420 x 620`。
- `desktop-settings.json` 读写逻辑已包含面板宽高。
- 新增 `save_desktop_panel_size()`，保存面板尺寸时会保留小助手位置、置顶、透明度和小助手尺寸。
- `AssistantPanel` 初始化时会按运行态设置恢复面板宽高。
- `AssistantPanel` 在 resize 和 close 时保存当前面板宽高。
- 小助手置顶、透明度和尺寸设置变更时，不会覆盖已保存的面板宽高。

## 验证结果

- `.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v`：8 个桌面设置测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`：15 个桌面 widget 测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v`：3 个桌面入口测试通过。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：123 个测试通过。
- `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：可以创建桌面小助手窗口并输出 `desktopPetWindow`。
- `git diff --check`：未发现空白错误。

## 下一步

1. 继续完善桌面主题或更细的面板布局。
2. 后续再评估安装包、开机自启动和更丰富的角色素材。
3. 摄像头、麦克风和真实语音识别继续放到后续阶段。
