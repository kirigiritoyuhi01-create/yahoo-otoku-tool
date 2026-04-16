import os
import requests
import json
import subprocess

YAHOO_CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID")
OUTPUT_FILE = "items.json"

JAN_LIST = [
    {"jan": "4902370550733", "buy_price": 42000}, # Switch
    {"jan": "4948872415545", "buy_price": 62000}, # PS5
]

def main():
    results = []
    for t in JAN_LIST:
        url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
        res = requests.get(url, params={"appid": YAHOO_CLIENT_ID, "jan_code": t["jan"], "results": 1})
        data = res.json()
        if "hits" in data and data["hits"]:
            item = data["hits"][0]
            # 実質価格を計算（ポイント8%還元想定）
            jisshitsu = int(item["price"] * 0.92)
            profit = t["buy_price"] - jisshitsu
            results.append({
                "name": item["name"],
                "price": int(item["price"]),
                "url": item["url"],
                "profit": profit,
                "buy_price": t["buy_price"]
            })
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    # GitHubに保存する設定
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"])
    subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    subprocess.run(["git", "add", OUTPUT_FILE])
    subprocess.run(["git", "commit", "-m", "Update data"], check=False)
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    main()
