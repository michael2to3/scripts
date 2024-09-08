FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    wget \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    gnupg \
    openjdk-17-jdk \
    wireguard-tools \
    iproute2 \
    sudo

RUN wget https://github.com/keycloak/keycloak/releases/download/23.0.6/keycloak-23.0.6.tar.gz && \
    tar xvfz keycloak-23.0.6.tar.gz && \
    mv keycloak-23.0.6 /opt/keycloak && \
    rm keycloak-23.0.6.tar.gz

RUN groupadd -r keycloak && useradd -r -g keycloak -d /opt/keycloak -s /sbin/nologin keycloak && \
    chown -R keycloak:keycloak /opt/keycloak

COPY ./mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/
RUN update-ca-certificates

COPY ./wg.conf /etc/wireguard/wg0.conf

COPY ./keycloak-multifactor-spi-jar-with-dependencies.jar /opt/keycloak/providers/

RUN echo 'ALL ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER keycloak

ENV KEYCLOAK_HOME /opt/keycloak

CMD ["/bin/bash", "-c", "$KEYCLOAK_HOME/bin/kc.sh start-dev & sudo wg-quick up wg0 && tail -f /dev/null"]
