FROM jupyter/minimal-notebook:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

USER root
RUN /bin/bash -c "apt update"
RUN /bin/bash -c "apt install curl -y"
COPY cli /home/jovyan/cli
COPY examples /home/jovyan/work/examples
RUN chown -R jovyan /home/jovyan/cli
RUN chown -R jovyan /home/jovyan/work/examples

USER $NB_UID
RUN pip install mlflow boto3
RUN pip uninstall minio -y
RUN pip install minio==7.0.2

RUN pip install /home/jovyan/cli/
