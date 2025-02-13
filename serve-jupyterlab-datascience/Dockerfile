FROM quay.io/jupyter/datascience-notebook:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/serve-images

ARG SERVE_BRANCH=develop
WORKDIR /home/jovyan

USER root
RUN apt-get update && apt-get install curl -y --no-install-recommends \
    && apt-get clean \
    && apt-get install git-lfs  -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && rm /opt/conda/lib/R/library/gargle/extdata/fake_service_account.json

USER $NB_UID
