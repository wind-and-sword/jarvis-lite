# 验证记录

> 日期：2026-06-01
> 执行者：Codex
> 说明：根目录只作为验证记录入口，不再长期追加完整命令和输出。

## 最近摘要

- 2026-06-01：发布 `0.23.0` 可安装测试包，收口桌面内脑候选快捷入口；桌面面板和托盘直接快捷命令新增“内脑候选”，一键执行 `/inner-brain-candidates` 查看待显式教学或标注的候选；全量 `unittest` 512 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.23.0.exe`。
- 2026-06-01：发布 `0.22.0` 可安装测试包，收口 InnerBrain 候选运行态统计 v1；候选出现次数会写入本地运行态上下文，跨最近 5 条路由继续保留，显式 teach、label 或 adopt 后移除对应候选；全量 `unittest` 511 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.22.0.exe`。
- 2026-06-01：发布 `0.21.0` 可安装测试包，收口 InnerBrain 候选频次排序 v1；`/inner-brain-candidates` 会聚合最近路由里的重复 fallback 候选，按出现次数优先展示，并让编号教学/编号标注使用同一排序；全量 `unittest` 508 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.21.0.exe`。
- 2026-06-01：发布 `0.20.0` 可安装测试包，收口 InnerBrain 候选按编号标注 v1；新增 `/inner-brain-label-candidate 编号 => intent [slot=value ...]`，可把 `/inner-brain-candidates` 当前候选显式标注为 runtime 样本，命令本身不污染路由历史；全量 `unittest` 505 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.20.0.exe`。
- 2026-06-01：发布 `0.19.0` 可安装测试包，收口 InnerBrain 候选按编号教学 v1；新增 `/inner-brain-teach-candidate 编号 => /命令`，可把 `/inner-brain-candidates` 当前候选显式教学为已知命令，命令本身不污染路由历史；全量 `unittest` 502 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.19.0.exe`。
- 2026-05-29：发布 `0.18.0` 可安装测试包，收口 InnerBrain 训练候选 v1；新增 `/inner-brain-candidates` 从最近路由历史中筛选 LLM fallback、记忆兜底和 InnerBrain 澄清输入，给出 teach/label 示例但不自动训练；全量 `unittest` 499 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.18.0.exe`。
- 2026-05-29：发布 `0.17.0` 可安装测试包，收口路由历史详情 v1；新增 `/route-history` 展示最近 5 条输入的完整路由、时间、输入、结果和依据，`/recent-context` 同步展示最近路由摘要；全量 `unittest` 496 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.17.0.exe`。
- 2026-05-29：发布 `0.16.0` 可安装测试包，收口最近路由历史 v1；桌面面板在最新路由详情后追加最近 5 条路由历史，便于连续测试时确认多次输入分别走了命令、InnerBrain、LLM fallback、知识库还是记忆兜底；全量 `unittest` 492 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.16.0.exe`。
- 2026-05-29：发布 `0.15.0` 可安装测试包，收口路由决策解释详情 v1；桌面面板在最近路由状态中追加 `依据`，展示 InnerBrain 的 source/confidence/missing/reason 或 LLM fallback 的 provider/model/type/summary/reason，便于确认自然语言回复的处理依据；全量 `unittest` 487 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.15.0.exe`。
- 2026-05-29：发布 `0.14.0` 可安装测试包，收口最近路由决策状态 v1；桌面面板会固定展示最近一条输入由 `command`、`inner-brain`、`knowledge`、`llm-fallback` 等哪一层处理，便于确认回复是否来自本地内脑、外脑或兜底；全量 `unittest` 483 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.14.0.exe`。
- 2026-05-29：发布 `0.13.0` 可安装测试包，收口桌面外脑运行状态 v1；桌面面板会固定展示外脑启用状态、provider、model、最近一次 LLM 调用触发来源、返回类型、输入摘要和结果摘要；全量 `unittest` 478 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.13.0.exe`。
- 2026-05-29：发布 `0.12.0` 可安装测试包，收口桌面外脑待补充状态 v1；桌面面板会固定展示当前 LLM 待补充问题、澄清轮次、原始问题和取消提示，取消或补齐后随响应刷新；全量 `unittest` 474 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.12.0.exe`。
- 2026-05-29：发布 `0.11.0` 可安装测试包，收口 LLM 外脑澄清轮数与过期策略 v1；连续 LLM `clarify` 会保留最初原始问题并递增轮次，超过 3 轮会结束 pending，超过 12 小时未补充的 runtime pending 会在 Agent 启动时清理；全量 `unittest` 471 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.11.0.exe`。
- 2026-05-29：发布 `0.10.0` 可安装测试包，收口 LLM 外脑澄清状态持久化 v1；LLM 待补充问题会写入运行态上下文，新 Agent 实例可恢复并继续补充，`/recent-context` 可查看待补充外脑问题且不消耗 pending；全量 `unittest` 468 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.10.0.exe`。
- 2026-05-29：发布 `0.9.0` 可安装测试包，收口 LLM 外脑多轮澄清 v1；LLM 返回澄清问题后，用户下一句补充会接回原始问题继续生成 answer 或白名单 command，取消补充不会二次调用 provider；全量 `unittest` 465 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.9.0.exe`。
- 2026-05-29：发布 `0.8.0` 可安装测试包，收口桌面配置面板 v1；桌面面板可填写 LLM/Search provider 配置并执行写入、检查和 smoke 测试，写入 API key 时 transcript 与会话历史只显示脱敏文本；全量 `unittest` 462 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.8.0.exe`。
- 2026-05-29：发布 `0.7.0` 可安装测试包，收口连通性诊断 v1；`/llm-smoke` 会在运行中重新读取当前本地 LLM 配置，新增 `/search-smoke [query]` 以不写入最近上下文的方式测试搜索 provider，InnerBrain 支持“测试外脑连接”“测试联网搜索连接”；全量 `unittest` 457 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.7.0.exe`。
- 2026-05-29：发布 `0.6.0` 可安装测试包，收口本地配置写入 v1；`/llm-config-set` 和 `/search-config-set` 可用显式 `key=value` 创建或更新本机 `local.json`，保留未指定字段，错误时不部分写入，响应和日志不泄漏真实 key；全量 `unittest` 452 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.6.0.exe`。
- 2026-05-29：发布 `0.5.0` 可安装测试包，收口本地配置检查 v1；`/llm-config-check` 和 `/search-config-check` 可只读检查本机 `local.json` 与环境变量覆盖，显示 provider、adapter、配置问题和 API key 状态但不发起网络请求、不泄漏真实 key；全量 `unittest` 446 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.5.0.exe`。
- 2026-05-29：发布 `0.4.0` 可安装测试包，收口运行态配置初始化 v1；`/llm-config-init [provider]` 和 `/search-config-init [provider]` 可生成不含真实 API key 的本机 `local.json` 草稿，已有配置不覆盖，支持自然语言“生成外脑配置/生成联网搜索配置”；全量 `unittest` 442 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.4.0.exe`。
- 2026-05-29：发布 `0.3.0` 可安装测试包，收口外脑 provider 配置闭环 v1；`qwen`/`gemini` 可作为 provider alias 写入本地配置并复用 OpenAI-compatible adapter，`/llm-status`、`/llm-enable` 和 `/llm-config-example` 会显示 alias 与实际 adapter；全量 `unittest` 438 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.3.0.exe`。
- 2026-05-29：发布 `0.2.0` 可安装测试包，收口 InnerBrain 多轮澄清 v1；文件路径、编号资料、当前资料标签、标签组+新标签、经验搜索关键词和经验建议关键词可在下一句直接补齐，全量 `unittest` 434 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.2.0.exe`。
- 2026-05-29：发布 `0.1.10` 可安装测试包，扩展 InnerBrain 目录别名和经验内容补槽；“打开那个常用位置”后可回复“目录是项目”，“记住这个经验”后可回复“经验是导入资料后先打标签”，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.10.exe`。
- 2026-05-29：发布 `0.1.9` 可安装测试包，扩展 InnerBrain 编号+标签联合补槽；“给那份资料打标签”后可直接回复“第二份 项目 Python”，编号不会写入标签，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.9.exe`。
- 2026-05-29：发布 `0.1.8` 可安装测试包，扩展 InnerBrain 多轮澄清 query 补槽；“帮我联网查一下”后可直接回复关键词继续搜索或搜索总结，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.8.exe`。
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
- [verification/2026-06/README.md](verification/2026-06/README.md)：2026-06 验证记录索引。
- [verification/2026-05/README.md](verification/2026-05/README.md)：2026-05 验证记录索引。
- [2026-06-01 周索引](verification/2026-06/week-2026-06-01.md)：2026-06-01 至 2026-06-07。
- [2026-05-18 周索引](verification/2026-05/week-2026-05-18.md)：2026-05-18 至 2026-05-24。
- [2026-05-25 周索引](verification/2026-05/week-2026-05-25.md)：2026-05-25 至 2026-05-31。
- [2026-06-01 验证记录](verification/2026-06/2026-06-01.md)：最近一次验证明细。

## 记录规则

- 根目录 `verification.md` 只保留最近摘要和索引。
- 完整验证命令、RED/GREEN 过程和收尾结果写入 `verification/YYYY-MM/YYYY-MM-DD.md`。
- 自然周文件只做索引，不再承载完整明细。
- 每次新增验证记录后同步更新对应月份索引和周索引。
