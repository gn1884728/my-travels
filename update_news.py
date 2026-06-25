import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 目標清單
targets = [
    {"brand": "遠見", "url": "https://www.gvm.com.tw/category/16"},
    {"brand": "天下", "url": "https://www.cw.com.tw/magazine/cw"},
    {"brand": "商周", "url": "https://www.businessweekly.com.tw/"}
]

def fetch_news():
    news_items = []
    for t in targets:
        try:
            res = requests.get(t['url'], headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            # 這是通用抓法，實際運作時若沒抓到，我們之後再微調 CSS 選取器
            titles = soup.find_all(['h2', 'h3'], limit=3)
            for title in titles:
                news_items.append({
                    "brand": t['brand'],
                    "title": title.text.strip(),
                    "url": t['url'],
                    "time": datetime.now().strftime("%H:%M"),
                    "desc": "每日財經精選"
                })
        except Exception as e:
            print(f"Error fetching {t['brand']}: {e}")
    return news_items

# 更新 data.json
with open('data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
    # 將新聞存入 '6' 月份的 'news' 類別
    if '6' not in data: data['6'] = {}
    data['6']['news'] = fetch_news()
    f.seek(0)
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.truncate()
