docker build -t openvpn-ssh-alpine .
docker run -d --name openvpn-ssh-container --cap-add=NET_ADMIN --device /dev/net/tun --privileged -p 1194:1194/udp -p 22:22/tcp openvpn-ssh-alpine
