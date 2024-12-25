import requests

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1321351247466463295/5DqSeKppI00w4vdRk61arQ86Vp3-RBgcDxCTSK5G5vDE22Z5dz1QWJleErN0HDBTf2Rt"

# Meteora API URL for all pairs
API_URL = "https://dlmm-api.meteora.ag/pair::route/all"

def fetch_all_pairs():
    """
    Fetch all pairs from the Meteora API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        pairs = response.json()
        return pairs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching pairs: {e}")
        return []

def filter_pairs(pairs):
    """
    Filter pairs to include only SOL pairs with 24hr Fee/TVL > 50%.
    """
    filtered_pairs = []
    for pair in pairs:
        try:
            # Ensure the pair has the necessary fields
            if (
                "SOL" in pair["pair"].upper() and
                "fee_tvl" in pair and
                float(pair["fee_tvl"]) > 50
            ):
                filtered_pairs.append(pair)
        except KeyError:
            continue
    return filtered_pairs

def format_discord_message(pairs):
    """
    Format the filtered pairs into a message for Discord.
    """
    if not pairs:
        return "No pairs meet the criteria (SOL pair and 24hr Fee/TVL > 50%)."

    message = "**Filtered SOL Pairs with 24hr Fee/TVL > 50%:**\n\n"
    for pair in pairs:
        message += f"- **Pair**: {pair['pair']}\n"
        message += f"  **TVL**: {pair.get('tvl', 'N/A')}\n"
        message += f"  **24hr Fee/TVL**: {pair.get('fee_tvl', 'N/A')}%\n\n"

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
    pairs = fetch_all_pairs()
    filtered_pairs = filter_pairs(pairs)
    message = format_discord_message(filtered_pairs)
    send_discord_notification(message)

if __name__ == "__main__":
    main()
