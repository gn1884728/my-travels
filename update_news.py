import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ✅ 改用 Google News RSS，不會被反爬蟲擋，文章連結是直連
targets = [
    {
        "brand": "遠見",
        "rss_url": "https://news.google.com/rss/search?q=site:gvm.com.tw&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        "limit": 5
    },
    {
        "brand": "商周",
        "rss_url": "https://news.google.com/rss/search?q=site:businessweekly.com.tw&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
        "limit": 5
    }
]

def fetch_news():
    news_items = []

    for t in targets:
        try:
            res = requests.get(t["rss_url"], headers=headers, timeout=20)
            if res.status_code != 200:
                print(f"[{t['brand']}] HTTP {res.status_code}，跳過")
                continue

            # 解析 XML
            root = ET.fromstring(res.content)
            channel = root.find("channel")
            if channel is None:
                print(f"[{t['brand']}] 找不到 channel")
                continue

            count = 0
            for item in channel.findall("item"):
                title = item.findtext("title", "").strip()
                url   = item.findtext("link", "").strip()

                # 篩選：標題長度合理 + 不重複
                if (
                    10 < len(title) < 100
                    and url
                    and not any(n["title"] == title for n in news_items)
                ):
                    news_items.append({
                        "brand": t["brand"],
                        "title": title,
                        "url": url,
                        "time": datetime.now().strftime("%H:%M")
                    })
                    count += 1

                if count >= t["limit"]:
                    break

            print(f"[{t['brand']}] 抓到 {count} 篇")

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
