FROM pytorch/torchserve:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

USER root 
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq upgrade  \
    && pip install --upgrade pip torch torchvision torchtext torchaudio future setuptools wheel \
    && rm -rf /home/venv \
    && apt-get autoremove -yq && apt-get autoclean -yq \ 
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.gradle \
    && chmod +x run_server.sh

COPY run_server.sh run_server.sh
RUN chmod +x /home/model-server/run_server.sh
USER model-server

ENTRYPOINT /home/model-server/run_server.sh
