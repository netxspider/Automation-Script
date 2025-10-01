import time
import random
import signal
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException, WebDriverException


# Global driver variable for cleanup
driver = None


def signal_handler(sig, frame):
    print("\n🛑 Stopping script...")
    if driver:
        try:
            driver.quit()
            print("🔒 Browser closed safely")
        except:
            pass
    sys.exit(0)


def main():
    global driver
    signal.signal(signal.SIGINT, signal_handler)

    urls = [
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=17",
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=16",
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=15",
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=14",
        "https://aiskillshouse.com/student/qr-mediator.html?uid=10809&promptId=13"
    ]

    # ChromeDriver path
    chromedriver_path = "/Users/arnavraj/Automation-Script/chromedriver-mac-arm64/chromedriver"

    options = Options()

    # Enhanced Tor SOCKS5 proxy configuration
    options.add_argument("--proxy-server=socks5://127.0.0.1:9050")

    # Additional arguments to ensure proxy works properly
    options.add_argument("--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE 127.0.0.1")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")

    # Avoid automation detection
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("detach", True)

    # Set user agent
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        print("🚀 Starting Chrome browser with Tor SOCKS proxy")
        print("📋 Make sure Tor service is running on port 9050")
    except Exception as e:
        print(f"❌ Failed to start Chrome: {e}")
        print("💡 Check:")
        print("  • ChromeDriver path is correct")
        print("  • Tor service is running: brew services start tor")
        return

    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"\n🔄 Cycle {cycle}")
            print("-" * 20)

            # Robust window management
            try:
                current_handles = driver.window_handles

                if not current_handles:
                    # No windows exist, create one
                    driver.execute_script("window.open('about:blank', '_blank');")
                    current_handles = driver.window_handles

                # Keep the first window, close others
                main_handle = current_handles[0]

                for handle in current_handles[1:]:
                    try:
                        driver.switch_to.window(handle)
                        driver.close()
                    except NoSuchWindowException:
                        continue

                # Switch to main window safely
                try:
                    driver.switch_to.window(main_handle)
                except NoSuchWindowException:
                    # Main window was closed, use any available window
                    available_handles = driver.window_handles
                    if available_handles:
                        driver.switch_to.window(available_handles[0])
                    else:
                        # No windows available, create new one
                        driver.execute_script("window.open('about:blank', '_blank');")
                        driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"⚠️  Window management error: {e}")
                # Try to recover
                try:
                    if not driver.window_handles:
                        driver.execute_script("window.open('about:blank', '_blank');")
                    driver.switch_to.window(driver.window_handles[0])
                except:
                    print("❌ Could not recover browser state")
                    continue

            # Open first URL in current tab
            try:
                print(f"📂 Opening URL 1: {urls[0]}")
                driver.get(urls[0])
                time.sleep(3)  # Wait for page load
            except Exception as e:
                print(f"❌ Error opening URL 1: {e}")

            # Open remaining URLs in new tabs
            for i, url in enumerate(urls[1:], start=2):
                try:
                    driver.execute_script(f"window.open('{url}', '_blank');")
                    print(f"📂 Opening URL {i}: {url}")
                    time.sleep(1.5)  # Delay between opens
                except Exception as e:
                    print(f"❌ Error opening URL {i}: {e}")

            print("✅ Finished opening URLs")

            # Wait before next cycle with countdown
            wait_time = random.randint(15, 45)
            print(f"⏳ Waiting {wait_time} seconds before next cycle...")

            # Show countdown every 10 seconds
            for remaining in range(wait_time, 0, -10):
                if remaining <= 10:
                    print(f"   ⏰ {remaining}s remaining...")
                    time.sleep(remaining)
                    break
                else:
                    time.sleep(10)
                    print(f"   ⏰ {remaining}s remaining...")

    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Try restarting Tor service: brew services restart tor")
    finally:
        if driver:
            try:
                driver.quit()
                print("🔒 Browser closed safely")
            except:
                pass


if __name__ == "__main__":
    print("🔧 URL OPENER WITH TOR INTEGRATION")
    print("=" * 45)
    print("⚠️  REQUIREMENTS:")
    print("• Tor service must be running on port 9050")
    print("• ChromeDriver must be accessible")
    print("• Press Ctrl+C to stop safely")
    print("=" * 45)
    print()
    main()
