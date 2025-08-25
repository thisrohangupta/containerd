### Migration: Go containerd to Python containerd-py

- Replaced Go daemons/CLI with Python 3.11 asyncio service and click-based CLI.
- gRPC API surface mirrored via generated Python stubs under `containerd_py/api/protos`.
- Minimal subset implemented for MVP: images.list, tasks.list (stubs), CLI commands print stub output.
- All Go code, make targets, vendor, and Go CI removed.

Known gaps:
- Full runtime integration with runc not implemented.
- Image pull/content store is stubbed.
- Many services unimplemented; tracked via issues with `parity-gap` label.

Compatibility:
- Unix socket default: `unix:///run/py-containerd/py-containerd.sock`.
- CLI entrypoints renamed to `containerd-py` and `ctr-py`.