
# 🛡️ TunnelVision-ESP: Frame-Based Remote Surveillance

A professional-grade home monitoring system utilizing the **ESP32-CAM** for real-time motion analysis and secure global access. This project replaces traditional PIR sensors with **pixel-difference algorithms** to detect intruders and uses **Cloudflare Zero Trust** for encrypted remote viewing.

## 🚀 Key Features

* **Intelligent Frame-Based Detection:** Analyzes consecutive video frames to detect motion. No external PIR sensor required.
* **Secure Cloudflare Tunnel:** Bypasses CGNAT and firewalls to provide a secure `https` dashboard access from anywhere in the world—no port forwarding needed.
* **Telegram Instant Alerts:** Automatically captures a high-resolution snapshot and sends it to a Telegram bot when an intruder is detected.
* **Web Dashboard:** Live MJPEG streaming and manual snapshot capture via a mobile-friendly web interface.

---

## 🛠️ Tech Stack

* **Hardware:** ESP32-CAM (OV2640 Module)
* **Firmware:** C++ / Arduino Framework
* **Networking:** Cloudflare Tunnel (`cloudflared`)
* **Messaging:** Telegram Bot API
* **Algorithms:** Temporal Frame Differencing for Motion Detection

---

## 📐 System Architecture

1. **Capture:** The ESP32-CAM continuously captures low-res frames for analysis.
2. **Analyze:** The firmware compares the current frame against a buffer. If the variance exceeds the threshold, "Motion" is triggered.
3. **Notify:** Upon trigger, a high-res JPG is captured and sent via HTTP POST to the Telegram Bot API.
4. **Access:** The local web server (Port 80) is tunneled to a public domain via Cloudflare for secure remote monitoring.

---


## ⚙️ Setup & Installation

1. **Telegram:** Create a bot via @BotFather and save your `BOT_TOKEN` and `CHAT_ID`.
2. **Cloudflare:** Install `cloudflared` on a local machine (PC/Pi) and point it to your ESP32-CAM's local IP.
3. **Firmware:** * Open the code in Arduino IDE.
* Input your WiFi credentials and Telegram API tokens.
* Flash to the ESP32-CAM using an FTDI adapter.

---
