# v94：InnerBrain 本机失败帮助待处理标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v93 本机报告导出待处理失败标题，明确 `0.90.0` 的本机失败帮助与日志待处理标签。

## 目标

`0.90.0` 在 `/help` 和本机失败视图运行日志中，把本机 evaluation 失败视图相关描述从泛化的“失败样本/失败报告”收紧为“待处理失败样本/待处理失败报告”。这样用户在帮助入口、反馈入口和日志留痕里看到的是同一套待处理失败语义。

## 范围

- 修改 `JarvisAgent._help()`：
  - `/inner-brain-eval-local-failed` 帮助文案改为只显示本机 InnerBrain 评估待处理失败样本。
  - `/inner-brain-eval-local-report [文件名]` 帮助文案改为导出本机 InnerBrain 评估待处理失败报告。
  - `/inner-brain-eval-local-file-failed 文件名` 帮助文案改为只显示指定本机评估 JSONL 的待处理失败样本。
- 修改本机失败视图运行日志：
  - `/inner-brain-eval-local-failed` 记录“只显示待处理失败样本”。
  - `/inner-brain-eval-local-file-failed 文件名` 记录“只显示待处理失败样本”。
- 同步 Agent 测试、版本一致性测试、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改固定评估集 `/inner-brain-eval-failed`，不修改命令集合、别名、失败筛选、排序、报告正文、报告路径、本机 evaluation JSONL payload 或训练样本写入。

## 验证

- RED：帮助文案和运行日志断言先失败，证明仍输出旧的“失败样本/失败评估报告”描述。
- GREEN：实现后目标测试通过，覆盖 `/help`、全量本机失败视图日志、指定文件失败视图日志和版本一致性。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
