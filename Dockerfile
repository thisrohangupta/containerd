FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates curl runc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -e .

VOLUME ["/run/py-containerd", "/var/lib/py-containerd"]

EXPOSE 9090

ENTRYPOINT ["py-containerd", "--listen", "unix:///run/py-containerd/py-containerd.sock"]

