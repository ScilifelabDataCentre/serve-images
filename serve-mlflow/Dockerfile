FROM ubuntu:20.04

ENV USER=jovyan
ENV HOME=/home/$USER

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq install --no-install-recommends\
        curl \
        git \
        python3 \
        python3-pip \
        python3-distutils \ 
        gcc \
        build-essential \ 
        libssl-dev \
        zlib1g-dev \ 
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        libncursesw5-dev \
        xz-utils tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libffi-dev \
        liblzma-dev \
    && apt-get -yq upgrade  \
    && apt-get autoremove -yq && apt-get autoclean -yq \ 
    && rm -rf /var/lib/apt/lists/* 

RUN useradd -m $USER \
    && mkdir -p $HOME/mlruns \
    && chown -R $USER:$USER $HOME/mlruns

RUN pip install --upgrade --no-cache-dir pip setuptools \
    && pip install --no-cache-dir mlflow boto3 virtualenv \
    && pip install --no-cache-dir --upgrade numba

WORKDIR $HOME 
USER $USER

# Setup PYENV
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl https://pyenv.run | bash
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
