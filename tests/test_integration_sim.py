import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2_grpc as images_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.images.v1 import images_pb2
from containerd_py.api.protos.github.com.containerd.containerd.api.services.containers.v1 import containers_pb2_grpc as containers_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.containers.v1 import containers_pb2
from containerd_py.api.protos.github.com.containerd.containerd.api.services.tasks.v1 import tasks_pb2_grpc as tasks_grpc
from containerd_py.api.protos.github.com.containerd.containerd.api.services.tasks.v1 import tasks_pb2


def _channel(addr: str) -> grpc.Channel:
    path = addr[len("unix://") :]
    return grpc.insecure_channel(f"unix://{path}")


def test_sim_lifecycle():
    with tempfile.TemporaryDirectory() as td:
        sock = os.path.join(td, "sim.sock")
        state = os.path.join(td, "state")
        env = os.environ.copy()
        env["CONTAINERD_PY_SIM_CMD"] = "sleep 2"
        p = subprocess.Popen([sys.executable, "-m", "containerd_py.daemon", "--listen", f"unix://{sock}", "--state", state], env=env)
        try:
            # wait for socket file to exist
            for _ in range(50):
                if Path(sock).exists():
                    break
                time.sleep(0.1)
            ch = _channel(f"unix://{sock}")

            # images create/list
            istub = images_grpc.ImagesStub(ch)
            istub.Create(images_pb2.CreateImageRequest(image=images_pb2.Image(name="demo:latest")))
            ilist = istub.List(images_pb2.ListImagesRequest())
            assert any(img.name == "demo:latest" for img in ilist.images)

            # containers create
            cstub = containers_grpc.ContainersStub(ch)
            cstub.Create(containers_pb2.CreateContainerRequest(container=containers_pb2.Container(id="c1", image="demo:latest")))

            # task start/list
            tstub = tasks_grpc.TasksStub(ch)
            sresp = tstub.Start(tasks_pb2.StartRequest(container_id="c1"))
            assert sresp.pid > 0
            lst = tstub.List(tasks_pb2.ListTasksRequest())
            assert any(p.id == "c1" for p in lst.tasks)

            # kill
            _ = tstub.Kill(tasks_pb2.KillRequest(container_id="c1", signal=15))
        finally:
            p.terminate()
            p.wait(timeout=5)