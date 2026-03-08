import os
import requests
from bs4 import BeautifulSoup

webhook_url = os.environ["DISCORD_WEBHOOK"]

KEYWORD = "GW2790Q"
TARGET_PRICE = 3799

url = f"https://m.momoshop.com.tw/search.momo?searchKeyword={KEYWORD}"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

products = soup.select(".goodsItemLi")

message = f"📊 MOMO 搜尋：{KEYWORD}\n\n"

for item in products[:5]:

    name = item.select_one(".prdName")
    price = item.select_one(".price")

    if name and price:

        name_text = name.text.strip()

        price_text = price.text.strip().replace(",", "")
        price_number = int(''.join(filter(str.isdigit, price_text)))

        link = "https://m.momoshop.com.tw" + item.select_one("a")["href"]

        if price_number <= TARGET_PRICE:
            message += f"🎯 {name_text}\n價格: {price_number}\n{link}\n\n"
        else:
            message += f"📌 {name_text}\n價格: {price_number}\n{link}\n\n"

requests.post(webhook_url, json={"content": message})

print("Done")
