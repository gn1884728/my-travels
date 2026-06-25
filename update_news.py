import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 修正：針對最新文章頁面的精準 CSS 標籤
targets = [
    {"brand": "遠見", "url": "https://www.gvm.com.tw/newest", "selector": ".list-item-title"},
    {"brand": "天下", "url": "https://www.cw.com.tw/article/newest", "selector": ".article-card__title"},
    {"brand": "商周", "url": "https://www.businessweekly.com.tw/latest", "selector": ".article-title"}
]

def fetch_news():
    news_items = []
    for t in targets:
        try:
            res = requests.get(t['url'], headers=headers, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 改為選取該 class 下的 <a> 標籤內文字
            elements = soup.select(t['selector'], limit=3)
            
            for el in elements:
                title = el.get_text(strip=True)
                if len(title) > 5:
                    news_items.append({
                        "brand": t['brand'],
                        "title": title,
                        "url": t['url'], # 如果需要連結更準確，可以改為 el.get('href')
                        "time": datetime.now().strftime("%H:%M"),
                        "desc": "每日快訊"
                    })
        except Exception as e:
            print(f"Error fetching {t['brand']}: {e}")
    return news_items

# 更新檔案
with open('data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
    data['news'] = fetch_news()
    f.seek(0)
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.truncate()
