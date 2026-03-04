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

# ====== DEBUG 區 ======
print("====== HTML 前 2000 字 ======")
print(html[:2000])
print("====== HTML 結束 ======")
# ======================

soup = BeautifulSoup(html, "html.parser")

# 先嘗試新版 selector
products = soup.select("ul#itemList li")

print("抓到商品數量:", len(products))

message = f"📊 MOMO 搜尋：{KEYWORD}\n\n"

for item in products[:5]:
    name_tag = item.select_one(".prdName")
    price_tag = item.select_one(".price")

    if name_tag and price_tag:
        name = name_tag.text.strip()

        price_text = price_tag.text.strip().replace(",", "")
        price_numbers = ''.join(filter(str.isdigit, price_text))

        if price_numbers:
            price = int(price_numbers)

            link_tag = item.select_one("a")
            link = "https://www.momoshop.com.tw" + link_tag["href"]

            if price <= TARGET_PRICE:
                message += f"🎯 {name}\n價格: {price}\n{link}\n\n"
            else:
                message += f"📌 {name}\n價格: {price}\n{link}\n\n"

requests.post(webhook_url, json={"content": message})

print("Done")
