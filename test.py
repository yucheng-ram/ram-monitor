import os
import requests

webhook_url = os.environ["DISCORD_WEBHOOK"]

KEYWORD = "記憶體"

url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results"

params = {
    "q": KEYWORD,
    "page": 1,
    "sort": "sale/dc"
}

response = requests.get(url, params=params)
data = response.json()

products = data.get("prods", [])

if products:
    product = products[0]
    name = product["name"]
    price = product["price"]
    message = f"📌 測試抓資料成功\n商品: {name}\n價格: {price}台幣"
else:
    message = "⚠️ 沒有找到商品"

requests.post(webhook_url, json={"content": message})

print("Done")
