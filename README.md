# Jarvis Lite

> 日期：2026-06-10
> 执行者：Codex
> 说明：本项目是本地优先的个人 PC Agent 实验项目。

Jarvis Lite 的目标是让 AI 逐步理解并使用个人电脑上的记忆、知识库、文件、目录、最近上下文和桌面工作流。它不是纯聊天机器人，也不是多端平台；当前主线是先把 PC Agent 做稳，再打磨 InnerBrain 本地内脑、LLM 外脑、联网搜索和桌面工作流。

当前版本：`0.146.0`。当前方案入口见 [word/PROJECT-PLAN.md](word/PROJECT-PLAN.md)，正式文档索引见 [word/文档索引.md](word/文档索引.md)。

## 当前路线

```text
PC Agent 稳定
  -> InnerBrain 本地内脑
  -> LLM 外脑
  -> Agent 控制的联网搜索
  -> PC + 内脑 + 外脑核心闭环
  -> Jarvis Lite 1.0 验收线
```

1.0 验收目标是：用户用中文、英文或中英混合表达常见电脑任务时，Jarvis Lite 能理解意图、补齐缺失信息、判断授权边界、操作目标应用，并在失败时记录上下文和给出下一步建议。

## 核心能力

- 命令行助手和 PySide6 桌面助手入口。
- 长期记忆、经验记忆、个人知识库、资料标签、最近资料/文件/目录/搜索结果和批量标签历史。
- InnerBrain 本地内脑：以 seed/runtime 样本分类器作为自然语言主识别路径，输出 `intent`、`slots`、`confidence`、`missing`、`source`、`reason` 和执行策略；旧规则只作为迁移期兜底。
- InnerBrain 样本闭环：`/inner-brain-adopt`、`/inner-brain-label`、`/inner-brain-teach` 可显式采纳、标注或教学；`/inner-brain-eval-add`、`/inner-brain-eval-label` 和候选写入命令只写本机 evaluation，不自动训练；本机 evaluation 为空时会提示补样本命令默认写入 `runtime.jsonl`；`/inner-brain-eval-local` 与 `/inner-brain-eval-local-file 文件名` 有样本时会提示只看待处理失败、查看已处理和按文件聚焦入口；`/inner-brain-eval-local-resolved [文件名]` 暂无已处理样本时会提示这里只显示已通过样本，并引导查看待处理失败或补充本机 evaluation 样本。
- LLM 外脑 Router：支持 `off`、`fake`、`openai`、`openai-compatible`、`qwen` 和 `gemini`，通过 provider 与 Agent 双层白名单返回结构化 `command`、`answer`、`clarify` 或 `no_action`。
- SearchRouter 联网搜索：支持 `off`、`fake` 和 `tavily`；搜索由 Agent 显式调用，结果可进入最近上下文和 LLM context。
- 自动记忆与配置管家：显式记录、查看、固化、确认、撤销、恢复和忽略记忆与配置候选；联系人别名、应用别名、授权规则和偏好都需要显式确认后写入本地配置。
- 偏好应用链路：已保存偏好可显式启停、预览、生成草稿、确认、查看历史和撤销确认；最近有效确认记录可进入普通 LLM fallback 上下文和本地回答附注，但不进入 LLM 命令白名单、SearchRouter、InnerBrain、路由或桌面执行决策；本地回答附注只对本地知识库回答和长期记忆兜底回答生效，并显示回答类型；可用 `/preference-answer-types` 显式查看和启停这两类本地回答附注，`0.146.0` 起可用 `/preference-reply-context` 显式查看和启停普通回复偏好上下文。
- 桌面与自动化基础：应用注册表、应用启动、只读窗口感知、窗口切换、截图、OCR、截图 OCR 串联、快捷键、鼠标点击、文本输入、Chrome/Clash/QQ/微信/IDEA 第一阶段工作流和任务失败复盘。
- 本地 `unittest` 验证体系和 Windows 安装包构建脚本。

## 快速启动

推荐使用 Python 3.13 系列：

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\activate
python -m pip install -e .
```

启动命令行助手：

```powershell
python src/app.py
```

一次性执行命令：

```powershell
python src/app.py --once "/status"
python src/app.py --once "/help"
python src/app.py --once "/kb"
python src/app.py --once "/inner-brain-status"
python src/app.py --once "/llm-context-preview"
python src/app.py --once "/search-config-check"
python src/app.py --once "/config-manager-status"
python src/app.py --once "/preference-status"
python src/app.py --once "/task-status"
```

启动桌面助手：

```powershell
python -m jarvis_lite.desktop.app
```

源码桌面 smoke：

```powershell
python -m jarvis_lite.desktop.app --smoke
```

安装桌面打包依赖并构建 Windows 安装包：

```powershell
python -m pip install -e ".[desktop-build]"
python scripts/build_windows_installer.py
```

`0.146.0` 测试包路径：`E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.146.0.exe`。

## 常用命令

- `/help`：查看命令入口。
- `/status`：查看当前能力摘要。
- `/kb`、`/kb-summary`、`/ask 问题`、`/read 文件名`：知识库与资料读取。
- `/inner-brain-status`、`/inner-brain-preview 文本`、`/inner-brain-eval-local`：本地内脑状态、预览和本机评估。
- `/llm-status`、`/llm-config-check`、`/llm-context-preview`、`/llm-smoke`：LLM 外脑配置与上下文检查。
- `/search 关键词`、`/search-summary 关键词`、`/search-config-check`、`/search-smoke`：联网搜索。
- `/config-manager-status`、`/config-candidates`、`/config-candidate-confirm 编号`、`/config-candidate-undo 编号`：记忆与配置候选管理。
- `/preference-status`、`/preference-answer-types`、`/preference-reply-context`、`/preference-preview [输入文本]`、`/preference-apply-confirm [输入文本]`、`/preference-apply-history`、`/preference-apply-undo 编号或ID`：偏好管理、回答类型开关、普通回复上下文开关和确认审计。
- `/apps`、`/windows`、`/screenshot`、`/screen-ocr`、`/hotkey`、`/mouse-click`、`/type-text`：桌面观察和基础自动化。
- `/task-start 任务名称`、`/task-step 步骤说明`、`/task-fail 失败原因`、`/task-fail-capture 失败原因`、`/task-status`：任务状态和失败复盘。

## 文档入口

- [DOCUMENTATION.md](DOCUMENTATION.md)：文档整理约定。
- [word/PROJECT-PLAN.md](word/PROJECT-PLAN.md)：当前项目方案唯一入口。
- [word/文档索引.md](word/文档索引.md)：正式文档完整索引。
- [word/progress/2026-06-10.md](word/progress/2026-06-10.md)：当日进度摘要。
- [verification.md](verification.md)：验证记录短入口。
- [verification/2026-06/2026-06-10.md](verification/2026-06/2026-06-10.md)：当日完整验证记录。
