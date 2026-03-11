def get_stock():

    url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_00645.tw"

    r = requests.get(url).json()

    data = r["msgArray"][0]

    name = data["n"]

    price = data["z"]

    if price == "-":
        price = data["y"]   # fallback 用昨收

    price = float(price)

    yesterday = float(data["y"])

    diff = price - yesterday
    percent = diff / yesterday * 100

    return name, price, diff, percent
