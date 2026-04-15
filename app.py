import streamlit as st
import urllib.parse
from datetime import date

st.set_page_config(page_title="ヤフ得ツール改良版", page_icon="🛍️", layout="wide")

VC_ID = "YOUR_VC_ID"

st.title("🛍️ ヤフ得ツール改良版")
st.caption("Yahoo!ショッピングのお得情報をまとめてチェック")

keyword = st.text_input("🔍 商品名・キーワードを入力", placeholder="例：エアコン、Nintendo Switch")

if keyword:
    encoded = urllib.parse.quote(keyword)
    st.subheader("📦 検索結果リンク")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Yahoo!ショッピング")
        yahoo_url = f"https://shopping.yahoo.co.jp/search?p={encoded}&vcptn={VC_ID}"
        st.link_button("Yahoo!ショッピングで検索 →", yahoo_url)
        st.caption("Paypayポイント還元あり")
    with col2:
        st.markdown("### ヤフオク")
        st.link_button("ヤフオクで検索 →", f"https://auctions.yahoo.co.jp/search/search?p={encoded}")
        st.caption("中古・掘り出し物を探す")
    with col3:
        st.markdown("### PayPayフリマ")
        st.link_button("PayPayフリマで検索 →", f"https://paypayflea.com/search/product?search_query={encoded}")
        st.caption("フリマ最安値をチェック")
    st.divider()
    st.subheader("💡 今日のお得情報")
    today = date.today().day
    if today in [10, 20, 30]:
        st.success("🎉 今日は0のつく日！Yahoo!ショッピングでポイント最大2倍")
    elif today in [5, 15, 25]:
        st.info("📅 今日は5のつく日 - PayPay残高払いでポイントUP")
    else:
        next_day = 10 if today < 10 else 20 if today < 20 else 30 if today < 30 else "来月10日"
        st.info(f"📅 次のお得な日: {next_day}日")

st.divider()
st.caption("※本サイトはアフィリエイト広告を利用しています")
