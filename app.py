import streamlit as st
import json
import pandas as pd
from datetime import datetime

# ページ設定
st.set_page_config(page_title="ヤフートクスコ", page_icon="🛒", layout="wide")

# カスタムCSS（スマホで見やすく、ボタンを可愛く）
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
    .stButton>button {
        width: 100%;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# タイトル
st.title("🛒 ヤフートクスコ")
st.caption("ヤフショと買取屋の価格差を1秒でチェック")

# サイドバー：ポイント設定
with st.sidebar:
    st.header("⚙️ ポイント設定")
    base_step = st.number_input("PayPayステップ (%)", value=8)
    
    # キャンペーン自動判定
    today = datetime.now().day
    weekday = datetime.now().weekday()
    campaign_bonus = 0
    campaign_name = "特になし"
    
    if today in [5, 15, 25]:
        campaign_bonus = 4
        campaign_name = "5のつく日 (+4%)"
    elif today == 1:
        campaign_bonus = 4
        campaign_name = "ファーストデイ (+4%)"
    elif weekday == 6: # 日曜日
        campaign_bonus = 4
        campaign_name = "LYPプレミアム (+4%)"
    
    st.info(f"📅 本日のキャンペーン: {campaign_name}")
    total_rate = (base_step + campaign_bonus) / 100

# データ読み込み
try:
    with open("items.json", "r", encoding="utf-8") as f:
        items = json.load(f)
except:
    items = []

if not items:
    st.warning("データ更新中です。しばらくお待ちください。")
else:
    # 並び替えボタン
    col_btn1, col_btn2 = st.columns(2)
    sort_key = "profit"
    if col_btn1.button("💰 利益額順"):
        sort_key = "profit"
    if col_btn2.button("📈 利益率順"):
        sort_key = "profit_rate"
    
    sorted_items = sorted(items, key=lambda x: x[sort_key], reverse=True)

    # 商品一覧表示
    for item in sorted_items:
        # 正確な再計算
        points = int(item["price"] * total_rate)
        jisshitsu = item["price"] - points
        real_profit = item["buy_price"] - jisshitsu
        real_rate = round((real_profit / jisshitsu) * 100, 1)

        with st.container():
            st.markdown(f"""
            <div class="item-card">
                <img src="{item['image']}" style="width:100px; float:left; margin-right:15px;">
                <b>{item['name'][:40]}...</b><br>
                実質価格: ¥{jisshitsu:,} <small>(定価: ¥{item['price']:,})</small><br>
                <span class="profit-text">利益: 💰¥{real_profit:,} ({real_rate}%)</span>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("詳細・販路を広げる🌏"):
                st.write(f"🏠 ショップ: {item['shop']}")
                st.write(f"🆔 JAN: {item['jan']}")
                st.write(f"📈 現在の相場目安: ¥{item['buy_price']:,}")
                
                c1, c2, c3 = st.columns(3)
                c1.link_button("ヤフショ", item["url"])
                # 販路展開（メインキーワードで検索するリンク）
                keyword = item['name'][:15]
                c2.link_button("メルカリ", f"https://jp.mercari.com/search?keyword={keyword}")
                c3.link_button("eBay", f"https://www.ebay.com/sch/i.html?_nkw={item['jan']}")
                
                st.button(f"🐦 Xでシェアする", key=item['jan'])

# 右下のAIチャット風（簡易版）
# 右下のAIチャット風（リスク回避・事務的スタイル）
st.sidebar.markdown("---")
st.sidebar.subheader("📋 秘書レポート")
st.sidebar.write(f"本日は「{campaign_name}」が適用されています。")
st.sidebar.write("各ショップの評価を確認し、安全な取引を優先してください。")
