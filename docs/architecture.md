### Architecture Overview

- **Daemon (`py-containerd`)**: asyncio process exposing gRPC services compatible with containerd (subset). Maintains state under `/var/lib/py-containerd`.
- **gRPC Services**: Images, Content, Containers, Tasks. Python stubs generated from containerd protobufs.
- **Content Store**: Local OCI CAS layout with blobs and indexes, GC safe via reference counts.
- **Image Manager**: Pulls from OCI registries, verifies descriptors, unpacks to runtime bundle.
- **Task Executor**: Spawns `runc` for create/start/kill, adheres to OCI Runtime Spec.
- **CLI (`pyctr`)**: Thin client mirroring containerd commands.

Data flows: CLI -> gRPC -> Managers -> Content Store / Executor.

Security: Least privilege, no default privileged containers, UID/GID mapping where applicable.

