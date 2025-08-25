# Contributing

## Dev setup

- Python 3.11+
- Create venv and install dev deps:

```bash
python -m venv .venv --without-pip
curl -sS https://bootstrap.pypa.io/get-pip.py -o .venv/get-pip.py
. .venv/bin/activate
python .venv/get-pip.py
pip install -e .[dev]
```

## Tooling
- Lint: ruff (configured via .ruff.toml)
- Format: black (via ruff format or black)
- Types: mypy (strict)
- Tests: pytest (+ pytest-asyncio)

## Running
- Daemon: `containerd-py --listen unix:///run/py-containerd/py-containerd.sock`
- CLI: `ctr-py --help`

## Protos
- Generated stubs live in `containerd_py/api/protos`. Use `make proto` if you have source protos available.
