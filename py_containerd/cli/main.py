
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
=======
import os
import sys
import click


@click.group()
@click.option(
    "--address",
    envvar="PY_CONTAINERD_ADDRESS",
    default="unix:///run/py-containerd/py-containerd.sock",
    help="Daemon gRPC address",
)
@click.pass_context
def cli(ctx: click.Context, address: str) -> None:
    ctx.ensure_object(dict)
    ctx.obj["address"] = address


@cli.group()
def images() -> None:
    """Image management"""


@images.command("pull")
@click.argument("reference")
@click.pass_context
def images_pull(ctx: click.Context, reference: str) -> None:
    address = ctx.obj["address"]
    click.echo(f"[stub] Pulling image {reference} via {address}")


@cli.group()
def containers() -> None:
    """Container management"""


@containers.command("create")
@click.argument("image")
@click.argument("id")
@click.pass_context
def containers_create(ctx: click.Context, image: str, id: str) -> None:
    address = ctx.obj["address"]
    click.echo(f"[stub] Creating container {id} from {image} via {address}")


@cli.group()
def tasks() -> None:
    """Task lifecycle"""


@tasks.command("start")
@click.argument("id")
@click.pass_context
def tasks_start(ctx: click.Context, id: str) -> None:
    address = ctx.obj["address"]
    click.echo(f"[stub] Starting task {id} via {address}")


@tasks.command("kill")
@click.argument("id")
@click.argument("signal")
@click.pass_context
def tasks_kill(ctx: click.Context, id: str, signal: str) -> None:
    address = ctx.obj["address"]
    click.echo(f"[stub] Killing task {id} with {signal} via {address}")


@cli.command("ps")
@click.pass_context
def ps(ctx: click.Context) -> None:
    address = ctx.obj["address"]
    click.echo(f"[stub] Listing tasks via {address}")


@cli.command("logs")
@click.argument("id")
@click.pass_context
def logs(ctx: click.Context, id: str) -> None:
    address = ctx.obj["address"]
    click.echo(f"[stub] Streaming logs for {id} via {address}")


if __name__ == "__main__":
    cli()


