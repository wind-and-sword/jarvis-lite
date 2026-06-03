import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.runtime_context import RuntimeRouteDecisionContext, load_runtime_context
from jarvis_lite.task_state import (
    cancel_task,
    complete_task,
    describe_task_status,
    record_task_failure,
    record_task_failure_with_screen_ocr,
    record_task_event_result,
    record_task_route_event,
    record_task_step,
    resume_task,
    start_task,
)


class TaskStateTests(unittest.TestCase):
    def test_describe_task_status_reports_empty_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            response = describe_task_status(paths)

            self.assertIn("任务状态：还没有当前任务", response)
            self.assertIn("/task-start 任务名称", response)
            self.assertIn("不自动截图、不自动 OCR、不自动重新执行外部动作", response)

    def test_task_step_failure_and_status_persist_to_runtime_context(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            start_response = start_task(paths, "发布 0.120.0", origin_prompt="用户要求继续下一个任务")
            first_step = record_task_step(paths, "写失败测试")
            second_step = record_task_step(paths, "实现任务状态模块")
            failure_response = record_task_failure(
                paths,
                "目标测试失败",
                route_summary="command / /task-fail",
                authorization_summary="explicit_command direct_execute",
            )
            status = describe_task_status(paths)
            runtime_context = load_runtime_context(paths)

            self.assertIn("已开始任务：发布 0.120.0", start_response)
            self.assertIn("当前步骤：写失败测试", first_step)
            self.assertIn("已完成上一步：写失败测试", second_step)
            self.assertIn("任务失败复盘：发布 0.120.0", failure_response)
            self.assertIn("失败步骤：实现任务状态模块", failure_response)
            self.assertIn("已完成步骤：写失败测试", failure_response)
            self.assertIn("失败原因：目标测试失败", failure_response)
            self.assertIn("用户原话：用户要求继续下一个任务", failure_response)
            self.assertIn("路由摘要：command / /task-fail", failure_response)
            self.assertIn("授权摘要：explicit_command direct_execute", failure_response)
            self.assertIn("屏幕/OCR：未采集", failure_response)
            self.assertIn("/task-resume", failure_response)
            self.assertIn("当前任务：发布 0.120.0（失败）", status)
            self.assertIn("最近失败记录：", status)
            self.assertIsNotNone(runtime_context.current_task)
            self.assertEqual(runtime_context.current_task.title, "发布 0.120.0")
            self.assertEqual(runtime_context.current_task.status, "failed")
            self.assertEqual(len(runtime_context.recent_task_failures), 1)

    def test_task_route_events_persist_and_feed_failure_replay(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            start_task(paths, "整理项目资料", origin_prompt="帮我整理这个项目")
            record_task_route_event(
                paths,
                RuntimeRouteDecisionContext(
                    route="command",
                    detail="/dir-open",
                    prompt="/dir-open 项目",
                    summary="显式命令",
                    explanation="source=explicit-command action=direct-dispatch",
                    created_at="2026-06-03T10:00:00",
                ),
            )
            status = describe_task_status(paths)
            failure_response = record_task_failure(paths, "目录打开失败")
            runtime_context = load_runtime_context(paths)

            self.assertIn("最近任务事件：", status)
            self.assertIn("command / /dir-open", status)
            self.assertIn("输入：/dir-open 项目", status)
            self.assertIn("自动采集上下文：", failure_response)
            self.assertIn("command / /dir-open", failure_response)
            self.assertIn("输入：/dir-open 项目", failure_response)
            self.assertEqual(len(runtime_context.recent_task_failures), 1)
            self.assertEqual(len(runtime_context.recent_task_failures[0].recent_events), 1)

    def test_task_route_event_result_updates_latest_matching_event(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            start_task(paths, "登记常用目录")
            record_task_route_event(
                paths,
                RuntimeRouteDecisionContext(
                    route="command",
                    detail="/dir-add",
                    prompt="/dir-add 工作区 C:/demo",
                    summary="显式命令",
                    explanation="source=explicit-command action=direct-dispatch",
                    created_at="2026-06-03T10:00:00",
                ),
            )

            record_task_event_result(paths, "/dir-add 工作区 C:/demo", "已登记常用目录：工作区 -> C:/demo")
            failure_response = record_task_failure(paths, "后续步骤失败")
            runtime_context = load_runtime_context(paths)

            self.assertIn("结果：已登记常用目录：工作区 -> C:/demo", failure_response)
            self.assertEqual(runtime_context.recent_task_failures[0].recent_events[0].summary, "已登记常用目录：工作区 -> C:/demo")

    def test_failed_task_can_resume_complete_and_cancel(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            start_task(paths, "整理资料")
            record_task_step(paths, "导入资料")
            record_task_failure(paths, "文件不存在")
            resume_response = resume_task(paths)
            complete_response = complete_task(paths)
            empty_after_complete = describe_task_status(paths)
            start_task(paths, "临时任务")
            cancel_response = cancel_task(paths)
            empty_after_cancel = describe_task_status(paths)

            self.assertIn("已恢复任务：整理资料", resume_response)
            self.assertIn("当前步骤：导入资料", resume_response)
            self.assertIn("已完成任务：整理资料", complete_response)
            self.assertIn("任务状态：还没有当前任务", empty_after_complete)
            self.assertIn("已取消任务：临时任务", cancel_response)
            self.assertIn("任务状态：还没有当前任务", empty_after_cancel)

    def test_commands_report_missing_current_task(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            self.assertIn("还没有当前任务", record_task_step(paths, "不存在步骤"))
            self.assertIn("还没有当前任务", record_task_failure(paths, "不存在失败"))
            self.assertIn("还没有可恢复的失败任务", resume_task(paths))
            self.assertIn("还没有当前任务", complete_task(paths))
            self.assertIn("还没有当前任务", cancel_task(paths))

    def test_task_failure_with_screen_ocr_records_capture_context(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            calls: list[tuple[Path, str]] = []

            def fake_capturer(target_path: Path) -> tuple[int, int]:
                target_path.write_bytes(b"png")
                return (1280, 720)

            def fake_recognizer(image_path: Path, language: str) -> str:
                calls.append((image_path, language))
                return "错误弹窗文字"

            start_task(paths, "发布 0.121.0", origin_prompt="用户要求继续")
            record_task_step(paths, "运行打包 smoke")

            response = record_task_failure_with_screen_ocr(
                paths,
                "打包后 smoke 失败",
                language="eng",
                route_summary="command / /task-fail-capture",
                authorization_summary="explicit_command direct_execute",
                capturer=fake_capturer,
                recognizer=fake_recognizer,
            )
            status = describe_task_status(paths)
            runtime_context = load_runtime_context(paths)

            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1], "eng")
            self.assertIn("任务失败复盘：发布 0.121.0", response)
            self.assertIn("失败步骤：运行打包 smoke", response)
            self.assertIn("截图：logs/screenshots/", response)
            self.assertIn("尺寸：1280x720", response)
            self.assertIn("OCR 图片识别：logs/screenshots/", response)
            self.assertIn("语言：eng", response)
            self.assertIn("错误弹窗文字", response)
            self.assertIn("当前阶段只记录失败上下文，不自动重新执行外部动作", response)
            self.assertIn("屏幕/OCR：截图：logs/screenshots/", status)
            self.assertIn("错误弹窗文字", status)
            self.assertEqual(runtime_context.current_task.status, "failed")
            self.assertEqual(len(runtime_context.recent_task_failures), 1)
            self.assertIn("错误弹窗文字", runtime_context.recent_task_failures[0].screen_context)

    def test_task_failure_with_screen_ocr_records_ocr_error_after_capture(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            def fake_capturer(target_path: Path) -> tuple[int, int]:
                target_path.write_bytes(b"png")
                return (800, 600)

            def fake_recognizer(image_path: Path, language: str) -> str:
                raise RuntimeError("未找到 tesseract.exe")

            start_task(paths, "检查屏幕")
            response = record_task_failure_with_screen_ocr(
                paths,
                "OCR 不可用",
                capturer=fake_capturer,
                recognizer=fake_recognizer,
            )

            self.assertIn("截图：logs/screenshots/", response)
            self.assertIn("尺寸：800x600", response)
            self.assertIn("OCR 图片识别失败：未找到 tesseract.exe", response)
            self.assertIn("当前阶段只记录失败上下文，不自动重新执行外部动作", response)


if __name__ == "__main__":
    unittest.main()
