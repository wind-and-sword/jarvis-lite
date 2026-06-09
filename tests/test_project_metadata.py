import sys
import tomllib
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION = "0.142.0"

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from jarvis_lite import __version__


class ProjectMetadataTests(unittest.TestCase):
    def test_pyproject_requires_python_313_series(self):
        pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(pyproject["project"]["requires-python"], ">=3.13,<3.14")

    def test_python_version_file_pins_313_series(self):
        self.assertEqual((PROJECT_ROOT / ".python-version").read_text(encoding="utf-8").strip(), "3.13")

    def test_current_test_runner_uses_python_313(self):
        self.assertEqual(sys.version_info[:2], (3, 13))

    def test_project_version_matches_release_package_version(self):
        pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(pyproject["project"]["version"], RELEASE_VERSION)
        self.assertEqual(__version__, RELEASE_VERSION)

    def test_current_docs_use_pending_failure_language_for_local_failed_view(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8-sig")
        project_plan = (PROJECT_ROOT / "word" / "PROJECT-PLAN.md").read_text(encoding="utf-8")

        self.assertIn("有样本时会提示只看待处理失败、查看已处理和按文件聚焦入口", readme)
        self.assertNotIn("有样本时会提示只看失败、查看已处理和按文件聚焦入口", readme)
        self.assertIn("`/inner-brain-eval-local-failed` 只显示本机待处理失败样本", project_plan)
        self.assertNotIn("`/inner-brain-eval-local-failed` 只显示本机失败样本", project_plan)

    def test_readme_inner_brain_summary_mentions_empty_resolved_guidance(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8-sig")
        inner_brain_summary = next(
            line
            for line in readme.splitlines()
            if line.startswith("- InnerBrain 样本闭环：")
        )

        self.assertIn("暂无已处理样本时会提示这里只显示已通过样本", inner_brain_summary)
        self.assertIn("引导查看待处理失败或补充本机 evaluation 样本", inner_brain_summary)

    def test_project_plan_inner_brain_summary_mentions_empty_resolved_guidance(self):
        project_plan = (PROJECT_ROOT / "word" / "PROJECT-PLAN.md").read_text(encoding="utf-8")
        inner_brain_summary = next(
            line
            for line in project_plan.splitlines()
            if line.startswith("- InnerBrain 可观察与样本闭环：")
        )

        self.assertIn("暂无已处理样本时会提示这里只显示已通过样本", inner_brain_summary)
        self.assertIn("引导查看待处理失败或补充本机 evaluation 样本", inner_brain_summary)


if __name__ == "__main__":
    unittest.main()
