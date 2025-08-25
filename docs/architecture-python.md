# Python Architecture Mapping

This document maps key Go components to their Python counterparts for the minimal lifecycle subset.

- Go `cmd/containerd` -> Python `containerd_py.daemon` (grpc aio server)
- Go `cmd/ctr` -> Python CLI `containerd_py.cli.main`
- Go `api/services/*` -> Python gRPC stubs in `containerd_py/api/protos/...`
- Go `pkg/*` runtime/image abstractions -> Python modules:
  - Images: `containerd_py.images`
  - Containers: `containerd_py.tasks` (MVP combines container+task)
  - Content: `containerd_py.content`
  - State: `containerd_py.state`

MVP scope:
- images.pull (stub/simulation)
- containers.create (stub)
- tasks.start, tasks.kill, list, delete (simulation mode, no root required)

Simulation mode stores state under `~/.local/share/containerd-py/state.json` and spawns subprocesses for start/kill when permitted.

