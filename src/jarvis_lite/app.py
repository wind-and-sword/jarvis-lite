from __future__ import annotations

import argparse

from .agent import JarvisAgent
from .config import build_project_paths
from .conversation import ConversationSession


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Jarvis Lite 命令行助手")
    parser.add_argument("--once", help="执行一次输入后退出，适合自动化验证。")
    args = parser.parse_args(argv)

    paths = build_project_paths()
    agent = JarvisAgent(paths)
    if args.once is not None:
        print(agent.handle(args.once))
        return 0

    session = ConversationSession(paths)
    print("Jarvis Lite 已启动。输入 /help 查看命令，输入 /exit 退出。")
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if user_input.strip() in {"/exit", "exit", "quit"}:
            print("已退出 Jarvis Lite。")
            return 0

        print(session.handle(user_input))
