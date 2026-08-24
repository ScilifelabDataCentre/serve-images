FROM openanalytics/shinyproxy:3.2.4

ENV SHINY_USER=shinyproxy

RUN mkdir /opt/shinyproxy/config \
    && cp /opt/shinyproxy/application.yml /opt/shinyproxy/config \
    && rm /opt/shinyproxy/application.yml \
    && chown $SHINY_USER:$SHINY_USER /opt/shinyproxy/ /opt/shinyproxy/config

WORKDIR /opt/shinyproxy
USER $SHINY_USER

CMD ["java", "-Dsun.net.inetaddr.ttl=5", "-XX:MaxRAMPercentage=50.0", "-XX:MinRAMPercentage=20.0", "-XX:+ExitOnOutOfMemoryError", "-jar", "/opt/shinyproxy/shinyproxy.jar", "--spring.jmx.enabled=false", "--spring.config.location=/opt/shinyproxy/config/application.yml"]
