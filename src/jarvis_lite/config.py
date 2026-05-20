import os
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """集中管理项目目录，避免各模块重复拼接路径。"""

    root: Path
    memory_dir: Path
    data_dir: Path
    logs_dir: Path
    word_dir: Path

    @property
    def profile_path(self) -> Path:
        return self.memory_dir / "profile.md"

    @property
    def notes_dir(self) -> Path:
        return self.memory_dir / "notes"

    @property
    def log_path(self) -> Path:
        return self.logs_dir / "jarvis.log"


def build_project_paths(root: Path | None = None) -> ProjectPaths:
    """构建并确保第一阶段需要的项目目录存在。"""

    project_root = root or _default_project_root()
    project_root = project_root.resolve()
    paths = ProjectPaths(
        root=project_root,
        memory_dir=project_root / "memory",
        data_dir=project_root / "data",
        logs_dir=project_root / "logs",
        word_dir=project_root / "word",
    )

    for directory in (paths.memory_dir, paths.notes_dir, paths.data_dir, paths.logs_dir, paths.word_dir):
        directory.mkdir(parents=True, exist_ok=True)

    return paths


def _default_project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "Jarvis Lite"
    return Path(__file__).resolve().parents[2]
