import os
import json
import requests

webhook_url = os.environ["DISCORD_WEBHOOK"]

TARGET_PRICE = 3799

# 監控商品
KEYWORDS = [
    "GW2790Q",
    "DDR4 16GB",
]

API_URL = "https://ecshweb.pchome.com.tw/search/v3.3/all/results"

# 讀取歷史價格
try:
    with open("price_history.json", "r") as f:
        history = json.load(f)
except:
    history = {}

message = "🛒 每日價格監控報告\n\n"

for keyword in KEYWORDS:

    params = {
        "q": keyword,
        "page": 1,
        "sort": "sale/dc"
    }

    r = requests.get(API_URL, params=params)
    data = r.json()

    message += f"🔎 {keyword}\n"

    for item in data["prods"][:3]:

        name = item["name"]
        price = item["price"]
        pid = item["Id"]

        link = f"https://24h.pchome.com.tw/prod/{pid}"

        # 歷史最低價
        if pid not in history:
            history[pid] = price

        lowest = history[pid]

        if price < lowest:
            history[pid] = price
            lowest = price

        # emoji
        if price <= TARGET_PRICE:
            icon = "🎯"
        else:
            icon = "📦"

        message += (
            f"{icon} {name}\n"
            f"💰 現價: {price}\n"
            f"📉 最低: {lowest}\n"
            f"{link}\n\n"
        )

# 存歷史
with open("price_history.json", "w") as f:
    json.dump(history, f)

# 發送 Discord
requests.post(webhook_url, json={"content": message})

print("Done")
