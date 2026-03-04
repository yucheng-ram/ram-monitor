import os
import requests

webhook_url = os.environ["DISCORD_WEBHOOK"]

KEYWORD = "GW2790Q"
TARGET_PRICE = 3799

url = "https://ecapi.momoshop.com.tw/search/v1/search"

params = {
    "q": KEYWORD,
    "page": 1,
    "sort": "sale/dc"
}

response = requests.get(url, params=params)
data = response.json()

products = data.get("products", [])

results = []

# 遍歷前 10 項結果
for p in products[:10]:
    name = p.get("name","")
    price = p.get("price",0)
    link = p.get("url", "")

    # 確保價格是數字
    try:
        price_int = int(price)
    except:
        price_int = 9999999

    results.append({
        "name": name,
        "price": price_int,
        "link": link
    })

message = "💡 MOMO 搜尋結果：\n"
notify_flag = False

for item in results:
    if item["price"] <= TARGET_PRICE:
        notify_flag = True
        message += f"\n🎯 {item['name']}\n價格: {item['price']}\n連結: {item['link']}\n"

if not notify_flag:
    message = f"⚠️ {KEYWORD} 價格沒有低於 {TARGET_PRICE}"

requests.post(webhook_url, json={"content": message})
print("Done")
