#!/usr/bin/env bash
set -euo pipefail

# Fetch and vendor containerd repository for proto generation.

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
VENDOR_DIR="$ROOT_DIR/vendor/containerd"
CONTAINERD_REF="v2.0.0" # adjust as needed

mkdir -p "$ROOT_DIR/vendor"

if [ ! -d "$VENDOR_DIR/.git" ]; then
  git clone --depth 1 --branch "$CONTAINERD_REF" https://github.com/containerd/containerd "$VENDOR_DIR"
else
  git -C "$VENDOR_DIR" fetch --depth 1 origin "$CONTAINERD_REF"
  git -C "$VENDOR_DIR" checkout -q "$CONTAINERD_REF"
fi

echo "Vendored containerd at $CONTAINERD_REF in $VENDOR_DIR"

