import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 三個網站的定義
targets = [
    {"brand": "遠見", "url": "https://www.gvm.com.tw/newest"},
    {"brand": "天下", "url": "https://www.cw.com.tw/"},
    {"brand": "商周", "url": "https://www.businessweekly.com.tw/"}
]

def fetch_news():
    news_items = []
    for t in targets:
        try:
            res = requests.get(t['url'], headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            # 針對不同網站抓取標題
            # 這裡簡單抓取 h2/h3 標籤
            titles = soup.find_all(['h2', 'h3'], limit=2) 
            for title in titles:
                text = title.text.strip()
                if len(text) > 5: # 過濾過短的字串
                    news_items.append({
                        "brand": t['brand'],
                        "title": text,
                        "url": t['url'],
                        "time": datetime.now().strftime("%H:%M"),
                        "desc": "最新報導"
                    })
        except: continue
    return news_items

# 讀取並更新 data.json，將 news 獨立出來，不放在月份下面
with open('data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
    data['news'] = fetch_news() # 直接放在根目錄，不需要月份
    f.seek(0)
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.truncate()
