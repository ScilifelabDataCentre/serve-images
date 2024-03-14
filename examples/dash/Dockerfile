FROM python:3.8-slim

ENV USER=serve
ENV HOME=/home/$USER

RUN apt-get update -yq \
    && useradd -m $USER \
    && pip install --upgrade --no-cache-dir pip \ 
    && rm -rf /var/lib/apt/lists/* 

COPY . $HOME/

RUN pip install --no-cache-dir --upgrade pip \ 
    && pip install --no-cache-dir -r $HOME/requirements.txt

USER $USER
EXPOSE 8000
WORKDIR $HOME

ENTRYPOINT ["gunicorn", "app:server", "-b", "0.0.0.0:8000"]
