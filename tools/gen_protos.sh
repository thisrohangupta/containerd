#!/usr/bin/env bash
set -euo pipefail

# Generates Python gRPC code from containerd protobufs vendored under vendor/containerd
# Output goes to py_containerd/api/protos

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
VENDOR_DIR="$ROOT_DIR/vendor/containerd"
OUT_DIR="$ROOT_DIR/py_containerd/api/protos"
PROTO_ROOT="$ROOT_DIR/vendor/_proto"

mkdir -p "$OUT_DIR"
mkdir -p "$PROTO_ROOT/github.com/containerd"

# Map Go import path to filesystem path via symlink
if [ ! -e "$PROTO_ROOT/github.com/containerd/containerd" ]; then
  ln -sfn "$VENDOR_DIR" "$PROTO_ROOT/github.com/containerd/containerd"
fi

PY_BIN=${PY_BIN:-python3}

if ! command -v "$PY_BIN" >/dev/null 2>&1; then
  echo "$PY_BIN not found" >&2
  exit 1
fi

if ! "$PY_BIN" -c "import grpc_tools.protoc" 2>/dev/null; then
  echo "grpcio-tools not installed. Run: pip install -e .[dev]" >&2
  exit 1
fi

PROTO_INCLUDES=(
  "-I$PROTO_ROOT"
)

# Selected services for MVP
PROTOS=(
  github.com/containerd/containerd/api/services/images/v1/images.proto
  github.com/containerd/containerd/api/services/containers/v1/containers.proto
  github.com/containerd/containerd/api/services/tasks/v1/tasks.proto
  github.com/containerd/containerd/api/services/content/v1/content.proto
  github.com/containerd/containerd/api/types/task/task.proto
  github.com/containerd/containerd/api/types/mount.proto
  github.com/containerd/containerd/api/types/descriptor.proto
  github.com/containerd/containerd/api/types/metrics.proto
)

pushd "$ROOT_DIR" >/dev/null
"$PY_BIN" -m grpc_tools.protoc \
  ${PROTO_INCLUDES[@]} \
  --python_out="$OUT_DIR" \
  --grpc_python_out="$OUT_DIR" \
  ${PROTOS[@]}
popd >/dev/null

echo "Generated protos to $OUT_DIR"

# Ensure Python packages can import generated modules by adding __init__.py
find "$OUT_DIR" -type d -print0 | while IFS= read -r -d '' d; do
  if [ ! -f "$d/__init__.py" ]; then
    touch "$d/__init__.py"
  fi
done

