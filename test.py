import requests
import os

webhook = os.environ["DISCORD_WEBHOOK"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

def pchome_search(keyword):
    url = f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={keyword}"
    r = requests.get(url, headers=headers).json()

    if r["prods"]:
        item = r["prods"][0]
        return item["price"], "https://24h.pchome.com.tw/prod/" + item["Id"]

    return None, None


def yahoo_search(keyword):
    url = f"https://tw.buy.yahoo.com/search/product?p={keyword}"
    r = requests.get(url, headers=headers)

    if "price" in r.text:
        import re
        price = re.search(r'"price":(\d+)', r.text)
        if price:
            return int(price.group(1)), url

    return None, None


def books_search(keyword):
    url = f"https://search.books.com.tw/search/query/key/{keyword}"
    r = requests.get(url, headers=headers)

    import re
    price = re.search(r'(\d{3,5})元', r.text)

    if price:
        return int(price.group(1)), url

    return None, None


def check_product(keyword):

    prices = []

    p_price, p_link = pchome_search(keyword)
    y_price, y_link = yahoo_search(keyword)
    b_price, b_link = books_search(keyword)

    report = f"\n🔎 {keyword}\n"

    if p_price:
        report += f"PChome：{p_price}\n"
        prices.append(("PChome", p_price, p_link))

    if y_price:
        report += f"Yahoo：{y_price}\n"
        prices.append(("Yahoo", y_price, y_link))

    if b_price:
        report += f"博客來：{b_price}\n"
        prices.append(("博客來", b_price, b_link))

    if prices:
        best = min(prices, key=lambda x: x[1])
        report += f"\n🏆 今日最低價：{best[0]} {best[1]}\n"
        report += f"🔗 <{best[2]}>\n"

    else:
        report += "沒有找到商品\n"

    return report


products = [
    "GW2790Q 2K",
    "DDR5 5600 16GB"
]

message = "📊 每日硬體價格監控\n"

for p in products:
    message += check_product(p)

requests.post(webhook, json={"content": message})
