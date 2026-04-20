```python
import requests
import json

def fetch_items(jan_code):
    url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
    params = {
        "appid": "dj00aiZpPUd0T3Q2eE5YRjNiWiZzPWNvbnN1bWVyc2V0fGlsZW6Fbl9lcw--",
        "jan_code": jan_code,
        "results": 10
    }
    response = requests.get(url, params=params)
    return json.loads(response.text)

# 検索するJANコードを入力してください
jan_code = "4580123456789"
items = fetch_items(jan_code)
print(items)
```