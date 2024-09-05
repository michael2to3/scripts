#!/bin/sh

openvpn --config /etc/openvpn/vpn.conf &

exec /usr/sbin/sshd -D
