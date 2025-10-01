#!/usr/bin/env python3
"""
Simple URL Opener with IP Rotation
A basic version for quick testing and demonstration
"""

import webbrowser
import time
import random
import signal
import sys
import subprocess
import platform

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Stopping script...")
    sys.exit(0)

def get_current_ip():
    """Get current IP using curl (cross-platform)"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(["curl", "https://ident.me"], 
                                  capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(["curl", "-s", "https://ident.me"], 
                                  capture_output=True, text=True, timeout=10)
        return result.stdout.strip() if result.returncode == 0 else "Unknown"
    except:
        return "Unknown"

def simulate_ip_change():
    """
    Simulate IP change using basic network operations
    This is a demonstration - real IP change requires VPN/Proxy/Tor
    """
    print("🔄 Simulating IP change...")

    # For demonstration purposes only - these don't actually change IP
    methods = [
        "Flushing DNS cache...",
        "Releasing/renewing IP lease...",
        "Changing network adapter settings...",
        "Reconnecting to network..."
    ]

    selected_method = random.choice(methods)
    print(f"   {selected_method}")

    # Simulate some processing time
    time.sleep(random.randint(2, 5))

    # On some systems, you could try these commands (requires admin/root):
    # Windows: subprocess.run(["ipconfig", "/release"], shell=True)
    #          subprocess.run(["ipconfig", "/renew"], shell=True)
    # Linux:   subprocess.run(["sudo", "dhclient", "-r"], shell=True)
    #          subprocess.run(["sudo", "dhclient"], shell=True)

    print("   ✅ IP change simulation completed")
    return True

def open_urls(urls):
    """Open URLs in default browser"""
    print(f"🌐 Opening {len(urls)} URLs...")

    for i, url in enumerate(urls, 1):
        try:
            print(f"  📂 Opening URL {i}: {url}")
            webbrowser.open_new_tab(url)
            # Small delay to prevent overwhelming the browser
            time.sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            print(f"  ❌ Error opening {url}: {e}")

    print("✅ Finished opening URLs")

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

    print("🚀 Simple URL Opener with IP Rotation")
    print("📋 Configuration:")
    print(f"   • URLs per cycle: {len(urls)}")
    print("   • IP change method: Simulation (for demo)")
    print("   • Press Ctrl+C to stop")
    print("=" * 50)

    cycle_count = 0

    try:
        while True:
            cycle_count += 1
            print(f"\n🔄 Cycle {cycle_count}")
            print("-" * 20)

            # Show current IP
            current_ip = get_current_ip()
            print(f"📍 Current IP: {current_ip}")

            # Open URLs
            open_urls(urls)

            print("\n⏳ Waiting before IP change...")
            time.sleep(3)

            # Simulate IP change
            simulate_ip_change()

            # Check IP again (may not actually change in simulation)
            new_ip = get_current_ip()
            print(f"📍 IP after change: {new_ip}")

            if current_ip != new_ip:
                print("✅ IP successfully changed!")
            else:
                print("ℹ️  IP unchanged (simulation mode)")

            # Wait before next cycle
            wait_time = random.randint(15, 45)
            print(f"\n⏳ Waiting {wait_time} seconds before next cycle...")
            print("   (Press Ctrl+C to stop)")

            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("⚠️  IMPORTANT NOTICE:")
    print("This script is for educational/testing purposes only.")
    print("Real IP changing requires VPN, proxy, or Tor setup.")
    print("Use responsibly and respect website terms of service.\n")

    main()
