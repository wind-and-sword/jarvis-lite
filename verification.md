# 验证记录

> 日期：2026-05-21
> 执行者：Codex

## 验证命令

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip show pypdf
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_assets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe src/app.py --once "/memory"
.\.venv\Scripts\python.exe src/app.py --once "/status"
.\.venv\Scripts\python.exe src/app.py --once "/kb"
.\.venv\Scripts\python.exe src/app.py --once "/import .codex/import-smoke.md import-smoke.md"
.\.venv\Scripts\python.exe src/app.py --once "/import .codex/import-smoke-dir"
.\.venv\Scripts\python.exe src/app.py --once "/list"
.\.venv\Scripts\python.exe src/app.py --once "你好"
.\.venv\Scripts\python.exe src/app.py --once "/ask Jarvis Lite 使用什么 Python 版本？"
.\.venv\Scripts\python.exe src/app.py --once "Jarvis Lite 当前可以读取什么？"
@'
import os
import tempfile
from pathlib import Path
from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths

with tempfile.TemporaryDirectory() as temp_dir:
    os.environ["JARVIS_LITE_VOICE_ENGINE"] = "transcript"
    paths = build_project_paths(Path(temp_dir))
    (paths.memory_dir / "profile.md").write_text("# 长期记忆\n\n- 用户偏好：中文回答\n", encoding="utf-8")
    (paths.data_dir / "runtime.md").write_text("Jarvis Lite 推荐使用 Python 3.13 系列运行。", encoding="utf-8")
    agent = JarvisAgent(paths)
    print(agent.handle("/voice-status"))
    print(agent.handle("/speak 你好 Jarvis"))
    print(agent.handle("/voice Jarvis Lite 推荐使用什么 Python 版本？"))
'@ | .\.venv\Scripts\python.exe -X utf8 -
@'
import tempfile
from pathlib import Path
from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths

with tempfile.TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)
    paths = build_project_paths(root)
    project_dir = root / "project"
    project_dir.mkdir()
    (project_dir / "notes.md").write_text("笔记", encoding="utf-8")
    (project_dir / "todo.txt").write_text("待办", encoding="utf-8")
    (project_dir / "README").write_text("无后缀", encoding="utf-8")
    (project_dir / "nested").mkdir()
    agent = JarvisAgent(paths)
    print(agent.handle("/automation-status"))
    print(agent.handle(f"/dir-add 项目 {project_dir}"))
    print(agent.handle("/dirs"))
    print(agent.handle("/daily-report today.md"))
    print(agent.handle("/organize-preview 项目"))
    print(agent.handle("/dir-open 项目"))
'@ | .\.venv\Scripts\python.exe -X utf8 -
@'
import tempfile
from pathlib import Path
from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths

with tempfile.TemporaryDirectory() as temp_dir:
    paths = build_project_paths(Path(temp_dir))
    (paths.data_dir / "note.txt").write_text("Jarvis Lite 支持本地知识库标签。", encoding="utf-8")
    agent = JarvisAgent(paths)
    print(agent.handle("/tag note.txt 项目 Python"))
    print(agent.handle("/kb"))
    print(agent.handle("/ask Python"))
'@ | .\.venv\Scripts\python.exe -X utf8 -
@'
import json
import tempfile
from pathlib import Path
from jarvis_lite.agent import JarvisAgent
from jarvis_lite.config import build_project_paths

def simple_pdf_bytes(text: str) -> bytes:
    stream = f"BT\n/F1 18 Tf\n72 720 Td\n({text}) Tj\nET\n".encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"endstream",
    ]
    pdf = b"%PDF-1.4\n"
    offsets = []
    for index, item in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += f"{index} 0 obj\n".encode("ascii") + item + b"\nendobj\n"
    xref_offset = len(pdf)
    pdf += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    pdf += b"0000000000 65535 f \n"
    for offset in offsets:
        pdf += f"{offset:010d} 00000 n \n".encode("ascii")
    pdf += b"trailer\n" + f"<< /Root 1 0 R /Size {len(objects) + 1} >>\n".encode("ascii") + b"startxref\n" + str(xref_offset).encode("ascii") + b"\n%%EOF\n"
    return pdf

with tempfile.TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)
    paths = build_project_paths(root)
    (paths.memory_dir / "profile.md").write_text("# 长期记忆\n\n- 用户偏好：中文回答\n", encoding="utf-8")
    chat = root / "chat.json"
    chat.write_text(json.dumps([{"role": "assistant", "content": "Jarvis Lite 可以导入聊天记录。"}], ensure_ascii=False), encoding="utf-8")
    pdf = root / "manual.pdf"
    pdf.write_bytes(simple_pdf_bytes("Jarvis Lite PDF import smoke"))
    agent = JarvisAgent(paths)
    print(agent.handle(f"/import {chat}"))
    print(agent.handle(f"/import {pdf}"))
    print(agent.handle("/ask 聊天记录"))
    print(agent.handle("/ask PDF import smoke"))
'@ | .\.venv\Scripts\python.exe -X utf8 -
@'
hello
/history
/save-summary cli-smoke
/exit
'@ | .\.venv\Scripts\python.exe -X utf8 src/app.py
@'
我叫测试用户
我是Jarvis Lite测试者
你知道我是谁吗
/exit
'@ | .\.venv\Scripts\python.exe -X utf8 src/app.py
```

## 验证结论

- 单元测试：166 个测试通过。
- 桌面桥接层：`tests.test_desktop_bridge` 4 个测试通过，覆盖会话调用、错误状态、完整快捷命令、无参数快捷命令筛选和更新检查/下载快捷入口。
- 桌面入口：`tests.test_desktop_app` 6 个测试通过，覆盖桌面标题、应用身份和图标、脚本入口、PySide6 依赖声明、设置同步、开机启动同步去重和 smoke 创建桌面小助手窗口。
- 桌面素材：`tests.test_desktop_assets` 3 个测试通过，覆盖 5 个桌面状态 SVG 素材和应用图标均在项目内。
- 桌面开机启动：`tests.test_desktop_autostart` 7 个测试通过，覆盖 Startup 目录、源码模式快捷方式、打包模式快捷方式、PowerShell 脚本、启用、关闭和同步。
- 桌面主题样式：`tests.test_desktop_style` 3 个测试通过，覆盖深色/浅色主题预设、无效主题回退和面板/小助手主题颜色。
- 桌面设置：`tests.test_desktop_settings` 9 个测试通过，覆盖运行态设置目录、窗口位置保存读取、偏好保存读取、开机启动偏好、主题偏好、面板尺寸保存读取、保存位置时保留偏好和损坏设置回退默认值。
- 桌面托盘：`tests.test_desktop_tray` 8 个测试通过，覆盖托盘菜单、关闭到托盘、显示助手、隐藏助手、常用命令入口、最近结果入口和退出应用。
- 桌面窗口：`tests.test_desktop_widgets` 18 个测试通过，覆盖小助手置顶无边框、点击展开/收起面板、面板调用会话核心、面板快捷命令按钮、最近提交结果、面板尺寸恢复与保存、小助手状态同步、状态图片切换、窗口位置保存、状态动效、启动恢复设置、应用设置、主题切换和面板设置回调。
- 桌面打包准备：`tests.test_desktop_packaging` 7 个测试通过，覆盖 PyInstaller 参数、项目外输出目录、打包可选依赖、Windows 图标和版本资源。
- Windows 安装器：`tests.test_windows_installer` 7 个测试通过，覆盖安装脚本、覆盖安装前关闭进程、卸载脚本、Startup 清理、用户数据保留约定、项目版本号和 IExpress SED 文件。
- Windows 打包产物：`scripts\build_windows_installer.py` 已重新生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe` 和 `E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe`。
- Windows exe 元数据：PyInstaller 构建日志显示已复制图标和版本信息；`JarvisLite.exe` 的 `FileDescription` 为 `Jarvis Lite desktop assistant`，`ProductName` 为 `Jarvis Lite`，版本为 `0.1.0`。
- 打包 exe smoke：`JarvisLite.exe --smoke` 退出码为 0。
- 桌面 smoke：`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 可创建桌面小助手窗口并输出 `desktopPetWindow`。
- 命令行入口：可启动并执行一次性输入。
- 记忆读取：`/memory` 可读取 `memory/profile.md`。
- 阶段状态：`/status` 可输出阶段 1 能力闭环和关键文件位置。
- 知识库状态：`/kb` 可输出 `data/` 中可检索资料数量、行数和资料列表。
- 资料导入：`/import 源文件或目录路径 [目标文件名]` 可把 Markdown、txt、PDF、JSON 聊天记录或目录批量导入 `data/`，导入后可被 `/kb` 和 `/ask` 使用。
- PDF 导入：使用 `pypdf` 抽取 PDF 文本并生成同名 Markdown 资料，当前不是大模型摘要。
- 聊天记录导入：JSON 列表或 `messages` 对象可以转换为 Markdown 对话记录。
- 资料标签：`/tag 文件名 标签...` 可给 `data/` 中的 Markdown 或 txt 资料设置标签，标签写入 `data/.knowledge-tags.json`。
- 标签展示与检索：`/kb` 会展示标签列表和资料标签，`/ask` 可以通过标签命中对应资料。
- 语音状态：`/voice-status` 可输出当前语音引擎、播报记录路径和麦克风识别状态。
- 语音播报：`/speak 文本` 可通过语音引擎播报；自动化验证使用 transcript 引擎写入 `logs/voice-output.txt`。
- 语音入口：`/voice 已识别的语音文本` 可复用现有 Agent 回答流程，并播报回答。
- 工作台自动化状态：`/automation-status` 可输出阶段 4 当前能力。
- 更新检查：`/update-status [清单路径或URL]` 可读取本地或远程 JSON 清单，显示当前版本、新版本、下载地址和更新说明；未配置更新源时会提示 `JARVIS_LITE_UPDATE_MANIFEST_URL`。
- 更新下载：`/update-download [清单路径或URL]` 可把新版本安装包下载或复制到项目外 `../jarvis-lite-runtime/updates/`，当前不自动运行安装器。
- 常用目录：`/dir-add 别名 目录路径` 可登记常用目录，`/dirs` 可查看登记结果。
- 日报生成：`/daily-report [文件名]` 可在 `word/` 生成 Markdown 日报。
- 文件整理预览：`/organize-preview 常用目录别名` 可按扩展名输出整理计划，不移动或删除文件。
- 目录打开记录：`/dir-open 常用目录别名` 可把打开目录请求写入 `logs/desktop-actions.txt`，当前不启动外部应用。
- 工具日志：`/list` 会写入 `logs/jarvis.log`。
- Python 版本：项目虚拟环境使用 Python 3.13.2。
- 资料问答：`/ask` 和普通问题可以基于 `data/` 文本返回最多 3 条带命中数量摘要、编号和来源的回答，并过滤弱相关片段。
- 资料问答排序：包含数字或版本号的查询词具备更高权重，能优先返回更具体的资料片段。
- 会话功能：交互式 CLI 可以查看 `/history`，并用 `/save-summary 文件名` 写入 `word/` 会话总结。
- 长期记忆写入：`/remember`、`我叫...`、`我是...` 可以写入 `memory/profile.md`，并支持回答“我是谁”。
- 长期记忆更新：同 key 记忆会替换旧值，例如 `用户姓名` 不会重复保留多个版本。

## 2026-05-20 桌面主题预设验证

### RED：主题预设、运行态字段和面板选择缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_style -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
```

结果：

- `tests.test_desktop_style` 失败原因：缺少主题预设 API。
- `tests.test_desktop_settings` 失败原因：`DesktopSettings` 缺少 `theme_name`。
- `tests.test_desktop_widgets` 失败原因：面板设置和小助手偏好不支持主题。
- `tests.test_desktop_app` 失败原因：设置同步不传递主题。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_style -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- 桌面主题样式测试 3 个通过。
- 桌面设置测试 9 个通过。
- 桌面 widget 测试 16 个通过。
- 桌面入口测试 6 个通过。
- 全量测试 151 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-20 桌面面板快捷命令收口验证

### RED：无参数快捷命令筛选和面板入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v
```

结果：

- `tests.test_desktop_bridge` 失败原因：缺少 `direct_quick_commands()`。
- `tests.test_desktop_widgets` 失败原因：`AssistantPanel` 缺少快捷命令文本和按钮入口。
- `tests.test_desktop_tray` 失败原因：托盘无法复用无参数快捷命令集合。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- 桌面桥接层、widget 和托盘专项测试共 30 个通过。
- 全量测试 154 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-20 桌面安装生命周期收口验证

### RED：卸载生命周期和覆盖安装前置处理缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v
```

结果：

- `test_install_script_prepares_for_cover_install_and_complete_uninstall_metadata` 失败原因：安装脚本缺少 `taskkill`、`DisplayIcon` 和 `QuietUninstallString`。
- `test_uninstall_script_removes_startup_shortcut_and_stops_running_app` 失败原因：卸载脚本缺少 Startup 清理和运行进程关闭。
- `test_uninstall_script_preserves_user_data_directory` 失败原因：卸载脚本缺少用户数据保留约定。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- Windows 安装器专项测试 7 个通过。
- 全量测试 157 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-20 桌面更新检查第一版验证

### RED：更新模块、命令和桌面入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v
```

结果：

- `tests.test_update` 失败原因：`jarvis_lite.update` 模块不存在。
- `tests.test_agent` 失败原因：`/update-status` 返回未知命令。
- `tests.test_desktop_bridge` 失败原因：快捷命令缺少 `/update-status`。
- `tests.test_desktop_widgets` 失败原因：面板快捷按钮缺少“检查更新”。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- 更新模块、Agent、桌面桥接、widget 和托盘专项测试共 64 个通过。
- 全量测试 162 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-21 桌面更新下载体验验证

### RED：更新下载函数、命令和桌面入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets -v
```

结果：

- `tests.test_update` 先因缺少 `describe_update_download` 和 `download_update` 导致导入失败。
- `tests.test_agent` 先因 `/update-download` 返回未知命令失败。
- `tests.test_desktop_bridge` 先因快捷命令缺少 `/update-download` 失败。
- `tests.test_desktop_widgets` 先因面板快捷按钮缺少“下载更新”失败。

### 验证命令

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets -v
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
Start-Process -FilePath "..\jarvis-lite-dist\desktop-exe\JarvisLite.exe" -ArgumentList "--smoke" -Wait -PassThru -NoNewWindow
```

结果：

- 更新模块、Agent、桌面桥接和 widget 专项测试共 60 个通过。
- 全量测试 166 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

### 本地测试交付

- 已推送远程 `main`：`0b7237d feat: 增加更新下载入口`。
- 已重新生成安装包：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 安装包大小：`47,468,544` 字节。
- 安装包生成时间：`2026-05-21 10:36:38`。
- 当前安装包未做代码签名，Windows 安装时可能出现未签名提示。

## 未覆盖事项

- 未接入大模型 API。
- 摄像头、麦克风等硬件入口按用户要求暂缓。
- 未做代码签名和专业安装器替换。

## 2026-05-21 自然语言本地大脑第一版验证

### RED：自然语言常用意图缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v
```

结果：

- `tests.test_memory` 先因 `我是你的什么人，你知道吗` 未识别为身份问题失败。
- `tests.test_agent` 先因自然语言能力询问、生成日报、查看知识库、检查更新和打开 D 盘都落入通用兜底失败。
- `/status` 旧断言显示文案仍停留在“阶段 1 状态”，已同步更新为当前完整状态。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v
```

结果：

- 记忆和 Agent 专项测试共 46 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 173 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 安装器重新生成成功：`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 安装包大小：`47,472,640` 字节。
- 安装包生成时间：`2026-05-21 11:17:54`。
- 打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。

## 2026-05-21 常用目录别名自然语言验证

### RED：打开和整理常用目录别名缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- `打开项目目录` 先未记录打开目录请求。
- `整理项目目录` 先落入通用兜底，未返回文件整理预览。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 39 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 175 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 已知桌面目录自然语言验证

### RED：整理桌面和打开桌面缺少系统目录 fallback

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_desktop_uses_known_desktop_directory tests.test_agent.AgentTests.test_natural_language_open_desktop_uses_known_desktop_directory -v
```

结果：

- `整理桌面` 先返回 `没有找到常用目录：桌面`。
- `打开桌面` 先没有写入 `logs/desktop-actions.txt`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_desktop_uses_known_desktop_directory tests.test_agent.AgentTests.test_natural_language_open_desktop_uses_known_desktop_directory -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 已知桌面目录新增 2 个测试通过。
- Agent 专项测试 41 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 177 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 资料标签自然语言验证

### RED：自然语言标签表达未映射到 /tag

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_mark_document_as_tags_updates_document_tags -v
```

结果：

- `给 note.txt 打标签 项目 Python` 先落入普通兜底，没有更新标签。
- `把 note.txt 标记为 私人资料` 先被当作资料问答，没有更新标签。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_mark_document_as_tags_updates_document_tags -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 自然语言资料标签新增 2 个测试通过。
- Agent 专项测试 43 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 179 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 自然语言导入资料验证

### RED：自然语言导入表达未映射到 /import

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_import_file_adds_document_to_knowledge_base tests.test_agent.AgentTests.test_natural_language_import_quoted_file_path_adds_document_to_knowledge_base -v
```

结果：

- `导入 <路径> 到知识库` 先落入普通兜底，没有导入资料。
- `把 "<带空格路径>" 导入知识库` 先落入普通兜底，没有导入资料。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_import_file_adds_document_to_knowledge_base tests.test_agent.AgentTests.test_natural_language_import_quoted_file_path_adds_document_to_knowledge_base -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 自然语言导入资料新增 2 个测试通过。
- Agent 专项测试 45 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 181 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近资料上下文验证

### RED：这个资料无法指向最近导入资料

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_imported_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_tag_recent_document_requires_recent_document_context -v
```

结果：

- 导入单个资料后，`给这个资料打标签 项目 Python` 先把 `这个资料` 当成真实文件名，标签更新失败。
- 未导入资料时，`给这个资料打标签 项目` 先把 `这个资料` 当成真实文件名，未给出最近资料缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_imported_document_updates_document_tags tests.test_agent.AgentTests.test_natural_language_tag_recent_document_requires_recent_document_context -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近资料上下文新增 2 个测试通过。
- Agent 专项测试 47 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 183 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近目录上下文验证

### RED：这个目录无法指向最近目录

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_recent_directory_after_open_common_directory tests.test_agent.AgentTests.test_natural_language_open_recent_directory_requires_recent_directory_context -v
```

结果：

- 打开 `项目` 常用目录后，`整理这个目录` 先把 `这个` 当成常用目录别名，提示没有找到常用目录。
- 未打开或整理目录时，`打开这个目录` 先把 `这个` 当成常用目录别名，未给出最近目录缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_organize_recent_directory_after_open_common_directory tests.test_agent.AgentTests.test_natural_language_open_recent_directory_requires_recent_directory_context -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近目录上下文新增 2 个测试通过。
- Agent 专项测试 49 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 185 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近搜索结果上下文验证

### RED：这个结果无法指向最近搜索命中

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_plain_question -v
```

结果：

- `/ask Python 3.13` 命中 `data/runtime.md` 后，`给这个结果打标签 运行环境` 先把 `这个结果` 当成真实文件名，标签更新失败。
- 普通问题命中 `data/runtime.md` 后，`给这个结果打标签 运行环境` 同样先把 `这个结果` 当成真实文件名，标签更新失败。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_recent_search_result_after_plain_question -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近搜索结果上下文新增 2 个测试通过。
- Knowledge 专项测试 23 个通过。
- Agent 专项测试 51 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 187 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近搜索结果编号选择验证

### RED：无法选择第二条搜索结果

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_requires_recent_results -v
```

结果：

- `/ask Jarvis Lite 使用什么？` 返回两条资料后，`给第二条结果打标签 运行环境` 先把 `第二条结果` 当成真实文件名，标签更新失败。
- 未提问时，`给第二条结果打标签 运行环境` 同样先把 `第二条结果` 当成真实文件名，未给出最近搜索结果缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_requires_recent_results -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v
```

结果：

- 最近搜索结果编号选择新增 2 个测试通过。
- Agent 专项测试 53 个通过。
- Knowledge 专项测试 23 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 189 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 查看编号搜索结果验证

### RED：无法查看第二条搜索结果

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_requires_recent_results -v
```

结果：

- `/ask Jarvis Lite 使用什么？` 返回两条资料后，`查看第二条结果` 先落入长期记忆兜底，没有读取第二条资料。
- 未提问时，`查看第二条结果` 先落入长期记忆兜底，未给出最近搜索结果缺失提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_read_numbered_search_result_requires_recent_results tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_after_ask_command tests.test_agent.AgentTests.test_natural_language_tag_numbered_search_result_requires_recent_results -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 查看编号搜索结果新增 2 个测试通过。
- 编号搜索结果相关 4 个测试通过。
- Agent 专项测试 55 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 191 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近搜索结果持久化验证

### RED：新 Agent 实例无法恢复最近搜索结果

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_search_results_survive_new_agent_instance -v
```

结果：

- 第一个 Agent 执行 `/ask Jarvis Lite 使用什么？` 后，新建第二个 Agent 再说 `查看第二条结果`，先提示还没有最近搜索结果。

### 根因与修复

- 根因：最近搜索结果列表只保存在 `JarvisAgent` 实例内。
- 修复：新增 `runtime_context.py`，把最近搜索结果路径列表写入项目外 `jarvis-lite-runtime/agent-context.json`，并在 Agent 初始化时恢复。
- 测试隔离：Agent 测试根目录改为临时目录下的 `jarvis-lite` 子目录，避免运行态文件写到系统临时目录的公共父级而串扰测试。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_search_results_survive_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近搜索结果持久化新增 1 个测试通过。
- Agent 专项测试 56 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 192 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近上下文状态查询验证

### RED：自然语言最近上下文查询缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_empty_state tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_current_context tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_search_results -v
```

结果：

- `查看最近上下文` 先落入长期记忆兜底，没有输出最近上下文空状态。
- `你还记得刚才什么` 先落入长期记忆兜底，没有展示最近资料、最近目录和最近搜索结果。
- `最近上下文状态` 在新 Agent 实例中也先落入长期记忆兜底，没有展示已恢复的搜索结果。

### 根因与修复

- 根因：自然语言意图层没有最近上下文状态意图，Agent 也没有统一格式化当前上下文的入口。
- 修复：新增 `recent_context_status` 意图，支持“查看最近上下文”“最近上下文状态”“你还记得刚才什么”等表达。
- 修复：Agent 新增最近上下文状态输出，展示最近资料、最近目录和最近搜索结果列表；空状态会提示下一步可先提问、导入资料或打开/整理目录。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_empty_state tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_current_context tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_search_results -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近上下文状态新增 3 个测试通过。
- Agent 专项测试 59 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 195 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 最近资料和最近目录持久化验证

### RED：新 Agent 实例无法恢复最近资料和最近目录

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_imported_document_survives_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_directory_survives_new_agent_instance -v
```

结果：

- 导入单个资料后新建 Agent，再说“给这个资料打标签 项目”先提示还没有最近资料。
- 打开常用目录后新建 Agent，再说“打开这个目录”先提示还没有最近目录。

### 根因与修复

- 根因：`RuntimeContext` 只保存最近搜索结果列表，最近资料和最近目录只保存在 `JarvisAgent` 实例内。
- 修复：`RuntimeContext` 新增 `recent_document_path` 和 `recent_directory`。
- 修复：`JarvisAgent` 初始化时恢复最近资料和最近目录；资料、目录、搜索结果变化时统一保存完整运行态上下文。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_imported_document_survives_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_directory_survives_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近资料持久化新增 1 个测试通过。
- 最近目录持久化新增 1 个测试通过。
- Agent 专项测试 61 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 197 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 经验记忆第一版验证

### RED：缺少独立经验记忆入口

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experiences_command_reports_empty_state tests.test_agent.AgentTests.test_experience_command_records_experience tests.test_agent.AgentTests.test_natural_language_record_experience_records_experience tests.test_agent.AgentTests.test_natural_language_experience_memory_status_maps_to_experiences -v
```

结果：

- `tests.test_memory` 先因缺少 `append_experience` 和 `read_experiences` 导入失败。
- `/experience` 和 `/experiences` 先返回未知命令。
- “记住这个经验：...” 先被 `parse_identity_fact()` 当成普通长期记忆写入。
- “查看经验记忆” 先落入长期记忆兜底。

### 根因与修复

- 根因：长期记忆只有 `memory/profile.md`，没有独立经验记忆文件和 Agent 入口。
- 修复：新增 `memory/experiences.md` 读写函数，重复经验不重复写入。
- 修复：新增 `/experience`、`/experiences` 和自然语言“记录经验：...”“记住这个经验：...”“查看经验记忆”。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Memory 专项测试 11 个通过。
- Agent 专项测试 65 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 203 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 经验引用第一版验证

### RED：能力摘要和日报未引用经验

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory.MemoryTests.test_list_recent_experiences_returns_latest_items_first -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_capability_question_reports_recent_experiences -v
.\.venv\Scripts\python.exe -m unittest tests.test_automation.AutomationTests.test_write_daily_report_creates_word_markdown -v
```

结果：

- `tests.test_memory` 先因缺少 `list_recent_experiences` 导入失败。
- 能力摘要先没有“最近经验”内容。
- 日报先没有“经验记忆”段。

### 根因与修复

- 根因：经验记忆只有写入和全文查看入口，没有结构化最近经验 API。
- 修复：新增 `list_recent_experiences(paths, limit=3)`，最新经验排在前面。
- 修复：能力摘要和日报复用最近经验列表。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent tests.test_automation -v
```

结果：

- Memory、Agent、Automation 专项测试共 83 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 205 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 经验搜索第一版验证

### RED：经验关键词检索入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory.MemoryTests.test_search_experiences_returns_matching_items_latest_first -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experience_search_command_returns_matching_experiences tests.test_agent.AgentTests.test_experience_search_command_reports_no_match tests.test_agent.AgentTests.test_experience_search_command_requires_keyword tests.test_agent.AgentTests.test_natural_language_search_experience_maps_to_experience_search -v
```

结果：

- `tests.test_memory` 先因缺少 `search_experiences` 导入失败。
- `/experience-search` 先返回未知命令。
- “搜索经验 导入”先未映射到经验搜索命令。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v
```

结果：

- Memory 和 Agent 专项测试共 83 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 210 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-21 经验操作建议第一版验证

### RED：经验建议入口缺失

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experience_advice_command_returns_related_experiences tests.test_agent.AgentTests.test_experience_advice_command_reports_no_related_experience tests.test_agent.AgentTests.test_experience_advice_command_requires_keyword tests.test_agent.AgentTests.test_natural_language_experience_advice_uses_related_experiences -v
```

结果：

- `/experience-advice` 相关 3 个测试先返回未知命令。
- “我该怎么导入资料”先落入资料问答，没有引用经验建议。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 74 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 214 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 经验建议命令联动第一版验证

### RED：经验建议缺少可执行命令

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experience_advice_command_suggests_import_commands tests.test_agent.AgentTests.test_experience_advice_command_suggests_known_commands_without_experience tests.test_agent.AgentTests.test_natural_language_experience_advice_includes_command_suggestions -v
```

结果：

- `/experience-advice 导入资料` 先只有相关经验，没有“可执行命令”。
- `/experience-advice 生成日报` 先只提示缺少经验，没有 `/daily-report [文件名]`。
- “导入资料有什么建议”先没有输出 `/import 源文件或目录路径 [目标文件名]`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 77 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 217 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 经验建议引用最近上下文第一版验证

### RED：经验建议无法引用最近资料和目录

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_experience_advice_for_recent_document_uses_recent_document_context tests.test_agent.AgentTests.test_experience_advice_for_recent_document_requires_recent_context tests.test_agent.AgentTests.test_experience_advice_for_recent_directory_uses_recent_directory_context -v
```

结果：

- `/experience-advice 这个资料` 先只按字面输出通用资料命令，没有当前资料和具体 `/read`、`/tag`。
- 缺少最近资料时先没有“还没有最近资料”的明确提示。
- `/experience-advice 这个目录` 先只输出通用目录命令，没有当前目录和具体 `/organize-preview 项目`、`/dir-open 项目`。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 80 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 220 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近建议编号查看第一版验证

### RED：无法查看编号建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_read_first_advice_after_experience_advice tests.test_agent.AgentTests.test_natural_language_read_numbered_advice_after_experience_advice tests.test_agent.AgentTests.test_natural_language_read_advice_requires_recent_advice -v
```

结果：

- “查看第一条建议”先落入普通兜底，没有读取最近建议。
- “查看第二条建议”同样落入普通兜底。
- 没有最近建议时没有明确提示。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- Agent 专项测试 83 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 223 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近建议持久化第一版验证

### RED：新 Agent 无法恢复最近建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_advice_suggestions_survive_new_agent_instance -v
```

结果：

- 新增测试先失败，新建 `JarvisAgent` 后返回“还没有最近建议”，无法读取上一轮 `/experience-advice` 的建议。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_recent_advice_suggestions_survive_new_agent_instance -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近建议持久化单测通过。
- Agent 专项测试 84 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 224 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近建议执行前确认第一版验证

### RED：无法准备或确认执行建议

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice tests.test_agent.AgentTests.test_natural_language_prepare_advice_requires_completed_parameters tests.test_agent.AgentTests.test_natural_language_confirm_advice_requires_pending_command -v
```

结果：

- “执行第二条建议”先落入长期记忆兜底，没有准备待确认命令。
- “执行第一条建议”先落入长期记忆兜底，没有提示补充参数。
- “确认执行”先落入长期记忆兜底，没有提示缺少待确认命令。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_prepare_and_confirm_executable_advice tests.test_agent.AgentTests.test_natural_language_prepare_advice_requires_completed_parameters tests.test_agent.AgentTests.test_natural_language_confirm_advice_requires_pending_command -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近建议执行前确认 3 个新增测试通过。
- Agent 专项测试 87 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 227 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。

## 2026-05-22 最近建议状态展示第一版验证

### RED：最近上下文不展示最近建议状态

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_advice tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_advice_command tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_advice -v
```

结果：

- 生成建议后，“查看最近上下文”仍返回“还没有记录”，没有展示最近建议。
- 准备执行建议后，“查看最近上下文”没有展示待确认建议命令。
- 新建 Agent 恢复最近建议后，“最近上下文状态”仍没有展示最近建议。

### 专项 GREEN

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_recent_advice tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_pending_advice_command tests.test_agent.AgentTests.test_natural_language_recent_context_status_reports_restored_advice -v
.\.venv\Scripts\python.exe -m unittest tests.test_agent -v
```

结果：

- 最近建议状态展示 3 个新增测试通过。
- Agent 专项测试 90 个通过。

### 收尾验证

命令：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke
git diff --check
```

结果：

- 全量测试 230 个通过。
- 源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check` 退出码为 0，仅出现 CRLF 换行提示。
