FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install R and RStudio Server dependencies
RUN apt-get update -qq\
  && apt-get install -yq \
    gdebi-core \
    dpkg-sig \
    libapparmor1 \
    libedit2 \
    libssl1.1 \
    lsb-release \
    psmisc \
    python3-setuptools \
    sudo \
    wget \
    libclang-dev \
    libcairo2-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libv8-dev \
    libjpeg-dev \
    libprotobuf-dev \
    protobuf-compiler \ 
    r-base

# Create a non-root user
ENV DEFAULT_USER=rstudio-server

# Obtain key
RUN gpg --keyserver keyserver.ubuntu.com --recv-keys 3F32EE77E331692F

# Download, verify and install RStudio Server
RUN wget https://download2.rstudio.org/server/bionic/amd64/rstudio-server-2022.12.0-353-amd64.deb -O rstudio-download.deb && \
  dpkg-sig --verify rstudio-download.deb && \
  gdebi --non-interactive rstudio-download.deb && \
  rm rstudio-download.deb && \
  
RUN mkdir -p /home/rstudio-server/.config/rstudio /home/rstudio-server/.local/share/rstudio  && \ 
    chown -R rstudio-server:rstudio-server /home/rstudio-server && \ 
    rm -rf /home/rstudio-server/R

## RStudio wants an /etc/R, will populate from $R_HOME/etc
RUN mkdir -p /etc/R

ENV R_BIN=/usr/bin/R
ENV RSTUDIO_CONFIG_DIR=/home/$DEFAULT_USER/.config/rstudio
ENV RSTUDIO_CONFIG_HOME=/home/$DEFAULT_USER/.config/rstudio
ENV RSTUDIO_DATA_HOME=/home/$DEFAULT_USER/.local/share/rstudio


RUN echo "rsession-which-r=${R_BIN}" >$RSTUDIO_CONFIG_DIR/rserver.conf && \
    echo "auth-minimum-user-id=999"  >> $RSTUDIO_CONFIG_DIR/rserver.conf && \
    echo "server-daemonize=0" >> $RSTUDIO_CONFIG_DIR/rserver.conf && \
    echo "auth-validate-users=0" >> $RSTUDIO_CONFIG_DIR/rserver.conf && \
    echo "auth-none=1" >> $RSTUDIO_CONFIG_DIR/rserver.conf && \
    echo "server-data-dir=/home/$DEFAULT_USER" && \
    echo "rsession-path=/usr/lib/rstudio-server/bin/rsession" 

# Set the working directory
WORKDIR /home/$DEFAULT_USER

COPY start-rstudio-server.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-rstudio-server.sh

ENTRYPOINT ["/usr/local/bin/start-rstudio-server.sh"] 
EXPOSE 8787
