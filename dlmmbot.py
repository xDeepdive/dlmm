from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import time

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1321351247466463295/5DqSeKppI00w4vdRk61arQ86Vp3-RBgcDxCTSK5G5vDE22Z5dz1QWJleErN0HDBTf2Rt"

# Meteora website URL
WEBSITE_URL = "https://app.meteora.ag/"

def fetch_pool_data():
    """
    Fetch pool data dynamically using Selenium.
    """
    # Set up Selenium WebDriver with headless Chrome
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"  # Specify the location of Chromium binary

    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)

    driver.get(WEBSITE_URL)
    time.sleep(5)  # Wait for the page to load

    pools = []

    try:
        # Adjust these selectors based on the actual HTML structure
        pool_sections = driver.find_elements(By.CLASS_NAME, "your-class-name-for-pools")  # Replace with actual class name
        for section in pool_sections:
            name = section.find_element(By.CLASS_NAME, "pool-name-class").text  # Replace with actual class name
            tvl = section.find_element(By.CLASS_NAME, "tvl-class").text  # Replace with actual class name
            fee_tvl = section.find_element(By.CLASS_NAME, "fee-tvl-class").text  # Replace with actual class name

            if "SOL" in name and float(fee_tvl.replace("%", "").strip()) > 50:
                pools.append({
                    "name": name,
                    "tvl": tvl,
                    "fee_tvl": fee_tvl
                })
    except Exception as e:
        print(f"Error extracting data: {e}")
    finally:
        driver.quit()

    return pools

def format_discord_message(pools):
    """
    Format the filtered pools into a message for Discord.
    """
    if not pools:
        return "No pools meet the criteria (SOL pair and 24hr Fee/TVL > 50%)."

    message = "**Filtered SOL Pools with 24hr Fee/TVL > 50%:**\n\n"
    for pool in pools:
        message += f"- **Name**: {pool['name']}\n  **TVL**: {pool['tvl']}\n  **24hr Fee/TVL**: {pool['fee_tvl']}%\n\n"

    return message

def send_discord_notification(message):
    """
    Send the formatted message to the Discord webhook.
    """
    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Notification sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")

def main():
    pools = fetch_pool_data()
    message = format_discord_message(pools)
    send_discord_notification(message)

if __name__ == "__main__":
    main()
