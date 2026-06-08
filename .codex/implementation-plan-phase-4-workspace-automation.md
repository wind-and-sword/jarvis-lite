# 阶段 4 工作台自动化第一批实现计划

> 日期：2026-05-19
> 执行者：Codex

## 目标

在暂缓摄像头、麦克风等硬件入口后，进入阶段 4 的非硬件能力：常用目录管理和日报生成。

## 方案取舍

1. 第一批只做文件和文档自动化，不启动外部应用、不接入摄像头、不接入麦克风。
2. 常用目录保存到 `memory/directories.json`，供后续打开程序、整理文件、生成日报复用。
3. 日报写入 `word/`，汇总长期记忆摘要、知识库状态、常用目录和最近工具日志。

## 接口契约

- 新增 `automation.py`：
  - `describe_automation(paths)`：输出阶段 4 状态。
  - `add_common_directory(paths, alias, directory)`：登记常用目录。
  - `list_common_directories(paths)`：列出常用目录。
  - `write_daily_report(paths, filename=None)`：生成日报 Markdown。
- 新增命令：
  - `/automation-status`
  - `/dir-add 别名 目录路径`
  - `/dirs`
  - `/daily-report [文件名]`

## 验证

- `unittest` 覆盖目录登记、目录列表、日报生成和 Agent 命令。
- CLI 冒烟使用临时目录，避免污染真实项目数据。
