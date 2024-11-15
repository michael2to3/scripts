# Fish AP

## Overview

Fish AP is a tool designed to create an Access Point (AP) and run a web server for targeted network testing. It enables network traffic redirection and the capture of authentication handshakes.

---

## Usage

### Step 1: Create Access Point

Use berate_ap to create an access point:

```bash
./berate_ap --no-virt -n wlan1 example --redirect-to-localhost --mac XX:XX:XX:XX:XX:XX
```

- **Arguments:**
  - --no-virt: Disables creation of a virtual interface.
  - -n wlan1: Specifies the network interface.
  - example: Name of the access point.
  - --redirect-to-localhost: Redirects all traffic to localhost.
  - --mac XX:XX:XX:XX:XX:XX: Sets a custom MAC address for the AP.

### Step 2: Set Up Web Server

Copy the captured handshake file to the web server directory:

```bash
cp ./airodump-wifi.cap ./web/handshake.cap
```

Run the script to start the app and check for a successful connection:

```bash
./run_app_exit_if_success.sh MM:MM:MM:MM:MM:MM 192.168.12.1
```

- **Arguments:**
  - MM:MM:MM:MM:MM:MM: MAC address to extract the message from the .cap file.
  - 192.168.12.1: IP address of the web server interface.

### Step 3: Wait for Client

- **Enhancing Effectiveness:**
  - To increase the likelihood of the target device connecting to your AP, ensure your AP has the same name (SSID) and security settings as the target network.
  - **Using Virtual Interfaces:** Create virtual interfaces to operate in different modes simultaneously, allowing you to combine techniques and enhance testing effectiveness.

---

## Adding Virtual Interfaces and Configuring WLAN Combinations

### Checking Supported Interface Combinations

Before creating virtual interfaces, verify that your Wi-Fi adapter supports the required mode combinations:

```bash
iw list
```

Look for the **"Supported interface combinations"** section. For example:

Valid interface combinations: \* #{ managed } <= 1, #{ AP } <= 1,
total <= 2, #channels <= 1

This indicates support for simultaneous client (managed) and access point (AP) modes using one channel.

### Creating Virtual Interfaces

Create virtual interfaces based on your physical interface (wlan0):

```bash
iw dev wlan0 interface add wlan0_ap type __ap
iw dev wlan0 interface add wlan0_sta type managed
```
