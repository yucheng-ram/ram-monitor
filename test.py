import os
import requests
from bs4 import BeautifulSoup

webhook_url = os.environ["DISCORD_WEBHOOK"]

KEYWORD = "GW2790Q"
TARGET_PRICE = 3799

url = f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={KEYWORD}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
html = response.text

soup = BeautifulSoup(html, "html.parser")

products = soup.select(".listArea li")

found = False
message = ""

for item in products[:10]:
    name_tag = item.select_one(".prdName")
    price_tag = item.select_one(".price")

    if name_tag and price_tag:
        name = name_tag.text.strip()

        price_text = price_tag.text.strip().replace(",", "")
        price_numbers = ''.join(filter(str.isdigit, price_text))

        if price_numbers:
            price = int(price_numbers)

            if price <= TARGET_PRICE:
                found = True
                link_tag = item.select_one("a")
                link = "https://www.momoshop.com.tw" + link_tag["href"]
                message += f"\n🎯 {name}\n價格: {price}\n{link}\n"

if not found:
    message = f"⚠️ {KEYWORD} 沒有低於 {TARGET_PRICE}"

requests.post(webhook_url, json={"content": message})

print("Done")
