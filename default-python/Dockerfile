# FROM python:3
FROM ubuntu:18.04

RUN /bin/bash -c "apt update"
RUN /bin/bash -c "apt install python3.7-dev -y"
RUN /bin/bash -c "apt install curl -y"
RUN /bin/bash -c "apt-get install python3-distutils -y"
RUN /bin/bash -c "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
RUN /bin/bash -c "python3.7 get-pip.py"
RUN /bin/bash -c "apt install gcc -y"
RUN /bin/bash -c "update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1"
RUN /bin/bash -c "pip3 install --upgrade pip"
# RUN /bin/bash -c "apt update"
# RUN /bin/bash -c "curl https://dl.min.io/client/mc/release/linux-amd64/mc --output mc && chmod +x mc"
COPY requirements.txt requirements.txt
RUN /bin/bash -c "pip3 install -r requirements.txt"

COPY serve.py serve.py
COPY deploy.sh deploy.sh

RUN /bin/bash -c "chmod +x deploy.sh"

CMD ./deploy.sh