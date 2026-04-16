import streamlit as st
import json
import urllib.parse
from datetime import date

st.set_page_config(page_title="ヤフートクスコ", page_icon="🛒", layout="wide")
st.title("🛒 ヤフートクスコ")
st.caption("Yahoo!ショッピングのお得情報・ポイント計算ツール")

# items.json読み込み
try:
    with open("items.json", "r", encoding="utf-8") as f:
        items = json.load(f)
except:
    items = []
    st.warning("商品データが見つかりません。しばらくお待ちください。")

# サイドバー
with st.sidebar:
    st.header("🔍 検索条件")
    keyword = st.text_input("🔎 商品名で絞り込み", placeholder="例：Nintendo Switch")
    sort_order = st.radio("並び順", ["価格が安い順", "価格が高い順"])
    st.divider()
    st.caption(f"取得済み商品数：{len(items)}件")

# フィルタリング
if keyword:
    items = [i for i in items if keyword.lower() in i["name"].lower()]

# 並び替え
if sort_order == "価格が安い順":
    items = sorted(items, key=lambda x: x["price"])
else:
    items = sorted(items, key=lambda x: x["price"], reverse=True)

st.divider()
st.subheader(f"📦 商品一覧（{len(items)}件）")

if not items:
    st.info("該当する商品が見つかりませんでした。")
else:
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            if item.get("image"):
                st.image(item["image"], use_container_width=True)
            st.markdown(f"**{item['name'][:40]}...**" if len(item['name']) > 40 else f"**{item['name']}**")
            price = item['price']
            if price >= 99999990:
                st.markdown("💰 価格：要確認")
            else:
                st.markdown(f"💰 **¥{price:,}**")
            st.link_button("🛒 Yahoo!で見る", item["url"], use_container_width=True)
            st.divider()

st.caption("※本サイトはアフィリエイト広告を利用しています")
