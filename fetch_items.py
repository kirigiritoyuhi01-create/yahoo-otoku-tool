import os
import requests
import json
from datetime import datetime

# 設定
YAHOO_CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID")
OUTPUT_FILE = "items.json"

def fetch_yahoo_shopping(jan_code):
    """JANコードでヤフショ最安値を検索"""
    url = "https://shopping.yahoo.co.jp/api/v1/itemSearch"
    params = {
        "appid": YAHOO_CLIENT_ID,
        "jan_code": jan_code,
        "sort": "+price",
        "results": 1
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
                "image": item["image"]["medium"],
                "shop": item["store"]["name"]
            }
    except:
        return None
    return None

def main():
    # テスト用：買取屋で人気のあるJANコードリスト
    # 本番ではここをスクレイピングで自動取得するように拡張します
    test_jans = [
        {"jan": "4902370550733", "buy_price": 42000}, # Switch有機EL
        {"jan": "4948872415545", "buy_price": 62000}, # PS5
        {"jan": "4549995427845", "buy_price": 125000}, # iPhone15
    ]
    
    results = []
    for target in test_jans:
        yahoo_data = fetch_yahoo_shopping(target["jan"])
        if yahoo_data:
            # 簡易利益計算（PayPay 8%還元想定）
            points = int(yahoo_data["price"] * 0.08)
            jisshitsu = yahoo_data["price"] - points
            profit = target["buy_price"] - jisshitsu
            
            yahoo_data.update({
                "jan": target["jan"],
                "buy_price": target["buy_price"],
                "profit": profit,
                "profit_rate": round((profit / jisshitsu) * 100, 1),
                "updated_at": datetime.now().strftime("%m/%d %H:%M")
            })
            results.append(yahoo_data)
    
    # 利益額が大きい順に並べ替え
    results = sorted(results, key=lambda x: x["profit"], reverse=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
