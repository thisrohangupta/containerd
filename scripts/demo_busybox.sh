#!/usr/bin/env bash
set -euo pipefail

ADDR="unix:///run/py-containerd/py-containerd.sock"

echo "Starting daemon..."
containerd-py --listen "$ADDR" &
DAEMON_PID=$!
trap "kill $DAEMON_PID || true" EXIT

sleep 1

echo "Pulling busybox..."
ctr-py --address "$ADDR" images pull docker.io/library/busybox:latest

echo "Creating container..."
ctr-py --address "$ADDR" containers create docker.io/library/busybox:latest demo

echo "Starting task..."
ctr-py --address "$ADDR" tasks start demo

echo "Listing tasks..."
ctr-py --address "$ADDR" ps

echo "Tailing logs..."
ctr-py --address "$ADDR" logs demo || true

echo "Stopping..."
ctr-py --address "$ADDR" tasks kill demo SIGTERM || true

wait $DAEMON_PID || true

