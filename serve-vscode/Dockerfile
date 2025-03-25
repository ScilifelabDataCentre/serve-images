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

# Create user with group id 1000 and assign permissions.
# User id is 1001 because 1000 is already assigned
# with default user 'ubuntu', which is auto-created 
# with this ubuntu image
RUN useradd -u 1001 -g 1000 -m serve && \
    mkdir -p /home/serve && \
    chown -R serve:1000 /home/serve && \
    chmod -R 770 /home/serve
    
# Switch to non-root user. Number instead of name is mandatory for 
# working 'runAsGroup' in chart after disabling 'runAsUser'
USER 1001
WORKDIR /home/serve

# Create virtual environment and install Jupyter
RUN python3 -m venv .venv
RUN /home/serve/.venv/bin/pip install --upgrade pip \
    && /home/serve/.venv/bin/pip install --no-cache-dir \
    jupyter

# Install VScode Python and Jupyter extension
RUN code-server --install-extension ms-python.python \
    && code-server --install-extension ms-toolsai.jupyter

# Configure environment and Python path for VS Code
ENV PATH="/home/serve/.venv/bin:${PATH}"

RUN mkdir -p /home/serve/.local/share/code-server/User \
    && echo '{"python.defaultInterpreterPath": "/home/serve/.venv/bin/python3"}' \
    > /home/serve/.local/share/code-server/User/settings.json

# Start code-server with Python from virtual environment
CMD ["/bin/bash", "-c", "/usr/bin/code-server --auth=none --bind-addr=0.0.0.0:1234 /home/serve/"]