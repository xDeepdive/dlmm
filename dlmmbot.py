import requests

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1321351247466463295/5DqSeKppI00w4vdRk61arQ86Vp3-RBgcDxCTSK5G5vDE22Z5dz1QWJleErN0HDBTf2Rt"

# Meteora DLMM API base URL
BASE_URL = 'https://dlmm-api.meteora.ag'

def fetch_active_pools():
    try:
        response = requests.get(f'{BASE_URL}/pool/active')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching active pools: {e}")
        return []

def fetch_pool_info(pool_address):
    try:
        response = requests.get(f'{BASE_URL}/pool/{pool_address}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching pool info for {pool_address}: {e}")
        return {}

def get_top_fee_generating_pools():
    active_pools = fetch_active_pools()
    pool_fee_data = []

    for pool in active_pools:
        pool_info = fetch_pool_info(pool['address'])
        if pool_info:
            fees_generated = pool_info.get('fees_generated', 0)  # Adjust based on actual API response
            pool_fee_data.append((pool['name'], fees_generated))

    # Sort pools by fees generated in descending order
    pool_fee_data.sort(key=lambda x: x[1], reverse=True)
    return pool_fee_data[:5]  # Top 5 pools

def send_discord_notification(top_pools):
    message = "**Top Fee-Generating Pools:**\n\n"
    for pool_name, fees in top_pools:
        message += f"**{pool_name}**: {fees} fees generated\n"

    payload = {"content": message}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Notification sent to Discord successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification to Discord: {e}")

if __name__ == "__main__":
    top_pools = get_top_fee_generating_pools()
    if top_pools:
        send_discord_notification(top_pools)
    else:
        print("No data to send.")
