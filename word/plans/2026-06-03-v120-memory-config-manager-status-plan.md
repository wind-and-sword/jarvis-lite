# v120：自动记忆与配置管家第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v119 意图授权层第一阶段，进入 Jarvis Lite 1.0 验收路线的自动记忆与配置管家主线。

## 背景

`0.114.0` 已完成意图授权层第一阶段：显式 slash command 继续执行，LLM 外脑建议桌面动作命令时由授权层降级，不自动触发键鼠、窗口或应用动作。

下一步需要让用户不用手工翻找 `memory/` 与 `config/` 文件，就能知道 Jarvis Lite 当前沉淀了哪些长期记忆、经验、常用目录、应用覆盖和 provider 配置。第一阶段先做只读盘点和管理入口，不自动写入长期配置。

## 目标

- 新增统一只读状态：`/config-manager-status`。
- 兼容别名：`/memory-config-status`。
- 报告长期记忆、经验记忆、常用目录、应用本地覆盖、LLM 本地配置和联网搜索本地配置。
- 输出已有管理入口，例如 `/remember`、`/experience`、`/dir-add`、`/apps`、`/llm-config-check`、`/search-config-check`。
- 所有 API key 只显示“已配置/未配置”，不回显真实值。

## 非目标

- 不自动保存联系人别名、免确认规则或应用路径。
- 不从普通聊天直接写入长期记忆。
- 不新增删除或撤销命令；本阶段只提示现有入口和后续边界。
- 不调用 LLM provider 或联网搜索 provider。

## 实施步骤

1. 新增 `tests/test_memory_config_manager.py`，先验证空状态、已配置状态和 API key 不泄露。
2. 在 `tests/test_agent.py` 增加 `/config-manager-status` 命令、帮助和 `/status` 断言。
3. 将版本元数据测试期望提升到 `0.115.0`，验证 RED。
4. 新增 `src/jarvis_lite/memory_config_manager.py`，复用现有路径、目录、应用、LLM 和搜索配置解析。
5. 将新命令接入 `JarvisAgent`、`TEACHABLE_INNER_BRAIN_COMMAND_INTENTS`、`/help` 和 `/status`。
6. 同步版本、README、PROJECT-PLAN、计划索引、文档索引、进度与验证记录。
7. 运行目标测试、相邻回归、全量 unittest、smoke、打包和静态检查。

## 验收标准

- `/config-manager-status` 输出“记忆与配置管家”并列出六类内部存储状态。
- `/memory-config-status` 返回同一能力视图。
- LLM/Search 本地配置包含 API key 时，响应和日志不出现真实 key。
- `/help` 和 `/status` 均提示配置管家入口。
- `0.115.0` 版本元数据、安装包脚本和版本资源一致。
