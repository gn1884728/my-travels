import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# 這裡就是你可以隨意擴充的地方！直接新增媒體物件即可
targets = [
    {"brand": "遠見", "url": "https://www.gvm.com.tw/newest", "base_url": "https://www.gvm.com.tw"},
    {"brand": "天下", "url": "https://www.cw.com.tw/article/newest", "base_url": "https://www.cw.com.tw"},
    {"brand": "商周", "url": "https://www.businessweekly.com.tw/latest", "base_url": "https://www.businessweekly.com.tw"}
]

def fetch_news():
    news_items = []
    for t in targets:
        try:
            res = requests.get(t['url'], headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            # 尋找所有帶連結的標題標籤
            links = soup.find_all('a', href=True)
            for link in links:
                title = link.get_text(strip=True)
                href = link['href']
                if 12 < len(title) < 50:
                    # 補全完整連結
                    full_url = href if href.startswith('http') else t['base_url'] + href
                    news_items.append({"brand": t['brand'], "title": title, "url": full_url, "time": datetime.now().strftime("%H:%M")})
                if len([n for n in news_items if n['brand'] == t['brand']]) >= 3: break
        except Exception as e: print(f"Error: {e}")
    return news_items

data = json.load(open('data.json', 'r', encoding='utf-8')) if os.path.exists('data.json') else {}
data['news'] = fetch_news()
with open('data.json', 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=4)
