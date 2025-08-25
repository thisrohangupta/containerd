### Limitations (MVP)

- Subset of containerd APIs only (Images, Content, Containers, Tasks).
- Linux only; no Windows support.
- Basic snapshotting using unpack-to-bundle; no advanced snapshotters.
- Networking: relies on host defaults; no CNI or CRI shim integration.
- Metrics exposed via simple HTTP endpoint (TBD).

