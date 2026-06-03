# v112：OCR 图片识别第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v111 屏幕截图保存第一阶段，补齐“看懂屏幕”路线中识别已存在图片文字的 OCR 基础。

## 目标

`0.107.0` 建立 OCR 图片识别第一阶段，让 Jarvis Lite 能诊断本机 OCR 引擎状态，并在本机安装 Tesseract CLI 时对指定图片执行 OCR。该阶段只识别用户指定的图片路径，不自动截图、不点击、不切换窗口、不做网页采集。

## 范围

- 新增 `src/jarvis_lite/ocr.py`：
  - 使用成熟的 Tesseract CLI 作为 OCR adapter，不新增 Python OCR 依赖。
  - 支持 `JARVIS_LITE_TESSERACT_CMD` 指定 `tesseract.exe` 路径，否则从 `PATH` 查找。
  - 默认语言为 `chi_sim+eng`，命令可用 `lang=...` 覆盖。
  - 返回 OCR 引擎可用性、命令路径、版本、不可用原因和图片识别结果。
- 在 `JarvisAgent` 增加命令：
  - `/ocr-status`：只诊断 OCR 引擎状态，不读取图片。
  - `/ocr-image 图片路径 [lang=chi_sim+eng]`：识别指定图片文字。
- 新增 `tests/test_ocr.py` 覆盖 OCR 状态、图片识别输出、缺失图片和引擎不可用错误。
- 更新帮助文案、当前方案、方案索引、文档索引、进度记录、验证记录和版本号到 `0.107.0`。

## 非目标

- 不安装 Tesseract 或任何系统级依赖。
- 不新增 Python OCR 依赖，不引入大模型视觉 OCR。
- 不自动截图，不把 `/screenshot` 与 OCR 串联。
- 不做屏幕元素定位、点击、窗口切换或键盘输入。
- 不把 OCR 文本自动写入长期记忆、知识库或训练样本。

## 文件计划

- 新增 `src/jarvis_lite/ocr.py`：OCR 状态诊断和图片识别逻辑。
- 新增 `tests/test_ocr.py`：OCR 单元测试。
- 修改 `src/jarvis_lite/agent.py`：接入 `/ocr-status`、`/ocr-image` 和帮助文案。
- 修改 `tests/test_agent.py`：Agent OCR 命令回归。
- 修改 `pyproject.toml` 和 `src/jarvis_lite/__init__.py`：版本提升到 `0.107.0`。
- 修改 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md` 和 `word/progress/2026-06-03.md`：文档同步。

## TDD 步骤

1. RED：新增 `tests/test_ocr.py`，先确认缺少 `jarvis_lite.ocr` 失败。
2. GREEN：实现 OCR 状态、图片路径解析、Tesseract CLI adapter、识别输出和错误反馈。
3. RED：新增 Agent `/ocr-status` 和 `/ocr-image` 测试，先确认 `JarvisAgent` 尚未接入。
4. GREEN：接入 Agent 命令、运行日志和帮助文案。
5. RED/GREEN：版本一致性测试更新到 `0.107.0`。
6. 回归：运行 `tests.test_ocr`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
7. Smoke：运行 `src\app.py --once "/ocr-status"`、桌面源码 smoke 和打包后 smoke。

## 验收

- `/ocr-status` 能显示 provider、默认语言、命令路径或不可用原因。
- `/ocr-image 图片路径` 能对存在的图片调用 OCR recognizer 并返回文本。
- 未安装 Tesseract CLI 时，`/ocr-status` 和 `/ocr-image` 给出清晰不可用说明。
- `lang=eng` 等语言覆盖能传递到 OCR adapter。
- 该阶段不截图、不点击、不切换窗口、不输入。
