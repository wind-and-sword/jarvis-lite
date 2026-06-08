# 0.15.0 路由解释详情 v1 计划

- 日期：2026-05-29
- 执行者：Codex

## 目标

在 `0.14.0` 最近路由决策状态基础上，为桌面和 Agent 状态增加“依据”行，解释最近一次回复为什么走 `inner-brain`、`inner-brain-clarify`、`knowledge`、`llm-fallback` 或记忆兜底。

## 约束

- 不新增自然语言正则规则。
- 不改变 InnerBrain、LLM、搜索、知识库、记忆兜底的执行优先级。
- 复用 `InnerBrainResult` 和 `RuntimeRouteDecisionContext`，不引入新自研路由组件。
- 本地配置文件和真实 API key 不提交。

## 实施步骤

1. 按 TDD 先写路由解释测试，覆盖 InnerBrain 执行、InnerBrain 澄清、LLM fallback、运行态恢复、Bridge/Panel 透传和版本提升。
2. 扩展运行态路由上下文，新增 `explanation` 字段并读写 JSON。
3. 在 `JarvisAgent` 中生成短解释文本：InnerBrain 使用 source/confidence/missing/reason，LLM 使用 provider/model/source/type/summary/reason，其他路径给出数据来源说明。
4. 更新版本、README、项目计划、方案索引、进度和验证记录。
5. 执行目标测试、相邻回归、全量测试、桌面 smoke、安装包构建、安装器元数据校验、静态检查、链接检查、敏感扫描，再提交并 push。

## 验收标准

- `route_status_text()` 对有解释的路径展示 `依据：...`。
- InnerBrain 问候状态包含 `source=seed_sample`、`confidence=` 和 `reason=`。
- InnerBrain 澄清状态包含缺失槽位。
- LLM fallback 状态包含 provider/model/type/summary 或 reason。
- 重启 Agent 后解释信息仍可恢复。
- 桌面 Bridge/Panel 展示同一段路由解释。
