import streamlit as st
import json
import os

st.set_page_config(page_title="ヤフートクスコ", page_icon="🛒", layout="wide")
st.title("🛒 ヤフートクスコ")

# items.jsonを読み込んで表示するだけのシンプルな役割
if os.path.exists("items.json"):
    with open("items.json", "r", encoding="utf-8") as f:
        items = json.load(f)
    
    for item in items:
        with st.container():
            st.write(f"### {item['name']}")
            st.write(f"💰 **利益目安: ¥{item['profit']:,}**")
            st.write(f"ヤフショ価格: ¥{item['price']:,} / 相場: ¥{item['buy_price']:,}")
            st.link_button("ヤフショで見る", item['url'])
            st.write("---")
else:
    st.info("データファイル(items.json)を生成中です。GitHubのActionsを実行してください。")
