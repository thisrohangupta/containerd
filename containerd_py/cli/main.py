import os
import sys
import click
import grpc

from containerd_py.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2_grpc as images_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2
from containerd_py.api.protos.github.com.containerd.containerd.api.services.containers.v1 import containers_pb2_grpc as containers_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.containers.v1 import containers_pb2
from containerd_py.api.protos.github.com.containerd.containerd.api.services.tasks.v1 import tasks_pb2_grpc as tasks_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.tasks.v1 import tasks_pb2


def _channel(address: str) -> grpc.Channel:
    if address.startswith("unix://"):
        path = address[len("unix://") :]
        return grpc.insecure_channel(f"unix://{path}")
    return grpc.insecure_channel(address)


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
@click.pass_context
def images(ctx: click.Context) -> None:
    """Image management"""


@images.command("pull")
@click.argument("reference")
@click.pass_context
def images_pull(ctx: click.Context, reference: str) -> None:
    address = ctx.obj["address"]
    ch = _channel(address)
    stub = images_grpc.ImagesStub(ch)
    # In simulation mode, create image record only
    resp = stub.Create(images_pb2.CreateImageRequest(image=images_pb2.Image(name=reference)))
    click.echo(resp.image.name)


@images.command("ls")
@click.pass_context
def images_ls(ctx: click.Context) -> None:
    address = ctx.obj["address"]
    ch = _channel(address)
    stub = images_grpc.ImagesStub(ch)
    resp = stub.List(images_pb2.ListImagesRequest())
    for img in resp.images:
        click.echo(img.name)


@cli.group()
@click.pass_context
def containers(ctx: click.Context) -> None:
    """Container management"""


@containers.command("create")
@click.argument("image")
@click.argument("id")
@click.pass_context
def containers_create(ctx: click.Context, image: str, id: str) -> None:
    address = ctx.obj["address"]
    ch = _channel(address)
    stub = containers_grpc.ContainersStub(ch)
    req = containers_pb2.CreateContainerRequest(container=containers_pb2.Container(id=id, image=image))
    resp = stub.Create(req)
    click.echo(resp.container.id)


@cli.group()
@click.pass_context
def tasks(ctx: click.Context) -> None:
    """Task lifecycle"""


@tasks.command("start")
@click.argument("id")
@click.pass_context
def tasks_start(ctx: click.Context, id: str) -> None:
    address = ctx.obj["address"]
    ch = _channel(address)
    stub = tasks_grpc.TasksStub(ch)
    resp = stub.Start(tasks_pb2.StartRequest(container_id=id))
    click.echo(resp.pid)


@tasks.command("kill")
@click.argument("id")
@click.argument("signal", default="15")
@click.pass_context
def tasks_kill(ctx: click.Context, id: str, signal: str) -> None:
    address = ctx.obj["address"]
    ch = _channel(address)
    stub = tasks_grpc.TasksStub(ch)
    _ = stub.Kill(tasks_pb2.KillRequest(container_id=id, signal=int(signal)))


@cli.command("ps")
@click.pass_context
def ps(ctx: click.Context) -> None:
    address = ctx.obj["address"]
    ch = _channel(address)
    stub = tasks_grpc.TasksStub(ch)
    resp = stub.List(tasks_pb2.ListTasksRequest())
    for p in resp.tasks:
        click.echo(f"{p.id}\t{p.pid}")


@cli.command("logs")
@click.argument("id")
@click.pass_context
def logs(ctx: click.Context, id: str) -> None:
    # Simulation: no logs
    click.echo(f"[sim] no logs for {id}")


if __name__ == "__main__":
    cli()

