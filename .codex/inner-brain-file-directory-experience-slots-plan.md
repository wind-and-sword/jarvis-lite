# InnerBrain 文件路径、目录和经验槽位迁移计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

将显式文件读取/导入、目录打开/整理和经验记录/搜索/建议从 `legacy_fallback` 迁移到 InnerBrain seed 样本分类器主路径。样本签名负责语义识别，解析函数只抽取结构化槽位。

## 接口契约

- `document.read_path`：抽取 `path`，映射到 `/read "path"`。
- `knowledge.import`：抽取 `source`，映射到 `/import "source"`。
- `directory.open_drive`：抽取 `alias` 和 `path`，映射到 `open_directory_path`。
- `directory.open_alias` / `directory.organize_alias`：抽取 `alias`。
- `directory.open_recent` / `directory.organize_recent`：不需要槽位。
- `experience.record`：抽取 `experience`，映射到 `/experience`。
- `experience.search` / `experience.advice`：抽取 `query`，映射到 `/experience-search` 或 `/experience-advice`。

## TDD 步骤

1. RED：在 `tests/test_inner_brain.py` 新增文件路径、目录、经验三组样本分类器测试，确认当前仍走 `legacy_fallback`。
2. GREEN：扩展 `seed_training_samples()`、intent-specific signature、槽位抽取和 `NaturalLanguageIntent` 映射。
3. 回归：运行目标测试、`tests.test_inner_brain`、`tests.test_inner_brain tests.test_agent` 和全量 `unittest`。
4. 文档：同步 v6 方案、README、当前方案、进度和验证记录。

## 风险

- 路径带空格、引号和 Windows 盘符必须从原始输入抽取。
- 泛化导入样本不能覆盖编号最近文件导入。
- 目录别名不能吞掉最近目录引用。
