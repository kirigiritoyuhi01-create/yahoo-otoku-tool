import os
import requests
import json
import csv
import time
from bs4 import BeautifulSoup
VC_ID = "3310634"
def get_items(url):
 headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
 response = requests.get(url, headers=headers)
 soup = BeautifulSoup(response.text, 'html.parser')
 items = soup.find_all('div', class_='item')
 return items
def fetch_items():
 url = "https://auctions.yahoo.co.jp/search/search"
 params = {"p": "search_word", "vc": VC_ID, "b": "1"}
 response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
 soup = BeautifulSoup(response.text, 'html.parser')
 items = soup.find_all('div', class_='item')
 return items
fetch_items()