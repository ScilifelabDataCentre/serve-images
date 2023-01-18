FROM ubuntu:latest

# RUN apt update
# RUN apt install python3.7 -y

RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install curl -y

RUN apt install python3.8 -y
RUN apt install python3-pip -y

# RUN apt-get install python3-distutils -y
# RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# RUN python3.7 get-pip.py
# RUN apt install gcc -y
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
# RUN pip3 install --upgrade pip

RUN apt install git -y
RUN apt install git-lfs -y
RUN pip3 install git+https://@github.com/scaleoutsystems/stackn@feature/STACKN-267#subdirectory=cli

# RUN /bin/bash -c "apt update"
# RUN /bin/bash -c "apt install curl -y"
RUN curl -fsSL https://code-server.dev/install.sh | sh

RUN useradd -m stackn
USER stackn

CMD /usr/bin/code-server --auth=none --bind-addr=localhost:1234