import streamlit as st
import json
import os
from datetime import datetime

# ページ設定
st.set_page_config(page_title="ヤフートクスコ", page_icon="🛒", layout="wide")

# スタイル設定
st.markdown("""
    <style>
    .item-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #f9f9f9;
    }
    .profit-text {
        color: #e74c3c;
        font-weight: bold;
        font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)

# タイトル
st.title("🛒 ヤフートクスコ")
st.caption("ヤフショ価格と相場の差を1秒でチェック")

# サイドバー設定
with st.sidebar:
    st.header("⚙️ ポイント設定")
    paypay_rate = st.number_input("PayPayステップ (%)", value=8.0) / 100

# データ読み込み
if os.path.exists("items.json"):
    with open("items.json", "r", encoding="utf-8") as f:
        items = json.load(f)
else:
    items = []

if not items:
    st.info("現在、データを収集しています。GitHubのActionsから実行するか、1分ほどお待ちください。")
else:
    # 利益額順に並び替え
    sorted_items = sorted(items, key=lambda x: x['profit'], reverse=True)
    
    for item in sorted_items:
        with st.container():
            st.markdown(f"""
            <div class="item-card">
                <b>{item['name'][:50]}...</b><br>
                実質価格: ¥{int(item['price'] * (1 - paypay_rate)):,} <small>(定価: ¥{item['price']:,})</small><br>
                <span class="profit-text">利益目安: 💰 ¥{item['profit']:,}</span>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("詳細・リンク"):
                st.write(f"📈 現在の相場目安: ¥{item['buy_price']:,}")
                st.link_button("ヤフショで商品を見る", item['url'])

# 秘書レポート
st.sidebar.markdown("---")
st.sidebar.subheader("📋 秘書レポート")
st.sidebar.write("データが古い場合はGitHubのActionsを手動実行してください。")
