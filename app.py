import os
import requests
import json
from datetime import datetime
import subprocess

YAHOO_CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID")
OUTPUT_FILE = "items.json"

JAN_LIST = [
    {"jan": "4902370550733", "buy_price": 42000},
    {"jan": "4948872415545", "buy_price": 62000},
    {"jan": "4549995427845", "buy_price": 125000},
    {"jan": "4902370542943", "buy_price": 23000},
    {"jan": "4549292183498", "buy_price": 85000},
    {"jan": "4547736066175", "buy_price": 35000},
]

def fetch_yahoo_shopping(jan_code):
    # 最新のV3 APIエンドポイントを使用
    url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
    params = {
        "appid": YAHOO_CLIENT_ID,
        "jan_code": jan_code,
        "results": 1,
    }
    try:
        res = requests.get(url, params=params)
        data = res.json()
        if "hits" in data and data["hits"]:
            item = data["hits"][0]
            return {
                "name": item["name"],
                "price": int(item["price"]),
                "url": item["url"],
                "image": item.get("image", {}).get("medium", ""),
                "shop": item.get("seller", {}).get("name", ""),
            }
    except: return None
    return None

def main():
    results = []
    for target in JAN_LIST:
        yahoo_data = fetch_yahoo_shopping(target["jan"])
        if yahoo_data:
            points = int(yahoo_data["price"] * 0.08)
            jisshitsu = yahoo_data["price"] - points
            profit = target["buy_price"] - jisshitsu
            yahoo_data.update({
                "jan": target["jan"],
                "buy_price": target["buy_price"],
                "profit": profit,
                "updated_at": datetime.now().strftime("%m/%d %H:%M")
            })
            results.append(yahoo_data)
    
    # データを保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    # 【ここが重要】GitHubにファイルを保存してアプリに反映させる命令
    try:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", OUTPUT_FILE], check=True)
        subprocess.run(["git", "commit", "-m", "Update items data"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("GitHubへのデータ保存に成功しました！")
    except Exception as e:
        print(f"保存エラー（変更がない場合もここを通ります）: {e}")

if __name__ == "__main__":
    main()
