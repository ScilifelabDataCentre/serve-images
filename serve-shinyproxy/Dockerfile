FROM openanalytics/shinyproxy:3.1.1

ENV SHINY_USER shinyproxy

RUN mkdir /opt/shinyproxy/config \
    && cp /opt/shinyproxy/application.yml /opt/shinyproxy/config \
    && rm /opt/shinyproxy/application.yml \ 
    && chown $SHINY_USER:$SHINY_USER /opt/shinyproxy/ /opt/shinyproxy/config

WORKDIR /opt/shinyproxy
USER $SHINY_USER

CMD ["java", "-noverify",  "-jar", "/opt/shinyproxy/shinyproxy.jar", "--spring.jmx.enabled=false", "--spring.config.location=/opt/shinyproxy/config/application.yml"]
