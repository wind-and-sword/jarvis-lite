# v113：截图 OCR 串联实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v111 屏幕截图保存第一阶段和 v112 OCR 图片识别第一阶段，补齐“截图后识别当前屏幕文字”的组合入口。

## 目标

`0.108.0` 建立截图 OCR 串联第一阶段，让 Jarvis Lite 能通过一个显式命令保存当前主屏幕截图，并立即对该截图执行 OCR。该阶段仍只做观察：不点击、不切换窗口、不输入、不启动外部应用，也不把 OCR 文本自动写入长期记忆、知识库或训练样本。

## 范围

- 在 `src/jarvis_lite/screen_capture.py` 新增组合描述函数：
  - 复用 `save_screen_capture` 保存 PNG。
  - 复用 `describe_image_ocr` 识别刚保存的截图。
  - 输出截图路径、尺寸、OCR 识别结果和只观察不操作边界。
- 在 `JarvisAgent` 增加命令 `/screen-ocr [文件名] [lang=chi_sim+eng]`：
  - 文件名可选，规则沿用 `/screenshot`。
  - 末尾 `lang=...` 覆盖 OCR 语言，规则沿用 `/ocr-image`。
  - 截图失败返回 `截图 OCR 失败：...`。
- 新增或扩展本地 `unittest`，覆盖组合函数、Agent 命令接入和版本一致性。
- 更新帮助文案、当前方案、方案索引、文档索引、进度记录、验证记录和版本号到 `0.108.0`。

## 非目标

- 不做窗口定位或目标窗口截图。
- 不新增 OCR Python 依赖，不引入视觉大模型。
- 不点击、不切换窗口、不输入、不启动应用。
- 不把截图或 OCR 文本自动写入长期记忆、知识库、InnerBrain 训练样本或 evaluation 样本。

## 文件计划

- 修改 `src/jarvis_lite/screen_capture.py`：增加截图 OCR 串联描述函数。
- 修改 `src/jarvis_lite/agent.py`：接入 `/screen-ocr` 和帮助文案。
- 修改 `tests/test_screen_capture.py`：覆盖组合函数截图路径、尺寸、OCR 调用参数和输出。
- 修改 `tests/test_agent.py`：覆盖 Agent `/screen-ocr` 命令和 `lang=...` 参数。
- 修改 `tests/test_project_metadata.py`：版本提升到 `0.108.0`。
- 修改 `pyproject.toml` 和 `src/jarvis_lite/__init__.py`：版本提升到 `0.108.0`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md`、`word/progress/2026-06-03.md`、`verification.md` 和 `verification/2026-06/*`。

## 执行步骤

1. RED：新增 `tests.test_screen_capture.ScreenCaptureTests.test_describe_screen_ocr_captures_then_recognizes_saved_image`，先确认缺少组合函数失败。
2. GREEN：实现组合函数，复用既有保存截图与图片 OCR 能力。
3. RED：新增 Agent `/screen-ocr` 测试，先确认命令尚未接入。
4. GREEN：在 `JarvisAgent` 接入命令、参数解析、日志和帮助文案。
5. RED/GREEN：版本一致性测试更新到 `0.108.0`。
6. 文档同步：更新当前方案、索引、README、进度和验证记录。
7. 回归：运行 `tests.test_screen_capture`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
8. Smoke：运行 `src\app.py --once "/screen-ocr smoke-0.108.0"`；在无 Tesseract 的机器上，允许截图成功后返回 OCR 引擎不可用诊断。
9. 打包验证：运行 Windows 安装包构建、版本化复制、安装脚本/SED/版本资源检查和打包后 smoke。

## 验收标准

- `/screen-ocr` 能保存当前主屏幕截图到 `logs/screenshots/`。
- 输出包含截图相对路径、尺寸、OCR 图片识别段落和语言。
- `lang=eng` 等语言覆盖能传递到 OCR adapter。
- 截图失败时给出可读错误。
- 未安装 Tesseract CLI 时，截图仍可保存，OCR 段落给出清晰不可用说明。
- 该阶段不点击、不切换窗口、不输入、不启动应用。
