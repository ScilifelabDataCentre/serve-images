FROM pytorch/torchserve:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

USER root 

COPY run_server.sh /home/model-server/run_server.sh

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq upgrade  \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x /home/model-server/run_server.sh

USER model-server

WORKDIR /home/model-server

ENTRYPOINT ["/home/model-server/run_server.sh"]
