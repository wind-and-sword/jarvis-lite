# 验证记录

> 日期：2026-05-29
> 执行者：Codex
> 说明：根目录只作为验证记录入口，不再长期追加完整命令和输出。

## 最近摘要

- 2026-05-29：发布 `0.1.7` 可安装测试包，包含 InnerBrain 多轮澄清补槽第一版；导入路径和桌面快捷方式名称可在下一句直接补齐后继续执行，全量 `unittest` 423 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.7.exe`。
- 2026-05-28：发布 `0.1.6` 可安装测试包，包含 v6 高频 legacy 别名迁移；版本一致性测试按 TDD 先失败后通过，全量 `unittest` 420 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.6.exe`。
- 2026-05-28：v6 高频 legacy 别名迁移完成，问候、身份/能力、上下文、知识库、最近文件、日报、更新、经验和礼貌前缀编号最近文件导入等 30 个代表表达返回 `seed_sample`；代表句复扫 `legacy=0 unknown=0`。
- 2026-05-28：v6 收尾与 `0.1.5` 可安装测试包完成，新增最近联网搜索来源编号查看、来源比较、摘要保存、摘要导入知识库、桌面快捷方式宾语前置表达迁移和 InnerBrain 缺槽澄清提示；全量 `unittest` 419 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.5.exe`。
- 2026-05-28：InnerBrain 显式文件名标签槽位迁移为 `document.tag_path`，`给 note.txt 打标签 项目` 和 `把 data/note.txt 标记为 项目 Python` 返回 `seed_sample`；全量 `unittest` 411 项通过。
- 2026-05-28：发布 `0.1.4` 可安装测试包，包含 SearchRouter + LLMRouter 搜索总结组合流程；版本一致性测试已按 TDD 先失败后通过。
- 2026-05-28：SearchRouter + LLMRouter 组合入口完成，`/search` 写入最近联网搜索上下文，`/search-summary` 和“联网查一下...并总结”会先搜索再把来源交给 LLM 外脑总结；全量 `unittest` 411 项通过。
- 2026-05-28：InnerBrain 文件路径、目录和经验槽位动作迁移为样本签名 + `path/source/alias/experience/query` 槽位抽取，显式文件读取/导入、目录打开/整理和经验记录/搜索/建议返回 `seed_sample`；全量 `unittest` 406 项通过。
- 2026-05-28：InnerBrain 标签槽位动作迁移为样本签名 + `tags/alias/result_index` 槽位抽取，当前资料/结果打标签、编号资料/结果打标签、标签组读取/预览和标签历史读取返回 `seed_sample`；全量 `unittest` 403 项通过。
- 2026-05-28：InnerBrain 第一批编号槽位动作迁移为样本签名 + `result_index` 槽位抽取，`读取第二份资料`、`查看第二条结果`、`执行第二条建议` 等返回 `seed_sample`；全量 `unittest` 402 项通过。
- 2026-05-28：InnerBrain 迁移为样本分类器优先，高频自然语言返回 `seed_sample`/`runtime_sample`，旧 parser 仅作为 `legacy_fallback` 迁移期兼容；全量 `unittest` 401 项通过。
- 2026-05-28：联网搜索第一版落地，新增 SearchRouter、Tavily/fake provider、`config/search.local.json` 本地配置、`/search-status`、`/search-enable`、`/search 关键词` 和自然语言“联网查一下...”入口；全量 `unittest` 399 项通过，敏感信息扫描通过。
- 2026-05-28：LLM 外脑新增本地 `config/llm.local.json` 配置读取、`/llm-enable` 和“开启外脑”运行中重载入口；全量 `unittest` 384 项通过，敏感信息扫描未命中真实 API key。
- 2026-05-28：`0.1.3` 可安装测试版完成，包含 InnerBrain v1、preview/status、runtime 样本采纳、人工标注和口语教学入口；全量 `unittest` 377 项通过，安装器生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 2026-05-28：新增 `/inner-brain-teach 文本 => /命令` 和“以后我说“文本”就是 /命令”，可把自然语言短句教学为已知命令，保存时不执行目标命令；全量 `unittest` 376 项通过。
- 2026-05-28：新增 `/inner-brain-label 文本 => intent [slot=value ...]`，可人工标注 unknown 或误识别样本，保存后当前 Agent 立即刷新 InnerBrain；全量 `unittest` 372 项通过。
- 2026-05-28：新增 `/inner-brain-adopt 文本`，可将 InnerBrain 正确识别结果保存为运行态 JSONL 样本，重复样本不重复写入，保存时不执行命令；全量 `unittest` 366 项通过。
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
- [2026-05-29 验证记录](verification/2026-05/2026-05-29.md)：最近一次验证明细。

## 记录规则

- 根目录 `verification.md` 只保留最近摘要和索引。
- 完整验证命令、RED/GREEN 过程和收尾结果写入 `verification/YYYY-MM/YYYY-MM-DD.md`。
- 自然周文件只做索引，不再承载完整明细。
- 每次新增验证记录后同步更新对应月份索引和周索引。
