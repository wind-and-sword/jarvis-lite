import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.idea_workflow import (
    describe_idea_focus,
    describe_idea_open,
    describe_idea_open_project,
    describe_idea_project_status,
    describe_idea_workflow_status,
    open_idea_app,
    open_idea_project,
)
from jarvis_lite.window_state import NativeWindow, build_window_snapshot


class IdeaWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")
        self.idea_path = self.paths.root / "tools" / "idea64.exe"
        self.idea_path.parent.mkdir(parents=True)
        self.idea_path.write_text("fake idea", encoding="utf-8")
        self.project_dir = self.paths.root / "projects" / "jarvis-lite"
        self.project_dir.mkdir(parents=True)
        (self.project_dir / ".idea").mkdir()
        (self.project_dir / ".git").mkdir()
        (self.project_dir / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
        (self.project_dir / "package.json").write_text("{}", encoding="utf-8")
        (self.paths.config_dir / "apps.local.json").write_text(
            json.dumps(
                {
                    "apps": {
                        "idea": {
                            "path": str(self.idea_path),
                            "aliases": ["我的IDEA"],
                        }
                    }
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_describe_idea_workflow_status_reports_first_stage_boundary(self):
        response = describe_idea_workflow_status(self.paths)

        self.assertIn("IDEA 工作流状态：第一阶段", response)
        self.assertIn("/idea-open", response)
        self.assertIn("/idea-open-project 项目路径", response)
        self.assertIn(str(self.idea_path.resolve()), response)
        self.assertIn("不运行测试、不打开终端、不点击、不输入", response)

    def test_open_idea_app_uses_configured_path_and_injected_executor(self):
        calls = []

        result = open_idea_app(self.paths, executor=lambda path: calls.append(path))

        self.assertEqual(result.app.app_id, "idea")
        self.assertEqual(result.alias, "idea")
        self.assertEqual(result.path, self.idea_path.resolve())
        self.assertEqual(calls, [self.idea_path.resolve()])

    def test_describe_idea_open_reports_scope_without_project_actions(self):
        response = describe_idea_open(self.paths, executor=lambda path: None)

        self.assertIn("IDEA 打开执行：IntelliJ IDEA (idea)", response)
        self.assertIn("不打开项目、不运行测试、不打开终端、不点击、不输入", response)

    def test_open_idea_app_reports_missing_path(self):
        empty_root = self.paths.root / "empty-program-files"
        empty_root.mkdir()
        (self.paths.config_dir / "apps.local.json").unlink()

        with patch.dict(
            os.environ,
            {
                "ProgramFiles": str(empty_root),
                "ProgramFiles(x86)": str(empty_root),
                "LOCALAPPDATA": str(empty_root),
                "APPDATA": str(empty_root),
            },
        ):
            with self.assertRaisesRegex(FileNotFoundError, "IDEA 启动路径未找到"):
                open_idea_app(self.paths, executor=lambda path: None)

    def test_describe_idea_focus_uses_existing_window_and_injected_executor(self):
        calls = []
        snapshot = build_window_snapshot(
            self.paths,
            (NativeWindow(handle=400, title="jarvis-lite - IntelliJ IDEA", process_id=40, process_name="idea64.exe"),),
            foreground_handle=None,
            platform_name="Windows",
        )

        response = describe_idea_focus(self.paths, snapshot=snapshot, executor=lambda handle: calls.append(handle))

        self.assertIn("IDEA 聚焦执行", response)
        self.assertIn("窗口切换执行：jarvis-lite - IntelliJ IDEA", response)
        self.assertIn("不点击、不输入、不运行测试、不打开终端", response)
        self.assertEqual(calls, [400])

    def test_describe_idea_focus_guides_open_when_window_missing(self):
        snapshot = build_window_snapshot(self.paths, (), foreground_handle=None, platform_name="Windows")

        with self.assertRaisesRegex(ValueError, "/idea-open"):
            describe_idea_focus(self.paths, snapshot=snapshot, executor=lambda handle: None)

    def test_open_idea_project_uses_configured_path_project_path_and_injected_executor(self):
        calls = []

        result = open_idea_project(
            self.paths,
            str(self.project_dir),
            executor=lambda idea_path, project_path: calls.append((idea_path, project_path)),
        )

        self.assertEqual(result.app.app_id, "idea")
        self.assertEqual(result.idea_path, self.idea_path.resolve())
        self.assertEqual(result.project_path, self.project_dir.resolve())
        self.assertEqual(calls, [(self.idea_path.resolve(), self.project_dir.resolve())])

    def test_open_idea_project_requires_existing_directory(self):
        with self.assertRaisesRegex(ValueError, "项目目录不存在"):
            open_idea_project(self.paths, str(self.project_dir / "missing"), executor=lambda idea_path, project_path: None)

        project_file = self.project_dir / "README.md"
        project_file.write_text("demo", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "项目路径不是目录"):
            open_idea_project(self.paths, str(project_file), executor=lambda idea_path, project_path: None)

    def test_describe_idea_open_project_reports_scope_without_running_project(self):
        response = describe_idea_open_project(
            self.paths,
            str(self.project_dir),
            executor=lambda idea_path, project_path: None,
        )

        self.assertIn("IDEA 打开项目执行", response)
        self.assertIn(f"项目路径：{self.project_dir.resolve()}", response)
        self.assertIn("不运行测试、不打开终端、不点击、不输入、不编辑项目文件", response)

    def test_describe_idea_project_status_reports_readonly_markers(self):
        response = describe_idea_project_status(self.paths, str(self.project_dir))

        self.assertIn("IDEA 项目状态：", response)
        self.assertIn(f"项目路径：{self.project_dir.resolve()}", response)
        self.assertIn(".idea：存在", response)
        self.assertIn("Git：存在", response)
        self.assertIn("项目标记：pyproject.toml、package.json", response)
        self.assertIn("不运行测试、不打开终端、不读取 IDE 内容、不写项目文件", response)

    def test_describe_idea_project_status_defaults_to_current_project_root(self):
        response = describe_idea_project_status(self.paths, "")

        self.assertIn(f"项目路径：{self.paths.root.resolve()}", response)
        self.assertIn("项目标记：未发现", response)


if __name__ == "__main__":
    unittest.main()
