### Quickstart

Prerequisites: Linux host, Python 3.11+, `runc` installed.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .[dev]

# Generate protos (requires vendored containerd in vendor/containerd)
make proto

# Run daemon
py-containerd --listen unix:///run/py-containerd/py-containerd.sock

# In another shell
pyctr images pull docker.io/library/busybox:latest
pyctr containers create docker.io/library/busybox:latest demo
pyctr tasks start demo
pyctr ps
pyctr logs demo
pyctr tasks kill demo SIGTERM
```

