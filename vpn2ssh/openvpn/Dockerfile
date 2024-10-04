FROM alpine:3.18

RUN apk update && apk add --no-cache \
    openvpn \
    openssh \
    bash \
    sudo \
    && rm -rf /var/cache/apk/*

RUN ssh-keygen -A

RUN mkdir -p /etc/openvpn

COPY ./vpn.conf /etc/openvpn/vpn.conf

RUN adduser -D vpn && echo "vpn:vpn" | chpasswd && echo "vpn ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY ./sshd /etc/ssh/sshd_config

EXPOSE 1194/udp 22/tcp

RUN apk add --no-cache tini

COPY start-services.sh /usr/local/bin/start-services.sh
RUN chmod +x /usr/local/bin/start-services.sh

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/usr/local/bin/start-services.sh"]
