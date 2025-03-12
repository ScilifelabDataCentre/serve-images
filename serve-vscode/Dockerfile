FROM ubuntu:latest

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    software-properties-common \
    git \
    git-lfs \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install code-server
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -fsSL https://code-server.dev/install.sh | sh

RUN useradd -m serve \
    && mkdir -p /home/serve \
    && chown -R serve:serve /home/serve

# Switch to non-root user
USER serve
WORKDIR /home/serve

# Create virtual environment and install Python packages
RUN python3 -m venv .venv
RUN /home/serve/.venv/bin/pip install --upgrade pip \
    && /home/serve/.venv/bin/pip install --no-cache-dir \
    jupyter

# Install Jupyter extension and configure environment
RUN code-server --install-extension ms-toolsai.jupyter
ENV PATH="/home/serve/.venv/bin:${PATH}"

# Install Python extension
RUN code-server --install-extension ms-python.python

# Configure Python path for VS Code
RUN mkdir -p /home/serve/.local/share/code-server/User \
    && echo '{"python.defaultInterpreterPath": "/home/serve/.venv/bin/python3"}' \
    > /home/serve/.local/share/code-server/User/settings.json

# Start code-server with Python from virtual environment
CMD ["/bin/bash", "-c", "/usr/bin/code-server --auth=none --bind-addr=0.0.0.0:1234 /home/serve/"]