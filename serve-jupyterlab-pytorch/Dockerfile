FROM quay.io/jupyter/pytorch-notebook:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/serve-images

ARG SERVE_BRANCH=develop
WORKDIR /home/jovyan

COPY requirements.txt /tmp

USER root
RUN apt-get update && apt-get install curl -y --no-install-recommends \
    && apt-get clean \
    && apt-get install git-lfs  -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    tcl \
    tcl-dev \
    environment-modules && \
    rm -rf /var/lib/apt/lists/*

# Download and extract modules-5.5.0
WORKDIR /tmp
RUN wget https://github.com/cea-hpc/modules/releases/download/v5.5.0/modules-5.5.0.tar.gz -nv \
    && tar -xzf modules-5.5.0.tar.gz \
    && rm modules-5.5.0.tar.gz

# Build and install from the extracted directory
WORKDIR /tmp/modules-5.5.0
RUN ./configure --prefix=/usr/local \
    && make \
    && make install

# Clean up the source directory
WORKDIR /tmp
RUN rm -rf /tmp/modules-5.5.0

# Set up the environment for modules
RUN echo "source /usr/local/init/bash" >> /etc/bash.bashrc

WORKDIR /home/jovyan

USER $NB_UID
RUN pip install --no-cache-dir -r /tmp/requirements.txt


CMD ["/bin/bash"]