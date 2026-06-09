# 操作记录

> 日期：2026-05-18
> 执行者：Codex

## 2026-05-18

- 调整并改名 `DOCUMENTATION.md` 文档整理约定，明确根目录长期约定、`word/` 正式文档、`.codex/` 本地过程记录、`logs/` 运行日志和 `日志.txt` 临时排障日志的边界。
- 保留 `.gitignore` 中的 `/日志.txt` 忽略规则，避免临时排障日志进入 Git。
- 开始初始化 Jarvis Lite 阶段 1 Python 命令行助手骨架。
- 当前工具列表中没有 `sequential-thinking`、`shrimp-task-manager`、`code-index`，本次使用本地文件读取、`rg`、`unittest` 和 `.codex/` 记录替代。
- 完成 Python 骨架实现，包含命令行入口、长期记忆读取、本地工具白名单、日志记录和本地测试。
- 验证 `python -m unittest discover -s tests -v` 通过，CLI 冒烟命令 `/memory`、`/list` 和普通输入通过。
- 根据用户确认，将项目 Python 版本固定到 3.13 系列，创建 `.venv`，新增 `.python-version`，并将 `pyproject.toml` 改为 `>=3.13,<3.14`。
- 推送本地 `main` 到 GitHub，远程更新到 `f7e35ee`。
- 继续阶段 1 的资料问答能力：新增 `knowledge.py`，支持检索 `data/` 下 `.txt` 和 `.md` 文件，`/ask` 和普通问题可返回带来源的回答。
- 增强资料问答质量：`answer_from_data` 最多返回 3 条来源片段，跳过 Markdown 标题，并过滤明显弱相关命中。
- 推送多片段问答提交到 GitHub，远程更新到 `8affb09`。
- 新增 `conversation.py` 交互式会话层，支持 `/history`、`/save-summary 文件名` 和 `/clear`。
- 新增长期记忆写入和身份问答闭环：`/remember`、`我叫...`、`我是...` 写入 `memory/profile.md`，并能回答“你知道我是谁吗”。
- 按用户要求拆分 README：整体方案和路线图迁移到 `word/jarvis-lite-overall-plan.md`，README 保留入口、启动命令和当前状态。
- 增强长期记忆更新：带 `key：value` 的记忆再次写入时替换旧 key，避免身份信息重复。
- 为阶段 1 收口新增 `/status` 命令，输出长期记忆、data 文本问答、工具日志、会话能力和本地验证命令。
- 修复 `/status` 在 Windows 上输出反斜杠路径的问题，统一为文档可读的项目相对路径。
- 推送阶段 1 收口提交到 GitHub，远程 `main` 更新到 `998f67a`。
- 开始阶段 2 个人知识库入口；判断云数据库暂不作为第一批依赖，优先完善本地 `data/` 资料索引。
- 新增知识库索引能力和 `/kb` 状态命令，统计支持格式、资料文件数量、可检索行数和资料列表。
- 阶段 2 第一批功能已本地提交为 `d0ed120 feat: 增加个人知识库状态入口`，尚未推送；当前分支 `main...origin/main [ahead 1]`。
- 下次继续建议先推送 `d0ed120`，再实现 Markdown/txt 资料导入命令，并用 `/kb` 与 `/ask` 做闭环验证。

## 2026-05-19

- 根据 `日志.txt` 和阶段 2 进度文档恢复上下文，确认昨日暂停点为本地 `main` 领先远程 2 个提交。
- 首次推送遇到 GitHub TLS 握手失败；只读 `ls-remote` 成功后重试 push，已将 `d0ed120` 和 `7df6924` 推送到远程 `main`。
- 继续阶段 2 资料导入能力，采用本地 `data/` 方案，暂不接入云数据库。
- 按 TDD 新增 `import_knowledge_file` 和 `/import 源文件路径 [目标文件名]`。
- 导入功能支持 `.md` 和 `.txt`，拒绝不支持格式，拒绝覆盖已存在目标文件。
- 推送 `a2afc23 feat: 增加知识库资料导入命令` 到远程 `main`。
- 继续扩展 `/import`，新增目录批量导入：递归扫描目录，保留相对结构，跳过隐藏路径和不支持格式。
- 目录导入命令输出扫描数量、成功数量、跳过数量和可检索行数摘要。
- 根据 `DOCUMENTATION.md` 的文档约定，读取 `word/文档索引.md`、阶段 2 进度文档、README、verification 和 `.codex/` 记录，确认当前下一项任务为增强 `/ask` 的排序和摘要质量。
- 当前工具列表中没有 `sequential-thinking`、`shrimp-task-manager`、`code-index`；本轮继续使用本地文件读取、`rg`、`unittest`、`update_plan` 和 `.codex/` 记录替代。
- 新增本轮上下文扫描和阶段 2 `/ask` 排序与摘要质量实现计划，目标是在不引入外部依赖的前提下改善规则式检索输出。
- 按 TDD 新增 `/ask` 排序和摘要格式测试，确认旧实现会把泛化资料排在包含 `3.13` 的具体资料前，并且缺少命中数量摘要和编号。
- 修改 `knowledge.py`：对包含数字或版本号的查询词加权；`answer_from_data` 输出命中数量摘要和编号，保留 `data/文件:行号` 来源格式。
- 全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 58 个测试。
- 本轮改动已提交到本地 Git：`a781cd1 feat: 优化知识库问答排序与摘要`。当前 `main` 相对 `origin/main` 本地领先 2 个提交，未执行远程 push。
- 用户确认 push 后，已执行 `git push origin main`，远程 `main` 更新到 `a781cd1`。
- 继续阶段 2 下一项：支持对导入资料做简单标签或分类。计划使用 `data/.knowledge-tags.json` 保存标签元数据，新增 `/tag 文件名 标签...` 命令，并让 `/kb` 与 `/ask` 使用标签信息。
- 按 TDD 新增标签相关测试，确认旧实现缺少 `set_document_tags` API，Agent 也不识别 `/tag`。
- 实现知识库标签能力：`KnowledgeDocument.tags`、标签元数据读写、标签规范化、`/kb` 标签展示、标签参与 `search_data` 得分和 `/tag` 命令。
- 全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 64 个测试。
- 本轮标签功能已提交并推送到远程 `main`：`d85a665 feat: 支持知识库资料标签`。
- 继续阶段 2 下一项：评估并实现 PDF 与聊天记录导入。确认 `pypdf` 当前最新可用版本为 `6.11.0`，方案采用 `pypdf>=6,<7` 抽取 PDF 文本，聊天记录 JSON 转换为 Markdown。
- 按 TDD 新增 PDF、JSON 聊天记录和目录批量导入测试，确认旧实现拒绝 `.pdf` 和 `.json`。
- 修改 `pyproject.toml` 增加 `pypdf>=6,<7`，执行 `.\.venv\Scripts\python.exe -m pip install -e .` 安装依赖。
- 实现 PDF 抽取文本转 Markdown、JSON 聊天记录转 Markdown，并让目录批量导入支持 `.pdf` 与 `.json`。
- 全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 68 个测试；临时目录 CLI 冒烟验证 `/import chat.json`、`/import manual.pdf` 和 `/ask` 命中通过。
- 用户要求 push 并继续下一个阶段；已推送 `74e3405 feat: 支持 PDF 和聊天记录导入` 到远程 `main`。
- 根据路线图进入阶段 3：语音入口。第一批目标是可验证的 `/voice-status`、`/speak 文本` 和 `/voice 文本`，先不接入麦克风实时识别。
- 按 TDD 新增 `tests/test_voice.py` 和 Agent 语音命令测试，确认旧实现缺少 `jarvis_lite.voice` 且 Agent 不识别 `/voice-status`。
- 新增 `voice.py`：支持语音状态、transcript 播报记录和 Windows `System.Speech` 播报入口。
- Agent 新增 `/voice-status`、`/speak 文本`、`/voice 已识别的语音文本`，其中 `/voice` 会复用现有 Agent 回答流程并播报回答。
- 全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 74 个测试。
- 阶段 3 第一批能力已提交并推送到远程 `main`：`a8e4485 feat: 增加语音入口基础命令`。
- 用户要求摄像头、麦克风等硬件能力先暂停，改为先完成其他非硬件任务；下一步转入阶段 4 工作台自动化第一批：常用目录管理和日报生成。
- 按 TDD 新增 `tests/test_automation.py` 和 Agent 自动化命令测试，确认旧实现缺少 `jarvis_lite.automation` 且 Agent 不识别 `/automation-status`。
- 新增 `automation.py`：支持常用目录登记、目录列表、阶段 4 自动化状态和 Markdown 日报生成。
- Agent 新增 `/automation-status`、`/dir-add 别名 目录路径`、`/dirs` 和 `/daily-report [文件名]`。
- 全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 80 个测试。
- 根据用户最新要求，确认摄像头、麦克风、真实麦克风语言识别等硬件入口继续暂缓，优先推进非硬件自动化。
- 复核 `DOCUMENTATION.md`、`word/jarvis-lite-overall-plan.md`、README、阶段 4 进度文档、Agent 和自动化模块改动。
- 再次执行全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，结果 80 个测试全部通过。
- 再次执行临时目录 CLI 冒烟，验证 `/automation-status`、`/dir-add`、`/dirs`、`/daily-report today.md` 可用，并确认 `word/today.md` 生成。
- 本地提交阶段 4 第一批能力：`6ac34ee feat: 增加工作台自动化基础命令`。
- 首次 `git push origin main` 失败，错误为 GitHub HTTPS `schannel` TLS 握手失败；只读 `git ls-remote origin -h refs/heads/main` 成功。
- 第二次 `git push origin main` 失败，错误为 GitHub 443 连接超时；`Test-NetConnection github.com -Port 443` 显示 TCP 可达。
- 检查到仓库本地配置使用 `http.sslbackend schannel`，用一次性覆盖 `git -c http.sslBackend=openssl push origin main` 推送成功，远程 `main` 更新到 `6ac34ee`。
- 继续阶段 4 非硬件自动化下一项：文件整理预览。目标是 `/organize-preview 常用目录别名`，只生成整理建议，不移动、不删除文件。
- 按 TDD 新增 `preview_file_organization` 核心测试，先确认旧实现缺少函数导致测试失败，再实现按扩展名分组、跳过子目录和无后缀文件归类。
- 按 TDD 新增 Agent 命令测试，先确认 `/organize-preview` 为未知命令，再接入常用目录别名解析和整理预览输出。
- 更新 README、阶段 4 进度文档和验证记录，补充 `/organize-preview` 使用方式。
- 全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 82 个测试。
- 临时目录 CLI 冒烟验证 `/automation-status`、`/dir-add`、`/dirs`、`/daily-report today.md`、`/organize-preview 项目` 均可执行，整理预览显示 3 个文件、跳过 1 个子目录。
- 提交前复跑 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 82 个测试；`git diff --check` 未发现空白错误。
- 文件整理预览已提交：`6c7658c feat: 增加文件整理预览命令`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `6c7658c`。
- 继续阶段 4 非硬件自动化下一项：常用目录打开 dry-run/transcript 记录。目标是 `/dir-open 常用目录别名`，只记录打开目录请求，不启动外部应用。
- 按 TDD 新增 `record_directory_open_request` 单元测试，先确认旧实现缺少函数，再实现写入 `logs/desktop-actions.txt`。
- 按 TDD 新增 Agent `/dir-open` 测试，先确认旧 Agent 未生成 transcript，再接入命令、帮助文本和工具日志。
- 更新 README、阶段 4 进度文档和验证记录，补充 `/dir-open` 用法和 dry-run 行为。
- 全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 84 个测试。
- 临时目录 CLI 冒烟验证 `/dir-open 项目` 可写入 `logs/desktop-actions.txt`，内容包含 `open_directory`、别名和目标路径。
- 常用目录打开记录已提交：`8db5f9d feat: 增加常用目录打开记录`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `8db5f9d`。
- 用户确认下一步要把 Jarvis Lite 从命令行推进为类似桌面虚拟宠物/桌面助手的应用，并要求先做方案再写代码。
- 使用 brainstorming 流程做方案设计；因项目文档约定优先，正式方案写入 `word/`，本地上下文写入 `.codex/`。
- 复核现有架构：`JarvisAgent.handle` 可作为单轮核心入口，`ConversationSession.handle` 可作为桌面 UI 的多轮会话入口，当前不需要重写核心。
- 新增正式方案文档 `word/jarvis-lite-desktop-pet-app-design.md`，推荐“桌面角落常驻小助手 + 点击展开完整助手面板”的两层体验。
- 方案建议第一版使用 PySide6/Qt 作为桌面壳，继续复用现有 Python 核心；摄像头、麦克风和真实硬件入口继续暂缓。
- 更新 `word/文档索引.md`，加入桌面虚拟助手应用方案入口。
- 文档检查 `git diff --check` 未发现空白错误；全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 84 个测试。
- 用户确认开始实现桌面虚拟助手应用；本轮先写 `.codex/desktop-pet-implementation-plan.md`，明确第一步只做 `desktop bridge`，不引入 PySide6 窗口代码。
- 按 TDD 新增 `tests/test_desktop_bridge.py`，先确认旧实现缺少 `jarvis_lite.desktop` 包。
- 新增 `src/jarvis_lite/desktop/` 包，包含 `DesktopState`、`DesktopBridge`、`DesktopResponse` 和 `quick_commands()`。
- `DesktopBridge` 复用现有 `ConversationSession.handle()`，为后续 UI 返回 `user_input`、`assistant_text`、`state` 和 `turn_count`。
- 新增桌面应用进度文档 `word/2026-05-19-jarvis-lite-desktop-app-progress.md`，并更新 `word/文档索引.md` 和 `verification.md`。
- 桌面 bridge 专项测试 `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v` 通过，3 个测试。
- 全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 87 个测试；`git diff --check` 未发现空白错误。
- 桌面助手 bridge 层已提交：`0ddfc3a feat: 增加桌面助手桥接层`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `0ddfc3a`。
- 继续桌面应用第二步：新增 PySide6 桌面入口和最小助手面板。
- 当前虚拟环境未安装 PySide6；按 TDD 新增 `tests/test_desktop_app.py`，先确认缺少 `jarvis_lite.desktop.app`。
- 修改 `pyproject.toml` 增加 `PySide6>=6,<7` 和 `jarvis-lite-desktop = "jarvis_lite.desktop.app:main"` 脚本。
- 执行 `.\.venv\Scripts\python.exe -m pip install -e .` 安装 PySide6 6.11.1 及相关依赖。
- 新增 `src/jarvis_lite/desktop/app.py`，提供最小 PySide6 助手面板、文本输入、快捷命令按钮和 `--smoke` 验证模式。
- 初版 smoke 创建 `QApplication` 时 Qt 输出字体目录警告，调整为 smoke 仅加载 PySide6 依赖并输出标题，真实运行仍创建窗口。
- `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v` 通过，2 个测试。
- `.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手`。
- 提交前复验：桌面入口专项测试 2 个通过；全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 89 个测试；桌面 smoke 输出 `Jarvis Lite 桌面助手`；`git diff --check` 未发现空白错误。
- 最小桌面入口已提交：`b54981c feat: 增加桌面助手最小入口`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `b54981c`。
- 用户希望等桌面虚拟助手目标完整落实后再测试；继续推进“桌面角落小助手 + 点击展开面板”。
- 按 TDD 新增 `tests/test_desktop_widgets.py`，先确认缺少 `jarvis_lite.desktop.widgets`，再实现 `AssistantPanel` 和 `DesktopPetWindow`。
- 新增 `src/jarvis_lite/desktop/widgets.py` 和 `app_style.py`；`DesktopPetWindow` 使用无边框、置顶、小尺寸窗口，点击可展开或收起 `AssistantPanel`。
- 将 `src/jarvis_lite/desktop/app.py` 从内嵌 QWidget 重构为调用 `AssistantPanel` 和 `DesktopPetWindow`。
- 处理 Qt 自动化测试环境警告：widget 测试使用 `QT_QPA_PLATFORM=minimal`，minimal/offscreen 下不调用 `raise_()`。
- 按 TDD 增强 `--smoke`：先确认只输出标题、不创建小助手窗口，再改为创建 `desktopPetWindow` 后立即退出。
- 按 TDD 新增小助手状态同步测试，先确认 `DesktopPetWindow` 缺少 `caption_text()`，再实现 `AssistantPanel` 状态监听和 `DesktopPetWindow.set_state()`。
- 小助手现在可根据面板执行结果显示 `待命`、`思考`、`工作`、`完成`、`错误`。
- 提交前复验：`tests.test_desktop_app` 3 个测试通过；`tests.test_desktop_widgets` 4 个测试通过；全量本地测试 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 94 个测试；桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 未发现空白错误。
- 桌面小助手窗口已提交：`9a9ee47 feat: 增加桌面小助手窗口`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `9a9ee47`。
- 用户确认项目相关图片和动效素材应放入项目并上传 GitHub，运行态文件暂放项目上一层 `ai` 目录中。
- 继续桌面应用第一版收口：新增项目内状态素材、运行态位置保存和轻量状态动效。
- 当前工具列表中没有 `sequential-thinking`、`shrimp-task-manager`、`code-index`；本轮使用本地文件读取、`rg`、`unittest`、`update_plan` 和 `.codex/` 记录替代。
- 新增 `src/jarvis_lite/desktop/assets.py` 和 `src/jarvis_lite/desktop/assets/*.svg`，将 `idle`、`thinking`、`working`、`success`、`error` 五个状态映射到项目内 SVG 素材。
- 新增 `src/jarvis_lite/desktop/settings.py`，运行态设置目录为项目根目录上一层 `jarvis-lite-runtime/desktop-settings.json`。
- 按 TDD 新增 `tests/test_desktop_assets.py` 和 `tests/test_desktop_settings.py`，覆盖项目内素材、运行态目录、窗口位置保存和损坏设置回退默认值。
- 更新 `DesktopPetWindow`，按状态切换 SVG 角色图，拖动或关闭时保存窗口位置，启动时恢复位置。
- 继续按 TDD 增加状态动效测试，先确认 `DesktopPetWindow` 缺少动效 profile 和帧推进接口，再用 Qt 定时器实现待机呼吸、思考脉冲、工作脉冲、完成弹跳和错误抖动。
- 更新 README、`verification.md` 和桌面应用进度文档，说明桌面第一版当前能力、素材位置、运行态设置位置和 103 个测试结果。
- 用户确认下一阶段按“系统托盘 + 关闭到托盘 + 退出控制”推进。
- 新增 `.codex/desktop-tray-lifecycle-plan.md`，明确托盘生命周期只处理显示/隐藏/退出，不扩展设置面板和安装包。
- 按 TDD 新增 `tests/test_desktop_tray.py`，先确认缺少 `jarvis_lite.desktop.tray` 导致测试失败。
- 新增 `src/jarvis_lite/desktop/tray.py`，使用 `QSystemTrayIcon`、`QMenu` 和 `QAction` 管理托盘菜单，菜单包含“显示助手”“隐藏助手”“退出”。
- 更新 `DesktopPetWindow`，新增 close-to-tray 开关；托盘模式下关闭窗口会保存位置、隐藏面板和小助手，并忽略关闭事件。
- 更新 `src/jarvis_lite/desktop/app.py`，正常启动时创建并显示托盘控制器，`--smoke` 保持快速创建窗口后退出。
- 更新 README、`verification.md` 和桌面应用进度文档，记录托盘生命周期和 106 个测试结果。
- 用户确认下一阶段按“桌面设置面板”推进，范围限定为置顶、透明度和小助手尺寸，不做托盘命令和打包。
- 新增 `.codex/desktop-settings-panel-plan.md`，明确设置模型、窗口应用设置、面板设置区域和验证步骤。
- 按 TDD 扩展 `tests/test_desktop_settings.py`，先确认缺少 `save_desktop_preferences`，再实现运行态偏好字段、保存偏好和保存位置保留偏好。
- 更新 `src/jarvis_lite/desktop/settings.py`，`DesktopSettings` 新增 `always_on_top`、`opacity_percent`、`pet_size`，并提供 `save_desktop_settings()` 和 `save_desktop_preferences()`。
- 按 TDD 扩展 `tests/test_desktop_widgets.py`，先确认 `AssistantPanel` 和 `DesktopPetWindow` 缺少设置控件、设置回调和应用偏好接口。
- 更新 `AssistantPanel`，新增设置区域：置顶复选框、透明度滑块、小助手尺寸滑块，并通过 `set_settings_listener()` 通知设置变化。
- 更新 `DesktopPetWindow`，新增启动恢复偏好、应用偏好、保存偏好、透明度、置顶和等比尺寸缩放能力。
- 更新 `src/jarvis_lite/desktop/app.py`，创建桌面应用时把运行态设置传入面板，并将面板设置变更连接到小助手。
- 更新 README、`verification.md` 和桌面应用进度文档，记录设置面板和 113 个测试结果。
- 用户确认继续后续任务；根据桌面进度文档，进入“托盘菜单常用命令入口”阶段。
- 新增 `.codex/desktop-tray-quick-commands-plan.md`，范围限定为状态、知识库、常用目录和生成日报 4 个低风险托盘命令。
- 按 TDD 扩展 `tests/test_desktop_tray.py`，先确认 `DesktopTrayController` 缺少 `quick_command_texts()` 和 `quick_command_action()`。
- 更新 `src/jarvis_lite/desktop/tray.py`，新增托盘快捷命令 action 映射；点击托盘命令会显示小助手和面板，并调用 `AssistantPanel.submit_text()`。
- 更新 README、`verification.md` 和桌面应用进度文档，记录托盘快捷命令和 115 个测试结果。
- 2026-05-20：用户确认继续下一阶段；本阶段选择“托盘最近结果反馈”，用于补齐托盘快捷命令执行后的可见反馈。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用本地文件读取、`rg`、`unittest`、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `word/2026-05-20-jarvis-lite-desktop-tray-feedback-design.md` 和 `.codex/desktop-tray-recent-result-plan.md`，明确不接入系统通知、摄像头、麦克风、真实语音识别、安装包或开机自启动。
- 按 TDD 新增 `tests.test_desktop_widgets.DesktopWidgetTests.test_panel_tracks_last_result_after_submission`，先确认 `AssistantPanel` 缺少 `last_result_text()`。
- 更新 `AssistantPanel`，新增最近结果记录；`submit_text()` 返回 `DesktopResponse | None`，便于托盘控制器复用执行结果。
- 按 TDD 扩展 `tests/test_desktop_tray.py`，先确认 `DesktopTrayController` 缺少 `recent_result_action` 和 `recent_result_text()`。
- 更新 `DesktopTrayController`，新增“最近结果”菜单项、最近结果文本、tooltip 更新和只显示不重跑的最近结果动作。
- 专项验证：`tests.test_desktop_widgets` 13 个测试通过；`tests.test_desktop_tray` 8 个测试通过。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 119 个测试；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅有 CRLF 提示。
- 托盘最近结果入口已提交：`b4ccae4 feat: 增加托盘最近结果入口`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `b4ccae4`。
- 2026-05-20：用户确认继续推荐方案，本阶段开始“助手面板尺寸持久化”。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用本地文件读取、`rg`、`unittest`、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `word/2026-05-20-jarvis-lite-desktop-panel-size-design.md` 和 `.codex/desktop-panel-size-plan.md`，范围限定为运行态面板宽高保存与恢复，不做主题、安装包、开机自启动和硬件入口。
- 按 TDD 扩展 `tests/test_desktop_settings.py`，先确认 `save_desktop_panel_size` 不存在、`DesktopSettings` 缺少面板宽高字段。
- 更新 `settings.py`，新增 `panel_width`、`panel_height` 和 `save_desktop_panel_size()`，保存位置和偏好时保留面板宽高。
- 按 TDD 扩展 `tests/test_desktop_widgets.py`，先确认面板不会恢复/保存宽高，且小助手偏好保存会重置面板尺寸。
- 更新 `AssistantPanel`，启动时恢复宽高，resize/close 时保存面板宽高；更新 `DesktopPetWindow.apply_preferences()` 保留已有面板宽高。
- 专项验证：`tests.test_desktop_settings` 8 个测试通过；`tests.test_desktop_widgets` 15 个测试通过。
- 收尾验证：`tests.test_desktop_settings` 8 个通过；`tests.test_desktop_widgets` 15 个通过；`tests.test_desktop_app` 3 个通过；全量 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 123 个测试；桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅有 CRLF 提示。
- 桌面面板尺寸持久化已提交：`49c487f feat: 持久化桌面面板尺寸`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `49c487f`。
- 2026-05-20：用户要求一口气完成安装包前 3 个阶段，但每阶段单独 push，执行记录和文档分清楚。
- 写入 `.codex/desktop-installation-three-stage-plan.md` 和 `word/2026-05-20-jarvis-lite-desktop-installation-plan.md`。
- 三阶段边界：阶段 1 桌面体验收口；阶段 2 打包前准备；阶段 3 Windows 可分发安装产物。二进制产物输出到项目外目录，不提交 Git。
- 阶段 1 按 TDD 新增应用图标和应用身份测试，先确认缺少 `desktop_app_icon_path()` 且 `QApplication.applicationName()` 仍为 `python`。
- 阶段 1 新增 `src/jarvis_lite/desktop/assets/app-icon.svg`、`desktop_app_icon_path()`，并统一设置 app、窗口、面板和托盘图标。
- 阶段 1 专项验证：`tests.test_desktop_assets tests.test_desktop_app tests.test_desktop_tray` 共 15 个测试通过。
- 阶段 1 收尾验证：全量 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 125 个测试；桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅有 CRLF 提示。
- 阶段 1 已提交：`8fb4da0 feat: 收口桌面应用体验`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `8fb4da0`。
- 阶段 2 按 TDD 新增冻结运行态和桌面打包准备测试，先确认冻结运行态仍指向源码目录且 `jarvis_lite.desktop.packaging` 不存在。
- 阶段 2 更新 `config.py`，冻结应用默认使用 `%LOCALAPPDATA%\Jarvis Lite` 作为用户数据根目录。
- 阶段 2 新增 `jarvis_lite.desktop.packaging`、`packaging/windows/desktop_launcher.py`、`scripts/build_desktop_exe.py` 和 `desktop-build` 可选依赖。
- 阶段 2 专项验证：`tests.test_config tests.test_desktop_packaging` 共 5 个测试通过。
- 阶段 2 收尾验证：全量 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 129 个测试；桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅有 CRLF 提示。
- 阶段 2 已提交：`b31c470 chore: 增加桌面打包准备`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `b31c470`。
- 阶段 3 按 TDD 新增 `tests/test_windows_installer.py`，先确认 `jarvis_lite.desktop.windows_installer` 不存在。
- 阶段 3 新增 `jarvis_lite.desktop.windows_installer` 和 `scripts/build_windows_installer.py`，生成安装脚本、卸载脚本和 IExpress SED 文件。
- 执行 `.\.venv\Scripts\python.exe -m pip install -e ".[desktop-build]"` 安装 PyInstaller 6.20.0。
- 执行 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py`，生成 `E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe` 和 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包 exe smoke：`Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。
- 阶段 3 收尾验证：`tests.test_windows_installer` 3 个通过；全量 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 132 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅有 CRLF 提示。
- 阶段 3 已提交：`16e6829 build: 增加 Windows 桌面安装包`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `16e6829`。
- 2026-05-20：用户要求继续下一任务；根据 Windows 安装器进度文档后续建议，本阶段选择“Windows 安装产物元数据收口”。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用本地文件读取、`rg`、`unittest`、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `word/2026-05-20-jarvis-lite-desktop-windows-metadata-design.md` 和 `.codex/desktop-windows-metadata-plan.md`，范围限定为 Windows 图标、版本资源和安装器版本号串联，不做代码签名、替换安装器或硬件入口。
- 本阶段 RED 验证：`tests.test_desktop_packaging` 因缺少版本资源函数失败；`tests.test_windows_installer` 因安装脚本不支持 `version` 参数失败。
- 新增 `scripts/generate_windows_icon.py` 并生成 `packaging/windows/JarvisLite.ico`。
- 更新桌面打包配置，PyInstaller 参数现在包含 `--icon` 和 `--version-file`；构建前写入 `JarvisLite.version.txt`。
- 更新 Windows 安装脚本，卸载注册表 `DisplayVersion` 使用项目版本号。
- 执行 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py`，PyInstaller 日志显示 `Copying icon to EXE` 和 `Copying version information to EXE`。
- 专项验证：`tests.test_desktop_packaging` 7 个通过，`tests.test_windows_installer` 4 个通过。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 137 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；打包 exe smoke 退出码为 0；Windows `VersionInfo` 显示版本 `0.1.0`；`git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- Windows 安装产物元数据收口已提交：`f0729f2 build: 收口 Windows 安装产物元数据`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `f0729f2`。
- 2026-05-20：用户要求先检查是否还有需要优化或调试的地方；本轮做新鲜验证和后续建议检查。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用本地文件读取、`rg`、`unittest`、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 审查结果：`main` 与 `origin/main` 同步；全量测试 137 个通过；源码桌面 smoke 正常；打包 exe smoke 退出码为 0；打包 exe `VersionInfo` 可读。未发现必须先修的回归问题。
- 后续建议中代码签名需要证书，Inno/NSIS 需要外部安装器工具；本阶段选择不依赖外部条件的“桌面开机自启动”。
- 写入 `word/2026-05-20-jarvis-lite-desktop-launch-at-login-design.md` 和 `.codex/desktop-launch-at-login-plan.md`，范围限定为当前用户 Startup 快捷方式和设置面板开关，不做硬件入口、系统服务、注册表启动项或代码签名。
- 本阶段 RED 验证：`tests.test_desktop_autostart` 因缺少 `jarvis_lite.desktop.autostart` 失败；`tests.test_desktop_settings` 因缺少 `launch_at_login` 失败；`tests.test_desktop_widgets` 因面板设置不支持开机启动失败；`tests.test_desktop_app` 因缺少 `apply_panel_settings` 失败。
- 新增 `src/jarvis_lite/desktop/autostart.py`，实现当前用户 Startup 快捷方式配置、PowerShell 创建脚本、启用、关闭、同步和状态检查。
- 更新 `DesktopSettings`，新增 `launch_at_login` 并在保存位置、保存面板尺寸时保留该偏好。
- 更新 `AssistantPanel`，设置区域新增“开机启动”复选框；更新 `DesktopPetWindow.apply_preferences()` 保存该偏好。
- 更新 `desktop.app`，新增 `apply_panel_settings()`，设置变更时同步当前用户级开机启动。
- 审查当前实现时发现：如果每次面板设置变化都同步 Startup，调整透明度或尺寸时会重复调用 PowerShell；新增测试并优化为只有 `launch_at_login` 值变化时才同步。
- 专项验证：`tests.test_desktop_autostart` 7 个通过；`tests.test_desktop_settings` 8 个通过；`tests.test_desktop_widgets` 15 个通过；`tests.test_desktop_app` 6 个通过。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 146 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 执行 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 重新生成项目外 exe 和安装器；打包 exe smoke 退出码为 0。
- 桌面开机自启动已提交：`a693ee6 feat: 增加桌面开机自启动`。
- push 首次失败：`OpenSSL SSL_read: Connection was reset, errno 10054`；第二次失败：连接 GitHub 443 超时。执行 `Test-NetConnection github.com -Port 443` 后确认端口连通，再次执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `a693ee6`。
- 2026-05-20：用户要求继续；本阶段选择“桌面主题预设”，作为不依赖硬件、证书或外部安装器工具的桌面体验优化。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用本地文件读取、`rg`、`unittest`、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `word/2026-05-20-jarvis-lite-desktop-theme-presets-design.md` 和 `.codex/desktop-theme-presets-plan.md`，范围限定为深色/浅色主题预设、运行态保存和面板控件，不做硬件入口、图片下载、复杂皮肤市场、安装器替换或代码签名。
- 本阶段 RED 验证：`tests.test_desktop_style` 因缺少主题 API 失败；`tests.test_desktop_settings` 因缺少 `theme_name` 失败；`tests.test_desktop_widgets` 因面板和小助手缺少主题设置失败；`tests.test_desktop_app` 因设置同步不传递主题失败。
- 更新 `src/jarvis_lite/desktop/app_style.py`，新增 `DesktopTheme`、`THEME_PRESETS`、主题名规范化、主题显示名、面板样式和小助手样式生成函数。
- 更新 `DesktopSettings`，新增 `theme_name`，运行态保存读取会规范化主题，保存位置、偏好和面板尺寸时保留主题。
- 更新 `AssistantPanel`，设置区新增主题下拉选择，面板变更会立即刷新主题并通知设置监听器。
- 更新 `DesktopPetWindow`，启动和偏好变更时应用主题，小助手样式与面板主题同步。
- 更新 `desktop.app.apply_panel_settings()`，主题随面板设置同步到桌面小助手。
- 专项验证：`tests.test_desktop_style` 3 个通过；`tests.test_desktop_settings` 9 个通过；`tests.test_desktop_widgets` 16 个通过；`tests.test_desktop_app` 6 个通过。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 151 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 执行 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 重新生成项目外 exe 和安装器；打包 exe smoke 退出码为 0。
- 桌面主题预设已提交：`5c7698b feat: 增加桌面主题预设`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `5c7698b`。
- 2026-05-20：用户继续要求推进；本阶段选择“桌面面板快捷命令收口”，修正面板无参数快捷按钮范围，避免 `/organize-preview` 这类需要参数的命令被一键触发后直接报用法错误。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用本地文件读取、`rg`、`unittest`、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `word/2026-05-20-jarvis-lite-desktop-panel-quick-commands-design.md` 和 `.codex/desktop-panel-quick-commands-plan.md`，范围限定为无参数快捷命令筛选、面板按钮和托盘复用，不做硬件入口、参数向导、安装器替换或代码签名。
- 本阶段 RED 验证：`tests.test_desktop_bridge` 因缺少 `direct_quick_commands()` 失败；`tests.test_desktop_widgets` 因面板缺少快捷命令文本和按钮入口失败；`tests.test_desktop_tray` 因无法复用无参数快捷命令集合失败。
- 更新 `src/jarvis_lite/desktop/bridge.py`，新增 `DIRECT_QUICK_COMMAND_PROMPTS` 和 `direct_quick_commands()`，完整能力清单继续保留 `/organize-preview`。
- 更新 `AssistantPanel`，快捷按钮改为只使用无参数命令，并新增 `quick_command_texts()` 和 `quick_command_button()`。
- 更新 `DesktopTrayController`，托盘快捷命令复用 `direct_quick_commands()`，删除本地重复筛选常量。
- 专项验证：`tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray` 共 30 个通过。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 154 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 执行 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 重新生成项目外 exe 和安装器；打包 exe smoke 退出码为 0；安装器路径 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，大小 47460352。
- 桌面面板快捷命令收口已提交：`0d33573 feat: 收口桌面面板快捷命令`。
- 使用一次性 OpenSSL 后端执行 `git -c http.sslBackend=openssl push origin main`，远程 `main` 已更新到 `0d33573`。
- 2026-05-20：用户提出安装后的卸载和更新体验问题；本轮开始第 4 阶段“安装生命周期收口”，更新机制作为第 5 阶段紧接着处理。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用本地文件读取、`rg`、`unittest`、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `word/2026-05-20-jarvis-lite-desktop-install-lifecycle-design.md` 和 `.codex/desktop-install-lifecycle-plan.md`，范围限定为卸载清理、覆盖安装前关闭运行进程、卸载保留用户数据和卸载注册表元数据；不做自动更新下载器、安装器替换、代码签名或硬件入口。
- 本阶段 RED 验证：`tests.test_windows_installer` 因安装脚本缺少进程关闭、`DisplayIcon`、`QuietUninstallString` 失败；因卸载脚本缺少 Startup 清理、运行进程关闭和用户数据保留约定失败。
- 更新 `render_install_script()`：复制 exe 前尝试关闭 `JarvisLite.exe`，并写入 `DisplayIcon` 和 `QuietUninstallString`。
- 更新 `render_uninstall_script()`：卸载前尝试关闭 `JarvisLite.exe`，清理 Startup 快捷方式，保留 `%LOCALAPPDATA%\Jarvis Lite` 用户数据目录并输出提示。
- 专项验证：`.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v` 通过，当前 7 个安装器测试。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 157 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 执行 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 重新生成项目外 exe 和安装器；打包 exe smoke 退出码为 0；安装器路径 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，大小 47460352。
- 桌面安装生命周期收口已提交：`34db26a build: 收口安装卸载生命周期`。
- push 前两次失败：OpenSSL 连接 reset；`Test-NetConnection github.com -Port 443` 显示 443 连通；`schannel` 后端超时。随后使用 `git -c http.version=HTTP/1.1 -c http.sslBackend=openssl push origin main` 成功，远程 `main` 已更新到 `34db26a`。
- 2026-05-20：用户要求继续；本轮开始第 5 阶段“更新检查第一版”，实现清单式手动检查更新和下载入口提示，不做自动下载、静默安装、安装器替换、代码签名或硬件入口。
- 写入 `word/2026-05-20-jarvis-lite-desktop-update-check-design.md` 和 `.codex/desktop-update-check-plan.md`。
- 本阶段 RED 验证：`tests.test_update` 因 `jarvis_lite.update` 不存在失败；`tests.test_agent` 因 `/update-status` 未接入失败；`tests.test_desktop_bridge` 因快捷命令缺少 `/update-status` 失败；`tests.test_desktop_widgets` 因面板快捷按钮缺少“检查更新”失败。
- 新增 `src/jarvis_lite/update.py`，支持本地路径或 `http/https` URL 更新清单、数字段版本比较、更新结果数据结构和用户可读状态文本。
- 更新 `JarvisAgent`，新增 `/update-status [清单路径或URL]` 命令；未传源时读取 `JARVIS_LITE_UPDATE_MANIFEST_URL`，未配置时输出配置提示。
- 更新桌面快捷命令，新增“检查更新”按钮；更新检查失败会映射为桌面错误状态。
- 专项验证：`tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray` 共 64 个通过。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 162 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 未发现空白错误，仅出现 CRLF 换行提示。
- 执行 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 重新生成项目外 exe 和安装器；打包 exe smoke 退出码为 0；安装器路径 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，大小 47464448。
- 桌面更新检查第一版已提交：`9822893 feat: 增加桌面更新检查入口`。
- 使用 `git -c http.version=HTTP/1.1 -c http.sslBackend=openssl push origin main` 成功，远程 `main` 已更新到 `9822893`。
- 2026-05-21：用户要求检查当前进度并继续下一阶段。检查 README、`verification.md`、`.codex/operations-log.md`、`word/2026-05-20-jarvis-lite-desktop-update-check-progress.md` 和 git log，确认当前进度停在“桌面更新检查第一版”，最新提交 `9822893` 已同步 `origin/main`，工作区干净。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用本地文件读取、`rg`、`unittest`、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 根据最新进度文档的后续建议，本阶段选择“桌面更新下载体验”：新增 `/update-download [清单路径或URL]`，把更新安装包下载或复制到项目外 `jarvis-lite-runtime/updates/`，不做静默安装、自动运行安装器、包校验、回滚、代码签名或硬件入口。
- 写入 `word/2026-05-21-jarvis-lite-desktop-update-download-design.md`、`.codex/context-scan-update-download.json` 和 `.codex/desktop-update-download-plan.md`。
- 本阶段 RED 验证：`tests.test_update` 因缺少 `describe_update_download` 和 `download_update` 导入失败；`tests.test_agent` 因 `/update-download` 返回未知命令失败；`tests.test_desktop_bridge` 和 `tests.test_desktop_widgets` 因缺少下载快捷入口失败。
- 更新 `src/jarvis_lite/update.py`，新增 `UpdateDownloadResult`、`update_download_dir()`、`download_update()` 和 `describe_update_download()`；下载目录为项目外 `jarvis-lite-runtime/updates/`。
- 更新 `JarvisAgent`，新增 `/update-download [清单路径或URL]` 命令，并记录下载更新安装包的工具日志。
- 更新桌面快捷命令，新增“下载更新”；桌面桥接层把 `更新下载失败：` 识别为错误状态。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_update tests.test_agent tests.test_desktop_bridge tests.test_desktop_widgets -v` 通过，当前 60 个相关测试；过程中修复 Windows 本地路径被 `urlparse` 识别为 `c` 协议的问题。
- 更新 README、`word/文档索引.md`、`word/2026-05-21-jarvis-lite-desktop-update-download-progress.md`、`verification.md` 和 `.codex/testing.md`，记录 `/update-download`、运行态下载目录和验证结果。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 166 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示；`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 重新生成安装器；打包 exe smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`，退出码为 0。
- 用户要求 push 并重新打安装包用于本地测试；执行 `git -c http.version=HTTP/1.1 -c http.sslBackend=openssl push origin main` 成功，远程 `main` 已更新到 `0b7237d`。
- 执行 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 重新生成安装包，输出 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，大小 `47468544` 字节，生成时间 `2026-05-21 10:36:38`。
- 执行打包 exe smoke，`Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru` 退出码为 0，输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 用户开始本地安装测试前，补充更新 `word/2026-05-21-jarvis-lite-desktop-update-download-progress.md` 和 `verification.md`，记录推送提交、安装包路径、大小、生成时间和本地测试重点。
- 2026-05-21：用户确认自然语言是语音和后续大模型接入的基础，并要求把本次内容与之前目标整理成关联方案后开始执行。
- 写入 `word/2026-05-21-jarvis-lite-natural-language-brain-design.md` 和 `.codex/natural-language-brain-plan.md`，明确本地确定性大脑与大模型外脑分层：本地层负责可测试的意图、记忆和工具执行，大模型后续作为百科、复杂理解和规划顾问。
- 本阶段 RED 验证：`tests.test_memory` 因 `我是你的什么人，你知道吗` 未识别为身份问题失败；`tests.test_agent` 因自然语言能力询问、生成日报、查看知识库、检查更新和打开 D 盘均落入通用兜底失败；`/status` 旧断言仍要求“阶段 1 状态”。
- 新增 `src/jarvis_lite/intent.py`，提供 `NaturalLanguageIntent` 和 `parse_natural_language_intent()`，支持第一批能力询问、知识库、常用目录、日报、更新、下载更新和打开盘符意图。
- 更新 `memory.py`，疑问句不再被 `我是...` 写入身份记忆，并扩展身份问句识别。
- 更新 `agent.py`，在资料问答前接入自然语言意图路由；新增能力摘要；`打开D盘` 可记录打开 `D:\` 请求；`/status` 更新为当前完整状态。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v` 通过，当前 46 个相关测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 173 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 自然语言本地意图层已提交：`d115d24 feat: 增加自然语言本地意图层`。
- 重新执行 `.\.venv\Scripts\python.exe scripts\build_windows_installer.py`，生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，大小 `47472640` 字节，生成时间 `2026-05-21 11:17:54`；打包 exe smoke 退出码为 0。
- 2026-05-21：用户要求继续开始一个任务；本轮继续自然语言本地大脑方向，选择“常用目录别名自然语言”，让“打开项目目录”“整理项目目录”复用已登记目录。
- 本阶段 RED 验证：`tests.test_agent` 中 `打开项目目录` 未记录打开目录请求；`整理项目目录` 落入通用兜底。
- 更新 `intent.py`，新增 `open_directory_alias` 和 `organize_directory_alias` 意图；更新 `agent.py`，分别复用 `_open_directory()` 与 `_organize_preview()`。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 39 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 175 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 常用目录自然语言别名已提交：`391516d feat: 支持常用目录自然语言别名`。
- 2026-05-21：继续自然语言参数补全，本轮选择“已知桌面目录自然语言”，让未登记常用目录时也可说“整理桌面”和“打开桌面”。
- 写入 `.codex/natural-language-known-directories-plan.md`，范围限定为桌面目录 fallback，不移动文件、不删除文件、不启动外部应用。
- 本阶段 RED 验证：新增 2 个 Agent 测试先分别因 `整理桌面` 找不到常用目录、`打开桌面` 未写入打开记录失败。
- 更新 `agent.py`，`_find_common_directory()` 在已登记目录未命中时 fallback 到系统已知目录；当前支持 `桌面` / `desktop`，候选路径为 `Path.home() / "Desktop"` 和 `Path.home() / "桌面"`。
- 专项 GREEN 验证：新增 2 个已知桌面目录测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 41 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 177 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 用户要求 push 并继续任务；推送前重新验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，177 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 无输出。执行 `git -c http.version=HTTP/1.1 -c http.sslBackend=openssl push origin main` 成功，远程 `main` 已更新到 `2006571`。
- 2026-05-21：继续自然语言参数补全，本轮选择“资料标签自然语言”，让“给 note.txt 打标签 项目 Python”“把 note.txt 标记为 私人资料”复用现有 `/tag` 能力。
- 写入 `.codex/natural-language-tagging-plan.md`，范围限定为明确文件名和标签，不做“这个资料”上下文指代，不做模糊文件名搜索。
- 本阶段 RED 验证：新增 2 个 Agent 测试先分别落入普通兜底和资料问答，均未更新标签。
- 更新 `intent.py`，新增保留空格的自然语言预处理、资料标签意图解析和标签文本拆分，解析结果直接返回 `/tag 文件名 标签...` 命令意图。
- 专项 GREEN 验证：新增 2 个自然语言标签测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 43 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 179 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 2026-05-21：用户要求继续一个任务；本轮选择“自然语言导入资料”，让明确文件路径表达复用现有 `/import` 能力。
- 写入 `.codex/natural-language-import-plan.md`，范围限定为明确路径导入；不做“这个文件”上下文指代、文件选择器、拖拽入口或模糊搜索。
- 本阶段 RED 验证：新增 2 个 Agent 测试先落入普通兜底，未导入资料。
- 更新 `intent.py`，新增自然语言导入意图解析，支持 `导入 <路径> 到知识库` 和 `把 <路径> 导入知识库`；解析结果直接返回 `/import "<路径>"`。
- 专项 GREEN 验证：新增 2 个自然语言导入测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 45 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 181 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 2026-05-21：用户要求继续下一个任务；本轮选择“最近资料上下文”，让导入单个资料后可说“给这个资料打标签 项目 Python”。
- 写入 `.codex/natural-language-recent-document-plan.md`，范围限定为最近一次成功导入的单个资料；没有最近资料时明确提示，目录批量导入不设置最近单个资料。
- 本阶段 RED 验证：新增 2 个 Agent 测试先把“这个资料”当成真实文件名，未能更新最近导入资料或提示缺少最近资料。
- 更新 `intent.py`，`NaturalLanguageIntent` 新增 `tags` 字段，`这个资料`、`这份资料`、`刚才的资料`、`最近的资料` 会解析为 `tag_recent_document`。
- 更新 `agent.py`，记录最近成功导入的单个资料；`tag_recent_document` 复用现有 `/tag` 流程，无最近资料时输出明确提示。
- 专项 GREEN 验证：新增 2 个最近资料上下文测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 47 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 183 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 2026-05-21：继续自然语言上下文方向；重新验证并提交最近资料上下文：`6b1b1c4 feat: 增加最近资料自然语言上下文`。
- 本轮选择“最近目录上下文”，让用户打开或整理一个目录后可继续说“整理这个目录”“打开这个目录”，为后续语音输入减少重复参数。
- 写入 `.codex/natural-language-recent-directory-plan.md`，范围限定为当前 Agent 实例内的最近目录，不做跨会话持久化、不实际移动或删除文件。
- 本阶段 RED 验证：新增 2 个 Agent 测试先把“这个目录”当成普通别名“这个”，未能使用最近目录或提示缺少最近目录。
- 更新 `intent.py`，将“这个/刚才的/最近的/当前目录”解析为最近目录打开或整理意图。
- 更新 `agent.py`，记录成功打开或整理的目录，并复用现有目录打开记录和整理预览流程处理最近目录。
- 专项 GREEN 验证：新增 2 个最近目录上下文测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 49 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 185 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近目录上下文已提交：`40047ef feat: 增加最近目录自然语言上下文`。
- 2026-05-21：用户要求继续；本轮选择“最近搜索结果上下文”，让 `/ask` 或普通问题命中资料后可以说“给这个结果打标签 运行环境”。
- 写入 `.codex/natural-language-recent-search-result-plan.md`，范围限定为记录第一条命中的 data 文件；不改变检索排序、得分、回答格式，不做结果编号选择。
- 本阶段 RED 验证：新增 2 个 Agent 测试先把“这个结果”当成真实文件名，标签更新失败。
- 更新 `knowledge.py`，新增 `find_data_matches()` 和 `answer_from_matches()`，让 Agent 能使用结构化命中结果并继续复用原回答格式。
- 更新 `agent.py`，`/ask` 和普通资料问答命中时记录第一条命中资料为最近资料。
- 更新 `intent.py`，把“这个结果”“这条结果”“刚才的结果”“最近的结果”解析为最近资料打标签意图。
- 专项 GREEN 验证：新增 2 个最近搜索结果上下文测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v` 通过，当前 23 个 Knowledge 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 51 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 187 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近搜索结果上下文已提交：`80b15a6 feat: 支持最近搜索结果上下文`。
- 2026-05-21：用户要求继续；本轮选择“最近搜索结果编号选择”，让多条问答结果后可说“给第二条结果打标签 运行环境”。
- 写入 `.codex/natural-language-result-index-plan.md`，范围限定为最近一次问答结果列表；不改变检索排序、过滤和回答格式，不做跨会话持久化。
- 本阶段 RED 验证：新增 2 个 Agent 测试先把“第二条结果”当成真实文件名，标签更新失败或缺少最近结果提示。
- 更新 `intent.py`，`NaturalLanguageIntent` 新增 `result_index` 字段，并解析 `第二条结果`、`第2条结果` 为 `tag_numbered_search_result`。
- 更新 `agent.py`，保存最近问答结果路径列表，支持按序号复用现有 `/tag` 流程；没有最近结果或序号越界时返回明确提示。
- 专项 GREEN 验证：新增 2 个最近搜索结果编号选择测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 53 个 Agent 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v` 通过，当前 23 个 Knowledge 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 189 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 2026-05-21：用户要求 push 并继续；推送前验证 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 189 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 无输出。执行 `git -c http.version=HTTP/1.1 -c http.sslBackend=openssl push origin main` 成功，远程 `main` 已更新到 `9de4186`。
- 2026-05-21：push 后继续自然语言上下文方向；本轮选择“查看编号搜索结果”，让用户问答后可说“查看第二条结果”读取对应资料内容。
- 写入 `.codex/natural-language-read-result-plan.md`，范围限定为读取 data 文件内容，不启动外部应用、不改变检索排序、不跨会话持久化。
- 本阶段 RED 验证：新增 2 个 Agent 测试先落入长期记忆兜底，未能读取第二条资料或提示缺少最近搜索结果。
- 更新 `intent.py`，新增 `read_numbered_search_result` 意图，支持 `查看第二条结果`、`查看第2条结果` 等简单表达。
- 更新 `agent.py`，复用最近搜索结果路径列表和 `read_data_file` 工具读取对应 data 文件，返回 `data/...` 路径和文件内容。
- 专项 GREEN 验证：新增 2 个查看编号搜索结果测试通过；结果编号相关 4 个测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 55 个 Agent 测试。
- 查看编号搜索结果已提交：`e2943ad feat: 支持查看编号搜索结果`。
- 2026-05-21：用户要求继续下一个任务；本轮选择“最近搜索结果持久化”，减少重启或新 Agent 实例后丢失上下文的问题。
- 写入 `.codex/natural-language-persistent-search-context-plan.md`，范围限定为最近搜索结果路径列表持久化到项目外运行态文件。
- 本阶段 RED 验证：新增 1 个 Agent 测试先证明新 Agent 实例无法恢复最近搜索结果。
- 更新 `runtime_context.py`，新增 `RuntimeContext`、`runtime_context_path()`、`load_runtime_context()`、`save_runtime_context()`，文件路径为 `jarvis-lite-runtime/agent-context.json`。
- 更新 `agent.py`，初始化时读取运行态上下文；问答命中时写入最近搜索结果路径列表。
- 调试发现 Agent 测试直接使用系统临时目录作为项目根，会把运行态文件写到公共临时父目录，导致跨测试串扰；已把 Agent 测试项目根改为临时目录下的 `jarvis-lite` 子目录。
- 专项 GREEN 验证：新增 1 个最近搜索结果持久化测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 56 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 192 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 2026-05-21：用户要求继续下一个阶段；本轮选择“最近上下文状态查询”，让用户能问“查看最近上下文”“你还记得刚才什么”。
- 写入 `.codex/context-scan-natural-language-context-status.json` 和 `.codex/natural-language-context-status-plan.md`；当前 code-index、sequential-thinking、shrimp-task-manager 不在可用工具列表中，已降级为 `rg`、文件读取、`update_plan` 和本地记录。
- 本阶段 RED 验证：新增 3 个 Agent 测试先全部落入长期记忆兜底，未能输出最近上下文状态。
- 更新 `intent.py`，新增 `recent_context_status` 意图，支持“查看最近上下文”“最近上下文状态”“你还记得刚才什么”等表达。
- 更新 `agent.py`，新增最近上下文状态输出，列出最近资料、最近目录和最近搜索结果；没有上下文时提示先提问、导入资料或打开/整理目录。
- 专项 GREEN 验证：新增 3 个最近上下文状态测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 59 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 195 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 2026-05-21：电脑重启后恢复任务。检查 `git status -sb`，确认工作区干净，`main` 比 `origin/main` 超前 3 个提交；最新本地提交为 `5bf9e72 feat: 支持最近上下文状态查询`。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 根据上一轮审查报告遗留风险，本阶段选择“最近资料和最近目录持久化”：复用现有 `RuntimeContext` 与项目外 `jarvis-lite-runtime/agent-context.json`，不新增数据库、外部依赖或真实目录打开行为。
- 写入 `.codex/context-scan-natural-language-persistent-recent-context.json` 和 `.codex/natural-language-persistent-recent-context-plan.md`。
- 本阶段 RED 验证：新增 2 个 Agent 测试先分别证明新 Agent 实例无法恢复最近导入资料和最近目录。
- 更新 `runtime_context.py`，新增 `RuntimeDirectoryContext`、`recent_document_path` 和 `recent_directory` 运行态字段，继续兼容缺失或损坏上下文文件。
- 更新 `agent.py`，初始化时恢复最近资料和最近目录；资料、搜索结果、目录变化时统一保存完整运行态上下文。
- 专项 GREEN 验证：新增 2 个持久化测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 61 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 197 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 更新 README、`word/jarvis-lite-overall-plan.md`、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`verification.md` 和 `.codex/testing.md`，记录最近资料和最近目录持久化结果。
- 用户要求先 push 并继续下一个任务。推送前验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 197 个测试；`git diff --check` 无输出。执行 `git -c http.version=HTTP/1.1 -c http.sslBackend=openssl push origin main` 成功，远端 `main` 已更新到 `d576cdf`。
- 继续自然语言本地大脑后续建议，本轮选择“经验记忆第一版”：新增独立经验记忆文件和明确记录/查看入口，不自动抽取日志、不接入大模型、不改变 `/remember` 身份偏好记忆。
- 写入 `.codex/context-scan-experience-memory.json` 和 `.codex/experience-memory-plan.md`。
- 本阶段 RED 验证：`tests.test_memory` 先因缺少 `append_experience` 和 `read_experiences` 导入失败；Agent 入口测试先因 `/experience`、`/experiences` 未知命令、“记住这个经验”误写长期记忆、“查看经验记忆”落入兜底失败。
- 更新 `memory.py`，新增 `memory/experiences.md` 读写函数和重复经验去重；`parse_identity_fact()` 不再吞掉“记住这个经验：...”。
- 更新 `intent.py`，新增经验记录和经验查看自然语言意图。
- 更新 `agent.py`，新增 `/experience`、`/experiences`，并在帮助、能力摘要和状态中展示经验记忆。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_memory -v` 通过，当前 11 个 Memory 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 65 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 203 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 更新 README、`word/jarvis-lite-overall-plan.md`、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`verification.md` 和 `.codex/testing.md`，记录经验记忆第一版。
- 2026-05-21：用户要求继续下一个任务。本轮选择“经验引用第一版”：让最近经验出现在能力摘要和日报中，不做经验搜索、分类、评分或自动抽取。
- 写入 `.codex/context-scan-experience-reference.json` 和 `.codex/experience-reference-plan.md`。
- 本阶段 RED 验证：`tests.test_memory` 先因缺少 `list_recent_experiences` 导入失败；能力摘要先没有“最近经验”；日报先没有“经验记忆”段。
- 更新 `memory.py`，新增 `list_recent_experiences(paths, limit=3)`，从 `memory/experiences.md` 读取最近经验，最新在前。
- 更新 `agent.py`，能力摘要在已有经验时展示最近经验列表。
- 更新 `automation.py`，日报新增“经验记忆”段，列出最近经验或暂无经验提示。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent tests.test_automation -v` 通过，当前 83 个相关测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 205 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`verification.md` 和 `.codex/testing.md`，记录经验引用第一版。
- 2026-05-21：用户表示继续推进。本轮选择“经验搜索第一版”：新增按关键词检索经验记忆，范围限定为简单包含匹配，不做分词、模糊匹配、评分或大模型改写。
- 写入 `.codex/context-scan-experience-search.json` 和 `.codex/experience-search-plan.md`。
- 本阶段 RED 验证：新增 Memory 和 Agent 测试先分别因缺少 `search_experiences()`、`/experience-search` 未知命令、自然语言搜索经验未映射而失败。
- 更新 `memory.py`，新增 `search_experiences(paths, query, limit=5)`，复用最近经验读取并按最新优先返回包含关键词的经验。
- 更新 `agent.py`，新增 `/experience-search 关键词`，无关键词提示用法，无匹配项输出明确空结果，匹配时编号展示经验。
- 更新 `intent.py`，新增“搜索经验 导入”“查找经验：导入”“经验搜索 导入”等自然语言映射，并放在经验记录解析前避免歧义。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_memory tests.test_agent -v` 通过，当前 83 个相关测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 210 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录经验搜索第一版。
- 经验搜索第一版已提交：`149bf97 feat: 支持经验搜索`。
- 按用户前序“先 push”要求执行 `git -c http.version=HTTP/1.1 -c http.sslBackend=openssl push origin main`，远端 `main` 已从 `d576cdf` 更新到 `149bf97`。
- 2026-05-21：继续下一个任务。本轮选择“经验操作建议第一版”：让“我该怎么导入资料”这类问题引用已有经验并提示后续命令；范围限定为确定性关键词匹配，不做开放式规划或大模型总结。
- 写入 `.codex/context-scan-experience-advice.json` 和 `.codex/experience-advice-plan.md`。
- 本阶段 RED 验证：新增 4 个 Agent 测试先分别因 `/experience-advice` 未知命令和“我该怎么导入资料”落入资料问答失败。
- 更新 `agent.py`，新增 `/experience-advice 关键词` 和 `_experience_advice()`，复用 `search_experiences()` 输出相关经验和后续 `/experience-search` 提示。
- 更新 `intent.py`，新增“我该怎么...”“...有什么经验”“给我...的建议”等经验建议表达解析。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 74 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录经验操作建议第一版。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 214 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 经验操作建议第一版已提交并推送：`9b79a16 feat: 增加经验操作建议`，远端 `main` 同步到该提交。
- 2026-05-22：用户要求继续。本轮选择“经验建议命令联动第一版”，让 `/experience-advice` 在相关经验之外直接给出可执行命令建议。
- 写入 `.codex/context-scan-experience-command-suggestions.json` 和 `.codex/experience-command-suggestions-plan.md`。
- 本阶段 RED 验证：新增 3 个 Agent 测试先因 `/experience-advice` 输出缺少“可执行命令”和具体命令建议而失败。
- 更新 `agent.py`，新增 `_experience_command_suggestions()`，按固定关键词映射 `/import`、`/kb`、`/tag`、`/daily-report`、目录、更新、语音和经验命令。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 77 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录经验建议命令联动第一版。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 217 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 经验建议命令联动第一版已提交并推送：`6cd27b6 feat: 增加经验建议命令提示`，远端 `main` 同步到该提交。
- 2026-05-22：用户要求继续。本轮选择“经验建议引用最近上下文第一版”，让 `/experience-advice 这个资料` 和 `/experience-advice 这个目录` 输出当前对象和具体命令建议。
- 写入 `.codex/context-scan-experience-context-advice.json` 和 `.codex/experience-context-advice-plan.md`。
- 本阶段 RED 验证：新增 3 个 Agent 测试先因 `/experience-advice 这个资料/这个目录` 未输出当前资料、当前目录和具体命令建议而失败。
- 更新 `agent.py`，新增最近资料/目录查询识别、经验搜索关键词映射和上下文行输出；最近资料建议 `/read`、`/tag`、`/ask`，最近目录建议 `/organize-preview`、`/dir-open`。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 80 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录经验建议引用最近上下文第一版。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 220 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 经验建议引用最近上下文第一版已提交并推送：`f254121 feat: 经验建议引用最近上下文`，远端 `main` 同步到该提交。
- 2026-05-22：用户要求继续。本轮选择“最近建议编号查看第一版”，让经验建议生成的命令建议可在当前会话内按编号查看。
- 写入 `.codex/context-scan-recent-advice-suggestions.json` 和 `.codex/recent-advice-suggestions-plan.md`。
- 本阶段 RED 验证：新增 3 个 Agent 测试先因“查看第一条建议/第二条建议”未被自然语言意图层识别而落入普通兜底。
- 更新 `agent.py`，当前 Agent 实例记录最近一次经验建议生成的命令建议列表，并新增编号读取方法。
- 更新 `intent.py`，新增 `read_numbered_advice_suggestion` 意图，支持“查看第一条建议”“查看第2条建议”。
- 专项 GREEN 验证：`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 83 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录最近建议编号查看第一版。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 223 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近建议编号查看第一版已提交并推送：`ca54783 feat: 支持查看最近建议`，远端 `main` 同步到该提交。
- 2026-05-22：继续下一个任务。本轮选择“最近建议持久化第一版”，让新建 `JarvisAgent` 实例可以继续读取上一轮经验建议编号。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-persistent-advice-suggestions.json` 和 `.codex/persistent-advice-suggestions-plan.md`；设计复用现有 `RuntimeContext` 与项目外 `jarvis-lite-runtime/agent-context.json`。
- 本阶段 RED 验证：新增 1 个 Agent 测试先证明新建 `JarvisAgent` 无法恢复上一轮最近建议。
- 更新 `runtime_context.py`，新增 `recent_advice_suggestions` 运行态字段，读取时复用字符串列表解析。
- 更新 `agent.py`，初始化时恢复最近建议，生成建议后写入完整运行态上下文。
- 专项 GREEN 验证：最近建议持久化单测通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 84 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 224 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近建议持久化第一版已提交：`d21a4fd feat: 持久化最近建议`。
- 首次 push 因 GitHub HTTPS 连接重置失败；确认本地 `main` 仅超前远端 1 个提交、远端 URL 正常后重试成功，远端 `main` 已从 `ca54783` 更新到 `d21a4fd`。
- 2026-05-22：用户继续要求推进。本轮选择“最近建议执行前确认第一版”，让“执行第 N 条建议”先展示将执行的命令，确认后再复用现有命令路径。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-advice-execution-confirmation.json` 和 `.codex/advice-execution-confirmation-plan.md`；设计限定为当前实例内待确认状态，不持久化 pending command。
- 本阶段 RED 验证：新增 3 个 Agent 测试先证明“执行第二条建议”“执行第一条建议”“确认执行”均落入长期记忆兜底。
- 更新 `intent.py`，新增执行编号建议、确认执行和取消执行自然语言意图。
- 更新 `agent.py`，新增当前实例内待确认建议命令；含占位符建议要求补全参数，确认后复用 `self.handle(command)` 执行。
- 专项 GREEN 验证：新增 3 个最近建议执行前确认测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 87 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 227 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 修正 README，说明“确认执行”需要同一交互或桌面会话，避免把 pending 命令能力误写成跨 `--once` 进程示例。
- 修正后再次验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 227 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近建议执行前确认第一版已提交并推送：`0049c25 feat: 支持确认执行最近建议`，远端 `main` 已从 `d21a4fd` 更新到 `0049c25`。
- 2026-05-22：用户继续要求推进。本轮选择“最近建议状态展示第一版”，让“查看最近上下文”显示最近建议列表和当前待确认建议命令。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-recent-advice-status.json` 和 `.codex/recent-advice-status-plan.md`；设计限定为状态展示，不改变执行语义。
- 本阶段 RED 验证：新增 3 个 Agent 测试先证明“查看最近上下文”没有展示最近建议、待确认建议命令和恢复后的最近建议。
- 更新 `agent.py`，最近上下文状态纳入最近建议和待确认建议命令；生成新建议时清空旧 pending 命令。
- 专项 GREEN 验证：新增 3 个最近建议状态展示测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 90 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 230 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 回填验证结果后再次验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 230 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近建议状态展示第一版已提交并推送：`2faf441 feat: 展示最近建议状态`，远端 `main` 已从 `0049c25` 更新到 `2faf441`。
- 2026-05-22：用户继续要求推进。本轮选择“建议命令参数补全草稿”，让含占位符的最近建议在执行前返回可编辑命令模板。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-advice-command-draft.json` 和 `.codex/advice-command-draft-plan.md`；设计限定为草稿提示，不推断参数、不执行不完整命令、不持久化待确认命令。
- 本阶段 RED 验证：新增 `test_natural_language_prepare_advice_with_missing_parameters_returns_command_draft` 先因响应缺少 `命令草稿：/import <源文件或目录路径> [目标文件名]` 失败。
- 更新 `agent.py`，抽出建议命令文本解析，新增占位符 token 草稿转换；含占位符建议返回草稿并保持 `_pending_advice_command` 为空。
- 专项 GREEN 验证：新增草稿测试和最近建议执行相关 3 个测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 91 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 231 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 回填 README、进度、验证和审查记录后再次验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 231 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 建议命令参数补全草稿已提交：`60225e0 feat: 增加建议命令草稿`。前两次 push 分别因 HTTPS 连接重置和 443 超时失败，第三次重试成功，远端 `main` 已从 `2faf441` 更新到 `60225e0`。
- 2026-05-22：用户要求沉淀 Agent 技术讨论和 Jarvis Lite 后续方案，并继续执行项目任务。本轮选择“草稿参数接收第一版”作为实现任务。
- 写入 `.codex/context-scan-personal-agent-roadmap.json` 和 `.codex/personal-agent-roadmap-plan.md`，记录当前工具降级、文档产物、实现范围和验证方式。
- 新增 `word/2026-05-22-ai-agent-learning-notes.md`，沉淀用户与 ChatGPT、Codex 关于 Agent、RAG、LLM、MCP、Function Calling 和个人设备级 Agent 的讨论。
- 新增 `word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`，把 Jarvis Lite 当前进度融合进个人设备级 Agent 路线，明确电脑、手机、手表三个阶段。
- 更新 README 和 `word/文档索引.md`，补充两份新文档入口。
- 本阶段 RED 验证：新增 `test_completed_advice_command_draft_waits_for_confirmation` 先证明补全后的 `/import` 会直接执行，没有等待确认。
- 更新 `agent.py`，新增当前实例内草稿命令名状态；补全同类完整命令后设置为待确认建议命令，并在确认后复用现有命令执行路径。
- 修正建议命令文本解析，只用中文冒号拆分建议描述，避免 Windows 路径中的 `C:` 被误切断。
- 专项 GREEN 验证：草稿参数接收相关 3 个测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 92 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 232 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本轮已提交并推送：`f2cc1de feat: 接收建议命令草稿参数`，远端 `main` 已从 `60225e0` 更新到 `f2cc1de`。
- 2026-05-22：用户要求继续。本轮选择“已知下载目录上下文增强”，衔接个人设备级 Agent 方案中的电脑工作台增强。
- 写入 `.codex/context-scan-known-downloads-directory.json` 和 `.codex/known-downloads-directory-plan.md`；设计限定为已知目录 fallback，不真实打开外部应用、不移动文件。
- 本阶段 RED 验证：新增 2 个 Agent 测试先证明 `整理下载目录` 找不到 `下载` 常用目录，`打开下载目录` 不会写入打开记录。
- 更新 `agent.py`，扩展 `_known_directory_candidates()`，将 `下载`、`download`、`downloads` 映射为用户主目录下的 `Downloads` 和 `下载` 候选目录。
- 专项 GREEN 验证：桌面和下载目录 fallback 相关 4 个测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 94 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录已知下载目录自然语言能力。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 234 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 已知下载目录自然语言已提交并推送：`99b6af9 feat: 识别下载目录`，远端 `main` 已从 `f2cc1de` 更新到 `99b6af9`。
- 2026-05-22：用户继续要求推进。本轮选择“已知项目目录上下文增强”，衔接电脑 Agent 常用工作对象增强。
- 写入 `.codex/context-scan-known-project-directory.json` 和 `.codex/known-project-directory-plan.md`；设计限定为项目根目录 fallback，不真实打开外部应用、不移动文件。
- 本阶段 RED 验证：新增 2 个 Agent 测试先证明 `整理项目目录` 和 `打开项目目录` 在未登记常用目录时都找不到 `项目`。
- 更新 `agent.py`，在 `_known_directory()` 中将 `项目`、`当前项目`、`project`、`repo`、`repository` 映射为 `self.paths.root`。
- 专项 GREEN 验证：项目目录 fallback 与用户登记目录优先级相关 4 个测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 96 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录已知项目目录自然语言能力。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 236 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 已知项目目录自然语言已提交并推送：`2eb04af feat: 识别项目目录`，远端 `main` 已从 `99b6af9` 更新到 `2eb04af`。
- 2026-05-22：继续推进“知识库问答证据增强”，让 `/ask` 输出更清楚的命中原因和可继续操作。
- 写入 `.codex/context-scan-knowledge-answer-evidence.json` 和 `.codex/knowledge-answer-evidence-plan.md`；设计限定为输出格式增强，不改变检索排序、打分算法、弱相关过滤和结果数量。
- 本阶段 RED 验证：新增 1 个 Knowledge 测试先证明回答缺少“命中原因”和“可继续操作”。
- 更新 `knowledge.py`，在 `answer_from_matches()` 中为每条结果输出关键词匹配分数，并追加“查看第一条结果”“给这个结果打标签 标签”和 `/read 文件名` 的继续操作提示。
- 专项 GREEN 验证：证据增强相关 4 个测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v` 通过，当前 24 个 Knowledge 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 96 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录知识库问答证据增强。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 237 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 知识库问答证据增强已提交：`f760961 feat: 增强知识库问答证据`。首次 push 因 GitHub 443 超时失败，确认本地 `main` 超前远端 1 个提交后重试成功，远端 `main` 已从 `2eb04af` 更新到 `f760961`。
- 2026-05-22：用户要求继续下一个任务。本轮选择“日报运行态上下文联动”，让 `/daily-report` 引用最近资料、目录、搜索结果和建议。
- 写入 `.codex/context-scan-daily-report-runtime-context.json` 和 `.codex/daily-report-runtime-context-plan.md`；设计限定为日报新增“最近上下文”段，不改变运行态上下文格式。
- 本阶段 RED 验证：新增 1 个 Automation 测试先证明日报缺少 `## 最近上下文`。
- 更新 `automation.py`，从 `runtime_context.py` 读取运行态上下文，日报新增最近资料、最近目录、最近搜索结果和最近建议输出；无上下文时写明暂无最近上下文。
- 专项 GREEN 验证：日报运行态上下文相关 2 个测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_automation -v` 通过，当前 6 个 Automation 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 96 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录日报运行态上下文联动。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 238 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 日报运行态上下文联动已提交并推送：`3206d32 feat: 日报引用最近上下文`，远端 `main` 已从 `f760961` 更新到 `3206d32`。
- 2026-05-22：用户要求继续。本轮选择“日报下一步建议生成”，让 `/daily-report` 在最近上下文、经验和工具日志之后给出可执行但不自动执行的下一步建议。
- 写入 `.codex/context-scan-daily-report-next-actions.json` 和 `.codex/daily-report-next-actions-plan.md`；设计限定为确定性建议生成，不调用 LLM，不改变运行态上下文格式。
- 本阶段 RED 验证：新增 1 个 Automation 测试先证明日报缺少 `## 下一步建议`。
- 更新 `automation.py`，日报新增“下一步建议”段，按最近资料、最近目录、最近建议、经验记忆和工具日志生成建议；空状态回退到导入资料、登记常用目录和记录经验。
- 专项 GREEN 验证：日报下一步建议相关 3 个测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_automation -v` 通过，当前 7 个 Automation 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 96 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录日报下一步建议生成。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 239 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 日报下一步建议生成已提交并推送：`7dcfff9 feat: 日报生成下一步建议`，远端 `main` 已从 `3206d32` 更新到 `7dcfff9`。
- 2026-05-22：用户继续要求推进。本轮选择“读取资料写入最近上下文”，补齐最近文件上下文第一步。
- 写入 `.codex/context-scan-read-command-recent-document.json` 和 `.codex/read-command-recent-document-plan.md`；设计限定为 `/read` 成功后复用 `recent_document_path`，不新增运行态字段。
- 本阶段 RED 验证：新增 1 个 Agent 测试先证明 `/read manual.md` 后重启 Agent 仍然没有最近资料。
- 更新 `agent.py`，在 `/read` 成功分支调用 `_remember_recent_document()`；读取失败时保持原错误返回，不写上下文。
- 专项 GREEN 验证：读取资料写入最近上下文新增测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 97 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录读取资料写入最近上下文。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 240 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 读取资料写入最近上下文已提交并推送：`483c893 feat: 读取资料记录最近上下文`，远端 `main` 已从 `7dcfff9` 更新到 `483c893`。
- 2026-05-22：用户继续要求推进。本轮选择“自然语言读取资料”，让“读取 note.md”“查看 note.txt”复用 `/read`。
- 写入 `.codex/context-scan-natural-language-read-document.json` 和 `.codex/natural-language-read-document-plan.md`；设计限定为识别 `.md`/`.txt` 文件名，避免误判状态查询和编号建议。
- 本阶段 RED 验证：调整测试内容后，新增 1 个 Agent 测试先证明“读取 manual.md”落入长期记忆兜底，没有返回文件内容。
- 更新 `intent.py`，新增 `_parse_read_document_intent()`，在标签解析之后、编号结果/建议解析之前将读取资料表达映射为 `/read "文件名"`。
- 专项 GREEN 验证：自然语言读取资料新增测试、编号搜索结果读取和编号建议读取回归共 3 个测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 98 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录自然语言读取资料。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 241 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 自然语言读取资料已提交并推送：`fd94ea1 feat: 支持自然语言读取资料`，远端 `main` 已从 `483c893` 更新到 `fd94ea1`。
- 2026-05-22：用户继续要求推进。本轮选择“自然语言读取最近资料”，让“读取这个资料”“查看这个资料”复用最近资料上下文。
- 写入 `.codex/context-scan-read-recent-document.json` 和 `.codex/read-recent-document-plan.md`；设计限定为新增 `read_recent_document` 意图，复用 `/read`，不新增运行态字段。
- 本阶段 RED 验证：新增 2 个 Agent 测试先证明“读取这个资料”落入普通知识库检索并命中 `note.txt`，无最近资料时没有明确提示。
- 更新 `intent.py`，在具体文件读取之后、编号读取之前识别这个资料/当前资料/刚才资料；更新 `agent.py`，新增 `_read_recent_document()` 复用 `/read`。
- 专项 GREEN 验证：读取最近资料新增 2 个测试通过，编号搜索结果读取和编号建议读取回归通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 100 个 Agent 测试。
- 更新 README、`word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`verification.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录自然语言读取最近资料。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 243 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 自然语言读取最近资料已提交并推送：`58c8c6a feat: 支持读取最近资料`，远端 `main` 已从 `fd94ea1` 更新到 `58c8c6a`。
- 2026-05-22：用户继续要求推进。本轮选择“最近资料列表第一版”，衔接个人设备级 Agent 方案中的最近文件列表能力，但范围限定为 data 资料列表，不扫描系统文件。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-recent-document-list.json` 和 `.codex/recent-document-list-plan.md`；设计复用 `RuntimeContext`，新增最近资料列表并保留单个当前资料指针。
- 本阶段 RED 验证：新增 2 个 Agent 测试和 1 个 Automation 测试先证明最近上下文和日报只展示单个最近资料，不展示最近资料列表。
- 更新 `runtime_context.py`，新增 `recent_document_paths` 运行态字段，并兼容旧上下文中只有 `recent_document_path` 的情况。
- 更新 `agent.py`，`_remember_recent_document()` 维护最多 5 条最近资料列表，最新在前；最近上下文状态展示最近资料列表。
- 更新 `automation.py`，日报最近上下文展示最近资料列表。
- 专项 GREEN 验证：最近资料列表 Agent 展示、跨实例恢复、读取当前资料回归和日报引用共 4 个测试通过。
- 专项验证：`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 102 个 Agent 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_automation -v` 通过，当前 7 个 Automation 测试。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 245 个测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 复跑通过，当前 245 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近资料列表第一版已提交并推送：`599ba30 feat: 记录最近资料列表`，远端 `main` 已从 `58c8c6a` 更新到 `599ba30`。
- 2026-05-22：用户继续要求推进。本轮选择“按编号读取最近资料”，补齐最近资料列表展示后的自然后续动作。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-read-numbered-recent-document.json` 和 `.codex/read-numbered-recent-document-plan.md`；设计限定为读取 data 最近资料列表，不读取系统最近文件。
- 本阶段 RED 验证：新增 3 个 Agent 测试，其中“读取第二份资料”和缺少最近资料列表提示都先落入普通知识库检索；“查看第二条结果”回归通过。
- 更新 `intent.py`，新增 `read_numbered_recent_document` 意图，支持“读取第二份资料”“查看第2个文档”等表达。
- 更新 `agent.py`，按编号从最近资料列表读取 data 文件，读取成功后复用 `/read` 逻辑更新当前资料。
- 专项 GREEN 验证：编号读取最近资料、缺上下文提示、搜索结果编号回归和当前资料读取回归共 4 个测试通过。
- 专项验证：`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 105 个 Agent 测试。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 248 个测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 复跑通过，当前 248 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 按编号读取最近资料已提交并推送：`4d81940 feat: 支持按编号读取最近资料`，远端 `main` 已从 `599ba30` 更新到 `4d81940`。
- 2026-05-22：用户继续要求推进。本轮选择“按编号给最近资料打标签”，补齐最近资料列表的标签操作。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-tag-numbered-recent-document.json` 和 `.codex/tag-numbered-recent-document-plan.md`；设计限定为给 data 最近资料列表打标签，不改变搜索结果编号语义。
- 本阶段 RED 验证：新增 2 个 Agent 测试先证明“给第二份资料打标签”会把“第二份资料”当普通文件名传给 `/tag`；搜索结果编号标签回归通过。
- 更新 `intent.py`，标签解析中识别“第 N 份资料/文档/文件”，新增 `tag_numbered_recent_document` 意图。
- 更新 `agent.py`，按编号从最近资料列表选择 data 文件并复用 `/tag`。
- 专项 GREEN 验证：按编号给最近资料打标签、缺列表提示、搜索结果标签回归和编号读取回归共 4 个测试通过。
- 更新 `README.md`、`verification.md` 和 `word/` 进度/方案文档，补充“给第二份资料打标签 项目”示例、验证记录和当前 250 个测试进度；同步更新 `.codex/testing.md` 与 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 250 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 按编号给最近资料打标签已提交并推送：`c7c81e9 feat: 支持按编号给最近资料打标签`，远端 `main` 已从 `4d81940` 更新到 `c7c81e9`。
- 2026-05-22：用户继续要求推进。本轮选择“系统最近文件列表第一版”，衔接个人设备级 Agent 方案中的最近文件列表能力。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-recent-files-first-version.json` 和 `.codex/recent-files-first-version-plan.md`；设计限定为扫描常用目录和项目/桌面/下载目录顶层普通文件，只展示最近修改文件，不执行打开、移动或删除。
- 本阶段 RED 验证：新增 1 个 Automation 测试和 2 个 Agent 测试；失败点为 `list_recent_files` 尚不存在、“查看最近文件”落入长期记忆兜底、`/recent-files` 是未知命令。
- 更新 `automation.py`，新增 `RecentFile` 与 `list_recent_files()`，按修改时间倒序列出目录顶层普通文件；更新 `intent.py` 与 `agent.py`，新增“查看最近文件”和 `/recent-files`。
- 更新 `/automation-status` 当前能力摘要，补充 `/recent-files`。
- 专项 GREEN 验证：最近文件列表 3 个新增测试通过；`tests.test_agent` 109 个测试通过，`tests.test_automation` 8 个测试通过。
- 更新 `README.md`、`verification.md` 和 `word/` 进度/方案文档；同步更新 `.codex/testing.md` 与 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 253 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 系统最近文件列表第一版已提交并推送：`3fa6f16 feat: 支持查看系统最近文件`，远端 `main` 已从 `c7c81e9` 更新到 `3fa6f16`。
- 2026-05-22：用户继续要求推进。本轮选择“按编号查看最近文件详情”，衔接最近文件列表的持久化和编号操作。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-read-numbered-recent-file.json` 和 `.codex/read-numbered-recent-file-plan.md`；设计限定为展示最近文件元数据，不读取内容、不打开文件、不移动或删除文件。
- 本阶段 RED 验证：新增 3 个 Agent 测试先证明“查看第一份最近文件”没有意图、最近文件列表不能跨实例恢复、缺列表时没有明确提示。
- 更新 `runtime_context.py`，新增最近文件运行态字段；更新 `agent.py`，`/recent-files` 会保存最近文件列表，并支持按编号查看最近文件元数据；更新 `intent.py`，新增“第 N 份最近文件”意图。
- 专项 GREEN 验证：按编号查看最近文件详情 3 个新增 Agent 测试通过；`tests.test_agent` 112 个测试通过，`tests.test_automation` 8 个测试通过。
- 更新 `README.md`、`verification.md` 和 `word/` 进度/方案文档；同步更新 `.codex/testing.md` 与 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 256 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 按编号查看最近文件详情已提交并推送：`050c34e feat: 支持按编号查看最近文件`，远端 `main` 已从 `3fa6f16` 更新到 `050c34e`。
- 2026-05-22：用户继续要求推进。本轮选择“最近文件纳入最近上下文和日报”，把已持久化的最近文件列表接入上下文状态与日报。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-recent-files-context-and-daily.json` 和 `.codex/recent-files-context-and-daily-plan.md`；设计限定为展示最近文件来源/路径，不读取内容、不打开文件、不移动或删除文件。
- 本阶段 RED 验证：新增 2 个 Agent 测试和扩展 2 个 Automation 测试，先证明最近文件列表未进入“查看最近上下文”、跨实例最近上下文和日报。
- 更新 `agent.py`，让“查看最近上下文”展示最近文件列表；更新 `automation.py`，让日报最近上下文和下一步建议读取 `recent_files`。
- 专项 GREEN 验证：最近文件上下文联动 4 个新增/扩展测试通过；`tests.test_agent` 114 个测试通过，`tests.test_automation` 8 个测试通过。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 258 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 收尾验证：`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近文件纳入最近上下文和日报已提交并推送：`38667b2 feat: 最近文件接入上下文日报`，远端 `main` 已从 `050c34e` 更新到 `38667b2`。
- 2026-05-22：用户要求继续下一个阶段。本轮选择“最近上下文输出下一步建议”，作为跨入口任务建议第一步。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-recent-context-next-actions.json` 和 `.codex/recent-context-next-actions-plan.md`；设计限定为复用日报建议生成逻辑，只展示建议文本，不自动执行。
- 本阶段 RED 验证：新增 Agent 测试先证明最近上下文已有资料、目录、最近文件和最近建议时，仍没有“下一步建议”段。
- 更新 `automation.py`，抽取 `suggest_next_actions_from_context()`；更新 `agent.py`，让“查看最近上下文”复用同一建议生成逻辑。
- 专项 GREEN 验证：最近上下文下一步建议新增 Agent 测试通过，日报下一步建议回归通过；`tests.test_agent` 115 个测试通过，`tests.test_automation` 8 个测试通过。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 259 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近上下文输出下一步建议已本地提交：`660fb84 feat: 最近上下文输出下一步建议`。推送到 `origin/main` 连续 3 次失败，前两次为 `OpenSSL SSL_read: Connection was reset, errno 10054`，第三次切换 `schannel` 后为连接 GitHub 443 超时；当前 `main` 比 `origin/main` ahead 1。
- 2026-05-23：用户要求继续下一个任务。先重试推送昨日提交，`660fb84 feat: 最近上下文输出下一步建议` 已成功推送，远端 `main` 从 `38667b2` 更新到 `660fb84`。
- 本轮选择“桌面快捷入口补齐最近上下文和最近文件”，延续跨入口任务建议路线。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-desktop-recent-quick-commands.json` 和 `.codex/desktop-recent-quick-commands-plan.md`；设计限定为新增无参数快捷入口，继续排除需要参数的整理预览。
- 本阶段 RED 验证：扩展桌面桥接和面板测试，先证明“最近上下文”和“最近文件”没有进入快捷命令集合，面板无法点击“最近上下文”。
- 更新 `desktop/bridge.py`，新增“最近上下文”(`查看最近上下文`) 和“最近文件”(`/recent-files`) 快捷命令，并加入无参数直接快捷入口。
- 专项 GREEN 验证：`tests.test_desktop_bridge` 4 个测试通过，`tests.test_desktop_widgets` 19 个测试通过，`tests.test_desktop_tray` 8 个测试通过。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 260 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 桌面快捷入口补齐最近上下文和最近文件已提交并推送：`ab94424 feat: 桌面快捷入口支持最近上下文`。前两次 OpenSSL 推送因 `SSL_read: Connection was reset` 失败，切换 `schannel` 后推送成功，远端 `main` 从 `660fb84` 更新到 `ab94424`。
- 2026-05-23：用户继续要求推进。本轮选择“按编号导入最近文件到知识库”，补齐最近文件列表后的知识库导入动作。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-import-numbered-recent-file.json` 和 `.codex/import-numbered-recent-file-plan.md`；设计限定为从已保存的最近文件列表按编号选路径，复用 `/import` 和 `import_knowledge_path()`，不新增导入实现。
- 本阶段 RED 验证：新增 3 个 Agent 测试先证明“第一份最近文件”会被通用导入意图误当成普通路径，缺列表和编号越界也没有最近文件语义提示。
- 更新 `intent.py`，新增 `import_numbered_recent_file` 意图，并放在通用 `_parse_import_intent()` 之前。
- 更新 `agent.py`，新增 `_import_numbered_recent_file()`，复用最近文件列表校验后调用 `/import "路径"`。
- 专项 GREEN 验证：按编号导入最近文件 3 个新增 Agent 测试通过；`tests.test_agent` 118 个测试通过；`tests.test_knowledge` 24 个测试通过。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 263 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 按编号导入最近文件已提交并推送：`8da1d65 feat: 支持按编号导入最近文件`，远端 `main` 已从 `ab94424` 更新到 `8da1d65`。
- 2026-05-25：用户继续要求推进。本轮选择“最近文件导入进入下一步建议”，把已完成的按编号导入动作接入最近上下文和日报建议。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-recent-file-import-suggestions.json` 和 `.codex/recent-file-import-suggestions-plan.md`；设计限定为更新共用建议文本，不自动执行导入。
- 本阶段 RED 验证：更新 1 个 Agent 测试和 1 个 Automation 测试，先证明最近文件下一步建议仍缺少“导入第一份最近文件到知识库”。
- 更新 `automation.py` 的 `suggest_next_actions_from_context()`，最近文件建议改为“查看第一份最近文件；导入第一份最近文件到知识库；/recent-files”。
- 专项 GREEN 验证：最近上下文和日报最近文件建议 2 个测试通过。
- 专项验证：`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 118 个 Agent 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_automation -v` 通过，当前 8 个 Automation 测试。
- 全量验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 263 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 最近文件导入进入下一步建议已提交并推送：`df6e8f9 feat: 最近文件建议支持导入入口`，远端 `main` 已从 `8da1d65` 更新到 `df6e8f9`。
- 2026-05-25：用户继续要求推进。本轮选择“知识库摘要增强”，为个人知识库补充可直接查看的确定性摘要。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 沿用上一轮写入的 `.codex/context-scan-knowledge-summary.json` 和 `.codex/knowledge-summary-plan.md`；设计限定为本地确定性摘要，不调用 LLM，不改变 `/kb` 和 `/ask`。
- 本阶段 RED 验证：新增 2 个 Knowledge 测试和 2 个 Agent 测试，先证明 `summarize_knowledge_base` 缺失、`/kb-summary` 未识别、“总结知识库”未映射。
- 更新 `knowledge.py`，新增 `summarize_knowledge_base()`，复用 `build_knowledge_index()`、`_searchable_lines()` 和标签元数据输出资料来源、行数、标签与首行预览。
- 更新 `agent.py`，新增 `/kb-summary`、`/knowledge-summary` 命令入口和帮助文案。
- 更新 `intent.py`，新增“总结知识库”“知识库摘要”“总结资料库”“资料库摘要”到 `/kb-summary` 的映射。
- 专项 GREEN 验证：知识库摘要 4 个目标测试通过；`tests.test_knowledge` 26 个测试通过；`tests.test_agent` 120 个测试通过。
- 更新 `README.md`、`verification.md` 和 `word/` 进度/方案文档；同步更新 `.codex/testing.md` 与 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 267 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 知识库摘要增强已提交并推送：`75f6899 feat: 支持知识库摘要`，远端 `main` 已从 `df6e8f9` 更新到 `75f6899`。
- 2026-05-25：用户继续要求推进。本轮选择“知识库摘要联动最近资料上下文”，让摘要结果可以直接衔接“读取第 N 份资料”和“给第 N 份资料打标签”。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-knowledge-summary-context.json` 和 `.codex/knowledge-summary-context-plan.md`；设计限定为 Agent 层写入最近资料上下文，不改变 `/kb`、`/ask` 和摘要底层函数。
- 本阶段 RED 验证：新增 3 个 Agent 测试先证明 `/kb-summary` 缺少可继续操作提示、摘要后不能读取第二份资料、新 Agent 实例不能恢复摘要资料列表。
- 更新 `agent.py`，新增 `_knowledge_summary()`，`/kb-summary` 会写入摘要资料路径到 `_recent_document_paths` 并保存运行态上下文，响应末尾追加“可继续操作：读取第一份资料；给第一份资料打标签 标签；/ask 关键词”。
- 专项 GREEN 验证：知识库摘要上下文联动 3 个目标测试通过；`tests.test_agent` 123 个测试通过；`tests.test_knowledge` 26 个测试通过。
- 更新 `README.md`、`verification.md` 和 `word/` 进度/方案文档；同步更新 `.codex/testing.md` 与 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 270 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 知识库摘要联动最近资料已提交并推送：`4368ce8 feat: 摘要结果联动最近资料`，远端 `main` 已从 `75f6899` 更新到 `4368ce8`。
- 2026-05-25：用户继续要求推进。本轮选择“知识库摘要长预览截断”，防止资料首行过长导致 `/kb-summary` 输出难扫读。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `.codex/` 记录替代。
- 写入 `.codex/context-scan-knowledge-summary-preview.json` 和 `.codex/knowledge-summary-preview-plan.md`；设计限定为摘要预览格式化，不改变索引、搜索、读取和导入。
- 本阶段 RED 验证：新增 1 个 Knowledge 测试先证明长预览完整输出，没有 `...` 省略标记。
- 更新 `knowledge.py`，新增 `SUMMARY_PREVIEW_MAX_CHARS = 80` 和 `_summary_preview()`；`summarize_knowledge_base()` 对首条可检索文本预览执行确定性截断。
- 专项 GREEN 验证：长预览截断目标测试通过；`tests.test_knowledge` 27 个测试通过。
- 更新 `README.md`、`verification.md` 和 `word/` 进度/方案文档；同步更新 `.codex/testing.md` 与 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 271 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 补记：知识库摘要长预览截断已提交并推送：`a94e5a9 feat: 截断知识库摘要预览`，远端 `main` 已从 `4368ce8` 更新到 `a94e5a9`。
- 2026-05-25：用户要求对照 `word/` 文档、项目代码进度和 `.codex/` 文档，核查 2026-05-22 之后是否缺少文档和进度执行记录。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager`、`code-index` 和 `exa`；本地 `codex sequential-thinking` 因 `stdin is not a terminal` 无法非交互运行。本轮使用 `rg`、`git log`、`Get-Content`、`update_plan` 和 `apply_patch` 降级执行，并写入 `.codex/context-scan-doc-progress-sync.json` 与 `.codex/doc-progress-sync-plan.md`。
- 对照结果：`word/文档索引.md` 的阶段进度入口只列到 2026-05-21，`word/` 没有独立的 2026-05-23 和 2026-05-25 日进度总账；但 `git log`、`.codex/operations-log.md`、`.codex/testing.md`、`.codex/review-report.md` 和 `verification.md` 已记录 2026-05-23 与 2026-05-25 的实际进度。
- 文档补齐：新增 `word/2026-05-23-jarvis-lite-progress.md`，汇总桌面最近上下文/最近文件快捷入口与按编号导入最近文件；新增 `word/2026-05-25-jarvis-lite-progress.md`，汇总最近文件导入建议、知识库摘要、摘要上下文联动、长预览截断和本轮文档审计；更新 `word/文档索引.md` 入口。
- 中断恢复：读取 `日志.txt` 后确认上次在写回验证/审查记录前因 `503 Service Unavailable` 中断；本轮补写 `.codex/testing.md`、`verification.md` 和 `.codex/review-report.md` 的文档同步收尾记录。
- 代码/文档映射复核：`rg` 确认 `summarize_knowledge_base()`、`SUMMARY_PREVIEW_MAX_CHARS`、`import_numbered_recent_file`、`suggest_next_actions_from_context()`、`/recent-files`、`/kb-summary`、桌面最近上下文快捷入口和 `desktopPetWindow` smoke 均有源码或测试证据。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 271 个测试；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅提示 `word/文档索引.md` 后续会从 LF 转 CRLF。
- 本地提交：`f59a86d docs: 补齐进度文档同步记录`，包含 `verification.md`、`word/文档索引.md`、`word/2026-05-23-jarvis-lite-progress.md` 和 `word/2026-05-25-jarvis-lite-progress.md`；未执行远端 push。
- 2026-05-25：用户要求 push 并继续后续任务。已执行 `git push`，远端 `main` 从 `a94e5a9` 更新到 `f59a86d`。
- 下一任务选择：根据 `word/2026-05-25-jarvis-lite-progress.md` 和个人设备 Agent 方案，选择“知识库摘要按标签分组展示”，保持与 `/kb-summary` 当前能力连续。
- 写入 `.codex/context-scan-kb-summary-grouping.json` 和 `.codex/kb-summary-grouping-plan.md`；设计为仅增强摘要格式，不改变最近资料编号顺序、`/kb`、`/ask`、导入和标签写入。
- RED 验证：新增 `tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_groups_documents_by_tags` 先失败，摘要缺少 `- 标签分组：`。
- GREEN 实现：更新 `knowledge.py`，`summarize_knowledge_base()` 在资料概览前输出标签分组；新增 `_summary_tag_group_lines()`，有标签资料按标签聚合，无标签资料归入“未标签”。
- 专项验证：标签分组目标测试通过；摘要来源预览和长预览截断回归通过；`.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v` 通过，当前 28 个 Knowledge 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 123 个 Agent 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 272 个测试；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交：`34330a0 feat: 知识库摘要按标签分组`。
- 已推送：远端 `main` 从 `f59a86d` 更新到 `34330a0`。
- 2026-05-25：用户要求继续下一个任务。本轮继续知识库摘要可读性路线，选择“知识库摘要按标签后续建议”。
- 写入 `.codex/context-scan-kb-summary-tag-suggestions.json` 和 `.codex/kb-summary-tag-suggestions-plan.md`；设计为在已有 `/kb-summary` 通用后续操作后，按知识库标签追加最多 3 个 `/ask 标签` 示例。
- RED 验证：新增 `tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_tagged_ask_followups` 先失败，摘要已有标签分组但没有 `按标签提问：/ask 助手；/ask 项目`。
- GREEN 实现：更新 `agent.py`，`_knowledge_summary()` 复用 `build_knowledge_index()` 结果追加按标签提问建议，并新增 `_knowledge_summary_tag_suggestions()`。
- 专项验证：标签化 `/ask` 建议目标测试通过；编号后续建议和最近资料上下文回归通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 124 个 Agent 测试；`.\.venv\Scripts\python.exe -m unittest tests.test_knowledge -v` 通过，当前 28 个 Knowledge 测试。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 273 个测试；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交：`fe557a3 feat: 知识库摘要提示标签提问`。
- 已推送：远端 `main` 从 `34330a0` 更新到 `fe557a3`。
- 2026-05-25：用户要求继续。本轮选择“桌面知识库摘要快捷入口”，把已稳定的 `/kb-summary` 暴露给桌面面板和托盘。
- 写入 `.codex/context-scan-desktop-kb-summary-quick-command.json` 和 `.codex/desktop-kb-summary-quick-command-plan.md`；设计为只更新 `desktop/bridge.py` 的统一快捷命令源。
- RED 验证：Desktop bridge 和 widgets 目标测试先失败，`quick_commands()`、`direct_quick_commands()` 和面板按钮均缺少“知识库摘要”。
- GREEN 实现：`DIRECT_QUICK_COMMAND_PROMPTS` 增加 `/kb-summary`，`quick_commands()` 在“知识库”后增加 `QuickCommand("知识库摘要", "/kb-summary")`。
- 专项验证：目标测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v` 通过，当前 4 个 bridge 测试；`tests.test_desktop_widgets` 19 个通过；`tests.test_desktop_tray` 8 个通过。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 273 个测试；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交：`1c1496c feat: 桌面快捷入口支持知识库摘要`。
- 已推送：远端 `main` 从 `fe557a3` 更新到 `1c1496c`。
- 2026-05-25：用户继续要求推进。本轮选择“按标签读取知识库资料组”，承接 `/kb-summary` 标签分组和标签 `/ask` 建议。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮使用 `rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest`、桌面 smoke 和 `git diff --check` 降级执行，并继续写入 `.codex/` 留痕。
- 写入 `.codex/context-scan-read-tagged-documents.json` 和 `.codex/read-tagged-documents-plan.md`；设计为自然语言层新增 `read_tagged_documents` 意图，Agent 复用 `build_knowledge_index()` 按标签筛选资料。
- RED 验证：新增 2 个 Agent 测试先失败，“读取项目标签资料”和“查看缺失标签资料”都落入普通资料问答，没有标签组读取或缺失提示。
- GREEN 实现：更新 `intent.py`，新增“读取/查看/看看 + 标签 + 标签资料/标签文档”解析；更新 `agent.py`，新增 `_read_tagged_documents()`，按标签列出资料并写入最近资料列表。
- 专项验证：目标测试通过；`.\.venv\Scripts\python.exe -m unittest tests.test_agent -v` 通过，当前 126 个 Agent 测试；`tests.test_knowledge` 28 个通过。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 275 个测试；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 更新 `README.md`、`verification.md`、`word/2026-05-25-jarvis-lite-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/文档索引.md`、`.codex/testing.md` 和 `.codex/review-report.md`，记录按标签读取资料组能力。
- 本地提交并推送：`5809837 feat: 支持按标签读取资料组`，远端 `main` 已从 `1c1496c` 更新到 `5809837`。
- 2026-05-25：用户继续要求推进。本轮选择“知识库摘要按标签读取建议”，让 `/kb-summary` 直接提示刚完成的“读取项目标签资料”入口。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-kb-summary-tag-read-suggestions.json` 和 `.codex/kb-summary-tag-read-suggestions-plan.md`；设计为只增强 `_knowledge_summary()` 末尾建议，不改变摘要正文和最近资料列表写入。
- RED 验证：新增 `tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_tagged_read_followups` 先失败，`/kb-summary` 只有按标签提问建议，没有按标签读取建议。
- GREEN 实现：更新 `agent.py`，新增 `_knowledge_summary_tag_read_suggestions()` 和 `_knowledge_summary_tags()`，复用同一批排序标签生成 `读取标签标签资料` 建议。
- 专项验证：目标测试和标签提问建议回归测试通过；`tests.test_agent` 127 个通过；`tests.test_knowledge` 28 个通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-25-jarvis-lite-progress.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 276 个测试；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`8243551 feat: 摘要提示按标签读取资料`，远端 `main` 已从 `5809837` 更新到 `8243551`。
- 2026-05-26：用户要求继续。本轮选择“标签组批量打标签前预览”，承接按标签读取资料组后的批量操作需求。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；`tool_search` 未找到相关工具。本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-tagged-documents-tag-preview.json` 和 `.codex/tagged-documents-tag-preview-plan.md`；设计为只做批量影响范围预览，不直接修改标签元数据。
- RED 验证：新增 2 个 Agent 测试先失败，“给项目标签资料都打标签 归档”和缺失标签组句式都落入普通 `/tag` 文件名路径。
- GREEN 实现：更新 `intent.py`，新增 `preview_tagged_documents_tagging` 意图且放在普通 tag 意图前；更新 `agent.py`，新增 `_preview_tagged_documents_tagging()`、标签合并和逐份确认建议。
- 专项验证：目标测试通过；普通自然语言打标签、按编号给最近资料打标签、按标签读取资料组和摘要按标签读取建议回归通过；`tests.test_knowledge` 28 个通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`word/文档索引.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 278 个测试；`.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`8c1e7a7 feat: 预览标签组批量打标签`，远端 `main` 已从 `8243551` 更新到 `8c1e7a7`。
- 2026-05-26：用户继续要求推进。本轮选择“标签组批量打标签确认闭环”，让前一轮预览支持“确认执行”和“取消执行”。
- 写入 `.codex/context-scan-confirm-tagged-documents-tagging.json` 和 `.codex/confirm-tagged-documents-tagging-plan.md`；设计为复用现有确认入口，待确认状态只保存在当前 Agent 会话。
- RED 验证：新增 2 个 Agent 测试先失败，预览后“确认执行/取消执行”仍只检查经验建议命令。
- GREEN 实现：更新 `agent.py`，保存待确认标签组状态；“确认执行”逐份追加标签，“取消执行”清空状态；准备经验建议命令时清空标签组待确认状态以避免入口冲突。
- 专项验证：确认/取消目标测试通过；经验建议确认、经验建议草稿确认、普通打标签和标签组预览回归通过；`tests.test_knowledge` 28 个通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 280 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`2a483ea feat: 确认执行标签组批量打标签`，远端 `main` 已从 `8c1e7a7` 更新到 `2a483ea`。
- 2026-05-26：用户继续要求推进。本轮选择“标签组批量打标签待确认状态接入最近上下文”，让预览后的待确认状态可被“查看最近上下文”看见。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；`tool_search` 未找到相关工具。本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-pending-tagged-documents-recent-context.json` 和 `.codex/pending-tagged-documents-recent-context-plan.md`；设计为只展示当前会话内待确认批量标签任务，不新增持久化状态。
- RED 验证：新增 1 个 Agent 测试先失败，预览后“查看最近上下文”没有显示待确认批量打标签状态。
- GREEN 实现：更新 `_recent_context_status()`，新增待确认批量打标签状态判断和展示行；空上下文判断也纳入该状态。
- 专项验证：目标测试通过；最近上下文待确认建议、最近建议、空状态、标签组确认和取消回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 281 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`4065745 feat: 最近上下文显示待确认批量标签`，远端 `main` 已从 `2a483ea` 更新到 `4065745`。
- 2026-05-26：用户继续要求推进。本轮选择“标签组批量打标签确认后的历史与恢复提示”，降低误确认后的恢复成本。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-tagged-documents-undo-hints.json` 和 `.codex/tagged-documents-undo-hints-plan.md`；设计为确认输出给出恢复命令，不新增持久化撤销栈。
- 工具调用异常记录：一次无关占位 shell 命令 `tool_search_placeholder` 失败，不影响代码和测试上下文收集。
- RED 验证：新增 1 个 Agent 测试先失败，确认批量打标签后没有操作记录和恢复提示。
- GREEN 实现：更新 `_confirm_pending_tagged_documents_tagging()`，确认前记录原标签，成功更新后生成逐份恢复命令，并输出本次更新数量。
- 专项验证：目标测试通过；标签组确认、取消、最近上下文、普通打标签和编号资料打标签回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 282 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`358cb66 feat: 批量标签确认提示恢复命令`，远端 `main` 已从 `4065745` 更新到 `358cb66`。
- 2026-05-26：用户继续要求推进。本轮选择“标签组批量操作摘要接入最近上下文”，把最近一次确认执行的批量标签操作摘要放进“查看最近上下文”。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-tagged-documents-operation-summary.json` 和 `.codex/tagged-documents-operation-summary-plan.md`；设计为当前会话内最近一次批量标签操作摘要，不新增持久化结构。
- RED 验证：新增 1 个 Agent 测试先失败，确认后“查看最近上下文”没有最近批量打标签摘要和恢复提示。
- GREEN 实现：`JarvisAgent` 新增会话内最近批量标签操作字段，确认成功后写入标签组、追加标签、更新数量和恢复命令；最近上下文新增摘要展示。
- 专项验证：目标测试通过；最近上下文待确认批量标签、空状态、标签组确认、恢复提示和取消回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 283 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`651835a feat: 最近上下文记录批量标签摘要`，远端 `main` 已从 `358cb66` 更新到 `651835a`。
- 2026-05-26：用户继续要求推进。本轮选择“持久化最近批量标签操作摘要”，让新 Agent 实例也能恢复最近一次批量标签操作摘要。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-persistent-tagged-documents-operation.json` 和 `.codex/persistent-tagged-documents-operation-plan.md`；设计为扩展 `RuntimeContext`，兼容旧运行态 JSON。
- RED 验证：新增 1 个 Agent 测试先失败，新 `JarvisAgent` 实例无法恢复最近批量标签操作摘要。
- GREEN 实现：`runtime_context.py` 新增 `RuntimeTaggedDocumentsOperationContext`，`RuntimeContext` 增加 `recent_tagged_documents_operation` 字段；Agent 初始化和保存路径接入该字段。
- 专项验证：目标测试通过；最近资料列表、最近文件列表、最近建议、当前批量摘要、确认恢复提示和取消回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 284 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`d2f7c0d feat: 持久化批量标签摘要`，远端 `main` 已从 `651835a` 更新到 `d2f7c0d`。
- 2026-05-26：用户继续要求推进。本轮选择“批量标签操作历史命令”，把最近一次批量标签摘要扩展为最近 5 条历史记录，并提供独立查看入口。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-batch-tag-history.json` 和 `.codex/batch-tag-history-plan.md`；设计为兼容旧运行态单值字段，同时新增历史列表字段。
- RED 验证：新增 1 个 Agent 测试先失败，`/tag-history` 返回未知命令。
- GREEN 实现：`RuntimeContext` 新增 `recent_tagged_documents_operations` 历史列表；`JarvisAgent` 确认批量标签后保存最近 5 条历史；新增 `/tag-history` 和“查看批量标签历史”入口。
- 专项验证：目标测试通过；最近批量摘要、标签组确认、恢复提示和取消回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`word/文档索引.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 285 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`7868c3b feat: 记录批量标签历史`，远端 `main` 已从 `d2f7c0d` 更新到 `7868c3b`。
- 2026-05-26：用户继续要求推进。本轮选择“桌面快捷入口接入批量标签历史”，把 `/tag-history` 作为无参数快捷按钮暴露到面板和托盘。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-desktop-tag-history-entry.json` 和 `.codex/desktop-tag-history-entry-plan.md`；设计为复用 `quick_commands()` 和 `DIRECT_QUICK_COMMAND_PROMPTS`，不新增桌面专用命令路径。
- RED 验证：桌面桥接目标测试先失败，快捷命令缺少 `/tag-history`；桌面面板目标测试先失败，按钮缺少“标签历史”。
- GREEN 实现：`desktop/bridge.py` 新增“标签历史”快捷命令，并把 `/tag-history` 加入直接快捷命令白名单。
- 专项验证：目标测试通过；桌面桥接、面板和托盘专项 32 个测试通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 286 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`07d1e22 feat: 桌面快捷入口显示标签历史`，远端 `main` 已从 `7868c3b` 更新到 `07d1e22`。
- 2026-05-26：用户继续要求推进。本轮选择“按编号读取批量标签历史影响资料”，把历史条目恢复为最近资料列表。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-tag-history-document-list.json` 和 `.codex/tag-history-document-list-plan.md`；设计为在历史摘要结构中新增受影响资料路径列表，兼容旧历史记录。
- RED 验证：新增 1 个 Agent 测试先失败，“读取第一条标签历史资料”被普通资料问答兜底，无法恢复历史影响资料列表。
- GREEN 实现：批量标签历史结构新增 `document_paths`；确认执行时保存影响资料路径；新增“读取第 N 条标签历史资料”意图并恢复最近资料列表。
- 专项验证：目标测试通过；批量标签历史、最近批量摘要、最近资料列表和恢复提示回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 287 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 2026-05-26：用户继续要求推进。本轮选择“批量标签历史资料读取恢复提示”，让“读取第一条标签历史资料”直接显示该历史条目的逐份恢复命令。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-tag-history-restore-hints.json` 和 `.codex/tag-history-restore-hints-plan.md`；设计为复用历史条目已有 `restore_commands`，不新增运行态字段。
- RED 验证：扩展现有 Agent 测试先失败，“读取第一条标签历史资料”已列出影响资料，但没有恢复提示。
- GREEN 实现：`_read_tagged_documents_history_documents()` 在历史条目存在 `restore_commands` 时追加恢复提示。
- 专项验证：目标测试通过；批量标签历史、最近批量摘要、最近资料列表和确认恢复提示回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 287 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`853737a feat: 标签历史资料显示恢复提示`，远端 `main` 已从 `f5e361f` 更新到 `853737a`。
- 2026-05-26：用户继续要求推进。本轮选择“批量标签历史资料缺失提示”，处理历史记录中的资料后来被删除或移动时的输出。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-tag-history-missing-documents.json` 和 `.codex/tag-history-missing-documents-plan.md`；设计为读取历史影响资料时逐项检查文件存在性，不修改历史结构。
- RED 验证：新增 Agent 测试先失败，删除历史中的第二份资料后，“读取第一条标签历史资料”触发 `FileNotFoundError`。
- GREEN 实现：`_read_tagged_documents_history_documents()` 逐项检查资料文件存在性，缺失时输出 `（资料缺失）` 并跳过摘要读取。
- 专项验证：目标测试通过；批量标签历史资料读取、历史列表、最近批量摘要、最近上下文和确认恢复提示回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 288 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`9d917ea feat: 标签历史资料标注缺失`，远端 `main` 已从 `853737a` 更新到 `9d917ea`。
- 2026-05-26：用户继续要求推进。本轮选择“编号最近资料缺失提示”，让“读取第二份资料”遇到已删除资料时保留编号上下文。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-numbered-recent-document-missing.json` 和 `.codex/numbered-recent-document-missing-plan.md`；设计为在 `_read_numbered_recent_document()` 调用 `/read` 前检查文件存在性。
- RED 验证：新增 Agent 测试先失败，“读取第二份资料”对已删除资料只返回底层 `文件不存在`，缺少编号缺失提示。
- GREEN 实现：`_read_numbered_recent_document()` 在调用 `/read` 前检查资料文件，缺失时返回 `第 N 份资料：data/<路径>（资料缺失）`。
- 专项验证：目标测试通过；编号读取、历史缺失、历史资料读取和最近资料持久化回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-26-jarvis-lite-progress.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 289 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`a6f522c feat: 编号资料标注缺失`，远端 `main` 已从 `9d917ea` 更新到 `a6f522c`。
- 2026-05-27：用户继续要求推进。本轮选择“编号最近资料打标签缺失提示”，让“给第二份资料打标签”遇到已删除资料时保留编号上下文。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用 `rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-tag-numbered-recent-document-missing.json` 和 `.codex/tag-numbered-recent-document-missing-plan.md`；设计为在 `_tag_numbered_recent_document()` 调用 `/tag` 前检查文件存在性。
- RED 验证：新增 Agent 测试先失败，“给第二份资料打标签 项目”对已删除资料只返回底层 `标签更新失败`，缺少编号缺失提示。
- GREEN 实现：`_tag_numbered_recent_document()` 在调用 `/tag` 前检查资料文件，缺失时返回 `第 N 份资料：data/<路径>（资料缺失）`。
- 专项验证：目标测试通过；编号打标签、编号读取缺失、历史缺失和普通标签更新回归通过。
- 更新 `README.md`、`verification.md`、`word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`、`word/2026-05-27-jarvis-lite-progress.md`、`word/文档索引.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 290 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出码为 0，仅出现 CRLF 提示。
- 本地提交并推送：`1a56288 feat: 编号标签标注缺失`，远端 `main` 已从 `a6f522c` 更新到 `1a56288`。
- 2026-05-27：用户确认开始后，本轮继续执行“LLM 外脑接入第一版”，并明确 provider 需要可切换，不绑定单一大模型。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest` 和官方 OpenAI 文档检索降级执行。
- 写入 `.codex/llm-provider-routing-implementation-plan.md`；设计为 `JarvisAgent` 本地优先，LLM 通过 `LLMRouter` / `LLMProvider` / `LLMIntent` 接入，厂商细节留在 provider adapter。
- RED 验证：Agent LLM 集成测试先失败，`JarvisAgent.__init__()` 不接受 `llm_router`；OpenAI provider 测试先因缺少 `OpenAIResponsesProvider` 失败；`/llm-status` 先返回未知命令。
- GREEN 实现：新增 `src/jarvis_lite/llm.py`，包含 provider-neutral 设置、fake provider、OpenAI Responses API adapter 和 Router；`JarvisAgent` 在知识库问答之后、长期记忆兜底之前调用 LLM；新增 `/llm-status`。
- 依赖更新：`pyproject.toml` 加入 `openai>=2,<3`，并通过 `.\.venv\Scripts\python.exe -m pip install -e .` 安装验证，当前解析到 `openai-2.38.0`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`、`word/progress/2026-05-27.md`、`verification/2026-05/2026-05-27.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`git diff --check` 退出 0，仅出现 CRLF 提示；Markdown 本地链接检查通过；`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 305 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 本地提交并推送：`bd663e6 feat: 接入 LLM 外脑 Router`，远端 `main` 已从 `b51b79f` 更新到 `bd663e6`。
- 2026-05-27：用户准备自行查看或购买 OpenAI API key，并要求继续先做不需要真实 API key 的内容。
- 本轮选择“OpenAI-compatible provider 和 token usage 日志”，避免依赖真实 API key，全部通过 fake client 与本地测试验证。
- RED 验证：新增 LLM/Agent 测试先失败，`LLMUsage` 尚未定义，`openai-compatible` 尚未接入 Router，Agent 尚未记录 usage。
- GREEN 实现：新增 `LLMUsage`；`OpenAIResponsesProvider` 支持 `openai-compatible` 并要求 `JARVIS_LITE_LLM_BASE_URL`；解析 Responses usage 为 provider-neutral 用量结构；Agent 把 usage 写入 `logs/jarvis.log`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`、`word/progress/2026-05-27.md`、`verification/2026-05/2026-05-27.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`git diff --check` 退出 0，仅出现 CRLF 提示；Markdown 本地链接检查通过；`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 309 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 本地提交并推送：`83e7c1c feat: 支持兼容 LLM 端点用量日志`，远端 `main` 已从 `bd663e6` 更新到 `83e7c1c`。
- 2026-05-27：用户的 OpenAI API key 尚未准备好，要求继续推进不依赖真实 key 的内容。
- 本轮选择“LLM 配置诊断”，让 `/llm-status` 在配置不完整时列出缺失项，降低后续接入 API key 的试错成本。
- RED 验证：新增 LLM/Agent 测试先失败，`LLMRouter.describe()` 只展示 provider/model，不展示缺少 model、API key、base URL 或未知 provider。
- GREEN 实现：新增 `VALID_LLM_PROVIDERS` 和 `LLMSettings.configuration_issues()`；`LLMRouter.describe()` 在启用状态下追加“配置问题”或“配置：可调用”；Agent `/llm-status` 复用 Router 输出。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`、`word/progress/2026-05-27.md`、`verification/2026-05/2026-05-27.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：`git diff --check` 退出 0，仅出现 LF/CRLF 提示；Markdown 本地链接检查通过；`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 313 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 本地提交并推送：`0fb2956 feat: 增强 LLM 配置诊断`，远端 `main` 已从 `83e7c1c` 更新到 `0fb2956`。
- 2026-05-27：用户的 OpenAI API key 仍未就绪，要求继续推进；本轮选择“LLM 本地用量汇总”，继续做不依赖真实 key 的基础设施。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-llm-usage-summary.json` 和 `.codex/llm-usage-summary-plan.md`；设计为 `llm.py` 负责 provider-neutral 日志汇总，`JarvisAgent` 只暴露 `/llm-usage`。
- RED 验证：新增 LLM/Agent 测试先失败，`summarize_llm_usage` 尚未导出，`/llm-usage` 返回未知命令，`/help` 未列出该命令。
- GREEN 实现：新增 `summarize_llm_usage()` 解析 `logs/jarvis.log` 中的 `LLM 外脑用量` 行，按 provider/model 汇总调用次数和 token；`JarvisAgent` 新增 `/llm-usage` 并更新 `/help`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`、`word/progress/2026-05-27.md`、`verification/2026-05/2026-05-27.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 专项验证：`tests.test_llm` 18 个通过，`tests.test_agent` 149 个通过。
- 收尾验证：`git diff --check` 退出 0，仅出现 LF/CRLF 提示；Markdown 本地链接检查通过；`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 317 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 本地提交并推送：`a75667a feat: 汇总 LLM 本地用量`，首次 push 超时后重试成功，远端 `main` 已从 `0fb2956` 更新到 `a75667a`。
- 2026-05-27：用户的 OpenAI API key 仍未就绪，要求继续推进；本轮选择“LLM 配置模板命令”，继续做不依赖真实 key 的接入准备。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-llm-config-example.json` 和 `.codex/llm-config-example-plan.md`；设计为 `llm.py` 负责配置模板文本，`JarvisAgent` 只暴露 `/llm-config-example [provider]`。
- RED 验证：新增 LLM/Agent 测试先失败，`describe_llm_config_examples` 尚未导出，`/llm-config-example` 返回未知命令，`/help` 未列出该命令。
- GREEN 实现：新增 `describe_llm_config_examples()`，输出 `off`、`fake`、`openai` 和 `openai-compatible` 的 PowerShell 环境变量模板；`qwen` / `gemini` 先映射到兼容端点模板；模板只显示占位符，不读取或保存真实 API key；`JarvisAgent` 新增命令并更新 `/help`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`、`word/progress/2026-05-27.md`、`verification/2026-05/2026-05-27.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 专项验证：`tests.test_llm` 22 个通过，`tests.test_agent` 152 个通过。
- 收尾验证：`git diff --check` 退出 0，仅出现 LF/CRLF 提示；Markdown 本地链接检查通过；`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 324 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 本地提交并推送：`25e7e58 feat: 增加 LLM 配置模板`，远端 `main` 已从 `a75667a` 更新到 `25e7e58`。
- 2026-05-27：用户提供真实兼容端点调用方式并要求继续完成中断任务；本轮只处理可配置接入，不把真实 API key 或具体 endpoint 写入代码、文档或提交。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮从用户保存的 `日志.txt` 恢复上下文，继续使用技能文件、`rg`、本地文件读取、`apply_patch`、`unittest` 和本地 smoke 验证降级执行。
- 中断点确认：已存在两个 RED 测试和初版实现，目标为支持 `openai-compatible` 直接粘贴完整 `/v1/responses` URL。
- RED 验证：兼容端点完整 URL 测试先失败，SDK 仍收到完整 `/v1/responses` URL，`/llm-status` 未展示 SDK Base URL；配置模板测试先失败，未提示“完整 `/v1/responses` URL”。
- GREEN 实现：新增 `LLMSettings.sdk_base_url()` 与 `normalize_responses_base_url()`；`OpenAIResponsesProvider` 调 SDK 时使用归一化 base URL；`LLMRouter.describe()` 在发生归一化时展示 SDK Base URL；配置模板提示可填 `/v1` 或完整 `/v1/responses` URL。
- 文档同步：更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`、`word/progress/2026-05-27.md`、`verification.md`、`verification/2026-05/README.md`、`verification/2026-05/2026-05-27.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 专项验证：完整 `/v1/responses` URL 归一化、`/llm-status` 展示和配置模板专项 4 个测试通过；`tests.test_llm` 24 个通过；`tests.test_agent` 152 个通过。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 326 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告；Markdown 本地链接检查通过。
- 2026-05-27：用户要求继续补全 LLM 调用能力；本轮选择 `/llm-smoke [prompt]`，用于真实 provider 配置 smoke 和用量观察，不写入真实 key 或具体 endpoint。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`apply_patch`、`unittest` 和本地 smoke 验证降级执行。
- 写入 `.codex/context-scan-llm-smoke-command.json` 和 `.codex/llm-smoke-command-plan.md`；设计为强制调用当前 `LLMRouter`，但只展示结构化 intent，不执行 LLM 返回的 command。
- RED 验证：新增 Agent 测试先失败，`/help` 未列出 `/llm-smoke`，`/llm-smoke` 返回未知命令，usage 日志测试没有生成日志文件。
- GREEN 实现：`JarvisAgent` 新增 `/llm-smoke [prompt]`；未启用时返回配置提示；启用时调用 Router；command intent 只展示建议不执行；usage 沿用 `_record_llm_usage()`。
- 文档同步：更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`、`word/progress/2026-05-27.md`、`verification.md`、`verification/2026-05/README.md`、`verification/2026-05/2026-05-27.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 专项验证：`/llm-smoke` 目标 5 个测试通过；`tests.test_agent` 156 个通过；`tests.test_llm` 24 个通过。
- 收尾验证：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 通过，当前 330 个测试；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出 0，仅提示 LF/CRLF 工作区换行警告；Markdown 本地链接检查通过。
- 2026-05-27：用户要求对今天所有 LLM 外脑整合工作做收口总结，确认代码、文档和后续项目实现是否与前面方案一致。
- 核对范围：`README.md`、`word/PROJECT-PLAN.md`、`word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`、`word/progress/2026-05-27.md`、`verification.md`、`verification/2026-05/2026-05-27.md`、`src/jarvis_lite/llm.py`、`src/jarvis_lite/agent.py`、`tests/test_llm.py`、`tests/test_agent.py`。
- 核对结论：当前实现与方案一致，保持 PC Agent 本地优先、LLM 作为外脑、provider 细节隔离、配置走环境变量、模型返回结构化意图、本地 Agent 控制执行、`/llm-smoke` 不执行命令建议。
- 文档整理：按 `DOCUMENTATION.md` 规则更新 README 能力摘要、`word/progress/2026-05-27.md` 验证摘要、`verification.md` 最近摘要、`verification/2026-05/README.md` 月索引和 `verification/2026-05/2026-05-27.md` 一致性核对明细。
- 验证：`git diff --check` 退出 0，仅提示 LF/CRLF；Markdown 本地链接检查通过；敏感信息扫描未命中真实 key 或具体网关；`tests.test_llm tests.test_agent` 180 个通过；全量 `unittest discover` 330 个通过；桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 2026-05-27：用户要求 push 后继续下一个任务；确认 `main` 已与 `origin/main` 对齐，上次 3 个 LLM 提交已推送，本轮继续“LLM provider 命令边界与 smoke 模板”。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest` 和本地 smoke 验证降级执行。
- RED 验证：新增 2 个 LLM 测试先失败，`OpenAIResponsesProvider._instructions()` 未列出可返回命令白名单，`describe_llm_config_examples()` 未包含 `/llm-smoke 请用一句话确认连接可用`。
- GREEN 实现：OpenAI Responses provider instructions 增加 Jarvis Lite 命令白名单和“不返回列表之外命令”约束；配置模板的“配置后可运行”加入 `/llm-smoke 请用一句话确认连接可用`。
- 文档同步：更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`、`word/progress/2026-05-27.md`、`verification.md`、`verification/2026-05/README.md` 和 `verification/2026-05/2026-05-27.md`。
- 专项验证：目标 2 个 LLM 测试通过；`tests.test_llm` 25 个通过；`tests.test_agent` 156 个通过；全量 `unittest discover` 331 个通过；桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；敏感信息扫描未命中。
- 2026-05-28：用户要求继续推进；本轮选择“LLM fallback 近期上下文增强”，继续沿 v3 路线打磨 LLM 外脑第一版，不依赖真实 API key。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest` 和本地 smoke 验证降级执行。
- 写入 `.codex/context-scan-llm-recent-context.json` 和 `.codex/llm-recent-context-plan.md`；设计为复用已有 `suggest_next_actions_from_context()`，把近期上下文的可执行下一步建议传给 LLM provider。
- RED 验证：新增 Agent 测试先失败，fake provider 收到的 context 只有记忆摘要和最近资料，没有 `下一步建议：继续处理最近资料...`。
- GREEN 实现：`JarvisAgent._llm_context_lines()` 在存在近期上下文或经验记忆时追加最多 3 条下一步建议。
- 专项验证：目标测试通过；`tests.test_agent` 157 个通过，`tests.test_llm` 25 个通过。
- 文档同步：新增 `word/progress/2026-05-28.md` 和 `verification/2026-05/2026-05-28.md`，并更新 README、当前方案、v3 方案、每日进度索引、文档索引、验证入口、月索引和周索引。
- 收尾验证：全量 `unittest discover` 332 个通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出 0，仅提示 LF/CRLF；Markdown 本地链接检查通过；敏感信息扫描未命中。
- 2026-05-28：用户要求继续推进；本轮选择“LLM fallback 最近搜索结果上下文”，承接刚完成的下一步建议 context。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest` 和本地 smoke 验证降级执行。
- 写入 `.codex/context-scan-llm-search-results-context.json` 和 `.codex/llm-search-results-context-plan.md`；设计为把 `_recent_search_result_paths` 中最多 3 条 `data/<path>` 加入 LLM context。
- RED 验证：新增 Agent 测试先失败，fake provider 收到的 context 有记忆摘要、最近资料和下一步建议，但没有 `最近搜索结果：2 条`。
- GREEN 实现：`JarvisAgent._llm_context_lines()` 追加最近搜索结果数量和最多 3 条编号路径。
- 专项验证：目标测试通过；`tests.test_agent` 158 个通过，`tests.test_llm` 25 个通过。
- 文档同步：更新 README、当前方案、v3 方案、`word/progress/2026-05-28.md`、`verification.md`、`verification/2026-05/README.md` 和 `verification/2026-05/2026-05-28.md`。
- 收尾验证：全量 `unittest discover` 333 个通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出 0，仅提示 LF/CRLF；Markdown 本地链接检查通过；敏感信息扫描未命中。
- 2026-05-28：用户要求一口气完成剩余小任务并打包新版本，同时明确已安装旧版时的升级策略。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest` 和本地打包验证降级执行。
- 写入 `.codex/context-scan-llm-install-package.json` 和 `.codex/llm-install-package-plan.md`；确认安装器当前是 IExpress，安装脚本会关闭旧进程并 copy /Y 覆盖程序文件，卸载脚本保留用户数据。
- RED 验证：新增目标测试先失败，覆盖 `/llm-context-preview` 缺失、未知 LLM 命令被交给 Agent 执行、provider 401/429 错误不可读、`/llm-status` 缺少 API key/网络调用诊断和安装脚本缺少覆盖安装提示。
- GREEN 实现：新增共享 `LLM_ALLOWED_COMMAND_SPECS`；Provider instructions 与 Agent 执行校验共用白名单；新增 `/llm-context-preview`；增强 `LLMRouter.describe()`；OpenAI provider 错误分类为 401/403/429/timeout/5xx；版本提升到 `0.1.1`；安装脚本提示覆盖安装和用户数据保留。
- 文档同步：更新 README、当前方案、v3 方案、今日进度、验证入口、月索引、日验证明细、`.codex/testing.md` 和 `.codex/review-report.md`。
- 验证：目标 9 个测试通过；`tests.test_llm` 28 个通过；`tests.test_agent` 160 个通过；安装器/桌面打包/项目元数据专项 18 个通过；全量 `unittest discover` 339 个通过；源码桌面 smoke 和打包后 exe smoke 通过。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，并复制 `JarvisLiteSetup-0.1.1.exe` 便于用户重装测试。
- 收尾静态检查：`git diff --check` 退出 0（仅 LF/CRLF 提示）；Markdown 本地链接检查通过；敏感信息扫描未命中真实 key 或具体网关片段。
- 2026-05-28：用户安装 `0.1.1` 后反馈“本质上还是不能识别自然语言”；读取 `日志.txt`，确认 `/help` 已包含 `/llm-context-preview`，新版本已生效，根因是本地自然语言意图层缺少问候、助手身份和桌面快捷方式删除意图。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest`、源码 smoke 和打包验证降级执行。
- 写入 `.codex/context-scan-natural-language-feedback.json` 和 `.codex/natural-language-feedback-plan.md`；方案为沿用 `NaturalLanguageIntent` + `JarvisAgent` dispatcher，不引入新解析框架。
- RED 验证：新增 8 个目标测试先失败，覆盖 `早上好`、`你好`、`你叫什么名字`、桌面两个指定 `.lnk` 快捷方式删除、缺失快捷方式提示、桌面 bridge 问候、安装脚本版本输出和 IExpress 完成消息版本提示。
- GREEN 实现：`intent.py` 新增 `greeting`、`assistant_identity`、`delete_desktop_shortcuts`；`agent.py` 新增问候/助手身份回复和桌面 `.lnk` 删除；安装器输出和完成弹窗加入版本；项目版本提升到 `0.1.2`。
- 验证：目标 8 个测试通过；相关回归 188 个通过；全量 `unittest discover` 345 个通过；源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 打包：刷新 editable 安装为 `jarvis-lite 0.1.2`；`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，并复制 `JarvisLiteSetup-0.1.2.exe` 便于用户安装测试。
- 2026-05-28：用户认可“内脑 + 外脑”方向，要求先按文档整理约定把方案落到项目文档。
- 文档方案：新增 `word/plans/2026-05-28-v4-inner-brain-llm-dual-brain-plan.md`，明确不继续堆正则、不从零训练通用小型 LLM，而是建立本地 InnerBrain 做 NLU、槽位抽取、置信度和执行策略判断。
- 文档同步：更新 `word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md` 和 `word/progress/2026-05-28.md`，将当前路线调整为 PC Agent -> InnerBrain 内脑 -> LLM 外脑 -> 多端入口。
- 2026-05-28：用户要求提交并开始下一任务；已推送 `dfd692d docs: 落地内脑外脑双脑方案` 到 `origin/main`。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-inner-brain-v1.json` 和 `.codex/inner-brain-v1-plan.md`；计划为新增 `InnerBrain` 本地轻量 NLU，先包装 legacy 自然语言规则，再用 seed/runtime JSONL 样本做相似度泛化，低置信度继续走 data/LLM fallback。
- RED 验证：`tests.test_inner_brain` 先因模块不存在失败；Agent 集成测试先失败，样本表达走到 LLM 或 data 问答。
- GREEN 实现：新增 `src/jarvis_lite/inner_brain.py`，定义结构化结果、策略、seed/runtime JSONL 样本加载、字符特征相似度和 legacy wrapper；`JarvisAgent` 接入 InnerBrain，高置信度执行，中置信度澄清，低置信度继续 fallback。
- 专项验证：`tests.test_inner_brain` 6 个通过；Agent 目标 3 个通过；`tests.test_inner_brain tests.test_agent` 共 174 个通过。
- 收尾验证：全量 `unittest discover` 354 个通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出 0，仅提示 LF/CRLF；Markdown 本地链接检查通过。
- 验证注意：一次命令行 smoke 误用了真实桌面快捷方式删除输入，输出显示删除 `比特浏览器.lnk`；随后从开始菜单同名快捷方式复制回 `C:\Users\hp\Desktop\比特浏览器.lnk`，已恢复该副作用。
- 2026-05-28：用户要求继续下一个任务；本轮选择 InnerBrain 可观察调试入口，新增 `/inner-brain-status` 和 `/inner-brain-preview 文本`，用于查看本地内脑样本、阈值和单句识别结果，preview 必须不执行本地动作。
- 写入 `.codex/context-scan-inner-brain-preview.json` 和 `.codex/inner-brain-preview-plan.md`；继续按 TDD 执行。
- RED 验证：`describe_inner_brain_result` 不存在导致 InnerBrain 测试导入失败；Agent 未识别 `/inner-brain-status` 和 `/inner-brain-preview`。
- GREEN 实现：`inner_brain.py` 新增 `describe_inner_brain_result()` 和 `InnerBrain.describe_status()`；`JarvisAgent` 新增 `/inner-brain-status` 与 `/inner-brain-preview 文本`，并更新 `/help`。
- 专项验证：目标 12 个测试通过；`tests.test_inner_brain tests.test_agent` 共 179 个通过。
- 收尾验证：全量 `unittest discover` 359 个通过；`/inner-brain-status` 和 `/inner-brain-preview 麻烦看一下知识库摘要` smoke 通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`git diff --check` 退出 0，仅提示 LF/CRLF；Markdown 本地链接检查通过。
- 2026-05-28：用户要求继续推进；本轮选择 InnerBrain runtime 样本采纳闭环，目标是把 preview/adopt 认可的识别结果写入 `data/inner-brain/training/runtime.jsonl`。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest`、临时目录 smoke、桌面 smoke 和静态检查降级执行。
- 写入 `.codex/context-scan-inner-brain-adopt-sample.json` 和 `.codex/inner-brain-adopt-sample-plan.md`；接口契约为 `/inner-brain-adopt 文本`，非 `unknown` 结果保存 runtime 样本，重复样本不重复写入，保存不执行命令。
- RED 验证：`tests.test_inner_brain` 因 `save_runtime_training_sample` 不存在导入失败；Agent 未识别 `/inner-brain-adopt`，help 缺少命令，runtime 样本文件未创建。
- GREEN 实现：`inner_brain.py` 新增 `InnerBrainTrainingSaveResult` 与 `save_runtime_training_sample()`；写入 JSONL 时合并 natural intent 槽位并去重；`JarvisAgent` 新增 `/inner-brain-adopt`、输出文案、日志和内脑刷新。
- 专项验证：`tests.test_inner_brain tests.test_agent` 共 186 个通过。
- 文档同步：更新 README、`word/PROJECT-PLAN.md`、`word/progress/2026-05-28.md`、`verification.md`、`verification/2026-05/README.md`、`verification/2026-05/2026-05-28.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：全量 `unittest discover` 366 个通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；临时目录 `/inner-brain-adopt 帮我看看资料库状态` smoke 输出 runtime_sample 1 条；`git diff --check` 退出 0，仅提示 LF/CRLF；Markdown 本地链接检查通过；敏感信息扫描未命中。
- 2026-05-28 14:12:20 +08:00：用户要求继续下一个任务；本轮承接 InnerBrain 样本闭环，选择“人工标注/纠错命令”，目标是让 `unknown` 或误识别输入也能沉淀为 runtime 样本。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`/本地文件读取、`update_plan`、`apply_patch`、`unittest`、临时目录 smoke、桌面 smoke 和静态检查降级执行。
- 写入 `.codex/context-scan-inner-brain-label-sample.json` 和 `.codex/inner-brain-label-sample-plan.md`；接口契约为 `/inner-brain-label 文本 => intent [slot=value ...]`，保存人工指定 intent/slots/missing，保存后刷新当前 Agent，保存动作不执行识别出的命令。
- RED 验证：`tests.test_inner_brain tests.test_agent -v` 先失败，`save_labeled_runtime_training_sample` 不存在、help 缺少 `/inner-brain-label`、Agent 无法处理人工标注命令。
- GREEN 实现：`inner_brain.py` 新增 `save_labeled_runtime_training_sample()` 并复用 runtime JSONL 写入/去重；`JarvisAgent` 新增 `/inner-brain-label` 命令、slot 解析、保存反馈、日志和 InnerBrain 刷新。
- 专项验证：`tests.test_inner_brain tests.test_agent -v` 共 192 个通过，覆盖人工写入、列表 slot、格式错误、slot 错误、保存刷新和不执行桌面快捷方式删除。
- 文档同步：更新 README、`word/PROJECT-PLAN.md`、`word/progress/2026-05-28.md`、`verification.md`、`verification/2026-05/README.md`、`verification/2026-05/2026-05-28.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：全量 `unittest discover` 372 个通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；临时目录 `/inner-brain-label 可以看看资料库吗 => knowledge.status command=/kb` smoke 确认 followup 生效且未污染仓库 `data/`；`git diff --check` 退出 0，仅提示 LF/CRLF；Markdown 本地链接检查通过；敏感信息扫描未命中。
- 最终复核：Markdown 本地链接脚本首次因 `git ls-files` 对中文路径转义导致读取路径异常；改用 `git -c core.quotePath=false ls-files -z -- *.md` 后重新验证通过。
- Git 收尾：提交 `4201c1b feat: 增加 InnerBrain 人工标注命令`，并推送到 `origin/main`；`git rev-list --left-right --count '@{u}...HEAD'` 输出 `0 0`。
- 2026-05-28 14:43:57 +08:00：用户要求继续；本轮承接人工标注入口，选择“InnerBrain 口语化教学入口”，目标是让用户不必理解 intent/slot，也能把自然语言短句绑定到已知命令。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`/本地文件读取、`update_plan`、`apply_patch`、`unittest`、临时目录 smoke、桌面 smoke 和静态检查降级执行。
- 写入 `.codex/context-scan-inner-brain-teach-command.json` 和 `.codex/inner-brain-teach-command-plan.md`；设计为 `/inner-brain-teach 文本 => /命令`，并支持“以后我说“文本”就是 /命令”“把“文本”记成 /命令”。
- RED 验证：目标 5 个测试先失败，`/help` 缺少 `/inner-brain-teach`，slash 教学返回未知命令，口语教学句式未保存 runtime 样本。
- GREEN 实现：`JarvisAgent` 新增可教学命令到 intent 的映射、`/inner-brain-teach` 和 `/teach` 命令、口语教学句式解析、保存反馈、日志和 InnerBrain 刷新。
- 专项验证：目标 5 个测试通过；`tests.test_inner_brain tests.test_agent -v` 共 196 个通过，覆盖 slash 教学、口语教学、保存刷新、不执行 `/daily-report` 和未知目标命令拒绝。
- 文档同步：更新 README、`word/PROJECT-PLAN.md`、`word/progress/2026-05-28.md`、`verification.md`、`verification/2026-05/README.md`、`verification/2026-05/2026-05-28.md`、`.codex/testing.md` 和 `.codex/review-report.md`。
- 收尾验证：全量 `unittest discover` 376 个通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；临时目录 `/inner-brain-teach 可以看看资料库吗 => /kb` smoke 确认 followup 生效且未污染仓库 `data/`；`git diff --check` 退出 0，仅提示 LF/CRLF；Markdown 本地链接检查通过；敏感信息扫描未命中。
- Git 收尾：提交 `423572c feat: 增加 InnerBrain 口语教学入口`，并推送到 `origin/main`；`git rev-list --left-right --count '@{u}...HEAD'` 输出 `0 0`。
- 2026-05-28 14:57:11 +08:00：用户要求继续下一个阶段；本轮选择发布收口阶段，将 InnerBrain v1、preview/status、runtime 样本采纳、人工标注和口语教学入口打包为 `0.1.3` 可安装测试版。
- 写入 `.codex/context-scan-inner-brain-install-package-013.json` 和 `.codex/inner-brain-install-package-013-plan.md`；确认当前版本仍为 `0.1.2`，后续能力尚未进入安装包。
- RED 验证：新增 `test_project_version_matches_release_package_version` 后先失败，`pyproject.toml` 版本为 `0.1.2`，期望 `0.1.3`。
- GREEN 实现：更新 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README、今日进度和验证文档到 `0.1.3`；专项测试 19 个通过；editable 安装刷新为 `jarvis-lite 0.1.3`。
- 收尾验证：全量 `unittest discover` 377 个通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包验证：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`install.cmd` 包含 `DisplayVersion /d "0.1.3"`、覆盖安装提示和用户数据保留提示；SED 包含 `Jarvis Lite 0.1.3 installation finished`。
- 版本化产物：复制生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.3.exe`，大小与主安装包一致。
- 静态验证：`git diff --check` 退出 0，仅提示 LF/CRLF；Markdown 本地链接检查通过；敏感信息扫描未命中。
- Git 收尾：提交 `d2c4c4d chore: 发布 InnerBrain 0.1.3 测试版`，并推送到 `origin/main`；`git rev-list --left-right --count '@{u}...HEAD'` 输出 `0 0`。
- 2026-05-28：用户指出当前聊天与处理方式仍离方案较远，强调外脑 LLM 应通过 URL + API key 直接配置开启，不应继续靠正则识别自然语言。
- 当前工具列表没有 `sequential-thinking`、`shrimp-task-manager` 和 `code-index`；本轮继续使用技能文件、`rg`/本地文件读取、`update_plan`、`apply_patch` 和 `unittest` 降级执行。
- 写入 `.codex/context-scan-llm-local-config.json` 和 `.codex/llm-local-config-plan.md`；决策为提交配置模板和加载逻辑，真实 `config/llm.local.json` 由 `.gitignore` 忽略，避免 API key 进入 Git 历史。
- RED 验证：目标测试先失败，`ProjectPaths.config_dir`、`llm_local_config_path()` 和本地配置读取入口不存在；“开启外脑”落入长期记忆兜底；运行中写入 `llm.local.json` 后 Router 未重新加载。
- GREEN 实现：新增运行态 `config` 目录、`LLMSettings.from_sources()`、本地配置读取、环境变量覆盖、`config/llm.example.json`、`/llm-enable` 和 InnerBrain seed 样本“开启外脑/连接外脑”。
- 专项验证：目标 11 个测试通过；`tests.test_config tests.test_llm tests.test_inner_brain tests.test_agent -v` 共 233 个通过。
- 收尾验证：全量 `unittest discover` 384 个通过；源码桌面 smoke 通过；源码“开启外脑”smoke 输出配置路径；`git diff --check` 退出 0（仅 LF/CRLF 提示）；Markdown 本地链接检查通过；敏感信息扫描未命中；`git ls-files config/llm.local.json` 无输出。
## 2026-05-28 联网搜索 Router 任务启动

- 工具降级：当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已改用本地结构化扫描、`rg`、`update_plan` 和 `.codex` 文档留痕。
- 上下文扫描：读取 `src/jarvis_lite/llm.py`、`src/jarvis_lite/agent.py`、`src/jarvis_lite/inner_brain.py`、`src/jarvis_lite/runtime_context.py`、`tests/test_llm.py`、`tests/test_agent.py`、README 和 v4 方案。
- 设计决策：联网搜索作为 SearchRouter/Provider 工具接入 JarvisAgent；LLM 外脑不直接浏览，后续只基于 Agent 提供的搜索结果做总结。
- 配置约定：沿用 LLM 的 `config/*.example.json` + ignored `*.local.json` 模式；真实 API key 不写入 Git。
- 方案落地：新增 `word/plans/2026-05-28-v5-agent-web-search-llm-complement-plan.md`，并同步 `word/PROJECT-PLAN.md`、`word/plans/README.md` 和 `word/文档索引.md`。
- TDD RED：`tests.test_search` 和 Agent 搜索入口测试先因 `jarvis_lite.search` 缺失失败。
- 实现：新增 `src/jarvis_lite/search.py`、`config/search.example.json`，接入 `JarvisAgent`、InnerBrain seed 样本和 LLM command 白名单；`pyproject.toml` 增加 `tavily-python>=0.7,<1`。
- 验证：`tests.test_search` 10 个通过；`tests.test_search tests.test_inner_brain tests.test_agent` 215 个通过；全量 `unittest discover` 399 个通过；源码桌面 smoke 通过；`/search-status` 和 fake provider `/search Python 版本` smoke 通过；`git diff --check` 退出 0（仅 LF/CRLF 提示）；Markdown 本地链接检查通过；敏感信息扫描通过；`config/search.local.json` 未被 Git 跟踪。

## 2026-05-28 InnerBrain 样本分类器优先迁移启动

- 用户更正“安装”为“按照”，要求继续按照预想方案和步骤推进，暂不测试过渡版，等流程初步实现后再测试。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已改用本地结构化扫描、`rg`、`update_plan`、`.codex` 计划文件和本地测试降级执行。
- 上下文扫描确认：`InnerBrain.understand()` 当前仍先调用 `parse_natural_language_intent()` 并返回 `source=legacy_rule`，与用户要求的“内脑不应靠正则主识别自然语言”不一致。
- 写入 `.codex/context-scan-inner-brain-classifier-first.json` 和 `.codex/inner-brain-classifier-first-plan.md`；本阶段目标是样本分类器优先，legacy parser 只作为迁移期兼容 fallback。
- RED 验证：`tests.test_inner_brain tests.test_agent -v` 按预期失败，失败集中在高频自然语言仍返回 `legacy_rule`、状态文案仍显示 `legacy_rule：启用`、复杂槽位规则未标记为 `legacy_fallback`。
- GREEN 实现：`InnerBrain.understand()` 改为 seed/runtime 样本高置信优先；中置信样本若旧 parser 能识别更具体动作则走 `legacy_fallback`；扩展高频 seed 样本并更新状态文案。
- 回归验证：`tests.test_inner_brain tests.test_agent -v` 207 个通过；全量 `unittest discover -s tests -v` 401 个通过。
- 补充样本 RED/GREEN：为 `有什么功能`、`目录列表`、`下载最新版`、`取消运行` 增加高频样本断言，先因 `legacy_fallback` 失败；扩展 seed 样本后目标测试通过。
- 收尾 smoke：源码桌面 smoke 通过；`/inner-brain-status` 输出样本分类器优先、`legacy_fallback` 和 `seed_sample：51 条`；`/inner-brain-preview 早上好` 输出 `source=seed_sample`。
- 静态验证：`git diff --check` 退出 0（仅 LF/CRLF 提示）；Markdown 本地链接检查通过；敏感信息扫描通过；`git ls-files config/llm.local.json config/search.local.json` 未输出 tracked 文件。
- 文档同步：新增 `word/plans/2026-05-28-v6-inner-brain-classifier-first-plan.md`，并同步 README、当前方案、方案索引、文档索引、今日进度、验证记录和 `.codex` 审查/测试记录。

## 2026-05-28 InnerBrain 编号槽位迁移

- 用户要求继续下一阶段；本轮承接 v6 方案，选择把第一批编号/对象槽位动作迁移出 `legacy_fallback`。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已改用技能文件、`rg`、本地文件读取、`update_plan`、`.codex` 记录和本地测试降级执行。
- 上下文扫描确认：`src/jarvis_lite/intent.py` 中读取当前资料、读取编号资料、读取/导入编号最近文件、读取编号搜索结果和建议相关函数仍是旧 parser；`JarvisAgent` 已经具备对应执行处理函数。
- 写入 `.codex/context-scan-inner-brain-slot-extractors.json` 和 `.codex/inner-brain-slot-extractors-plan.md`；设计为样本签名负责语义识别，正则只抽取 `result_index` 槽位。
- RED 验证：`tests.test_inner_brain.InnerBrainTests.test_numbered_object_intents_use_sample_classifier_slots` 先失败，8 个样例均返回 `legacy.*`。
- GREEN 实现：扩展 seed 样本，新增编号动作 intent-specific signature，将编号归一为 `{index}`；新增 `result_index` 槽位抽取和 `NaturalLanguageIntent` 映射。
- 专项验证：目标测试通过；`tests.test_inner_brain` 16 项通过；`tests.test_agent` 192 项通过。
- 全量与 smoke：全量 `unittest discover` 402 项通过；源码桌面 smoke 通过；`/inner-brain-status` 显示 `seed_sample：66 条`；`/inner-brain-preview 读取第二份资料` 显示 `document.read_numbered_recent`、`seed_sample`、`编号：2`。
- 文档同步：更新 v6 方案、今日进度、根验证入口、日验证明细、`.codex/testing.md` 和 `.codex/review-report.md`。

## 2026-05-28 InnerBrain 标签槽位迁移

- 用户要求继续；本轮承接编号槽位迁移，选择标签类高频动作作为下一批 `legacy_fallback` 迁移目标。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已改用技能文件、`rg`、本地文件读取、`update_plan`、`.codex` 记录和本地测试降级执行。
- 上下文扫描确认：`src/jarvis_lite/intent.py` 中 `_parse_tag_intent`、`_parse_tagged_documents_tag_preview_intent`、`_parse_read_tagged_documents_intent` 和 `_parse_read_tagged_documents_history_intent` 仍由旧 parser 处理；`JarvisAgent` 已具备对应执行函数。
- 写入 `.codex/context-scan-inner-brain-tag-slots.json` 和 `.codex/inner-brain-tag-slots-plan.md`；设计为样本签名负责语义识别，解析函数只抽取 `tags`、`alias`、`result_index`。
- RED 验证：`tests.test_inner_brain.InnerBrainTests.test_tag_intents_use_sample_classifier_slots` 先失败，7 个样例均返回 `legacy.*`。
- GREEN 实现：扩展标签 seed 样本；新增 `{tags}`、`{tag}`、`{index}` 签名归一化；新增标签槽位抽取和 `NaturalLanguageIntent` 映射。
- 专项验证：目标测试通过；`tests.test_inner_brain` 17 项通过；`tests.test_agent` 192 项通过。
- 全量与 smoke：全量 `unittest discover` 403 项通过；源码桌面 smoke 通过；`/inner-brain-status` 显示 `seed_sample：75 条`；`/inner-brain-preview 给第二份资料打标签 项目 Python` 显示 `document.tag_numbered_recent`、`seed_sample`、`标签：项目、Python`、`编号：2`。
- 文档同步：更新 v6 方案、README、当前项目方案、今日进度、验证入口、日验证明细、月/周索引、`.codex/testing.md` 和 `.codex/review-report.md`。

## 2026-05-28 InnerBrain 文件路径、目录和经验槽位迁移

- 2026-05-28 18:24:15 +08:00：用户要求“自己往方案结束一直执行”；本轮承接 v6 方案继续迁移剩余高频 legacy 槽位动作。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已改用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest` 和本地 smoke 降级执行。
- 上下文扫描确认：`src/jarvis_lite/intent.py` 中 `_parse_read_document_intent`、`_parse_import_intent`、`_parse_open_drive`、`_parse_directory_alias_intent`、`_parse_experience_intent`、`_parse_experience_search_intent` 和 `_parse_experience_advice_intent` 仍由旧 parser 处理；`JarvisAgent` 已具备对应执行链路。
- RED 验证：新增文件路径、目录和经验 3 个 InnerBrain 测试后先失败；样例均返回 `legacy.*` 或 `command`/`legacy_fallback`。
- GREEN 实现：扩展 seed 样本；新增 `document.read_path`、`knowledge.import`、`directory.open_drive`、`directory.open_alias`、`directory.organize_alias`、`directory.open_recent`、`directory.organize_recent`、`experience.record`、`experience.search` 和 `experience.advice`；新增签名归一化和 `path/source/alias/experience/query` 槽位抽取。
- 专项验证：三个目标测试通过；`tests.test_inner_brain` 20 项通过；`tests.test_inner_brain tests.test_agent` 212 项通过。
- 全量验证：全量 `unittest discover` 406 项通过。
- 收尾验证：源码桌面 smoke 通过；`/inner-brain-status` 显示 `seed_sample：90 条`；三个 preview smoke 分别覆盖导入路径、目录别名和经验建议；`git diff --check` 通过且仅有 LF/CRLF 提示；敏感信息差异扫描通过；本地配置文件未被 Git 跟踪。
- 验证注意：Markdown 本地链接脚本首次因根目录 Markdown 文件 parent path 为空报错；修正脚本后复跑通过，输出 `Markdown local links OK`。
- 文档同步：更新 README、`word/PROJECT-PLAN.md`、v6 方案、今日进度、验证入口、日验证明细、月/周索引、`.codex/testing.md` 和 `.codex/review-report.md`。

## 2026-05-28 SearchRouter + LLMRouter 搜索总结组合

- 用户要求继续自主推进到方案结束；本轮承接 v5/v6 方案，把联网搜索来源上下文和 LLM 总结组合补齐。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已改用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest` 和 `.codex` 留痕降级执行。
- 写入 `.codex/context-scan-search-summary-combo.json` 和 `.codex/search-summary-combo-plan.md`；确认搜索和 LLM 是互补关系：SearchRouter 获取当前来源，LLMRouter 只基于 Agent 注入的来源总结。
- RED 验证：新增 InnerBrain 和 Agent 测试先失败，`联网查一下 Python 版本并总结` 被普通 `web.search` 吞掉，`/search` 结果未进入最近上下文。
- GREEN 实现：新增运行态 `RuntimeWebSearchContext`，`/search` 成功后持久化最近联网搜索结果，`/llm-context-preview` 注入标题、URL、摘要和来源；新增 `/search-summary`，明确总结时先搜索再调用 LLM。
- 补充 RED/GREEN：`/search-summary` 在 LLM 关闭时先因 `NoneType.usage` 崩溃；`/inner-brain-teach ... => /search-summary ...` 先保存为不一致的 `web.search_summary`。修复后 LLM 关闭返回搜索来源和启用提示，教学样本统一为 `web.search_summarize`，并优先执行 command slot。
- 专项验证：目标 3 个测试通过；新增补充 2 个测试通过。
- 收尾验证：`tests.test_inner_brain tests.test_agent` 217 项通过；全量 `unittest discover` 411 项通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；`/inner-brain-status` 显示 `seed_sample：92 条`；`/inner-brain-preview 联网查一下 Python 版本并总结` 输出 `web.search_summarize` 和 `/search-summary Python 版本`；默认 `/search-summary Python 版本` 输出联网搜索未启用提示；fake 搜索+fake LLM 自然语言 smoke 输出搜索来源和 `LLM 外脑总结`。
- 静态验证：`git diff --check` 退出 0（仅 LF/CRLF 工作区换行提示）；Markdown 本地链接检查通过；敏感信息差异扫描通过；`git ls-files config/llm.local.json config/search.local.json` 无输出。

## 2026-05-29 InnerBrain 多轮澄清状态与 0.1.7 安装包

- 用户要求继续下一阶段，并已授权按方案持续执行；本轮承接 `.codex/v6-clarification-state-plan.md` 和 v6 方案后续重点。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已按项目降级规则使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest` 和本地 smoke 执行。
- RED/GREEN：新增 3 个 Agent 测试先失败，导入路径补充落到 LLM、桌面快捷方式名称补充落到普通兜底、取消补充未清空 pending；实现后 4 个澄清相关测试通过。
- 实现：`JarvisAgent` 在 InnerBrain `CLARIFY` 时保存 pending `InnerBrainResult`，下一句输入先进入 `complete_inner_brain_clarification()` 补槽；补齐后复用既有 `NaturalLanguageIntent` 执行链路。
- 当前覆盖：`knowledge.import` 的 `source`、`desktop.delete_shortcut` 的 `items`，并支持“取消”“取消补充”“不用了”“先不用”“算了”取消 pending。
- 版本：将 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README 和版本一致性测试同步为 `0.1.7`。
- 验证：`tests.test_inner_brain tests.test_agent` 229 项通过；全量 `unittest discover` 423 项通过；源码桌面 smoke 通过。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.1.7.exe`；两者大小均为 57,069,568 bytes。
- 打包验证：打包后 `JarvisLite.exe --smoke` 通过；`install.cmd` 包含 `DisplayVersion /d "0.1.7"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.7 installation finished`。
- 文档同步：更新 README、`word/PROJECT-PLAN.md`、v6 方案、方案索引、今日进度、验证入口、日/月/周验证索引和正式文档索引。
- 提交前验证：全量 `unittest discover` 423 项通过；源码桌面 smoke 通过；打包后 exe smoke 退出码 0；`git diff --check` 退出 0 且仅 LF/CRLF 提示；Markdown 本地链接检查通过；敏感信息扫描通过；本地 LLM/Search 配置未被 Git 跟踪。

## 2026-05-29 InnerBrain 多轮澄清 query 补槽与 0.1.8 安装包

- 0.1.7 本地提交后继续按方案推进多轮澄清覆盖面；扫描确认 `query` 补槽框架已存在，但 `web.search` 和 `web.search_summarize` 映射仍从整句 prompt 重新抽 query。
- 写入 `.codex/context-scan-v6-clarification-query-slots.json` 和 `.codex/v6-clarification-query-slots-plan.md`。
- RED/GREEN：新增 2 个 Agent 测试先失败，澄清文案显示原始 `query`，没有 `/search 关键词` 或 `/search-summary 关键词`；补齐后不能继续执行搜索。修复后目标测试通过。
- 实现：`_sample_to_natural_language_intent()` 对 `web.search` 和 `web.search_summarize` 优先读取 `slots.query`；Agent 澄清提示把 `query` 显示为“查询关键词”并给出对应补全命令。
- 回归：`tests.test_inner_brain tests.test_agent` 231 项通过。
- 版本：将 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README 和版本一致性测试同步为 `0.1.8`。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.1.8.exe`；两者大小均为 57,069,568 bytes。
- 打包验证：打包后 `JarvisLite.exe --smoke` 通过；`install.cmd` 包含 `DisplayVersion /d "0.1.8"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.8 installation finished`。
- 提交前验证：全量 `unittest discover` 425 项通过；源码桌面 smoke 和打包后 exe smoke 均通过；`git diff --check` 退出 0 且仅 LF/CRLF 提示；Markdown 本地链接检查通过；敏感信息扫描通过；本地 LLM/Search 配置未被 Git 跟踪。
- Git 收尾：提交 `2edc81f feat: 增加联网搜索总结组合流程`，未 push。

## 2026-05-29 InnerBrain 编号+标签联合补槽与 0.1.9 安装包

- 继续 v6 多轮澄清覆盖面，本轮目标为 `document.tag_numbered_recent missing=result_index,tags`。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地文件读取、`update_plan`、`apply_patch`、`unittest`、PyInstaller 打包和 smoke 验证。
- 写入 `.codex/context-scan-v6-clarification-multi-slot-tags.json` 和 `.codex/v6-clarification-multi-slot-tags-plan.md`。
- RED/GREEN：新增 Agent 测试先失败，澄清文案显示原始 `result_index、tags`，且用户回复“第二份 项目 Python”时编号词可能污染标签；修复后目标测试通过。
- 实现：`_clarification_slots_from_reply()` 在已知 intent 的补槽阶段清理 tags 前缀编号词；Agent 澄清提示显示“编号、标签”，并给出“第二份 项目 Python”示例。
- 回归：`tests.test_inner_brain tests.test_agent` 232 项通过。
- 版本：将 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README 和版本一致性测试同步为 `0.1.9`。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.1.9.exe`；两者大小均为 57,069,568 bytes。
- 打包验证：源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`；打包后 `JarvisLite.exe --smoke` 退出码 0；`install.cmd` 包含 `DisplayVersion /d "0.1.9"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.9 installation finished`。
- 提交前验证：全量 `unittest discover` 426 项通过；源码桌面 smoke 通过；打包后 exe smoke 退出码 0；`git diff --check` 退出 0 且仅 LF/CRLF 提示；Markdown 本地链接检查通过；敏感信息扫描通过；本地 LLM/Search 配置未被 Git 跟踪。

## 2026-05-29 InnerBrain 目录别名和经验内容补槽与 0.1.10 安装包

- 继续 v6 多轮澄清覆盖面，本轮目标为 `directory.open_alias missing=alias` 和 `experience.record missing=experience`。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地文件读取、`rg`、`update_plan`、`apply_patch`、`unittest`、PyInstaller 打包和 smoke 验证。
- 写入 `.codex/context-scan-v6-clarification-alias-experience.json` 和 `.codex/v6-clarification-alias-experience-plan.md`。
- RED/GREEN：新增 2 个 Agent 测试先失败，澄清文案显示原始 `alias`/`experience`，且“目录是”“经验是”前缀不能清理；修复后目标测试通过。
- 实现：Agent 澄清提示显示“目录别名”“经验内容”并给出示例；`_normalize_clarification_value()` 在已知 pending 补槽阶段清理目录、别名、经验、关键词等补充前缀。
- 回归：`tests.test_inner_brain tests.test_agent` 234 项通过；全量 `unittest discover` 428 项通过；源码桌面 smoke 通过。
- 版本：将 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README 和版本一致性测试同步为 `0.1.10`。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.1.10.exe`；两者大小均为 57,069,568 bytes。
- 打包验证：打包后 `JarvisLite.exe --smoke` 退出码 0；`install.cmd` 包含 `DisplayVersion /d "0.1.10"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.10 installation finished`。
- 提交前验证：全量 `unittest discover` 428 项通过；源码桌面 smoke 通过；打包后 exe smoke 退出码 0；`git diff --check` 退出 0 且仅 LF/CRLF 提示；Markdown 本地链接检查通过；敏感信息扫描通过；本地 LLM/Search 配置未被 Git 跟踪。

## 2026-05-28 SearchRouter + LLMRouter 0.1.4 安装包

- 本轮继续自主推进可测试版本，目标是把搜索总结组合流程和前序 InnerBrain 迁移打成 `0.1.4` 安装包。
- 写入 `.codex/context-scan-search-summary-install-package-014.json` 和 `.codex/search-summary-install-package-014-plan.md`。
- RED 验证：将 `tests/test_project_metadata.py` 目标版本改为 `0.1.4` 后，版本一致性测试先失败，`pyproject.toml` 仍为 `0.1.3`。
- GREEN 实现：更新 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README、今日进度和验证记录到 `0.1.4`；版本一致性目标测试通过。
- 源码验证：全量 `unittest discover` 411 项通过；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- 打包验证：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 通过；`install.cmd` 包含 `taskkill`、`DisplayVersion /d "0.1.4"`、`Jarvis Lite 0.1.4 installed`、覆盖安装提示和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.4 installation finished`。
- 版本化产物：复制 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.4.exe`，大小与主安装包一致，均为 57,057,280 bytes。
- 静态验证：`git diff --check` 退出 0（仅 LF/CRLF 工作区换行提示）；Markdown 本地链接检查通过；敏感信息差异扫描通过；`git ls-files config/llm.local.json config/search.local.json` 无输出。
- Git 收尾：提交 `d9742ac chore: 发布搜索总结 0.1.4 测试版`，未 push。

## 2026-05-28 InnerBrain 显式文件名标签槽位迁移

- 承接 v6 方案剩余项，迁移 `给 note.txt 打标签 项目` 这类显式文件名标签动作。
- 写入 `.codex/context-scan-inner-brain-explicit-file-tag.json` 和 `.codex/inner-brain-explicit-file-tag-plan.md`。
- RED 验证：`tests.test_inner_brain.InnerBrainTests.test_explicit_file_tag_intents_use_sample_classifier_slots` 先失败，两个样例均返回 `command`/`legacy_fallback`。
- GREEN 实现：新增 `document.tag_path` seed 样本、签名归一化、`path/tags` 槽位抽取，并映射到既有 `/tag` 命令。
- 目标验证：`test_explicit_file_tag_intents_use_sample_classifier_slots`、`test_natural_language_tag_document_updates_document_tags`、`test_natural_language_mark_document_as_tags_updates_document_tags` 共 3 项通过。
- 收尾验证：`tests.test_inner_brain tests.test_agent` 217 项通过；全量 `unittest discover` 411 项通过；源码桌面 smoke 通过；`/inner-brain-preview 给 note.txt 打标签 项目` 输出 `document.tag_path`、`seed_sample` 和 `/tag "note.txt" 项目`。
- 静态验证：`git diff --check` 退出 0（仅 LF/CRLF 工作区换行提示）；Markdown 本地链接检查通过；敏感信息差异扫描通过；`git ls-files config/llm.local.json config/search.local.json` 无输出。

## 2026-05-28 v6 搜索后续动作与 0.1.5 安装包

- 用户要求无需继续人工回复，按方案一直执行到阶段结束；本轮在既有 v6 方案基础上继续收口。
- 写入 `.codex/context-scan-v6-finish.json` 和 `.codex/v6-finish-plan.md`；记录 sequential-thinking、shrimp-task-manager、code-index、exa 当前不可用的降级情况。
- RED 验证：搜索后续动作测试先失败，`打开第一条联网搜索结果` 被误识别为目录打开，`/search-save-summary` 未知，`导入这个搜索摘要到知识库` 被旧导入路径误吞。
- GREEN 实现：新增 `/search-open`、`/search-compare`、`/search-save-summary`、`/search-import-summary`，并迁移自然语言样本为 `web_search.open_numbered`、`web_search.compare_recent`、`web_search.save_summary`、`web_search.import_summary`。
- RED/GREEN：桌面快捷方式宾语前置表达 `把桌面快捷方式比特浏览器删掉` 先落到 LLM fallback；新增 `桌面快捷方式{item}删除` seed 样本、签名归一化和槽位抽取后通过。
- RED/GREEN：InnerBrain 缺槽澄清先只返回意图和缺失字段；新增补全命令、`/inner-brain-label` 和 `/inner-brain-teach` 提示后通过。
- RED/GREEN：版本一致性测试先因 `pyproject.toml` 仍为 `0.1.4` 失败；同步 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README 和元数据测试到 `0.1.5` 后通过。
- 验证：`tests.test_inner_brain tests.test_agent` 225 项通过；全量 `unittest discover` 419 项通过；源码桌面 smoke 通过；打包 exe smoke 通过。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.5.exe`；两者大小均为 57,065,472 bytes。
- 安装脚本验证：`install.cmd` 包含 `DisplayVersion /d "0.1.5"`、`Jarvis Lite 0.1.5 installed`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.5 installation finished`。
- 静态验证：`git diff --check` 退出 0（仅 LF/CRLF 工作区换行提示）；Markdown 本地链接检查通过；敏感信息差异扫描通过；`git ls-files config/llm.local.json config/search.local.json` 无输出。

## 2026-05-28 v6 高频 legacy 别名迁移与 0.1.6 安装包

- 用户要求不再等待人工反复回复“继续”，按已确认方案自主执行到阶段结束；本轮承接 `.codex/v6-legacy-aliases-plan.md`。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已改用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest` 和本地 smoke 降级执行。
- RED/GREEN：高频 legacy 别名测试先失败，29 个子用例返回 `source=legacy_fallback`；礼貌前缀编号最近文件导入先返回 `legacy.import_numbered_recent_file`。扩展 seed 样本和编号最近文件导入签名后目标测试通过。
- 专项验证：`tests.test_inner_brain tests.test_agent` 226 项通过；源码桌面 smoke 通过；代表句复扫 `legacy=0 unknown=0`。复扫脚本首次因引用不存在的 `jarvis_lite.paths` 失败，修正为 `build_project_paths` 后通过。
- RED/GREEN：版本一致性测试先因 `pyproject.toml` 仍为 `0.1.5` 失败；同步 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README 和元数据测试到 `0.1.6` 后通过。
- 全量验证：全量 `unittest discover` 420 项通过。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.1.6.exe`；两者大小均为 57,065,472 bytes。
- 打包验证：`..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke` 通过；`install.cmd` 包含 `DisplayVersion /d "0.1.6"`、`Jarvis Lite 0.1.6 installed`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.1.6 installation finished`。
- 静态验证：`git diff --check` 退出 0（仅 LF/CRLF 工作区换行提示）；Markdown 本地链接检查通过；敏感信息差异扫描通过；`git ls-files config/llm.local.json config/search.local.json` 无输出。

## 2026-05-29 InnerBrain 多轮澄清 v1 收口与 0.2.0 安装包

- 用户要求 push 后继续自主推进到 `0.2.0`；已先完成上一提交 `ea12db1` push，再把 `0.2.0` 定义为 InnerBrain 样本分类器优先 + LLM/Search 外脑互补 + 多轮澄清 v1 可安装闭环。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 写入 `.codex/context-scan-v020-clarification-closure.json` 和 `.codex/v020-clarification-closure-plan.md`，明确本轮不追求通用自然语言理解，而是收口当前已支持 intent 的主要 missing 槽位。
- RED/GREEN：新增 6 个 Agent 测试先失败，覆盖 `document.read_path path`、`document.read_numbered_recent result_index`、`document.tag_recent tags`、`tag_group.preview_tagging alias+tags`、`experience.search query` 和 `experience.advice query`。
- 实现：Agent 澄清提示按 intent 展示“文件路径”“经验关键词”“标签组”；编号资料提示改为“第二份”；标签组补槽只在已知 `tag_group.preview_tagging` pending clarification 下把第一个词作为 `alias`、后续词作为 `tags`。
- 版本：按 TDD 将 `tests/test_project_metadata.py` 目标版本先改为 `0.2.0` 并确认失败，再同步 `pyproject.toml`、`src/jarvis_lite/__init__.py` 和 README。
- 回归：目标 6 项通过；`tests.test_inner_brain tests.test_agent` 240 项通过；全量 `unittest discover` 434 项通过；源码桌面 smoke 通过。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.2.0.exe`；两者大小均为 57,073,664 bytes。
- 打包验证：打包后 `JarvisLite.exe --smoke` 退出码 0；`install.cmd` 包含 `DisplayVersion /d "0.2.0"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.2.0 installation finished`。
- 提交前验证：`git diff --check` 退出 0 且仅 LF/CRLF 提示；Markdown 本地链接检查通过；敏感信息扫描通过；本地 LLM/Search 配置未被 Git 跟踪。

## 2026-05-29 外脑 provider 配置闭环与 0.3.0 安装包

- 用户要求开始 `0.3.0` 阶段；本轮把 `0.3.0` 定义为外脑 provider 配置闭环 v1，目标是让 `qwen`/`gemini` 可作为直观 provider alias 进入现有 LLMRouter。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已记录降级，使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 写入 `.codex/context-scan-v030-llm-search-provider-closure.json`、`.codex/v030-llm-search-provider-closure-plan.md` 和 `word/plans/2026-05-29-v7-llm-provider-config-closure-plan.md`。
- RED/GREEN：新增 5 个 LLM/Agent 测试先失败，覆盖 `qwen` alias 构建、`gemini` 缺 `base_url` 诊断、qwen/gemini 配置模板和 `/llm-enable` 状态展示；实现后目标测试通过。
- 实现：新增 `LLM_PROVIDER_ALIASES`、`LLMSettings.adapter_provider`，`build_llm_router()` 对 alias 复用 `OpenAIResponsesProvider`；状态展示保留原始 `Provider` 并补充实际 `Adapter`。
- 版本：按 TDD 将 `tests/test_project_metadata.py` 目标版本先改为 `0.3.0` 并确认失败，再同步 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README 和方案文档。
- 回归：`tests.test_llm tests.test_agent` 251 项通过；全量 `unittest discover` 438 项通过；源码桌面 smoke 通过。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.3.0.exe`；两者大小均为 57,069,568 bytes。
- 打包验证：打包后 `JarvisLite.exe --smoke` 退出码 0；`install.cmd` 包含 `DisplayVersion /d "0.3.0"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.3.0 installation finished`。
- 提交前验证：`git diff --check` 退出 0 且仅 LF/CRLF 提示；Markdown 本地链接检查通过；敏感信息扫描未命中常见 API key 模式；本地 LLM/Search 配置未被 Git 跟踪。

## 2026-05-29 运行态配置初始化与 0.4.0 安装包

- 用户要求继续 `0.4.0`；本轮把 `0.4.0` 定义为运行态外脑与联网搜索配置初始化 v1，减少安装后手动复制模板和定位本机配置目录的摩擦。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已记录降级，使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 写入 `.codex/context-scan-v040-runtime-config-init.json`、`.codex/v040-runtime-config-init-plan.md` 和 `word/plans/2026-05-29-v8-runtime-config-init-plan.md`。
- RED/GREEN：新增 4 个 Agent 测试先失败，覆盖 `/llm-config-init qwen` 草稿创建、已有 LLM 配置不覆盖且不泄漏 key、`/search-config-init tavily` 草稿创建和自然语言配置初始化入口；实现后通过。
- 实现：新增 `write_llm_local_config_draft()`、`write_search_local_config_draft()`，新增 `/llm-config-init [provider]` 与 `/search-config-init [provider]` 命令，草稿敏感字段为空，已有配置不覆盖。
- InnerBrain：新增“生成外脑配置”“创建外脑配置文件”“生成联网搜索配置”“创建搜索配置文件”seed 样本，仍通过 `JarvisAgent` 执行命令。
- 版本：按 TDD 将 `tests/test_project_metadata.py` 目标版本先改为 `0.4.0` 并确认失败，再同步 `pyproject.toml`、`src/jarvis_lite/__init__.py` 和 README。
- 回归：目标 5 项通过；`tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search` 289 项通过；全量 `unittest discover` 442 项通过；源码桌面 smoke 通过。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.4.0.exe`；两者大小均为 57,073,664 bytes。
- 打包验证：打包后 `JarvisLite.exe --smoke` 退出码 0；`install.cmd` 包含 `DisplayVersion /d "0.4.0"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.4.0 installation finished`。
- 接手后最终复验：重新执行全量 `unittest discover` 442 项通过；源码桌面 smoke 通过；重新构建安装器并复制 `JarvisLiteSetup-0.4.0.exe`；打包后 exe smoke 退出码 0；`git diff --check`、Markdown 本地链接、敏感信息扫描均通过；本地 LLM/Search 配置未被 Git 跟踪。

## 2026-05-29 本地配置检查与 0.5.0 安装包

- 用户要求继续推进；本轮把 `0.5.0` 定义为本地配置检查 v1，补齐 `0.4.0` 生成草稿后的只读检查闭环。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已记录降级，使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 写入 `.codex/context-scan-v050-config-check.json`、`.codex/v050-config-check-plan.md` 和 `word/plans/2026-05-29-v9-runtime-config-check-plan.md`。
- RED/GREEN：新增 4 个 Agent 测试先失败，覆盖 `/llm-config-check`、`/search-config-check`、LLM 无效 JSON 报告和自然语言配置检查入口；实现后目标测试通过。
- 实现：新增 `/llm-config-check` 与 `/search-config-check` 命令，复用 Router.describe() 做只读诊断；命令只读取本地配置和环境变量，不发起网络请求，不显示真实 API key。
- 修复：`LLMSettings.configuration_issues()` 在 `provider=off` 且存在 config_error 时不再吞掉 JSON 错误。
- InnerBrain：新增“检查外脑配置”“看看外脑配置有没有问题”“检查联网搜索配置”“看看搜索配置有没有问题”seed 样本。
- 版本：按 TDD 将 `tests/test_project_metadata.py` 目标版本先改为 `0.5.0` 并确认失败，再同步 `pyproject.toml`、`src/jarvis_lite/__init__.py` 和 README。
- 回归：目标 5 项通过；`tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search` 首次因测试清单版本仍为 `0.4.1` 失败，改为 `0.5.1` 后 293 项通过；全量 `unittest discover` 446 项通过。
- Smoke：源码桌面 smoke 通过；`/llm-config-check` 与 `/search-config-check` CLI smoke 通过；打包后 `JarvisLite.exe --smoke` 退出码 0。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.5.0.exe`；两者大小均为 57,077,760 bytes。
- 打包验证：`install.cmd` 包含 `DisplayVersion /d "0.5.0"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.5.0 installation finished`。

## 2026-05-29 本地配置写入与 0.6.0 安装包

- 用户要求继续；本轮把 `0.6.0` 定义为本地配置写入 v1，在 `/llm-config-init`、`/search-config-init` 和配置检查后补齐运行态写入命令。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已按项目降级规则使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 写入 `.codex/context-scan-v060-config-set.json`、`.codex/v060-config-set-plan.md` 和 `word/plans/2026-05-29-v10-runtime-config-set-plan.md`。
- RED/GREEN：新增 6 个 Agent 测试先失败，覆盖 `/llm-config-set`、`/search-config-set`、保留未指定字段、错误不部分写入、自然语言配置写入用法和 API key 不泄漏；实现后目标测试通过。
- 实现：新增 `write_llm_local_config_values()`、`write_search_local_config_values()`，新增 `/llm-config-set key=value ...` 与 `/search-config-set key=value ...` 命令，写入响应和日志仅展示字段名。
- InnerBrain：新增“设置外脑配置”“修改外脑配置”“设置联网搜索配置”“修改搜索配置”seed 样本，入口只返回显式命令用法。
- 版本：按 TDD 将 `tests/test_project_metadata.py` 目标版本先改为 `0.6.0` 并确认失败，再同步 `pyproject.toml`、`src/jarvis_lite/__init__.py` 和 README。
- 回归：目标 7 项通过；`tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search` 299 项通过；全量 `unittest discover` 452 项通过。
- Smoke：源码桌面 smoke 通过；`/llm-config-set`、`/llm-config-check`、`/search-config-set`、`/search-config-check` CLI smoke 通过，CLI smoke 后已删除临时 `config/*.local.json`；打包后 `JarvisLite.exe --smoke` 退出码 0。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.6.0.exe`；两者大小均为 57,081,856 bytes。
- 打包验证：`install.cmd` 包含 `DisplayVersion /d "0.6.0"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.6.0 installation finished`。
- 静态验证：`git diff --check` 退出 0（仅 LF/CRLF 工作区换行提示）；Markdown 本地链接检查通过；敏感信息扫描通过；本地 LLM/Search 配置未被 Git 跟踪且文件不存在。

## 2026-05-29 连通性诊断与 0.7.0 安装包

- 用户要求继续下一阶段；本轮把 `0.7.0` 定义为连通性诊断 v1，在本地配置写入后补齐 LLM/Search 可控 smoke 测试。
- 当前会话未提供 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已按项目降级规则使用技能文件、`rg`、本地文件读取、`update_plan`、`apply_patch`、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 写入 `.codex/context-scan-v070-smoke-diagnostics.json`、`.codex/v070-smoke-diagnostics-plan.md` 和 `word/plans/2026-05-29-v11-smoke-diagnostics-plan.md`。
- RED/GREEN：新增 5 个 Agent 测试和 1 个版本测试先失败，覆盖 `/llm-smoke` 运行中重读本地配置、`/search-smoke` 新命令、搜索 smoke 不污染最近上下文、自然语言 smoke 入口和 `0.7.0` 元数据；实现后目标测试通过。
- 实现：`/llm-smoke` 在非注入 router 场景下执行前重建 `LLMRouter`；新增 `/search-smoke [query]`，执行前重建 `SearchRouter`，默认查询 `Python 版本`，只输出 provider 调用结果，不调用 `_remember_recent_web_search()`。
- InnerBrain：新增“测试外脑连接”“检查外脑连接”“测试联网搜索连接”“检查搜索连接”seed 样本；`TEACHABLE_INNER_BRAIN_COMMAND_INTENTS` 和 LLM 命令白名单同步新增 `/llm-smoke`、`/search-smoke`。
- 版本：按 TDD 将 `tests/test_project_metadata.py` 目标版本先改为 `0.7.0` 并确认失败，再同步 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README、PROJECT-PLAN、方案索引和验证记录。
- 回归：目标 6 项通过；`tests.test_agent tests.test_inner_brain tests.test_llm tests.test_search` 304 项通过；全量 `unittest discover` 457 项通过。
- Smoke：源码桌面 smoke 通过；`/llm-smoke` 与 `/search-smoke` CLI fake 配置 smoke 通过，CLI smoke 后已删除临时 `config/*.local.json`；打包后 `JarvisLite.exe --smoke` 退出码 0。
- 打包：`scripts\build_windows_installer.py` 生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`，复制 `JarvisLiteSetup-0.7.0.exe`；两者大小均为 57,081,856 bytes。
- 打包验证：`install.cmd` 包含 `DisplayVersion /d "0.7.0"`、覆盖安装和用户数据保留提示；`JarvisLiteSetup.sed` 包含 `Jarvis Lite 0.7.0 installation finished`。
- 静态验证：`git diff --check` 退出 0（仅 LF/CRLF 工作区换行提示）；Markdown 本地链接检查通过；敏感信息扫描通过；本地 LLM/Search 配置未被 Git 跟踪且文件不存在。
## 2026-05-29 0.8.0 桌面配置面板

- 时间：2026-05-29 14:30
- 工具：rg / Select-String / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 0.8.0 聚焦桌面配置面板 v1；当前缺口是桌面用户必须手敲配置命令，且直接输入 api_key 会进入面板 transcript。已记录 `.codex/context-scan-v080-desktop-config-panel.json` 和 `.codex/v080-desktop-config-panel-plan.md`。
- 降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP，按项目约定记录降级并使用本地检索与 TDD 流程。

- 时间：2026-05-29 15:00
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- 摘要：完成桌面配置面板 v1；新增 `send_sensitive`、外脑/联网搜索配置控件和脱敏写入；版本提升到 `0.8.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.8.0.exe`。
- 验证：目标测试 6 项通过，邻近回归 316 项通过，全量 unittest 462 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，静态与敏感扫描通过。

## 2026-05-29 0.9.0 LLM 外脑多轮澄清

- 时间：2026-05-29 15:20
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 0.9.0 聚焦 LLM 外脑多轮澄清 v1；当前缺口是 LLM 返回 `clarify` 后只单次提示，不保存原始问题和澄清上下文，用户后续补充会被当作新输入。已记录 `.codex/context-scan-v090-llm-clarification.json`、`.codex/v090-llm-clarification-plan.md` 和 `word/plans/2026-05-29-v13-llm-clarification-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index MCP；按项目降级规则使用本地检索、计划文件和 TDD 留痕。

- 时间：2026-05-29 15:45
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 3 个 Agent 测试和 1 个版本测试先失败，覆盖 LLM 澄清后补充执行最终命令、补充后返回 answer、取消补充不二次调用 provider 和版本提升；实现 pending LLM 澄清状态后目标测试通过。
- 实现：`JarvisAgent` 新增 `PendingLLMClarification` 和 `_pending_llm_clarification`，在 InnerBrain pending 后优先消费 LLM 待澄清；补充信息会与原始问题和澄清问题组成续聊 prompt，最终仍走 LLM 白名单命令处理。
- 摘要：完成 LLM 外脑多轮澄清 v1；版本提升到 `0.9.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.9.0.exe`。
- 验证：目标测试 4 项通过，邻近回归 332 项通过，全量 unittest 465 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- 提交：`cc363cb feat: 增加 LLM 外脑多轮澄清 0.9.0`。
- 推送：前两次 `openssl` push 分别因连接 reset 和 443 超时失败；`Test-NetConnection github.com -Port 443` 成功后，改用 `schannel` push 成功，远端 `main` 已更新到 `cc363cb`。

## 2026-05-29 0.10.0 LLM 外脑澄清状态持久化

- 时间：2026-05-29 16:05
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 0.10.0 聚焦 LLM 外脑澄清状态持久化和可观察；当前缺口是 0.9.0 的 `_pending_llm_clarification` 只存在于当前 Agent 内存，桌面重启后丢失，最近上下文也看不到待补充外脑问题。已记录 `.codex/context-scan-v0100-llm-clarification-runtime.json`、`.codex/v0100-llm-clarification-runtime-plan.md` 和 `word/plans/2026-05-29-v14-llm-clarification-runtime-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index MCP；按项目降级规则使用本地检索、计划文件和 TDD 留痕。

- 时间：2026-05-29 16:50
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 3 个 Agent 测试和 1 个版本测试先失败，覆盖 LLM pending 跨 Agent 恢复、`/recent-context` 可观察且不消耗 pending、取消补充清理运行态 pending 和版本提升；实现后目标测试通过。
- 实现：`RuntimeContext` 新增 `pending_llm_clarification`；`JarvisAgent` 启动时恢复 LLM pending，LLM clarify、补齐、取消和无结果路径都会同步保存；`/recent-context` 直接展示待补充外脑问题和原始问题。
- 摘要：完成 LLM 外脑澄清状态持久化 v1；版本提升到 `0.10.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.10.0.exe`。
- 验证：目标测试 4 项通过，邻近回归 335 项通过，全量 unittest 468 项通过，源码桌面 smoke 通过，打包后 exe smoke 命令退出码 0，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-05-29 0.11.0 LLM 外脑澄清轮数与过期策略

- 时间：2026-05-29 17:20
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 0.11.0 聚焦 LLM pending 澄清的轮数上限与过期清理；当前缺口是 0.10.0 的 pending 可长期残留，且 LLM 连续返回 `clarify` 时容易把已经组合过的 prompt 当作新的原始问题。已记录 `.codex/context-scan-v0110-llm-clarification-guard.json`、`.codex/v0110-llm-clarification-guard-plan.md` 和 `word/plans/2026-05-29-v15-llm-clarification-guard-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-05-29 17:55
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 3 个 Agent 测试和 1 个版本测试先失败，覆盖连续澄清保留最初原始问题并递增轮次、超过最大轮数后清空 pending、过期 runtime pending 启动后清理和版本提升；实现后目标测试通过。
- 实现：`PendingLLMClarification` 与 `RuntimeLLMClarificationContext` 新增 `clarification_count` 和 `created_at`；连续 LLM `clarify` 保留最初 `original_prompt` 并更新轮次；超过 3 轮时清空 pending；启动恢复时清理超过 12 小时的 pending；`/recent-context` 显示轮次和过期策略。
- 摘要：完成 LLM 外脑澄清轮数与过期策略 v1；版本提升到 `0.11.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.11.0.exe`。
- 验证：目标测试 4 项通过，邻近回归 338 项通过，全量 unittest 471 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.11.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-05-29 0.12.0 桌面外脑待补充状态

- 时间：2026-05-29 16:20
- 工具：Get-Content / git diff / update_plan / apply_patch / unittest / PyInstaller / IExpress
- 摘要：继续下一阶段，确认 `0.12.0` 聚焦桌面外脑待补充状态固定展示；当前缺口是 0.11.0 已有可靠 pending，但用户需要手动点“最近上下文”才知道外脑正在等待补充。已记录 `.codex/context-scan-v0120-desktop-llm-pending-status.json`、`.codex/v0120-desktop-llm-pending-status-plan.md` 和 `word/plans/2026-05-29-v16-desktop-llm-pending-status-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-05-29 16:35
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 1 个 Bridge 测试、3 个 Panel 测试和 1 个版本测试先失败，覆盖 LLM clarify 后状态快照、桌面面板固定展示、取消后刷新、重启恢复和版本提升；实现后目标测试通过。
- 实现：`JarvisAgent` 新增 `llm_clarification_status_text()` 只读状态；`DesktopResponse` 和 `DesktopBridge` 透传 `llm_pending_status_text`；`AssistantPanel` 新增 `llmPendingStatusLabel`，启动时读取状态并在每次响应后刷新。
- 摘要：完成桌面外脑待补充状态 v1；版本提升到 `0.12.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.12.0.exe`。
- 验证：目标测试 5 项通过，邻近回归 347 项通过，全量 unittest 474 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.12.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-05-29 0.13.0 桌面外脑运行状态

- 时间：2026-05-29 16:40
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.13.0` 聚焦外脑运行状态与最近调用结果；当前缺口是 0.12.0 只能显示 pending，仍无法直观看出某次聊天是否真的走了 LLM 外脑、返回类型是什么。已记录 `.codex/context-scan-v0130-desktop-llm-activity-status.json`、`.codex/v0130-desktop-llm-activity-status-plan.md` 和 `word/plans/2026-05-29-v17-desktop-llm-activity-status-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-05-29 16:55
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 2 个 Agent 测试、1 个 Bridge 测试、2 个 Panel 测试和 1 个版本测试先失败，覆盖最近外脑调用快照、跨启动恢复、桌面响应透传、面板固定展示和版本提升；实现后目标测试通过。
- 实现：`RuntimeContext` 新增 `recent_llm_call`；`JarvisAgent` 在 LLM fallback、smoke、搜索总结/比较、摘要保存和澄清补充路径记录最近调用；`DesktopResponse`、`DesktopBridge` 和 `AssistantPanel` 新增外脑运行状态透传和固定展示。
- 摘要：完成桌面外脑运行状态 v1；版本提升到 `0.13.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.13.0.exe`。
- 验证：目标测试 6 项通过，邻近回归 351 项通过，全量 unittest 478 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.13.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-05-29 0.14.0 最近路由决策状态

- 时间：2026-05-29 17:10
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / PyInstaller / IExpress / git diff --check
- 摘要：继续下一阶段，确认 `0.14.0` 聚焦最近路由决策状态；当前缺口是 0.13.0 只能显示 LLM 是否调用，仍无法说明某条回复是命令、本地内脑、知识库、LLM fallback 还是记忆兜底。已记录 `.codex/context-scan-v0140-route-decision-status.json`、`.codex/v0140-route-decision-status-plan.md` 和 `word/plans/2026-05-29-v18-route-decision-status-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-05-29 17:35
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 3 个 Agent 测试、1 个 Bridge 测试、2 个 Panel 测试和 1 个版本测试先失败，覆盖 InnerBrain 问候不调用外脑、LLM fallback 路由、身份记忆路由、桌面响应透传、面板固定展示和版本提升；实现后目标测试通过。
- 实现：`RuntimeContext` 新增 `recent_route_decision`；`JarvisAgent` 在 `command`、身份记忆、记忆写入、`inner-brain`、`inner-brain-clarify`、`knowledge`、`llm-fallback` 和 `memory-fallback` 路径记录最近路由；`DesktopResponse`、`DesktopBridge` 和 `AssistantPanel` 新增路由状态透传和固定展示。
- 摘要：完成最近路由决策状态 v1；版本提升到 `0.14.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.14.0.exe`。
- 验证：目标测试 7 项通过，邻近回归 356 项通过，全量 unittest 483 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.14.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-05-29 0.15.0 路由解释详情

- 时间：2026-05-29 18:06
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.15.0` 聚焦最近路由决策的解释详情；当前缺口是 0.14.0 只能展示由哪一层处理，无法直接看到 InnerBrain 的 source/confidence/reason、澄清缺失槽位或 LLM fallback 的外脑调用摘要。已记录 `.codex/context-scan-v0150-route-decision-explanation.json` 和 `.codex/v0150-route-decision-explanation-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-05-29 18:20
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 4 个 Agent 测试并扩展 1 个 Bridge 测试、1 个 Panel 测试和 1 个版本测试先失败，覆盖 InnerBrain 执行依据、InnerBrain 澄清缺失槽位依据、路由解释跨 Agent 恢复、LLM fallback provider/model/type/summary/reason 依据、桌面透传和版本提升；实现后目标测试通过。
- 实现：`RuntimeRouteDecisionContext` 新增 `explanation`；`RuntimeLLMCallContext` 新增 `reason`；`JarvisAgent.route_status_text()` 追加 `依据` 行；InnerBrain 路径展示 source/confidence/missing/reason；LLM fallback 展示 provider/model/source/type/summary/reason；命令、知识库和记忆路径展示简短 source/action。
- 摘要：完成路由解释详情 v1；版本提升到 `0.15.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.15.0.exe`。
- 验证：目标测试 10 项通过，邻近回归 360 项通过，全量 unittest 487 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.15.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-05-29 0.16.0 最近路由历史

- 时间：2026-05-29 18:25
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.16.0` 聚焦最近多次路由历史；当前缺口是 0.15.0 只能展示最新一条路由依据，无法观察连续输入中 InnerBrain、LLM fallback、命令和记忆兜底的切换轨迹。已记录 `.codex/context-scan-v0160-route-history.json` 和 `.codex/v0160-route-history-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-05-29 18:55
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 3 个 Agent 测试、1 个 Bridge 测试、1 个 Panel 测试和 1 个版本测试先失败，覆盖最近路由历史展示、跨 Agent 恢复、最多 5 条、桌面透传和版本提升；实现后目标测试通过。
- 实现：`RuntimeContext` 新增 `recent_route_decisions`；运行态读写兼容旧 `recent_route_decision`；`JarvisAgent._remember_route_decision()` 同步保存最新路由和最近 5 条历史；`route_status_text()` 追加“最近路由历史”短列表；桌面复用既有 Bridge/Panel 透传。
- 摘要：完成最近路由历史 v1；版本提升到 `0.16.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.16.0.exe`。
- 验证：目标测试 6 项通过，邻近回归 365 项通过，全量 unittest 492 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.16.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-05-29 0.17.0 路由历史详情

- 时间：2026-05-29 18:39
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.17.0` 聚焦路由历史详情命令和最近上下文集成；当前缺口是 0.16.0 桌面状态只展示压缩短历史，用户需要可读、可复制的明细来判断某条回复来自 InnerBrain、LLM fallback、知识库、命令还是记忆兜底。已记录 `.codex/context-scan-v0170-route-history-detail.json`、`.codex/v0170-route-history-detail-plan.md` 和 `word/plans/2026-05-29-v21-route-history-detail-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-05-29 18:50
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 4 个 Agent 测试和 1 个版本测试先失败，覆盖 `/route-history` 空历史、最近路由完整详情、跨 Agent 恢复、`/recent-context` 路由摘要和版本提升；实现后目标测试通过。
- 实现：`JarvisAgent` 新增 `/route-history` 详情入口、路由详情格式化、`/recent-context` 最近路由摘要，并让这两个只读诊断入口不写入路由历史，避免查询动作污染测试轨迹。
- 摘要：完成路由历史详情 v1；版本提升到 `0.17.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.17.0.exe`。
- 验证：目标测试 5 项通过，邻近回归 369 项通过，全量 unittest 496 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.17.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-05-29 0.18.0 InnerBrain 训练候选

- 时间：2026-05-29 18:53
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.18.0` 聚焦基于最近路由历史展示 InnerBrain 训练候选；当前缺口是 0.17.0 能看见完整路由，但还没有把 LLM fallback、记忆兜底或 InnerBrain 澄清场景整理成可人工教学的候选清单。已记录 `.codex/context-scan-v0180-inner-brain-candidates.json`、`.codex/v0180-inner-brain-candidates-plan.md` 和 `word/plans/2026-05-29-v22-inner-brain-candidates-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-05-29 19:08
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 3 个 Agent 测试和 1 个版本测试先失败，覆盖空候选、不污染路由历史、LLM fallback/记忆兜底候选、跨 Agent 恢复和版本提升；实现后目标测试通过。
- 实现：`JarvisAgent` 新增 `/inner-brain-candidates` 只读入口，从最近路由历史筛选 `llm-fallback`、`memory-fallback`、`inner-brain-clarify`，展示候选输入、当前路由、结果、依据以及 teach/label 示例；不自动训练，不污染路由历史。
- 摘要：完成 InnerBrain 训练候选 v1；版本提升到 `0.18.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.18.0.exe`。
- 验证：目标测试 4 项通过，邻近回归 372 项通过，全量 unittest 499 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.18.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.19.0 InnerBrain 候选按编号教学

- 时间：2026-06-01 09:16
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.19.0` 聚焦从训练候选按编号教学为明确命令；当前缺口是 0.18.0 能列候选，但用户仍要复制候选原文才能执行 `/inner-brain-teach`。已记录 `.codex/context-scan-v0190-inner-brain-teach-candidate.json`、`.codex/v0190-inner-brain-teach-candidate-plan.md` 和 `word/plans/2026-06-01-v23-inner-brain-teach-candidate-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-06-01 09:34
- 工具：unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- RED/GREEN：新增 3 个 Agent 测试和 1 个版本测试先失败，覆盖候选按编号教学、候选不存在、未知目标命令和版本提升；实现后目标测试 4 项通过。
- 实现：`JarvisAgent` 新增 `/inner-brain-teach-candidate 编号 => /命令`，复用 `/inner-brain-candidates` 的候选筛选顺序和 `_save_inner_brain_teach_command()`；教学入口不写入最近路由历史。
- 摘要：完成 InnerBrain 候选按编号教学 v1；版本提升到 `0.19.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.19.0.exe`。
- 验证：目标测试 4 项通过，邻近回归 375 项通过，全量 unittest 502 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.19.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.20.0 InnerBrain 候选按编号标注

- 时间：2026-06-01 09:40
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.20.0` 聚焦 `/inner-brain-label-candidate 编号 => intent [slot=value ...]`，用于把候选按编号标注为非命令型 runtime 样本；当前缺口是 0.19.0 只能按编号教学为命令，非命令型标注仍需复制候选原文。已记录 `.codex/context-scan-v0200-inner-brain-label-candidate.json`、`.codex/v0200-inner-brain-label-candidate-plan.md` 和 `word/plans/2026-06-01-v24-inner-brain-label-candidate-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-06-01 09:45
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 3 个 Agent 测试和 1 个版本测试先失败，覆盖候选按编号标注、候选不存在、slot 格式错误和版本提升；实现后目标测试 4 项通过。
- 实现：`JarvisAgent` 新增 `/inner-brain-label-candidate 编号 => intent [slot=value ...]`，复用 `/inner-brain-candidates` 的候选筛选顺序和 `/inner-brain-label` 的保存逻辑；标注入口不写入最近路由历史。
- 摘要：完成 InnerBrain 候选按编号标注 v1；版本提升到 `0.20.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.20.0.exe`。
- 验证：目标测试 4 项通过，邻近回归 378 项通过，全量 unittest 505 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.20.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.21.0 InnerBrain 候选频次排序

- 时间：2026-06-01 09:50
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.21.0` 聚焦 `/inner-brain-candidates` 的重复候选聚合与频次排序；当前缺口是 0.20.0 能按编号教学/标注，但重复 fallback 输入不会优先展示。已记录 `.codex/context-scan-v0210-inner-brain-candidate-frequency.json`、`.codex/v0210-inner-brain-candidate-frequency-plan.md` 和 `word/plans/2026-06-01-v25-inner-brain-candidate-frequency-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-06-01 10:38
- 工具：apply_patch / unittest / PyInstaller / IExpress / git diff --check
- RED/GREEN：新增 3 个 Agent 测试和 1 个版本测试先失败，覆盖重复候选优先排序、编号教学使用频次排序、编号标注使用频次排序和版本提升；实现后目标测试 4 项通过。
- 实现：`JarvisAgent` 新增 `InnerBrainCandidateSummary`，`/inner-brain-candidates` 按 prompt 精确聚合最近 5 条候选，按出现次数降序、同频按最近一次出现顺序展示；编号教学和编号标注复用同一候选排序。
- 摘要：完成 InnerBrain 候选频次排序 v1；版本提升到 `0.21.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.21.0.exe`。
- 验证：目标测试 4 项通过，邻近回归 381 项通过，全量 unittest 508 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.21.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
## 2026-06-01 0.22.0 InnerBrain 候选运行态统计

- 工具降级：sequential-thinking、shrimp-task-manager、code-index、exa 当前会话不可用；已用 `rg`、定向文件读取、`update_plan` 和 TDD 流程替代。
- 完成 0.21.0 提交并推送：`e6ebf0e feat: 支持候选频次排序 0.21.0`。
- 新增 RED 测试：候选统计跨最近历史保留、编号教学使用运行态排序、教学后移除候选、版本提升。
- 实现：新增 `RuntimeInnerBrainCandidateContext`，在 `JarvisAgent` 记录候选路由时维护本地运行态候选统计。
- 实现：`/inner-brain-candidates`、`/inner-brain-teach-candidate`、`/inner-brain-label-candidate` 共用运行态候选统计编号。
- 实现：teach、label、adopt 后移除对应候选统计。
- 修复：版本升到 0.22.0 后，更新测试 manifest 从 `0.21.1` 调整为 `0.22.1`，保持“可更新”夹具高于当前版本。
- 验证：目标 GREEN 4 项 OK，相邻回归 384 项 OK，全量 unittest 511 项 OK。
- 打包：生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.22.0.exe`，大小 `57,106,432` 字节。

## 2026-06-01 0.23.0 桌面内脑候选快捷入口

- 时间：2026-06-01 11:07
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.23.0` 聚焦桌面面板和托盘直接打开 `/inner-brain-candidates`；当前缺口是候选列表已具备运行态统计和编号训练闭环，但桌面测试时仍需要手输命令。已记录 `.codex/context-scan-v0230-desktop-inner-brain-candidate-shortcut.json`、`.codex/v0230-desktop-inner-brain-candidate-shortcut-plan.md` 和 `word/plans/2026-06-01-v27-desktop-inner-brain-candidate-shortcut-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-06-01 11:15
- 工具：apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- RED/GREEN：新增 4 个桌面快捷入口测试和 1 个版本测试先失败，覆盖快捷命令能力清单、直接快捷命令清单、桌面按钮展示、点击“内脑候选”执行 `/inner-brain-candidates` 和版本提升；实现后目标测试 5 项通过。
- 实现：`quick_commands()` 新增 `QuickCommand("内脑候选", "/inner-brain-candidates")`，`DIRECT_QUICK_COMMAND_PROMPTS` 纳入 `/inner-brain-candidates`；不改变后端路由、不新增自然语言正则、不自动训练。
- 修复：版本升到 0.23.0 后，更新测试 manifest 从 `0.22.1` 调整为 `0.23.1`，保持“可更新”夹具高于当前版本。
- 摘要：完成桌面内脑候选快捷入口；版本提升到 `0.23.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.23.0.exe`。
- 验证：目标测试 5 项通过，相邻回归 385 项通过，全量 unittest 512 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.23.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.24.0 桌面候选训练模板填充

- 时间：2026-06-01 11:20
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.24.0` 聚焦桌面面板按候选编号填入 teach/label 模板；当前缺口是 0.23.0 已能一键打开候选列表，但仍需要用户手动输入完整 `/inner-brain-teach-candidate` 或 `/inner-brain-label-candidate` 模板。已记录 `.codex/context-scan-v0240-desktop-inner-brain-candidate-template.json`、`.codex/v0240-desktop-inner-brain-candidate-template-plan.md` 和 `word/plans/2026-06-01-v28-desktop-inner-brain-candidate-template-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-06-01 11:35
- 工具：apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- RED/GREEN：新增 3 个桌面候选模板测试和 1 个版本测试先失败，覆盖候选编号控件、填教学只填输入框不提交、填标注按编号填入模板和版本提升；实现后目标测试 4 项通过。
- 实现：`AssistantPanel` 新增候选编号 `QSpinBox`、`填教学`、`填标注` 按钮和输入框填充方法；填充动作只写 `conversationInput`、设置光标和焦点，不调用提交、不写 transcript。
- 修复：版本升到 0.24.0 后，更新测试 manifest 从 `0.23.1` 调整为 `0.24.1`，保持“可更新”夹具高于当前版本。
- 摘要：完成桌面候选训练模板填充；版本提升到 `0.24.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.24.0.exe`。
- 验证：目标测试 4 项通过，相邻回归 388 项通过，全量 unittest 515 项通过，源码桌面 smoke 通过，打包后 exe smoke 退出码 0，安装脚本文案为 `0.24.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.25.0 桌面候选模板状态同步

- 时间：2026-06-01 11:41
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.25.0` 聚焦 `/inner-brain-candidates` 后同步桌面候选模板状态；当前缺口是 0.24.0 已能填 teach/label 模板，但按钮和编号上限不会随候选列表是否存在而变化。已记录 `.codex/context-scan-v0250-desktop-inner-brain-candidate-template-sync.json`、`.codex/v0250-desktop-inner-brain-candidate-template-sync-plan.md` 和 `word/plans/2026-06-01-v29-desktop-inner-brain-candidate-template-sync-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-06-01 11:57
- 工具：apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- RED/GREEN：新增 2 个桌面候选模板状态同步测试和 1 个版本测试先失败，覆盖空候选禁用按钮、有候选同步编号上限和版本提升；实现后目标测试 3 项通过。
- 实现：`AssistantPanel._append_response()` 在收到 `/inner-brain-candidates` 响应后同步候选模板状态；空候选显示“候选模板：暂无候选”并禁用模板按钮，有候选显示数量、启用按钮并同步编号上限。
- 修复：版本升到 0.25.0 后，更新测试 manifest 从 `0.24.1` 调整为 `0.25.1`，保持“可更新”夹具高于当前版本。
- 摘要：完成桌面候选模板状态同步；版本提升到 `0.25.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.25.0.exe`。
- 验证：目标测试 3 项通过，相邻回归 390 项通过，全量 unittest 517 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.25.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.26.0 桌面候选选择绑定

- 时间：2026-06-01 12:00
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.26.0` 聚焦把 `/inner-brain-candidates` 的单条候选绑定到桌面下拉选择；当前缺口是 0.25.0 会同步按钮和编号上限，但用户仍要在 transcript 中查候选编号。已记录 `.codex/context-scan-v0260-desktop-inner-brain-candidate-selection.json`、`.codex/v0260-desktop-inner-brain-candidate-selection-plan.md` 和 `word/plans/2026-06-01-v30-desktop-inner-brain-candidate-selection-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-06-01 12:09
- 工具：apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- RED/GREEN：新增 2 个桌面候选选择绑定测试和 1 个版本测试先失败，覆盖空候选禁用下拉框、有候选展示候选选项、选择候选同步编号、模板使用所选编号和版本提升；实现后目标测试 3 项通过。
- 实现：`AssistantPanel` 新增候选下拉框；从候选响应文本解析 `N. 文本` 行并填充选项；下拉框和候选编号 stepper 双向同步。
- 修复：版本升到 0.26.0 后，更新测试 manifest 从 `0.25.1` 调整为 `0.26.1`，保持“可更新”夹具高于当前版本。
- 摘要：完成桌面候选选择绑定；版本提升到 `0.26.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.26.0.exe`。
- 验证：目标测试 3 项通过，桌面 widget 专项 37 项通过，相邻回归 355 项通过，全量 unittest 519 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.26.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.27.0 桌面候选目标预填

- 时间：2026-06-01 12:24
- 工具：rg / Get-Content / update_plan / apply_patch
- 摘要：继续下一阶段，确认 `0.27.0` 聚焦桌面候选训练目标预填；当前缺口是 0.26.0 可选择候选，但用户仍需手写常见 `/命令` 或 `intent slot=value` 目标。已记录 `.codex/context-scan-v0270-desktop-inner-brain-candidate-target-prefill.json`、`.codex/v0270-desktop-inner-brain-candidate-target-prefill-plan.md` 和 `word/plans/2026-06-01-v31-desktop-inner-brain-candidate-target-prefill-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。

- 时间：2026-06-01 12:36
- 工具：apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- RED/GREEN：新增 3 个桌面候选目标预填测试和 1 个版本测试先失败，覆盖目标下拉框选项、教学命令预填、标注 intent 模板预填、填入不提交和版本提升；实现后目标测试 4 项通过。
- 实现：`AssistantPanel` 新增教学目标和标注目标下拉框；教学命令复用 `TEACHABLE_INNER_BRAIN_COMMAND_INTENTS`；标注目标提供常见 `intent slot=value` 模板；填充动作仍只写入输入框。
- 修复：版本升到 0.27.0 后，更新测试 manifest 从 `0.26.1` 调整为 `0.27.1`，保持“可更新”夹具高于当前版本。
- 摘要：完成桌面候选目标预填；版本提升到 `0.27.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.27.0.exe`。
- 验证：目标测试 4 项通过，桌面 widget 专项 39 项通过，相邻回归 355 项通过，全量 unittest 521 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.27.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.28.0 InnerBrain 样本包含签名置信度补偿

- 时间：2026-06-01 12:55
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String
- 摘要：继续下一阶段，确认 `0.28.0` 聚焦 InnerBrain 分类器评分增强，而不是继续堆自然语言正则。已记录 `.codex/context-scan-v0280-inner-brain-contained-signature-boost.json`、`.codex/v0280-inner-brain-contained-signature-boost-plan.md` 和 `word/plans/2026-06-01-v32-inner-brain-contained-signature-boost-plan.md`。
- RED/GREEN：新增 1 个 InnerBrain 样本包含签名测试和 1 个版本测试先失败；失败点为 `帮我看一下知识库状态` 只能进入 `CLARIFY`，版本仍为 `0.27.0`。实现后目标测试 2 项通过。
- 实现：`_sample_similarity()` 保留 Dice 相似度，并新增 `_contained_sample_signature_similarity()`；当 prompt 完整包含长度不少于 4 的样本签名时，按覆盖率给出受上限约束的高置信补偿。
- 说明：该实现复用已知样本签名，不新增意图正则、不自动训练、不自动猜测 unknown 候选。
- 修复：版本升到 0.28.0 后，更新测试 manifest 从 `0.27.1` 调整为 `0.28.1`，保持“可更新”夹具高于当前版本。
- 摘要：完成 InnerBrain 样本包含签名置信度补偿；版本提升到 `0.28.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.28.0.exe`。
- 验证：目标测试 2 项通过，InnerBrain 专项 25 项通过，相邻回归 395 项通过，全量 unittest 522 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.28.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.29.0 InnerBrain 固定评估集

- 时间：2026-06-01 13:12
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String
- 摘要：继续下一阶段，确认 `0.29.0` 聚焦建立 InnerBrain 可重复评估基线，为后续字符 n-gram、轻量 embedding 或小型分类器调整提供基准，而不是继续堆正则。已记录 `.codex/context-scan-v0290-inner-brain-seed-evaluation.json`、`.codex/v0290-inner-brain-seed-evaluation-plan.md` 和 `word/plans/2026-06-01-v33-inner-brain-seed-evaluation-plan.md`。
- RED/GREEN：新增 InnerBrain 评估 API 测试、Agent `/inner-brain-eval` 命令测试和版本一致性测试先失败；失败点为评估 API 不存在、命令未知、版本仍为 `0.28.0`。实现后目标测试 3 项通过。
- 实现：新增 `InnerBrainEvaluationCase`、`InnerBrainEvaluationCaseResult`、`InnerBrainEvaluationReport`、`seed_evaluation_cases()`、`evaluate_inner_brain()` 和 `describe_inner_brain_evaluation()`。
- 接入：Agent 新增 `/inner-brain-eval` 与 `brain-eval` 别名，作为路由观察命令处理，不写入 runtime 样本、不自动训练、不污染候选。
- 摘要：完成 InnerBrain 固定评估集；版本提升到 `0.29.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.29.0.exe`。
- 验证：目标测试 3 项通过，InnerBrain 专项 26 项通过，相邻回归 397 项通过，全量 unittest 524 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.29.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.30.0 InnerBrain 本机评估集扩展

- 时间：2026-06-01 13:27
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- 摘要：继续下一阶段，确认 `0.30.0` 聚焦让真实日志先进入本机评估集观察，而不是直接自动训练或继续堆自然语言正则。已记录 `.codex/context-scan-v0300-inner-brain-local-evaluation.json`、`.codex/v0300-inner-brain-local-evaluation-plan.md` 和 `word/plans/2026-06-01-v34-inner-brain-local-evaluation-plan.md`。
- RED/GREEN：新增本机评估 JSONL 加载测试、Agent `/inner-brain-eval` 合并本机评估样本测试和版本一致性测试先失败；失败点为 `load_evaluation_cases` 不存在、命令仍只显示 seed 评估、版本仍为 `0.29.0`。实现后目标测试 3 项通过。
- 实现：`InnerBrainEvaluationCase` 增加 `source` 字段；新增 `load_evaluation_cases()` 读取 `data/inner-brain/evaluation/*.jsonl`；`evaluate_inner_brain()` 默认合并 seed/local cases；`describe_inner_brain_evaluation()` 输出来源计数。
- 说明：本机评估 JSONL 只作为 `/inner-brain-eval` 观察输入，不写入 runtime 训练样本、不自动训练、不改变正常聊天路由。
- 摘要：完成 InnerBrain 本机评估集扩展；版本提升到 `0.30.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.30.0.exe`。
- 验证：目标测试 3 项通过，InnerBrain 专项 27 项通过，相邻回归 399 项通过，全量 unittest 526 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.30.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.31.0 InnerBrain 评估失败修复建议

- 时间：2026-06-01 14:14
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- 摘要：继续下一阶段，确认 `0.31.0` 聚焦把评估失败转成显式训练提示，而不是自动训练或继续堆自然语言正则。已记录 `.codex/context-scan-v0310-inner-brain-evaluation-fix-suggestion.json`、`.codex/v0310-inner-brain-evaluation-fix-suggestion-plan.md` 和 `word/plans/2026-06-01-v35-inner-brain-evaluation-fix-suggestion-plan.md`。
- RED/GREEN：新增 InnerBrain 失败评估建议测试、Agent `/inner-brain-eval` 失败建议测试和版本一致性测试先失败；失败点为评估描述缺少 `失败修复建议：`，版本仍为 `0.30.0`。实现后目标测试 3 项通过。
- 实现：`InnerBrainEvaluationReport` 增加 `failed_case_results`；`describe_inner_brain_evaluation()` 对失败样本追加显式训练建议；`expected_command` 使用 `/inner-brain-teach`，可执行 intent 使用 `/inner-brain-label`。
- 说明：失败建议只是文本提示，不写入 runtime 训练样本、不自动训练、不改变正常聊天路由。
- 摘要：完成 InnerBrain 评估失败修复建议；版本提升到 `0.31.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.31.0.exe`。
- 验证：目标测试 3 项通过，InnerBrain 专项 28 项通过，相邻回归 401 项通过，全量 unittest 528 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.31.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.32.0 InnerBrain 评估失败过滤视图

- 时间：2026-06-01 继续执行
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- 摘要：继续下一阶段，确认 `0.32.0` 聚焦只看 InnerBrain 评估失败样本，避免完整评估输出过长时掩盖失败项。已记录 `.codex/context-scan-v0320-inner-brain-evaluation-failures-only.json`、`.codex/v0320-inner-brain-evaluation-failures-only-plan.md` 和 `word/plans/2026-06-01-v36-inner-brain-evaluation-failures-only-plan.md`。
- RED/GREEN：新增 InnerBrain 失败过滤描述测试、Agent `/inner-brain-eval-failed` 命令测试和版本一致性测试先失败；失败点为 `describe_inner_brain_evaluation()` 尚无 `failures_only` 参数、命令未知、版本仍为 `0.31.0`。实现后目标测试 3 项通过。
- 实现：`describe_inner_brain_evaluation(report, failures_only=True)` 只格式化 `failed_case_results`，无失败时输出 `- 无`；Agent 新增 `/inner-brain-eval-failed`、`brain-eval-failed` 和 `inner-brain-eval-failures` 别名。
- 说明：失败过滤视图只改变评估展示，不写 runtime 训练样本、不自动训练、不污染最近路由候选。
- 摘要：完成 InnerBrain 评估失败过滤视图；版本提升到 `0.32.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.32.0.exe`。
- 验证：目标测试 3 项通过，InnerBrain 专项 29 项通过，相邻回归 403 项通过，全量 unittest 530 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.32.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.33.0 InnerBrain 本机评估过滤视图

- 时间：2026-06-01 继续执行
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- 摘要：继续下一阶段，确认 `0.33.0` 聚焦让本机 `data/inner-brain/evaluation/*.jsonl` 评估样本可独立查看，避免完整 seed+local 报告过长时影响真实日志样本排查。已记录 `word/plans/2026-06-01-v37-inner-brain-local-evaluation-view-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- RED/GREEN：新增 InnerBrain `source_filter` 评估测试、Agent `/inner-brain-eval-local`、Agent `/inner-brain-eval-local-failed` 和版本一致性测试先失败；失败点为 `evaluate_inner_brain()` 参数缺失、两个命令未知、版本仍为 `0.32.0`。实现后目标测试 4 项通过。
- 实现：`evaluate_inner_brain()` 增加 `source_filter` 参数；Agent 新增 `/inner-brain-eval-local`、`/inner-brain-eval-local-failed` 及别名；两个入口作为路由观察命令处理，不写 runtime 样本、不自动训练、不污染最近路由候选。
- 摘要：完成 InnerBrain 本机评估过滤视图；版本提升到 `0.33.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.33.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain 专项 30 项通过，相邻回归 406 项通过，全量 unittest 533 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.33.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-01 0.34.0 InnerBrain 本机评估样本写入

- 时间：2026-06-01 17:30
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- 摘要：继续下一阶段，确认 `0.34.0` 聚焦把真实日志中的自然语言样本显式保存到本机评估集，而不是直接写入训练集或继续堆正则。已记录 `.codex/context-scan-v0340-inner-brain-local-evaluation-save.json` 和 `word/plans/2026-06-01-v38-inner-brain-local-evaluation-save-plan.md`。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地检索、计划文件、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- RED/GREEN：新增 InnerBrain 本机评估写入测试、Agent `/inner-brain-eval-add`、Agent `/inner-brain-eval-label`、未知命令拒绝和版本一致性测试先失败；失败点为 API/命令缺失、版本仍为 `0.33.0`。实现后目标测试 5 项通过。
- 实现：新增 `save_local_evaluation_case()` 和 `InnerBrainEvaluationSaveResult`；Agent 新增 `/inner-brain-eval-add 文本 => /命令` 与 `/inner-brain-eval-label 文本 => intent [slot=value ...]`，写入 `data/inner-brain/evaluation/runtime.jsonl`。
- 约束：本阶段只写本机评估 JSONL，不写 `data/inner-brain/training/runtime.jsonl`，不刷新 InnerBrain 训练，不自动训练，不改变正常聊天路由。
- 摘要：完成 InnerBrain 本机评估样本显式写入；版本提升到 `0.34.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.34.0.exe`。
- 验证：目标测试 5 项通过，InnerBrain 专项 31 项通过，相邻回归 410 项通过，全量 unittest 537 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.34.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-02 0.35.0 InnerBrain 候选编号写入本机评估样本

- 时间：2026-06-02 10:07
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- 摘要：接续 `日志.txt` 中断的 0.35.0 任务；确认上次停在 RED 测试和 v39 方案文档阶段，根因是接口 `502 Bad Gateway` 中断，未进入实现和收尾。
- RED/GREEN：沿用已写好的 3 个 Agent 候选评估写入测试和 1 个版本测试，先验证 4 项失败；实现后目标测试 4 项通过。
- 实现：`JarvisAgent` 新增 `/inner-brain-eval-add-candidate 编号 => /命令` 与 `/inner-brain-eval-label-candidate 编号 => intent [slot=value ...]`，复用候选编号、命令白名单、label slot 解析和 `save_local_evaluation_case()`。
- 约束：新入口只写 `data/inner-brain/evaluation/runtime.jsonl`，不写 `data/inner-brain/training/runtime.jsonl`，不刷新 InnerBrain，不移除候选，不污染最近路由历史。
- 摘要：完成 InnerBrain 候选编号写入本机评估样本；版本提升到 `0.35.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.35.0.exe`。
- 验证：目标测试 4 项通过，相邻回归 413 项通过，全量 unittest 540 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.35.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-02 0.36.0 InnerBrain 本机评估 JSONL 文件过滤

- 时间：2026-06-02 11:24
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 链接检查 / 敏感信息扫描
- 摘要：按 `日志.txt` 与 v39 后续继续下一阶段，选择“按来源文件过滤本机 evaluation JSONL”作为 0.36.0 小闭环。
- 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；已降级使用本地检索、TDD、`update_plan`、`unittest`、PyInstaller 打包和本地 smoke 验证。
- RED/GREEN：新增 InnerBrain 文件过滤、Agent 指定文件评估、Agent 指定文件失败视图和版本一致性测试先失败；失败点为 `source_file_filter` API 缺失、两个命令未知、版本仍为 `0.35.0`。实现后目标测试 4 项通过。
- 实现：`InnerBrainEvaluationCase` 增加只读 `source_file`；`evaluate_inner_brain()` 增加 `source_file_filter`；Agent 新增 `/inner-brain-eval-local-file 文件名` 与 `/inner-brain-eval-local-file-failed 文件名`。
- 约束：新入口只读本机评估样本，不写 `data/inner-brain/training/runtime.jsonl`，不改变 evaluation JSONL payload 和去重键，不污染最近路由历史。
- 摘要：完成 InnerBrain 本机评估 JSONL 文件过滤；版本提升到 `0.36.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.36.0.exe`。
- 验证：目标测试 4 项通过，相邻回归 416 项通过，全量 unittest 543 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.36.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-02 0.37.0 InnerBrain 本机评估失败文件分组

- 时间：2026-06-02 10:50
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地 `rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v40 后续继续下一阶段，选择“InnerBrain 本机失败评估按 JSONL 来源文件分组”作为 0.37.0 小闭环，避免 `/inner-brain-eval-local-failed` 同时展示通过文件计数造成排查噪音。
- RED/GREEN：新增 InnerBrain 失败文件分组、Agent 本机失败文件分组和版本一致性测试先失败；失败点为失败视图缺少 `失败文件：`、仍混入通过文件计数、版本仍为 `0.36.0`。实现后目标测试 3 项通过。
- 实现：`InnerBrainEvaluationReport` 增加 `failed_source_file_counts`；`describe_inner_brain_evaluation(report, failures_only=True)` 在未指定单个文件时显示 `失败文件：`，只列出失败来源文件和失败条数。
- 约束：新逻辑只改变本机失败评估展示，不写 `data/inner-brain/training/runtime.jsonl`，不新增自然语言正则，不自动训练，不导出报告，不改变单文件过滤视图。
- 摘要：完成 InnerBrain 本机评估失败文件分组；版本提升到 `0.37.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.37.0.exe`。
- 验证：目标测试 3 项通过，相邻回归 418 项通过，全量 unittest 545 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.37.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-02 0.38.0 InnerBrain 本机评估失败报告导出

- 时间：2026-06-02 11:07
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地 `rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v41 后续继续下一阶段，选择“本机失败评估 Markdown 报告导出”作为 0.38.0 小闭环，便于后续按文件处理失败样本。
- RED/GREEN：新增 InnerBrain 报告导出、Agent 本机失败报告导出、Agent 指定文件报告导出和版本一致性测试先失败；失败点为导出 API 缺失、`/inner-brain-eval-local-report` 未知、版本仍为 `0.37.0`。实现后目标测试 4 项通过。
- 调试：InnerBrain + Agent 相邻回归首次失败 2 项，根因是版本提升到 `0.38.0` 后更新检测测试 fixture 仍为 `0.37.1`；按既有版本测试模式同步为 `0.38.1` 后复跑通过。
- 实现：新增 `InnerBrainEvaluationReportSaveResult` 和 `export_inner_brain_evaluation_report()`；Agent 新增 `/inner-brain-eval-local-report [文件名]`，可导出全部本机失败评估或指定 JSONL 文件失败项到 `word/inner-brain-evaluation-report.md`。
- 约束：新入口只读本机评估样本，只写 Markdown 报告，不写 `data/inner-brain/training/runtime.jsonl`，不新增自然语言正则，不自动训练，不改变正常聊天路由。
- 摘要：完成 InnerBrain 本机失败评估 Markdown 报告导出；版本提升到 `0.38.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.38.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 327 项通过，全量 unittest 548 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.38.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-02 0.39.0 InnerBrain 本机评估失败原因汇总

- 时间：2026-06-02 继续执行
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地 `rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v42 后续继续下一阶段，选择“本机失败评估原因汇总”作为 0.39.0 小闭环，避免报告只能逐条看失败原因。
- RED/GREEN：新增 InnerBrain 失败原因汇总、InnerBrain 报告导出包含原因汇总、Agent 本机失败报告包含原因汇总和版本一致性测试先失败；失败点为 `failed_reason_counts` 缺失、报告缺少 `失败原因汇总：`、版本仍为 `0.38.0`。实现后目标测试 4 项通过。
- 调试：InnerBrain + Agent 相邻回归首次失败 1 项，根因是版本提升到 `0.39.0` 后更新检测测试 fixture 已改为 `0.39.1`，断言仍停在 `0.38.1`；同步断言后复跑通过。
- 实现：`InnerBrainEvaluationReport` 增加 `failed_reason_counts`；`describe_inner_brain_evaluation(report, failures_only=True)` 在失败文件分组后输出失败原因、数量和典型样本；报告导出继续复用 failures-only 描述。
- 约束：新逻辑只读本机评估样本，只改变失败视图和 Markdown 报告展示，不写 `data/inner-brain/training/runtime.jsonl`，不新增自然语言正则，不自动训练，不改变 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机失败评估原因汇总；版本提升到 `0.39.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.39.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 328 项通过，全量 unittest 549 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.39.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-02 0.40.0 InnerBrain 本机评估失败类型汇总

- 时间：2026-06-02 继续执行
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地 `rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v43 后续继续下一阶段，选择“本机失败评估失败类型汇总”作为 0.40.0 小闭环，避免同类根因因具体 reason 文本不同而难以先按维度处理。
- 计划：新增 `InnerBrainEvaluationReport.failed_reason_category_counts`；failures-only 视图新增 `失败类型汇总：`；报告导出继续复用 failures-only 描述；不改命令接口、不写训练样本、不改变 evaluation JSONL。
- RED/GREEN：新增 InnerBrain 失败类型汇总、InnerBrain 报告导出包含类型汇总、Agent 本机失败报告包含类型汇总和版本一致性测试先失败；失败点为 `failed_reason_category_counts` 缺失、报告缺少 `失败类型汇总：`、版本仍为 `0.39.0`。实现后目标测试 4 项通过。
- 实现：`InnerBrainEvaluationReport` 增加 `failed_reason_category_counts`；`describe_inner_brain_evaluation(report, failures_only=True)` 在失败文件分组后输出失败类型、数量和典型样本；报告导出继续复用 failures-only 描述。
- 约束：新逻辑只读本机评估样本，只改变失败视图和 Markdown 报告展示，不写 `data/inner-brain/training/runtime.jsonl`，不新增自然语言正则，不自动训练，不改变 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机失败评估类型汇总；版本提升到 `0.40.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.40.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 329 项通过，全量 unittest 550 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.40.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-02 0.41.0 InnerBrain 本机评估失败期望意图汇总

- 时间：2026-06-02 继续执行
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地 `rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v44 后续继续下一阶段，选择“本机失败评估期望意图汇总”作为 0.41.0 小闭环，便于按高频 `expected_intent` 优先补样本、槽位或评分。
- 计划：新增 `InnerBrainEvaluationReport.failed_expected_intent_counts`；failures-only 视图新增 `失败期望意图汇总：`；报告导出继续复用 failures-only 描述；不改命令接口、不写训练样本、不改变 evaluation JSONL。
- RED/GREEN：新增 InnerBrain 失败期望意图汇总、InnerBrain 报告导出包含期望意图汇总、Agent 本机失败报告包含期望意图汇总和版本一致性测试先失败；失败点为 `failed_expected_intent_counts` 缺失、报告缺少 `失败期望意图汇总：`、版本仍为 `0.40.0`。实现后目标测试 4 项通过。
- 实现：`InnerBrainEvaluationReport` 增加 `failed_expected_intent_counts`；`describe_inner_brain_evaluation(report, failures_only=True)` 在失败类型汇总后输出 expected intent、数量和典型样本；报告导出继续复用 failures-only 描述。
- 约束：新逻辑只读本机评估样本，只改变失败视图和 Markdown 报告展示，不写 `data/inner-brain/training/runtime.jsonl`，不新增自然语言正则，不自动训练，不改变 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机失败评估期望意图汇总；版本提升到 `0.41.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.41.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 330 项通过，全量 unittest 551 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.41.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-02 0.42.0 InnerBrain 本机评估失败意图混淆汇总

- 时间：2026-06-02 14:05
- 工具：tool_search / rg / Get-Content / update_plan / apply_patch
- 工具降级：tool_search 未发现 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v45 后续继续下一阶段，选择“本机失败评估意图混淆汇总”作为 0.42.0 小闭环，帮助定位 `expected_intent -> actual intent` 高频混淆方向。
- 计划：新增 `InnerBrainEvaluationReport.failed_intent_confusion_counts`；failures-only 视图新增 `失败意图混淆汇总：`；报告导出继续复用 failures-only 描述；只统计 expected intent 与 actual intent 不一致的失败样本，不改命令接口、不写训练样本、不改变 evaluation JSONL。
- RED：首次目标命令误用旧测试类名导致测试加载错误；修正为 `InnerBrainTests` / `AgentTests` 后，目标 RED 为 1 项 ERROR、3 项 FAIL，失败点为 `failed_intent_confusion_counts` 缺失、报告缺少 `失败意图混淆汇总：`、版本仍为 `0.41.0`。
- GREEN：实现后目标测试 4 项通过。
- 实现：`InnerBrainEvaluationReport` 增加 `failed_intent_confusion_counts`；`describe_inner_brain_evaluation(report, failures_only=True)` 在失败期望意图汇总后输出 `失败意图混淆汇总：`，按 `expected -> actual` 统计数量和典型样本，并排除意图一致的策略/命令失败。
- 约束：新逻辑只读本机评估样本，只改变失败视图和 Markdown 报告展示，不写 `data/inner-brain/training/runtime.jsonl`，不新增自然语言正则，不自动训练，不改变 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机失败评估意图混淆汇总；版本提升到 `0.42.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.42.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 331 项通过，全量 unittest 552 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.42.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。

## 2026-06-02 0.43.0 InnerBrain 本机评估失败文件意图混淆汇总

- 时间：2026-06-02 14:54
- 工具：tool_search / rg / Get-Content / update_plan / apply_patch
- 工具降级：tool_search 未发现 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v46 后续继续下一阶段，选择“本机失败评估文件意图混淆交叉汇总”作为 0.43.0 小闭环，帮助定位 `source_file + expected -> actual` 高频混淆来源。
- 计划：新增 `InnerBrainEvaluationReport.failed_source_file_intent_confusion_counts`；failures-only 视图在未指定单个文件时新增 `失败文件意图混淆汇总：`；报告导出继续复用 failures-only 描述；只统计有来源文件且 expected intent 与 actual intent 不一致的失败样本，不改命令接口、不写训练样本、不改变 evaluation JSONL。
- RED/GREEN：新增 InnerBrain 失败文件意图混淆汇总、InnerBrain 报告导出包含文件混淆汇总、Agent 本机失败报告包含文件混淆汇总和版本一致性测试先失败；失败点为 `failed_source_file_intent_confusion_counts` 缺失、报告缺少 `失败文件意图混淆汇总：`、版本仍为 `0.42.0`。实现后目标测试 4 项通过。
- 实现：`InnerBrainEvaluationReport` 增加 `failed_source_file_intent_confusion_counts`；`describe_inner_brain_evaluation(report, failures_only=True)` 在失败意图混淆汇总后输出 `失败文件意图混淆汇总：`，按来源 JSONL 文件和 `expected -> actual` 混淆方向统计数量和典型样本，并排除无来源文件或意图一致的策略/命令失败。
- 约束：新逻辑只读本机评估样本，只改变失败视图和 Markdown 报告展示，不写 `data/inner-brain/training/runtime.jsonl`，不新增自然语言正则，不自动训练，不改变 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机失败评估文件意图混淆汇总；版本提升到 `0.43.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.43.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 332 项通过，全量 unittest 553 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.43.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：提交 `9524134 feat: 汇总本机评估文件意图混淆 0.43.0`，已 push 到 `origin/main`；`git rev-list --left-right --count HEAD...origin/main` 输出 `0 0`。

## 2026-06-02 0.44.0 InnerBrain 本机评估失败意图混淆修复建议分组

- 时间：2026-06-02 继续执行
- 工具：tool_search / rg / Get-Content / update_plan / apply_patch
- 工具降级：tool_search 未发现 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v47 后续继续下一阶段，选择“本机失败评估意图混淆修复建议分组”作为 0.44.0 小闭环，帮助按同一 `expected -> actual` 混淆方向集中处理显式 teach/label 建议。
- 计划：新增 `失败意图混淆修复建议：` 展示段落；只统计 expected intent 与 actual intent 不一致的失败样本；保留现有平铺 `失败修复建议：`；不改命令接口、不写训练样本、不改变 evaluation JSONL。
- RED/GREEN：新增 InnerBrain 意图混淆修复建议分组、InnerBrain 报告导出包含分组建议、Agent 本机失败报告包含分组建议和版本一致性测试先失败；失败点为失败视图和报告缺少 `失败意图混淆修复建议：`、版本仍为 `0.43.0`。实现后目标测试 4 项通过。
- 实现：`describe_inner_brain_evaluation(report, failures_only=True)` 在现有 `失败修复建议：` 前新增 `失败意图混淆修复建议：`，按 `expected_intent -> actual_intent` 聚合 `_inner_brain_evaluation_fix_suggestion()` 输出，并排除意图一致的策略或命令失败。
- 约束：新逻辑只读本机评估样本，只改变失败视图和 Markdown 报告展示，不写 `data/inner-brain/training/runtime.jsonl`，不新增自然语言正则，不自动训练，不改变 Agent 命令接口或 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机失败评估意图混淆修复建议分组；版本提升到 `0.44.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.44.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 333 项通过，全量 unittest 554 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.44.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `c3ba5c4 feat: 分组本机评估混淆修复建议 0.44.0` 已创建；多次 `git push origin main` 因 GitHub HTTPS 443 连接超时或 `schannel` TLS 握手失败未完成，`main` 当前相对 `origin/main` 为 ahead 1。

## 2026-06-02 0.45.0 InnerBrain 本机失败评估文件意图混淆修复建议分组

- 时间：2026-06-02 继续执行
- 工具：rg / Get-Content / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v48 后续继续下一阶段，选择“本机失败评估文件意图混淆修复建议分组”作为 0.45.0 小闭环，帮助按来源 JSONL 文件和同一 `expected -> actual` 混淆方向集中处理显式 teach/label 建议。
- RED/GREEN：新增 InnerBrain 文件意图混淆修复建议分组、InnerBrain 报告导出包含文件分组建议、Agent 本机失败报告包含文件分组建议和版本一致性测试先失败；失败点为失败视图和报告缺少 `失败文件意图混淆修复建议：`、版本仍为 `0.44.0`。补强单文件过滤负向断言后目标测试 5 项通过。
- 实现：`describe_inner_brain_evaluation(report, failures_only=True)` 在 `失败意图混淆修复建议：` 后新增 `失败文件意图混淆修复建议：`，按 `source_file + expected_intent -> actual_intent` 聚合 `_inner_brain_evaluation_fix_suggestion()` 输出，并排除无来源文件或意图一致的策略/命令失败。
- 约束：新逻辑只读本机评估样本，只改变失败视图和 Markdown 报告展示，不写 `data/inner-brain/training/runtime.jsonl`，不新增自然语言正则，不自动训练，不改变 Agent 命令接口或 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机失败评估文件意图混淆修复建议分组；版本提升到 `0.45.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.45.0.exe`。
- 验证：目标测试 5 项通过，InnerBrain + Agent 相邻回归 334 项通过，全量 unittest 555 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.45.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `ddf6511 feat: 分组本机评估文件混淆修复建议 0.45.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 2。

## 2026-06-02 0.46.0 InnerBrain 本机评估空样本引导

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v49 后续继续下一阶段，选择“本机 evaluation 空样本引导”作为 0.46.0 小闭环，让空的 `/inner-brain-eval-local` 与 `/inner-brain-eval-local-failed` 明确提示如何添加本机 evaluation 样本。
- 计划：当 `local_evaluation` 没有样本时，在评估描述中追加 `本机评估样本：- 无`、四个 evaluation 样本添加命令和“不自动训练”说明；不新增命令、不写 training runtime 样本、不改变 evaluation JSONL payload。
- RED/GREEN：新增 InnerBrain 空本机评估描述、Agent 本机失败空样本命令和版本一致性测试先失败；失败点为空状态缺少添加样本引导、版本仍为 `0.45.0`。实现后目标测试 3 项通过。
- 实现：`describe_inner_brain_evaluation()` 在 `report.total_count == 0` 且评估集名称为 `local_evaluation` 时追加本机样本空状态和 `/inner-brain-eval-add`、`/inner-brain-eval-label`、`/inner-brain-eval-add-candidate`、`/inner-brain-eval-label-candidate` 示例。
- 约束：新逻辑只改变空评估展示，不自动采纳、不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变 Agent 命令接口或 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机 evaluation 空样本引导；版本提升到 `0.46.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.46.0.exe`。
- 验证：目标测试 3 项通过，InnerBrain + Agent 相邻回归 336 项通过，全量 unittest 557 项通过，实际空本机评估命令输出添加样本引导，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.46.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `8c6f8c5 feat: 引导本机评估空样本添加 0.46.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 3。

## 2026-06-02 0.47.0 InnerBrain 本机评估样本保存后续验证提示

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v51 后续继续下一阶段，选择“本机 evaluation 样本保存后续验证提示”作为 0.47.0 小闭环，让保存样本后立即看到复跑、失败过滤、文件聚焦和报告导出入口。
- 计划：在 `_describe_inner_brain_evaluation_case_save()` 统一追加 `后续验证：` 段落；四条 evaluation 保存命令共享反馈；不新增命令、不自动运行评估、不写 training runtime 样本、不改变 evaluation JSONL payload、去重键或保存路径。
- RED/GREEN：新增 Agent 本机 evaluation 保存反馈后续验证提示和版本一致性测试先失败；失败点为保存反馈缺少 `后续验证：`、版本仍为 `0.46.0`。实现后目标测试 3 项通过。
- 实现：保存反馈末尾追加 `/inner-brain-eval-local`、`/inner-brain-eval-local-failed`、`/inner-brain-eval-local-file runtime.jsonl` 和 `/inner-brain-eval-local-report`，聚焦文件名来自保存结果路径。
- 约束：新逻辑只改变保存后的文本提示，不自动采纳、不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变 Agent 命令接口或 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机 evaluation 样本保存后续验证提示；版本提升到 `0.47.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.47.0.exe`。
- 验证：目标测试 3 项通过，InnerBrain + Agent 相邻回归 336 项通过，全量 unittest 557 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.47.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `9d7e6e0 feat: 提示本机评估样本保存后续验证 0.47.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 4。

## 2026-06-02 0.48.0 InnerBrain 本机失败报告导出后续处理提示

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v52 后续继续下一阶段，选择“本机失败报告导出后续处理提示”作为 0.48.0 小闭环，让导出报告后立即看到失败视图、文件聚焦和 evaluation 样本补充入口。
- 计划：在 `_export_inner_brain_local_evaluation_report()` 统一追加 `后续处理：` 段落；指定文件时使用当前文件名，未指定文件时使用 `文件名` 占位；不新增命令、不自动运行评估、不写 training runtime 样本、不改变导出的 Markdown 报告内容。
- RED/GREEN：新增 Agent 本机失败报告导出后续处理提示和版本一致性测试先失败；失败点为报告导出响应缺少 `后续处理：`、版本仍为 `0.47.0`。实现后目标测试 3 项通过。
- 实现：报告导出响应末尾追加 `/inner-brain-eval-local-failed`、`/inner-brain-eval-local-file-failed 文件名` 或当前文件命令、`/inner-brain-eval-add 文本 => /命令`、`/inner-brain-eval-label 文本 => intent [slot=value ...]`。
- 约束：新逻辑只改变导出后的文本提示，不自动采纳、不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变 Agent 命令接口、报告 Markdown 或 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机失败报告导出后续处理提示；版本提升到 `0.48.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.48.0.exe`。
- 验证：目标测试 3 项通过，InnerBrain + Agent 相邻回归 336 项通过，全量 unittest 557 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.48.0`，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `706185e feat: 提示本机失败报告后续处理 0.48.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 5。

## 2026-06-02 0.49.0 InnerBrain 本机失败视图导出报告提示

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v53 后续继续下一阶段，选择“本机失败视图导出报告提示”作为 0.49.0 小闭环，让用户在失败列表视图里直接看到报告导出入口。
- 计划：在 Agent 本机失败视图响应层追加 `后续处理：`；全部本机失败视图提示 `/inner-brain-eval-local-report` 和 `/inner-brain-eval-local-report 文件名`；指定文件失败视图提示当前文件报告导出和全部报告导出；空样本或无失败样本不追加提示。
- RED/GREEN：新增 Agent 本机失败视图导出报告提示、文件级失败视图导出报告提示、空样本负向断言和版本一致性测试先失败；失败点为失败视图缺少 `后续处理：`、版本仍为 `0.48.0`。实现后目标测试 4 项通过。
- 实现：新增 `_describe_inner_brain_local_failed_evaluation()` 统一包装本机失败视图；只在 `report.failed_case_results` 非空时追加导出报告提示；`/inner-brain-eval-local-file-failed 文件名` 使用 `report.source_file_filter` 输出当前文件命令。
- 约束：新逻辑只改变 Agent 文本提示，不新增命令、不自动运行报告导出、不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变导出的 Markdown 报告内容、evaluation JSONL payload、去重键或保存路径。
- 摘要：完成 InnerBrain 本机失败视图导出报告提示；版本提升到 `0.49.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.49.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 336 项通过，全量 unittest 557 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.49.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `bf62440 feat: 提示本机失败视图导出报告 0.49.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 6。

## 2026-06-02 0.50.0 InnerBrain 本机失败视图文件聚焦提示

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v54 后续继续下一阶段，选择“本机失败视图文件聚焦提示”作为 0.50.0 小闭环，让用户在失败列表和文件失败视图之间直接切换。
- 计划：在 0.49.0 的 `_describe_inner_brain_local_failed_evaluation()` 后续处理段落中补充文件聚焦提示；全部本机失败视图提示 `/inner-brain-eval-local-file-failed 文件名`；指定文件失败视图提示 `/inner-brain-eval-local-failed`；空样本或无失败样本不追加提示。
- RED/GREEN：新增 Agent 本机失败视图文件聚焦提示、文件失败视图查看全部提示、空样本负向断言和版本一致性测试先失败；失败点为失败视图缺少文件聚焦/查看全部失败样本提示、版本仍为 `0.49.0`。实现后目标测试 4 项通过。
- 实现：`_describe_inner_brain_local_failed_evaluation()` 在全部失败视图追加 `按文件聚焦失败`，在文件失败视图追加 `查看全部本机失败样本`，继续复用同一个 `后续处理：` 段落。
- 约束：新逻辑只改变 Agent 文本提示，不新增命令、不自动运行报告导出、不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变导出的 Markdown 报告内容、evaluation JSONL payload、去重键或保存路径。
- 摘要：完成 InnerBrain 本机失败视图文件聚焦提示；版本提升到 `0.50.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.50.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 336 项通过，全量 unittest 557 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.50.0`，安装包大小 `57,126,912` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `917ff19 feat: 提示本机失败视图文件聚焦 0.50.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 7。

## 2026-06-02 0.51.0 InnerBrain 本机 evaluation 已处理样本只读清单

- 时间：2026-06-02 继续执行
- 工具：tool_search / Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；`tool_search` 未发现可用替代工具，按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按当前文档“若真实样本继续堆积，再考虑把已处理建议状态做成单独只读清单”的方向，选择“本机 evaluation 已处理样本只读清单”作为 0.51.0 小闭环。
- 计划：新增 `/inner-brain-eval-local-resolved [文件名]` 只读列出当前已通过的本机 evaluation 样本；支持按 JSONL 文件过滤；无已处理样本时显示 `- 无`；不自动训练、不写 training runtime、不改变 evaluation JSONL payload。
- RED/GREEN：新增 InnerBrain 已处理样本只读描述、Agent 本机已处理样本清单、文件过滤、空清单和版本一致性测试先失败；失败点为描述函数未导出、命令未知、版本仍为 `0.50.0`。实现后目标测试 6 项通过。
- 实现：`InnerBrainEvaluationReport` 新增 `passed_case_results`；新增 `describe_inner_brain_resolved_evaluation()` 只展示当前通过样本；Agent 接入 `/inner-brain-eval-local-resolved [文件名]` 并追加查看待处理失败样本的后续入口。
- 约束：新逻辑只读执行本机 evaluation 评估，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变本机 evaluation JSONL payload、保存路径、报告导出内容或 LLM/Search 路由。
- 摘要：完成 InnerBrain 本机 evaluation 已处理样本只读清单；版本提升到 `0.51.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.51.0.exe`。
- 验证：目标测试 6 项通过，InnerBrain + Agent 相邻回归 341 项通过，全量 unittest 562 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.51.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `1c86e7f feat: 增加本机评估已处理样本清单 0.51.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 8。

## 2026-06-02 0.52.0 InnerBrain 本机评估全量视图后续处理提示

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 v55 后续继续增强本机 evaluation 治理入口，选择“本机评估全量视图后续处理提示”作为 0.52.0 小闭环。
- 计划：在 `/inner-brain-eval-local` 和 `/inner-brain-eval-local-file 文件名` 有样本时追加 `后续处理：`，提示切换失败视图、已处理清单和文件聚焦入口；空样本不追加，保留添加样本引导。
- RED/GREEN：新增 Agent 本机全量评估后续处理提示、文件全量评估后续处理提示、空本机样本负向断言和版本一致性测试先失败；失败点为本机全量评估/文件全量评估缺少 `后续处理：`，版本仍为 `0.51.0`。实现后目标测试 4 项通过。
- 实现：新增 `_describe_inner_brain_local_evaluation()` 包装本机全量评估描述；全部本机样本视图提示 `/inner-brain-eval-local-failed`、`/inner-brain-eval-local-resolved` 和 `/inner-brain-eval-local-file 文件名`；文件视图提示当前文件失败视图、当前文件已处理清单和返回全部本机评估。
- 约束：新逻辑只改变 Agent 文本提示，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变 `describe_inner_brain_evaluation()` 主体、本机 evaluation JSONL payload 或报告导出内容。
- 摘要：完成 InnerBrain 本机评估全量视图后续处理提示；版本提升到 `0.52.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.52.0.exe`。
- 验证：目标测试 4 项通过，InnerBrain + Agent 相邻回归 341 项通过，全量 unittest 562 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.52.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `a64d2b3 feat: 提示本机评估全量视图后续处理 0.52.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 9。

## 2026-06-02 0.53.0 InnerBrain 本机评估全量视图文件名候选提示

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.52.0 后续“文件名候选或状态摘要”方向，选择“本机评估全量视图文件名候选提示”作为 0.53.0 小闭环。
- 计划：在 `/inner-brain-eval-local` 的后续处理段落中复用 `report.source_file_counts` 列出真实本机 evaluation JSONL 文件名、样本数量和可复制的 `/inner-brain-eval-local-file 文件名` 命令；不改文件过滤视图、失败视图、已处理视图或报告导出。
- RED/GREEN：新增 Agent 本机全量评估文件名候选提示和版本一致性测试先失败；失败点为全量视图缺少 `可聚焦文件：` 与具体 `/inner-brain-eval-local-file 文件名` 命令，版本仍为 `0.52.0`。实现后目标测试 3 项通过。
- 实现：`_describe_inner_brain_local_evaluation()` 在全部本机样本视图后续处理段落中读取 `report.source_file_counts`，逐个输出来源 JSONL 文件、样本数量和可复制文件聚焦命令。
- 约束：新逻辑只改变 Agent 文本提示，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变文件过滤视图、失败视图、已处理视图、报告导出或本机 evaluation JSONL payload。
- 摘要：完成 InnerBrain 本机评估全量视图文件名候选提示；版本提升到 `0.53.0`；生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.53.0.exe`。
- 验证：目标测试 3 项通过，InnerBrain + Agent 相邻回归 341 项通过，全量 unittest 562 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.53.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `662453a feat: 提示本机评估文件候选 0.53.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 10。

## 2026-06-02 0.54.0 InnerBrain 本机评估全量视图文件候选状态摘要

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.53.0 后续“状态摘要”方向，选择“本机评估全量视图文件候选状态摘要”作为 0.54.0 小闭环。
- 计划：在 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选行中追加每个来源 JSONL 文件的通过/失败数量；不改文件过滤视图、失败视图、已处理视图或报告导出。
- RED/GREEN：新增 Agent 本机全量评估文件候选状态摘要和版本一致性测试先失败；失败点为候选行缺少 `通过 N 条，失败 N 条`，版本仍为 `0.53.0`。实现后目标测试 3 项通过。
- 实现：`_describe_inner_brain_local_evaluation()` 复用 `report.source_file_counts` 保持候选文件顺序，并从 `report.case_results` 按 `source_file` 统计通过/失败数量，候选行输出总数、通过数、失败数和可复制文件聚焦命令。
- 约束：新逻辑只改变 Agent 响应文本，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变文件过滤视图、失败视图、已处理视图、报告导出或本机 evaluation JSONL payload。
- 验证：目标测试 3 项通过，InnerBrain + Agent 相邻回归 341 项通过，全量 unittest 562 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.54.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `67204c3 feat: 汇总本机评估文件候选状态 0.54.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 11。

## 2026-06-02 0.55.0 InnerBrain 本机评估全量视图文件候选失败优先排序

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.54.0 后续“文件级排序提示”方向，选择“本机评估全量视图文件候选失败优先排序”作为 0.55.0 小闭环。
- 计划：在 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选列表中按失败数量降序、总样本数降序、文件名升序排列；不改候选行格式、文件过滤视图、失败视图、已处理视图或报告导出。
- RED/GREEN：新增 Agent 本机全量评估文件候选失败优先排序和版本一致性测试先失败；失败点为失败文件仍排在按文件名更早的纯通过文件之后，版本仍为 `0.54.0`。实现后目标测试 3 项通过。
- 实现：`_describe_inner_brain_local_evaluation()` 在输出候选行前对 `source_file_counts` 排序，排序键为失败数量降序、总样本数降序、文件名升序；候选行格式保持不变。
- 约束：新逻辑只改变 Agent 响应文本顺序，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变文件过滤视图、失败视图、已处理视图、报告导出或本机 evaluation JSONL payload。
- 验证：目标测试 3 项通过，InnerBrain + Agent 相邻回归 341 项通过，全量 unittest 562 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.55.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `706ba26 feat: 优先展示本机评估失败文件 0.55.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 12。

## 2026-06-02 0.56.0 InnerBrain 本机失败视图失败文件汇总排序

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.55.0 后续“失败视图文件级排序”方向，选择“本机失败视图失败文件汇总排序”作为 0.56.0 小闭环。
- 计划：在 `describe_inner_brain_evaluation(report, failures_only=True)` 的 `失败文件：` 分组中按失败数量降序、文件名升序排序；不改评估对象、失败样例、修复建议、JSONL payload 或训练路径。
- RED/GREEN：新增 InnerBrain 本机失败文件汇总排序、Agent 本机失败文件汇总排序和版本一致性测试先失败；失败点为失败数更多但文件名更靠后的 JSONL 仍排在后面，版本仍为 `0.55.0`。实现后目标测试 3 项通过。
- 实现：`describe_inner_brain_evaluation()` 在输出 `failed_source_file_counts` 前排序，排序键为失败数量降序、文件名升序。
- 约束：新逻辑只改变失败文件分组展示顺序，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变本机 evaluation JSONL payload、失败样例、失败原因或修复建议。
- 验证：目标测试 3 项通过，InnerBrain + Agent 相邻回归 343 项通过，全量 unittest 564 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.56.0`，安装包大小 `57,135,104` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `76ed3c0 feat: 优先展示本机失败评估文件 0.56.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 13。

## 2026-06-02 0.57.0 InnerBrain 本机文件失败视图已处理入口

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.56.0 后续“文件聚焦视图更具体入口”方向，选择“本机文件失败视图已处理入口”作为 0.57.0 小闭环。
- 计划：在 `/inner-brain-eval-local-file-failed 文件名` 的 `后续处理：` 中追加 `/inner-brain-eval-local-resolved 当前文件名`；不改未指定文件失败视图、评估对象、失败样例、汇总分组、报告导出、JSONL payload 或训练路径。
- RED/GREEN：新增 Agent 当前文件失败视图已处理入口和版本一致性测试先失败；失败点为当前文件失败视图缺少 `/inner-brain-eval-local-resolved failed-log.jsonl`，版本仍为 `0.56.0`。实现后目标测试 2 项通过。
- 实现：`_describe_inner_brain_local_failed_evaluation()` 在 `source_file_filter` 分支追加当前文件已处理样本入口。
- 约束：新逻辑只改变 Agent 响应文本，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变本机 evaluation JSONL payload、失败样例、失败原因、汇总分组或报告导出。
- 验证：目标测试 2 项通过，Agent + ProjectMetadata 相邻回归 302 项通过，全量 unittest 564 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.57.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `35dd342 feat: 提示本机文件已处理样本 0.57.0` 已创建；远端未推送，`main` 当前相对 `origin/main` 为 ahead 14。

## 2026-06-02 0.58.0 InnerBrain 本机已处理视图文件候选提示

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.57.0 后续“文件聚焦视图更具体入口”方向，选择“本机已处理视图文件候选提示”作为 0.58.0 小闭环。
- 计划：在 `/inner-brain-eval-local-resolved` 未指定文件时，从通过样本的 `source_file` 统计可查看文件候选；候选按通过数量降序、文件名升序排序，纯失败文件不显示。
- RED/GREEN：新增 Agent 全量已处理视图文件候选和版本一致性测试先失败；失败点为全量已处理视图缺少 `可查看文件：`，版本仍为 `0.57.0`。实现后目标测试 2 项通过。
- 实现：`_inner_brain_local_resolved_evaluation()` 在全量已处理视图后续处理段落中统计通过样本来源文件并输出 `/inner-brain-eval-local-resolved 文件名`。
- 约束：新逻辑只改变 Agent 响应文本，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变指定文件已处理视图、本机 evaluation JSONL payload、失败样例或报告导出。
- 验证：目标测试 2 项通过，Agent + ProjectMetadata 相邻回归 302 项通过，全量 unittest 564 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.58.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `d3b6c64 feat: 提示本机已处理文件候选 0.58.0` 已创建；远端未推送。

## 2026-06-02 0.59.0 InnerBrain 本机已处理视图文件候选状态摘要

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.58.0 后续“已处理视图更多文件级优先级提示”方向，选择“本机已处理视图文件候选状态摘要”作为 0.59.0 小闭环。
- 计划：在 `/inner-brain-eval-local-resolved` 未指定文件时，候选行同时展示已处理数量和同文件待处理失败数量；候选仍只列有通过样本的文件，排序仍按通过数量降序、文件名升序。
- RED/GREEN：新增 Agent 全量已处理视图文件候选状态摘要和版本一致性测试先失败；失败点为候选行缺少 `已处理 1 条，待处理失败 1 条`，版本仍为 `0.58.0`。实现后目标测试 2 项通过。
- 实现：`_inner_brain_local_resolved_evaluation()` 在全量已处理视图中同时统计通过和失败样本来源文件，候选行输出已处理数量、待处理失败数量和 `/inner-brain-eval-local-resolved 文件名`。
- 约束：新逻辑只改变 Agent 响应文本，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变指定文件已处理视图、本机 evaluation JSONL payload、失败样例或报告导出。
- 验证：目标测试 2 项通过，Agent + ProjectMetadata 相邻回归 302 项通过，全量 unittest 564 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.59.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `a0b552a feat: 汇总本机已处理文件状态 0.59.0` 已创建；远端未推送。

## 2026-06-02 0.60.0 InnerBrain 本机已处理视图文件候选待处理优先排序

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.59.0 后续“已处理视图更多文件级优先级提示”方向，选择“本机已处理视图文件候选待处理优先排序”作为 0.60.0 小闭环。
- 计划：在 `/inner-brain-eval-local-resolved` 未指定文件时，候选排序改为待处理失败数量降序、已处理数量降序、文件名升序；候选仍只列有通过样本的文件。
- RED/GREEN：新增 Agent 全量已处理视图文件候选待处理优先排序和版本一致性测试先失败；失败点为纯已处理但通过数更多的 `clean-log.jsonl` 排在仍有失败的 `real-log.jsonl` 前，版本仍为 `0.59.0`。实现后目标测试 2 项通过。
- 实现：`_inner_brain_local_resolved_evaluation()` 的候选排序键调整为待处理失败数量降序、已处理数量降序、文件名升序。
- 约束：新逻辑只改变 Agent 响应文本顺序，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变指定文件已处理视图、本机 evaluation JSONL payload、失败样例或报告导出。
- 验证：目标测试 2 项通过，Agent + ProjectMetadata 相邻回归 302 项通过，全量 unittest 564 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.60.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `236b1ef feat: 优先展示本机已处理待处理文件 0.60.0` 已创建；远端未推送。

## 2026-06-02 0.61.0 InnerBrain 本机已处理视图文件候选待处理入口

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.60.0 后续“失败、已处理和文件聚焦视图更多文件级优先级提示”方向，选择“本机已处理视图文件候选待处理入口”作为 0.61.0 小闭环。
- 计划：在 `/inner-brain-eval-local-resolved` 未指定文件时，`可查看文件：` 候选行若同文件待处理失败数量大于 0，则追加 `/inner-brain-eval-local-file-failed 当前文件名`；纯已处理候选不追加失败入口。
- RED/GREEN：新增 Agent 全量已处理视图文件候选待处理入口和版本一致性测试先失败；失败点为候选行缺少 `待处理：/inner-brain-eval-local-file-failed real-log.jsonl`，版本仍为 `0.60.0`。实现后目标测试 2 项通过。
- 实现：`_inner_brain_local_resolved_evaluation()` 在构造 `可查看文件：` 候选行时，若同文件失败数量大于 0，则追加同文件失败聚焦命令；失败数量为 0 的候选保持原行格式。
- 约束：新逻辑只改变 Agent 响应文本，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变排序、指定文件已处理视图、本机 evaluation JSONL payload、失败样例或报告导出。
- 验证：目标测试 2 项通过，Agent + ProjectMetadata 相邻回归 302 项通过，全量 unittest 564 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.61.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `43d9454 feat: 提示本机已处理待处理入口 0.61.0` 已创建；远端未推送。

## 2026-06-02 0.62.0 InnerBrain 本机评估全量视图文件候选待处理入口

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.61.0 的行内待处理入口模式，选择“本机评估全量视图文件候选待处理入口”作为 0.62.0 小闭环。
- 计划：在 `/inner-brain-eval-local` 未指定文件时，`可聚焦文件：` 候选行若同文件失败数量大于 0，则追加 `/inner-brain-eval-local-file-failed 当前文件名`；纯通过候选不追加失败入口。
- RED/GREEN：新增 Agent 本机评估全量视图文件候选待处理入口和版本一致性测试先失败；失败点为候选行缺少 `待处理：/inner-brain-eval-local-file-failed zzz-failed-log.jsonl`，版本仍为 `0.61.0`。实现后目标测试 2 项通过。
- 实现：`_describe_inner_brain_local_evaluation()` 在构造 `可聚焦文件：` 候选行时，若同文件失败数量大于 0，则追加同文件失败聚焦命令；失败数量为 0 的候选保持原行格式。
- 约束：新逻辑只改变 Agent 响应文本，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变排序、指定文件本机评估视图、本机 evaluation JSONL payload、失败样例或报告导出。
- 验证：目标测试 2 项通过，Agent + ProjectMetadata 相邻回归 302 项通过，全量 unittest 564 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.62.0`，安装包大小 `57,131,008` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- Git：本地提交 `0ce0f12 feat: 提示本机评估待处理入口 0.62.0` 已创建；远端未推送。

## 2026-06-02 0.63.0 InnerBrain 本机失败视图失败文件分组聚焦入口

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.62.0 的行内文件聚焦入口模式，选择“本机失败视图失败文件分组聚焦入口”作为 0.63.0 小闭环。
- 计划：在 `/inner-brain-eval-local-failed` 未指定文件时，`失败文件：` 分组行追加 `/inner-brain-eval-local-file-failed 当前文件名`；指定文件失败视图继续不显示跨文件分组。
- 约束：新逻辑只改变失败文件分组文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变排序、失败样例、本机 evaluation JSONL payload、修复建议或报告导出路径。
- RED/GREEN：新增 InnerBrain 格式化、Agent 命令输出、失败文件排序完整行和版本一致性测试先失败；修正首次 RED 命令中的旧测试方法名后，目标 5 项按预期 FAIL。实现后同一目标命令 5 项通过。
- 实现：`describe_inner_brain_evaluation()` 在 failures_only 且未指定 `source_file_filter` 时，为每个失败文件分组行追加 `/inner-brain-eval-local-file-failed 当前文件名`；项目版本提升到 `0.63.0`，更新更新清单测试夹具到 `0.63.1`。
- 验证：InnerBrain + Agent + ProjectMetadata 相邻回归 347 项通过，全量 unittest 564 项通过，源码桌面 smoke 通过，打包后 exe smoke 通过，安装脚本文案为 `0.63.0`，安装包大小 `57,135,104` 字节，静态检查、Markdown 链接检查、敏感扫描和本地配置文件检查通过。
- 路径更正：安装脚本检查首次使用旧 `installer-work` 路径失败；查构建脚本和 dist 目录后确认当前 stage 为 `..\jarvis-lite-dist\windows-installer-stage\install.cmd`，SED 为 `..\jarvis-lite-dist\JarvisLiteSetup.sed`，按实际路径复核通过。
- Git：本地提交 `1accbf6 feat: 提示本机失败文件聚焦入口 0.63.0` 已创建；远端未推送。

## 2026-06-02 0.64.0 InnerBrain 本机失败视图失败文件分组报告入口

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.63.0 的失败文件分组行内入口模式，选择“本机失败视图失败文件分组报告入口”作为 0.64.0 小闭环。
- 计划：在 `/inner-brain-eval-local-failed` 未指定文件时，`失败文件：` 分组行继续保留同文件失败聚焦入口，并追加 `/inner-brain-eval-local-report 当前文件名`；指定文件失败视图继续不显示跨文件分组。
- 约束：新逻辑只改变失败文件分组文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变排序、失败样例、本机 evaluation JSONL payload、修复建议或报告导出路径。
- RED/GREEN：新增 InnerBrain 格式化、Agent 命令输出、失败文件排序完整行和版本一致性测试先失败；失败点为失败文件行缺少 `报告：/inner-brain-eval-local-report failed-log.jsonl`，版本仍为 `0.63.0`。实现后同一目标命令 5 项通过。
- 实现：`describe_inner_brain_evaluation()` 在 failures_only 且未指定 `source_file_filter` 时，为每个失败文件分组行保留 `/inner-brain-eval-local-file-failed 当前文件名` 并追加 `/inner-brain-eval-local-report 当前文件名`；项目版本提升到 `0.64.0`，更新更新清单测试夹具到 `0.64.1`。
- 验证：InnerBrain + Agent + ProjectMetadata 相邻回归 347 项通过，全量 unittest 564 项通过，源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后窗口版 exe smoke 退出码 0，安装脚本文案为 `0.64.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 368 checked across 155 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `09221d4 feat: 提示本机失败文件报告入口 0.64.0` 已创建；远端按用户要求暂不推送。

## 2026-06-02 0.65.0 InnerBrain 本机评估全量视图文件候选报告入口

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.62.0 的全量视图文件候选待处理入口和 0.64.0 的失败文件报告入口模式，选择“本机评估全量视图文件候选报告入口”作为 0.65.0 小闭环。
- 计划：在 `/inner-brain-eval-local` 未指定文件时，`可聚焦文件：` 候选行若同文件失败数量大于 0，则保留同文件失败入口并追加 `/inner-brain-eval-local-report 当前文件名`；纯通过文件不追加报告入口。
- 约束：新逻辑只改变全量本机评估候选行文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变排序、指定文件视图、失败视图分组、本机 evaluation JSONL payload、修复建议或报告导出路径。
- RED/GREEN：新增 Agent 本机全量评估文件候选报告入口和版本一致性测试先失败；失败点为候选行缺少 `报告：/inner-brain-eval-local-report zzz-failed-log.jsonl`，版本仍为 `0.64.0`。实现后同一目标命令 2 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_evaluation()` 在同文件失败数量大于 0 时，为候选行保留 `/inner-brain-eval-local-file-failed 当前文件名` 并追加 `/inner-brain-eval-local-report 当前文件名`；项目版本提升到 `0.65.0`，更新更新清单测试夹具到 `0.65.1`。
- 验证：Agent + ProjectMetadata 相邻回归 302 项通过，全量 unittest 564 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.65.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 369 checked across 156 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `71ac6af feat: 提示本机评估文件报告入口 0.65.0` 已创建；远端按用户要求暂不推送。

## 2026-06-02 0.66.0 InnerBrain 本机已处理视图文件候选报告入口

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.65.0 的全量评估文件候选报告入口模式，选择“本机已处理视图文件候选报告入口”作为 0.66.0 小闭环。
- 计划：在 `/inner-brain-eval-local-resolved` 未指定文件时，`可查看文件：` 候选行若同文件待处理失败数量大于 0，则保留同文件失败入口并追加 `/inner-brain-eval-local-report 当前文件名`；纯通过文件不追加报告入口。
- 约束：新逻辑只改变本机已处理视图候选行文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变排序、指定文件视图、本机全量评估视图、失败视图分组、本机 evaluation JSONL payload、修复建议或报告导出路径。
- RED/GREEN：新增 Agent 本机已处理视图文件候选报告入口和版本一致性测试先失败；失败点为候选行缺少 `报告：/inner-brain-eval-local-report real-log.jsonl`，版本仍为 `0.65.0`。实现后同一目标命令 2 项通过。
- 实现：`JarvisAgent._inner_brain_local_resolved_evaluation()` 在同文件待处理失败数量大于 0 时，为候选行保留 `/inner-brain-eval-local-file-failed 当前文件名` 并追加 `/inner-brain-eval-local-report 当前文件名`；项目版本提升到 `0.66.0`，更新更新清单测试夹具到 `0.66.1`。
- 验证：Agent + ProjectMetadata 相邻回归 302 项通过，全量 unittest 564 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.66.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 374 checked across 157 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `a1c9085 feat: 提示本机已处理文件报告入口 0.66.0` 已创建；远端按用户要求暂不推送。

## 2026-06-02 0.67.0 InnerBrain 本机文件视图报告入口

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.65.0 全量文件候选报告入口、0.66.0 已处理文件候选报告入口和既有指定文件失败视图报告入口模式，选择“本机文件视图报告入口”作为 0.67.0 小闭环。
- 计划：在 `/inner-brain-eval-local-file 文件名` 指定文件总览中，若当前文件仍有失败样本，则在后续处理追加 `/inner-brain-eval-local-report 当前文件名`；纯通过文件不追加报告入口。
- 约束：新逻辑只改变指定文件总览后续处理文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变排序、失败视图、已处理视图、本机 evaluation JSONL payload、修复建议或报告导出路径。
- RED/GREEN：新增 Agent 指定文件总览报告入口、纯通过文件负向断言和版本一致性测试先失败；失败点为当前文件总览缺少 `导出当前文件失败报告：/inner-brain-eval-local-report failed-log.jsonl`，版本仍为 `0.66.0`。实现后同一目标命令 3 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_evaluation()` 在指定 `source_file_filter` 且当前报告存在失败样本时，为后续处理追加 `/inner-brain-eval-local-report 当前文件名`；项目版本提升到 `0.67.0`，更新更新清单测试夹具到 `0.67.1`。
- 验证：Agent + ProjectMetadata 相邻回归 303 项通过，全量 unittest 565 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.67.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 376 checked across 158 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `36f7037 feat: 提示本机文件视图报告入口 0.67.0` 已创建；远端按用户要求暂不推送。

## 2026-06-02 0.68.0 InnerBrain 本机已处理指定文件视图报告入口

- 时间：2026-06-02 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.66.0 全量已处理文件候选报告入口和 0.67.0 指定文件总览报告入口模式，选择“本机已处理指定文件视图报告入口”作为 0.68.0 小闭环。
- 计划：在 `/inner-brain-eval-local-resolved 文件名` 指定文件已处理视图中，若同文件仍有待处理失败样本，则在后续处理追加 `/inner-brain-eval-local-report 当前文件名`；纯通过文件不追加报告入口。
- 约束：新逻辑只改变指定文件已处理视图后续处理文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变全量候选排序、指定文件总览、失败视图、本机 evaluation JSONL payload、修复建议或报告导出路径。
- RED/GREEN：新增 Agent 指定文件已处理视图报告入口、纯通过文件负向断言和版本一致性测试先失败；失败点为指定文件已处理视图缺少 `导出当前文件失败报告：/inner-brain-eval-local-report real-log.jsonl`，版本仍为 `0.67.0`。实现后同一目标命令 3 项通过。
- 实现：`JarvisAgent._inner_brain_local_resolved_evaluation()` 在指定 `source_file_filter` 且同文件仍有失败样本时，为后续处理追加 `/inner-brain-eval-local-report 当前文件名`；项目版本提升到 `0.68.0`，更新更新清单测试夹具到 `0.68.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.68.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 378 checked across 159 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `53c3e26 feat: 提示本机已处理指定文件报告入口 0.68.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.69.0 InnerBrain 本机 evaluation 保存反馈按文件报告入口

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.65.0-0.68.0 的按文件报告入口模式，选择“本机 evaluation 保存反馈按文件报告入口”作为 0.69.0 小闭环。
- 计划：在四条本机 evaluation 保存入口的统一反馈中，把报告入口明确为 `/inner-brain-eval-local-report runtime.jsonl`，与现有 `/inner-brain-eval-local-file runtime.jsonl` 聚焦入口保持同文件治理。
- RED：新增四条保存入口的按文件报告断言和版本一致性测试先失败；失败点为保存反馈仍输出全局 `/inner-brain-eval-local-report`，项目版本仍为 `0.68.0`。
- GREEN：同一目标命令 5 项通过。
- 实现：`JarvisAgent._describe_inner_brain_evaluation_case_save()` 复用已保存样本文件名，把反馈中的报告入口改为 `/inner-brain-eval-local-report runtime.jsonl`；项目版本提升到 `0.69.0`，更新更新清单测试夹具到 `0.69.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.69.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 394 checked across 334 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `6c698b4 feat: 提示本机评估保存文件报告入口 0.69.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.70.0 InnerBrain 本机失败报告导出反馈当前文件已处理入口

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.57.0 文件失败视图已处理入口和 0.68.0 已处理指定文件报告入口模式，选择“本机失败报告导出反馈当前文件已处理入口”作为 0.70.0 小闭环。
- 计划：在 `/inner-brain-eval-local-report 文件名` 导出指定文件失败报告后，后续处理除复查当前文件失败样本外，追加 `/inner-brain-eval-local-resolved 当前文件名`，便于对照同文件已处理样本。
- 约束：新逻辑只改变报告导出后的反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变 Markdown 报告正文、失败过滤、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：新增文件级报告导出反馈已处理入口断言和版本一致性测试先失败；失败点为反馈缺少 `/inner-brain-eval-local-resolved failed-log.jsonl`，项目版本仍为 `0.69.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._export_inner_brain_local_evaluation_report()` 在指定 `source_file_filter` 的报告导出反馈中追加 `/inner-brain-eval-local-resolved 当前文件名`；项目版本提升到 `0.70.0`，更新更新清单测试夹具到 `0.70.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.70.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 398 checked across 335 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `a41cc38 feat: 提示本机报告导出已处理入口 0.70.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.71.0 InnerBrain 本机失败报告导出反馈当前文件总览入口

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / build_windows_installer / PyInstaller / Markdown 链接检查
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.70.0 的指定文件报告导出已处理入口模式，选择“本机失败报告导出反馈当前文件总览入口”作为 0.71.0 小闭环。
- 计划：在 `/inner-brain-eval-local-report 文件名` 导出指定文件失败报告后，后续处理除复查当前文件失败样本和查看当前文件已处理样本外，追加 `/inner-brain-eval-local-file 当前文件名`，便于回到同文件通过/失败总览。
- 约束：新逻辑只改变报告导出后的反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变 Markdown 报告正文、失败过滤、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：新增文件级报告导出反馈当前文件总览入口断言和版本一致性测试先失败；失败点为反馈缺少 `/inner-brain-eval-local-file failed-log.jsonl`，项目版本仍为 `0.70.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._export_inner_brain_local_evaluation_report()` 在指定 `source_file_filter` 的报告导出反馈中追加 `/inner-brain-eval-local-file 当前文件名`；项目版本提升到 `0.71.0`，更新更新清单测试夹具到 `0.71.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.71.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 401 checked across 336 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `8d6cf6a feat: 提示本机报告导出文件总览入口 0.71.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.72.0 InnerBrain 本机文件失败视图当前文件总览入口

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / build_windows_installer / PyInstaller / Markdown 链接检查
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.57.0 指定文件失败视图已处理入口和 0.71.0 指定文件报告导出反馈当前文件总览入口模式，选择“本机文件失败视图当前文件总览入口”作为 0.72.0 小闭环。
- 计划：在 `/inner-brain-eval-local-file-failed 文件名` 聚焦指定文件失败样本后，后续处理除当前文件已处理样本、全部失败样本和当前文件报告外，追加 `/inner-brain-eval-local-file 当前文件名`，便于回到同文件通过/失败总览。
- 约束：新逻辑只改变指定文件失败视图反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变评估主体、失败修复建议、报告正文、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：新增指定文件失败视图当前文件总览入口断言和版本一致性测试先失败；失败点为反馈缺少 `/inner-brain-eval-local-file failed-log.jsonl`，项目版本仍为 `0.71.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_failed_evaluation()` 在指定 `source_file_filter` 的失败视图反馈中追加 `/inner-brain-eval-local-file 当前文件名`；项目版本提升到 `0.72.0`，更新更新清单测试夹具到 `0.72.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.72.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 404 checked across 337 files`，敏感扫描和本地配置文件检查通过。
- 备注：安装脚本检查首次使用了错误的 `dist\installer` 路径；按系统化调试定位到实际路径 `windows-installer-stage\install.cmd` 与 `JarvisLiteSetup.sed` 后复验通过。
- Git：本地提交 `c0401d1 feat: 提示本机文件失败视图总览入口 0.72.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.73.0 InnerBrain 本机已处理指定文件视图当前文件总览入口

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / build_windows_installer / PyInstaller / Markdown 链接检查
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 InnerBrain 本机 evaluation 同文件导航后，发现指定文件已处理视图缺少回到当前文件全部样本的入口，选择“本机已处理指定文件视图当前文件总览入口”作为 0.73.0 小闭环。
- 计划：在 `/inner-brain-eval-local-resolved 文件名` 展示指定文件已处理样本后，后续处理除当前文件待处理失败、当前文件报告、全部已处理和全部待处理失败外，追加 `/inner-brain-eval-local-file 当前文件名`。
- 约束：新逻辑只改变指定文件已处理视图反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变已处理筛选、评估主体、失败修复建议、报告正文、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：新增指定文件已处理视图当前文件总览入口断言和版本一致性测试先失败；失败点为反馈缺少 `/inner-brain-eval-local-file real-log.jsonl`，项目版本仍为 `0.72.0`。
- GREEN：同一目标命令 3 项通过。
- 实现：`JarvisAgent._inner_brain_local_resolved_evaluation()` 在指定 `source_file_filter` 的已处理视图反馈中追加 `/inner-brain-eval-local-file 当前文件名`；项目版本提升到 `0.73.0`，更新更新清单测试夹具到 `0.73.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.73.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 407 checked across 338 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `8f7814f feat: 提示本机已处理视图总览入口 0.73.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.74.0 InnerBrain 本机失败视图失败文件分组当前文件总览入口

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / build_windows_installer / PyInstaller / Markdown 链接检查
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.63.0 失败文件分组聚焦入口、0.64.0 失败文件分组报告入口和 0.72.0 指定文件失败视图当前文件总览入口模式，选择“本机失败视图失败文件分组当前文件总览入口”作为 0.74.0 小闭环。
- 计划：在 `/inner-brain-eval-local-failed` 的 `失败文件：` 分组中，为每个失败来源文件追加 `/inner-brain-eval-local-file 当前文件名`，并保留同文件待处理失败入口和按文件报告入口。
- 约束：新逻辑只改变全量本机失败视图的失败文件分组文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变失败排序、指定文件失败视图、已处理视图、本机 evaluation JSONL payload、修复建议或报告导出路径。
- RED：新增失败文件分组总览入口断言和版本一致性测试先失败；失败点为失败文件分组缺少 `总览：/inner-brain-eval-local-file failed-log.jsonl`，项目版本仍为 `0.73.0`。
- GREEN：同一目标命令 4 项通过。
- 实现：`describe_inner_brain_evaluation()` 在本机失败视图 `失败文件：` 分组行中追加 `总览：/inner-brain-eval-local-file 当前文件名`；项目版本提升到 `0.74.0`，更新更新清单测试夹具到 `0.74.1`。
- 验证：Agent + InnerBrain + ProjectMetadata 相邻回归 349 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.74.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 410 checked across 339 files`，敏感扫描和本地配置文件检查通过。
- 备注：SED 目标路径检查首次使用 `Select-String -Pattern` 导致 Windows 反斜杠正则解析失败；按系统化调试定位为命令写法后，改用 `-SimpleMatch` 复验通过。
- Git：本地提交 `996d452 feat: 提示本机失败文件分组总览入口 0.74.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.75.0 InnerBrain 本机已处理视图文件候选当前文件总览入口

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / build_windows_installer / PyInstaller / Markdown 链接检查
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描本机 evaluation 同文件导航后，发现全量已处理视图的 `可查看文件：` 候选行缺少回到同文件全部样本的入口，选择“本机已处理视图文件候选当前文件总览入口”作为 0.75.0 小闭环。
- 计划：在 `/inner-brain-eval-local-resolved` 未指定文件时，为 `可查看文件：` 候选行追加 `总览：/inner-brain-eval-local-file 当前文件名`，并将原入口标注为 `已处理：/inner-brain-eval-local-resolved 当前文件名`。
- 约束：新逻辑只改变全量已处理视图文件候选文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变候选排序、指定文件已处理视图、失败视图、本机 evaluation JSONL payload、修复建议或报告导出路径。
- RED：新增全量已处理视图文件候选总览入口断言和版本一致性测试先失败；失败点为候选行缺少 `总览：/inner-brain-eval-local-file real-log.jsonl`，项目版本仍为 `0.74.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._inner_brain_local_resolved_evaluation()` 在全量已处理视图文件候选行中追加 `总览：/inner-brain-eval-local-file 当前文件名`，原已处理入口显式标注为 `已处理：/inner-brain-eval-local-resolved 当前文件名`；项目版本提升到 `0.75.0`，更新更新清单测试夹具到 `0.75.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.75.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 413 checked across 340 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `1c6dcdf feat: 提示本机已处理文件候选总览入口 0.75.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.76.0 InnerBrain 本机评估全量视图文件候选总览标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / build_windows_installer / PyInstaller / Markdown 链接检查
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描本机 evaluation 同文件导航后，发现全量 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选行仍使用裸 `/inner-brain-eval-local-file 当前文件名`，选择“本机评估全量视图文件候选总览标签”作为 0.76.0 小闭环。
- 计划：在 `/inner-brain-eval-local` 未指定文件时，为 `可聚焦文件：` 候选行把主入口标注为 `总览：/inner-brain-eval-local-file 当前文件名`，并保留失败文件的待处理和报告入口。
- 约束：新逻辑只改变全量本机评估视图文件候选文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变候选排序、失败视图、已处理视图、本机 evaluation JSONL payload、修复建议或报告导出路径。
- RED：新增全量本机评估文件候选总览标签断言和版本一致性测试先失败；失败点为候选行仍使用裸 `/inner-brain-eval-local-file zzz-failed-log.jsonl`，项目版本仍为 `0.75.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_evaluation()` 在全量本机评估视图文件候选行中把同文件全部样本入口标注为 `总览：/inner-brain-eval-local-file 当前文件名`；项目版本提升到 `0.76.0`，更新更新清单测试夹具到 `0.76.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.76.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 416 checked across 348 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `7b39a37 feat: 标注本机评估文件候选总览入口 0.76.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.77.0 InnerBrain 本机文件失败视图当前文件总览标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.72.0 指定文件失败视图当前文件总览入口和 0.76.0 全量本机评估文件候选总览标签模式，选择“本机文件失败视图当前文件总览标签”作为 0.77.0 小闭环。
- 计划：在 `/inner-brain-eval-local-file-failed 文件名` 的后续处理中，把回到同文件全部样本的入口从 `查看当前文件全部样本：/inner-brain-eval-local-file 当前文件名` 调整为 `当前文件总览：/inner-brain-eval-local-file 当前文件名`。
- 约束：新逻辑只改变指定文件失败视图后续处理文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变评估主体、失败排序、失败修复建议、Markdown 报告正文、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新指定文件失败视图当前文件总览标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `查看当前文件全部样本：...`，项目版本仍为 `0.76.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_failed_evaluation()` 在指定 `source_file_filter` 的失败视图反馈中把同文件全部样本入口标注为 `当前文件总览：/inner-brain-eval-local-file 当前文件名`；项目版本提升到 `0.77.0`，更新更新清单测试夹具到 `0.77.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.77.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 419 checked across 169 files`，敏感扫描和本地配置文件检查通过。
- 备注：安装脚本和 SED 首次按错误仓库内路径检查失败；按系统化调试定位到构建产物真实路径后复验通过。Markdown 链接检查使用 Git 跟踪的 Markdown 文件范围，未把 `.codex` 忽略留痕文件计入提交验证范围。
- Git：本地提交 `7f47b71 feat: 标注本机文件失败视图总览入口 0.77.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.78.0 InnerBrain 本机已处理指定文件视图当前文件总览标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / git ls-files / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 InnerBrain 本机 evaluation 同文件导航后，发现指定文件已处理视图仍用 `查看当前文件全部样本`，选择“本机已处理指定文件视图当前文件总览标签”作为 0.78.0 小闭环。
- 计划：在 `/inner-brain-eval-local-resolved 文件名` 的后续处理中，把回到同文件全部样本的入口从 `查看当前文件全部样本：/inner-brain-eval-local-file 当前文件名` 调整为 `当前文件总览：/inner-brain-eval-local-file 当前文件名`。
- 约束：新逻辑只改变指定文件已处理视图后续处理文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变已处理筛选、评估主体、失败修复建议、Markdown 报告正文、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新指定文件已处理视图当前文件总览标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `查看当前文件全部样本：...`，项目版本仍为 `0.77.0`。
- GREEN：同一目标命令 3 项通过。
- 实现：`JarvisAgent._inner_brain_local_resolved_evaluation()` 在指定 `source_file_filter` 的已处理视图反馈中把同文件全部样本入口标注为 `当前文件总览：/inner-brain-eval-local-file 当前文件名`；项目版本提升到 `0.78.0`，更新更新清单测试夹具到 `0.78.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.78.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 422 checked across 170 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `6cd77ac feat: 标注本机已处理视图总览入口 0.78.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.79.0 InnerBrain 本机失败报告导出反馈当前文件总览标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-CimInstance
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 InnerBrain 本机 evaluation 同文件导航后，发现指定文件报告导出反馈仍用 `查看当前文件全部样本`，选择“本机失败报告导出反馈当前文件总览标签”作为 0.79.0 小闭环。
- 计划：在 `/inner-brain-eval-local-report 文件名` 的导出反馈中，把回到同文件全部样本的入口从 `查看当前文件全部样本：/inner-brain-eval-local-file 当前文件名` 调整为 `当前文件总览：/inner-brain-eval-local-file 当前文件名`。
- 约束：新逻辑只改变指定文件报告导出反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新指定文件报告导出反馈当前文件总览标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `查看当前文件全部样本：...`，项目版本仍为 `0.78.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._export_inner_brain_local_evaluation_report()` 在指定 `source_file_filter` 的报告导出反馈中把同文件全部样本入口标注为 `当前文件总览：/inner-brain-eval-local-file 当前文件名`；项目版本提升到 `0.79.0`，更新更新清单测试夹具到 `0.79.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.79.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 425 checked across 169 files`，敏感扫描和本地配置文件检查通过。
- 备注：SED 目标路径检查首次使用 `Select-String -Pattern` 导致 Windows 反斜杠正则解析失败，改用 `-SimpleMatch` 复验通过；打包后 smoke 首次并行检查时短暂看到 `JarvisLite` 进程，等待后自动退出，复跑确认无残留进程。
- Git：本地提交 `10ef5ef feat: 标注本机报告导出总览入口 0.79.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.80.0 InnerBrain 本机失败报告导出反馈当前文件待处理失败标签

- 时间：2026-06-03 03:32 +08:00 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 InnerBrain 本机 evaluation 同文件导航后，发现指定文件报告导出反馈仍用 `复查当前文件失败样本`，选择“本机失败报告导出反馈当前文件待处理失败标签”作为 0.80.0 小闭环。
- 计划：在 `/inner-brain-eval-local-report 文件名` 的导出反馈中，把同文件失败入口从 `复查当前文件失败样本：/inner-brain-eval-local-file-failed 当前文件名` 调整为 `查看当前文件待处理失败样本：/inner-brain-eval-local-file-failed 当前文件名`。
- 约束：新逻辑只改变指定文件报告导出反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新指定文件报告导出反馈待处理失败标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `复查当前文件失败样本：...`，项目版本仍为 `0.79.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._export_inner_brain_local_evaluation_report()` 在指定 `source_file_filter` 的报告导出反馈中把同文件失败入口标注为 `查看当前文件待处理失败样本：/inner-brain-eval-local-file-failed 当前文件名`；项目版本提升到 `0.80.0`，更新更新清单测试夹具到 `0.80.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.80.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 428 checked across 172 files`，敏感扫描和本地配置文件检查通过。
- 备注：打包后 smoke 与进程检查合并命令首次因 `Get-Process` 无结果产生非零退出；按系统化调试确认根因为检查命令写法后，改用显式分支复验无残留进程。
- Git：本地提交 `d1e930c feat: 标注本机报告导出待处理入口 0.80.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.81.0 InnerBrain 本机当前文件反馈全部待处理失败标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 InnerBrain 本机 evaluation 当前文件反馈后，发现指定文件失败视图和指定文件报告导出反馈仍用 `查看全部本机失败样本`，选择“本机当前文件反馈全部待处理失败标签”作为 0.81.0 小闭环。
- 计划：在 `/inner-brain-eval-local-file-failed 文件名` 和 `/inner-brain-eval-local-report 文件名` 的后续处理中，把返回全量失败视图的入口从 `查看全部本机失败样本：/inner-brain-eval-local-failed` 调整为 `查看全部待处理失败样本：/inner-brain-eval-local-failed`。
- 约束：新逻辑只改变当前文件反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变失败视图主体、报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新指定文件失败视图、指定文件报告导出反馈全部待处理失败标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `查看全部本机失败样本：...`，项目版本仍为 `0.80.0`。
- GREEN：同一目标命令 3 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_failed_evaluation()` 和 `JarvisAgent._export_inner_brain_local_evaluation_report()` 在指定 `source_file_filter` 的后续处理中把返回全量失败视图入口标注为 `查看全部待处理失败样本：/inner-brain-eval-local-failed`；项目版本提升到 `0.81.0`，更新更新清单测试夹具到 `0.81.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.81.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 431 checked across 174 files`，敏感扫描和本地配置文件检查通过。
- Git：本地提交 `f596b6e feat: 标注本机当前文件待处理入口 0.81.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.82.0 InnerBrain 本机失败报告导出反馈全量待处理失败标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：按 0.81.0 当前文件反馈全部待处理失败标签模式，选择“本机失败报告导出反馈全量待处理失败标签”作为 0.82.0 小闭环。
- 计划：在 `/inner-brain-eval-local-report` 未指定文件的导出反馈中，把返回全量失败视图的入口从 `查看本机失败样本：/inner-brain-eval-local-failed` 调整为 `查看待处理失败样本：/inner-brain-eval-local-failed`。
- 约束：新逻辑只改变未指定文件报告导出反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新全量报告导出反馈待处理失败标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `查看本机失败样本：...`，项目版本仍为 `0.81.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._export_inner_brain_local_evaluation_report()` 在未指定 `source_file_filter` 的报告导出反馈中把返回失败视图入口标注为 `查看待处理失败样本：/inner-brain-eval-local-failed`；项目版本提升到 `0.82.0`，更新更新清单测试夹具到 `0.82.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.82.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK (175 files).`，敏感扫描、过期标记扫描和本地配置文件检查通过。
- 备注：Markdown 链接检查首次脚本正则未正确转义 Windows 盘符反斜杠，改用 `Path.IsPathFullyQualified()` 后复验通过。
- Git：本地提交 `e59b140 feat: 标注本机报告导出待处理入口 0.82.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.83.0 InnerBrain 本机文件失败视图全部待处理失败报告标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 InnerBrain 本机 evaluation 当前文件失败视图后，发现指定文件失败视图仍用 `导出全部本机失败报告`，选择“本机文件失败视图全部待处理失败报告标签”作为 0.83.0 小闭环。
- 计划：在 `/inner-brain-eval-local-file-failed 文件名` 的后续处理中，把全量报告入口从 `导出全部本机失败报告：/inner-brain-eval-local-report` 调整为 `导出全部待处理失败报告：/inner-brain-eval-local-report`。
- 约束：新逻辑只改变指定文件失败视图反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新指定文件失败视图全部待处理失败报告标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `导出全部本机失败报告：...`，项目版本仍为 `0.82.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_failed_evaluation()` 在指定 `source_file_filter` 的失败视图反馈中把全量报告入口标注为 `导出全部待处理失败报告：/inner-brain-eval-local-report`；项目版本提升到 `0.83.0`，更新更新清单测试夹具到 `0.83.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案为 `0.83.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK (176 files).`，敏感扫描、当前文档过期标记扫描和本地配置文件检查通过。
- Git：本地提交 `06db634 feat: 标注本机文件失败报告待处理入口 0.83.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.84.0 InnerBrain 本机失败视图待处理失败报告标签

- 时间：2026-06-03 04:39 +08:00 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v87 后继续收口全量失败视图报告入口语义，发现 `/inner-brain-eval-local-failed` 未指定文件仍用 `导出本机失败报告`，选择“本机失败视图待处理失败报告标签”作为 0.84.0 小闭环。
- 计划：在 `/inner-brain-eval-local-failed` 未指定文件的后续处理中，把全量报告入口从 `导出本机失败报告：/inner-brain-eval-local-report` 调整为 `导出待处理失败报告：/inner-brain-eval-local-report`。
- 约束：主变更只改变全量失败视图反馈文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新全量失败视图待处理失败报告标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `导出本机失败报告：...`，项目版本仍为 `0.83.0`。
- 附加调试：打包后 smoke 首次在 2 秒检查点残留 `JarvisLite.exe`；使用系统化调试复查源码和打包入口后，定位为 smoke 分支只关闭窗口但未显式销毁 Qt widget。
- GREEN：目标测试、版本一致性测试和新增桌面 smoke 清理测试 3 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_failed_evaluation()` 未指定文件分支把全量报告入口标注为 `导出待处理失败报告：/inner-brain-eval-local-report`；`jarvis_lite.desktop.app.main()` 的 `--smoke` 分支显式关闭并 `deleteLater()` 面板和桌面窗口，处理 Qt `DeferredDelete` 事件后退出；项目版本提升到 `0.84.0`，更新更新清单测试夹具到 `0.84.1`。
- 验证：Agent + ProjectMetadata + DesktopApp 相邻回归 310 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案为 `0.84.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 440 checked across 177 files`，敏感扫描、旧文案扫描和本地配置文件检查通过。
- Git：本地提交 `45d498e feat: 标注本机失败报告待处理入口 0.84.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.85.0 InnerBrain 本机失败视图按文件待处理失败报告标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 0.84.0 后的全量失败视图反馈，发现同一后续处理组中全量报告入口已使用 `导出待处理失败报告`，但按文件报告入口仍用 `按文件导出失败报告`。
- 计划：在 `/inner-brain-eval-local-failed` 未指定文件的后续处理中，把按文件报告入口从 `按文件导出失败报告：/inner-brain-eval-local-report 文件名` 调整为 `按文件导出待处理失败报告：/inner-brain-eval-local-report 文件名`。
- 约束：新逻辑只改变全量失败视图按文件报告入口文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新全量失败视图按文件待处理失败报告标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `按文件导出失败报告：...`，项目版本仍为 `0.84.0`。
- GREEN：同一目标命令 2 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_failed_evaluation()` 未指定文件分支把按文件报告入口标注为 `按文件导出待处理失败报告：/inner-brain-eval-local-report 文件名`；项目版本提升到 `0.85.0`，更新更新清单测试夹具到 `0.85.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案为 `0.85.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 443 checked across 178 files`，敏感扫描、旧文案扫描和本地配置文件检查通过。
- Git：本地提交 `0295fe5 feat: 标注本机失败视图按文件报告入口 0.85.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.86.0 InnerBrain 本机当前文件待处理失败报告标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 0.85.0 后的 InnerBrain 本机失败报告入口，发现当前文件总览、当前文件失败视图和当前文件已处理视图仍用 `导出当前文件失败报告`。
- 计划：在三个当前文件反馈中，把当前文件报告入口从 `导出当前文件失败报告：/inner-brain-eval-local-report 文件名` 调整为 `导出当前文件待处理失败报告：/inner-brain-eval-local-report 文件名`。
- 约束：新逻辑只改变当前文件报告入口文案，不自动训练、不写 `data/inner-brain/training/runtime.jsonl`，不改变报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新当前文件总览、当前文件失败视图、当前文件已处理视图和版本一致性测试先失败；失败点为反馈仍输出旧的 `导出当前文件失败报告：...`，项目版本仍为 `0.85.0`。
- GREEN：同一目标命令 4 项通过。
- 调试：Agent + ProjectMetadata 相邻回归首次因更新测试 manifest 夹具仍为 `0.85.1` 且断言未同步而失败；按系统化调试确认根因为版本提升后的测试数据残留，更新到 `0.86.1` 后复验通过。
- 实现：`JarvisAgent._describe_inner_brain_local_evaluation()`、`JarvisAgent._describe_inner_brain_local_failed_evaluation()` 和 `JarvisAgent._inner_brain_local_resolved_evaluation()` 的当前文件报告入口改为 `导出当前文件待处理失败报告：/inner-brain-eval-local-report 文件名`；项目版本提升到 `0.86.0`，更新更新清单测试夹具到 `0.86.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案为 `0.86.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 437 checked across 175 files`，敏感扫描、旧文案扫描和本地配置文件检查通过。
- Git：本地提交 `699ff22 feat: 标注本机当前文件报告入口 0.86.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.87.0 InnerBrain 本机评估样本保存反馈待处理失败标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 0.86.0 后的保存反馈，发现本机 evaluation 样本保存后续验证仍用 `只看失败样本` 和 `导出样本文件失败报告`。
- 计划：在保存反馈中，把失败视图入口标注为 `只看待处理失败样本：/inner-brain-eval-local-failed`，把报告入口标注为 `导出样本文件待处理失败报告：/inner-brain-eval-local-report runtime.jsonl`。
- 约束：新逻辑只改变保存反馈后续验证文案，不自动训练、不改变候选保留、报告正文、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：更新四个保存入口待处理失败标签断言和版本一致性测试先失败；失败点为反馈仍输出旧的 `只看失败样本` / `导出样本文件失败报告`，项目版本仍为 `0.86.0`。
- GREEN：同一目标命令 5 项通过。
- 实现：`JarvisAgent._describe_inner_brain_evaluation_case_save()` 的后续验证入口改为 `只看待处理失败样本：/inner-brain-eval-local-failed` 和 `导出样本文件待处理失败报告：/inner-brain-eval-local-report runtime.jsonl`；项目版本提升到 `0.87.0`，更新更新清单测试夹具到 `0.87.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案为 `0.87.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 440 checked across 176 files`，严格密钥形态扫描、旧文案扫描和本地配置文件检查通过。
- Git：本地提交 `d516777 feat: 标注评估样本保存待处理入口 0.87.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.88.0 InnerBrain 本机文件候选待处理报告标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Select-String / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 0.87.0 后的文件候选和失败文件分组，发现短标签仍用 `报告：/inner-brain-eval-local-report 文件名`。
- 计划：在本机失败文件分组、本机评估全量文件候选和本机已处理全量文件候选中，把短标签改为 `待处理报告：/inner-brain-eval-local-report 文件名`。
- 约束：新逻辑只改变文件候选短标签，不自动训练、不改变候选排序、报告正文、报告导出路径、本机 evaluation JSONL payload 或命令集合。
- RED：修正测试名后，目标测试 7 项先失败；失败点为文件候选/失败文件分组仍输出旧的 `报告` 短标签，项目版本仍为 `0.87.0`。
- GREEN：同一目标命令 7 项通过。
- 实现：`describe_inner_brain_evaluation()`、`JarvisAgent._describe_inner_brain_local_evaluation()` 和 `JarvisAgent._inner_brain_local_resolved_evaluation()` 的文件候选短标签改为 `待处理报告：/inner-brain-eval-local-report 文件名`；项目版本提升到 `0.88.0`，更新更新清单测试夹具到 `0.88.1`。
- 验证：Agent + InnerBrain + ProjectMetadata 相邻回归 349 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.88.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 452 checked across 353 files`，严格密钥形态扫描、旧短标签扫描、过期版本扫描和本地配置文件检查通过。
- Git：本地提交 `1bd9d71 feat: 标注本机文件候选待处理报告 0.88.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.89.0 InnerBrain 本机报告导出待处理失败标题

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / PowerShell 文档同步 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v93，发现本机报告导出反馈、运行日志和 Markdown H1 仍用“本机评估失败报告”，与最近一系列待处理失败标签不一致，选择“本机报告导出待处理失败标题”作为 `0.89.0` 小闭环。
- 计划：在 `/inner-brain-eval-local-report [文件名]` 的导出反馈、运行日志和 `export_inner_brain_evaluation_report()` Markdown 标题中统一为“本机评估待处理失败报告”。
- 约束：新逻辑只改变导出标题/反馈/日志文案，不自动训练、不改变报告路径、报告正文统计、失败筛选、本机 evaluation JSONL payload 或命令集合。
- RED：更新两个 Agent 导出反馈测试、InnerBrain 报告标题测试和版本一致性测试后先失败；失败点为旧标题和旧版本。
- GREEN：同一目标命令 4 项通过。
- 实现：`JarvisAgent._export_inner_brain_local_evaluation_report()` 的日志与成功反馈、`export_inner_brain_evaluation_report()` 的 docstring 与 H1 标题改为“本机评估待处理失败报告”；项目版本提升到 `0.89.0`，更新更新清单测试夹具到 `0.89.1`。
- 验证：Agent + InnerBrain + ProjectMetadata 相邻回归 349 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.89.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 455 checked across 354 files`，严格密钥形态扫描、旧标题/旧反馈扫描、过期版本扫描和本地配置文件检查通过。
- Git：本地提交 `196fcad feat: 标注本机报告导出待处理标题 0.89.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.90.0 InnerBrain 本机失败帮助待处理标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / PowerShell 文档同步 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v94，发现本机失败视图相关 `/help` 文案和运行日志仍用泛化“失败样本/失败报告”，选择“本机失败帮助待处理标签”作为 `0.90.0` 小闭环。
- 计划：在 `/help` 中把本机失败视图和报告入口收紧为“待处理失败样本/待处理失败报告”；在 `/inner-brain-eval-local-failed` 和 `/inner-brain-eval-local-file-failed 文件名` 运行日志中改为“只显示待处理失败样本”。
- 约束：新逻辑只改变帮助和日志文案，不自动训练、不改变命令集合、失败筛选、排序、报告正文、报告路径、本机 evaluation JSONL payload 或训练样本写入。
- RED：目标测试 4 项先失败；失败点为旧帮助/旧日志和旧版本。
- GREEN：同一目标命令 4 项通过。
- 实现：`JarvisAgent._help()` 的三个本机失败相关入口改为待处理失败标签；本机失败视图和指定文件失败视图 record_log 改为“只显示待处理失败样本”；项目版本提升到 `0.90.0`，更新更新清单测试夹具到 `0.90.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.90.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 458 checked across 181 files`，严格密钥形态扫描、旧帮助/旧日志扫描、过期版本扫描和本地配置文件检查通过。
- Git：本地提交 `8cf48de feat: 标注本机失败帮助待处理标签 0.90.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.91.0 InnerBrain 本机报告导出反馈待处理失败计数标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / PowerShell 文档同步 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v95，发现 `/inner-brain-eval-local-report [文件名]` 成功反馈的计数行仍使用泛化 `失败样本：N`，选择“本机报告导出反馈待处理失败计数标签”作为 `0.91.0` 小闭环。
- 计划：在报告导出成功反馈中把计数行改为 `待处理失败样本：N`，让导出反馈与帮助、运行日志、失败视图和报告标题的待处理失败语义一致。
- 约束：新逻辑只改变成功反馈计数文案，不改变 Markdown 报告正文统计标题、命令集合、失败筛选、排序、报告路径、本机 evaluation payload 或训练样本写入。
- RED：目标测试 3 项先失败；失败点为报告导出反馈仍输出旧的 `失败样本：1`，版本仍为 `0.90.0`。
- GREEN：同一目标命令 3 项通过。
- 实现：`JarvisAgent._export_inner_brain_local_evaluation_report()` 的成功反馈计数行改为 `待处理失败样本：{save_result.failed_count}`；项目版本提升到 `0.91.0`，更新更新清单测试夹具到 `0.91.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.91.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 461 checked across 356 files`，严格密钥形态扫描、旧反馈/旧断言/旧 manifest 夹具扫描、当前文档过期标记扫描和本地配置文件检查通过。
- Git：本地提交 `9cdb02e feat: 标注报告导出反馈待处理计数 0.91.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.92.0 InnerBrain 本机全量反馈按文件聚焦待处理失败标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / PowerShell 文档同步 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v96，发现本机全量失败视图和全量报告导出反馈中仍使用泛化 `按文件聚焦失败：/inner-brain-eval-local-file-failed 文件名`，选择“本机全量反馈按文件聚焦待处理失败标签”作为 `0.92.0` 小闭环。
- 计划：在 `_describe_inner_brain_local_failed_evaluation()` 未指定文件分支和 `_export_inner_brain_local_evaluation_report()` 未指定文件反馈中，把按文件聚焦入口标注为 `按文件聚焦待处理失败：/inner-brain-eval-local-file-failed 文件名`。
- 约束：新逻辑只改变两个全量反馈文案，不改变固定评估、指定文件反馈、命令集合、别名、筛选、排序、报告路径、本机 evaluation payload 或训练样本写入。
- RED：目标测试 3 项先失败；失败点为两个全量反馈仍输出旧的 `按文件聚焦失败：...`，版本仍为 `0.91.0`。
- GREEN：同一目标命令 3 项通过。
- 实现：`JarvisAgent._describe_inner_brain_local_failed_evaluation()` 和 `JarvisAgent._export_inner_brain_local_evaluation_report()` 的未指定文件后续处理入口改为 `按文件聚焦待处理失败：/inner-brain-eval-local-file-failed 文件名`；项目版本提升到 `0.92.0`，更新更新清单测试夹具到 `0.92.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.92.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 464 checked across 184 files`，严格密钥形态扫描、旧标签/旧 manifest 夹具扫描、当前文档过期标记扫描和本地配置文件检查通过。
- Git：本地提交 `cbfc974 feat: 标注按文件聚焦待处理失败 0.92.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.93.0 InnerBrain 全量评估运行日志固定与本机评估集标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / PowerShell 文档同步 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / Get-Process
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v97，发现 `/inner-brain-eval` 与 `/inner-brain-eval-failed` 的运行日志仍使用“本地评估集”，容易和只看本机样本的 `/inner-brain-eval-local` 混淆。
- 计划：把两个全量评估命令的运行日志标注为“固定与本机评估集”，只改变日志文案，不改变评估输出正文或本机评估命令。
- 约束：不修改 `/inner-brain-eval-local` 或指定文件本机评估日志，不改变命令集合、别名、筛选、排序、报告路径、本机 evaluation payload 或训练样本写入。
- RED：目标测试 3 项先失败；失败点为两个全量评估日志仍输出旧的“本地评估集”，版本仍为 `0.92.0`。
- GREEN：同一目标命令 3 项通过。
- 实现：`JarvisAgent.handle()` 中 `/inner-brain-eval` 和 `/inner-brain-eval-failed` 分支的 `record_log` 文案改为 `执行 InnerBrain 固定与本机评估集` 与 `执行 InnerBrain 固定与本机评估集并只显示失败样本`；项目版本提升到 `0.93.0`，更新更新清单测试夹具到 `0.93.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.93.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 467 checked across 185 files`，严格密钥形态扫描、旧全量评估日志/旧 manifest 夹具扫描、当前文档过期标记扫描和本地配置文件检查通过。
- Git：本地提交 `7a6e64c feat: 标注全量评估运行日志 0.93.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.94.0 InnerBrain 全量评估输出固定与本机评估集标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / PowerShell 精确文档替换 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Get-Item VersionInfo / Start-Process / Get-Process / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v98，发现普通评估描述已接入用户可读标签，但已处理样本 resolved 描述仍输出 `local_evaluation` 内部名。
- 计划：复用 `_inner_brain_evaluation_display_name()` 映射普通评估与 resolved 评估的 `report.name` 和 `source_counts` 展示名，只改变响应正文显示标签。
- 约束：不改变 `report.name`、source key、筛选、排序、JSONL payload、命令集合、报告路径或训练样本写入。
- RED：目标测试 7 项先失败；补充 resolved 函数层 2 项先失败，确认 resolved 输出仍为内部名。
- GREEN：目标命令 7 项通过；补充 resolved 函数层 2 项通过。
- 实现：`describe_inner_brain_evaluation()` 和 `describe_inner_brain_resolved_evaluation()` 的评估集名与来源计数统一走 `_inner_brain_evaluation_display_name()`；项目版本提升到 `0.94.0`，更新更新清单测试夹具到 `0.94.1`。
- 验证：Agent + InnerBrain + ProjectMetadata 相邻回归 349 项通过，全量 unittest 566 项通过，源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后 exe smoke 退出码 0 且进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.94.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 470 checked across 186 files`，严格密钥形态扫描、旧内部评估集显示名扫描和本地配置文件检查通过。
- Git：本地提交 `c721e64 feat: 标注全量评估输出 0.94.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.95.0 InnerBrain 全量评估帮助固定与本机评估集标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / Python 字节级文档替换 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Get-Item VersionInfo / Start-Process / Get-Process / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v99，发现 `/help` 的全量评估入口仍使用泛化“评估集/评估失败样本”，与 `0.93.0` 运行日志和 `0.94.0` 输出正文不一致。
- 计划：把 `/inner-brain-eval` 帮助说明改为执行固定评估集和本机评估集，把 `/inner-brain-eval-failed` 帮助说明改为只显示固定与本机评估集失败样本。
- 约束：只改变帮助文案，不改变评估输出正文、运行日志、命令集合、别名、筛选、排序、报告路径、本机 evaluation payload 或训练样本写入。
- RED：目标测试 4 项中 2 项先失败；失败点为旧帮助文案和旧版本。
- GREEN：同一目标命令 4 项通过。
- 实现：`JarvisAgent._help()` 两行全量评估说明改为固定与本机评估集标签；项目版本提升到 `0.95.0`，更新更新清单测试夹具到 `0.95.1`。
- 验证：Agent + ProjectMetadata 相邻回归 304 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.95.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 472 checked across 187 tracked files`，严格密钥形态扫描、旧全量评估帮助文案扫描、README BOM 和本地配置文件检查通过。
- Git：本地提交 `bec5806 feat: 标注全量评估帮助 0.95.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.96.0 InnerBrain 本机报告处理边界待处理失败标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Get-Item VersionInfo / Start-Process / Get-Process / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / git status / git diff
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；`tool_search` 查询也未发现对应工具；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v99，发现导出的 `word/inner-brain-evaluation-report.md` 处理边界仍提示“需要修复失败样本时”，与本机评估待处理失败报告标题、反馈和计数不一致。
- 计划：把 `export_inner_brain_evaluation_report()` 的处理边界提示收紧为“需要修复待处理失败样本时”，同步版本、方案、进度、验证索引和本地审查记录。
- 约束：只改变 Markdown 报告处理边界提示，不改变报告标题、统计分组、失败筛选、修复建议内容、报告路径、本机 evaluation JSONL payload、命令集合或训练样本写入。
- RED：目标测试 4 项先失败；失败点为旧处理边界提示和旧版本。
- GREEN：同一目标命令 4 项通过。
- 实现：`export_inner_brain_evaluation_report()` 处理边界提示改为 `需要修复待处理失败样本时`；`tests/test_inner_brain.py` 增加新提示断言和旧提示负断言；项目版本提升到 `0.96.0`，更新更新清单测试夹具到 `0.96.1`。
- 验证：Agent + InnerBrain + ProjectMetadata 相邻回归 349 项通过，全量 unittest 566 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.96.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 474 checked across 188 tracked files`，严格密钥形态扫描、旧报告处理边界提示扫描、过期版本扫描、README BOM 和本地配置文件检查通过。
- Git：本地提交 `e207857 feat: 标注报告处理边界待处理标签 0.96.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.97.0 InnerBrain 本机失败视图文档待处理失败标签

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / PowerShell 精确文档替换 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Get-Item VersionInfo / Start-Process / Get-Process / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：扫描 0.96.0 后的公开文档，发现 README 概要段仍写“只看失败”，PROJECT-PLAN 仍写“本机失败样本”，与 `/help`、运行日志、报告标题、报告反馈和报告处理边界的待处理失败语义不一致。
- 计划：增加公开文档一致性测试，把 README 与 PROJECT-PLAN 的本机失败视图说明收紧为待处理失败标签，同步版本、v101 方案、进度和验证索引。
- 约束：只改变公开文档和版本/测试夹具，不修改运行时代码、命令集合、报告正文、报告路径、本机 evaluation JSONL payload 或训练样本写入。
- RED：目标文档一致性测试和版本一致性测试先失败；失败点为 README/PROJECT-PLAN 旧表述和旧版本。
- GREEN：目标命令 4 项通过。
- 实现：`tests/test_project_metadata.py` 增加文档一致性测试；README 概要和 PROJECT-PLAN 能力描述统一为待处理失败标签；项目版本提升到 `0.97.0`，更新更新清单测试夹具到 `0.97.1`。
- 验证：Agent + ProjectMetadata 相邻回归 305 项通过，全量 unittest 567 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `ProcessCount=0`，安装脚本文案和版本资源为 `0.97.0`，安装包大小 `57,131,008` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 479 checked across 190 tracked files`，严格密钥形态扫描、活动公开文档旧标签扫描、更新清单旧夹具扫描、安装产物旧版本标记扫描、README BOM 和本地配置文件检查通过。
- Git：本地提交 `a8a8d68 feat: 标注文档待处理失败标签 0.97.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.98.0 InnerBrain 本机报告指定文件样本计数提示

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Get-Item VersionInfo / Start-Process / Get-Process / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / git status / git diff
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v101，检查发现真实 `data/inner-brain/evaluation/runtime.jsonl` 当前不存在；指定文件报告可导出空报告，但反馈只有待处理失败数和文件名，无法直接区分“无失败”和“当前文件无样本”。
- 计划：在 `/inner-brain-eval-local-report [文件名]` 成功反馈的指定文件分支中追加 `当前文件样本：N`，复用已生成报告的 `report.total_count`。
- 约束：只改变指定文件报告导出反馈；不改变报告正文、报告路径、缺失文件空报告行为、命令集合、筛选、排序、本机 evaluation payload 或训练样本写入。
- RED：目标测试和版本一致性测试先失败；失败点为指定文件报告反馈缺少 `当前文件样本：0`，版本仍为 `0.97.0`。
- GREEN：扩展后的目标命令 4 项通过。
- 实现：`JarvisAgent._export_inner_brain_local_evaluation_report()` 在 `source_file_filter` 存在时输出 `当前文件样本：{report.total_count}`；新增空指定文件报告反馈断言；项目版本提升到 `0.98.0`，更新更新清单测试夹具到 `0.98.1`。
- 验证：Agent + ProjectMetadata 相邻回归 306 项通过，全量 unittest 568 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `RunningJarvisAfterSmoke=0`，安装脚本文案和版本资源为 `0.98.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 482 checked across 191 tracked files`，严格密钥形态扫描、README BOM 和本地配置文件检查通过。
- Git：本地提交 `7fff963 feat: 标注报告指定文件样本计数 0.98.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.99.0 InnerBrain 本机报告空筛选文件补样本写入提示

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / PowerShell 精确文档替换 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Get-Item VersionInfo / Get-Process / git diff --check / Markdown 本地链接检查 / 敏感信息扫描 / Test-Path / git status / git diff
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v102，真实 `runtime.jsonl` 仍不存在；指定文件报告虽已显示 `当前文件样本：0`，但没有说明通用补样本命令默认写入 `runtime.jsonl`，容易让任意筛选文件的空报告后续处理产生误解。
- 计划：在 `/inner-brain-eval-local-report [文件名]` 指定文件分支中，当 `report.total_count == 0` 时追加空筛选文件补样本写入目标提示。
- 约束：不新增按任意 JSONL 文件写入 evaluation 样本的命令；不改变 `/inner-brain-eval-add` 或 `/inner-brain-eval-label` 的默认写入目标；不改变报告正文、报告路径、缺失文件空报告行为、本机 evaluation payload 或训练样本写入。
- RED：目标测试和版本一致性测试先失败；失败点为指定文件空报告反馈缺少 `提示：当前筛选文件暂无本机 evaluation 样本；补样本命令默认写入 runtime.jsonl。`，版本仍为 `0.98.0`。
- GREEN：扩展后的目标命令 4 项通过。
- 实现：`JarvisAgent._export_inner_brain_local_evaluation_report()` 在指定文件且 `report.total_count == 0` 时追加默认写入 `runtime.jsonl` 的提示；项目版本提升到 `0.99.0`，更新更新清单测试夹具到 `0.99.1`。
- 验证：Agent + ProjectMetadata 相邻回归 306 项通过，全量 unittest 568 项通过，源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后 exe smoke 退出码 0 且输出包含 `Jarvis Lite` 与 `desktopPetWindow`，打包后进程检查输出 `RunningJarvisAfterSmoke=0`，安装脚本文案和版本资源为 `0.99.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 484 checked across 192 tracked/untracked files`，严格密钥形态扫描、README BOM、本地配置文件检查和临时报告文件检查通过。
- Git：本地提交 `a1c7f2b feat: 标注报告空筛选文件提示 0.99.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.100.0 InnerBrain 本机空评估视图补样本写入提示

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / PowerShell 精确文档替换 / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Get-Item VersionInfo / Get-Process / git diff --check / Markdown 本地链接检查 / 严格密钥形态扫描 / Test-Path / git status / git diff
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v103，发现本机 evaluation 样本为空时，`/inner-brain-eval-local` 与 `/inner-brain-eval-local-failed` 只列添加入口和“不自动训练”说明，没有说明这些补样本命令默认写入 `runtime.jsonl`。
- 计划：复用 `describe_inner_brain_evaluation()` 的空本机 evaluation 分支，追加 `提示：补样本命令默认写入 runtime.jsonl。`，同步版本、v104 方案、进度和验证索引。
- 约束：不新增按任意 JSONL 文件写入 evaluation 样本的命令；不改变 `/inner-brain-eval-add` 或 `/inner-brain-eval-label` 的默认写入目标；不改变报告正文、报告路径、本机 evaluation payload 或训练样本写入。
- RED：目标测试和版本一致性测试先失败；失败点为三处空本机 evaluation 视图缺少 `提示：补样本命令默认写入 runtime.jsonl。`，版本仍为 `0.99.0`。
- GREEN：同一目标命令 6 项通过。
- 实现：`describe_inner_brain_evaluation()` 在空本机 evaluation 分支追加默认写入 `runtime.jsonl` 的提示；项目版本提升到 `0.100.0`，更新更新清单测试夹具到 `0.100.1`。
- 验证：Agent + InnerBrain + ProjectMetadata 相邻回归 352 项通过，全量 unittest 569 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `RunningJarvisAfterSmoke=0`，安装脚本文案和版本资源为 `0.100.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 488 checked across 193 tracked/untracked files`，严格密钥形态扫描、README BOM、本地配置文件检查和临时报告文件检查通过。
- Git：本地提交 `87e39f7 feat: 标注空评估写入提示 0.100.0` 已创建；远端按用户要求暂不推送。

## 2026-06-03 0.101.0 InnerBrain 本机已处理空视图行动提示

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v104，发现 `/inner-brain-eval-local-resolved [文件名]` 在没有已通过样本时只输出 `- 无` 和只读说明，缺少“这里只显示已通过样本”的行动解释。
- 计划：在 `describe_inner_brain_resolved_evaluation()` 的空已处理样本分支追加提示，引导用户先查看待处理失败样本或补充本机 evaluation 样本；同步版本、v105 方案、进度和验证索引。
- 约束：不改变已处理样本筛选、排序、文件候选、报告入口、后续处理链接、本机 evaluation payload、报告正文、报告路径或训练样本写入。
- RED：目标测试 5 项中 3 项先失败；失败点为空已处理样本视图缺少 `提示：这里只显示已通过样本；暂无已处理样本时，请先查看待处理失败样本或补充本机 evaluation 样本。`，版本仍为 `0.100.0`。
- 实现：`describe_inner_brain_resolved_evaluation()` 在空已处理样本分支追加行动提示；项目版本提升到 `0.101.0`，更新更新清单测试夹具到 `0.101.1`。
- GREEN：同一目标命令 5 项通过。
- 验证：Agent + InnerBrain + ProjectMetadata 相邻回归 352 项通过，全量 unittest 569 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后进程检查输出 `RunningJarvisAfterSmoke=0`，安装脚本文案和版本资源为 `0.101.0`，安装包大小 `57,135,104` 字节，静态检查通过，Markdown 链接检查输出 `Markdown local links OK: 490 checked across 194 tracked/untracked files`，严格密钥形态扫描、README BOM、本地配置文件检查和临时报告文件检查通过。
- Git：本地提交 `e6485f6 feat: 标注已处理空视图提示 0.101.0` 已创建；远端按用户要求暂不推送。本轮任务完成后按用户最新要求暂停，不继续下一个任务。

## 2026-06-03 0.102.0 InnerBrain README 已处理空视图概要同步

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v105，发现 README 安装说明长段已记录本机已处理空视图行动提示，但顶部“InnerBrain 样本闭环”概要仍只说明已处理视图可只读查看已通过样本，未同步空态行动提示。
- 计划：新增 README 顶部概要一致性测试，限定检查 `InnerBrain 样本闭环` bullet；补充概要说明，版本提升到 `0.102.0` 并同步公开文档和验证记录。
- 约束：不修改运行时代码，不改变已处理样本筛选、排序、文件候选、报告入口、后续处理链接、本机 evaluation payload、报告正文、报告路径或训练样本写入。
- RED：目标测试 4 项中 2 项先失败；失败点为 README 顶部概要缺少 `暂无已处理样本时会提示这里只显示已通过样本` 和版本仍为 `0.101.0`。
- 实现：README 顶部 `InnerBrain 样本闭环` 概要补充本机已处理空视图行动提示；项目版本提升到 `0.102.0`，更新更新清单测试夹具到 `0.102.1`。
- GREEN：同一目标命令 4 项通过。
- 验证：Agent + ProjectMetadata 相邻回归 308 项通过，全量 unittest 570 项通过，源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，安装脚本文案和版本资源为 `0.102.0`，安装包大小 `57,135,104` 字节，打包后 exe smoke 输出正常且延迟复查无残留进程，静态检查、Markdown 链接、严格密钥形态扫描、README BOM、本地配置文件检查和临时报告文件检查通过。
- 调试留痕：首次安装脚本校验误用 dist 根目录 `install.cmd` 路径，定位后确认实际路径为 `windows-installer-stage\install.cmd` 并复验通过；首次 README BOM 检查误用 PowerShell 7 不支持的 `-Encoding Byte`，改用 `[System.IO.File]::ReadAllBytes()` 后确认 BOM 为 `EF-BB-BF`；旧版本扫描命中 v105 历史方案中的旧更新清单夹具描述，收窄到本轮活动文件后无遗留旧版本。
- Git：本地提交 `9e323df feat: 同步已处理空视图概要 0.102.0` 已创建；远端按用户要求暂不推送。本轮任务完成后按用户最新要求暂停，不继续下一个任务。

## 2026-06-03 0.103.0 InnerBrain PROJECT-PLAN 已处理空视图主干同步

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / update_plan / apply_patch / unittest / jarvis_lite.desktop.app --smoke / scripts\build_windows_installer.py / Copy-Item / Get-Item VersionInfo / Get-Process / git diff --check / Markdown 本地链接检查 / 严格密钥形态扫描 / Test-Path / git status / git diff
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 摘要：承接 v106，发现 README 顶部概要已同步本机已处理空视图行动提示，但 `word/PROJECT-PLAN.md` 主干“InnerBrain 可观察与样本闭环”概要仍未提到暂无已处理样本时的行动指引。
- 计划：新增 PROJECT-PLAN 主干概要一致性测试，限定检查 `InnerBrain 可观察与样本闭环` bullet；补充主干概要说明，版本提升到 `0.103.0` 并同步公开文档和验证记录。
- 约束：不修改运行时代码，不改变已处理样本筛选、排序、文件候选、报告入口、后续处理链接、本机 evaluation payload、报告正文、报告路径或训练样本写入。
- RED：目标测试 4 项中 2 项先失败；失败点为 PROJECT-PLAN 主干概要缺少 `暂无已处理样本时会提示这里只显示已通过样本` 和版本仍为 `0.102.0`。
- 实现：`word/PROJECT-PLAN.md` 主干 `InnerBrain 可观察与样本闭环` 概要补充本机已处理空视图行动提示；项目版本提升到 `0.103.0`，更新更新清单测试夹具到 `0.103.1`，同步 README、v107 方案、进度、计划索引和验证索引。
- GREEN：同一目标命令 4 项通过。
- 验证：Agent + ProjectMetadata 相邻回归 309 项通过，全量 unittest 571 项通过，源码桌面 smoke 和打包后 exe smoke 均输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`，打包后延迟复查无残留进程，安装脚本文案和版本资源为 `0.103.0`，安装包大小 `57,135,104` 字节，静态检查、Markdown 链接、严格密钥形态扫描、当前范围旧版本扫描、README BOM、本地配置文件检查和临时报告文件检查通过。
- 调试留痕：首次将 `JarvisLite.version.txt` 误按单行版本文件检查导致产物校验失败；根因确认该文件是 PyInstaller 版本资源脚本，既有 verification 记录也按 `FileVersion` 与 `ProductVersion` 检查，按正确口径复验通过。
- Git：本地提交 `f6c21b7 feat: 同步已处理空视图主干 0.103.0` 已创建；远端按用户要求暂不推送。本轮任务完成后按用户最新要求暂停，不继续下一个任务。

## 2026-06-03 0.108.0 截图 OCR 串联恢复执行

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / git status / git log / update_plan / apply_patch / unittest
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 日志核对：`日志.txt` 显示上次在 `0.107.0` OCR 图片识别阶段完成验证并本地提交 `101fef9 feat: 增加 OCR 图片识别 0.107.0` 后，准备进入 `0.108.0` 截图+OCR 串联阶段时因 429 中断。
- 实际状态：`git status --short --branch` 显示工作区干净，`main...origin/main [ahead 65]`；`git log --oneline -5` 的最新提交为 `101fef9 feat: 增加 OCR 图片识别 0.107.0`。
- 文档核对：`word/PROJECT-PLAN.md` 当前版本仍为 `0.107.0`，下一阶段明确包含“截图+OCR 串联”；`word/plans/` 尚无 v113/0.108.0 计划。
- 计划：新增 v113 计划，复用 `screen_capture` 与 `ocr`，增加 `/screen-ocr [文件名] [lang=...]` 组合命令；版本提升到 `0.108.0` 并同步 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
- RED：目标命令 3 项先失败；失败点为 `describe_screen_ocr` 不存在、Agent 未接入 `describe_screen_ocr`、项目版本仍为 `0.107.0`。
- 实现：`screen_capture` 新增 `describe_screen_ocr`，复用 `save_screen_capture` 与 `describe_image_ocr`；`JarvisAgent` 新增 `/screen-ocr [文件名] [lang=...]`、帮助文案和语言参数复用解析；项目版本提升到 `0.108.0`，更新更新清单测试夹具到 `0.108.1`。
- GREEN：同一目标命令 3 项通过；相邻回归 330 项通过；全量 `unittest` 592 项通过。
- Smoke：`/screen-ocr smoke-0.108.0 lang=eng` 保存 `logs/screenshots/smoke-0.108.0.png`，尺寸 `1920x1080`、大小 `195,407` 字节；当前机器未安装 Tesseract，OCR 段落返回可读不可用诊断；截图产物已删除。
- 打包：安装包构建成功，PyInstaller 仅出现既有 `Hidden import "tzdata" not found!` 警告；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.108.0.exe` 已生成，大小 `57,155,584` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.108.0`；打包后 exe smoke 通过且无残留进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查 372 项通过；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。
- 审查降级：`superpowers:requesting-code-review` 要求派发 reviewer 子代理，但当前 `multi_agent_v1.spawn_agent` 工具说明限定只有用户显式要求代理/委派时才能使用；本轮未派发子代理，改做本地自审。

## 2026-06-03 0.109.0 快捷键自动化第一阶段

- 时间：2026-06-03 继续执行
- 工具：Get-Content / rg / git status / git log / update_plan / apply_patch / unittest
- 技能：使用 `superpowers:brainstorming` 确定小阶段边界，使用 `superpowers:test-driven-development` 执行 RED/GREEN，使用 `superpowers:verification-before-completion` 做完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：最新提交为 `00fc4eb feat: 增加截图 OCR 串联 0.108.0`，工作区干净，`word/PROJECT-PLAN.md` 下一阶段为键鼠自动化基础层。
- 设计选择：`0.109.0` 先做显式 `/hotkey key1+key2 [...]`，不做点击、文本输入、窗口切换、应用启动或自然语言自动执行；真实执行使用主流 `pyautogui`，单元测试通过执行器注入避免真实按键。
- 实现：`automation.py` 新增快捷键组合解析、执行结果、执行器注入和 `pyautogui.hotkey()` adapter；`JarvisAgent` 新增 `/hotkey` 命令、帮助文案、运行日志和错误反馈；项目版本提升到 `0.109.0`，更新更新清单测试夹具到 `0.109.1`。
- 验证：目标测试 7 项通过，相邻回归 331 项通过，全量 `unittest` 598 项通过；`/automation-status` smoke 输出当前能力包含 `/hotkey`；真实 `/hotkey` smoke 因会影响当前焦点窗口跳过。
- 打包：安装包构建成功，PyInstaller 出现既有可选 `tzdata` hidden import 警告和 `pyautogui` 依赖侧无阻塞 SyntaxWarning；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.109.0.exe` 已生成，大小 `60,383,232` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.109.0`；打包后 exe smoke 退出码 0 且无残留进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查 376 项通过；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.110.0 鼠标点击自动化第一阶段

- 时间：2026-06-03 继续执行
- 工具：git fetch / git status / Get-Content / rg / update_plan / apply_patch
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：用户已 push 0.109.0 后要求继续；`git fetch origin` 仍遇到 GitHub schannel TLS 握手失败，但 `git status --short --branch` 显示 `main...origin/main` 无 ahead/behind，最新提交为 `f46a271 feat: 增加快捷键自动化 0.109.0`。
- 设计选择：`0.110.0` 先做显式 `/mouse-click x y [button=left|right|middle]`，不做目标识别、拖动、文本输入、窗口切换、应用启动或自然语言自动点击；真实执行复用 `pyautogui`，单元测试通过执行器注入避免真实点击。
- 实现：`automation.py` 新增鼠标点击请求、结果、坐标解析、按钮校验、执行器注入和 `pyautogui.click()` adapter；`JarvisAgent` 新增 `/mouse-click` 命令、帮助文案、运行日志和错误反馈；项目版本提升到 `0.110.0`，更新更新清单测试夹具到 `0.110.1`。
- 验证：目标测试 8 项通过，相邻回归 338 项通过，全量 `unittest` 605 项通过；`/automation-status` smoke 输出当前能力包含 `/mouse-click`；真实 `/mouse-click` smoke 因会影响当前桌面跳过。
- 打包：安装包构建成功，PyInstaller 出现既有可选 `tzdata` hidden import 警告和 `pyautogui` 依赖侧无阻塞 SyntaxWarning；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.110.0.exe` 已生成，大小 `60,383,232` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.110.0`；打包后 exe smoke 退出码 0 且无残留进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查 379 项通过；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。
- 收尾：承接用户已 push 0.109.0 后的后续任务，复验 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` 为 605 项通过，`git diff --check` 退出码 0 且仅 LF/CRLF 提示，`/automation-status` 输出包含 `/mouse-click`，安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.110.0.exe` 当前大小 `60,383,232` 字节；已创建本地提交 `d54e969 feat: 增加鼠标点击自动化 0.110.0`，当前 `main...origin/main [ahead 1]`，按约定未 push。

## 2026-06-03 0.111.0 文本输入自动化第一阶段

- 时间：2026-06-03 继续执行
- 工具：git push / git status / Get-Content / rg / update_plan / apply_patch / unittest / scripts\build_windows_installer.py / Copy-Item / Select-String / Start-Process / git diff --check / Markdown 本地链接检查 / 严格密钥形态扫描 / Test-Path
- 技能：使用 `superpowers:brainstorming` 确定小阶段边界，使用 `superpowers:test-driven-development` 执行 RED/GREEN，使用 `superpowers:verification-before-completion` 做完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD、`unittest`、PyInstaller 打包和本地 smoke 验证。
- 上下文：按用户明确要求先 push 0.110.0，`git push origin main` 成功把 `d54e969` 推送到远端；随后 `git status --short --branch` 显示 `main...origin/main`，公开工作区干净。路线图下一项仍为键鼠自动化基础。
- 设计选择：`0.111.0` 先做显式 `/type-text 文本`，不做目标输入框识别、点击、窗口切换、应用启动或自然语言自动输入；真实执行使用 `pyperclip` 写剪贴板并通过 `pyautogui.hotkey("ctrl", "v")` 粘贴，单元测试通过执行器注入避免真实输入。
- RED：目标测试 7 项先失败；失败点为缺少文本输入 API、Agent 未接入 `describe_text_input_automation`、项目版本仍为 `0.110.0`。
- 实现：`automation.py` 新增 `TextInputRequest`、`TextInputAutomationResult`、文本解析、执行器注入和 pyperclip + pyautogui adapter；`JarvisAgent` 新增 `/type-text` 命令、帮助文案、运行日志和错误反馈；项目版本提升到 `0.111.0`，新增 `pyperclip>=1.9,<2` 依赖，更新更新清单测试夹具到 `0.111.1`。
- GREEN：同一目标命令 7 项通过；相邻回归 344 项通过；全量 `unittest` 611 项通过。
- Smoke：`/automation-status` 输出当前能力包含 `/type-text`；真实 `/type-text` smoke 因会影响当前焦点输入和剪贴板跳过。
- 打包：安装包构建成功，PyInstaller 出现既有可选 `tzdata` hidden import 警告和 `pyautogui` 依赖侧无阻塞 SyntaxWarning；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.111.0.exe` 已生成，大小 `60,387,328` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.111.0`；打包后 exe smoke 退出码 0 且无残留进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查 533 项通过；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.112.0 窗口切换自动化第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / git log / git push / Get-Content / rg / update_plan / apply_patch / unittest
- 技能：使用 `superpowers:brainstorming` 压定小阶段边界，使用 `superpowers:test-driven-development` 执行 RED/GREEN，使用 `superpowers:verification-before-completion` 做提交与完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：按用户明确要求先提交并 push `0.111.0`，`git push origin main` 成功把 `3923c01 feat: 增加文本输入自动化 0.111.0` 推送到远端；随后 `git status --short --branch` 显示 `main...origin/main`，公开工作区干净。
- 设计选择：`0.112.0` 先做显式 `/window-focus 编号或标题/应用名`，复用只读 `/windows` 的窗口快照和 AppRegistry 匹配；匹配到多个窗口时返回候选，不自动切换；不点击、不输入、不启动应用、不接入自然语言自动切换。
- RED：目标测试先失败，缺少 `describe_window_focus`、`select_window_focus_target`，Agent 未暴露 `describe_window_focus`，项目版本仍为 `0.111.0`。
- 实现：`window_state.py` 新增窗口目标选择、`WindowFocusSelection`、`WindowFocusResult`、执行器注入和 Windows `ShowWindow` + `SetForegroundWindow` adapter；`JarvisAgent` 新增 `/window-focus` 命令、帮助文案、运行日志和错误反馈；`automation.py` 的 `/automation-status` 增加 `/window-focus`；项目版本提升到 `0.112.0`，更新更新清单测试夹具到 `0.112.1`。
- GREEN：同一目标命令 11 项通过；相邻回归 336 项通过；全量 `unittest` 618 项通过。
- Smoke：`/automation-status` 输出当前能力包含 `/window-focus`；`/windows` 在当前 Windows 桌面输出 11 个可见窗口并识别前台窗口应用；真实 `/window-focus` smoke 因会改变当前前台窗口跳过。
- 打包：安装包构建成功，PyInstaller 出现既有可选 `tzdata` hidden import 警告和 `pyautogui` 依赖侧无阻塞 SyntaxWarning；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.112.0.exe` 已生成，大小 `60,387,328` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.112.0`；打包后 exe smoke 退出码 0 且无残留进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；首次 Markdown 链接检查因 Git quoted 中文路径误解析失败，改用 `git ls-files -z` 复跑 537 项通过；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.113.0 应用启动自动化第一阶段

- 时间：2026-06-03 继续执行
- 工具：tool_search / git status / git log / Get-Content / rg / update_plan / apply_patch
- 技能：使用 `superpowers:brainstorming` 压定小阶段边界，使用 `superpowers:test-driven-development` 执行 RED/GREEN，使用 `superpowers:verification-before-completion` 做提交与完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`git status --short --branch` 显示 `main...origin/main`，公开工作区干净；最新提交为 `cbd0327 feat: 增加窗口切换自动化 0.112.0`。
- 文档和实现核对：`AppRegistry` 已支持五个首批应用、别名匹配、本地 path 覆盖和 `launch_path`；`JarvisAgent` 已有 `/apps`、`/app-find`、`/window-focus` 相邻命令；`automation.py` 当前能力列表到 `/window-focus`。
- 设计选择：`0.113.0` 先做显式 `/app-launch 应用名称或别名`，只启动已登记且有可用启动路径的应用；不切换窗口、不点击、不输入、不发送快捷键、不接入自然语言自动启动；单元测试通过执行器注入避免真实启动应用。
- RED：目标测试先失败；失败点为缺少 `describe_app_launch`、`launch_registered_app`、Agent 未接入 `describe_app_launch`，项目版本仍为 `0.112.0`。
- 实现：`app_registry.py` 新增 `AppLaunchResult`、`launch_registered_app()`、`describe_app_launch()` 和标准库 `subprocess.Popen()` adapter；`JarvisAgent` 新增 `/app-launch` 命令、帮助文案、运行日志和错误反馈；`automation.py` 的 `/automation-status` 增加 `/app-launch`；项目版本提升到 `0.113.0`，更新更新清单测试夹具到 `0.113.1`。
- GREEN：同一目标扩展相邻断言后 13 项通过；相邻回归 339 项通过；全量 `unittest` 625 项通过。
- Smoke：`/automation-status` 输出当前能力包含 `/app-launch`；`/apps` 输出应用注册表并在当前机器识别 Chrome 路径；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`；真实 `/app-launch` smoke 因会启动本机应用跳过。
- 打包：安装包构建成功，PyInstaller 出现既有可选 `tzdata` hidden import 警告和 `pyautogui` 依赖侧无阻塞 SyntaxWarning；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.113.0.exe` 已生成，大小 `60,387,328` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.113.0`；打包后 exe smoke 退出码 0 且无残留进程。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查 541 项通过；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。
- 调试留痕：首次版本资源脚本校验误查 `windows-installer-stage\JarvisLite.version.txt`；根因确认构建脚本实际输出为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLite.version.txt`，改用真实路径后复验通过。

## 2026-06-03 0.114.0 意图授权层第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / git log / Get-Content / rg / update_plan / apply_patch
- 技能：使用 `superpowers:brainstorming` 压定小阶段边界，使用 `superpowers:test-driven-development` 执行 RED/GREEN，使用 `superpowers:verification-before-completion` 做提交与完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`git status --short --branch` 显示 `main...origin/main`，公开工作区干净；最新提交为 `7c704ae feat: 增加应用启动自动化 0.113.0`。
- 文档核对：`word/PROJECT-PLAN.md` 和 v108 验收方案均显示下一主线为意图授权层。
- 设计选择：`0.114.0` 先做独立授权决策模块和 `/authorization-status` 只读入口；显式 slash command 继续直接执行；自然语言/LLM/建议命令涉及桌面动作时先走准备确认或降级，不新增自然语言自动桌面操作。
- RED：目标测试 6 组先失败；失败点为缺少 `jarvis_lite.authorization`、Agent 未接入 `/authorization-status`、`/status` 与 `/help` 未包含授权层、LLM 桌面动作仍走旧白名单拒绝，版本仍为 `0.113.0`。
- GREEN：目标命令 14 项通过；相邻回归 343 项通过；全量 `unittest` 636 项通过。
- Smoke：`/authorization-status` 输出完整授权层策略；LLM 外脑 `/hotkey ctrl+l` 桌面动作命令被授权层降级且未执行真实快捷键；源码桌面 smoke 输出 `Jarvis Lite 桌面助手` 与 `desktopPetWindow`。
- 打包：安装包构建成功并复制为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.114.0.exe`，大小 `60,395,520` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 exe 版本资源均为 `0.114.0`。
- 调试留痕：直接执行打包后的 GUI 子系统 exe 做 smoke 时 PowerShell 未可靠等待，2 秒进程检查曾命中退出中的 `JarvisLite.exe`；核对 `Win32_Process` 后无残留，改用 `Start-Process -Wait` 复验退出码 0 且 `RunningJarvisAfterSmoke=0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接检查 545 项通过；严格真实密钥形态扫描 16 个公开变更文件无命中；初次广义扫描命中 `tests/test_agent.py` 既有测试假 key，核对 diff 后确认不是本轮新增泄露。

## 2026-06-03 0.115.0 自动记忆与配置管家第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / git log / git push / Get-Content / rg / update_plan / apply_patch
- 技能：使用 `superpowers:brainstorming` 压定小阶段边界，使用 `superpowers:test-driven-development` 执行 RED/GREEN，使用 `superpowers:verification-before-completion` 做提交与完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：按用户明确授权先提交并 push `0.114.0`，第一次推送 GitHub 443 超时，第二次 schannel TLS 握手失败，第三次使用单次 `http.sslBackend=openssl` 推送成功；`git status --short --branch` 显示 `main...origin/main`，公开工作区干净。
- 文档核对：`word/PROJECT-PLAN.md` 与 v108 验收方案显示下一主线为自动记忆与配置管家。
- 设计选择：`0.115.0` 先做统一只读状态和入口提示，不自动保存联系人别名、免确认规则、应用路径或普通聊天内容；配置摘要必须隐藏 API key 原文。
- RED：目标命令 5 组先失败；失败点为缺少 `jarvis_lite.memory_config_manager`、Agent 未接入 `/config-manager-status`、`/status` 与 `/help` 未包含配置管家，版本仍为 `0.114.0`。
- GREEN：目标命令 6 项通过，覆盖空状态、已配置状态、API key 脱敏、Agent 命令别名、`/status`、`/help` 和版本一致性。
- 验证：相邻回归 406 项通过，全量 `unittest` 639 项通过；`/config-manager-status` 与 `/memory-config-status` smoke 输出记忆与配置管家状态；源码桌面 smoke 和打包后 exe smoke 均输出 `desktopPetWindow` 且无残留进程。
- 打包：安装包构建成功，版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.115.0.exe`，大小 `60,399,616` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.115.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接 549 项通过；严格真实密钥形态扫描 19 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.116.0 Chrome 低风险工作流第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / git log / Get-Content / rg / update_plan / apply_patch / unittest / scripts\build_windows_installer.py / Start-Process / git diff --check
- 技能：使用 `superpowers:brainstorming` 压定小阶段边界，使用 `superpowers:test-driven-development` 执行 RED/GREEN，使用 `superpowers:verification-before-completion` 做提交与完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.115.0` 已提交并推送到远端 `main`；v108 推荐顺序显示下一项为 Chrome 和 Clash Verge 低风险工作流。
- 设计选择：`0.116.0` 先做 Chrome 第一阶段显式命令 `/chrome-workflow-status`、`/chrome-open URL` 和 `/chrome-search 关键词`；不读取网页、不点击页面、不输入页面内容、不自动截图、不接入自然语言自动执行；单元测试通过执行器注入避免真实启动 Chrome。
- RED：目标命令 19 项先失败；失败点为缺少 `jarvis_lite.chrome_workflow`、Agent 未接入 Chrome 命令、自动化状态未列出 Chrome 能力、授权层未识别 Chrome 桌面动作、LLM 白名单缺少 `/chrome-workflow-status`，版本仍为 `0.115.0`。
- GREEN：目标命令 26 项通过；相邻回归 417 项通过；全量 `unittest` 653 项通过。
- Smoke：`/chrome-workflow-status` 输出 Chrome 工作流第一阶段状态并识别当前 Chrome 路径；真实 `/chrome-open` 与 `/chrome-search` 因会启动浏览器跳过；源码桌面 smoke 和打包后 exe smoke 均输出 `desktopPetWindow` 且无残留进程。
- 打包：安装包构建成功，版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.116.0.exe`，大小 `60,403,712` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.116.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接 552 项通过；严格真实密钥形态扫描 22 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.117.0 Clash Verge 低风险工作流第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / git log / Get-Content / rg / update_plan / apply_patch
- 技能：使用 `superpowers:brainstorming` 压定小阶段边界，使用 `superpowers:test-driven-development` 准备 RED/GREEN，使用 `superpowers:verification-before-completion` 做提交与完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.116.0` 已提交并推送到远端 `main`，提交 `1c87fdd feat: 增加 Chrome 低风险工作流 0.116.0`；工作区公开文件干净。
- 设计选择：`0.117.0` 先做 Clash Verge 第一阶段显式命令 `/clash-workflow-status`、`/clash-open` 和 `/clash-focus`；不切换节点、不开关系统代理、不修改配置、不点击、不输入、不接入自然语言自动执行；单元测试通过执行器和窗口快照注入避免真实启动或切换窗口。
- RED：目标命令 20 项先失败；失败点为缺少 `jarvis_lite.clash_workflow`、Agent 未接入 Clash 命令、自动化状态未列出 Clash 能力、授权层未识别 Clash 桌面动作、LLM 白名单缺少 `/clash-workflow-status`，版本仍为 `0.116.0`。
- GREEN：目标命令 25 项通过；相邻回归 429 项通过；全量 `unittest` 666 项通过。
- Smoke：`/clash-workflow-status` 输出 Clash Verge 工作流第一阶段状态和边界；真实 `/clash-open` 与 `/clash-focus` 因会启动或切换本机应用跳过；源码桌面 smoke 和打包后 exe smoke 均输出 `desktopPetWindow` 且无残留进程。
- 打包：安装包构建成功，版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.117.0.exe`，大小 `60,403,712` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.117.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接 554 项通过；严格真实密钥形态扫描 22 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.118.0 QQ/微信准备式工作流第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / git log / rg / update_plan / apply_patch
- 技能：使用 `superpowers:brainstorming` 压定小阶段边界，使用 `superpowers:test-driven-development` 准备 RED/GREEN，使用 `superpowers:verification-before-completion` 做提交与完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.117.0` 已提交并推送到远端 `main`，提交 `170d533 feat: 增加 Clash Verge 低风险工作流 0.117.0`；工作区公开文件干净。
- 设计选择：`0.118.0` 先做 QQ/微信第一阶段显式命令 `/messaging-workflow-status`、`/qq-open`、`/qq-focus`、`/qq-prepare-message 联系人 => 消息`、`/wechat-open`、`/wechat-focus` 和 `/wechat-prepare-message 联系人 => 消息`；准备消息只生成本地准备单，不查找真实联系人、不点击、不输入、不发送消息、不接入自然语言自动执行。
- RED：目标命令先失败；失败点为缺少 `jarvis_lite.messaging_workflow`、Agent 未接入消息工作流命令、自动化状态未列出消息能力、授权层未识别 QQ/微信打开与聚焦动作、LLM 白名单缺少 `/messaging-workflow-status`，版本仍为 `0.117.0`。
- GREEN：目标命令 29 项通过；相邻回归 440 项通过；全量 `unittest` 683 项通过。
- Smoke：`/messaging-workflow-status` 输出 QQ/微信准备式工作流第一阶段状态和边界；真实 QQ/微信打开与聚焦因会启动或切换本机应用跳过；源码桌面 smoke 和打包后 exe smoke 均输出 `desktopPetWindow`，打包后无残留 `JarvisLite.exe`。
- 打包：安装包构建成功，版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.118.0.exe`，大小 `60,411,904` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.118.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 工作区换行提示；Markdown 本地链接 652 项通过；严格密钥形态扫描无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。
- 文档：公开验证记录、周/月索引和进度记录已补齐到 `0.118.0`；`.codex/testing.md` 与 `.codex/review-report.md` 仅本地留痕，不进入提交。

## 2026-06-03 0.119.0 IDEA 项目状态第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / git log / Get-Content / rg / update_plan / apply_patch / unittest / scripts\build_windows_installer.py / Start-Process
- 技能：使用 `superpowers:brainstorming` 压定小阶段边界，使用 `superpowers:test-driven-development` 执行 RED/GREEN，使用 `superpowers:verification-before-completion` 做提交与完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.118.0` 已提交并推送到远端 `main`，提交 `e5f52f7 feat: 增加 QQ 微信准备式工作流 0.118.0`；工作区公开文件干净。
- 设计选择：`0.119.0` 先做 IDEA 第一阶段显式命令 `/idea-workflow-status`、`/idea-open`、`/idea-focus`、`/idea-open-project 项目路径` 和 `/idea-project-status [项目路径]`；项目状态只读检查目录标记，不运行测试、不打开终端、不点击、不输入、不编辑项目文件、不接入自然语言自动执行。
- RED：目标命令先失败；失败点为缺少 `jarvis_lite.idea_workflow`、Agent 未接入 IDEA 命令、自动化状态未列出 IDEA 能力、授权层未识别 IDEA 打开/聚焦/打开项目动作、LLM 白名单缺少 `/idea-workflow-status`，版本仍为 `0.118.0`。
- GREEN：目标命令 24 项通过；相邻回归 451 项通过；全量 `unittest` 702 项通过。
- Smoke：`/idea-workflow-status` 输出 IDEA 工作流第一阶段状态和边界；`/idea-project-status` 只读识别当前仓库 `.idea`、`.git` 与 `pyproject.toml`；真实 IDEA 打开、聚焦和打开项目因会启动或切换本机应用跳过；源码桌面 smoke 和打包后 exe smoke 均输出 `desktopPetWindow`，打包后无残留 `JarvisLite.exe`。
- 打包：安装包构建成功，版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.119.0.exe`，大小 `60,416,000` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.119.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接检查改用 `git ls-files -z` 复跑通过，559 项通过；严格真实密钥形态扫描排除测试假值前缀后无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。
- 文档：README、PROJECT-PLAN、v124 计划、方案索引、文档索引、公开验证记录、周/月索引和进度记录已补齐到 `0.119.0`；`.codex/testing.md` 与 `.codex/review-report.md` 仅本地留痕，不进入提交。

## 2026-06-03 0.120.0 任务状态与失败复盘第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / rg / Get-Content / update_plan / apply_patch
- 技能：使用 `superpowers:brainstorming` 压定小阶段边界，使用 `superpowers:writing-plans` 产出 v125 计划，后续使用 `superpowers:test-driven-development` 执行 RED/GREEN，提交前使用 `superpowers:verification-before-completion`。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.119.0` 已提交并推送到远端 `main`，提交 `f68840d feat: 增加 IDEA 项目状态 0.119.0`；工作区公开文件干净。
- 设计选择：`0.120.0` 先做显式任务状态命令和运行态持久化，记录当前任务、步骤、失败原因和复盘占位；不自动截图、不自动 OCR、不自动重新执行外部动作，不接入自然语言自动任务编排。
- 实现：新增 `task_state.py`、运行态任务上下文、Agent 任务状态命令、`/help`、`/status`、`/recent-context` 和 LLM 状态命令白名单；版本提升到 `0.120.0`。
- 验证：目标 GREEN 9 项通过，相邻回归 425 项通过，全量 `unittest` 710 项通过；`/task-status`、start/cancel、临时项目失败复盘、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.120.0.exe`，大小 `60,424,192` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.120.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 562 项通过；严格密钥形态扫描 15 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.121.0 任务失败截图 OCR 复盘第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / rg / Get-Content / update_plan / apply_patch / unittest / scripts\build_windows_installer.py / Start-Process
- 技能：使用 `superpowers:executing-plans` 承接 v126 计划，使用 `superpowers:verification-before-completion` 做提交与完成前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 既有记录和 `unittest`。
- 上下文：`0.120.0` 已提交并推送到远端 `main`，提交 `2f46053 feat: 增加任务状态失败复盘 0.120.0`；工作区处于 `0.121.0` 半完成状态，代码和目标测试已有一轮通过，公开验证文档尚未补齐。
- 设计选择：`0.121.0` 只新增显式 `/task-fail-capture 失败原因 [lang=chi_sim+eng]`，在已有当前任务时保存截图并尝试 OCR，把截图路径、尺寸、OCR 文本或 OCR 失败诊断写入失败复盘；不自动重新执行外部动作、不点击、不输入，不接入自然语言自动任务编排；真实命令 smoke 因会保存当前屏幕截图而跳过。
- 实现：`task_state.py` 新增 `record_task_failure_with_screen_ocr()`；`JarvisAgent` 接入 `/task-fail-capture`、帮助和状态文案；LLM 白名单仍只允许 `/task-status`，不允许 `/task-fail-capture`；版本提升到 `0.121.0`。
- 验证：目标 GREEN 9 项通过，相邻回归 435 项通过，全量 `unittest` 713 项通过；`/task-status` smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.121.0.exe`，大小 `60,424,192` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.121.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 565 项通过；严格密钥形态扫描 12 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.122.0 记忆与配置候选池第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / rg / Get-Content / update_plan / apply_patch / unittest / src\app.py smoke / scripts\build_windows_installer.py / PowerShell 版本资源检查
- 技能：使用 `superpowers:executing-plans` 承接 v127 计划，使用 `superpowers:test-driven-development` 延续已验证 RED 测试，使用 `superpowers:verification-before-completion` 做提交前验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.121.0` 已提交并推送到远端 `main`，提交 `f1276c7 feat: 增加任务失败截图复盘 0.121.0`；工作区包含 v127 RED 测试和方案文档。
- 设计选择：候选池复用 `jarvis-lite-runtime/agent-context.json`，只保存运行态候选；显式 `/config-candidate-add 类型 内容` 写入候选、`/config-candidates` 查看、`/config-candidate-dismiss 编号` 忽略；不自动写长期记忆、目录、应用配置、联系人或授权规则，不加入 LLM 白名单。
- 实现：`runtime_context.py` 新增 `RuntimeMemoryConfigCandidateContext` 和 `memory_config_candidates` 序列化；新增 `memory_config_candidates.py` 负责类型归一、重复合并、忽略和统计；`memory_config_manager.py` 展示候选统计；`JarvisAgent` 接入候选命令、帮助、状态和运行态保留；版本提升到 `0.122.0`。
- 调试留痕：目标测试首轮 GREEN 前，`test_describe_memory_config_manager_reports_empty_storage` 被运行态候选污染；根因是测试项目根使用 `temp_dir` 时 runtime 文件落在 `temp_dir.parent/jarvis-lite-runtime`，跨测试共享。修正为 `temp_dir/jarvis-lite` 后目标测试通过。
- 验证：目标 GREEN 9 项通过，相邻回归 411 项通过，全量 `unittest` 718 项通过；`/config-candidates` 与 `/config-manager-status` smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.122.0.exe`，大小 `60,432,384` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.122.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 569 项通过；初次广义密钥扫描命中历史方案文件名 `sk-...` slug 假阳性，严格真实密钥形态复跑 16 个公开变更文件无命中；本地敏感配置文件不存在。

## 2026-06-03 0.123.0 记忆与配置候选固化第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / rg / Get-Content / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Start-Process / git diff --check
- 技能：使用 `superpowers:using-superpowers` 选择流程，使用 `superpowers:writing-plans` 产出 v128 计划，使用 `superpowers:test-driven-development` 执行 RED/GREEN，遇到相邻回归失败后使用 `superpowers:systematic-debugging` 查明根因，提交前使用 `superpowers:verification-before-completion`。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.122.0` 已本地提交为 `e3b7cc6 feat: 增加记忆配置候选池 0.122.0`；推送 `origin/main` 连续失败，`schannel` 报 TLS 握手失败，使用 `http.sslBackend=openssl` 重试后 GitHub 443 超时，先继续后续阶段。
- 设计选择：新增显式 `/config-candidate-apply 编号` 固化低风险候选；只固化 `memory`、`experience` 和 `directory`，分别复用既有长期记忆、经验记忆和常用目录登记逻辑；联系人别名、授权规则、应用别名、偏好和其他候选保持活跃并返回边界说明；不加入 LLM 白名单，不从普通聊天自动写入长期配置。
- RED：目标测试先失败；失败点为缺少 `apply_memory_config_candidate`、Agent 未接入 `/config-candidate-apply`、项目元数据仍为 `0.122.0`；补充候选列表固化入口提示时先添加断言并确认缺少 `/config-candidate-apply 编号` 后再补实现。
- 实现：`memory_config_candidates.py` 新增 `apply_memory_config_candidate()`、目录候选解析、低风险固化和 unsupported 类型拒绝；`runtime_context.py` 允许 `applied` 状态重启后保留；`JarvisAgent` 接入 `/config-candidate-apply`、帮助和状态；版本提升到 `0.123.0`。
- 调试留痕：相邻回归首次失败在更新检查 Agent 测试，根因是测试 manifest 仍写 `0.122.1`，当前版本升到 `0.123.0` 后不再表示可用新版本；将测试夹具提升为 `0.123.1` 后复跑通过。
- 验证：目标 GREEN 11 项通过，相邻回归 417 项通过，全量 `unittest` 724 项通过；临时项目命令 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.123.0.exe`，大小 `60,436,480` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.123.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 415 项通过；严格真实密钥形态扫描 15 个公开变更文件无命中；本地敏感配置文件不存在。
- 提交与推送：`0.123.0` 本地提交 `80b8ef7 feat: 增加记忆配置候选固化 0.123.0` 已创建；`git push origin main` 失败，错误为 GitHub HTTPS `schannel` 握手失败；`git -c http.sslBackend=openssl push origin main` 失败，错误为 GitHub 443 超时；`Invoke-WebRequest https://github.com -Method Head` 返回 200，判断为 Git 传输通道不稳定，本地分支领先远程 2 个提交后继续执行下一阶段。

## 2026-06-03 0.124.0 任务状态自动采集第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / Get-Content / rg / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Start-Process / git diff --check
- 技能：使用 `superpowers:using-superpowers` 选择流程，使用 `superpowers:test-driven-development` 执行 RED/GREEN，使用 `superpowers:verification-before-completion` 做提交前验证；`superpowers:brainstorming` 的人工审批门与用户“继续执行、无需等待”冲突，只保留上下文探索和方案取舍。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.123.0` 已本地提交但 push 失败；`word/PROJECT-PLAN.md` 与 `word/progress/2026-06-03.md` 指向任务状态自动采集、失败复盘深化和更高风险候选确认/撤销闭环。
- 设计选择：`0.124.0` 只自动采集当前任务运行中的最近路由事件，内容为输入原话、路由类型、命令/意图详情、摘要、依据和时间；`/task-status` 展示最近任务事件，`/task-fail` 与 `/task-fail-capture` 复制这些事件到失败复盘；不采集执行结果全文、不截图、不 OCR、不重放外部动作。
- RED：目标测试先失败；失败点为缺少 `record_task_route_event`、失败复盘缺少“自动采集上下文”、项目元数据仍为 `0.123.0`。
- 实现：`runtime_context.py` 新增 `RuntimeTaskEventContext` 和任务/失败记录的 `recent_events` 序列化；`task_state.py` 新增任务路由事件写入、状态展示和失败复盘展示；`JarvisAgent._remember_route_decision()` 在当前任务运行中自动写入普通路由事件，并过滤 `/task-*` 管理命令；版本提升到 `0.124.0`。
- 验证：目标 GREEN 3 项通过；相邻回归 417 项通过；全量 `unittest` 726 项通过；临时项目命令 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.124.0.exe`，大小 `60,436,480` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.124.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 419 项通过；严格真实密钥形态扫描 17 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.125.0 任务执行结果摘要采集第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / Get-Content / rg / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Start-Process / git diff --check
- 技能：使用 `superpowers:using-superpowers` 选择流程，沿用 `superpowers:test-driven-development` 的既有 RED/GREEN 链路，临时 smoke 断言失败后使用 `superpowers:systematic-debugging` 查明根因，提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.124.0` 已提交并 push 到 `origin/main`；`word/PROJECT-PLAN.md` 和进度记录指向任务执行结果采集、截图/OCR 失败上下文深化和候选确认/撤销闭环。
- 设计选择：`0.125.0` 只在显式 slash command 分支返回后，把紧凑结果摘要写回当前任务最近匹配的任务事件；不重构 `JarvisAgent.handle()` 全部返回路径，不采集全文输出，不截图、不 OCR、不重放外部动作。
- RED：目标测试先失败；失败点为缺少 `record_task_event_result`、失败复盘仍显示 `结果：显式命令`、项目元数据仍为 `0.124.0`。
- 实现：`task_state.py` 新增 `record_task_event_result()` 和结果压缩；`JarvisAgent.handle()` 显式命令分支在 `_handle_command()` 返回后写回结果摘要；版本提升到 `0.125.0`；新增 v130 方案并同步 README、PROJECT-PLAN、方案索引、文档索引、进度和验证记录。
- 调试留痕：临时项目 smoke 首次失败，因为脚本把 `/task-fail` 响应标题“自动采集上下文”套用到 `/task-status`；根因是 smoke 断言与实际接口文案不一致，产品输出中的“最近任务事件”和最近失败记录“自动采集”均包含结果摘要，修正 smoke 断言后复跑通过。
- 验证：目标 GREEN 3 项通过；相邻回归 418 项通过；全量 `unittest` 727 项通过；临时项目命令 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.125.0.exe`，大小 `60,436,480` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.125.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 583 项通过；首次广义密钥扫描命中 Markdown 文件名 slug 假阳性，收紧真实 key 形态后 17 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.126.0 任务失败复盘行动建议第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / Get-Content / rg / update_plan / apply_patch / unittest / scripts\build_windows_installer.py / Start-Process / PowerShell 版本资源检查 / git diff --check
- 技能：使用 `superpowers:using-superpowers` 选择流程，沿用 `superpowers:test-driven-development` 的 RED/GREEN 记录，使用 `superpowers:verification-before-completion` 做提交前新鲜验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.125.0` 已提交并 push 到 `origin/main`；`0.126.0` 的代码、测试和公开文档处于未提交状态，目标是补强普通失败复盘的下一步建议。
- 设计选择：普通 `/task-fail 失败原因` 如果失败记录仍是默认屏幕上下文，则下一步建议前置 `补充截图/OCR：/task-fail-capture 失败原因`；已有截图/OCR 上下文的失败继续只提示恢复任务，避免自我重复建议。
- RED：目标测试先失败；失败点为普通失败复盘和 `/task-status` 最近失败记录仍只显示通用恢复建议，项目元数据仍为 `0.125.0`；截图/OCR 分支不重复建议测试作为边界覆盖。
- 实现：`task_state.py` 新增 `_failure_next_step()` 并让 `record_task_failure()` 使用动态下一步建议；版本提升到 `0.126.0`；README、PROJECT-PLAN、v131 计划、计划索引、文档索引、进度和验证记录同步。
- 验证：目标 GREEN 4 项通过；相邻回归 418 项通过；当前会话复跑全量 `unittest` 727 项通过；临时项目 smoke、fake capturer/OCR 失败记录 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.126.0.exe`，大小 `60,436,480` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.126.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 588 项通过；严格真实密钥形态扫描 16 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。
- 提交与推送：`0.126.0` 本地提交 `2e81819 feat: 增强任务失败复盘建议 0.126.0` 已创建；`git push origin main` 失败，错误为 GitHub HTTPS `schannel` 握手失败；`git -c http.sslBackend=openssl push origin main` 和 `git -c http.sslBackend=openssl -c http.version=HTTP/1.1 push origin main` 均因 GitHub 443 超时失败；`Test-NetConnection github.com -Port 443` 成功，`Invoke-WebRequest https://github.com -Method Head` 返回 200，判断为 Git 传输通道不稳定；SSH 未配置 host key，不自动修改 `known_hosts`。

## 2026-06-03 0.127.0 任务失败复盘样本建议第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / Get-Content / rg / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Start-Process / PowerShell 版本资源检查 / git diff --check
- 技能：使用 `superpowers:using-superpowers` 选择流程，沿用 `superpowers:test-driven-development` 的 RED/GREEN 链路，临时 smoke 发现状态边界缺口后使用 `superpowers:systematic-debugging` 查明根因，提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 设计选择：只把当前任务最近显式命令事件格式化为可复制的 `/inner-brain-eval-add 原始输入 => /命令` 建议；失败复盘和 `/task-status` 最近失败记录均展示建议与样本建议边界；不自动写入 evaluation、不训练、不重放外部动作。
- RED：目标测试先失败；失败点为带显式命令事件的失败复盘缺少样本建议、项目元数据仍为 `0.126.0`；临时项目 smoke 进一步暴露 `/task-status` 最近失败记录缺少样本建议边界，补充 RED 断言后确认失败。
- 实现：`task_state.py` 新增任务事件到 evaluation 建议的格式化 helper，并让失败复盘和最近失败记录复用；`/task-status` 最近失败记录补充样本建议边界；版本提升到 `0.127.0`；README、PROJECT-PLAN、v132 计划、计划索引、文档索引、进度和验证记录同步。
- 验证：目标 GREEN 5 项通过；相邻回归 418 项通过；全量 `unittest` 727 项通过；临时项目 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.127.0.exe`，大小 `60,440,576` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.127.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 593 项通过；严格真实密钥形态扫描 16 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。
- 提交与推送：`0.127.0` 本地提交 `ddd1450 feat: 增强任务失败复盘样本建议 0.127.0` 已创建；`git push origin main` 成功，将 `0.126.0` 与 `0.127.0` 本地队列一起推送到远端，输出 `035f237..ddd1450 main -> main`。

## 2026-06-03 0.128.0 记忆与配置候选恢复第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / Get-Content / rg / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Start-Process / PowerShell 版本资源检查 / git diff --check
- 技能：使用 `superpowers:using-superpowers` 选择流程，使用 `superpowers:executing-plans` 执行既有 v133 计划，临时 smoke 脚本断言失败后使用 `superpowers:systematic-debugging` 查明根因，提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 设计选择：新增 `/config-candidate-history` 只读展示已忽略或已固化候选；新增 `/config-candidate-restore 编号` 将历史候选恢复为 active；恢复只改变运行态候选状态，不自动删除已经写入的长期记忆、经验记忆或常用目录，不写高风险配置，不加入 LLM 白名单。
- RED：目标测试先失败；失败点为缺少 `describe_memory_config_candidate_history` 和 `restore_memory_config_candidate`、Agent 未接入 `/config-candidate-history`、项目元数据仍为 `0.127.0`。
- 实现：`memory_config_candidates.py` 新增历史候选描述、历史编号映射和恢复 helper；`JarvisAgent` 接入历史查看、恢复命令、帮助和状态；版本提升到 `0.128.0`；README、PROJECT-PLAN、v133 计划、计划索引、文档索引、进度和验证记录同步。
- 调试留痕：临时项目 smoke 首次失败，因为脚本把 `CommonDirectory.path` 当作字符串比较；根因是目录对象内保存为 `WindowsPath`，产品功能已写入正确路径，修正 smoke 断言后复跑通过。
- 验证：目标 GREEN 11 项通过；相邻回归 421 项通过；全量 `unittest` 730 项通过；临时项目 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.128.0.exe`，大小 `60,440,576` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.128.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 598 项通过；严格真实密钥形态扫描 18 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-03 0.129.0 高风险记忆与配置候选确认草稿第一阶段

- 时间：2026-06-03 继续执行
- 工具：git status / Get-Content / rg / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Start-Process / PowerShell 版本资源检查 / git diff --check
- 技能：使用 `superpowers:brainstorming` 做最小设计梳理，因用户明确要求继续执行不等待，确认步骤折叠为本地设计审查；使用 `superpowers:writing-plans` 产出 v134 计划，使用 `superpowers:test-driven-development` 执行 RED/GREEN，相邻回归失败后使用 `superpowers:systematic-debugging` 查明根因，提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 设计选择：不新增长期联系人、授权、应用别名或偏好存储；不新增真实确认固化命令；只让现有 `/config-candidate-apply 编号` 对高风险候选返回确认草稿、撤销入口和不写入长期配置边界，候选保持 active。
- RED：目标测试先失败；失败点为联系人别名和授权规则候选仍输出旧“暂不支持”文案，项目元数据仍为 `0.128.0`。
- 实现：`memory_config_candidates.py` 新增高风险候选集合和 `_confirmation_draft_message()`；`apply_memory_config_candidate()` 在低风险固化前识别高风险候选并返回草稿，不改变候选状态；版本提升到 `0.129.0`；README、PROJECT-PLAN、v134 计划、计划索引、文档索引、进度和验证记录同步。
- 调试留痕：相邻回归首次失败在更新检查 Agent 测试，根因是测试 manifest 仍写 `0.128.1`，当前版本升到 `0.129.0` 后不再表示可用新版本；将测试夹具提升为 `0.129.1` 后复跑通过。
- 验证：目标 GREEN 12 项通过；相邻回归 422 项通过；全量 `unittest` 731 项通过；临时项目 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.129.0.exe`，大小 `60,440,576` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.129.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 603 项通过；严格真实密钥形态扫描 16 个公开变更文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-04 0.130.0 任务失败复盘窗口与授权摘要第一阶段

- 时间：2026-06-04 继续执行
- 工具：git status / Get-Content / rg / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Start-Process / PowerShell 版本资源检查 / git diff --check
- 技能：使用 `superpowers:using-superpowers` 选择流程，使用 `superpowers:executing-plans` 执行既有 v135 计划，提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 既有记录和 `unittest`。
- 上下文：`日志.txt` 显示 `0.129.0` 已提交并 push 到 `origin/main`，断线点位于“识别并启动下一阶段”；本轮接续 v135 任务失败复盘窗口与授权摘要第一阶段。
- 设计选择：复用现有 `capture_window_snapshot()`，新增紧凑只读前台窗口摘要；失败复盘和 `/task-status` 展示窗口、路由与授权摘要；普通 `/task-fail` 不自动截图/OCR，不切换窗口、不点击、不输入、不自动重放外部动作。
- RED：目标测试先失败；失败点为缺少 `describe_task_window_context()`、任务失败运行态缺少 `window_context`、Agent 未传递窗口上下文、项目元数据仍为 `0.129.0`。
- 实现：`window_state.py` 新增 `describe_task_window_context()`；`RuntimeTaskFailureContext` 增加 `window_context` JSON 读写；`record_task_failure()` 与 `record_task_failure_with_screen_ocr()` 接收并展示窗口上下文；Agent `/task-fail` 与 `/task-fail-capture` 传入当前窗口摘要；版本提升到 `0.130.0`；README、PROJECT-PLAN、v135 计划、计划索引、文档索引、进度和验证记录同步。
- 验证：目标 GREEN 5 项通过；相邻回归 429 项通过；全量 `unittest` 734 项通过；临时项目命令 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.130.0.exe`，大小 `60,440,576` 字节；安装脚本、SED、版本资源和 exe 版本信息均为 `0.130.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 612 项通过；严格真实密钥形态扫描 20 个公开变更/新增文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-04 0.131.0 联系人别名确认固化与撤销第一阶段

- 时间：2026-06-04 继续执行
- 工具：git status / Get-Content / rg / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Start-Process / PowerShell 版本资源检查 / git diff --check
- 技能：使用 `superpowers:using-superpowers` 选择流程，使用 `superpowers:executing-plans` 执行既有 v136 计划，使用 `superpowers:test-driven-development` 承接已确认失败的 RED 测试，测试断言时间点失败后使用 `superpowers:systematic-debugging` 查明根因，提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.130.0` 已完成并推送到 `origin/main`；v136 计划明确只做联系人别名真实确认固化与撤销，不扩展授权规则、应用别名或偏好，不查找真实联系人、不发送消息。
- 设计选择：新增 `contacts.py` 作为 `config/contacts.local.json` 唯一读写入口；`/config-candidate-confirm 编号` 只确认活跃 `contact_alias`，`/config-candidate-undo 编号` 只撤销历史中 `applied` 的 `contact_alias`；其他高风险候选保持草稿或暂不支持。
- RED：目标测试先失败；失败点为缺少 `jarvis_lite.contacts`、Agent 未接入 `/config-candidate-confirm` 和 `/config-candidate-undo`、确认草稿缺少确认固化入口、版本仍为 `0.130.0`。
- 调试留痕：目标 GREEN 首次剩余 `tests/test_contacts.py` 失败，根因为测试在 `remove_contact_alias()` 之后才断言保存后数量为 1；同类问题也存在于候选确认测试的采样时间点，修正为删除前采样后复跑通过。敏感信息扫描首次命中 Markdown 文件名 slug 中的 `sk-...` 假阳性，收紧真实 key 形态后复跑通过。
- 实现：`contacts.py` 新增联系人别名解析、读写、删除、计数和描述；`memory_config_candidates.py` 新增确认/撤销 helper，确认草稿增加 `/config-candidate-confirm`，候选历史增加撤销提示；`memory_config_manager.py` 增加联系人别名计数；`JarvisAgent` 接入显式确认/撤销命令、帮助和状态；版本提升到 `0.131.0`；README、PROJECT-PLAN、v136 计划、计划索引、文档索引、进度和验证记录同步。
- 验证：目标 GREEN 12 项通过；相邻回归 428 项通过；全量 `unittest` 739 项通过；临时项目联系人别名 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 打包：版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.131.0.exe`，大小 `60,448,768` 字节；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.131.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 616 项通过；严格真实密钥形态扫描 21 个公开变更/新增文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-04 0.132.0 应用别名确认固化与撤销第一阶段

- 时间：2026-06-04 继续执行
- 工具：git status / git log / Get-Content / rg / Select-String / update_plan / apply_patch / unittest（后续补充）
- 技能：使用 `superpowers:using-superpowers` 选择流程，使用 `superpowers:brainstorming` 做最小设计梳理，因 AGENTS 明确要求默认自主执行不等待确认；使用 `superpowers:writing-plans` 按项目文档计划降级；使用 `superpowers:test-driven-development` 执行 RED/GREEN。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`word/PROJECT-PLAN.md` 指向继续实现更高风险候选真实确认固化与撤销闭环，下一批优先应用别名或授权规则；选择应用别名，因为已有 `config/apps.local.json` 与 AppRegistry 读写模式，风险面小于授权规则。
- 设计选择：`app_alias` 候选格式为 `别名 => 应用标识或已登记应用名`，兼容 `->` 和 `=`；确认时只把别名写入 `config/apps.local.json` 的 `apps.<app_id>.aliases`，撤销时只删除该别名，不删除已有 path 覆盖，不启动应用，不切换窗口、不点击、不输入。
- RED：目标测试先失败；失败点为缺少应用别名解析/写入/删除 helper、候选确认暂不支持 `app_alias`、Agent 尚未接入应用别名确认/撤销、版本仍为 `0.131.0`。
- 调试留痕：命令行 smoke 首次暴露 `_read_local_registry_payload()` 中循环变量遮蔽顶层 payload，撤销应用别名后可能把 `aliases` 或 `path` 写到 JSON 根节点；改名为 `app_payload` 并增加 JSON 结构断言后复跑通过。
- 实现：`app_registry.py` 新增应用别名候选解析、保存和删除 helper；`memory_config_candidates.py` 让确认/撤销同时支持 `contact_alias` 与 `app_alias`；`JarvisAgent` 帮助和状态文案更新为联系人/应用别名；版本提升到 `0.132.0`；README、PROJECT-PLAN、v137 计划、计划索引、文档索引、进度和验证记录同步。
- 验证：目标 GREEN 6 项通过；相邻回归 437 项通过；全量 `unittest` 743 项通过；临时项目应用别名 smoke、源码桌面 smoke、安装包构建和打包后 smoke 通过。
- 验证脚本留痕：打包后 smoke 前两次失败在 PowerShell 包装脚本输出展示阶段，根因是空 stderr 通过 `Get-Content -Raw` 后仍可能为空值并触发 `.Trim()`；程序 stdout 已包含 `desktopPetWindow`、stderr 为空且无残留进程。改用 `System.IO.File.ReadAllText()` 和布尔断言后复跑通过。
- 打包：最终源码变更后重跑安装包构建时，工具包装在 IExpress 阶段超时；检查进程发现 `iexpress`/`makecab` 仍在运行，等待后产物刷新。版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.132.0.exe`，大小 `60,448,768` 字节，时间戳 `2026/6/4 14:11:28`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.132.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 620 项通过；严格真实密钥形态扫描 19 个公开变更/新增文件无命中；本地敏感配置文件不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-04 0.132.0 断线后执行结果复核

- 时间：2026-06-04 用户要求复核 `日志.txt` 中断线后继续完成的执行是否按方案落地。
- 工具：Get-Content / rg / git log / git show / git rev-parse / unittest / 临时项目 Agent smoke / git diff --check / Get-Item / update_plan。
- 工具降级：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`、`Get-Content`、`git` 和 `unittest`。
- 日志核对：`日志.txt` 尾部显示 0.132.0 已提交 `8db0ed7 feat: 增加应用别名确认固化 0.132.0` 并成功推送，最终 `git status --short --branch` 为 `## main...origin/main`。
- 计划对照：`.codex/v137-app-alias-confirmation-plan.md` 和 `word/plans/2026-06-04-v137-app-alias-confirmation-plan.md` 要求 app_alias 显式确认写入 `config/apps.local.json` 的 `apps.<app_id>.aliases`、撤销删除对应别名并恢复候选、不启动应用、不加入 LLM 白名单；当前代码和测试均覆盖这些项。
- 代码核对：`app_registry.py` 提供 `parse_app_alias_candidate()`、`save_app_alias()`、`remove_app_alias()`，撤销保留同一应用已有 `path` 等覆盖；`memory_config_candidates.py` 的 confirm/undo 分支支持 `contact_alias` 与 `app_alias`，其他高风险类型仍不真实固化。
- 白名单核对：`tests/test_llm.py` 明确断言 OpenAI provider instructions 不包含 `/config-candidate-confirm` 和 `/config-candidate-undo`。
- 新鲜验证：目标与白名单回归 7 项通过；`python -m unittest discover -s tests` 重新运行 743 项通过；临时项目 smoke 通过 apply 草稿、confirm、`/app-find` 命中、undo、撤销后 `/app-find` 不命中、候选恢复活跃；`git diff --check` 退出码 0。
- 状态核对：`HEAD` 与 `origin/main` 均为 `8db0ed71bde9bc6b1ed91e6538acb308468ebacc`；安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.132.0.exe` 存在，大小 `60448768` 字节，时间戳 `2026/6/4 14:11:28`。

## 2026-06-05 0.133.0 授权规则确认固化与撤销第一阶段

- 时间：2026-06-05 继续执行。
- 工具：Get-Content / rg / git status / git diff / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Select-String / PowerShell 版本资源检查 / git diff --check。
- 技能：使用 `superpowers:using-superpowers` 选择流程，提交前使用 `superpowers:verification-before-completion` 做新鲜验证；延续上一轮 `superpowers:test-driven-development` 的 RED/GREEN 证据。
- 工具降级：当前会话仍未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- skill 影响核对：`日志.txt` 显示 Codex 启动时报告 `C:\Users\hp\.codex\skills\urban-life-novel-writing\SKILL.md` 的 YAML `description` 类型错误；复核 `git status` 和 `日志.txt` 后确认这是用户目录 skill 元数据警告，未修改本项目仓库文件。
- 上下文：`0.132.0` 已提交并推送到 `origin/main`，提交为 `8db0ed7 feat: 增加应用别名确认固化 0.132.0`；本阶段承接高风险候选显式确认固化与撤销闭环，优先处理授权规则候选。
- 设计选择：新增 `authorization_rules.py` 统一读写 `config/authorization.local.json`；`authorization_rule` 候选确认只保存规则文本并标记候选已固化，撤销只删除对应规则并恢复候选活跃；`/authorization-status` 和配置管家只读展示本地授权规则。当前阶段不改变 `authorize_intent_execution()` 决策，不把确认/撤销命令加入 LLM 白名单。
- RED：目标命令先失败，失败点为缺少 `jarvis_lite.authorization_rules`、候选确认暂不支持 `authorization_rule`、Agent 仍返回暂不支持、版本仍为 `0.132.0`。
- GREEN：同一目标命令 27 项通过；配置管家 `/authorization-status` 管理入口补 RED 后复跑通过。
- 调试留痕：相邻回归首次失败在更新检查 Agent 测试，根因是 manifest 夹具仍写 `0.132.1`，当前版本升到 `0.133.0` 后不再表示新版本；将夹具提升为 `0.133.1` 后复跑通过。安装包元数据首次按仓库内旧路径检查失败，定位到实际生成路径 `E:\oyzj\ai\jarvis-lite-dist\windows-installer-stage\install.cmd`、`E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.sed` 和 `E:\oyzj\ai\jarvis-lite-dist\JarvisLite.version.txt` 后复验通过。
- 验证：相邻回归 440 项通过；全量 `unittest` 当前会话复跑 746 项通过；临时项目授权规则确认/撤销 smoke 输出 `authorization-rule-smoke OK`；源码桌面 smoke 和打包后 smoke 均输出 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.133.0.exe`，大小 `60,452,864` 字节，时间戳 `2026/6/5 10:26:50`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.133.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 630 项通过；严格真实密钥形态扫描 23 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-05 0.134.0 偏好确认固化与撤销第一阶段

- 时间：2026-06-05 继续执行。
- 工具：Get-Content / rg / git status / git diff / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Select-String / PowerShell 版本资源检查 / git diff --check / Markdown 本地链接检查 / 严格真实密钥形态扫描。
- 技能：使用 `superpowers:using-superpowers` 选择流程；使用 `superpowers:brainstorming` 做最小设计梳理，因 AGENTS 明确要求默认自主执行不等待确认；使用 `superpowers:writing-plans` 按项目文档计划降级；使用 `superpowers:test-driven-development` 执行 RED/GREEN；相邻回归夹具失败时使用 `superpowers:systematic-debugging` 查明根因；提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话仍未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.133.0` 已完成本地提交 `afc62e5 feat: 增加授权规则确认固化 0.133.0`，当前分支在推送前继续追加 `0.134.0`；v139 计划明确只做偏好候选显式确认固化与撤销，不自动改变回复风格、LLM prompt、路由或执行决策。
- 设计选择：新增 `preferences.py` 统一读写 `config/preferences.local.json`；`preference` 候选确认只保存偏好文本并标记候选已固化，撤销只删除对应偏好并恢复候选活跃；配置管家只读展示本地偏好数量。当前阶段不把确认/撤销命令加入 LLM 白名单，不从普通聊天或 LLM fallback 自动写入偏好。
- RED：目标命令先失败，失败点为缺少 `jarvis_lite.preferences`、候选确认暂不支持 `preference`、版本仍为 `0.133.0`。
- GREEN：同一目标命令 20 项通过。
- 调试留痕：相邻回归首次失败在更新检查 Agent 测试，根因是 manifest 夹具仍写 `0.133.1`，当前版本升到 `0.134.0` 后不再表示新版本；将夹具提升为 `0.134.1` 后复跑通过。实现复核时确认 `memory_config_candidates.py` 中 `authorization_rule` 与 `preference` 分支已经分离，偏好不会写入授权规则文件。
- 验证：相邻回归 434 项通过；全量 `unittest` 当前会话复跑 750 项通过；临时项目偏好确认/撤销 smoke 输出 `preference-smoke OK`；源码桌面 smoke 和打包后 smoke 均输出 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.134.0.exe`，大小 `60,461,056` 字节，时间戳 `2026/6/5 11:46:55`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.134.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 308 项通过；严格真实密钥形态扫描 20 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-05 0.135.0 偏好显式启用与停用第一阶段

- 时间：2026-06-05 继续执行。
- 工具：Get-Content / rg / git status / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Select-String / PowerShell 版本资源检查 / git diff --check。
- 技能：使用 `superpowers:using-superpowers` 选择流程；使用 `superpowers:brainstorming` 做最小设计梳理，因 AGENTS 明确要求默认自主执行不等待确认；使用 `superpowers:writing-plans` 按项目文档计划降级；使用 `superpowers:test-driven-development` 执行 RED/GREEN；相邻回归夹具失败时使用 `superpowers:systematic-debugging` 查明根因；提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话仍未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.134.0` 已完成本地提交 `e86c316 feat: 增加偏好确认固化 0.134.0`；PROJECT-PLAN 后续目标明确下一批优先评估已保存偏好的显式启用/停用方案。
- 设计选择：扩展 `preferences.py` 的 `Preference.enabled`，旧记录缺失 `enabled` 时按未启用读取；新增 `/preference-status`、`/preference-enable 编号`、`/preference-disable 编号`，启用状态只写入 `config/preferences.local.json`，不接入回复风格、LLM prompt、路由或执行决策。
- RED：目标命令先失败，失败点为缺少 `set_preference_enabled`、`Preference.enabled`、`/preference-status` 命令、配置管家偏好入口和版本仍为 `0.134.0`。
- GREEN：同一目标命令 10 项通过。
- 调试留痕：相邻回归首次失败在更新检查 Agent 测试，根因是 manifest 夹具仍写 `0.134.1`，当前版本升到 `0.135.0` 后不再表示新版本；将夹具提升为 `0.135.1` 后复跑通过。
- 验证：相邻回归 437 项通过；全量 `unittest` 753 项通过；临时项目偏好启停 smoke 输出 `preference-enable-smoke OK`；源码桌面 smoke 和打包后 smoke 均输出 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.135.0.exe`，大小 `60,461,056` 字节，时间戳 `2026/6/5 13:02:31`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.135.0`。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，7 项通过。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 494 项通过；严格真实密钥形态扫描 20 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-05 0.136.0 偏好应用预览第一阶段

- 时间：2026-06-05 继续执行。
- 工具：Get-Content / rg / git status / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Select-String / PowerShell 版本资源检查 / git diff --check。
- 技能：使用 `superpowers:using-superpowers` 选择流程；使用 `superpowers:brainstorming` 做最小设计梳理，因 AGENTS 明确要求默认自主执行不等待确认；使用 `superpowers:writing-plans` 按项目文档计划降级；使用 `superpowers:test-driven-development` 执行 RED/GREEN；提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话仍未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.135.0` 已完成本地提交 `dff70fd feat: 增加偏好显式启停 0.135.0`；PROJECT-PLAN 后续目标明确下一批优先评估已启用偏好的显式预览和应用策略。
- 设计选择：新增 `/preference-preview [输入文本]` 和 `describe_preference_preview()`，只读展示当前已启用偏好和应用草案；无输入时展示通用预览，有输入时展示预览输入。当前阶段不自动改变回复风格、LLM prompt、路由或执行决策，不把预览命令加入 LLM 白名单。
- RED：目标命令先失败，失败点为缺少 `describe_preference_preview`、`/preference-preview` 命令、配置管家偏好预览入口和版本仍为 `0.135.0`。
- GREEN：同一目标命令 11 项通过。
- 验证：相邻回归 440 项通过；全量 `unittest` 756 项通过；临时项目偏好应用预览 smoke 输出 `preference-preview-smoke OK`；源码桌面 smoke 和打包后 smoke 均输出 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.136.0.exe`，大小 `60,465,152` 字节，时间戳 `2026/6/5 14:43:18`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.136.0`。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，7 项通过。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 498 项通过；严格真实密钥形态扫描 20 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-05 0.137.0 偏好稳定 ID 与冲突提示第一阶段

- 时间：2026-06-05 继续执行。
- 工具：Get-Content / rg / git status / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Select-String / PowerShell 版本资源检查。
- 技能：使用 `superpowers:using-superpowers` 选择流程；使用 `superpowers:brainstorming` 做最小设计梳理，因 AGENTS 明确要求默认自主执行不等待确认；使用 `superpowers:writing-plans` 按项目文档计划降级；使用 `superpowers:test-driven-development` 执行 RED/GREEN；相邻回归夹具失败时使用 `superpowers:systematic-debugging` 查明根因；提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话仍未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`；记录 `.codex/context-scan-v142-preference-id-conflict.json`。
- 上下文：`0.136.0` 已完成本地提交 `f6893eb feat: 增加偏好应用预览 0.136.0`；PROJECT-PLAN 后续目标明确下一批优先评估偏好冲突提示、稳定 ID 和真正应用前的显式确认策略。
- 设计选择：新增确定性偏好 ID，基于偏好文本 SHA-1 前 10 位生成 `pref-...`，旧记录缺失 ID 时读取阶段可得到同一 ID，后续保存或启停会写回；`/preference-enable` 与 `/preference-disable` 支持编号或 ID；冲突提示只检查已启用偏好中简洁/详细、中文/英文等明显互斥表达，只提示人工确认，不自动裁决优先级。
- RED：目标命令先失败，失败点为缺少 `Preference.preference_id`、存储缺少 `id`、命令仍只接受数字编号、状态/预览缺少 ID 与冲突提示、版本仍为 `0.136.0`。
- GREEN：同一目标命令 13 项通过。
- 调试留痕：相邻回归首次失败在更新检查 Agent 测试，根因是 manifest 夹具仍写 `0.136.1`，当前版本升到 `0.137.0` 后不再表示新版本；将夹具提升为 `0.137.1` 后复跑通过。
- 验证：相邻回归 442 项通过；全量 `unittest` 758 项通过；临时项目偏好 ID 与冲突提示 smoke 输出 `preference-id-conflict-smoke OK`；源码桌面 smoke 和打包后 smoke 均输出 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.137.0.exe`，大小 `60,465,152` 字节，时间戳 `2026/6/5 16:05:57`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.137.0`。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，7 项通过。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 646 项通过；严格真实密钥形态扫描 15 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-05 0.138.0 偏好应用确认草稿第一阶段

- 时间：2026-06-05 继续执行。
- 工具：Get-Content / rg / git status / update_plan / apply_patch / unittest。
- 技能：使用 `superpowers:using-superpowers` 选择流程；使用 `superpowers:brainstorming` 做最小设计梳理，因用户已经反复要求“继续下一阶段”且 AGENTS 明确要求默认自主执行，不等待额外确认；使用 `superpowers:writing-plans` 按项目 `word/plans` 文档计划降级；使用 `superpowers:test-driven-development` 执行 RED/GREEN；提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话仍未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`；记录 `.codex/context-scan-v143-preference-apply-confirmation.json`。
- 上下文：`0.137.0` 已完成本地提交 `0446e77 feat: 增加偏好稳定 ID 与冲突提示 0.137.0`，当前分支未推送；PROJECT-PLAN 后续目标明确下一批优先评估已启用偏好真正应用前的显式确认策略。
- 设计选择：新增 `/preference-apply-draft [输入文本]` 和 `describe_preference_application_draft()`，只生成“待确认偏好应用草稿”，展示输入、启用偏好、稳定 ID、冲突提示和确认边界；当前阶段不真正应用偏好，不接入普通回复、LLM prompt、SearchRouter、InnerBrain 或执行决策。
- RED：目标命令先失败，失败点为缺少 `describe_preference_application_draft`、`/preference-apply-draft` 命令和版本仍为 `0.137.0`。
- GREEN：`.\.venv\Scripts\python.exe -m unittest tests.test_preferences tests.test_agent tests.test_llm tests.test_project_metadata -v` 通过，429 项通过。
- 验证：相邻回归 445 项通过；全量 `unittest` 761 项通过；临时项目偏好应用确认草稿 smoke 输出 `preference-apply-draft-smoke OK`；源码桌面 smoke 输出 `desktopPetWindow`；打包后 smoke 退出码 0、stdout 包含 `desktopPetWindow`、stderr 为空且无残留 `JarvisLite` 进程。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.138.0.exe`，大小 `60,465,152` 字节，时间戳 `2026/6/5 17:10:33`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.138.0`。
- 文档后新鲜复验：`.\.venv\Scripts\python.exe -m unittest tests.test_project_metadata -v`，7 项通过。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 650 项通过；严格真实密钥形态扫描 16 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-05 0.139.0 偏好应用确认命令第一阶段

- 时间：2026-06-05 继续执行。
- 工具：Get-Content / rg / git status / update_plan / apply_patch / unittest。
- 技能：使用 `superpowers:using-superpowers` 选择流程；使用 `superpowers:brainstorming` 做最小设计梳理，因用户已经明确要求“继续下一阶段”且 AGENTS 明确要求默认自主执行，不等待额外确认；使用 `superpowers:writing-plans` 按项目 `word/plans` 文档计划降级；使用 `superpowers:test-driven-development` 执行 RED/GREEN；提交前使用 `superpowers:verification-before-completion` 做新鲜验证。
- 工具降级：当前会话仍未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`；记录 `.codex/context-scan-v144-preference-apply-confirm.json`。
- 上下文：`0.138.0` 已完成本地提交 `07c1b50 feat: 增加偏好应用确认草稿 0.138.0`，当前分支未推送；PROJECT-PLAN 后续目标明确下一批优先评估偏好确认草稿后的真实应用确认命令和应用范围。
- 设计选择：新增 `/preference-apply-confirm [输入文本]` 和 `describe_confirmed_preference_application()`，只在显式确认命令中输出“已确认本次偏好应用”；无启用偏好或存在明显冲突时拒绝确认；应用范围仅限本次命令输出，不写入普通回复、LLM prompt、SearchRouter、InnerBrain、执行决策或持久 pending 状态。
- RED：目标命令先失败，失败点为缺少 `describe_confirmed_preference_application`、Agent 未接入 `/preference-apply-confirm`、配置管家缺少入口、版本仍为 `0.138.0`。
- GREEN：实现 `describe_confirmed_preference_application()`，Agent 接入显式确认命令、帮助和状态，配置管家展示入口，LLM 指令继续排除该命令，版本提升到 `0.139.0`。
- 验证：相邻回归 449 项通过；全量 `unittest` 765 项通过；临时项目偏好应用确认 smoke 输出 `preference-apply-confirm smoke OK`；源码桌面 smoke 输出 `desktopPetWindow`；打包后 smoke 退出码 0、stdout 包含 `desktopPetWindow`、stderr 为空且无残留 `JarvisLite` 进程。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`；版本化安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.139.0.exe`，大小 `60,469,248` 字节，时间戳 `2026/6/5 18:09:00`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.139.0`。
- 调试留痕：安装包元数据首次按旧路径 `windows-installer-stage\JarvisLite.version.txt` 检查失败；定位实际生成路径为 `E:\oyzj\ai\jarvis-lite-dist\JarvisLite.version.txt` 后复验通过。打包后 stdout 中文在 PowerShell 表格中显示乱码，按 UTF-8 重新读取后确认包含 `desktopPetWindow`，stderr 长度为 0。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 654 项通过；严格真实密钥形态扫描 17 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-09 0.140.0 偏好应用确认记录与撤销第一阶段

- 时间：2026-06-09 继续执行并恢复断线现场。
- 工具：Get-Content / rg / git status / git diff / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / Select-String / PowerShell 版本资源检查 / git diff --check / Markdown 本地链接检查 / 严格真实密钥形态扫描。
- 技能：使用 `superpowers:using-superpowers` 选择流程；使用 `superpowers:systematic-debugging` 处理断线与 smoke 失败；追加 bugfix 前使用 `superpowers:test-driven-development`，先写 RED 再改实现。
- 工具降级：当前会话仍未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 断线定位：`日志.txt` 尾部显示上次已完成 v145 主要实现和全量回归，随后命令行 smoke 因临时脚本导入不存在的 `load_preferences` 失败，读取 `preferences.py` 时会话遇到 503 断开。
- 上下文：`0.139.0` 已完成偏好应用确认命令第一阶段；v145 计划要求确认成功写运行态审计记录、历史查看、撤销确认记录，且不自动接入普通聊天、LLM prompt、路由或执行决策。
- 设计选择：确认记录写入项目外运行态 `jarvis-lite-runtime/agent-context.json` 的 `recent_preference_applications`；撤销只把确认记录状态标记为 `undone`，不修改 `config/preferences.local.json` 的偏好定义或启用状态。
- 调试留痕：隔离 smoke 首次发现同一秒、同一输入、同一启用偏好连续确认会生成相同 `prefapp-*` ID，运行态读取按 ID 去重后历史坍缩为 1 条。新增 RED 用例复现后，改为检测已有确认 ID 并在碰撞时追加序号参与哈希。
- 验证：目标复验 438 项通过；全量 `unittest` 770 项通过；命令行 smoke 输出 `preference-apply-audit-smoke OK`；源码桌面 smoke 输出 `desktopPetWindow`；打包后 smoke 退出码 0、stdout 包含 `desktopPetWindow`、stderr 为空且无残留 `JarvisLite` 进程。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；构建日志包含既有 `Hidden import "tzdata" not found!` 警告和第三方 `pyautogui` 的 `SyntaxWarning: invalid escape sequence '\e'`；版本化安装包 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.140.0.exe`，大小 `59,715,584` 字节，时间戳 `2026/6/9 15:28:13`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.140.0`。
- 断线恢复最终复验：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`，`Ran 770 tests in 11.525s`，`OK`；`git diff --check` 退出码 0，仅 LF/CRLF 提示。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 666 项通过；严格真实密钥形态扫描 25 个公开变更/新增文件无命中；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。

## 2026-06-09 0.141.0 偏好进入普通回复上下文第一阶段

- 时间：2026-06-09 继续执行 v146。
- 工具：Get-Content / rg / git status / git diff / update_plan / apply_patch / unittest / 临时项目 Agent smoke / scripts\build_windows_installer.py / PowerShell 版本资源检查 / git diff --check / Markdown 本地链接检查 / 严格真实密钥形态扫描。
- 技能：使用 `superpowers:using-superpowers` 选择流程；使用 `superpowers:executing-plans` 承接已有 v146 计划；提交前使用 `superpowers:verification-before-completion` 做新鲜验证；密钥扫描误报时使用 `superpowers:systematic-debugging` 查明根因。
- 工具降级：当前会话仍未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目降级规则使用本地结构化分析、`rg`/`Get-Content`、`update_plan`、superpowers 流程、TDD 和 `unittest`。
- 上下文：`0.140.0` 已完成本地提交 `a09fd9c feat: 增加偏好应用确认记录与撤销 0.140.0`，当前分支未推送；v146 计划明确只把最近有效确认记录接入普通 LLM fallback 上下文和 `/llm-context-preview`。
- 设计选择：新增 `describe_preference_reply_context()`，只选择最近一条状态为 `confirmed`、当前已启用偏好 ID/文本与确认记录完全一致、且无明显冲突的确认记录；撤销确认、停用偏好、删除偏好或启用集合变化后旧确认自动失效。
- 边界：不把 `/preference-*` 管理命令加入 LLM provider command 白名单，不改变 SearchRouter、InnerBrain、路由、授权层或桌面执行决策；本阶段不重写本地知识库命中回答或长期记忆兜底回答。
- RED/GREEN：目标测试先失败后通过；`tests.test_preferences`、Agent LLM 上下文测试、LLM 白名单边界和版本一致性目标复验 23 项通过。
- 验证：相邻回归 458 项通过；全量 `unittest` 774 项通过；命令行 smoke 输出 `preference-reply-context-smoke OK`；源码桌面 smoke 和打包后 smoke 均输出 `desktopPetWindow`。
- 打包：`.\.venv\Scripts\python.exe scripts\build_windows_installer.py` 成功；版本化安装包 `E:\ai\jarvis-lite-dist\JarvisLiteSetup-0.141.0.exe`，大小 `59,711,488` 字节，时间戳 `2026-06-09 17:31:22`；安装脚本、SED、`JarvisLite.version.txt` 和 `JarvisLite.exe` 版本资源均为 `0.141.0`。
- 静态检查：`git diff --check` 退出码 0，仅 LF/CRLF 提示；Markdown 本地链接 671 项通过；严格真实密钥形态扫描 14 个公开变更/新增文件无命中；首次密钥扫描被历史方案文件名中的 `sk-...-plan` 误报，收窄真实 key 形态后复跑通过；`config/llm.local.json`、`config/search.local.json`、`word/inner-brain-evaluation-report.md` 不存在；README BOM 为 `EF-BB-BF`。
