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

