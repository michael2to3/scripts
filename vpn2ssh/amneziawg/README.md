```bash
docker build -t amneziawg .

docker run -d --name awg --privileged --cap-add=NET_ADMIN --device /dev/net/tun -p 22:22/tcp awg
```
