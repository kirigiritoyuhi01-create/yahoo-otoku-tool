import streamlit as st
import urllib.parse
from datetime import date

st.set_page_config(page_title="ヤフートクスコ", page_icon="🛒", layout="wide")

st.title("🛒 ヤフートクスコ")
st.caption("Yahoo!ショッピングのお得情報・ポイント計算ツール")

# サイドバー：フィルター設定
with st.sidebar:
    st.header("🔧 検索条件")
    
    price_range = st.radio(
        "価格帯",
        ["すべて", "低価格（〜10,000円）", "中価格（10,001〜50,000円）", "高価格（50,001円〜）"]
    )
    
    sort_order = st.radio(
        "並び順",
        ["お得額が高い順", "お得率が高い順", "価格が安い順"]
    )
    
    st.divider()
    st.subheader("💡 ポイント設定")
    base_point = st.number_input("基本ポイント還元率（%）", min_value=1.0, value=1.0, step=0.5)
    rank_bonus = st.selectbox("会員ランクボーナス", ["×1（通常）", "×2（ゴールド）", "×3（プラチナ）"])
    rank_mul = float(rank_bonus[1])

# メイン：キーワード検索
keyword = st.text_input("🔍 商品名を入力", placeholder="例：Nintendo Switch、エアコン")

# 今日のキャンペーン自動表示
today = date.today().day
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 今日のお得情報")
    if today in [10, 20, 30]:
        st.success("🎉 0のつく日！ポイント最大2倍")
        campaign_mul = 2.0
    elif today in [5, 15, 25]:
        st.info("📌 5のつく日！PayPay残高でポイントUP")
        campaign_mul = 1.5
    else:
        next_day = 10 if today < 10 else 20 if today < 20 else 30 if today < 30 else "来月10日"
        st.warning(f"⏳ 次のお得な日：{next_day}日")
        campaign_mul = 1.0

with col2:
    st.subheader("🧮 ポイントシミュレーター")
    sim_price = st.number_input("購入予定金額（円）", min_value=0, value=10000, step=500)
    total_rate = base_point * rank_mul * campaign_mul
    point_get = int(sim_price * total_rate / 100)
    real_cost = sim_price - point_get
    st.metric("獲得予定ポイント", f"{point_get:,} pt")
    st.metric("実質購入価格", f"¥{real_cost:,}")
    st.caption(f"還元率：{total_rate:.1f}%（基本{base_point}% × ランク{rank_mul}倍 × キャンペーン{campaign_mul}倍）")

# 検索リンク
if keyword:
    st.divider()
    encoded = urllib.parse.quote(keyword)
    
    # 価格帯パラメータ
    price_param = ""
    if price_range == "低価格（〜10,000円）":
        price_param = "&max_price=10000"
    elif price_range == "中価格（10,001〜50,000円）":
        price_param = "&min_price=10001&max_price=50000"
    elif price_range == "高価格（50,001円〜）":
        price_param = "&min_price=50001"

    # 並び順パラメータ
    sort_param = ""
    if sort_order == "価格が安い順":
        sort_param = "&sort=price"

    yahoo_url = f"https://shopping.yahoo.co.jp/search?p={encoded}{price_param}{sort_param}"
    yahuco_url = f"https://auctions.yahoo.co.jp/search/search?p={encoded}"
    paypay_url = f"https://paypayflea.com/search/product?search_query={encoded}"

    st.subheader(f"「{keyword}」の検索結果")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.link_button("🛍️ Yahoo!ショッピング", yahoo_url, use_container_width=True)
    with col4:
        st.link_button("🔨 ヤフオク", yahuco_url, use_container_width=True)
    with col5:
        st.link_button("📦 PayPayフリマ", paypay_url, use_container_width=True)

st.divider()
st.caption("※本サイトはアフィリエイト広告を利用しています")
