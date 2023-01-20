FROM ubuntu:20.04

# Common environment variables
ENV NB_USER jovyan
ENV NB_UID 1000
ENV HOME /home/$NB_USER

# Arguments for software versions
ARG S6_ARCH="amd64"
ARG S6_VERSION=v2.2.0.3
ARG RSTUDIO_ARCH="amd64"
ARG RSTUDIO_VERSION=2022.12.0+353

# Set shell to bash
SHELL ["/bin/bash", "-c"]

# Install useful Linux packages and cleanup
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq install --no-install-recommends \
      apt-transport-https \
      bash \
      bzip2 \
      ca-certificates \
      curl \
      git \
      gnupg \
      gnupg2 \
      locales \
      lsb-release \
      nano \
      software-properties-common \
      tzdata \
      unzip \
      vim \
      wget \
      zip \
      dpkg-sig \
      libapparmor1 \
      libc6 \
      libclang-dev \
      libedit2 \
      libpq5 \
      psmisc \
      rrdtool \
      sudo \
      r-base \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -yq update \ 
    && apt-get autoremove -yq && apt-get autoclean -yq

# Create user and set permissions
RUN useradd -M -s /bin/bash -N -u ${NB_UID} ${NB_USER} \
   && mkdir -p ${HOME} \
   && chown -R ${NB_USER}:users ${HOME} \
   && mkdir ${HOME}/.gnupg \
   && chmod 700 ${HOME}/.gnupg

# Install - s6 overlay
RUN export GNUPGHOME=/tmp/ \
   && curl -sL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-${S6_ARCH}-installer" -o /tmp/s6-overlay-${S6_VERSION}-installer \
   && curl -sL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-${S6_ARCH}-installer.sig" -o /tmp/s6-overlay-${S6_VERSION}-installer.sig \
   && gpg --keyserver keys.gnupg.net --keyserver pgp.surfnet.nl --recv-keys 6101B2783B2FD161 \
   && gpg -q --verify /tmp/s6-overlay-${S6_VERSION}-installer.sig /tmp/s6-overlay-${S6_VERSION}-installer \
   && chmod +x /tmp/s6-overlay-${S6_VERSION}-installer \
   && /tmp/s6-overlay-${S6_VERSION}-installer / \
   && rm /tmp/s6-overlay-${S6_VERSION}-installer.sig /tmp/s6-overlay-${S6_VERSION}-installer \ 
   && chown -R ${NB_USER}:users /usr/local/bin \
   && chown -R ${NB_USER}:users /etc/s6

# Set locale configs
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

ENV R_HOME usr/lib/R

# R needs TZ set
ENV TZ Etc/UTC
RUN echo "TZ=${TZ}" >> ${R_HOME}/etc/Renviron.site

# Set default CRAN repo to RSPM (it has pre-compiled R packages, increasing user install speed)
ENV R_HOME usr/lib/R
RUN echo 'options(repos=c(CRAN="https://packagemanager.rstudio.com/all/__linux__/focal/latest"))' >>  ${R_HOME}/etc/Rprofile.site \
 && echo 'options(HTTPUserAgent=sprintf("R/%s R (%s)", getRversion(), paste(getRversion(), R.version$platform, R.version$arch, R.version$os)))' >> ${R_HOME}/etc/Rprofile.site

RUN curl -sL "https://download2.rstudio.org/server/bionic/${RSTUDIO_ARCH}/rstudio-server-${RSTUDIO_VERSION//+/-}-${RSTUDIO_ARCH}.deb" -o /tmp/rstudio-server.deb \
 && gpg --keyserver keys.gnupg.net --keyserver pgp.surfnet.nl --recv-keys 3F32EE77E331692F \
 && dpkg-sig --verify /tmp/rstudio-server.deb \
 && dpkg -i /tmp/rstudio-server.deb \
 && rm -f /tmp/rstudio-server.deb \
 && mv -n /var/run/rstudio-server* /run \
 && echo "lock-type=advisory" > /etc/rstudio/file-locks \
 && echo "www-frame-origin=same" >> /etc/rstudio/rserver.conf \
 && chown -R ${NB_USER}:users /etc/rstudio \
 && chown -R ${NB_USER}:users /run/rstudio-server* \
 && chown -R ${NB_USER}:users /usr/lib/rstudio-server \
 && chown -R ${NB_USER}:users /var/lib/rstudio-server

# s6 - copy scripts
COPY --chown=${NB_USER}:users s6/ /etc

# s6 - 01-copy-tmp-home
RUN mkdir -p /tmp_home \
 && cp -r ${HOME} /tmp_home \
 && chown -R ${NB_USER}:users /tmp_home

USER ${NB_UID}
EXPOSE 8787
ENTRYPOINT ["/init"]
