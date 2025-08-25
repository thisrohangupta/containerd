import asyncio
import logging
import os
import signal
from typing import Optional

import grpc

from py_containerd.server.grpc_server import create_server


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


async def serve(listen: str, state_dir: str) -> None:
    server = await create_server(state_dir)

    if listen.startswith("unix://"):
        path = listen[len("unix://") :]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path):
            os.remove(path)
        server.add_insecure_port(listen)
    else:
        server.add_insecure_port(listen)

    await server.start()
    logging.getLogger(__name__).info("py-containerd listening on %s", listen)

    # Handle shutdown signals
    stop_event = asyncio.Event()

    loop = asyncio.get_running_loop()

    def _signal_handler() -> None:
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _signal_handler)
        except NotImplementedError:
            pass

    await stop_event.wait()
    await server.stop(grace=None)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser("py-containerd")
    parser.add_argument(
        "--listen",
        default="unix:///run/py-containerd/py-containerd.sock",
        help="gRPC listen address (unix:///path or 0.0.0.0:9090)",
    )
    parser.add_argument(
        "--state",
        default="/var/lib/py-containerd",
        help="State directory for metadata and runtime state",
    )
    args = parser.parse_args()

    configure_logging()
    asyncio.run(serve(args.listen, args.state))


if __name__ == "__main__":
    main()

