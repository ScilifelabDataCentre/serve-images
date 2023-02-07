FROM pytorch/torchserve:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

COPY run_server.sh run_server.sh
USER root 

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq upgrade  \
    && pip install --upgrade pip future setuptools wheel \
    && pip install --upgrade torch torchvision torchaudio torchtext --extra-index-url https://download.pytorch.org/whl/cpu \
    && pip cache purge \
    && rm -rf /home/venv \
    && apt-get autoremove -yq && apt-get autoclean -yq \ 
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.gradle \
    && chmod +x run_server.sh

USER model-server

ENTRYPOINT /home/model-server/run_server.sh