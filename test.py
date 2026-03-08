import os
import json
import requests

webhook_url = os.environ["DISCORD_WEBHOOK"]

API_URL = "https://ecshweb.pchome.com.tw/search/v3.3/all/results"

# 監控商品
KEYWORDS = [
    "GW2790Q",
    "DDR5 5600 16GB"
]

# 讀歷史
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

    message += f"🔎 **{keyword}**\n\n"

    for item in data["prods"][:3]:

        name = item["name"]
        price = item["price"]
        pid = item["Id"]

        link = f"https://24h.pchome.com.tw/prod/{pid}"

        change_text = ""

        if pid not in history:
            history[pid] = {
                "lowest": price,
                "last": price
            }
            change_text = "🆕 新商品"

        else:

            last_price = history[pid]["last"]

            if price < last_price:
                diff = last_price - price
                change_text = f"⬇️ 降價 {diff}"

            elif price > last_price:
                diff = price - last_price
                change_text = f"⬆️ 漲價 {diff}"

            history[pid]["last"] = price

            if price < history[pid]["lowest"]:
                history[pid]["lowest"] = price

        lowest = history[pid]["lowest"]

        message += (
            f"📦 {name}\n"
            f"💰 現價: **{price}**\n"
            f"📉 最低: {lowest}\n"
        )

        if change_text:
            message += f"{change_text}\n"

        message += f"{link}\n\n"

    message += "----------------------\n\n"


# 存回歷史
with open("price_history.json", "w") as f:
    json.dump(history, f)

# 發送 Discord
requests.post(webhook_url, json={"content": message})

print("Done")
