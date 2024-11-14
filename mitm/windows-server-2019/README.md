To enable vpn:
```powershell
wireguard /installtunnelservice $configDir\vpn.conf
```
To stop use vpn:
```powershell
net stop 'WireGuardTunnel$vpn'
```
