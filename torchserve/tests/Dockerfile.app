FROM pytorch/torchserve:latest
LABEL org.opencontainers.image.source https://github.com/scilifelabdatacentre/stackn-images

ENV MODEL_STORE=models
COPY run_server.test.sh run_server.sh

USER root
RUN chmod +x run_server.sh
USER model-server
RUN mkdir -p model-store/$MODEL_STORE
COPY models/* model-store/$MODEL_STORE/

CMD /home/model-server/run_server.sh