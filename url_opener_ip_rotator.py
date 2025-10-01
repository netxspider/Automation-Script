import subprocess
import time
import random
import signal
import sys
import requests
from stem import Signal
from stem.control import Controller

def open_urls_in_chrome(urls):
    for url in urls:
        subprocess.run(['open', '-a', 'Google Chrome', url])
        print(f"🌐 Opening URL: {url}")  # Wait 10 seconds per URL for page load

def quit_chrome():
    subprocess.run(['osascript', '-e', 'quit app "Google Chrome"'])
    print("❌ Quit Chrome completely")
    time.sleep(3)

def get_current_ip():
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        response = requests.get('https://icanhazip.com', proxies=proxies, timeout=10)
        ip = response.text.strip()
        print(f"📍 Current Tor IP: {ip}")
        return ip
    except Exception as e:
        print(f"❌ Error getting IP: {e}")
        return None

def change_tor_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print("🔄 Tor new identity requested")
            time.sleep(10)  # Wait for new IP to become active
            return get_current_ip()
    except Exception as e:
        print(f"❌ Tor IP change failed: {e}")
        return None

def signal_handler(sig, frame):
    print("\n🛑 Stopping script...")
    try:
        quit_chrome()
    except:
        pass
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    urls = [
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=17",
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=16",
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=15",
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=14",
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=13"
    ]

    while True:
        print("\n🔄 Starting new cycle with Tor proxy")

        quit_chrome()

        open_urls_in_chrome(urls)

        wait_time = 20
        print(f"⏳ Waiting {wait_time} seconds before changing IP...")
        time.sleep(wait_time)

        new_ip = change_tor_ip()
        if not new_ip:
            print("⚠️ Failed to change Tor IP, retrying in 30 seconds...")
            time.sleep(30)

if __name__ == "__main__":
    main()
