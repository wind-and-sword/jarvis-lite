# 0.20.0 InnerBrain 候选按编号标注计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

在 `0.19.0` 候选按编号教学命令的基础上，补齐非命令型标注入口：

```text
/inner-brain-label-candidate 编号 => intent [slot=value ...]
```

## 边界

- 不自动推断 intent。
- 不自动写入候选，必须用户显式执行命令。
- 不执行被标注出来的本地动作。
- 不把标注命令写入最近路由历史，避免候选编号变化。
- 复用 `/inner-brain-label` 的 slot 解析、runtime 样本写入和 InnerBrain 刷新逻辑。

## 验收

- 候选编号有效时保存候选原文为 labeled runtime 样本。
- 候选编号不存在时返回明确提示且不写样本。
- slot 缺少 `=` 时返回标注参数错误且不写样本。
- `/inner-brain-candidates` 输出给出按编号标注提示。
- 版本、README、方案索引、进度和验证记录同步到 `0.20.0`。
