import asyncio
import os
import signal
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import grpc
from google.protobuf import empty_pb2
from google.protobuf import any_pb2
from google.protobuf import timestamp_pb2
from google.protobuf.timestamp_pb2 import Timestamp

from containerd_py.state.store import JsonStateStore
from containerd_py.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2_grpc as images_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2
from containerd_py.api.protos.github.com.containerd.containerd.api.services.containers.v1 import containers_pb2_grpc as containers_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.containers.v1 import containers_pb2
from containerd_py.api.protos.github.com.containerd.containerd.api.services.tasks.v1 import tasks_pb2_grpc as tasks_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.tasks.v1 import tasks_pb2
from containerd_py.api.protos.github.com.containerd.containerd.api.types.task import task_pb2 as types_task_pb2


@dataclass
class SimConfig:
    state_dir: str


class ImagesService(images_grpc.ImagesServicer):
    def __init__(self, cfg: SimConfig) -> None:
        self.store = JsonStateStore(os.path.join(cfg.state_dir, "images"))

    async def Get(self, request: images_pb2.GetImageRequest, context: grpc.aio.ServicerContext) -> images_pb2.GetImageResponse:  # type: ignore[override]
        data = self.store.get("default", request.name)
        if data is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "image not found")
        image = images_pb2.Image(name=request.name)
        return images_pb2.GetImageResponse(image=image)

    async def List(self, request: images_pb2.ListImagesRequest, context: grpc.aio.ServicerContext) -> images_pb2.ListImagesResponse:  # type: ignore[override]
        images: list[images_pb2.Image] = []
        ns_dir = Path(self.store.root) / "default"
        if ns_dir.exists():
            for f in ns_dir.glob("*.json"):
                name = f.stem
                images.append(images_pb2.Image(name=name))
        return images_pb2.ListImagesResponse(images=images)

    async def Create(self, request: images_pb2.CreateImageRequest, context: grpc.aio.ServicerContext) -> images_pb2.CreateImageResponse:  # type: ignore[override]
        name = request.image.name
        self.store.put("default", name, {"name": name})
        return images_pb2.CreateImageResponse(image=images_pb2.Image(name=name))

    async def Update(self, request: images_pb2.UpdateImageRequest, context: grpc.aio.ServicerContext) -> images_pb2.UpdateImageResponse:  # type: ignore[override]
        name = request.image.name
        self.store.put("default", name, {"name": name})
        return images_pb2.UpdateImageResponse(image=images_pb2.Image(name=name))

    async def Delete(self, request: images_pb2.DeleteImageRequest, context: grpc.aio.ServicerContext) -> empty_pb2.Empty:  # type: ignore[override]
        self.store.delete("default", request.name)
        return empty_pb2.Empty()


class ContainersService(containers_grpc.ContainersServicer):
    def __init__(self, cfg: SimConfig) -> None:
        self.store = JsonStateStore(os.path.join(cfg.state_dir, "containers"))

    async def Get(self, request: containers_pb2.GetContainerRequest, context: grpc.aio.ServicerContext) -> containers_pb2.GetContainerResponse:  # type: ignore[override]
        data = self.store.get("default", request.id)
        if data is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "container not found")
        container = containers_pb2.Container(id=request.id, image=data.get("image", ""))
        return containers_pb2.GetContainerResponse(container=container)

    async def List(self, request: containers_pb2.ListContainersRequest, context: grpc.aio.ServicerContext) -> containers_pb2.ListContainersResponse:  # type: ignore[override]
        items: list[containers_pb2.Container] = []
        ns_dir = Path(self.store.root) / "default"
        if ns_dir.exists():
            for f in ns_dir.glob("*.json"):
                cid = f.stem
                data = self.store.get("default", cid) or {}
                items.append(containers_pb2.Container(id=cid, image=data.get("image", "")))
        return containers_pb2.ListContainersResponse(containers=items)

    async def Create(self, request: containers_pb2.CreateContainerRequest, context: grpc.aio.ServicerContext) -> containers_pb2.CreateContainerResponse:  # type: ignore[override]
        cid = request.container.id
        image = request.container.image
        self.store.put("default", cid, {"image": image})
        return containers_pb2.CreateContainerResponse(container=containers_pb2.Container(id=cid, image=image))

    async def Update(self, request: containers_pb2.UpdateContainerRequest, context: grpc.aio.ServicerContext) -> containers_pb2.UpdateContainerResponse:  # type: ignore[override]
        cid = request.container.id
        image = request.container.image
        self.store.put("default", cid, {"image": image})
        return containers_pb2.UpdateContainerResponse(container=containers_pb2.Container(id=cid, image=image))

    async def Delete(self, request: containers_pb2.DeleteContainerRequest, context: grpc.aio.ServicerContext) -> empty_pb2.Empty:  # type: ignore[override]
        self.store.delete("default", request.id)
        return empty_pb2.Empty()


class TasksService(tasks_grpc.TasksServicer):
    def __init__(self, cfg: SimConfig) -> None:
        self.store = JsonStateStore(os.path.join(cfg.state_dir, "tasks"))

    async def Create(self, request: tasks_pb2.CreateTaskRequest, context: grpc.aio.ServicerContext) -> tasks_pb2.CreateTaskResponse:  # type: ignore[override]
        container_id = request.container_id
        # Record with no pid yet
        self.store.put("default", container_id, {"pid": 0})
        return tasks_pb2.CreateTaskResponse(container_id=container_id, pid=0)

    async def Start(self, request: tasks_pb2.StartRequest, context: grpc.aio.ServicerContext) -> tasks_pb2.StartResponse:  # type: ignore[override]
        container_id = request.container_id
        # Determine command: env SIM_CMD or default sleep 5
        cmd = os.environ.get("CONTAINERD_PY_SIM_CMD", "sleep 5")
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.store.put("default", container_id, {"pid": proc.pid})
        return tasks_pb2.StartResponse(pid=proc.pid)

    async def Delete(self, request: tasks_pb2.DeleteTaskRequest, context: grpc.aio.ServicerContext) -> tasks_pb2.DeleteResponse:  # type: ignore[override]
        data = self.store.get("default", request.container_id) or {"pid": 0}
        pid = int(data.get("pid", 0))
        if pid:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        self.store.delete("default", request.container_id)
        ts = timestamp_pb2.Timestamp()
        ts.GetCurrentTime()
        return tasks_pb2.DeleteResponse(id=request.container_id, pid=pid, exit_status=0, exited_at=ts)

    async def Kill(self, request: tasks_pb2.KillRequest, context: grpc.aio.ServicerContext) -> empty_pb2.Empty:  # type: ignore[override]
        data = self.store.get("default", request.container_id) or {"pid": 0}
        pid = int(data.get("pid", 0))
        if pid:
            try:
                os.kill(pid, request.signal or signal.SIGTERM)
            except ProcessLookupError:
                pass
        return empty_pb2.Empty()

    async def List(self, request: tasks_pb2.ListTasksRequest, context: grpc.aio.ServicerContext) -> tasks_pb2.ListTasksResponse:  # type: ignore[override]
        processes: list[types_task_pb2.Process] = []
        ns_dir = Path(self.store.root) / "default"
        if ns_dir.exists():
            for f in ns_dir.glob("*.json"):
                cid = f.stem
                data = self.store.get("default", cid) or {"pid": 0}
                pid = int(data.get("pid", 0))
                processes.append(types_task_pb2.Process(id=cid, pid=pid))
        return tasks_pb2.ListTasksResponse(tasks=processes)