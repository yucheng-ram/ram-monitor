import os
import requests

webhook_url = os.environ["DISCORD_WEBHOOK"]

# 測試用 keyword（先用容易有結果的詞）
KEYWORD = "記憶體"  

url = "https://shopee.tw/api/v4/search/search_items"

params = {
    "by": "relevancy",
    "keyword": KEYWORD,
    "limit": 10,
    "newest": 0,
    "order": "desc",
    "page_type": "search",
    "scenario": "PAGE_GLOBAL_SEARCH",
    "version": 2
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()

items = data.get("items", [])

# 先抓第一筆商品名稱 + 價格
if items:
    item = items[0]["item_basic"]
    name = item["name"]
    price = item["price"] / 100000

    message = f"📌 測試抓資料成功\n商品: {name}\n價格: {price}台幣"
else:
    message = "⚠️ 沒有找到商品"

# Discord 通知
requests.post(webhook_url, json={"content": message})

print("Done")
