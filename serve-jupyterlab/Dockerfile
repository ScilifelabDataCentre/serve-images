FROM jupyter/minimal-notebook:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/serve-images

ARG SERVE_BRANCH=develop
WORKDIR /home/jovyan

COPY requirements.txt /tmp

USER root
RUN apt-get update && apt-get install curl -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone -b $SERVE_BRANCH https://github.com/ScilifelabDataCentre/stackn /tmp/serve \
    && mv /tmp/serve/examples /home/jovyan/work \
    && rm -rf /tmp/serve \
    && chown -R jovyan /home/jovyan/work/examples \
    && chgrp -R $NB_GID /home/jovyan/work/examples

RUN npm remove package-lock.json \
    && npm install npm@9.8.1 -g \
    && npm cache clean --force \
    && npm -v


USER $NB_UID
RUN pip install --no-cache-dir -r /tmp/requirements.txt
