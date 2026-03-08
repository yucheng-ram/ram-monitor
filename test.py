import os
import requests
from bs4 import BeautifulSoup

webhook_url = os.environ["DISCORD_WEBHOOK"]

KEYWORD = "GW2790Q"

url = f"https://m.momoshop.com.tw/search.momo?searchKeyword={KEYWORD}"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
}

response = requests.get(url, headers=headers)

print("status:", response.status_code)

html = response.text

print("==== HTML 前1000字 ====")
print(html[:1000])
print("==== END ====")

soup = BeautifulSoup(html, "html.parser")

products = soup.select("li")

print("抓到 li 數量:", len(products))

requests.post(webhook_url, json={"content": f"測試完成: li={len(products)}"})
