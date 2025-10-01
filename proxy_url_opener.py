#!/usr/bin/env python3
"""
URL Opener with Proxy Rotation
Version that uses only proxy servers for IP rotation
"""

import requests
import webbrowser
import time
import random
import signal
import sys
from itertools import cycle

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Stopping script...")
    sys.exit(0)

class ProxyRotator:
    """
    Handle proxy rotation for IP changes
    """

    def __init__(self):
        # Free proxy list (replace with working proxies)
        # You can get proxies from: https://www.proxy-list.download/api/v1/get?type=http
        self.proxy_list = [
            # Add your working proxies here in this format:
            # {'http': 'http://proxy_ip:port', 'https': 'http://proxy_ip:port'},
            # Example (these are placeholders - replace with real proxies):
            {'http': 'http://8.8.8.8:8080', 'https': 'http://8.8.8.8:8080'},
            {'http': 'http://1.1.1.1:3128', 'https': 'http://1.1.1.1:3128'},
            # Add more proxies for better rotation
        ]

        if not self.proxy_list or all('8.8.8.8' in str(proxy) for proxy in self.proxy_list):
            print("⚠️  Warning: Using placeholder proxies. Replace with working proxies!")
            print("💡 Get free proxies from: https://www.proxy-list.download/")

        self.proxy_cycle = cycle(self.proxy_list)
        self.current_proxy = None
        self.no_proxy_mode = len(self.proxy_list) == 0

    def get_current_ip(self):
        """Get current IP address"""
        try:
            if self.current_proxy and not self.no_proxy_mode:
                response = requests.get('https://httpbin.org/ip', 
                                      proxies=self.current_proxy, 
                                      timeout=10)
                return response.json()['origin']
            else:
                response = requests.get('https://httpbin.org/ip', timeout=10)
                return response.json()['origin']
        except Exception as e:
            print(f"Error getting IP: {e}")
            return "Unknown"

    def rotate_proxy(self):
        """Switch to the next proxy"""
        if self.no_proxy_mode:
            print("🔄 No proxies configured - simulating IP change...")
            time.sleep(2)
            return True

        try:
            self.current_proxy = next(self.proxy_cycle)
            print(f"🔄 Switched to proxy: {self.current_proxy['http']}")
            return True
        except Exception as e:
            print(f"❌ Error switching proxy: {e}")
            return False

def open_urls_browser(urls):
    """Open URLs in default browser"""
    print(f"🌐 Opening {len(urls)} URLs in browser...")

    for i, url in enumerate(urls, 1):
        try:
            print(f"  📂 Opening URL {i}: {url}")
            webbrowser.open_new_tab(url)
            time.sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            print(f"  ❌ Error opening {url}: {e}")

    print("✅ Finished opening URLs")

def open_urls_requests(urls, proxy_rotator):
    """Open URLs using requests with proxy"""
    print(f"🌐 Making requests to {len(urls)} URLs...")

    session = requests.Session()

    # Set proxy if available
    if proxy_rotator.current_proxy:
        session.proxies = proxy_rotator.current_proxy

    # Random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]

    session.headers.update({
        'User-Agent': random.choice(user_agents)
    })

    for i, url in enumerate(urls, 1):
        try:
            print(f"  🔗 Requesting URL {i}: {url}")
            response = session.get(url, timeout=10)
            print(f"    ✅ Status: {response.status_code}")
        except Exception as e:
            print(f"    ❌ Error accessing {url}: {e}")

def main():
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # URLs to open (customize these)
    urls = [
        "https://httpbin.org/ip",
        "https://www.whatismyipaddress.com/",
        "https://www.google.com",
        "https://www.github.com",
        "https://stackoverflow.com"
    ]

    # Initialize proxy rotator
    proxy_rotator = ProxyRotator()

    print("🚀 URL Opener with Proxy Rotation")
    print("📋 Configuration:")
    print(f"   • URLs per cycle: {len(urls)}")
    print(f"   • Proxies configured: {len(proxy_rotator.proxy_list)}")
    print("   • Press Ctrl+C to stop")
    print("=" * 50)

    cycle_count = 0

    try:
        while True:
            cycle_count += 1
            print(f"\n🔄 Cycle {cycle_count}")
            print("-" * 20)

            # Show current IP
            current_ip = proxy_rotator.get_current_ip()
            print(f"📍 Current IP: {current_ip}")

            # Choose opening method
            use_browser = True  # Change to False for headless requests

            if use_browser:
                open_urls_browser(urls)
            else:
                open_urls_requests(urls, proxy_rotator)

            print("\n🔄 Rotating proxy/IP...")

            # Rotate proxy
            proxy_rotator.rotate_proxy()

            # Check new IP
            new_ip = proxy_rotator.get_current_ip()
            print(f"📍 New IP: {new_ip}")

            if current_ip != new_ip:
                print("✅ IP successfully changed!")
            else:
                print("⚠️  IP unchanged (proxy might not be working)")

            # Wait before next cycle
            wait_time = random.randint(20, 60)
            print(f"⏳ Waiting {wait_time} seconds before next cycle...")
            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("⚠️  PROXY CONFIGURATION REQUIRED:")
    print("Edit the proxy_list in this script with working proxy servers.")
    print("Free proxies: https://www.proxy-list.download/")
    print("Paid proxies recommended for better reliability.\n")

    main()
