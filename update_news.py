import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 為了繞過防爬機制，加上更完整的 User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

targets = [
    {"brand": "遠見", "url": "https://www.gvm.com.tw/newest", "selector": ".list-item-title"},
    {"brand": "天下", "url": "https://www.cw.com.tw/article", "selector": ".article-card__title"},
    {"brand": "商周", "url": "https://www.businessweekly.com.tw/latest", "selector": ".article-title"}
]

def fetch_news():
    news_items = []
    for t in targets:
        try:
            res = requests.get(t['url'], headers=headers, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 使用指定好的 selector 抓取
            elements = soup.select(t['selector'], limit=3)
            
            for el in elements:
                title_text = el.text.strip()
                if len(title_text) > 8: # 字數限制設長一點，過濾無效標題
                    news_items.append({
                        "brand": t['brand'],
                        "title": title_text,
                        "url": t['url'],
                        "time": datetime.now().strftime("%H:%M"),
                        "desc": "每日精選"
                    })
        except Exception as e:
            print(f"抓取 {t['brand']} 失敗: {e}")
            continue
    return news_items

# 讀取並更新 data.json
with open('data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
    data['news'] = fetch_news()
    f.seek(0)
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.truncate()
