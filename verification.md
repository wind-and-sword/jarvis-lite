# 验证记录

> 日期：2026-05-27
> 执行者：Codex
> 说明：根目录只作为验证记录入口，不再长期追加完整命令和输出。

## 最近摘要

- 2026-05-27：编号最近资料打标签缺失提示已完成专项验证，历史记录已迁入周归档。
- 2026-05-27：项目文档整理第一阶段完成验证，`git diff --check` 退出 0，Markdown 本地链接检查通过。
- 2026-05-27：本地 `unittest` 全量 290 项通过，桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。

## 详细记录

- [verification/README.md](verification/README.md)：验证记录归档规则和入口。
- [verification/2026-05/README.md](verification/2026-05/README.md)：2026-05 验证记录索引。
- [2026-05-18 周](verification/2026-05/week-2026-05-18.md)：2026-05-18 至 2026-05-24 的验证明细。
- [2026-05-25 周](verification/2026-05/week-2026-05-25.md)：2026-05-25 至 2026-05-31 的验证明细。

## 记录规则

- 根目录 `verification.md` 只保留最近摘要和索引。
- 完整验证命令、RED/GREEN 过程和收尾结果写入 `verification/YYYY-MM/week-YYYY-MM-DD.md`。
- 每周文件按自然周拆分；如果单周文件明显过大，再按自然日拆分。
- 每次新增验证记录后同步更新对应月份索引。
