import streamlit as st
import json
import os

# ページ設定
st.set_page_config(page_title="ヤフートクスコ", page_icon="🛒", layout="wide")

# スタイル設定
st.markdown("""
    <style>
    .item-card { border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px; background-color: #f9f9f9; }
    .profit-text { color: #e74c3c; font-weight: bold; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛒 ヤフートクスコ")

# データの読み込み
if os.path.exists("items.json"):
    with open("items.json", "r", encoding="utf-8") as f:
        items = json.load(f)
    
    for item in items:
        with st.container():
            st.markdown(f"""
            <div class="item-card">
                <b>{item['name']}</b><br>
                <span class="profit-text">利益目安: 💰 ¥{item['profit']:,}</span><br>
                ヤフショ価格: ¥{item['price']:,} / 買取目安: ¥{item['buy_price']:,}
            </div>
            """, unsafe_allow_html=True)
            st.link_button("商品ページを開く", item['url'])
else:
    st.warning("データファイル(items.json)が見つかりません。Actionsを実行してください。")
