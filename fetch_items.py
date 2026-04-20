import requests
import json
from datetime import datetime

# ============================================================
# ヤフートクスコ - Yahoo!ショッピングAPI版
# ============================================================

YAHOO_CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID", "")

import os

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
            name = item.get("name", "")
            price = item.get("price", 0)
            url_item = item.get("url", "")
            jan = item.get("janCode", "")
            shop = item.get("seller", {}).get("name", "")
            image = item.get("image", {}).get("small", "")

            if name and price:
                items.append({
                    "name": name,
                    "jan": jan,
                    "price": price,
                    "shop": shop,
                    "url": url_item,
                    "image": image,
                })

        print(f"  ✅ {len(items)}件取得")
    except Exception as e:
        print(f"  ❌ エラー: {e}")
    return items


# ============================================================
# メイン実行
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("🛒 ヤフートクスコ 商品取得開始")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    all_items = []

    # 検索キーワード一覧
    keywords = [
        "Nintendo Switch",
        "PlayStation 5",
        "iPhone",
        "iPad",
        "AirPods",
        "ポケモンカード",
    ]

    for keyword in keywords:
        all_items += fetch_yahoo_shopping(keyword)

    # 重複を除去（URLで判定）
    seen = set()
    unique_items = []
    for item in all_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique_items.append(item)

    print(f"\n📊 合計 {len(unique_items)} 商品取得")

    output = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(unique_items),
        "items": unique_items
    }

    with open("items.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("✅ items.json 保存完了！")
    print("=" * 50)
