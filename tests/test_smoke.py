import subprocess
import sys


def test_cli_help():
    out = subprocess.check_output([sys.executable, "-m", "containerd_py.cli.main", "--help"]).decode()
    assert "Usage:" in out

