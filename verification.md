# 验证记录

> 日期：2026-05-19
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

- 单元测试：115 个测试通过。
- 桌面桥接层：`tests.test_desktop_bridge` 3 个测试通过，覆盖会话调用、错误状态和快捷命令。
- 桌面入口：`tests.test_desktop_app` 3 个测试通过，覆盖桌面标题、脚本入口、PySide6 依赖声明和 smoke 创建桌面小助手窗口。
- 桌面素材：`tests.test_desktop_assets` 2 个测试通过，覆盖 5 个桌面状态 SVG 素材均在项目内。
- 桌面设置：`tests.test_desktop_settings` 6 个测试通过，覆盖运行态设置目录、窗口位置保存读取、偏好保存读取、保存位置时保留偏好和损坏设置回退默认值。
- 桌面托盘：`tests.test_desktop_tray` 5 个测试通过，覆盖托盘菜单、关闭到托盘、显示助手、隐藏助手、常用命令入口和退出应用。
- 桌面窗口：`tests.test_desktop_widgets` 12 个测试通过，覆盖小助手置顶无边框、点击展开/收起面板、面板调用会话核心、小助手状态同步、状态图片切换、窗口位置保存、状态动效、启动恢复设置、应用设置和面板设置回调。
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

## 未覆盖事项

- 未接入大模型 API。
- 摄像头、麦克风等硬件入口按用户要求暂缓。
- 未制作桌面安装包、系统托盘和开机自启动。
