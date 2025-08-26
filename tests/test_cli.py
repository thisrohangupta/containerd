import subprocess
import sys


def run_cli(*args: str) -> str:
    return subprocess.check_output([sys.executable, "-m", "py_containerd.cli.main", *args]).decode()


def test_cli_help():
    out = run_cli("--help")
    assert "Usage:" in out


def test_cli_images_pull_stub():
    out = run_cli("images", "pull", "busybox:latest")
    assert "[stub] Pulling image busybox:latest" in out


def test_cli_containers_create_stub():
    out = run_cli("containers", "create", "busybox:latest", "demo")
    assert "[stub] Creating container demo from busybox:latest" in out


def test_cli_tasks_start_kill_stub():
    out = run_cli("tasks", "start", "demo")
    assert "[stub] Starting task demo" in out
    out = run_cli("tasks", "kill", "demo", "SIGTERM")
    assert "[stub] Killing task demo with SIGTERM" in out