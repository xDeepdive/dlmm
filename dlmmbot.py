import requests

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1321351247466463295/5DqSeKppI00w4vdRk61arQ86Vp3-RBgcDxCTSK5G5vDE22Z5dz1QWJleErN0HDBTf2Rt"

# Meteora API URL for active pools
API_URL = "https://dlmm-api.meteora.ag/pool/active"

def fetch_active_pools():
    """
    Fetch active pools from the Meteora API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        pools = response.json()
        return pools
    except requests.exceptions.RequestException as e:
        print(f"Error fetching active pools: {e}")
        return []

def filter_pools(pools):
    """
    Filter pools to include only SOL pairs with 24hr Fee/TVL > 50%.
    """
    filtered_pools = []
    for pool in pools:
        try:
            # Ensure the pool has the necessary fields
            if (
                "SOL" in pool["name"].upper() and
                "fee_tvl" in pool and
                float(pool["fee_tvl"]) > 50
            ):
                filtered_pools.append(pool)
        except KeyError:
            continue
    return filtered_pools

def format_discord_message(pools):
    """
    Format the filtered pools into a message for Discord.
    """
    if not pools:
        return "No pools meet the criteria (SOL pair and 24hr Fee/TVL > 50%)."

    message = "**Filtered SOL Pools with 24hr Fee/TVL > 50%:**\n\n"
    for pool in pools:
        message += f"- **Name**: {pool['name']}\n"
        message += f"  **TVL**: {pool.get('tvl', 'N/A')}\n"
        message += f"  **24hr Fee/TVL**: {pool.get('fee_tvl', 'N/A')}%\n\n"

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
    pools = fetch_active_pools()
    filtered_pools = filter_pools(pools)
    message = format_discord_message(filtered_pools)
    send_discord_notification(message)

if __name__ == "__main__":
    main()
