import os
import json
import urllib.request

def fetch_items(query):
    url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
    params = {
        "appid": os.environ.get("YAHOO_CLIENT_ID"),
        "query": query,
        "results": 10
    }
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"}, data=json.dumps(params).encode("utf-8"))
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode("utf-8"))
    return data["hits"]