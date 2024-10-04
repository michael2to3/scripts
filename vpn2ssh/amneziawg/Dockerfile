FROM amneziavpn/amneziawg-go:latest

RUN apk update && apk add --no-cache \
    openssh \
    bash \
    sudo \
    && rm -rf /var/cache/apk/*

RUN ssh-keygen -A

RUN adduser -D vpn && echo "vpn:vpn" | chpasswd && echo "vpn ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN mkdir -p /etc/amnezia/amneziawg/

COPY ./sshd /etc/ssh/sshd_config

COPY ./wg0.conf /etc/amnezia/amneziawg/

EXPOSE 51820/udp 22/tcp

COPY start-services.sh /usr/local/bin/start-services.sh
RUN chmod +x /usr/local/bin/start-services.sh

CMD ["/usr/local/bin/start-services.sh"]
