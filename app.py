import streamlit as st
import json
import os

# ページ設定
st.set_page_config(page_title="ヤフートクスコ", page_icon="🛒", layout="wide")

st.title("🛒 ヤフートクスコ")
st.caption("ヤフショ価格と相場の差を1秒でチェック")

# データ読み込み
if os.path.exists("items.json"):
    with open("items.json", "r", encoding="utf-8") as f:
        items = json.load(f)
    
    for item in items:
        with st.container():
            st.subheader(item['name'])
            st.write(f"💰 **利益目安: ¥{item['profit']:,}**")
            st.write(f"ヤフショ価格: ¥{item['price']:,} / 相場: ¥{item['buy_price']:,}")
            st.link_button("ヤフショで見る", item['url'])
            st.write("---")
else:
    st.info("現在データを準備しています。GitHub Actionsの完了をお待ちください。")
