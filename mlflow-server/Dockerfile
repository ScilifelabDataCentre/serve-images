FROM ubuntu:20.04

ENV USER=jovyan

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq install \
        curl \
        python3 \
        python3-pip \
        python3-distutils \ 
        gcc \
    && apt-get -yq upgrade  \
    && apt-get autoremove -yq && apt-get autoclean -yq \ 
    && rm -rf /var/lib/apt/lists/* 

RUN useradd -m $USER \
    && mkdir -p home/$USER/mlruns \
    && chown -R $USER:$USER home/$USER/mlruns

COPY deploy.sh deploy.sh
RUN chmod +x deploy.sh

RUN pip install --upgrade pip setuptools \
    && pip install mlflow boto3 \
    && pip install --upgrade numba 

WORKDIR /home/$USER
USER $USER

CMD ["./deploy.sh"]