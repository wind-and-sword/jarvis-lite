# Jarvis Lite 当前项目方案

> 日期：2026-06-10
> 执行者：Codex
> 说明：本文是当前项目方案入口。历史方案版本保存在 `word/plans/`。

## 项目定位

Jarvis Lite 是一个本地优先的个人 PC Agent，目标是让 AI 逐步理解用户的文件、知识库、记忆、最近上下文和桌面工作流，并通过命令行和桌面入口帮助用户完成真实任务。

它当前不是多端平台，也不是纯聊天机器人。当前重点是把 PC 上的本地 Agent 主干做稳，再引入本地内脑增强自然语言理解和决策，让 LLM 作为外脑增强复杂理解、总结、规划和自然表达能力，并把联网搜索作为由 Agent 控制的外部资料获取工具接入。

## 当前路线

```text
PC Agent 稳定
  -> 引入本地内脑 InnerBrain
  -> 接入并打磨 LLM 外脑
  -> 接入 Agent 控制的联网搜索工具
  -> 打磨 PC + 内脑 + 外脑核心闭环
  -> 进入 Jarvis Lite 1.0 验收路线：能听懂自然语言并真实操作常用电脑应用
  -> 再评估手机、手表、车机、AR 眼镜等多端入口
```

## 1.0 验收线

Jarvis Lite 1.0 的正式验收目标是：用户用中文、英文或中英混合自然语言表达常见电脑任务，Jarvis Lite 能理解意图、补齐缺失信息、判断是否具备执行授权、操作目标应用完成任务，并在失败时记录上下文和给出下一步建议。

1.0 P0 能力包括：

- 自然语言主入口：不要求用户记忆 slash command，高频任务由 InnerBrain 本地处理，复杂或低置信输入进入 LLM 外脑 fallback。
- 意图授权层：区分询问、准备、执行和建议，并基于动作风险、授权明确度、缺失槽位、免确认规则和识别置信度决定直接执行、准备后确认、追问或拒绝。
- 自动记忆与配置管家：通过日常对话沉淀应用别名、常用路径、联系人、免确认规则和真实自然语言样本；用户可查看、修改、删除和撤销，但不需要手工维护配置文件。
- 常用应用能力：首批覆盖 Chrome、QQ、微信、IntelliJ IDEA 和 Clash Verge，支持打开、切换、窗口识别、截图、OCR 和第一批低风险工作流。
- 桌面自动化基础：支持应用启动、窗口切换、快捷键、文本输入、点击目标和截图保存，并返回可复盘的执行结果。
- 任务状态与失败复盘：多步骤任务能记录当前步骤、失败位置、屏幕/OCR 上下文、授权依据和下一步建议。

详细验收清单见 [v108：Jarvis Lite 1.0 验收线方案](plans/2026-06-03-v108-jarvis-lite-1-acceptance-plan.md)。

## 当前主干

```text
用户输入
  -> 命令 / 身份 / 本地自然语言意图 / 知识库问答优先
  -> InnerBrain 输出 intent / slots / confidence / missing
  -> 高置信度进入 JarvisAgent；中置信度追问；低置信度进入 LLMRouter
  -> 需要当前互联网资料时由 JarvisAgent 调用 SearchRouter
  -> LLMIntent(command / answer / clarify / no_action)
  -> JarvisAgent
  -> 记录最近路由决策
  -> 长期记忆 / 经验记忆 / 知识库 / 最近上下文
  -> 文件、目录、知识库、日报、更新、桌面入口等工具
  -> 结果反馈 / 下一步建议 / 确认执行
```

## 已完成基础

- 命令行助手和 PySide6 桌面助手入口。
- 长期记忆、经验记忆和个人知识库。
- Markdown、txt、PDF、JSON 聊天记录和资料目录导入。
- 知识库问答、摘要、标签、按标签读取资料组。
- 最近资料、最近文件、最近目录、最近搜索结果、最近建议和批量标签历史。
- InnerBrain 本地内脑：新增结构化 `InnerBrainResult`，包含 `intent`、`slots`、`confidence`、`missing`、`source`、`reason` 和策略；当前已迁移为 seed/runtime 样本分类器优先，并在字符 n-gram Dice 相似度基础上增加包含签名置信度补偿，同时提供固定 seed 评估集和本机 local evaluation JSONL，既有自然语言规则只作为 `legacy_fallback` 迁移期兼容兜底。
- InnerBrain 多轮澄清 v1：当本地内脑已识别 intent 但缺少 `source`、`items`、`path`、`query`、`result_index`、`tags`、`alias`、`experience` 等槽位时，`JarvisAgent` 会保留本轮澄清状态；用户下一句可直接补充文件路径、桌面快捷方式名称、联网搜索关键词、经验搜索/建议关键词、目录别名、经验内容、当前资料标签，或用“第二份 项目 Python”“项目 归档”这类一句式回复补齐组合槽位，Agent 补齐后继续执行原请求，用户也可用“取消补充”等表达取消。
- InnerBrain 可观察与样本闭环：`/inner-brain-status` 查看样本数量、阈值和训练目录；`/inner-brain-eval` 执行固定评估集和本机 `data/inner-brain/evaluation/*.jsonl` 评估样本，失败时给出 `/inner-brain-teach` 或 `/inner-brain-label` 显式修复建议，但不写入训练样本或运行态上下文；`/inner-brain-eval-failed` 复用同一评估集但只显示失败样例和修复建议；`/inner-brain-eval-local` 只执行本机 `local_evaluation` 样本，有样本时会提示切换到待处理失败视图、已处理清单和文件聚焦视图，并按失败数优先列出可聚焦文件名候选及每个文件通过/失败数量，候选行会把同文件总览标注为 `总览：/inner-brain-eval-local-file 文件名`，对仍有待处理失败的文件提示同文件待处理失败入口和按文件待处理报告入口；`/inner-brain-eval-local-failed` 只显示本机待处理失败样本，并按失败数优先展示失败来源文件分组，分组行会提示同文件总览、同文件待处理失败和同文件待处理报告入口，同时展示失败类型汇总、失败期望意图汇总、失败意图混淆汇总、失败文件意图混淆汇总、失败原因汇总、失败意图混淆分组修复建议、失败文件意图混淆分组修复建议和平铺修复建议；本机 evaluation 为空时，两者会提示只写 evaluation、不自动训练的添加入口，并提示补样本命令默认写入 `runtime.jsonl`；`/inner-brain-eval-local-report [文件名]` 可导出本机评估待处理失败报告（Markdown）并汇总失败类型、期望意图、意图混淆方向、文件意图混淆方向、失败原因、意图混淆修复建议和文件意图混淆修复建议，导出反馈会显示待处理失败样本计数，指定文件报告还会显示当前文件样本数，当前筛选文件无样本时会提示补样本命令默认写入 `runtime.jsonl`，并提示继续查看待处理失败样本、按文件聚焦待处理失败和补 evaluation 样本；指定单个文件导出时还会提示当前文件总览、当前文件待处理失败、当前文件已处理样本和全部待处理失败样本，并省略文件意图混淆交叉汇总和文件级修复建议分组，`/inner-brain-eval-local-file 文件名` 有样本时会提示当前文件待处理失败视图、当前文件已处理清单和返回全部本机评估，`/inner-brain-eval-local-file-failed 文件名` 可进一步按本机 JSONL 文件过滤待处理失败样本，并以当前文件总览标签提示同文件全部样本入口，同时提示当前文件已处理样本和全部待处理失败样本，`/inner-brain-eval-local-resolved [文件名]` 可只读查看当前已通过的本机 evaluation 样本，暂无已处理样本时会提示这里只显示已通过样本，并引导查看待处理失败或补充本机 evaluation 样本，指定文件已处理视图会提示当前文件总览；全量已处理视图按待处理失败数优先列出有通过样本的文件候选，候选行提示同文件总览和同文件已处理入口，并为仍有待处理失败的文件提示同文件待处理失败入口；`/inner-brain-eval-add 文本 => /命令`、`/inner-brain-eval-label 文本 => intent [slot=value ...]`、`/inner-brain-eval-add-candidate 编号 => /命令` 和 `/inner-brain-eval-label-candidate 编号 => intent [slot=value ...]` 可把用户确认的真实日志或当前训练候选先写入本机 evaluation 样本，不自动训练，保存反馈会提示复跑本机评估、只看待处理失败、聚焦 `runtime.jsonl` 和按 `runtime.jsonl` 导出待处理失败报告；`/inner-brain-preview 文本` 只预览识别结果，不执行命令或本地动作；`/inner-brain-adopt 文本` 将正确识别结果保存为运行态 JSONL 样本；`/inner-brain-label 文本 => intent [slot=value ...]` 可人工标注 unknown 或误识别样本；`/inner-brain-teach 文本 => /命令` 和“以后我说“文本”就是 /命令”可把用户口语短句教学为已知命令；`/inner-brain-candidates` 会把 fallback/澄清候选写入本地运行态统计，按出现次数优先展示，显式 teach、label 或 adopt 后移除对应候选，写入 evaluation 的候选仍保留，便于先评估再训练。
- 本地自然语言意图层，可处理常见中文表达，包括问候、助手身份/能力询问、最近上下文、最近文件、显式文件读取/导入、显式文件打标签、读取编号资料、查看/导入编号最近文件、查看编号搜索结果、查看/执行编号建议、当前资料/结果打标签、编号资料/搜索结果打标签、标签组读取与批量标签预览、知识库、常用目录打开/整理、最近目录打开/整理、日报、更新、经验记录/搜索/建议、确认/取消执行、联网搜索、联网搜索后续来源处理和明确点名的桌面 `.lnk` 快捷方式删除；InnerBrain 高置信度命中后仍由 `JarvisAgent` 执行。
- LLM 外脑 Router 第一版：provider-neutral 配置、`config/llm.local.json` 本地配置文件、fake provider 测试路径、OpenAI Responses API adapter、OpenAI-compatible 端点、`qwen`/`gemini` provider alias、完整 `/v1/responses` URL 归一化、provider 与 Agent 双层命令白名单、LLM fallback 近期上下文与最近搜索结果、LLM `clarify` 多轮澄清续聊、LLM 澄清状态运行态恢复、LLM 澄清轮数限制和过期清理、`/llm-config-init` 本地配置草稿生成、`/llm-config-set` 本地配置写入、`/llm-config-check` 本地配置只读检查、`/llm-enable` 外脑启用入口、`/llm-context-preview`、`/llm-smoke` 运行时配置验证、token usage 日志、`/llm-status` API key/网络调用诊断、`/llm-usage` 本地汇总和 `/llm-config-example` 配置模板。
- 联网搜索方案已明确为 SearchRouter 工具能力：搜索负责获取当前网页来源和摘要，LLM 外脑负责在 Agent 提供来源后做总结、比较和自然表达；两者互补，均不绕过 `JarvisAgent`。当前 `/search` 会把联网搜索结果写入最近上下文和 LLM context，`/search-summary` 与“联网查一下...并总结”会先搜索再把来源交给 LLM 总结；`/search-open`、`/search-compare`、`/search-save-summary` 和 `/search-import-summary` 负责最近联网搜索的来源查看、来源比较、摘要保存和知识库导入；`/search-config-init` 可生成本地搜索配置草稿，`/search-config-set` 可写入本地搜索配置，`/search-config-check` 可做只读配置检查，`/search-smoke` 可做不写入最近上下文的 provider 连通性测试。
- 应用注册表第一阶段：`/apps` 查看 Chrome、QQ、微信、IntelliJ IDEA 和 Clash Verge 的注册表，`/app-find 名称或别名` 按中文、英文或常用简称匹配已登记应用，支持 `config/apps.local.json` 覆盖路径和追加别名；匹配本身不启动应用。
- 应用启动自动化第一阶段：`/app-launch 应用名称或别名` 启动 AppRegistry 中已登记且有可用路径的应用；当前阶段不自动切换窗口、不点击、不输入、不发送快捷键，不接入自然语言自动启动。
- 只读窗口感知第一阶段：`/windows` 查看当前 Windows 可见顶层窗口、前台窗口、标题、PID、进程名和 AppRegistry 应用匹配结果；当前阶段只做只读观察，不切换窗口、不点击、不输入、不截图。
- 窗口切换自动化第一阶段：`/window-focus 编号或标题/应用名` 切换到当前已存在的可见窗口，按 `/windows` 编号、窗口标题、进程名或 AppRegistry 应用匹配；当前阶段不启动应用、不点击、不输入，不接入自然语言自动切换。
- 屏幕截图保存第一阶段：`/screenshot [文件名]` 保存当前主屏幕 PNG 到 `logs/screenshots/`，返回相对路径和图片尺寸；当前阶段只做截图落盘，不 OCR、不点击、不切换窗口、不输入。
- OCR 图片识别第一阶段：`/ocr-status` 诊断 Tesseract CLI 状态，`/ocr-image 图片路径 [lang=chi_sim+eng]` 识别已存在图片文字；当前阶段不自动截图、不点击、不切换窗口、不输入。
- 截图 OCR 串联第一阶段：`/screen-ocr [文件名] [lang=chi_sim+eng]` 保存当前主屏幕 PNG 后立即对该截图执行 OCR；当前阶段只截图和识别文字，不点击、不切换窗口、不输入、不启动应用。
- 快捷键自动化第一阶段：`/hotkey key1+key2 [key3+key4 ...]` 按顺序发送显式快捷键组合；当前阶段不点击、不输入文本、不切换窗口、不启动应用，不接入自然语言自动执行。
- 鼠标点击自动化第一阶段：`/mouse-click x y [button=left|right|middle]` 执行一次显式坐标点击；当前阶段不做目标识别、不拖动、不切换窗口、不启动应用，不接入自然语言自动点击。
- 文本输入自动化第一阶段：`/type-text 文本` 向当前焦点输入显式文本；当前阶段不做目标识别、不点击、不切换窗口、不启动应用，不接入自然语言自动输入。
- 意图授权层第一阶段：`/authorization-status` 查看直接执行、准备后确认、追问补充和降级策略；显式 slash command 继续直接执行，LLM 外脑建议桌面动作命令时只返回降级说明，不自动触发键鼠、窗口或应用动作。
- 自动记忆与配置管家第一阶段：`/config-manager-status` 和 `/memory-config-status` 只读汇总长期记忆、经验记忆、常用目录、联系人别名、授权规则、偏好、应用本地覆盖、LLM 本地配置、联网搜索本地配置和运行态候选池，并提示现有管理入口；`/config-candidate-add 类型 内容`、`/config-candidates`、`/config-candidate-history`、`/config-candidate-apply 编号`、`/config-candidate-confirm 编号`、`/config-candidate-undo 编号`、`/config-candidate-restore 编号` 和 `/config-candidate-dismiss 编号` 可显式记录、查看、查看历史、固化、确认、撤销、恢复和忽略记忆与配置候选；固化第一阶段只直接写入长期记忆、经验记忆和常用目录，联系人别名候选需显式确认后写入 `config/contacts.local.json`，应用别名候选需显式确认后写入 `config/apps.local.json` 的 `aliases`，授权规则候选需显式确认后写入 `config/authorization.local.json`，偏好候选需显式确认后写入 `config/preferences.local.json`，撤销固化会删除对应别名、规则或偏好并恢复候选为活跃；`/preference-status`、`/preference-enable 编号或ID` 和 `/preference-disable 编号或ID` 可显式查看、启用或停用已保存偏好，`/preference-answer-types`、`/preference-answer-type-enable 类型` 和 `/preference-answer-type-disable 类型` 可显式查看、启用或停用本地回答附注类型开关，状态、预览、草稿、确认结果和确认历史会展示稳定 ID，`/preference-preview [输入文本]` 可只读预览已启用偏好的应用草案，`/preference-apply-draft [输入文本]` 可生成待确认偏好应用草稿，`/preference-apply-confirm [输入文本]` 可确认偏好仅应用到本次显式命令输出并写入运行态确认记录，确认结果会展示按确认 ID 的精确撤销命令，`/preference-apply-history` 可查看最近确认记录，`/preference-apply-undo 编号或ID` 只把确认记录标记为已撤销；最近一条未撤销且仍匹配当前已启用偏好集合的确认记录会进入普通 LLM fallback 上下文和 `/llm-context-preview`，并会以可审计附注追加到本地知识库命中回答和长期记忆兜底回答，本地回答附注会展示回答类型和同一确认 ID 的精确撤销命令，且可通过显式回答类型开关控制知识库与长期记忆两类附注是否展示；撤销确认、停用偏好、删除偏好、启用集合变化或停用对应回答类型后旧附注自动失效；偏好确认上下文和本地回答附注不进入 LLM 命令白名单、SearchRouter、InnerBrain、路由或桌面执行决策，撤销确认记录不会停用偏好、删除偏好或回滚已经展示的输出，API key 只显示已配置/未配置。
- Chrome 低风险工作流第一阶段：`/chrome-workflow-status` 查看边界，`/chrome-open URL` 用 Chrome 打开明确网页，`/chrome-search 关键词` 用 Chrome 打开搜索结果页；当前阶段不读取网页、不点击页面、不输入页面内容、不自动截图或保存资料，不接入自然语言自动执行。
- Clash Verge 低风险工作流第一阶段：`/clash-workflow-status` 查看边界，`/clash-open` 打开代理面板，`/clash-focus` 聚焦已有代理面板窗口；当前阶段不切换节点、不开关系统代理、不修改配置、不点击、不输入，不接入自然语言自动执行。
- QQ/微信准备式工作流第一阶段：`/messaging-workflow-status` 查看边界，`/qq-open` 与 `/wechat-open` 打开应用，`/qq-focus` 与 `/wechat-focus` 聚焦已有窗口，`/qq-prepare-message 联系人 => 消息` 与 `/wechat-prepare-message 联系人 => 消息` 生成未发送消息准备单；当前阶段不查找真实联系人、不点击、不输入、不发送消息，不接入自然语言自动执行。
- IDEA 项目状态第一阶段：`/idea-workflow-status` 查看边界，`/idea-open` 打开 IDEA，`/idea-focus` 聚焦已有 IDEA 窗口，`/idea-open-project 项目路径` 用 IDEA 打开显式项目目录，`/idea-project-status [项目路径]` 只读检查项目目录、`.idea`、`.git` 和常见构建文件；当前阶段不运行测试、不打开终端、不点击、不输入、不编辑项目文件，不接入自然语言自动执行。
- 任务状态与失败复盘第一阶段：`/task-status` 查看当前任务、当前步骤、已完成步骤、最近任务事件和最近失败记录，`/task-start 任务名称`、`/task-step 步骤说明`、`/task-fail 失败原因`、`/task-resume`、`/task-complete` 和 `/task-cancel` 显式记录、恢复、完成或取消任务；当前任务运行中执行普通命令会自动采集输入原话、路由类型、命令详情、结果摘要和依据，并在失败复盘中带上自动采集上下文；失败复盘会记录路由摘要、授权摘要和当前只读窗口摘要；普通失败缺少屏幕/OCR 上下文时会提示显式 `/task-fail-capture 失败原因` 补充截图和 OCR；显式命令事件会反向生成可复制的 `/inner-brain-eval-add 原始输入 => /命令` 样本建议，但不自动写入 evaluation、不训练、不重放命令；当前阶段不自动截图、不自动 OCR、不自动重新执行外部动作，不接入自然语言自动任务编排。
- 任务失败截图 OCR 复盘第一阶段：`/task-fail-capture 失败原因 [lang=chi_sim+eng]` 在显式失败记录时保存截图并尝试 OCR，把截图路径、尺寸、OCR 文本或 OCR 失败诊断写入最近失败复盘；当前阶段不自动重新执行外部动作、不点击、不输入，不接入自然语言自动任务编排。
- 桌面小助手、助手面板、托盘、快捷命令、主题、尺寸、开机启动和更新入口；助手面板已提供外脑和联网搜索配置区，可写入、检查和 smoke 测试 provider 配置，写入 API key 时不会把真实 key 显示到 transcript 或会话历史；面板固定展示 LLM 外脑待补充问题、澄清轮次、取消提示、外脑启用状态、最近一次 LLM 调用结果、最近一条用户输入的路由决策和路由选择依据；桌面面板和托盘快捷命令已提供“内脑候选”入口，桌面面板会根据候选列表同步 teach/label 模板按钮状态、编号上限、候选下拉选择和显式训练目标预填。
- 本地 `unittest` 验证体系。

## 下一阶段

当前已经完成 `0.145.0` 里程碑：

> InnerBrain 样本分类器优先、本机 evaluation 样本与报告闭环、LLM 外脑、Agent 联网搜索、桌面配置面板、桌面 smoke 清理，以及 1.0 路线第一步应用注册表第一阶段、应用启动自动化第一阶段、只读窗口感知第一阶段、窗口切换自动化第一阶段、屏幕截图保存第一阶段、OCR 图片识别第一阶段、截图 OCR 串联第一阶段、快捷键自动化第一阶段、鼠标点击自动化第一阶段、文本输入自动化第一阶段、意图授权层第一阶段、自动记忆与配置管家第一阶段、记忆与配置候选池第一阶段、记忆与配置候选固化第一阶段、记忆与配置候选恢复第一阶段、高风险记忆与配置候选确认草稿第一阶段、联系人别名确认固化与撤销第一阶段、应用别名确认固化与撤销第一阶段、授权规则确认固化与撤销第一阶段、偏好确认固化与撤销第一阶段、偏好显式启用与停用第一阶段、偏好应用预览第一阶段、偏好稳定 ID 与冲突提示第一阶段、偏好应用确认草稿第一阶段、偏好应用确认命令第一阶段、偏好应用确认记录与撤销第一阶段、偏好进入普通回复上下文第一阶段、偏好格式化本地回答第一阶段、偏好应用撤销提示第一阶段、偏好本地回答附注范围第一阶段、偏好本地回答类型开关第一阶段、Chrome 低风险工作流第一阶段、Clash Verge 低风险工作流第一阶段、QQ/微信准备式工作流第一阶段、IDEA 项目状态第一阶段、任务状态与失败复盘第一阶段、任务失败截图 OCR 复盘第一阶段、任务状态自动采集第一阶段、任务执行结果摘要采集第一阶段、任务失败复盘行动建议第一阶段、任务失败复盘样本建议第一阶段和任务失败复盘窗口与授权摘要第一阶段已完成。当前桌面观察能力可启动已登记且有路径的应用、读取窗口、切换已存在的显式窗口、保存截图、识别指定图片文字，并能截图后立即识别当前屏幕文字；快捷键、鼠标点击、文本输入、窗口切换、应用启动、Chrome 打开网页/搜索、Clash Verge 打开/聚焦代理面板、QQ/微信打开/聚焦/生成消息准备单以及 IDEA 打开/聚焦/打开项目只能通过显式 slash command 执行，不做目标识别，不把自然语言自动映射为键鼠执行；Clash Verge 当前不切换节点、不开关系统代理、不修改配置；QQ/微信当前不查找真实联系人、不点击、不输入、不发送消息；IDEA 当前不运行测试、不打开终端、不点击、不输入、不编辑项目文件；任务状态当前可显式记录任务、步骤、失败原因、恢复入口、最近任务事件和失败时截图/OCR 上下文，运行中执行的普通命令会进入自动采集上下文，显式命令返回后会把紧凑结果摘要写回最近匹配任务事件，普通失败会记录当前只读窗口摘要、路由摘要和授权摘要，缺少屏幕/OCR 上下文时会提示显式补充采集入口，显式命令事件可生成可复制的 evaluation 样本建议，但不自动写入、不训练、不自动重新执行外部动作、不点击、不输入；LLM 外脑建议桌面动作命令时会由授权层降级为说明，不自动执行；记忆与配置管家当前支持显式候选记录、查看、查看历史、忽略、低风险固化、候选恢复以及联系人别名/应用别名/授权规则/偏好确认固化与撤销，低风险固化只覆盖长期记忆、经验记忆和常用目录，联系人别名需通过 `/config-candidate-confirm 编号` 写入 `config/contacts.local.json`，应用别名需通过 `/config-candidate-confirm 编号` 写入 `config/apps.local.json` 的 `aliases`，授权规则需通过 `/config-candidate-confirm 编号` 写入 `config/authorization.local.json`，偏好需通过 `/config-candidate-confirm 编号` 写入 `config/preferences.local.json`，可通过 `/config-candidate-undo 编号` 删除对应别名、规则或偏好并恢复候选；已保存偏好可通过 `/preference-status` 查看启用状态和稳定 ID，通过 `/preference-enable 编号或ID` 和 `/preference-disable 编号或ID` 显式启停，通过 `/preference-answer-types` 查看本地回答附注类型开关，通过 `/preference-answer-type-enable 类型` 和 `/preference-answer-type-disable 类型` 显式启停本地知识库回答与长期记忆兜底回答两类附注，通过 `/preference-preview [输入文本]` 只读预览已启用偏好的应用草案，通过 `/preference-apply-draft [输入文本]` 生成待确认偏好应用草稿，通过 `/preference-apply-confirm [输入文本]` 确认偏好仅应用到本次显式命令输出并写入运行态确认记录，确认结果会展示 `撤销确认：/preference-apply-undo prefapp-...`，通过 `/preference-apply-history` 查看最近确认记录，通过 `/preference-apply-undo 编号或ID` 只撤销确认记录；已启用偏好存在明显互斥表达时会只读提示人工确认并拒绝确认应用，最近一条未撤销且仍匹配当前已启用偏好集合的确认记录会进入普通 LLM fallback 上下文和 `/llm-context-preview`，并会以可审计附注追加到本地知识库命中回答和长期记忆兜底回答，本地回答附注会展示回答类型和同一确认 ID 的精确撤销命令，未知回答类型默认不生成附注，停用对应回答类型后该类本地回答不再展示附注；撤销确认、停用偏好、删除偏好或启用集合变化后旧确认自动失效；偏好确认上下文和本地回答附注不进入 LLM 命令白名单、SearchRouter、InnerBrain、路由或桌面执行决策。

后续目标：

- 从 v108 起，下一阶段主线切换为 Jarvis Lite 1.0 验收路线。InnerBrain 本机 evaluation、LLM 外脑、联网搜索和桌面面板继续作为支撑能力维护，不再把报告文案、空状态和局部提示微调作为主线。
- 继续完善已确认偏好的普通回复应用策略、适用范围和更细粒度撤销语义；默认仍不从普通聊天或 LLM 白名单自动写入、启停或确认偏好。
- 旧的真实 `runtime.jsonl` 观察与本机 evaluation 报告能力保留，用于为 1.0 的自然语言理解、失败复盘和用户习惯学习提供样本来源。
- 继续扩展 InnerBrain seed/runtime 样本，把用户真实日志和现有命令能力持续沉淀为 `text -> intent -> slots` 数据。
- 继续扩展 InnerBrain 固定评估集，再评估字符 n-gram、轻量 embedding 相似度或小型分类器，不从零训练通用 LLM。
- 继续扩大缺失槽位的自然语言补全范围，把更多 `missing` 场景接入多轮澄清状态，并沉淀更细的用户纠错样本；`0.2.0` 已收口文件路径、编号资料、当前资料标签、标签组+新标签、经验搜索关键词和经验建议关键词。
- 继续打磨真实 provider 的兼容端点体验、运行态本地配置体验和用量观察能力；`0.3.0` 已让 `qwen`/`gemini` 可作为 provider alias 复用 OpenAI-compatible adapter，`0.4.0` 已支持 `/llm-config-init` 与 `/search-config-init` 生成本机配置草稿，`0.5.0` 已支持 `/llm-config-check` 与 `/search-config-check` 做只读配置检查，`0.6.0` 已支持 `/llm-config-set` 与 `/search-config-set` 用显式 `key=value` 写入本机配置，`0.7.0` 已支持 `/llm-smoke` 重新读取当前本地配置和 `/search-smoke` provider 连通性测试，`0.8.0` 已把写入、检查和 smoke 入口放入桌面配置面板，`0.9.0` 已补齐 LLM `clarify` 的多轮续聊，`0.10.0` 已让 LLM 待澄清状态进入运行态上下文，`0.11.0` 已补齐连续澄清轮数和过期清理边界，`0.12.0` 已把 LLM 待补充状态固定展示到桌面面板，`0.13.0` 已把外脑启用状态和最近调用结果固定展示到桌面面板，`0.14.0` 已把最近路由决策固定展示到桌面面板，`0.15.0` 已把路由选择依据固定展示到同一段路由状态，`0.16.0` 已把最近 5 条路由历史固定展示到同一状态区，`0.17.0` 已提供 `/route-history` 路由历史详情并让 `/recent-context` 展示最近路由摘要，`0.18.0` 已提供 `/inner-brain-candidates` 从 fallback/澄清路由中列出人工训练候选，`0.19.0` 已支持 `/inner-brain-teach-candidate 编号 => /命令` 按编号教学候选，`0.20.0` 已支持 `/inner-brain-label-candidate 编号 => intent [slot=value ...]` 按编号标注候选，`0.21.0` 已让候选按出现次数优先排序，`0.22.0` 已把候选出现次数写入本地运行态统计并在训练后移除对应候选，`0.23.0` 已把“内脑候选”加入桌面面板和托盘直接快捷命令，`0.24.0` 已在桌面面板增加候选编号和 teach/label 模板填充入口，`0.25.0` 已让模板状态和编号上限随最近候选列表同步，`0.26.0` 已把候选列表单条候选绑定到桌面下拉选择，`0.27.0` 已为 teach/label 模板增加常见命令和 intent 的显式目标预填，`0.28.0` 已补齐样本包含签名置信度补偿，`0.29.0` 已提供 `/inner-brain-eval` 固定评估集，`0.30.0` 已支持本机 `data/inner-brain/evaluation/*.jsonl` 评估样本，`0.31.0` 已在评估失败时输出显式训练修复建议，`0.32.0` 已提供 `/inner-brain-eval-failed` 只看失败样本，`0.33.0` 已提供 `/inner-brain-eval-local` 和 `/inner-brain-eval-local-failed` 只看本机样本，`0.34.0` 已提供 `/inner-brain-eval-add` 和 `/inner-brain-eval-label` 显式写入本机评估样本，`0.35.0` 已提供 `/inner-brain-eval-add-candidate` 和 `/inner-brain-eval-label-candidate` 按候选编号写入本机评估样本，`0.36.0` 已提供 `/inner-brain-eval-local-file` 和 `/inner-brain-eval-local-file-failed` 按本机评估 JSONL 文件过滤，`0.67.0` 已在本机指定文件总览中为仍有失败的当前文件追加按文件报告入口，`0.37.0` 已让本机失败评估按来源 JSONL 文件分组，`0.74.0` 已在本机失败视图失败文件分组中追加 `/inner-brain-eval-local-file 当前文件名` 当前文件总览入口，`0.38.0` 已支持 `/inner-brain-eval-local-report [文件名]` 导出本机失败评估 Markdown 报告，`0.39.0` 已在本机失败评估报告中加入失败原因汇总和典型样本，`0.40.0` 已在本机失败评估报告中加入失败类型汇总和典型样本，`0.41.0` 已在本机失败评估报告中加入失败期望意图汇总和典型样本，`0.42.0` 已在本机失败评估报告中加入失败意图混淆汇总和典型样本，`0.43.0` 已在本机失败评估报告中加入失败文件意图混淆交叉汇总和典型样本，`0.44.0` 已在本机失败评估报告中加入失败意图混淆修复建议分组，`0.45.0` 已在本机失败评估报告中加入失败文件意图混淆修复建议分组，`0.46.0` 已在本机 evaluation 样本为空时加入只读添加入口引导，`0.47.0` 已在本机 evaluation 样本保存反馈中加入后续验证提示，`0.69.0` 已在本机 evaluation 样本保存反馈中把报告入口收紧到 `/inner-brain-eval-local-report runtime.jsonl`，`0.48.0` 已在本机失败报告导出反馈中加入后续处理提示，`0.70.0` 已在本机失败报告导出指定文件反馈中追加 `/inner-brain-eval-local-resolved 当前文件名`，`0.71.0` 已在本机失败报告导出指定文件反馈中追加 `/inner-brain-eval-local-file 当前文件名`，`0.79.0` 已在本机失败报告导出指定文件反馈中把同文件全部样本入口标注为当前文件总览，`0.80.0` 已在本机失败报告导出指定文件反馈中把同文件失败入口标注为当前文件待处理失败样本，`0.49.0` 已在本机失败视图中加入导出失败报告提示，`0.50.0` 已在本机失败视图中加入按文件聚焦和返回全部失败样本提示，`0.51.0` 已提供 `/inner-brain-eval-local-resolved [文件名]` 只读查看本机 evaluation 已处理样本，`0.68.0` 已在本机已处理指定文件视图中为仍有待处理失败的当前文件追加按文件报告入口，`0.73.0` 已在本机已处理指定文件视图中追加 `/inner-brain-eval-local-file 当前文件名` 当前文件总览入口，`0.78.0` 已在本机已处理指定文件视图中把同文件全部样本入口标注为当前文件总览，`0.52.0` 已在本机评估全量视图中加入失败/已处理/文件聚焦后续处理提示，`0.53.0` 已在本机评估全量视图中列出可聚焦文件名候选，`0.54.0` 已在本机评估全量视图的文件候选行中追加通过/失败数量，`0.55.0` 已让本机评估全量视图的文件候选按失败数量优先排序，`0.62.0` 已在本机评估全量视图文件候选中为仍有失败的文件追加同文件失败入口，`0.65.0` 已在本机评估全量视图文件候选中为仍有失败的文件追加按文件报告入口，`0.76.0` 已在本机评估全量视图文件候选中把同文件全部样本入口标注为总览入口，`0.63.0` 已在本机失败视图的失败文件分组中为每个失败文件追加同文件失败入口，`0.64.0` 已在本机失败视图的失败文件分组中为每个失败文件追加按文件报告入口，`0.56.0` 已让本机失败视图的失败文件分组按失败数量优先排序，`0.57.0` 已在本机文件失败视图中提示查看当前文件已处理样本，`0.72.0` 已在本机文件失败视图中追加 `/inner-brain-eval-local-file 当前文件名` 当前文件总览入口，`0.77.0` 已在本机文件失败视图中把同文件全部样本入口标注为当前文件总览，`0.58.0` 已在本机已处理视图中列出可查看文件候选，`0.59.0` 已在本机已处理视图文件候选行中追加已处理/待处理失败数量，`0.60.0` 已让本机已处理视图文件候选按待处理失败数量优先排序，`0.61.0` 已在本机已处理视图文件候选中为仍有待处理失败的文件追加同文件失败入口，`0.66.0` 已在本机已处理视图文件候选中为仍有待处理失败的文件追加按文件报告入口，`0.75.0` 已在本机已处理视图文件候选中追加 `/inner-brain-eval-local-file 当前文件名` 当前文件总览入口，`0.88.0` 已把仍有失败的本机文件候选报告入口标注为待处理报告，`0.89.0` 已把本机报告导出反馈、运行日志和 Markdown H1 标题统一为本机评估待处理失败报告，`0.90.0` 已把本机失败帮助和运行日志收紧为待处理失败标签，`0.91.0` 已把本机报告导出反馈计数标注为待处理失败样本，`0.92.0` 已把本机全量失败视图和全量报告导出反馈中的按文件聚焦入口标注为待处理失败，`0.93.0` 已把全量评估运行日志标注为固定与本机评估集，`0.94.0` 已把全量评估输出正文标注为固定评估集和本机评估集，`0.95.0` 已把全量评估帮助文案标注为固定与本机评估集，`0.96.0` 已把本机报告处理边界提示标注为待处理失败样本，`0.97.0` 已把公开文档里的本机失败视图标注为待处理失败样本，`0.98.0` 已在本机报告导出指定文件反馈中追加当前文件样本计数，`0.99.0` 已在空筛选文件报告反馈中提示补样本命令默认写入 `runtime.jsonl`，`0.100.0` 已在空本机 evaluation 评估视图中提示补样本命令默认写入 `runtime.jsonl`，`0.101.0` 已在本机已处理空视图中提示只显示已通过样本并引导查看待处理失败或补充本机 evaluation 样本，`0.102.0` 已把该提示同步到 README 顶部 InnerBrain 样本闭环概要，`0.103.0` 已把该提示同步到 PROJECT-PLAN 主干描述。
- 如果兼容端点无法覆盖真实使用，再评估 Gemini 和 Qwen 原生 provider adapter。
- 继续打磨 LLM 结构化意图提示词、命令参数澄清、provider 错误可读化和失败兜底。
- 让 LLM 生成更稳定的命令建议、资料总结、任务拆解、澄清问题和澄清后的最终回答。
- 扩展联网搜索结果后续动作，例如按编号打开来源、保存摘要、对比多个来源和沉淀为知识库资料。
- 持续把用户真实日志里的自然语言缺口沉淀为内脑训练样本和回归测试，再交给 LLM 处理更开放的问题。
- 继续由 `JarvisAgent` 承接工具调用、上下文更新和结果反馈。

## 暂缓方向

以下方向在 PC + 内脑 + LLM 核心闭环稳定前暂缓：

- 手机端。
- 手表健康数据。
- 车机入口。
- AR 眼镜入口。
- 跨设备同步。

## 方案版本

- [v1：整体方案与路线图](plans/2026-05-18-v1-overall-plan.md)
- [v2：个人设备级 Agent 融合方案](plans/2026-05-22-v2-personal-device-agent-plan.md)
- [v3：PC Agent 与 LLM 外脑优先方案](plans/2026-05-27-v3-pc-agent-llm-first-plan.md)
- [v4：内脑与外脑双脑架构方案](plans/2026-05-28-v4-inner-brain-llm-dual-brain-plan.md)
- [v5：Agent 联网搜索与 LLM 外脑互补方案](plans/2026-05-28-v5-agent-web-search-llm-complement-plan.md)
- [v6：InnerBrain 样本分类器优先方案](plans/2026-05-28-v6-inner-brain-classifier-first-plan.md)
- [v7：外脑 Provider 配置闭环方案](plans/2026-05-29-v7-llm-provider-config-closure-plan.md)
- [v8：运行态配置初始化方案](plans/2026-05-29-v8-runtime-config-init-plan.md)
- [v9：运行态配置检查方案](plans/2026-05-29-v9-runtime-config-check-plan.md)
- [v10：运行态配置写入方案](plans/2026-05-29-v10-runtime-config-set-plan.md)
- [v11：连通性诊断方案](plans/2026-05-29-v11-smoke-diagnostics-plan.md)
- [v12：桌面配置面板方案](plans/2026-05-29-v12-desktop-config-panel-plan.md)
- [v13：LLM 外脑多轮澄清方案](plans/2026-05-29-v13-llm-clarification-plan.md)
- [v14：LLM 外脑澄清状态持久化方案](plans/2026-05-29-v14-llm-clarification-runtime-plan.md)
- [v15：LLM 外脑澄清轮数与过期策略](plans/2026-05-29-v15-llm-clarification-guard-plan.md)
- [v16：桌面外脑待补充状态方案](plans/2026-05-29-v16-desktop-llm-pending-status-plan.md)
- [v17：桌面外脑运行状态方案](plans/2026-05-29-v17-desktop-llm-activity-status-plan.md)
- [v18：最近路由决策状态方案](plans/2026-05-29-v18-route-decision-status-plan.md)
- [v19：路由决策解释详情方案](plans/2026-05-29-v19-route-decision-explanation-plan.md)
- [v20：最近路由历史方案](plans/2026-05-29-v20-route-history-plan.md)
- [v21：路由历史详情方案](plans/2026-05-29-v21-route-history-detail-plan.md)
- [v22：InnerBrain 训练候选方案](plans/2026-05-29-v22-inner-brain-candidates-plan.md)
- [v23：InnerBrain 候选按编号教学方案](plans/2026-06-01-v23-inner-brain-teach-candidate-plan.md)
- [v24：InnerBrain 候选按编号标注方案](plans/2026-06-01-v24-inner-brain-label-candidate-plan.md)
- [v25：InnerBrain 候选频次排序方案](plans/2026-06-01-v25-inner-brain-candidate-frequency-plan.md)
- [v26：InnerBrain 候选运行态统计方案](plans/2026-06-01-v26-inner-brain-candidate-runtime-stats-plan.md)
- [v27：桌面内脑候选快捷入口方案](plans/2026-06-01-v27-desktop-inner-brain-candidate-shortcut-plan.md)
- [v28：桌面候选训练模板填充方案](plans/2026-06-01-v28-desktop-inner-brain-candidate-template-plan.md)
- [v29：桌面候选模板状态同步方案](plans/2026-06-01-v29-desktop-inner-brain-candidate-template-sync-plan.md)
- [v30：桌面候选选择绑定方案](plans/2026-06-01-v30-desktop-inner-brain-candidate-selection-plan.md)
- [v31：桌面候选目标预填方案](plans/2026-06-01-v31-desktop-inner-brain-candidate-target-prefill-plan.md)
- [v32：InnerBrain 包含签名置信度补偿方案](plans/2026-06-01-v32-inner-brain-contained-signature-boost-plan.md)
- [v33：InnerBrain 固定评估集方案](plans/2026-06-01-v33-inner-brain-seed-evaluation-plan.md)
- [v34：InnerBrain 本机评估集扩展方案](plans/2026-06-01-v34-inner-brain-local-evaluation-plan.md)
- [v35：InnerBrain 评估失败修复建议方案](plans/2026-06-01-v35-inner-brain-evaluation-fix-suggestion-plan.md)
- [v36：InnerBrain 评估失败过滤视图方案](plans/2026-06-01-v36-inner-brain-evaluation-failures-only-plan.md)
- [v37：InnerBrain 本机评估过滤视图方案](plans/2026-06-01-v37-inner-brain-local-evaluation-view-plan.md)
- [v38：InnerBrain 本机评估样本显式写入方案](plans/2026-06-01-v38-inner-brain-local-evaluation-save-plan.md)
- [v39：InnerBrain 候选编号写入本机评估样本方案](plans/2026-06-01-v39-inner-brain-candidate-evaluation-save-plan.md)
- [v40：InnerBrain 本机评估 JSONL 文件过滤方案](plans/2026-06-02-v40-inner-brain-local-evaluation-file-filter-plan.md)
- [v41：InnerBrain 本机评估失败按 JSONL 文件分组方案](plans/2026-06-02-v41-inner-brain-local-evaluation-failure-group-plan.md)
- [v42：InnerBrain 本机评估失败报告导出方案](plans/2026-06-02-v42-inner-brain-local-evaluation-report-export-plan.md)
- [v43：InnerBrain 本机评估失败原因汇总方案](plans/2026-06-02-v43-inner-brain-failure-reason-summary-plan.md)
- [v44：InnerBrain 本机评估失败类型汇总方案](plans/2026-06-02-v44-inner-brain-failure-type-summary-plan.md)
- [v45：InnerBrain 本机评估失败期望意图汇总方案](plans/2026-06-02-v45-inner-brain-failure-expected-intent-summary-plan.md)
- [v46：InnerBrain 本机评估失败意图混淆汇总方案](plans/2026-06-02-v46-inner-brain-intent-confusion-summary-plan.md)
- [v47：InnerBrain 本机评估失败文件意图混淆汇总方案](plans/2026-06-02-v47-inner-brain-file-intent-confusion-summary-plan.md)
- [v48：InnerBrain 本机评估失败意图混淆修复建议分组方案](plans/2026-06-02-v48-inner-brain-intent-confusion-fix-suggestions-plan.md)
- [v49：InnerBrain 本机失败评估文件意图混淆修复建议分组方案](plans/2026-06-02-v49-inner-brain-file-intent-confusion-fix-suggestions-plan.md)
- [v50：InnerBrain 本机评估空样本引导方案](plans/2026-06-02-v50-inner-brain-local-evaluation-empty-guidance-plan.md)
- [v51：InnerBrain 本机评估样本保存后续验证提示方案](plans/2026-06-02-v51-inner-brain-local-evaluation-save-next-steps-plan.md)
- [v52：InnerBrain 本机失败评估报告导出后续处理提示方案](plans/2026-06-02-v52-inner-brain-report-export-next-steps-plan.md)
- [v53：InnerBrain 本机失败视图导出报告提示方案](plans/2026-06-02-v53-inner-brain-local-failed-report-hint-plan.md)
- [v54：InnerBrain 本机失败视图文件聚焦提示方案](plans/2026-06-02-v54-inner-brain-local-failed-file-focus-hint-plan.md)
- [v55：InnerBrain 本机 evaluation 已处理样本只读清单方案](plans/2026-06-02-v55-inner-brain-local-resolved-list-plan.md)
- [v56：InnerBrain 本机评估全量视图后续处理提示方案](plans/2026-06-02-v56-inner-brain-local-eval-next-steps-plan.md)
- [v57：InnerBrain 本机评估全量视图文件名候选提示方案](plans/2026-06-02-v57-inner-brain-local-eval-file-suggestions-plan.md)
- [v58：InnerBrain 本机评估全量视图文件候选状态摘要方案](plans/2026-06-02-v58-inner-brain-local-eval-file-status-plan.md)
- [v59：InnerBrain 本机评估全量视图文件候选失败优先排序方案](plans/2026-06-02-v59-inner-brain-local-eval-file-priority-plan.md)
- [v60：InnerBrain 本机失败视图失败文件汇总排序方案](plans/2026-06-02-v60-inner-brain-local-failed-file-priority-plan.md)
- [v61：InnerBrain 本机文件失败视图已处理入口方案](plans/2026-06-02-v61-inner-brain-local-file-failed-resolved-hint-plan.md)
- [v62：InnerBrain 本机已处理视图文件候选提示方案](plans/2026-06-02-v62-inner-brain-local-resolved-file-suggestions-plan.md)
- [v63：InnerBrain 本机已处理视图文件候选状态摘要方案](plans/2026-06-02-v63-inner-brain-local-resolved-file-status-plan.md)
- [v64：InnerBrain 本机已处理视图文件候选待处理优先排序方案](plans/2026-06-02-v64-inner-brain-local-resolved-file-priority-plan.md)
- [v65：InnerBrain 本机已处理视图文件候选待处理入口方案](plans/2026-06-02-v65-inner-brain-local-resolved-file-failed-shortcut-plan.md)
- [v66：InnerBrain 本机评估全量视图文件候选待处理入口方案](plans/2026-06-02-v66-inner-brain-local-eval-file-failed-shortcut-plan.md)
- [v67：InnerBrain 本机失败视图失败文件分组聚焦入口方案](plans/2026-06-02-v67-inner-brain-local-failed-file-shortcut-plan.md)
- [v68：InnerBrain 本机失败视图失败文件分组报告入口方案](plans/2026-06-02-v68-inner-brain-local-failed-file-report-shortcut-plan.md)
- [v69：InnerBrain 本机评估全量视图文件候选报告入口方案](plans/2026-06-02-v69-inner-brain-local-eval-file-report-shortcut-plan.md)
- [v70：InnerBrain 本机已处理视图文件候选报告入口方案](plans/2026-06-02-v70-inner-brain-local-resolved-file-report-shortcut-plan.md)
- [v71：InnerBrain 本机文件视图报告入口方案](plans/2026-06-02-v71-inner-brain-local-file-report-shortcut-plan.md)
- [v72：InnerBrain 本机已处理指定文件视图报告入口方案](plans/2026-06-02-v72-inner-brain-local-resolved-filtered-report-shortcut-plan.md)
- [v73：InnerBrain 本机 evaluation 保存反馈按文件报告入口方案](plans/2026-06-03-v73-inner-brain-eval-save-file-report-shortcut-plan.md)
- [v74：InnerBrain 本机失败报告导出反馈当前文件已处理入口方案](plans/2026-06-03-v74-inner-brain-report-export-resolved-shortcut-plan.md)
- [v75：InnerBrain 本机失败报告导出反馈当前文件总览入口方案](plans/2026-06-03-v75-inner-brain-report-export-file-overview-shortcut-plan.md)
- [v76：InnerBrain 本机文件失败视图当前文件总览入口方案](plans/2026-06-03-v76-inner-brain-local-file-failed-overview-shortcut-plan.md)
- [v77：InnerBrain 本机已处理指定文件视图当前文件总览入口方案](plans/2026-06-03-v77-inner-brain-local-resolved-overview-shortcut-plan.md)
- [v78：InnerBrain 本机失败视图失败文件分组当前文件总览入口方案](plans/2026-06-03-v78-inner-brain-local-failed-file-overview-shortcut-plan.md)
- [v79：InnerBrain 本机已处理视图文件候选当前文件总览入口方案](plans/2026-06-03-v79-inner-brain-local-resolved-file-overview-shortcut-plan.md)
- [v80：InnerBrain 本机评估全量视图文件候选总览标签方案](plans/2026-06-03-v80-inner-brain-local-file-candidate-overview-label-plan.md)
- [v81：InnerBrain 本机文件失败视图当前文件总览标签方案](plans/2026-06-03-v81-inner-brain-local-file-failed-overview-label-plan.md)
- [v82：InnerBrain 本机已处理指定文件视图当前文件总览标签方案](plans/2026-06-03-v82-inner-brain-local-resolved-overview-label-plan.md)
- [v83：InnerBrain 本机失败报告导出反馈当前文件总览标签方案](plans/2026-06-03-v83-inner-brain-report-export-overview-label-plan.md)
- [v84：InnerBrain 本机失败报告导出反馈当前文件待处理失败标签方案](plans/2026-06-03-v84-inner-brain-report-export-file-failed-label-plan.md)
- [v85：InnerBrain 本机当前文件反馈全部待处理失败标签方案](plans/2026-06-03-v85-inner-brain-report-export-all-pending-label-plan.md)
- [v86：InnerBrain 本机失败报告导出反馈全量待处理失败标签方案](plans/2026-06-03-v86-inner-brain-report-export-pending-label-plan.md)
- [v87：InnerBrain 本机文件失败视图全部待处理失败报告标签方案](plans/2026-06-03-v87-inner-brain-local-file-failed-all-report-label-plan.md)
- [v88：InnerBrain 本机失败视图待处理失败报告标签方案](plans/2026-06-03-v88-inner-brain-local-failed-report-label-plan.md)
- [v89：InnerBrain 本机失败视图按文件待处理失败报告标签方案](plans/2026-06-03-v89-inner-brain-local-failed-file-report-label-plan.md)
- [v90：InnerBrain 本机当前文件待处理失败报告标签方案](plans/2026-06-03-v90-inner-brain-current-file-report-label-plan.md)
- [v91：InnerBrain 本机评估样本保存反馈待处理失败标签方案](plans/2026-06-03-v91-inner-brain-eval-save-pending-label-plan.md)
- [v92：InnerBrain 本机文件候选待处理报告标签方案](plans/2026-06-03-v92-inner-brain-file-candidate-report-label-plan.md)
- [v93：InnerBrain 本机报告导出待处理失败标题方案](plans/2026-06-03-v93-inner-brain-report-export-pending-title-plan.md)
- [v94：InnerBrain 本机失败帮助待处理标签方案](plans/2026-06-03-v94-inner-brain-help-pending-label-plan.md)
- [v95：InnerBrain 本机报告导出反馈待处理失败计数标签方案](plans/2026-06-03-v95-inner-brain-report-count-pending-label-plan.md)
- [v96：InnerBrain 本机全量反馈按文件聚焦待处理失败标签方案](plans/2026-06-03-v96-inner-brain-file-focus-pending-label-plan.md)
- [v97：InnerBrain 全量评估运行日志固定与本机评估集标签方案](plans/2026-06-03-v97-inner-brain-full-eval-log-label-plan.md)
- [v98：InnerBrain 全量评估输出固定与本机评估集标签方案](plans/2026-06-03-v98-inner-brain-full-eval-output-label-plan.md)
- [v99：InnerBrain 全量评估帮助固定与本机评估集标签方案](plans/2026-06-03-v99-inner-brain-full-eval-help-label-plan.md)
- [v100：InnerBrain 本机报告处理边界待处理失败标签方案](plans/2026-06-03-v100-inner-brain-report-boundary-pending-label-plan.md)
- [v101：InnerBrain 本机失败视图文档待处理失败标签方案](plans/2026-06-03-v101-inner-brain-doc-pending-label-plan.md)
- [v102：InnerBrain 本机报告指定文件样本计数提示方案](plans/2026-06-03-v102-inner-brain-report-file-sample-count-plan.md)
- [v103：InnerBrain 本机报告空筛选文件补样本写入提示方案](plans/2026-06-03-v103-inner-brain-report-empty-filter-guidance-plan.md)
- [v104：InnerBrain 本机空评估视图补样本写入提示方案](plans/2026-06-03-v104-inner-brain-empty-evaluation-runtime-guidance-plan.md)
- [v105：InnerBrain 本机已处理空视图行动提示方案](plans/2026-06-03-v105-inner-brain-resolved-empty-guidance-plan.md)
- [v106：InnerBrain README 已处理空视图概要同步方案](plans/2026-06-03-v106-inner-brain-readme-resolved-empty-summary-plan.md)
- [v107：InnerBrain PROJECT-PLAN 已处理空视图主干同步方案](plans/2026-06-03-v107-inner-brain-project-plan-resolved-empty-summary-plan.md)
- [v108：Jarvis Lite 1.0 验收线方案](plans/2026-06-03-v108-jarvis-lite-1-acceptance-plan.md)
- [v109：应用注册表第一阶段实施计划](plans/2026-06-03-v109-app-registry-plan.md)
- [v110：只读窗口感知第一阶段实施计划](plans/2026-06-03-v110-window-state-plan.md)
- [v111：屏幕截图保存第一阶段实施计划](plans/2026-06-03-v111-screen-capture-plan.md)
- [v112：OCR 图片识别第一阶段实施计划](plans/2026-06-03-v112-ocr-image-plan.md)
- [v113：截图 OCR 串联实施计划](plans/2026-06-03-v113-screen-ocr-plan.md)
- [v114：快捷键自动化第一阶段实施计划](plans/2026-06-03-v114-hotkey-automation-plan.md)
- [v115：鼠标点击自动化第一阶段实施计划](plans/2026-06-03-v115-mouse-click-automation-plan.md)
- [v116：文本输入自动化第一阶段实施计划](plans/2026-06-03-v116-text-input-automation-plan.md)
- [v117：窗口切换自动化第一阶段实施计划](plans/2026-06-03-v117-window-focus-automation-plan.md)
- [v118：应用启动自动化第一阶段实施计划](plans/2026-06-03-v118-app-launch-automation-plan.md)
- [v119：意图授权层第一阶段实施计划](plans/2026-06-03-v119-intent-authorization-layer-plan.md)
- [v120：自动记忆与配置管家第一阶段实施计划](plans/2026-06-03-v120-memory-config-manager-status-plan.md)
- [v121：Chrome 低风险工作流第一阶段实施计划](plans/2026-06-03-v121-chrome-workflow-plan.md)
- [v122：Clash Verge 低风险工作流第一阶段实施计划](plans/2026-06-03-v122-clash-workflow-plan.md)
- [v123：QQ/微信准备式工作流第一阶段实施计划](plans/2026-06-03-v123-messaging-workflow-plan.md)
- [v124：IDEA 项目状态第一阶段实施计划](plans/2026-06-03-v124-idea-workflow-plan.md)
- [v125：任务状态与失败复盘第一阶段实施计划](plans/2026-06-03-v125-task-state-failure-replay-plan.md)
- [v126：任务失败截图 OCR 复盘第一阶段实施计划](plans/2026-06-03-v126-task-failure-screen-ocr-plan.md)
- [v127：记忆与配置候选池第一阶段实施计划](plans/2026-06-03-v127-memory-config-candidates-plan.md)
- [v128：记忆与配置候选固化第一阶段实施计划](plans/2026-06-03-v128-memory-config-candidate-apply-plan.md)
- [v129：任务状态自动采集第一阶段实施计划](plans/2026-06-03-v129-task-state-auto-capture-plan.md)
- [v130：任务执行结果摘要采集第一阶段实施计划](plans/2026-06-03-v130-task-event-result-summary-plan.md)
- [v131：任务失败复盘行动建议第一阶段实施计划](plans/2026-06-03-v131-task-failure-next-step-plan.md)
- [v132：任务失败复盘样本建议第一阶段实施计划](plans/2026-06-03-v132-task-failure-eval-suggestion-plan.md)
- [v133：记忆与配置候选恢复第一阶段实施计划](plans/2026-06-03-v133-memory-config-candidate-restore-plan.md)
- [v134：高风险记忆与配置候选确认草稿第一阶段实施计划](plans/2026-06-03-v134-memory-config-high-risk-candidate-draft-plan.md)
- [v135：任务失败复盘窗口与授权摘要第一阶段实施计划](plans/2026-06-04-v135-task-failure-window-context-plan.md)
- [v136：联系人别名确认固化与撤销第一阶段实施计划](plans/2026-06-04-v136-contact-alias-confirmation-plan.md)
- [v137：应用别名确认固化与撤销第一阶段实施计划](plans/2026-06-04-v137-app-alias-confirmation-plan.md)
- [v138：授权规则确认固化与撤销第一阶段实施计划](plans/2026-06-05-v138-authorization-rule-confirmation-plan.md)
- [v139：偏好确认固化与撤销第一阶段实施计划](plans/2026-06-05-v139-preference-confirmation-plan.md)
- [v140：偏好显式启用与停用第一阶段实施计划](plans/2026-06-05-v140-preference-enable-plan.md)
- [v141：偏好应用预览第一阶段实施计划](plans/2026-06-05-v141-preference-preview-plan.md)
- [v142：偏好稳定 ID 与冲突提示第一阶段实施计划](plans/2026-06-05-v142-preference-id-conflict-plan.md)
- [v143：偏好应用确认草稿第一阶段实施计划](plans/2026-06-05-v143-preference-apply-confirmation-plan.md)
- [v144：偏好应用确认命令第一阶段实施计划](plans/2026-06-05-v144-preference-apply-confirm-plan.md)
- [v145：偏好应用确认记录与撤销第一阶段实施计划](plans/2026-06-09-v145-preference-apply-audit-plan.md)
- [v146：偏好进入普通回复上下文第一阶段实施计划](plans/2026-06-09-v146-preference-reply-context-plan.md)
- [v147：偏好格式化本地回答第一阶段实施计划](plans/2026-06-09-v147-preference-local-answer-format-plan.md)
- [v148：偏好应用撤销提示第一阶段实施计划](plans/2026-06-09-v148-preference-undo-hints-plan.md)
- [v149：偏好本地回答附注范围第一阶段实施计划](plans/2026-06-09-v149-preference-local-answer-scope-plan.md)
- [v150：偏好本地回答类型开关第一阶段实施计划](plans/2026-06-10-v150-preference-local-answer-type-settings-plan.md)
