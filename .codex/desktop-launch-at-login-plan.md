# Jarvis Lite 桌面开机自启动执行计划

> 日期：2026-05-20
> 执行者：Codex

## 当前审查结论

本轮先做了新鲜验证和后续建议检查：

- `main` 与 `origin/main` 同步，无未提交变更。
- 全量测试 137 个通过。
- 源码桌面 smoke 正常。
- 打包 exe smoke 退出码为 0。
- 打包 exe 版本信息可读取。

未发现必须先修的回归问题。继续推进下一个不依赖硬件和外部证书的阶段：桌面开机自启动。

## 目标

给桌面助手增加当前用户级“开机启动”能力：

- 设置面板增加“开机启动”开关。
- 运行态设置保存 `launch_at_login`。
- Windows 启用时创建当前用户 Startup 目录中的 `Jarvis Lite.lnk`。
- Windows 关闭时删除该快捷方式。
- 测试通过注入 runner 验证命令，不在自动化测试里真实修改用户系统。

## 不做事项

- 不接入摄像头、麦克风或真实语音识别。
- 不做管理员级系统服务。
- 不写注册表启动项。
- 不做代码签名。
- 不替换安装器。

## TDD 步骤

1. 新增 `tests/test_desktop_autostart.py`，先确认 `jarvis_lite.desktop.autostart` 不存在。
2. 扩展 `tests/test_desktop_settings.py`，先确认 `DesktopSettings` 缺少 `launch_at_login`。
3. 扩展 `tests/test_desktop_widgets.py`，先确认面板没有开机启动设置值。
4. 扩展 `tests/test_desktop_app.py`，先确认设置应用没有同步自启动的边界函数。
5. 实现 autostart 模块、设置字段、面板 checkbox 和 app 同步函数。
6. 跑专项测试、全量测试、桌面 smoke 和 `git diff --check`。
7. 更新 `word/` 文档、`README.md`、`verification.md` 和 `.codex/testing.md`。
8. 单独提交并 push 本阶段。
