FROM pytorch/torchserve:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

ENV MODEL_STORE=models
USER root 

COPY tests/run_server.test.sh /home/model-server/run_server.sh

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq upgrade  \
    && pip install --upgrade --no-cache-dir pip future setuptools wheel \
    && pip install --upgrade --no-cache-dir torch torchvision torchaudio torchtext --extra-index-url https://download.pytorch.org/whl/cpu \
    && pip cache purge \
    && rm -rf /home/venv \
    && apt-get autoremove -yq && apt-get autoclean -yq \ 
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.gradle \
    && chmod +x /home/model-server/run_server.sh

USER model-server

RUN mkdir -p model-store/$MODEL_STORE
WORKDIR /home/model-server

ENTRYPOINT ["/home/model-server/run_server.sh"]
