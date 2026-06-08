# 阶段 3 语音入口第一批实现计划

> 日期：2026-05-19
> 执行者：Codex

## 目标

进入阶段 3，先建立可自动验证的语音入口基础闭环：语音状态、文本转语音播报、已识别语音文本进入 Agent 对话流程。

## 方案取舍

1. 先做语音播报和“识别后文本”入口，不做麦克风实时识别。
2. 播报使用平台能力：Windows 下可启用 `System.Speech`；默认和测试使用 transcript 模式，把播报内容写入 `logs/voice-output.txt`。
3. `/voice 文本` 表示已经由外部语音识别得到的文本，Jarvis Lite 负责调度回答并播报结果。
4. 后续如果要真实麦克风识别，再接入主流语音识别库或系统服务，而不是自研识别器。

## 接口契约

- 新增 `voice.py`：
  - `describe_voice(paths)`：返回语音状态说明。
  - `speak_text(paths, text, engine=None)`：播报文本并记录 transcript。
- 新增命令：
  - `/voice-status`：查看语音入口状态。
  - `/speak 文本`：播报指定文本。
  - `/voice 文本`：把已识别语音文本交给 Agent 处理，并播报回答。

## 验证

- `unittest` 覆盖 transcript 模式、空文本校验、Agent 命令和 `/voice` 调度。
- CLI 冒烟使用 `JARVIS_LITE_VOICE_ENGINE=transcript`，避免自动化验证依赖扬声器。
