# 验证记录

> 日期：2026-05-19
> 执行者：Codex

## 验证命令

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip show pypdf
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
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

- 单元测试：68 个测试通过。
- 命令行入口：可启动并执行一次性输入。
- 记忆读取：`/memory` 可读取 `memory/profile.md`。
- 阶段状态：`/status` 可输出阶段 1 能力闭环和关键文件位置。
- 知识库状态：`/kb` 可输出 `data/` 中可检索资料数量、行数和资料列表。
- 资料导入：`/import 源文件或目录路径 [目标文件名]` 可把 Markdown、txt、PDF、JSON 聊天记录或目录批量导入 `data/`，导入后可被 `/kb` 和 `/ask` 使用。
- PDF 导入：使用 `pypdf` 抽取 PDF 文本并生成同名 Markdown 资料，当前不是大模型摘要。
- 聊天记录导入：JSON 列表或 `messages` 对象可以转换为 Markdown 对话记录。
- 资料标签：`/tag 文件名 标签...` 可给 `data/` 中的 Markdown 或 txt 资料设置标签，标签写入 `data/.knowledge-tags.json`。
- 标签展示与检索：`/kb` 会展示标签列表和资料标签，`/ask` 可以通过标签命中对应资料。
- 工具日志：`/list` 会写入 `logs/jarvis.log`。
- Python 版本：项目虚拟环境使用 Python 3.13.2。
- 资料问答：`/ask` 和普通问题可以基于 `data/` 文本返回最多 3 条带命中数量摘要、编号和来源的回答，并过滤弱相关片段。
- 资料问答排序：包含数字或版本号的查询词具备更高权重，能优先返回更具体的资料片段。
- 会话功能：交互式 CLI 可以查看 `/history`，并用 `/save-summary 文件名` 写入 `word/` 会话总结。
- 长期记忆写入：`/remember`、`我叫...`、`我是...` 可以写入 `memory/profile.md`，并支持回答“我是谁”。
- 长期记忆更新：同 key 记忆会替换旧值，例如 `用户姓名` 不会重复保留多个版本。

## 未覆盖事项

- 未接入大模型 API。
- 未实现语音入口、桌面 UI 或外部系统控制。
