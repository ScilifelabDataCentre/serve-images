FROM filebrowser/filebrowser

ARG USER=serve
ARG HOME=/home/$USER

COPY filebrowser.json /.filebrowser.json

COPY startup.sh /usr/local/bin/startup.sh
RUN apk add --update --no-cache \
    wget~=1.21 \
    zip~=3 \
    unzip~=6 \
    && adduser -D -u 1000 -g 1000 -h $HOME $USER \
    && chmod +x /usr/local/bin/startup.sh \
    && rm -rf /var/lib/apt/lists/*

COPY branding/ $HOME/branding

USER $USER
ENTRYPOINT [ "/usr/local/bin/startup.sh" ]
