```bash
docker build -t openvpn .
docker run -d --name openvpn --cap-add=NET_ADMIN --device /dev/net/tun --privileged -p 22:22/tcp openvpn
```
