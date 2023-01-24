FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq install \
        curl \
        python3 \
        python3-pip \
        python3-distutils \ 
        gcc \
    && apt-get -yq upgrade  \
    && pip install --upgrade pip setuptools \
    && pip install mlflow boto3 \
    && apt-get autoremove -yq && apt-get autoclean -yq \ 
    && rm -rf /var/lib/apt/lists/* 

COPY deploy.sh deploy.sh

RUN /bin/bash -c "chmod +x deploy.sh"

CMD ["deploy.sh"]