import requests

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1321351247466463295/5DqSeKppI00w4vdRk61arQ86Vp3-RBgcDxCTSK5G5vDE22Z5dz1QWJleErN0HDBTf2Rt"

# Meteora DLMM API base URL
BASE_URL = "https://dlmm-api.meteora.ag"

def fetch_trading_pairs():
    """
    Fetch all trading pairs from the Meteora DLMM API.
    """
    try:
        response = requests.get(f"{BASE_URL}/pair/all")
        response.raise_for_status()
        return response.json()  # Assuming the API returns a JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trading pairs: {e}")
        return []

def format_trading_pairs_message(trading_pairs):
    """
    Format the trading pairs into a message for Discord.
    """
    if not trading_pairs:
        return "No active trading pairs found."

    message = "**Active Trading Pairs:**\n\n"
    for pair in trading_pairs:
        # Customize this based on the structure of the trading pair data
        name = pair.get("name", "Unknown")
        address = pair.get("address", "N/A")
        message += f"- **Name**: {name}\n  **Address**: {address}\n\n"
    return message

def send_discord_notification(message):
    """
    Send a notification to the Discord webhook.
    """
    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Notification sent to Discord successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification to Discord: {e}")

def main():
    trading_pairs = fetch_trading_pairs()
    message = format_trading_pairs_message(trading_pairs)
    send_discord_notification(message)

if __name__ == "__main__":
    main()
