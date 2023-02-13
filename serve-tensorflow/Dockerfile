FROM tensorflow/serving:latest-devel as builder
FROM ubuntu:20.04

ENV USER=jovyan
ENV HOME=/home/$USER

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/tensorflow_model_server /usr/bin/tensorflow_model_server

EXPOSE 8500
EXPOSE 8501

ENV MODEL_BASE_PATH=$HOME/models
ENV MODEL_NAME=model

RUN useradd -m $USER \
    && mkdir -p $MODEL_BASE_PATH \
    && chown -R $USER:$USER $MODEL_BASE_PATH

WORKDIR $HOME
USER $USER

ENTRYPOINT ["tensorflow_model_server", "--port=8500", "--rest_api_port=8501", "--model_name=${MODEL_NAME}" ,"--model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME}"]

