FROM pytorch/torchserve:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

USER root 
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get remove --purge python-setuptools
    && apt-get -yq update \
    && apt-get -yq install --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -yq update \ 
    && apt-get upgrade -yq \
    && apt-get autoremove -yq && apt-get autoclean -yq \ 
    && pip install --upgrade pip torch torchvision torchtext torchaudio setuptools future 

COPY run_server.sh run_server.sh
RUN chmod +x run_server.sh
USER model-server

ENTRYPOINT /home/model-server/run_server.sh
