import os
import requests
import json
from datetime import datetime

# ==================================================================
# ヤフートクスコ - Yahoo!ショッピングAPI版
# ==================================================================

YAHOO_CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID", "")

def fetch_yahoo_shopping(keyword, results=100):
    """Yahoo!ショッピング商品検索API"""
    print(f"🔍 '{keyword}' を検索中...")
    items = []
    try:
        url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
        params = {
            "appid": YAHOO_CLIENT_ID,
            "query": keyword,
            "results": results,
            "sort": "-score",
            "in_stock": True,
        }
        res = requests.get(url, params=params, timeout=15)
        data = res.json()

        hits = data.get("hits", [])
        for item in hits:
            items.append({
                "name": item.get("name", ""),
                "price": item.get("price", 0),
                "image": item.get("image", {}).get("medium", ""),
                "url": item.get("url", ""),
                "store": item.get("seller", {}).get("name", ""),
                "fetched_at": datetime.now().isoformat(),
            })
        print(f"✅ {len(items)}件取得")
    except Exception as e:
        print(f"❌ エラー: {e}")
    return items

def main():
    keywords = [
        "タイムセール",
        "激安",
        "送料無料 お得",
    ]

    all_items = []
    for kw in keywords:
        all_items.extend(fetch_yahoo_shopping(kw))

    with open("items.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"🎉 合計 {len(all_items)}件 → items.json に保存完了")

if __name__ == "__main__":
    main()
