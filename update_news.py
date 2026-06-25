import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 各來源設定
# article_keyword：網址必須包含此字串，才算是文章直連網址
targets = [
    {
        "brand": "遠見",
        "url": "https://www.gvm.com.tw/newest",
        "base_url": "https://www.gvm.com.tw",
        "article_keyword": "/article/"   # 遠見文章格式：/article/數字
    },
    {
        "brand": "商周",
        "url": "https://www.businessweekly.com.tw/latest",
        "base_url": "https://www.businessweekly.com.tw",
        "article_keyword": "/article/"   # 商周文章格式：含 /article/
    }
]

def fetch_news():
    news_items = []

    for t in targets:
        try:
            res = requests.get(t["url"], headers=headers, timeout=20)
            if res.status_code != 200:
                print(f"[{t['brand']}] HTTP {res.status_code}，跳過")
                continue

            soup = BeautifulSoup(res.text, "html.parser")

            for link in soup.find_all("a", href=True):
                title = link.get_text(strip=True)
                href  = link.get("href", "")

                # 組完整網址
                if href.startswith("http"):
                    full_url = href
                elif href.startswith("/"):
                    full_url = t["base_url"] + href
                else:
                    continue  # 相對路徑不明確，略過

                # ✅ 核心篩選：
                # 1. 標題長度合理（10~80字）
                # 2. 網址必須含文章關鍵字（確保是文章直連，不是首頁/分類頁）
                # 3. 排除重複標題
                if (
                    10 < len(title) < 80
                    and t["article_keyword"] in full_url
                    and not any(n["title"] == title for n in news_items)
                ):
                    news_items.append({
                        "brand": t["brand"],
                        "title": title,
                        "url": full_url,
                        "time": datetime.now().strftime("%H:%M")
                    })

                # 每個來源最多抓 5 篇
                if len([n for n in news_items if n["brand"] == t["brand"]]) >= 5:
                    break

        except Exception as e:
            print(f"[{t['brand']}] 錯誤：{e}")

    return news_items


# ── 主程式：更新 data.json ──
data = json.load(open("data.json", "r", encoding="utf-8")) if os.path.exists("data.json") else {}

data["news"] = fetch_news()
data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"✅ 完成，共抓到 {len(data['news'])} 篇文章")
