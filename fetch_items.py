import os
import requests

def fetch_items(query):
    url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
    params = {
        "appid": os.environ.get("YAHOO_CLIENT_ID"),
        "query": query,
        "results": 10
    }
    response = requests.get(url, params=params)
    return response.json()["hits"]