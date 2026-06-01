# Jarvis Lite v32：InnerBrain 包含签名置信度补偿方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v31 桌面候选目标预填，明确 `0.28.0` 的样本分类器相似度增强。

## 目标

`0.28.0` 增强 InnerBrain 样本分类器：当用户长句中完整包含某个已知样本签名时，适度提升该样本的相似度置信度，让“帮我看一下知识库状态”这类多了礼貌词和上下文词的表达可以直接命中 `knowledge.status`。

## 边界

- 不新增自然语言意图正则，不通过模板枚举用户所有说法。
- 不改变 seed/runtime 样本格式。
- 不改变 `HIGH_CONFIDENCE`、`MEDIUM_CONFIDENCE` 阈值。
- 只在样本相似度层做补偿；仍由已知样本 intent 和槽位抽取决定后续行为。
- 过短样本不参与包含补偿，避免“早”“hi”等短词误吞长句。

## 实现要点

- `_sample_similarity()` 保留原有 Dice 相似度。
- 新增 `_contained_sample_signature_similarity()`：当 `sample_text` 长度不少于 4 且被 `prompt_text` 包含时，根据覆盖比例返回一个受上限约束的补偿分数。
- 最终相似度取 Dice 分数和包含补偿分数的最大值。
- 该补偿只依赖样本签名，不解析具体意图短语，因此属于分类器评分增强而不是新意图规则。

## 验证

- RED：新增 InnerBrain 测试先失败，证明“帮我看一下知识库状态”当前只到中置信澄清，版本也未提升。
- GREEN：目标测试通过。
- 回归：InnerBrain 专项、相邻 Agent/LLM/桌面/Conversation 回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 继续观察真实日志里“核心样本签名 + 礼貌/上下文前后缀”的表达，必要时评估更系统的字符 n-gram 权重或轻量 embedding。
- 若出现误吞，应优先加回归样例约束补偿条件，而不是降低整体阈值。
