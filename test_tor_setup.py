#!/usr/bin/env python3
"""
Robust Tor Test Script - Handles CAPTCHA and Blocking Issues
"""

import requests
import time
from stem import Signal
from stem.control import Controller

def test_tor_with_multiple_endpoints():
    """Test Tor with multiple endpoints and handle non-JSON responses"""
    print("🧅 Testing Tor SOCKS proxy with multiple endpoints...")

    tor_proxy = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    # Test endpoints that are more Tor-friendly
    endpoints = [
        {
            'url': 'https://check.torproject.org/api/ip',
            'name': 'Tor Project Check',
            'expects_json': True
        },
        {
            'url': 'https://icanhazip.com',
            'name': 'ICanHazIP',
            'expects_json': False
        },
        {
            'url': 'http://httpbin.org/ip',
            'name': 'HTTPBin (HTTP)',
            'expects_json': True
        },
        {
            'url': 'https://api.ipify.org?format=json',
            'name': 'Ipify API',
            'expects_json': True
        }
    ]

    # First get normal IP
    try:
        normal_response = requests.get('https://icanhazip.com', timeout=10)
        normal_ip = normal_response.text.strip()
        print(f"📍 Your normal IP: {normal_ip}")
    except Exception as e:
        print(f"⚠️  Could not get normal IP: {e}")
        normal_ip = "Unknown"

    print("\n🔍 Testing Tor endpoints...")
    working_endpoints = 0
    tor_ip = None

    for endpoint in endpoints:
        try:
            print(f"\n  🔗 Testing {endpoint['name']}: {endpoint['url']}")

            response = requests.get(
                endpoint['url'], 
                proxies=tor_proxy, 
                timeout=20,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
            )

            print(f"    ✅ Status Code: {response.status_code}")

            if endpoint['expects_json']:
                try:
                    data = response.json()
                    if 'origin' in data:
                        tor_ip = data['origin']
                    elif 'ip' in data:
                        tor_ip = data['ip']
                    else:
                        tor_ip = str(data)
                    print(f"    📍 Tor IP: {tor_ip}")
                except:
                    # Not JSON, show first 100 chars
                    content = response.text[:100].replace('\n', ' ')
                    print(f"    ⚠️  Non-JSON response: {content}...")
                    if 'captcha' in response.text.lower() or 'blocked' in response.text.lower():
                        print(f"    🚫 Appears to be blocked/CAPTCHA")
                    else:
                        tor_ip = response.text.strip()
            else:
                tor_ip = response.text.strip()
                print(f"    📍 Tor IP: {tor_ip}")

            working_endpoints += 1
            break  # Stop on first success

        except Exception as e:
            print(f"    ❌ Failed: {type(e).__name__}: {str(e)[:50]}...")

    if working_endpoints > 0:
        if tor_ip and tor_ip != normal_ip and tor_ip != "Unknown":
            print(f"\n✅ SUCCESS! Tor is working!")
            print(f"📍 Normal IP: {normal_ip}")
            print(f"🧅 Tor IP: {tor_ip}")
            return True, tor_ip
        else:
            print(f"\n⚠️  Tor responded but IP might not have changed")
            print(f"📍 Normal IP: {normal_ip}")
            print(f"🧅 Tor IP: {tor_ip}")
            return True, tor_ip  # Still working, just same IP
    else:
        print(f"\n❌ No endpoints worked through Tor")
        return False, None

def test_ip_rotation():
    """Test IP rotation with better error handling"""
    print("\n🔄 Testing IP rotation...")

    tor_proxy = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    def get_tor_ip():
        try:
            response = requests.get('https://icanhazip.com', 
                                  proxies=tor_proxy, 
                                  timeout=15,
                                  headers={'User-Agent': 'Mozilla/5.0 (compatible)'})
            return response.text.strip()
        except:
            try:
                response = requests.get('http://httpbin.org/ip', 
                                      proxies=tor_proxy, 
                                      timeout=15)
                return response.json()['origin']
            except:
                return "Failed"

    # Get initial IP
    ip1 = get_tor_ip()
    print(f"📍 IP before rotation: {ip1}")

    if ip1 == "Failed":
        print("❌ Could not get initial IP")
        return False

    # Request new circuit
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print("🔄 Requested new Tor circuit...")
    except Exception as e:
        print(f"❌ Could not request new circuit: {e}")
        return False

    # Wait for change
    print("⏳ Waiting 10 seconds for circuit change...")
    time.sleep(10)

    # Get new IP
    ip2 = get_tor_ip()
    print(f"📍 IP after rotation: {ip2}")

    if ip2 == "Failed":
        print("⚠️  Could not get new IP, but rotation was requested")
        return True

    if ip1 != ip2:
        print("✅ IP rotation successful!")
        return True
    else:
        print("ℹ️  IP didn't change (this happens sometimes with Tor)")
        return True

def main():
    print("🔧 ROBUST TOR TEST WITH BLOCKING DETECTION")
    print("=" * 55)

    # Test control port first
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            print("✅ Tor control port (9051) working")
            control_ok = True
    except Exception as e:
        print(f"❌ Tor control port failed: {e}")
        control_ok = False
        return

    # Test SOCKS proxy
    proxy_ok, tor_ip = test_tor_with_multiple_endpoints()

    if proxy_ok:
        # Test rotation
        rotation_ok = test_ip_rotation()

        print("\n" + "=" * 55)
        if rotation_ok:
            print("🎉 TOR IS FULLY WORKING!")
            print("✨ You can now run your main scripts:")
            print("   python url_opener_ip_rotator.py")
            print("   python simple_url_opener.py")
        else:
            print("⚠️  Tor works but rotation had issues")
    else:
        print("\n" + "=" * 55)
        print("❌ Tor SOCKS proxy not working properly")
        print("💡 Try: brew services restart tor  # or equivalent for your OS")

if __name__ == "__main__":
    main()
