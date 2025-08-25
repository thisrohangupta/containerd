#!/usr/bin/env bash
set -euo pipefail

ADDR="unix:///run/py-containerd/py-containerd.sock"

echo "Starting daemon..."
py-containerd --listen "$ADDR" &
DAEMON_PID=$!
trap "kill $DAEMON_PID || true" EXIT

sleep 1

echo "Pulling busybox..."
pyctr --address "$ADDR" images pull docker.io/library/busybox:latest

echo "Creating container..."
pyctr --address "$ADDR" containers create docker.io/library/busybox:latest demo

echo "Starting task..."
pyctr --address "$ADDR" tasks start demo

echo "Listing tasks..."
pyctr --address "$ADDR" ps

echo "Tailing logs..."
pyctr --address "$ADDR" logs demo || true

echo "Stopping..."
pyctr --address "$ADDR" tasks kill demo SIGTERM || true

wait $DAEMON_PID || true

