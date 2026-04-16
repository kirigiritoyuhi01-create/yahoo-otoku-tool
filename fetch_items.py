import requests
import json
import os

CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID")

url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"

params = {
    "appid": CLIENT_ID,
    "query": "Nintendo Switch",
    "results": 20,
    "sort": "-price",
    "in_stock": 1,
}

response = requests.get(url, params=params)
data = response.json()

items = []
for hit in data.get("hits", []):
    items.append({
        "name": hit.get("name", ""),
        "price": hit.get("price", 0),
        "image": hit.get("image", {}).get("medium", ""),
        "url": hit.get("url", ""),
        "inStock": hit.get("inStock", False),
    })

with open("items.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"✅ {len(items)}件取得完了")
