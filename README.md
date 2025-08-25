## containerd-py

Python reimplementation of containerd's control plane (subset), exposing API-compatible gRPC services for Images, Content, Containers, and Tasks. Uses OCI runtimes (e.g., `runc`) for execution.

### Status
- MVP scaffolding in progress. Supports daemon startup and CLI skeleton.

### Quickstart
```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .

# Start the daemon
containerd-py --listen unix:///run/py-containerd/py-containerd.sock

# CLI help
ctr-py --help
```

### Goals
- gRPC parity (subset) with containerd for Images, Content, Containers, Tasks
- Local OCI CAS content store
- Image pull/unpack
- Task execution via `runc`

### Repository Layout
- `containerd_py/`: Python package
- `docs/`: Architecture, quickstart, limitations
- `scripts/`: Demo scripts
- `tests/`: E2E tests

### License
Apache-2.0

![containerd banner light mode](https://raw.githubusercontent.com/cncf/artwork/master/projects/containerd/horizontal/color/containerd-horizontal-color.png#gh-light-mode-only)
![containerd banner dark mode](https://raw.githubusercontent.com/cncf/artwork/master/projects/containerd/horizontal/white/containerd-horizontal-white.png#gh-dark-mode-only)