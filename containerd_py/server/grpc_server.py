import asyncio
from typing import Any

import grpc

from containerd_py.server.services import ImagesService, ContainersService, TasksService, SimConfig
from containerd_py.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2_grpc as images_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.containers.v1 import containers_pb2_grpc as containers_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.tasks.v1 import tasks_pb2_grpc as tasks_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.content.v1 import content_pb2_grpc as content_grpc


class UnimplementedContent(content_grpc.ContentServicer):
    pass


async def create_server(state_dir: str) -> grpc.aio.Server:
    server = grpc.aio.server(options=[("grpc.max_receive_message_length", 64 * 1024 * 1024)])
    cfg = SimConfig(state_dir=state_dir)

    images_grpc.add_ImagesServicer_to_server(ImagesService(cfg), server)
    containers_grpc.add_ContainersServicer_to_server(ContainersService(cfg), server)
    tasks_grpc.add_TasksServicer_to_server(TasksService(cfg), server)
    content_grpc.add_ContentServicer_to_server(UnimplementedContent(), server)

    return server