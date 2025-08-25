import asyncio
from typing import Any

import grpc

from py_containerd.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2_grpc as images_grpc
from py_containerd.api.protos.github.com.containerd.containerd.api.services.containers.v1 import containers_pb2_grpc as containers_grpc
from py_containerd.api.protos.github.com.containerd.containerd.api.services.tasks.v1 import tasks_pb2_grpc as tasks_grpc
from py_containerd.api.protos.github.com.containerd.containerd.api.services.content.v1 import content_pb2_grpc as content_grpc


class UnimplementedImages(images_grpc.ImagesServicer):
    pass


class UnimplementedContainers(containers_grpc.ContainersServicer):
    pass


class UnimplementedTasks(tasks_grpc.TasksServicer):
    pass


class UnimplementedContent(content_grpc.ContentServicer):
    pass


async def create_server(state_dir: str) -> grpc.aio.Server:
    server = grpc.aio.server(options=[("grpc.max_receive_message_length", 64 * 1024 * 1024)])

    images_grpc.add_ImagesServicer_to_server(UnimplementedImages(), server)
    containers_grpc.add_ContainersServicer_to_server(UnimplementedContainers(), server)
    tasks_grpc.add_TasksServicer_to_server(UnimplementedTasks(), server)
    content_grpc.add_ContentServicer_to_server(UnimplementedContent(), server)

    return server

