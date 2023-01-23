FROM ubuntu:latest

RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install curl -y

RUN apt install python3.8 -y
RUN apt install python3-pip -y

RUN apt install git -y
RUN apt install git-lfs -y
RUN pip3 install git+https://@github.com/scaleoutsystems/stackn@feature/STACKN-267#subdirectory=cli

RUN curl -fsSL https://code-server.dev/install.sh | sh

RUN useradd -m stackn
USER stackn

CMD /usr/bin/code-server --auth=none --bind-addr=localhost:1234