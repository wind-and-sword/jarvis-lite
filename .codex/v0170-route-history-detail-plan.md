# 0.17.0 路由历史详情实施计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

新增 `/route-history` 诊断入口，展示最近 5 条路由的完整可读详情，并把最近路由摘要纳入 `/recent-context`。本阶段不改变自然语言识别、InnerBrain、LLM fallback 或联网搜索顺序。

## 接口契约

- `/route-history`、`route-history`、`/routes`、`routes`：返回最近路由历史详情。
- 无历史时返回“路由历史：还没有记录。”并提示先输入问题或命令。
- 有历史时返回：
  - 路由、明细、时间、输入、结果、依据。
  - 每条历史按最近优先编号，最多 5 条。
- `/recent-context` 在已有内容后追加最近路由短摘要。

## TDD 步骤

1. 新增 `test_route_history_command_reports_empty_state`，先验证失败。
2. 新增 `test_route_history_command_reports_recent_decisions_with_explanations`，先验证失败。
3. 新增 `test_recent_context_includes_recent_route_history`，先验证失败。
4. 新增 `test_route_history_command_restores_on_startup`，先验证失败。
5. 实现 `JarvisAgent._route_history_status()` 与 `_route_history_detail_lines()`。
6. 将命令接入 `handle()`、`_help()`、`_is_explicit_command_prompt()`，并在 `_recent_context_status()` 追加短摘要。
7. 版本提升到 `0.17.0`，同步文档和验证记录。

## 验证

- 目标测试：新增路由历史详情测试和版本测试。
- 邻近回归：`tests.test_desktop_widgets tests.test_desktop_bridge tests.test_desktop_app tests.test_agent tests.test_llm tests.test_inner_brain tests.test_conversation`。
- 全量回归：`python -m unittest discover -s tests -v`。
- 桌面源码 smoke、打包安装器、打包后 exe smoke、安装器元数据、静态检查、Markdown 链接检查、敏感信息扫描和本地配置文件检查。
