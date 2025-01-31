FROM jupyter/minimal-notebook:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/serve-images

ARG SERVE_BRANCH=develop
WORKDIR /home/jovyan

COPY requirements.txt /tmp

USER root
RUN apt-get update && apt-get install curl -y --no-install-recommends \
    && apt-get clean \
    && apt-get install git-lfs \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID
RUN pip install --no-cache-dir -r /tmp/requirements.txt
