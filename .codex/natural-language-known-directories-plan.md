# 自然语言已知目录别名计划

> 日期：2026-05-21
> 执行者：Codex

## 上下文扫描

- 现有自然语言解析集中在 `src/jarvis_lite/intent.py`。
- `JarvisAgent._handle_natural_language_intent()` 已能把 `open_directory_alias` 和 `organize_directory_alias` 转成 `_open_directory()` 与 `_organize_preview()`。
- `_open_directory()` 和 `_organize_preview()` 当前只查 `memory/directories.json` 中已登记的常用目录。
- `preview_file_organization()` 只生成预览，不移动或删除文件；`record_directory_open_request()` 只写入 `logs/desktop-actions.txt`，不启动外部应用。

## 关键疑问

- 用户说“整理桌面”时，是否应该要求先登记 `/dir-add 桌面 ...`？
  - 判断：不应该。桌面是操作系统已知目录，属于高频自然语言表达。
- 是否真实整理或移动桌面文件？
  - 判断：不做。本阶段继续复用文件整理预览，只输出建议。
- 是否引入第三方目录解析库？
  - 判断：不需要。当前只用 `Path.home() / "Desktop"`，优先保持标准库实现。

## 充分性检查

- 接口契约：`_find_common_directory("桌面")` 在未登记常用目录时可返回桌面目录；登记目录仍优先。
- 技术选型：复用 `CommonDirectory`、`preview_file_organization()` 和 `record_directory_open_request()`，不新增执行层。
- 风险点：有些系统桌面目录不存在或被重定向，若不存在则保持原有“没有找到常用目录”提示。
- 验证方式：先写 Agent 失败测试，mock `Path.home()` 指向临时目录，再实现。

## 任务拆分

1. 新增测试：未登记常用目录时，“整理桌面”可预览临时 Desktop 目录。
2. 新增测试：未登记常用目录时，“打开桌面”可记录打开请求。
3. 实现 Agent 已知目录 fallback，先支持 `桌面`。
4. 更新文档、测试记录和审查报告。
