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
        return response.json()
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
        # Extract relevant fields
        name = pair.get("name", "Unknown")
        address = pair.get("address", "N/A")
        message += f"- **Name**: {name}\n  **Address**: {address}\n\n"
    
    # Ensure the message does not exceed Discord's 2000-character limit
    if len(message) > 2000:
        message = message[:1997] + "..."
    return message

def send_discord_notification(message):
    """
    Send a notification to the Discord webhook.
    """
    if not message.strip():
        print("No content to send to Discord.")
        return

    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Notification sent to Discord successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification to Discord: {e}")

def main():
    trading_pairs = fetch_trading_pairs()
    unique_trading_pairs = {pair['address']: pair for pair in trading_pairs}.values()  # Remove duplicates by address
    message = format_trading_pairs_message(unique_trading_pairs)
    send_discord_notification(message)

if __name__ == "__main__":
    main()
