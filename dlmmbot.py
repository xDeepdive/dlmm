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

def filter_trading_pairs(trading_pairs):
    """
    Filter trading pairs to include only those with 'SOL' and 24hr Fee/TVL > 50%.
    """
    filtered_pairs = []
    for pair in trading_pairs:
        name = pair.get("name", "")
        fee_tvl = pair.get("24hr_fee_tvl", 0)  # Adjust key based on actual API response
        if "SOL" in name and fee_tvl > 50:
            filtered_pairs.append(pair)
    return filtered_pairs

def format_trading_pairs_message(filtered_pairs):
    """
    Format the filtered trading pairs into a message for Discord.
    """
    if not filtered_pairs:
        return "No trading pairs meet the criteria (SOL pair and 24hr Fee/TVL > 50%)."

    message = "**Filtered Trading Pairs (SOL pairs with 24hr Fee/TVL > 50%):**\n\n"
    for pair in filtered_pairs:
        name = pair.get("name", "Unknown")
        address = pair.get("address", "N/A")
        fee_tvl = pair.get("24hr_fee_tvl", "N/A")  # Adjust key based on actual API response
        message += f"- **Name**: {name}\n  **Address**: {address}\n  **24hr Fee/TVL**: {fee_tvl}%\n\n"

    # Truncate the message if it exceeds 2000 characters
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
    filtered_pairs = filter_trading_pairs(trading_pairs)
    message = format_trading_pairs_message(filtered_pairs)
    send_discord_notification(message)

if __name__ == "__main__":
    main()
