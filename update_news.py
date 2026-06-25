import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

targets = [
    {"brand": "遠見", "url": "https://www.gvm.com.tw/newest", "base_url": "https://www.gvm.com.tw", "keyword": "/article/"},
    {"brand": "商周", "url": "https://www.businessweekly.com.tw/latest", "base_url": "https://www.businessweekly.com.tw", "keyword": "/article/"}
]

def fetch_news():
    news_items = []
    for t in targets:
        try:
            res = requests.get(t['url'], headers=headers, timeout=20) # 延長 timeout
            if res.status_code != 200: continue
            soup = BeautifulSoup(res.text, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                # 安全獲取屬性，如果沒標題直接跳過
                title = link.get_text(strip=True)
                href = link.get('href', '')
                
                if 10 < len(title) < 60 and t['keyword'] in href:
                    full_url = href if href.startswith('http') else t['base_url'] + href
                    # 避免重複
                    if not any(n['title'] == title for n in news_items):
                        news_items.append({
                            "brand": t['brand'],
                            "title": title,
                            "url": full_url,
                            "time": datetime.now().strftime("%H:%M")
                        })
                
                if len([n for n in news_items if n['brand'] == t['brand']]) >= 3:
                    break
        except Exception as e:
            print(f"Skipping {t['brand']} due to error: {e}")
            continue
    return news_items

# 確保 data.json 存在且格式正確
if not os.path.exists('data.json'):
    data = {}
else:
    with open('data.json', 'r', encoding='utf-8') as f:
        try: data = json.load(f)
        except: data = {}

data['news'] = fetch_news()

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
