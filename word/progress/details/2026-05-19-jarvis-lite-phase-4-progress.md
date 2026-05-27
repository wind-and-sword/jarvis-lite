# Jarvis Lite 阶段 4 进度记录

> 日期：2026-05-19
> 执行者：Codex

## 当前目标

根据用户要求，摄像头、麦克风等硬件入口先暂停。阶段 4 先推进非硬件的工作台自动化能力：常用目录管理、日报生成、文件整理预览和目录打开记录。

## 当前取舍

- 第一批不接入摄像头、麦克风或其他硬件。
- 第一批不启动外部应用，只做可自动验证的本地文件和文档自动化。
- 文件整理先只做预览，不移动、不删除文件。
- 目录打开先只写入 transcript，不真实启动资源管理器或外部应用。
- 常用目录登记到 `memory/directories.json`，作为后续打开目录、整理文件、项目切换的基础数据。
- 日报写入 `word/`，方便用户直接阅读。

## 已完成

- 新增 `automation.py`，封装工作台自动化状态、常用目录登记、常用目录列表和日报生成。
- 新增 `/automation-status` 命令，查看阶段 4 自动化状态。
- 新增 `/dir-add 别名 目录路径` 命令，登记常用目录。
- 新增 `/dirs` 命令，查看已登记的常用目录。
- 新增 `/daily-report [文件名]` 命令，生成 Markdown 日报到 `word/`。
- 日报内容包含长期记忆摘要、知识库资料数量、可检索行数、常用目录和最近工具日志。
- 新增 `/organize-preview 常用目录别名` 命令，按扩展名生成文件整理预览。
- 整理预览会跳过子目录，只列出建议目标文件夹和文件名，不执行移动或删除。
- 新增 `/dir-open 常用目录别名` 命令，把打开目录请求记录到 `logs/desktop-actions.txt`。
- `/dir-open` 当前是 dry-run/transcript 模式，不启动外部应用。

## 验证结果

- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：80 个测试通过。
- 临时目录 Agent 冒烟验证：`/automation-status` 可输出阶段 4 状态。
- 临时目录 Agent 冒烟验证：`/dir-add 项目 <目录>` 后，`/dirs` 可显示登记结果。
- 临时目录 Agent 冒烟验证：`/daily-report today.md` 可写入 `word/today.md`。
- 临时目录 Agent 冒烟验证：`/organize-preview 项目` 可输出按扩展名分组的整理预览。
- 临时目录 Agent 冒烟验证：`/dir-open 项目` 可写入 `logs/desktop-actions.txt`。

## 下一步

1. 增加文件整理执行前的二次确认或 dry-run 输出落盘能力。
2. 增加常用目录打开的真实执行模式，但默认仍保留 transcript 模式用于验证。
3. 再评估是否接入真实桌面应用启动能力。
