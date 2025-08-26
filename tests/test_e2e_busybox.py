import os
import shutil
import subprocess
import sys

import pytest


@pytest.mark.skip(reason="MVP features not implemented yet: pull/unpack/tasks")
@pytest.mark.parametrize("ref", ["docker.io/library/busybox:latest"]) 
def test_busybox_end_to_end(ref: str, tmp_path):
    addr = "unix:///run/py-containerd/py-containerd.sock"
    env = os.environ.copy()
    env["PY_CONTAINERD_ADDRESS"] = addr

    # start daemon
    daemon = subprocess.Popen([sys.executable, "-m", "py_containerd.daemon", "--listen", addr, "--state", str(tmp_path / "state")], env=env)
    try:
        # pull
        subprocess.check_call([sys.executable, "-m", "py_containerd.cli.main", "images", "pull", ref], env=env)
        # create
        subprocess.check_call([sys.executable, "-m", "py_containerd.cli.main", "containers", "create", ref, "e2e-demo"], env=env)
        # start
        subprocess.check_call([sys.executable, "-m", "py_containerd.cli.main", "tasks", "start", "e2e-demo"], env=env)
        # ps
        subprocess.check_call([sys.executable, "-m", "py_containerd.cli.main", "ps"], env=env)
        # logs
        subprocess.call([sys.executable, "-m", "py_containerd.cli.main", "logs", "e2e-demo"], env=env)
        # stop
        subprocess.call([sys.executable, "-m", "py_containerd.cli.main", "tasks", "kill", "e2e-demo", "SIGTERM"], env=env)
    finally:
        daemon.terminate()
        daemon.wait(timeout=5)