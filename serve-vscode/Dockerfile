FROM ubuntu:latest

RUN apt-get update && apt-get install curl software-properties-common -y --no-install-recommends \
    && apt-get install python3.8 python3-pip -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install git git-lfs -y --no-install-recommends \
    && pip3 install --no-cache-dir git+https://@github.com/scaleoutsystems/stackn@feature/STACKN-267#subdirectory=cli

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -fsSL https://code-server.dev/install.sh | /bin/bash

RUN useradd -m stackn
USER stackn

CMD ["/bin/bash", "-c", "/usr/bin/code-server --auth=none --bind-addr=localhost:1234"]