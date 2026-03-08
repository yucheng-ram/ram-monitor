import os
import requests

webhook_url = os.environ["DISCORD_WEBHOOK"]

KEYWORD = "GW2790Q"
TARGET_PRICE = 3799

url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results"

params = {
    "q": KEYWORD,
    "page": 1,
    "sort": "sale/dc"
}

response = requests.get(url, params=params)
data = response.json()

message = f"📊 PChome 搜尋：{KEYWORD}\n\n"

for item in data["prods"][:5]:

    name = item["name"]
    price = item["price"]
    link = f"https://24h.pchome.com.tw/prod/{item['Id']}"

    if price <= TARGET_PRICE:
        message += f"🎯 {name}\n價格: {price}\n{link}\n\n"
    else:
        message += f"📌 {name}\n價格: {price}\n{link}\n\n"

requests.post(webhook_url, json={"content": message})

print("Done")
