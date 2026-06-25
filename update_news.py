name: Daily News Update
on:
  schedule:
    - cron: '0 8 * * *'
  workflow_dispatch: 

permissions:
  contents: write

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Run crawler
        run: python update_news.py

      - name: Commit and Push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data.json
          # 如果沒有變更，git commit 會失敗，我們用 || echo 忽略錯誤，確保任務成功
          git commit -m "自動更新財經新聞與時間戳記" || echo "沒有新的資料變更，跳過 Commit"
          git push || echo "沒有新的推送，跳過 Push"
