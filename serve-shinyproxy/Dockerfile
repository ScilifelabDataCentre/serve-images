FROM openanalytics/shinyproxy:3.0.2

ENV SHINY_USER shinyproxy
RUN chown $SHINY_USER:$SHINY_USER /opt/shinyproxy/

WORKDIR /opt/shinyproxy
USER $SHINY_USER

CMD ["java", "-noverify",  "-jar", "/opt/shinyproxy/shinyproxy.jar", "--spring.jmx.enabled=false", "--spring.config.location=/opt/shinyproxy/application.yml"]
