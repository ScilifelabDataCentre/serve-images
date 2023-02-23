FROM ubuntu:20.04 as base

SHELL ["/bin/bash", "-c"]

# Install useful Linux packages and cleanup
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq install --no-install-recommends \
      curl \
      dpkg-sig \
      libpq5 \
      psmisc \
      sudo \
      lsb-release \
      libclang-dev \
      locales \
      ca-certificates 

ARG RSTUDIO_ARCH="amd64"
ARG RSTUDIO_VERSION=2022.12.0+353

RUN curl -sL "https://download2.rstudio.org/server/bionic/${RSTUDIO_ARCH}/rstudio-server-${RSTUDIO_VERSION//+/-}-${RSTUDIO_ARCH}.deb" -o /tmp/rstudio-server.deb \
 && gpg --keyserver keys.gnupg.net --keyserver pgp.surfnet.nl --recv-keys 3F32EE77E331692F \
 && dpkg-sig --verify /tmp/rstudio-server.deb \
 && dpkg -i /tmp/rstudio-server.deb \
 && rm -f /tmp/rstudio-server.deb \
 && echo "lock-type=advisory" > /etc/rstudio/file-locks \
 && echo "www-frame-origin=same" >> /etc/rstudio/rserver.conf

FROM ubuntu:20.04 as build

# Common environment variables
ENV USER jovyan
ENV GROUP users
ENV PASSWORD default
ENV DISABLE_AUTH 1
ENV UID 1000
ENV HOME /home/$USER

# Set locale configs
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Install useful Linux packages and cleanup
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq install --no-install-recommends \
      locales \
      libpq5 \
      psmisc \
      sudo \
      lsb-release \
      libclang-dev \
      libxml2 \ 
      libodbc1 \
      libglpk-dev \
      r-base \
      r-base-dev \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -yq update \ 
    && apt-get autoremove -yq && apt-get autoclean -yq


RUN useradd -s /bin/bash -N -u ${UID} -l ${USER} \
    && mkdir -p ${HOME} \
    && chown -R ${USER}:${GROUP} ${HOME} \
    && echo "${USER}:password123" | chpasswd

ENV R_HOME usr/lib/R

# R needs TZ set
RUN echo "TZ=Etc/UTC" >> ${R_HOME}/etc/Renviron.site

# Set default CRAN repo to RSPM (it has pre-compiled R packages, increasing user install speed)
RUN echo 'options(repos=c(CRAN="https://packagemanager.rstudio.com/all/__linux__/focal/latest"))' >>  ${R_HOME}/etc/Rprofile.site \
 && echo 'options(HTTPUserAgent=sprintf("R/%s R (%s)", getRversion(), paste(getRversion(), R.version$platform, R.version$arch, R.version$os)))' >> ${R_HOME}/etc/Rprofile.site

COPY --from=base --chown=${USER}:${GROUP} /etc/rstudio/ /etc/rstudio/
COPY --from=base --chown=${USER}:${GROUP} /var/run/rstudio-server/ /var/run/rstudio-server/
COPY --from=base --chown=${USER}:${GROUP} /usr/lib/rstudio-server/ /usr/lib/rstudio-server/
COPY --from=base --chown=${USER}:${GROUP} /var/lib/rstudio-server/ /var/lib/rstudio-server/

WORKDIR $HOME

COPY run.sh /etc/run.sh

RUN chown ${USER}:${GROUP} /etc/run.sh \
    && chmod +x /etc/run.sh

USER ${USER}
EXPOSE 8787

ENTRYPOINT ["/etc/run.sh"]
