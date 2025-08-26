import asyncio
import contextlib
import socket

import grpc
import pytest

from py_containerd.server.grpc_server import create_server
from py_containerd.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2_grpc as images_grpc
from py_containerd.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2


async def _free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.mark.asyncio
async def test_unimplemented_methods_return_status_unimplemented(tmp_path):
    server = await create_server(str(tmp_path))
    port = await _free_port()
    server.add_insecure_port(f"127.0.0.1:{port}")
    await server.start()
    try:
        async with grpc.aio.insecure_channel(f"127.0.0.1:{port}") as channel:
            stub = images_grpc.ImagesStub(channel)
            with pytest.raises(grpc.aio.AioRpcError) as err:
                await stub.Get(images_pb2.GetImageRequest(name="foo"))
            assert err.value.code() == grpc.StatusCode.UNIMPLEMENTED
    finally:
        await server.stop(0)