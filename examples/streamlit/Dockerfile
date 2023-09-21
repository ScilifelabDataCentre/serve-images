FROM python:3.9-slim


ENV USER=username
ENV HOME=/home/$USER
RUN useradd -m -u 1000 $USER


WORKDIR $HOME/app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common \ 
    curl

COPY requirements.txt requirements.txt
COPY app.py app.py
COPY start-script.sh start-script.sh

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x start-script.sh \
    && chown -R $USER:$USER $HOME \ 
    && rm -rf /var/lib/apt/lists/*

USER $USER
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
