import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

targets = [
    # 遠見：文章內頁通常包含 /article/ 或 /books/
    {"brand": "遠見", "url": "https://www.gvm.com.tw/newest", "base_url": "https://www.gvm.com.tw", "keyword": "/article/"},
    # 商周：文章內頁通常包含 /article/
    {"brand": "商周", "url": "https://www.businessweekly.com.tw/latest", "base_url": "https://www.businessweekly.com.tw", "keyword": "/article/"}
]

def fetch_news():
    news_items = []
    for t in targets:
        try:
            res = requests.get(t['url'], headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 尋找所有 <a> 標籤
            for link in soup.find_all('a', href=True):
                title = link.get_text(strip=True)
                href = link['href']
                
                # 關鍵邏輯：標題夠長，且連結強制包含我們定義的「文章關鍵字」
                if 12 < len(title) < 50 and t['keyword'] in href:
                    full_url = href if href.startswith('http') else t['base_url'] + href
                    
                    # 避免重複
                    if not any(n['title'] == title for n in news_items):
                        news_items.append({
                            "brand": t['brand'],
                            "title": title,
                            "url": full_url,
                            "time": datetime.now().strftime("%H:%M")
                        })
                
                # 每家各抓 3 則就收工
                if len([n for n in news_items if n['brand'] == t['brand']]) >= 3:
                    break
        except Exception as e: 
            print(f"Error fetching {t['brand']}: {e}")
    return news_items

# 寫入檔案
data = json.load(open('data.json', 'r', encoding='utf-8')) if os.path.exists('data.json') else {}
data['news'] = fetch_news()
with open('data.json', 'w', encoding='utf-8') as f: 
    json.dump(data, f, ensure_ascii=False, indent=4)
