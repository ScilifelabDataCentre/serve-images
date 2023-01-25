FROM jupyter/minimal-notebook:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

USER root
RUN apt-get update && apt-get install curl -y

COPY cli /home/jovyan/cli
COPY examples /home/jovyan/work/examples
RUN chown -R jovyan /home/jovyan/cli && \
    chown -R jovyan /home/jovyan/work/examples

USER $NB_UID
RUN pip install mlflow boto3 /home/jovyan/cli/ && \
    pip install --force-reinstall "minio==7.0.2"
