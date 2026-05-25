# Jarvis Lite

> 日期：2026-05-23
> 执行者：Codex
> 说明：本项目是个人 AI 助手实验项目。

Jarvis Lite 是一个本地优先的个人智能助手起点。当前重点是先把命令行助手跑通，再逐步扩展长期记忆、个人知识库、语音入口和桌面自动化。

完整方案和路线图见：[word/jarvis-lite-overall-plan.md](word/jarvis-lite-overall-plan.md)。

## 当前状态

当前已具备：

- 读取 `memory/profile.md` 长期记忆。
- 通过 `/remember`、`我叫...`、`我是...` 写入长期记忆，并能回答“我是谁”。
- 通过 `/experience`、`/experiences`、`/experience-search`、`/experience-advice` 或“记录经验：...”维护、检索并引用 `memory/experiences.md` 经验记忆，用于沉淀可复用流程；经验建议会引用相关经验、最近资料/目录上下文，并带出下一步可执行命令，后续可说“查看第一条建议”“执行第一条建议”拿到参数草稿，补全草稿后可进入确认执行，或“执行第二条建议”准备确认执行，重启后也能恢复最近建议，能力摘要和日报会引用最近经验。
- 具备第一版本地自然语言意图层，可用“你现在能做什么事”“查看知识库”“生成日报”“检查更新”“打开D盘”“打开下载目录”等表达触发常见能力。
- 支持最近上下文：问答、读取资料、导入资料、查看最近文件、打开或整理目录、生成经验建议后，可继续说“查看最近上下文”“给这个资料打标签 项目”“读取这个资料”“读取第二份资料”“给第二份资料打标签 项目”“查看第一份最近文件”“导入第一份最近文件到知识库”“打开这个目录”“查看第一条建议”；“读取 note.md”“查看 note.txt”会复用 `/read` 并更新最近资料列表；最近上下文状态会列出最近资料列表、最近文件列表、最近建议、待确认建议命令和下一步建议；最近资料列表、最近文件列表、最近目录、最近搜索结果和最近建议会保存到项目外 `../jarvis-lite-runtime/agent-context.json`，日报和最近上下文状态会引用这些上下文并生成“下一步建议”，其中最近文件建议会提示查看详情、导入知识库和刷新列表；同一交互或桌面会话内，执行建议采用“执行第 N 条建议”后再“确认执行”的两步确认，含参数草稿的建议也需要在同一会话内补全后确认。
- 读取 `data/` 目录中的 `.txt` 和 `.md` 文本资料，并通过 `/ask` 或普通问题返回最多 3 条带来源、命中摘要、命中原因和可继续操作的基础回答。
- 通过 `/kb` 查看个人知识库状态，包括资料文件数量、可检索行数和资料列表。
- 通过 `/import` 把外部 Markdown、txt、PDF、JSON 聊天记录或资料目录导入 `data/` 个人知识库。
- 通过 `/tag` 给知识库资料设置简单标签，标签会出现在 `/kb` 中，并参与 `/ask` 检索。
- 通过 `/voice-status`、`/speak` 和 `/voice` 使用阶段 3 第一批语音入口能力。
- 通过 `/automation-status`、`/recent-files`、`/dir-add`、`/dirs`、`/daily-report`、`/organize-preview` 和 `/dir-open` 使用阶段 4 第一批工作台自动化能力；未登记常用目录时，也能用“查看最近文件”“查看第一份最近文件”“导入第一份最近文件到知识库”“打开桌面/下载目录/项目目录”“整理桌面/下载目录/项目目录”识别系统常见目录。
- 桌面虚拟助手应用已完成第一版：包含常驻小助手窗口、可展开助手面板、设置区域、系统托盘、状态图片、状态动效、文本输入和快捷命令。
- 桌面应用已具备项目内应用图标，应用窗口、助手面板和系统托盘使用一致的应用身份。
- Windows 桌面 exe 打包已包含 `.ico` 图标和版本资源；安装器卸载信息使用项目版本号。
- Windows 安装器已收口基础生命周期：覆盖安装前关闭运行中的 exe，卸载时清理桌面、开始菜单、Startup 开机启动项和卸载注册表，并默认保留用户数据。
- 支持清单式更新检查：通过 `/update-status [清单路径或URL]` 或桌面“检查更新”快捷命令查看当前版本、新版本、下载地址和更新说明。
- 支持手动下载更新安装包：通过 `/update-download [清单路径或URL]` 或桌面“下载更新”快捷命令，把新版本安装包保存到项目外 `../jarvis-lite-runtime/updates/`。
- 通过 `jarvis-lite-desktop` 启动 PySide6 桌面助手入口；窗口位置会保存到项目外的 `../jarvis-lite-runtime/desktop-settings.json`。
- 桌面设置支持置顶开关、透明度和小助手尺寸，设置同样保存到项目外运行态文件。
- 桌面设置支持当前用户级“开机启动”，会在 Windows Startup 目录创建或删除 `Jarvis Lite.lnk`。
- 桌面设置支持深色和浅色主题预设，面板与小助手会同步切换并保存到项目外运行态文件。
- 助手面板宽高会随用户调整保存到项目外运行态文件，下次启动会自动恢复。
- 桌面入口支持关闭到托盘，托盘菜单可显示助手、隐藏助手、触发常用命令或退出应用。
- 助手面板和托盘快捷命令只展示可直接执行的无参数命令，已包含最近上下文和最近文件入口，避免一键触发需要额外参数的命令。
- 托盘快捷命令执行后会更新“最近结果”入口，可重新打开面板查看最近一次托盘命令结果，且不会重复执行命令。
- 在交互式命令行中记录当前会话历史，并可把本轮会话总结写入 `word/`。
- 将工具调用记录到 `logs/jarvis.log`。
- 通过 `/status` 查看第一阶段能力闭环和关键文件位置。
- 使用 Python 3.13 系列和标准库 `unittest` 执行本地测试。

## 快速启动

推荐使用 Python 3.13 系列创建本地虚拟环境：

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\activate
python --version
python -m pip install -e .
```

启动交互式命令行助手：

```powershell
python src/app.py
```

一次性执行命令：

```powershell
python src/app.py --once "/memory"
python src/app.py --once "/experiences"
python src/app.py --once "/status"
python src/app.py --once "/kb"
python src/app.py --once "/import E:\path\to\note.md"
python src/app.py --once "/import E:\path\to\manual.pdf"
python src/app.py --once "/import E:\path\to\chat.json"
python src/app.py --once "/import E:\path\to\knowledge-folder"
python src/app.py --once "/tag jarvis-lite.md 项目 Python"
python src/app.py --once "/voice-status"
python src/app.py --once "/speak 你好，我是 Jarvis Lite"
python src/app.py --once "/voice Jarvis Lite 使用什么 Python 版本？"
python src/app.py --once "/automation-status"
python src/app.py --once "/recent-files"
python src/app.py --once "/update-status E:\path\to\update.json"
python src/app.py --once "/update-download E:\path\to\update.json"
python src/app.py --once "你现在能做什么事"
python src/app.py --once "查看知识库"
python src/app.py --once "生成日报"
python src/app.py --once "打开D盘"
python src/app.py --once "打开下载目录"
python src/app.py --once "整理下载目录"
python src/app.py --once "打开项目目录"
python src/app.py --once "整理项目目录"
python src/app.py --once "查看最近上下文"
python src/app.py --once "查看最近文件"
python src/app.py --once "查看第一份最近文件"
python src/app.py --once "导入第一份最近文件到知识库"
python src/app.py --once "记录经验：导入资料后先打标签"
python src/app.py --once "查看经验记忆"
python src/app.py --once "搜索经验 导入"
python src/app.py --once "我该怎么导入资料"
python src/app.py --once "查看第一条建议"
python src/app.py --once "执行第一条建议"
python src/app.py --once "读取 note.md"
python src/app.py --once "读取这个资料"
python src/app.py --once "读取第二份资料"
python src/app.py --once "给这个资料打标签 项目"
python src/app.py --once "给第二份资料打标签 项目"
python src/app.py --once "打开这个目录"
python src/app.py --once "/dir-add 项目 E:\path\to\project"
python src/app.py --once "/dirs"
python src/app.py --once "/daily-report today.md"
python src/app.py --once "/organize-preview 项目"
python src/app.py --once "/dir-open 项目"
python src/app.py --once "/list"
python src/app.py --once "/ask Jarvis Lite 使用什么 Python 版本？"
python src/app.py --once "我叫张三"
python src/app.py --once "你知道我是谁吗"
jarvis-lite-desktop --smoke
```

启动桌面虚拟助手：

```powershell
jarvis-lite-desktop
```

桌面助手运行后，关闭小助手窗口只会隐藏到托盘；需要结束进程时使用托盘菜单里的“退出”。
托盘菜单里的常用命令会自动显示助手面板，并把结果写入面板对话区；执行后可通过“最近结果”重新打开最近一次结果。

准备桌面 exe 打包环境：

```powershell
python -m pip install -e ".[desktop-build]"
python scripts/build_desktop_exe.py
python scripts/build_windows_installer.py
```

桌面 exe 打包输出默认位于项目外的 `../jarvis-lite-dist/desktop-exe/`；Windows 安装器输出到 `../jarvis-lite-dist/JarvisLiteSetup.exe`。
Windows exe 构建会使用项目内 `packaging/windows/JarvisLite.ico`，并在项目外构建目录生成 PyInstaller 版本资源文件。

运行本地测试：

```powershell
python -m unittest discover -s tests -v
```

语音入口默认使用自动模式。自动化验证或无扬声器环境可使用 transcript 模式：

```powershell
$env:JARVIS_LITE_VOICE_ENGINE = "transcript"
python src/app.py --once "/speak 你好，我是 Jarvis Lite"
```

## 常用命令

```text
/help
/memory
/status
/kb
/voice-status
/speak 文本
/voice 已识别的语音文本
/automation-status
/update-status [清单路径或URL]
/update-download [清单路径或URL]
/dir-add 别名 目录路径
/dirs
/daily-report [文件名]
/organize-preview 常用目录别名
/dir-open 常用目录别名
/import 源文件或目录路径 [目标文件名]
/tag 文件名 标签...
/remember 记忆内容
/experience 经验内容
/experiences
/experience-search 关键词
/experience-advice 关键词
/list [目录]
/read 文件名
/ask 问题
/note 标题 内容
/summary 文件名 内容
/history
/save-summary 文件名
/clear
/exit
```

## 文档入口

- [DOCUMENTATION.md](DOCUMENTATION.md)：项目文档整理约定。
- [word/文档索引.md](word/文档索引.md)：正式文档索引。
- [word/jarvis-lite-overall-plan.md](word/jarvis-lite-overall-plan.md)：整体方案与路线图。
- [word/2026-05-22-ai-agent-learning-notes.md](word/2026-05-22-ai-agent-learning-notes.md)：AI Agent 学习记录。
- [word/2026-05-22-jarvis-lite-personal-device-agent-plan.md](word/2026-05-22-jarvis-lite-personal-device-agent-plan.md)：Jarvis Lite 个人设备级 Agent 融合方案。
- [word/jarvis-lite-desktop-pet-app-design.md](word/jarvis-lite-desktop-pet-app-design.md)：桌面虚拟助手应用方案。
- [word/2026-05-20-jarvis-lite-desktop-tray-feedback-design.md](word/2026-05-20-jarvis-lite-desktop-tray-feedback-design.md)：桌面托盘最近结果反馈设计。
- [word/2026-05-20-jarvis-lite-desktop-panel-size-design.md](word/2026-05-20-jarvis-lite-desktop-panel-size-design.md)：桌面面板尺寸持久化设计。
- [word/2026-05-20-jarvis-lite-desktop-installation-plan.md](word/2026-05-20-jarvis-lite-desktop-installation-plan.md)：桌面安装包三阶段计划。
- [word/2026-05-20-jarvis-lite-desktop-experience-closeout-design.md](word/2026-05-20-jarvis-lite-desktop-experience-closeout-design.md)：桌面体验收口设计。
- [word/2026-05-20-jarvis-lite-desktop-package-prep-design.md](word/2026-05-20-jarvis-lite-desktop-package-prep-design.md)：桌面打包前准备设计。
- [word/2026-05-20-jarvis-lite-desktop-windows-installer-design.md](word/2026-05-20-jarvis-lite-desktop-windows-installer-design.md)：Windows 桌面安装器设计。
- [word/2026-05-20-jarvis-lite-desktop-windows-metadata-design.md](word/2026-05-20-jarvis-lite-desktop-windows-metadata-design.md)：Windows 安装产物元数据设计。
- [word/2026-05-20-jarvis-lite-desktop-launch-at-login-design.md](word/2026-05-20-jarvis-lite-desktop-launch-at-login-design.md)：桌面开机自启动设计。
- [word/2026-05-20-jarvis-lite-desktop-theme-presets-design.md](word/2026-05-20-jarvis-lite-desktop-theme-presets-design.md)：桌面主题预设设计。
- [word/2026-05-20-jarvis-lite-desktop-panel-quick-commands-design.md](word/2026-05-20-jarvis-lite-desktop-panel-quick-commands-design.md)：桌面面板快捷命令收口设计。
- [word/2026-05-20-jarvis-lite-desktop-install-lifecycle-design.md](word/2026-05-20-jarvis-lite-desktop-install-lifecycle-design.md)：桌面安装生命周期收口设计。
- [word/2026-05-20-jarvis-lite-desktop-update-check-design.md](word/2026-05-20-jarvis-lite-desktop-update-check-design.md)：桌面更新检查第一版设计。
- [word/2026-05-21-jarvis-lite-desktop-update-download-design.md](word/2026-05-21-jarvis-lite-desktop-update-download-design.md)：桌面更新下载体验设计。
- [word/2026-05-21-jarvis-lite-natural-language-brain-design.md](word/2026-05-21-jarvis-lite-natural-language-brain-design.md)：自然语言本地大脑设计。
- [word/2026-05-18-jarvis-lite-progress.md](word/2026-05-18-jarvis-lite-progress.md)：阶段 1 当前进度。
- [word/2026-05-18-jarvis-lite-phase-2-progress.md](word/2026-05-18-jarvis-lite-phase-2-progress.md)：阶段 2 当前进度。
- [word/2026-05-19-jarvis-lite-phase-2-progress.md](word/2026-05-19-jarvis-lite-phase-2-progress.md)：阶段 2 资料导入进度。
- [word/2026-05-19-jarvis-lite-phase-3-progress.md](word/2026-05-19-jarvis-lite-phase-3-progress.md)：阶段 3 语音入口进度。
- [word/2026-05-19-jarvis-lite-phase-4-progress.md](word/2026-05-19-jarvis-lite-phase-4-progress.md)：阶段 4 工作台自动化进度。
- [word/2026-05-19-jarvis-lite-desktop-app-progress.md](word/2026-05-19-jarvis-lite-desktop-app-progress.md)：桌面虚拟助手应用进度。
- [word/2026-05-20-jarvis-lite-desktop-app-progress.md](word/2026-05-20-jarvis-lite-desktop-app-progress.md)：桌面虚拟助手最近结果入口进度。
- [word/2026-05-20-jarvis-lite-desktop-panel-size-progress.md](word/2026-05-20-jarvis-lite-desktop-panel-size-progress.md)：桌面面板尺寸持久化进度。
- [word/2026-05-20-jarvis-lite-desktop-experience-closeout-progress.md](word/2026-05-20-jarvis-lite-desktop-experience-closeout-progress.md)：桌面体验收口进度。
- [word/2026-05-20-jarvis-lite-desktop-package-prep-progress.md](word/2026-05-20-jarvis-lite-desktop-package-prep-progress.md)：桌面打包前准备进度。
- [word/2026-05-20-jarvis-lite-desktop-windows-installer-progress.md](word/2026-05-20-jarvis-lite-desktop-windows-installer-progress.md)：Windows 桌面安装器进度。
- [word/2026-05-20-jarvis-lite-desktop-windows-metadata-progress.md](word/2026-05-20-jarvis-lite-desktop-windows-metadata-progress.md)：Windows 安装产物元数据进度。
- [word/2026-05-20-jarvis-lite-desktop-launch-at-login-progress.md](word/2026-05-20-jarvis-lite-desktop-launch-at-login-progress.md)：桌面开机自启动进度。
- [word/2026-05-20-jarvis-lite-desktop-theme-presets-progress.md](word/2026-05-20-jarvis-lite-desktop-theme-presets-progress.md)：桌面主题预设进度。
- [word/2026-05-20-jarvis-lite-desktop-panel-quick-commands-progress.md](word/2026-05-20-jarvis-lite-desktop-panel-quick-commands-progress.md)：桌面面板快捷命令收口进度。
- [word/2026-05-20-jarvis-lite-desktop-install-lifecycle-progress.md](word/2026-05-20-jarvis-lite-desktop-install-lifecycle-progress.md)：桌面安装生命周期收口进度。
- [word/2026-05-20-jarvis-lite-desktop-update-check-progress.md](word/2026-05-20-jarvis-lite-desktop-update-check-progress.md)：桌面更新检查第一版进度。
- [word/2026-05-21-jarvis-lite-desktop-update-download-progress.md](word/2026-05-21-jarvis-lite-desktop-update-download-progress.md)：桌面更新下载体验进度。
- [word/2026-05-21-jarvis-lite-natural-language-brain-progress.md](word/2026-05-21-jarvis-lite-natural-language-brain-progress.md)：自然语言本地大脑第一版进度。
