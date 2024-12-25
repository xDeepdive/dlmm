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
        return response.json()  # Assuming the API returns JSON data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trading pairs: {e}")
        return []

def filter_sol_pairs(trading_pairs):
    """
    Filter trading pairs to include only those with 'SOL' and 24hr Fee/TVL > 50%.
    """
    filtered_pairs = []
    for pair in trading_pairs:
        name = pair.get("name", "")
        fee_tvl = pair.get("24hr_fee_tvl", 0)  # Replace with actual field from the API response
        if "SOL" in name and fee_tvl > 50:
            filtered_pairs.append({
                "name": name,
                "address": pair.get("address", "N/A"),
                "fee_tvl": fee_tvl
            })
    return filtered_pairs

def format_discord_message(filtered_pairs):
    """
    Format the filtered trading pairs into a message for Discord.
    """
    if not filtered_pairs:
        return "No trading pairs meet the criteria (SOL pair and 24hr Fee/TVL > 50%)."

    message = "**Filtered SOL Pools with 24hr Fee/TVL > 50%:**\n\n"
    for pair in filtered_pairs:
        message += f"- **Name**: {pair['name']}\n  **Address**: {pair['address']}\n  **24hr Fee/TVL**: {pair['fee_tvl']}%\n\n"

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
    trading_pairs = fetch_trading_pairs()
    if not trading_pairs:
        print("No trading pairs data fetched.")
        return

    filtered_pairs = filter_sol_pairs(trading_pairs)
    message = format_discord_message(filtered_pairs)
    send_discord_notification(message)

if __name__ == "__main__":
    main()
