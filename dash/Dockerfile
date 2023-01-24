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

COPY requirements.txt requirements.txt
RUN /bin/bash -c "pip3 install -r requirements.txt"

COPY deploy.sh /deploy.sh
RUN /bin/bash -c "chmod +x /deploy.sh"
COPY run_server.sh /run_server.sh
RUN /bin/bash -c "chmod +x /run_server.sh"
CMD /deploy.sh