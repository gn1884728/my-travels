import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 使用更廣泛的標題抓取策略
targets = [
    {"brand": "遠見", "url": "https://www.gvm.com.tw/newest"},
    {"brand": "天下", "url": "https://www.cw.com.tw/article/newest"},
    {"brand": "商周", "url": "https://www.businessweekly.com.tw/latest"}
]

def fetch_news():
    news_items = []
    for t in targets:
        try:
            res = requests.get(t['url'], headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 尋找頁面上所有 h2, h3 標籤，並篩選長度大於 10 個字以上的 (通常才是新聞標題)
            candidates = soup.find_all(['h2', 'h3', 'a'])
            count = 0
            for el in candidates:
                title = el.get_text(strip=True)
                # 篩選標準：長度夠長，且不包含一些無用的網頁導覽字眼
                if 12 < len(title) < 50 and any(char.isalpha() or '\u4e00' <= char <= '\u9fff' for char in title):
                    # 避免重複
                    if not any(item['title'] == title for item in news_items):
                        news_items.append({
                            "brand": t['brand'],
                            "title": title,
                            "url": t['url'],
                            "time": datetime.now().strftime("%H:%M"),
                            "desc": "最新財經趨勢"
                        })
                        count += 1
                if count >= 3: break # 每家只抓 3 則
        except Exception as e:
            print(f"Error: {t['brand']} - {e}")
    return news_items

# 執行更新
if os.path.exists('data.json'):
    with open('data.json', 'r', encoding='utf-8') as f:
        try: data = json.load(f)
        except: data = {}
else:
    data = {}

data['news'] = fetch_news()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
