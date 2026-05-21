# Jarvis Lite 自然语言本地大脑第一版进度

> 日期：2026-05-21
> 执行者：Codex

## 当前目标

把用户安装测试日志中暴露的自然语言问题收口，让常见操作不依赖斜杠命令，并为后续语音入口和大模型外脑接入提供统一文本意图层。

## 已完成

- 新增 `jarvis_lite.intent`：
  - `NaturalLanguageIntent`：表示本地大脑识别出的意图。
  - `parse_natural_language_intent()`：把常见中文表达映射为内部命令或本地动作。
- 自然语言已支持：
  - “你现在能做什么事”
  - “查看知识库”
  - “查看常用目录”
  - “生成日报”
  - “检查更新”
  - “下载更新”
  - “打开D盘”
- 修复身份误写入：
  - `我是你的什么人，你知道吗` 现在会作为身份问题处理。
  - 疑问句不会被 `我是...` 规则写入 `用户身份`。
- `/status` 文案更新为当前完整状态，覆盖命令行、桌面、自然语言、语音、工作台和更新能力。
- `/voice 文本` 会复用同一套 Agent 流程，因此自然语言意图层也能被语音入口复用。

## 验证结果

- RED 验证：
  - `tests.test_memory` 先因身份关系问句未识别失败。
  - `tests.test_agent` 先因能力询问、日报、知识库、更新和打开 D 盘自然语言都落入通用兜底失败。
- 专项 GREEN 验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v`：46 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：173 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：未发现空白错误，仅出现 CRLF 换行提示。

## 后续建议

- 下一步可以扩展自然语言参数补全，例如“整理桌面”“打开项目目录”“给这个资料打标签”。
- 后续接入大模型时，应让大模型输出结构化意图建议，再由本地大脑决定是否执行。
- 可以把成功任务沉淀为“经验记忆”，让助手逐步学习用户常用表达和常用流程。
