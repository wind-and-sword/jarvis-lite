# Jarvis Lite 桌面面板尺寸持久化设计

> 日期：2026-05-20
> 执行者：Codex

## 目标

让桌面助手面板在用户调整大小后保存宽高，并在下次启动时恢复，减少每次启动后重新调整窗口的成本。

## 范围

- 在桌面运行态设置中增加面板宽度和高度。
- 面板启动时读取并恢复上次保存的宽高。
- 面板被用户调整大小后保存宽高。
- 面板关闭时再次保存当前宽高。
- 不做主题切换、安装包、开机自启动、摄像头、麦克风或真实语音识别。

## 实现边界

- `DesktopSettings` 继续保存桌面运行态设置，新增 `panel_width` 和 `panel_height`。
- `settings.py` 新增 `save_desktop_panel_size()`，保存面板尺寸时保留已有位置、置顶、透明度和小助手尺寸。
- `AssistantPanel` 负责恢复和保存自己的尺寸，不改变 `DesktopPetWindow` 的位置保存逻辑。
- 面板尺寸仍保存到项目外 `../jarvis-lite-runtime/desktop-settings.json`，不进入 Git。

## 验证标准

- 保存并读取 `panel_width`、`panel_height`。
- 保存面板尺寸时不会丢失小助手位置和偏好。
- `AssistantPanel` 初始化后恢复设置中的面板宽高。
- 用户调整面板大小后，运行态设置文件记录新宽高。
- 桌面设置、桌面窗口、桌面入口和全量测试通过。
