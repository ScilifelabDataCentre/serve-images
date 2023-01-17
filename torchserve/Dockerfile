FROM pytorch/torchserve:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

COPY run_server.sh run_server.sh
USER root
RUN chmod +x run_server.sh
USER model-server
ENTRYPOINT /home/model-server/run_server.sh
