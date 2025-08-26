"""py_containerd CLI entrypoint.

This module provides a minimal CLI that supports `--help` without relying on
third-party libraries. It is designed to be imported and executed with:

    python -m py_containerd.cli.main --help
"""

from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="py_containerd",
        description="Containerd Python CLI (minimal; help-only for smoke tests)",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # Placeholder subcommand to demonstrate structure (no external deps)
    ping_parser = subparsers.add_parser(
        "ping",
        help="Print 'pong' and exit",
        description="Diagnostic command to verify CLI wiring",
    )
    ping_parser.set_defaults(func=lambda _args: print("pong"))

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = build_parser()

    # If no args provided, show help similar to `tool --help`
    if not argv:
        parser.print_help()
        return 0

    args = parser.parse_args(argv)

    if hasattr(args, "func"):
        args.func(args)
        return 0

    # Unknown or incomplete command; show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

