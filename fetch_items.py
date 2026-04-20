import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

# ============================================================
# ヤフトクスコ - 買取価格取得スクリプト
# 対象：ルデヤ・森森買取・買取wiki・家電市場・買取商店
# 実行：GitHub Actions 毎日18時
# ============================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_price(text):
    """価格テキストから数値を抽出"""
    if not text:
        return None
    nums = re.sub(r"[^\d]", "", text)
    return int(nums) if nums else None

# ============================================================
# 1. 買取ルデヤ
# ============================================================
def fetch_rudeya():
    print("📦 ルデヤ取得中...")
    items = []
    try:
        res = requests.get("https://kaitori-rudeya.com/focus", headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        for row in soup.select("div.product-item, tr"):
            name_el = row.select_one("h2, h3, .product-name, a[href*='/product/item/']")
            price_el = row.select_one(".price, .buy-price, td")
            jan_el = row.find(string=re.compile(r"\d{13}"))

            if not name_el:
                continue

            name = name_el.get_text(strip=True)
            price_text = price_el.get_text(strip=True) if price_el else ""
            price = clean_price(price_text)
            jan = jan_el.strip() if jan_el else ""

            if name and price and price > 0:
                items.append({
                    "name": name,
                    "jan": jan,
                    "price": price,
                    "shop": "ルデヤ",
                    "url": "https://kaitori-rudeya.com/focus"
                })

        print(f"  ✅ {len(items)}件取得")
    except Exception as e:
        print(f"  ❌ エラー: {e}")
    return items

# ============================================================
# 2. 森森買取
# ============================================================
def fetch_morimori():
    print("📦 森森買取取得中...")
    items = []
    try:
        res = requests.get("https://www.morimori-kaitori.jp/", headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        for row in soup.select("div.product, tr, .item-row"):
            name_el = row.select_one("h3, h4, a[href*='/product/']")
            price_el = row.select_one(".price, .buy-price, strong")
            jan_text = row.get_text()
            jan_match = re.search(r"JAN[：:]\s*(\d{8,13})", jan_text)

            if not name_el:
                continue

            name = name_el.get_text(strip=True)
            price = clean_price(price_el.get_text(strip=True)) if price_el else None
            jan = jan_match.group(1) if jan_match else ""

            if name and price and price > 0:
                items.append({
                    "name": name,
                    "jan": jan,
                    "price": price,
                    "shop": "森森買取",
                    "url": "https://www.morimori-kaitori.jp/"
                })

        print(f"  ✅ {len(items)}件取得")
    except Exception as e:
        print(f"  ❌ エラー: {e}")
    return items

# ============================================================
# 3. 買取wiki
# ============================================================
def fetch_kaitoriwiki():
    print("📦 買取wiki取得中...")
    items = []
    try:
        # ページネーション対応（最初の5ページ）
        for page in range(1, 6):
            url = f"https://gamekaitori.jp/search/{page}"
            res = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")

            for row in soup.select("li.goods-list-item, .product-item"):
                name_el = row.select_one("a, h3, h4")
                price_el = row.select_one(".price, .buy-price")
                jan_text = row.get_text()
                jan_match = re.search(r"JAN[：:]\s*(\d{8,13})", jan_text)

                if not name_el:
                    continue

                name = name_el.get_text(strip=True)
                price = clean_price(price_el.get_text(strip=True)) if price_el else None
                jan = jan_match.group(1) if jan_match else ""

                if name and price and price > 0:
                    items.append({
                        "name": name,
                        "jan": jan,
                        "price": price,
                        "shop": "買取wiki",
                        "url": url
                    })

            time.sleep(1)  # サーバー負荷軽減

        print(f"  ✅ {len(items)}件取得")
    except Exception as e:
        print(f"  ❌ エラー: {e}")
    return items

# ============================================================
# 4. 家電市場
# ============================================================
def fetch_kaden_ichiba():
    print("📦 家電市場取得中...")
    items = []
    try:
        for page in range(1, 4):
            url = f"https://www.kaden-ichiba.com/item?impo=1&page={page}"
            res = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")

            for row in soup.select("tr"):
                tds = row.select("td")
                if len(tds) < 3:
                    continue

                text = row.get_text()
                jan_match = re.search(r"JAN[：:]\s*(\d{8,13})", text)
                name_el = row.select_one("strong, b, a")
                price_el = None

                # 「強化買取」バッジの次の価格を探す
                for td in tds:
                    price_text = td.get_text(strip=True)
                    if re.search(r"\d+,\d+円|\d+円", price_text):
                        price_el = td
                        break

                if not name_el:
                    continue

                name = name_el.get_text(strip=True)
                price = clean_price(price_el.get_text(strip=True)) if price_el else None
                jan = jan_match.group(1) if jan_match else ""

                if name and price and price > 0:
                    items.append({
                        "name": name,
                        "jan": jan,
                        "price": price,
                        "shop": "家電市場",
                        "url": url
                    })

            time.sleep(1)

        print(f"  ✅ {len(items)}件取得")
    except Exception as e:
        print(f"  ❌ エラー: {e}")
    return items

# ============================================================
# 5. 買取商店（JANコードリストから検索）
# ============================================================
def fetch_kaitorishouten(jan_list):
    print("📦 買取商店取得中...")
    items = []
    try:
        for jan in jan_list[:50]:  # 最大50件
            url = f"https://www.kaitorishouten-co.jp/search?q={jan}"
            res = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")

            name_el = soup.select_one("h1, h2, .product-name")
            price_el = soup.select_one(".price, .buy-price, strong")

            if name_el and price_el:
                name = name_el.get_text(strip=True)
                price = clean_price(price_el.get_text(strip=True))
                if price and price > 0:
                    items.append({
                        "name": name,
                        "jan": jan,
                        "price": price,
                        "shop": "買取商店",
                        "url": url
                    })

            time.sleep(1)  # 検索型なのでより丁寧に待機

        print(f"  ✅ {len(items)}件取得")
    except Exception as e:
        print(f"  ❌ エラー: {e}")
    return items

# ============================================================
# JANコードごとに買取最高値をまとめる
# ============================================================
def merge_by_jan(all_items):
    merged = {}
    for item in all_items:
        jan = item["jan"]
        if not jan:
            continue
        if jan not in merged:
            merged[jan] = {
                "name": item["name"],
                "jan": jan,
                "kaitori": {}
            }
        shop = item["shop"]
        price = item["price"]
        # 同じ店で複数ある場合は最高値を採用
        if shop not in merged[jan]["kaitori"] or price > merged[jan]["kaitori"][shop]:
            merged[jan]["kaitori"][shop] = price

    # 買取最高値を計算
    result = []
    for jan, data in merged.items():
        max_price = max(data["kaitori"].values()) if data["kaitori"] else 0
        data["kaitori_max"] = max_price
        data["kaitori_shop"] = max(data["kaitori"], key=data["kaitori"].get) if data["kaitori"] else ""
        result.append(data)

    return result

# ============================================================
# メイン実行
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("🛒 ヤフトクスコ 買取価格取得開始")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    all_items = []

    # 各サイトから取得
    all_items += fetch_rudeya()
    time.sleep(2)
    all_items += fetch_morimori()
    time.sleep(2)
    all_items += fetch_kaitoriwiki()
    time.sleep(2)
    all_items += fetch_kaden_ichiba()

    # JANコードリストを集めて買取商店を検索
    jan_list = list(set([i["jan"] for i in all_items if i["jan"]]))
    time.sleep(2)
    all_items += fetch_kaitorishouten(jan_list)

    # JANコードでまとめる
    merged = merge_by_jan(all_items)

    print(f"\n📊 合計 {len(merged)} 商品取得")

    # items.jsonに保存
    output = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(merged),
        "items": merged
    }

    with open("items.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("✅ items.json 保存完了！")
    print("=" * 50)
