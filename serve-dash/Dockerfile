FROM ubuntu:18.04

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq upgrade  \
    && apt-get install --no-install-recommends -y python3.7-dev curl python3-distutils gcc \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.7 get-pip.py \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 \
    && pip3 install --upgrade --no-cache-dir pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home

COPY deploy.sh deploy.sh
COPY run_server.sh run_server.sh
COPY requirements.txt requirements.txt
RUN pip3 install -r --no-cache-dir requirements.txt \
    && chmod +x deploy.sh run_server.sh

CMD ["/deploy.sh"]