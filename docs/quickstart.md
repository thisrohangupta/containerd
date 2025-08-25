### Quickstart

Prerequisites: Linux host, Python 3.11+, `runc` installed.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .[dev]

# Generate protos (requires vendored containerd in vendor/containerd)
make proto

# Run daemon
containerd-py --listen unix:///run/py-containerd/py-containerd.sock

# In another shell
ctr-py images pull docker.io/library/busybox:latest
ctr-py containers create docker.io/library/busybox:latest demo
ctr-py tasks start demo
ctr-py ps
ctr-py logs demo
ctr-py tasks kill demo SIGTERM
```

