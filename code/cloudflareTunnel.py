import subprocess
import re
import requests
import time

# 🔹 Replace with your ESP32 MAC address
ESP32_MAC = "78:42:1C:6D:C4:8C"

# 🔹 Telegram Bot credentials
BOT_TOKEN = "7541177164:AAExr-ozcDn5Hhsd5G3USe55Y9-Tn9EfboI"
CHAT_ID = "6414041079"

# 🔹 Path to cloudflared
CLOUDFLARED_PATH = "/usr/local/bin/cloudflared"

# 🔹 Interface to scan
INTERFACE = "eth0"


def get_local_subnet(interface):
    """Get subnet like 192.168.1.0/24 from 'ip a'."""
    try:
        output = subprocess.check_output(["ip", "a", "show", interface], text=True)
        match = re.search(r'inet (\d+\.\d+\.\d+)\.\d+/\d+', output)
        if match:
            subnet = match.group(1) + ".0/24"
            print(f"[+] Subnet detected: {subnet}")
            return subnet
    except subprocess.CalledProcessError as e:
        print("⚠ Could not detect subnet:", e)
    return None


def scan_network_for_mac(subnet, target_mac):
    """Scan network using nmap and return IP if MAC is matched."""
    print(f"🔍 Scanning {subnet} for MAC {target_mac}...")
    try:
        output = subprocess.check_output(["nmap", "-sn", subnet], text=True)
        ip, mac = None, None
        for line in output.splitlines():
            if "Nmap scan report for" in line:
                ip_match = re.search(r"Nmap scan report for (.+)", line)
                ip = ip_match.group(1).strip() if ip_match else None
            elif "MAC Address" in line:
                mac_match = re.search(r"MAC Address: ([0-9A-F:]+)", line, re.IGNORECASE)
                mac = mac_match.group(1).upper() if mac_match else None
                if ip and mac and mac == target_mac.upper():
                    return ip
    except subprocess.CalledProcessError as e:
        print("⚠ Error running nmap:", e)
    return None


def start_cloudflare_tunnel(esp_ip):
    """Start Cloudflare tunnel and return the public URL."""
    print(f"✅ Found ESP32 at {esp_ip}. Starting Cloudflare Tunnel...")
    tunnel_cmd = f"{CLOUDFLARED_PATH} tunnel --url http://{esp_ip}:80 --no-chunked-encoding > cf_tunnel.log 2>&1 &"
    subprocess.Popen(tunnel_cmd, shell=True)

    for _ in range(15):
        time.sleep(1)
        try:
            with open("cf_tunnel.log", "r") as log:
                match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", log.read())
                if match:
                    return match.group(0)
        except Exception:
            pass
    return None


def send_telegram_message(url):
    """Send the stream URL to Telegram."""
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": f"ESP32-CAM Stream: {url}"}
        )
        if response.status_code == 200:
            print("📩 Sent URL via Telegram!")
        else:
            print("⚠ Failed to send Telegram message.")
    except Exception as e:
        print("⚠ Telegram error:", e)


# 🔁 Main logic
while True:
    subnet = get_local_subnet(INTERFACE)
    if not subnet:
        print("❌ Cannot detect subnet. Retrying...")
        time.sleep(5)
        continue

    esp_ip = scan_network_for_mac(subnet, ESP32_MAC)
    if esp_ip:
        cf_url = start_cloudflare_tunnel(esp_ip)
        if cf_url:
            print(f"🌍 ESP32-CAM Public URL: {cf_url}")
            send_telegram_message(cf_url)
            break
        else:
            print("⚠ Cloudflare tunnel URL not found. Retrying...")
    else:
        print("🔄 ESP32 not found. Retrying in 5 seconds...")

    time.sleep(5)
