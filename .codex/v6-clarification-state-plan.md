# v6 多轮澄清状态执行计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

让 InnerBrain 缺槽澄清从“只提示补全命令”升级为“下一句自然语言可直接补齐槽位并继续执行”。

## 范围

- 第一批覆盖 `knowledge.import missing=source` 和 `desktop.delete_shortcut missing=items`。
- 同步提供取消待澄清状态的自然语言入口。
- 不新增独立执行层，补齐后仍转换为既有 `NaturalLanguageIntent` 或 slash command，由 `JarvisAgent` 执行。

## 执行

1. 写 RED 测试：
   - runtime 样本“帮我导入这份资料”缺 `source`，用户下一句给路径后导入成功。
   - “删除桌面快捷方式”缺 `items`，用户下一句给快捷方式名后删除成功。
   - “取消补充”清除待澄清状态。
2. 实现 pending clarification 状态：
   - Agent 保存最近一次 `InnerBrainPolicy.CLARIFY` 结果。
   - 下一条普通输入先尝试回填 missing slot。
   - 补齐成功后清除 pending 并执行。
3. 更新文档和验证记录。
4. 运行目标测试、全量测试、smoke、静态检查和敏感信息扫描。
5. 本地提交，不 push。
