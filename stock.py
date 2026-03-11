import requests
import os

webhook = os.environ["DISCORD_STOCK_WEBHOOK"]

def get_stock():

    url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_00645.tw"

    r = requests.get(url).json()

    data = r["msgArray"][0]

    name = data["n"]

    price = data["z"]

    if price == "-":
        price = data["y"]

    price = float(price)

    yesterday = float(data["y"])

    diff = price - yesterday
    percent = diff / yesterday * 100

    return name, price, diff, percent


name, price, diff, percent = get_stock()

emoji = "📈" if diff > 0 else "📉"

message = f"""
📊 ETF 每日監控

{name}

💰 現價：${price:.2f}
{emoji} 漲跌：{diff:.2f} ({percent:.2f}%)
"""

requests.post(webhook, json={"content": message})
