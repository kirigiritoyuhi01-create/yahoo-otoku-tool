import streamlit as st
import json
import os

st.set_page_config(page_title="ヤフートクスコ", page_icon="🛒", layout="wide")
st.title("🛒 ヤフートクスコ")

if os.path.exists("items.json"):
    with open("items.json", "r", encoding="utf-8") as f:
        items = json.load(f)
    for item in items:
        with st.container():
            st.write(f"### {item['name']}")
            st.write(f"💰 **利益目安: ¥{item['profit']:,}** (実質価格: ¥{int(item['price']*0.92):,})")
            st.link_button("ヤフショで見る", item['url'])
            st.write("---")
else:
    st.info("データファイル(items.json)を生成中です。GitHubのActionsを実行してください。")
