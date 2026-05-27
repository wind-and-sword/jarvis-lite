# Jarvis Lite 阶段 3 进度记录

> 日期：2026-05-19
> 执行者：Codex

## 当前目标

阶段 3 聚焦语音入口。第一批先建立可自动验证的基础闭环：查看语音状态、播报文本、把外部已识别的语音文本送入 Jarvis Lite 处理并播报回答。

## 当前取舍

- 先不做麦克风实时识别，避免把不可稳定自动验证的硬件流程放入主链路。
- 语音播报复用平台能力：Windows 可使用 `System.Speech`；自动化测试和无语音环境使用 transcript 引擎。
- transcript 引擎会把播报文本写入 `logs/voice-output.txt`，便于本地验证和排障。

## 已完成

- 新增 `voice.py`，封装语音入口状态和文本播报。
- 新增 `/voice-status` 命令，显示当前语音引擎、播报记录路径和麦克风识别状态。
- 新增 `/speak 文本` 命令，播报指定文本，并记录到 `logs/voice-output.txt`。
- 新增 `/voice 已识别的语音文本` 命令，把已识别文本交给现有 Agent 处理，并播报回答。
- 新增环境变量 `JARVIS_LITE_VOICE_ENGINE`，可设为 `transcript` 或 `windows`；默认 `auto`。
- 自动化测试使用 `transcript` 引擎，避免依赖扬声器或系统语音服务。

## 验证结果

- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：74 个测试通过。
- `JARVIS_LITE_VOICE_ENGINE=transcript` 下，`/voice-status` 可输出语音入口状态。
- `JARVIS_LITE_VOICE_ENGINE=transcript` 下，`/speak 你好 Jarvis` 可写入 `logs/voice-output.txt`。
- `JARVIS_LITE_VOICE_ENGINE=transcript` 下，`/voice Jarvis Lite 推荐使用什么 Python 版本？` 可复用知识库回答，并把回答写入播报记录。

## 下一步

1. 接入真实麦克风语音识别，优先评估主流库或系统服务。
2. 增加语音会话模式，让一次启动后可以连续处理多轮语音输入。
3. 评估语音播报参数，例如语速、音量和可选声音。
