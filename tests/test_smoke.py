import subprocess
import sys


def test_cli_help():
    out = subprocess.check_output([sys.executable, "-m", "py_containerd.cli.main", "--help"]).decode()
    assert "Usage:" in out

