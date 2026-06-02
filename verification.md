# 验证记录

> 日期：2026-06-03
> 执行者：Codex
> 说明：根目录只作为验证记录入口，不再长期追加完整命令和输出。

## 最近摘要

- 2026-06-03：发布 `0.84.0` 可安装测试包，收口 InnerBrain 本机失败视图待处理失败报告标签；`/inner-brain-eval-local-failed` 未指定文件时会用 `导出待处理失败报告：/inner-brain-eval-local-report` 提示导出全量待处理失败报告；同时修复桌面 smoke 清理，打包后 `JarvisLite.exe --smoke` 在 2 秒检查点无残留进程；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.84.0.exe`。
- 2026-06-03：发布 `0.83.0` 可安装测试包，收口 InnerBrain 本机文件失败视图全部待处理失败报告标签；`/inner-brain-eval-local-file-failed 文件名` 的后续处理会用 `导出全部待处理失败报告：/inner-brain-eval-local-report` 提示导出全量待处理失败报告；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.83.0.exe`。
- 2026-06-03：发布 `0.82.0` 可安装测试包，收口 InnerBrain 本机失败报告导出反馈全量待处理失败标签；`/inner-brain-eval-local-report` 未指定文件时会用 `查看待处理失败样本：/inner-brain-eval-local-failed` 提示回到全量待处理失败视图；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.82.0.exe`。
- 2026-06-03：发布 `0.81.0` 可安装测试包，收口 InnerBrain 本机当前文件反馈全部待处理失败标签；`/inner-brain-eval-local-file-failed 文件名` 和 `/inner-brain-eval-local-report 文件名` 的后续处理会用 `查看全部待处理失败样本：/inner-brain-eval-local-failed` 提示回到全量待处理失败视图；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.81.0.exe`。
- 2026-06-03：发布 `0.80.0` 可安装测试包，收口 InnerBrain 本机失败报告导出反馈当前文件待处理失败标签；`/inner-brain-eval-local-report 文件名` 的导出反馈会用 `查看当前文件待处理失败样本：/inner-brain-eval-local-file-failed 当前文件名` 提示进入同文件失败样本；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.80.0.exe`。
- 2026-06-03：发布 `0.79.0` 可安装测试包，收口 InnerBrain 本机失败报告导出反馈当前文件总览标签；`/inner-brain-eval-local-report 文件名` 的导出反馈会用 `当前文件总览：/inner-brain-eval-local-file 当前文件名` 提示回到同文件全部样本；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.79.0.exe`。
- 2026-06-03：发布 `0.78.0` 可安装测试包，收口 InnerBrain 本机已处理指定文件视图当前文件总览标签；`/inner-brain-eval-local-resolved 文件名` 的后续处理会用 `当前文件总览：/inner-brain-eval-local-file 当前文件名` 提示回到同文件全部样本；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.78.0.exe`。
- 2026-06-03：发布 `0.77.0` 可安装测试包，收口 InnerBrain 本机文件失败视图当前文件总览标签；`/inner-brain-eval-local-file-failed 文件名` 的后续处理会用 `当前文件总览：/inner-brain-eval-local-file 当前文件名` 提示回到同文件全部样本；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.77.0.exe`。
- 2026-06-03：发布 `0.76.0` 可安装测试包，收口 InnerBrain 本机评估全量视图文件候选总览标签；`/inner-brain-eval-local` 的 `可聚焦文件：` 候选会把同文件总览入口标注为 `总览：/inner-brain-eval-local-file 当前文件名`，有失败时继续提示待处理和报告入口；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.76.0.exe`。
- 2026-06-03：发布 `0.75.0` 可安装测试包，收口 InnerBrain 本机已处理视图文件候选当前文件总览入口；`/inner-brain-eval-local-resolved` 的 `可查看文件：` 候选会提示 `/inner-brain-eval-local-file 当前文件名` 和 `/inner-brain-eval-local-resolved 当前文件名`，有待处理失败时继续提示失败和报告入口；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.75.0.exe`。
- 2026-06-03：发布 `0.74.0` 可安装测试包，收口 InnerBrain 本机失败视图失败文件分组当前文件总览入口；`/inner-brain-eval-local-failed` 的 `失败文件：` 分组会为每个失败文件提示 `/inner-brain-eval-local-file 当前文件名`，并继续保留同文件待处理失败入口和按文件报告入口；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.74.0.exe`。
- 2026-06-03：发布 `0.73.0` 可安装测试包，收口 InnerBrain 本机已处理指定文件视图当前文件总览入口；`/inner-brain-eval-local-resolved 文件名` 查看指定文件已处理样本后会提示 `/inner-brain-eval-local-file 当前文件名`，便于回到同文件通过/失败总览；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.73.0.exe`。
- 2026-06-03：发布 `0.72.0` 可安装测试包，收口 InnerBrain 本机文件失败视图当前文件总览入口；`/inner-brain-eval-local-file-failed 文件名` 聚焦指定文件失败样本后会提示 `/inner-brain-eval-local-file 当前文件名`，便于回到同文件通过/失败总览；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.72.0.exe`。
- 2026-06-03：发布 `0.71.0` 可安装测试包，收口 InnerBrain 本机失败报告导出反馈当前文件总览入口；`/inner-brain-eval-local-report 文件名` 导出指定文件失败报告后会提示 `/inner-brain-eval-local-file 当前文件名`，便于回到同文件通过/失败总览；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.71.0.exe`。
- 2026-06-03：发布 `0.70.0` 可安装测试包，收口 InnerBrain 本机失败报告导出反馈当前文件已处理入口；`/inner-brain-eval-local-report 文件名` 导出指定文件失败报告后会提示 `/inner-brain-eval-local-resolved 当前文件名`，便于对照同文件已处理样本；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.70.0.exe`。
- 2026-06-02：发布 `0.68.0` 可安装测试包，收口 InnerBrain 本机已处理指定文件视图报告入口；`/inner-brain-eval-local-resolved 文件名` 会在同文件仍有待处理失败时追加 `/inner-brain-eval-local-report 当前文件名`，纯通过文件不追加报告入口；全量 `unittest` 566 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.68.0.exe`。
- 2026-06-02：发布 `0.67.0` 可安装测试包，收口 InnerBrain 本机文件视图报告入口；`/inner-brain-eval-local-file 文件名` 的当前文件总览会在当前文件仍有失败时追加 `/inner-brain-eval-local-report 当前文件名`，纯通过文件不追加报告入口；全量 `unittest` 565 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.67.0.exe`。
- 2026-06-02：发布 `0.66.0` 可安装测试包，收口 InnerBrain 本机已处理视图文件候选报告入口；`/inner-brain-eval-local-resolved` 的可查看文件候选会在同文件仍有待处理失败时追加 `/inner-brain-eval-local-report 当前文件名`，纯通过文件不追加报告入口；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.66.0.exe`。
- 2026-06-02：发布 `0.65.0` 可安装测试包，收口 InnerBrain 本机评估全量视图文件候选报告入口；`/inner-brain-eval-local` 的可聚焦文件候选会在同文件仍有失败时追加 `/inner-brain-eval-local-report 当前文件名`，纯通过文件不追加报告入口；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.65.0.exe`。
- 2026-06-02：发布 `0.64.0` 可安装测试包，收口 InnerBrain 本机失败视图失败文件分组报告入口；`/inner-brain-eval-local-failed` 的 `失败文件：` 分组会为每个失败文件追加 `/inner-brain-eval-local-report 当前文件名`；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.64.0.exe`。
- 2026-06-02：发布 `0.63.0` 可安装测试包，收口 InnerBrain 本机失败视图失败文件分组聚焦入口；`/inner-brain-eval-local-failed` 的 `失败文件：` 分组会为每个失败文件追加 `/inner-brain-eval-local-file-failed 当前文件名`；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.63.0.exe`。
- 2026-06-02：发布 `0.62.0` 可安装测试包，收口 InnerBrain 本机评估全量视图文件候选待处理入口；`/inner-brain-eval-local` 的可聚焦文件候选会在同文件仍有失败时追加 `/inner-brain-eval-local-file-failed 当前文件名`，纯通过文件不追加失败入口；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.62.0.exe`。
- 2026-06-02：发布 `0.61.0` 可安装测试包，收口 InnerBrain 本机已处理视图文件候选待处理入口；`/inner-brain-eval-local-resolved` 的可查看文件候选会在同文件仍有待处理失败时追加 `/inner-brain-eval-local-file-failed 当前文件名`，纯已处理文件不追加失败入口；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.61.0.exe`。
- 2026-06-02：发布 `0.60.0` 可安装测试包，收口 InnerBrain 本机已处理视图文件候选待处理优先排序；`/inner-brain-eval-local-resolved` 的可查看文件候选会按同文件待处理失败数量优先展示，并继续显示已处理/待处理失败数量；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.60.0.exe`。
- 2026-06-02：发布 `0.59.0` 可安装测试包，收口 InnerBrain 本机已处理视图文件候选状态摘要；`/inner-brain-eval-local-resolved` 的可查看文件候选会显示已处理数量和同文件待处理失败数量，并继续跳过纯失败文件；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.59.0.exe`。
- 2026-06-02：发布 `0.58.0` 可安装测试包，收口 InnerBrain 本机已处理视图文件候选提示；`/inner-brain-eval-local-resolved` 会列出有通过样本的 JSONL 文件候选，并跳过纯失败文件；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.58.0.exe`。
- 2026-06-02：发布 `0.57.0` 可安装测试包，收口 InnerBrain 本机文件失败视图已处理入口；`/inner-brain-eval-local-file-failed 文件名` 有失败样本时会提示 `/inner-brain-eval-local-resolved 当前文件名` 对照当前文件已处理样本；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.57.0.exe`。
- 2026-06-02：发布 `0.56.0` 可安装测试包，收口 InnerBrain 本机失败视图失败文件汇总排序；`/inner-brain-eval-local-failed` 的 `失败文件：` 分组会按失败数量优先展示 JSONL 文件；全量 `unittest` 564 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.56.0.exe`。
- 2026-06-02：发布 `0.55.0` 可安装测试包，收口 InnerBrain 本机评估全量视图文件候选失败优先排序；`/inner-brain-eval-local` 有样本时会按失败数量优先列出可聚焦 JSONL 文件候选，并保留总数、通过数、失败数和文件聚焦命令；全量 `unittest` 562 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.55.0.exe`。
- 2026-06-02：发布 `0.54.0` 可安装测试包，收口 InnerBrain 本机评估全量视图文件候选状态摘要；`/inner-brain-eval-local` 有样本时会在每个可聚焦 JSONL 文件候选行展示总数、通过数、失败数和 `/inner-brain-eval-local-file 文件名` 命令；全量 `unittest` 562 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.54.0.exe`。
- 2026-06-02：发布 `0.53.0` 可安装测试包，收口 InnerBrain 本机评估全量视图文件名候选提示；`/inner-brain-eval-local` 有样本时会列出可复制的 `/inner-brain-eval-local-file 文件名` 命令和来源文件样本数量；全量 `unittest` 562 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.53.0.exe`。
- 2026-06-02：发布 `0.52.0` 可安装测试包，收口 InnerBrain 本机评估全量视图后续处理提示；`/inner-brain-eval-local` 与 `/inner-brain-eval-local-file 文件名` 有样本时会提示失败视图、已处理清单和文件聚焦入口；全量 `unittest` 562 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.52.0.exe`。
- 2026-06-02：发布 `0.51.0` 可安装测试包，收口 InnerBrain 本机 evaluation 已处理样本只读清单；新增 `/inner-brain-eval-local-resolved [文件名]`，可只读查看当前已通过的本机评估样本并支持按 JSONL 文件过滤；全量 `unittest` 562 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.51.0.exe`。
- 2026-06-02：发布 `0.50.0` 可安装测试包，收口 InnerBrain 本机失败视图文件聚焦提示；`/inner-brain-eval-local-failed` 有失败样本时会提示按文件聚焦，`/inner-brain-eval-local-file-failed 文件名` 会提示回到全部本机失败样本；全量 `unittest` 557 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.50.0.exe`。
- 2026-06-02：发布 `0.49.0` 可安装测试包，收口 InnerBrain 本机失败视图导出报告提示；`/inner-brain-eval-local-failed` 与 `/inner-brain-eval-local-file-failed 文件名` 有失败样本时会提示导出全部或当前文件失败报告；全量 `unittest` 557 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.49.0.exe`。
- 2026-06-02：发布 `0.48.0` 可安装测试包，收口 InnerBrain 本机失败报告导出后续处理提示；`/inner-brain-eval-local-report [文件名]` 导出报告后会提示继续查看失败样本、按文件聚焦失败和补充本机 evaluation 样本；全量 `unittest` 557 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.48.0.exe`。
- 2026-06-02：发布 `0.47.0` 可安装测试包，收口 InnerBrain 本机 evaluation 样本保存后续验证提示；`/inner-brain-eval-add`、`/inner-brain-eval-label`、`/inner-brain-eval-add-candidate` 与 `/inner-brain-eval-label-candidate` 保存样本后会提示复跑本机评估、只看失败、聚焦 `runtime.jsonl` 和导出失败报告；全量 `unittest` 557 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.47.0.exe`。
- 2026-06-02：发布 `0.46.0` 可安装测试包，收口 InnerBrain 本机 evaluation 空样本引导；当 `/inner-brain-eval-local` 或 `/inner-brain-eval-local-failed` 没有本机 JSONL 样本时，会明确显示 `本机评估样本：- 无` 并列出 `/inner-brain-eval-add`、`/inner-brain-eval-label`、`/inner-brain-eval-add-candidate` 与 `/inner-brain-eval-label-candidate`，说明这些命令只写本机 evaluation 样本、不自动训练；全量 `unittest` 557 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.46.0.exe`。
- 2026-06-02：发布 `0.45.0` 可安装测试包，收口 InnerBrain 本机失败评估文件意图混淆修复建议分组；`/inner-brain-eval-local-report [文件名]` 未指定文件时会按 `source_file + expected_intent -> actual_intent` 集中列出显式 `/inner-brain-teach` 或 `/inner-brain-label` 建议，只读导出且不写入 runtime 训练样本；全量 `unittest` 555 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.45.0.exe`。
- 2026-06-02：发布 `0.44.0` 可安装测试包，收口 InnerBrain 本机失败评估意图混淆修复建议分组；`/inner-brain-eval-local-report [文件名]` 导出的 `word/inner-brain-evaluation-report.md` 会按 `expected_intent -> actual_intent` 混淆方向集中列出显式 `/inner-brain-teach` 或 `/inner-brain-label` 建议，只读导出且不写入 runtime 训练样本；全量 `unittest` 554 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.44.0.exe`。
- 2026-06-02：发布 `0.43.0` 可安装测试包，收口 InnerBrain 本机失败评估文件意图混淆汇总；`/inner-brain-eval-local-report [文件名]` 在未指定单个文件时会按失败样本的 `source_file + expected_intent -> actual_intent` 统计数量并列出典型样本，只读导出且不写入 runtime 训练样本；全量 `unittest` 553 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.43.0.exe`。
- 2026-06-02：发布 `0.41.0` 可安装测试包，收口 InnerBrain 本机失败评估期望意图汇总；`/inner-brain-eval-local-report [文件名]` 导出的 `word/inner-brain-evaluation-report.md` 会按失败样本的 `expected_intent` 统计数量并列出典型样本，只读导出且不写入 runtime 训练样本；全量 `unittest` 551 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.41.0.exe`。
- 2026-06-02：发布 `0.40.0` 可安装测试包，收口 InnerBrain 本机失败评估类型汇总；`/inner-brain-eval-local-report [文件名]` 导出的 `word/inner-brain-evaluation-report.md` 会按意图、命令、策略失败类型统计数量并列出典型样本，只读导出且不写入 runtime 训练样本；全量 `unittest` 550 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.40.0.exe`。
- 2026-06-02：发布 `0.39.0` 可安装测试包，收口 InnerBrain 本机失败评估原因汇总；`/inner-brain-eval-local-report [文件名]` 导出的 `word/inner-brain-evaluation-report.md` 会按失败原因统计数量并列出典型样本，只读导出且不写入 runtime 训练样本；全量 `unittest` 549 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.39.0.exe`。
- 2026-06-02：发布 `0.38.0` 可安装测试包，收口 InnerBrain 本机失败评估 Markdown 报告导出；新增 `/inner-brain-eval-local-report [文件名]` 写入 `word/inner-brain-evaluation-report.md`，只读导出且不写入 runtime 训练样本；全量 `unittest` 548 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.38.0.exe`。
- 2026-06-02：发布 `0.37.0` 可安装测试包，收口 InnerBrain 本机失败评估按文件分组；`/inner-brain-eval-local-failed` 会显示失败来源 JSONL 文件和失败条数；全量 `unittest` 545 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.37.0.exe`。
- 2026-06-02：发布 `0.36.0` 可安装测试包，收口 InnerBrain 本机评估 JSONL 文件过滤；新增 `/inner-brain-eval-local-file` 与 `/inner-brain-eval-local-file-failed`，可按本机 evaluation 文件名只看指定样本或指定失败样本；全量 `unittest` 543 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.36.0.exe`。
- 2026-06-02：发布 `0.35.0` 可安装测试包，收口 InnerBrain 候选编号写入本机评估样本；新增 `/inner-brain-eval-add-candidate` 与 `/inner-brain-eval-label-candidate`，可把 `/inner-brain-candidates` 当前候选按编号写入本机 evaluation JSONL，不写入 runtime 训练样本且不移除候选；全量 `unittest` 540 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.35.0.exe`。
- 2026-06-01：发布 `0.34.0` 可安装测试包，收口 InnerBrain 本机评估样本显式写入；新增 `/inner-brain-eval-add` 与 `/inner-brain-eval-label` 把用户确认的真实日志写入本机 evaluation JSONL，不写入 runtime 训练样本；全量 `unittest` 537 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.34.0.exe`。
- 2026-06-01：发布 `0.33.0` 可安装测试包，收口 InnerBrain 本机评估过滤视图；新增 `/inner-brain-eval-local` 与 `/inner-brain-eval-local-failed` 单独查看本机 JSONL 评估样本，不写入 runtime 样本；全量 `unittest` 533 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.33.0.exe`。
- 2026-06-01：发布 `0.32.0` 可安装测试包，收口 InnerBrain 评估失败过滤视图；新增 `/inner-brain-eval-failed` 只显示失败样本和显式修复建议，不写入 runtime 样本；全量 `unittest` 530 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.32.0.exe`。
- 2026-06-01：发布 `0.31.0` 可安装测试包，收口 InnerBrain 评估失败修复建议；`/inner-brain-eval` 在失败样本下追加可复制的 `/inner-brain-teach` 或 `/inner-brain-label` 显式训练提示，但不写入 runtime 样本；全量 `unittest` 528 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.31.0.exe`。
- 2026-06-01：发布 `0.30.0` 可安装测试包，收口 InnerBrain 本机评估集扩展；`/inner-brain-eval` 默认合并固定 seed 评估集和 `data/inner-brain/evaluation/*.jsonl` 本机 JSONL 样本，输出来源计数且不写入 runtime 训练样本；全量 `unittest` 526 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.30.0.exe`。
- 2026-06-01：发布 `0.29.0` 可安装测试包，收口 InnerBrain 固定评估集；新增 `/inner-brain-eval` 执行 seed 评估基线，输出通过数、失败数、准确率和逐条样例，不写入 runtime 样本、不自动训练；全量 `unittest` 524 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.29.0.exe`。
- 2026-06-01：发布 `0.28.0` 可安装测试包，收口 InnerBrain 样本包含签名置信度补偿；当用户长句完整包含不少于 4 字的已知样本签名时，分类器在样本相似度层提升置信度，不新增自然语言意图正则；全量 `unittest` 522 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.28.0.exe`。
- 2026-06-01：发布 `0.27.0` 可安装测试包，收口桌面候选目标预填；桌面候选训练区可选择常见教学命令或常见 `intent slot=value` 标注模板，但仍只写入输入框，不自动提交、不自动训练；全量 `unittest` 521 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.27.0.exe`。
- 2026-06-01：发布 `0.26.0` 可安装测试包，收口桌面候选选择绑定；执行 `/inner-brain-candidates` 后，桌面候选下拉框会展示当前候选，选择某条候选会同步编号，随后“填教学”“填标注”继续只把对应编号模板写入输入框；全量 `unittest` 519 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.26.0.exe`。
- 2026-06-01：发布 `0.25.0` 可安装测试包，收口桌面候选模板状态同步；执行 `/inner-brain-candidates` 后，桌面候选模板会显示空候选或候选数量，自动禁用/启用“填教学”“填标注”，并把编号上限收紧到实际候选数；全量 `unittest` 517 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.25.0.exe`。
- 2026-06-01：发布 `0.24.0` 可安装测试包，收口桌面候选训练模板填充；桌面面板新增候选编号、 “填教学”和“填标注”入口，只把 teach/label 模板写入输入框，由用户显式补全并发送；全量 `unittest` 515 项通过，安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.24.0.exe`。
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
- [2026-06-03 验证记录](verification/2026-06/2026-06-03.md)：最近一次验证明细。
- [2026-06-02 验证记录](verification/2026-06/2026-06-02.md)：2026-06-02 验证明细。
- [2026-06-01 验证记录](verification/2026-06/2026-06-01.md)：2026-06-01 验证明细。

## 记录规则

- 根目录 `verification.md` 只保留最近摘要和索引。
- 完整验证命令、RED/GREEN 过程和收尾结果写入 `verification/YYYY-MM/YYYY-MM-DD.md`。
- 自然周文件只做索引，不再承载完整明细。
- 每次新增验证记录后同步更新对应月份索引和周索引。
