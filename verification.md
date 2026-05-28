# 验证记录

> 日期：2026-05-28
> 执行者：Codex
> 说明：根目录只作为验证记录入口，不再长期追加完整命令和输出。

## 最近摘要

- 2026-05-28：新增 `/inner-brain-status` 和 `/inner-brain-preview 文本`，可查看内脑样本、阈值和单句识别结果，preview 不执行本地动作；全量 `unittest` 359 项通过。
- 2026-05-28：InnerBrain 本地内脑第一版落地，新增结构化结果、legacy 规则包装、seed/runtime JSONL 样本相似度识别和 Agent 接入；全量 `unittest` 354 项通过。
- 2026-05-28：根据用户安装后的真实日志修复自然语言识别缺口，新增问候、助手身份询问和桌面 `.lnk` 快捷方式删除意图；项目版本提升到 `0.1.2`，安装完成弹窗显示版本号，全量 `unittest` 345 项通过，安装器生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 2026-05-28：LLM 调用收口与 `0.1.1` 打包完成，新增 `/llm-context-preview`、Agent 硬白名单、状态/错误诊断和覆盖安装提示；全量 `unittest` 339 项通过，安装器生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 2026-05-27：LLM provider instructions 增加 Jarvis Lite 命令白名单，`/llm-config-example` 补充 `/llm-smoke 请用一句话确认连接可用`，全量 `unittest` 331 项通过。
- 2026-05-27：新增 `/llm-smoke [prompt]`，可强制调用当前 LLM Router 做配置验证，且不会执行模型返回的命令建议。
- 2026-05-27：LLM OpenAI-compatible 端点支持直接粘贴完整 `/v1/responses` URL，SDK 调用会自动归一化为 `/v1` base URL；本地 `unittest` 全量 326 项通过。
- 2026-05-27：LLM 外脑整合一致性核对完成，代码、README、当前方案、v3 方案、每日进度和验证记录口径一致。
- 2026-05-27：编号最近资料打标签缺失提示已完成专项验证，历史记录已迁入周归档。
- 2026-05-27：项目文档整理第一阶段完成验证，`git diff --check` 退出 0，Markdown 本地链接检查通过。
- 2026-05-27：项目文档整理第二阶段完成验证，验证记录已拆为日文件，自然语言大进度已拆为主题明细。
- 2026-05-27：早期文档整理收尾时本地 `unittest` 全量 290 项通过，桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。

## 详细记录

- [verification/README.md](verification/README.md)：验证记录归档规则和入口。
- [verification/2026-05/README.md](verification/2026-05/README.md)：2026-05 验证记录索引。
- [2026-05-18 周索引](verification/2026-05/week-2026-05-18.md)：2026-05-18 至 2026-05-24。
- [2026-05-25 周索引](verification/2026-05/week-2026-05-25.md)：2026-05-25 至 2026-05-31。
- [2026-05-28 验证记录](verification/2026-05/2026-05-28.md)：最近一次验证明细。

## 记录规则

- 根目录 `verification.md` 只保留最近摘要和索引。
- 完整验证命令、RED/GREEN 过程和收尾结果写入 `verification/YYYY-MM/YYYY-MM-DD.md`。
- 自然周文件只做索引，不再承载完整明细。
- 每次新增验证记录后同步更新对应月份索引和周索引。
