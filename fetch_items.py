import os, requests, json, subprocess
YAHOO_CLIENT_ID = os.environ.get("YAHOO_CLIENT_ID")
JAN_LIST = [{"jan": "4902370550733", "buy_price": 42000}, {"jan": "4948872415545", "buy_price": 62000}]

def main():
    results = []
    for t in JAN_LIST:
        res = requests.get("https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch", params={"appid": YAHOO_CLIENT_ID, "jan_code": t["jan"], "results": 1})
        data = res.json()
        if "hits" in data and data["hits"]:
            item = data["hits"][0]
            profit = t["buy_price"] - int(item["price"] * 0.92)
            results.append({"name": item["name"], "price": int(item["price"]), "url": item["url"], "profit": profit, "buy_price": t["buy_price"]})
    
    with open("items.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    # GitHubに保存する命令
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"])
    subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    subprocess.run(["git", "add", "items.json"])
    subprocess.run(["git", "commit", "-m", "update data"], check=False)
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    main()
