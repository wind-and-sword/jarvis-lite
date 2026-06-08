# v6 多轮澄清目录别名与经验内容补槽执行计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

把目录别名和经验内容纳入可测试的多轮澄清体验，让用户不需要写命令，也不需要重新说完整句子。

## 范围

- `directory.open_alias missing=alias`：用户可下一句回复“目录是项目”，Agent 清理为 `alias=项目` 并继续执行打开目录请求。
- `experience.record missing=experience`：用户可下一句回复“经验是导入资料后先打标签”，Agent 清理为 `experience=导入资料后先打标签` 并继续写入经验记忆。
- 澄清提示把 `alias` 展示为“目录别名”，把 `experience` 展示为“经验内容”，并给出一句式示例。
- 不新增执行层，补齐后仍复用现有 `NaturalLanguageIntent` 和 `JarvisAgent` 执行链路。

## 执行

1. 写 RED 测试：runtime 样本缺 `alias` 和缺 `experience`，验证澄清提示和下一句补齐执行。
2. 扩展 `_normalize_clarification_value()`，清理“目录是”“目录别名是”“经验是”“经验内容是”等补充前缀。
3. 扩展 Agent 澄清提示和缺槽中文标签。
4. 将版本提升到 `0.1.10`，更新 README 和正式文档。
5. 运行目标测试、回归测试、全量测试、源码 smoke、打包 smoke、静态检查和敏感信息扫描。
6. 生成 `JarvisLiteSetup-0.1.10.exe` 并本地提交，不 push。
