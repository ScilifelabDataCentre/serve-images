FROM jupyter/minimal-notebook:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

USER root
RUN apt-get update && apt-get install curl -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY cli /home/jovyan/cli
COPY examples /home/jovyan/work/examples
RUN chown -R jovyan /home/jovyan/cli \
    && chown -R jovyan /home/jovyan/work/examples

RUN npm install npm@latest -g \
    && npm cache clean --force \
    && npm -v

USER $NB_UID
RUN pip install --no-cache-dir mlflow boto3 /home/jovyan/cli/ \
    && pip install --no-cache-dir --force-reinstall "minio==7.0.2"
