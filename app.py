import os
import requests
import json
from datetime import datetime
import subprocess

# 設定
YAHOO_CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID")
OUTPUT_FILE = "items.json"

def fetch_yahoo_shopping(jan_code):
    url = "https://shopping.yahoo.co.jp/api/v1/itemSearch"
    params = {"appid": YAHOO_CLIENT_ID, "jan_code": jan_code, "sort": "+price", "results": 1}
    try:
        res = requests.get(url, params=params)
        data = res.json()
        if "hits" in data and data["hits"]:
            item = data["hits"][0]
            return {"name": item["name"], "price": int(item["price"]), "url": item["url"], "image": item["image"]["medium"], "shop": item["store"]["name"]}
    except: return None
    return None

def main():
    test_jans = [
        {"jan": "4902370550733", "buy_price": 42000}, # Switch
        {"jan": "4948872415545", "buy_price": 62000}, # PS5
    ]
    results = []
    for target in test_jans:
        yahoo_data = fetch_yahoo_shopping(target["jan"])
        if yahoo_data:
            points = int(yahoo_data["price"] * 0.08)
            jisshitsu = yahoo_data["price"] - points
            profit = target["buy_price"] - jisshitsu
            yahoo_data.update({"jan": target["jan"], "buy_price": target["buy_price"], "profit": profit, "profit_rate": round((profit / jisshitsu) * 100, 1)})
            results.append(yahoo_data)
    
    # データを保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # 【重要】GitHubにデータを強制保存するための設定
    subprocess.run(["git", "config", "user.name", "GitHub Actions"])
    subprocess.run(["git", "config", "user.email", "actions@github.com"])
    subprocess.run(["git", "add", OUTPUT_FILE])
    subprocess.run(["git", "commit", "-m", "Auto Update Data"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    main()
