# 验证记录

> 日期：2026-06-10
> 执行者：Codex
> 说明：根目录只作为验证记录入口，不长期追加完整命令和输出。完整明细进入 `verification/YYYY-MM/YYYY-MM-DD.md`。

## 最近摘要

- 2026-06-10：发布 `0.146.0` 可安装测试包，完成偏好普通回复上下文开关第一阶段；默认保持最近有效确认记录进入普通 LLM fallback 上下文，可用 `/preference-reply-context`、`/preference-reply-context-enable` 和 `/preference-reply-context-disable` 显式查看或启停，停用后不影响本地回答附注；补齐每日进度索引后全量 `unittest` 787 项通过，安装包生成到 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.146.0.exe`。
- 2026-06-10：发布 `0.145.0` 可安装测试包，完成偏好本地回答类型开关第一阶段；默认保持本地知识库回答和长期记忆兜底回答附注启用，可用 `/preference-answer-types`、`/preference-answer-type-enable 类型` 和 `/preference-answer-type-disable 类型` 显式查看或启停，新增命令不进入 LLM 白名单；全量 `unittest` 783 项通过，安装包生成到 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.145.0.exe`。
- 2026-06-09：发布 `0.144.0` 可安装测试包，完成偏好本地回答附注范围第一阶段；本地知识库回答和长期记忆兜底回答分别展示回答类型标签，未知回答类型不生成附注，普通 LLM fallback 上下文仍不展示本地附注或撤销命令；全量 `unittest` 778 项通过，安装包生成到 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.144.0.exe`。
- 2026-06-09：发布 `0.143.0` 可安装测试包，完成偏好应用撤销提示第一阶段；确认输出和本地回答附注会展示 `撤销确认：/preference-apply-undo prefapp-...`，普通 LLM fallback 上下文不展示该命令；全量 `unittest` 777 项通过。
- 2026-06-09：发布 `0.142.0` 可安装测试包，完成偏好格式化本地回答第一阶段；最近有效确认记录可作为可审计附注追加到本地知识库命中回答和长期记忆兜底回答；全量 `unittest` 777 项通过。
- 2026-06-09：发布 `0.141.0` 可安装测试包，完成偏好进入普通回复上下文第一阶段；最近有效确认记录可进入普通 LLM fallback 上下文和 `/llm-context-preview`；全量 `unittest` 774 项通过。
- 2026-06-09：发布 `0.140.0` 可安装测试包，完成偏好应用确认记录与撤销第一阶段；确认成功写入运行态历史，撤销只改确认记录状态；全量 `unittest` 770 项通过。

## 索引

- [2026-06 验证索引](verification/2026-06/README.md)
- [2026-06-10 完整验证记录](verification/2026-06/2026-06-10.md)
- [2026-06-09 完整验证记录](verification/2026-06/2026-06-09.md)
- [2026-06-08 自然周索引](verification/2026-06/week-2026-06-08.md)
