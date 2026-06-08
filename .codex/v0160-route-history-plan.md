# 0.16.0 最近路由历史 v1 计划

- 日期：2026-05-29
- 执行者：Codex

## 目标

在 `0.15.0` 最近路由解释基础上，保存并展示最近 5 次路由决策历史，便于观察连续输入中哪些走了 InnerBrain、LLM fallback、显式命令、知识库或记忆兜底。

## 约束

- 不新增自然语言正则规则。
- 不改变 InnerBrain/LLM/Search/知识库/记忆的路由顺序。
- 保持 `recent_route_decision` 作为最新单条记录，新增短历史字段兼容旧运行态。
- 桌面继续复用现有 `route_status_text`，不做后台轮询。

## 实施步骤

1. TDD 新增 Agent、Bridge、Panel 和版本测试，先验证缺少“最近路由历史”。
2. `RuntimeContext` 新增 `recent_route_decisions`，读写最多 5 条，并兼容旧的 `recent_route_decision`。
3. `JarvisAgent._remember_route_decision()` 同步更新最新单条和短历史。
4. `route_status_text()` 追加紧凑历史行，显示序号、route/detail、输入和结果。
5. 更新版本、README、PROJECT-PLAN、方案索引、进度和验证记录。
6. 执行目标测试、相邻回归、全量测试、桌面 smoke、安装包构建、安装器元数据校验、静态检查、链接检查和敏感扫描，再提交并 push。

## 验收标准

- 最近路由状态仍保留当前最新输入的详细说明和 `依据`。
- 连续两次输入后展示“最近路由历史”，最新项排在第 1 条。
- 重启 Agent 后历史仍可恢复。
- 历史最多保留 5 条。
- 桌面 Bridge/Panel 能看到同一段历史。
