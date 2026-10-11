# 翰林版 選修生物（Ⅲ）互動教學網站

首頁 `index.html` → 六個章節頁 `chapter1.html`～`chapter6.html` → 各節互動教學網頁（本資料夾內 `ch1-1/`～`ch6-4/`、`lab1-1/`～`lab6-3/`）與教學影片（Google 雲端硬碟）。

## 章節（依課本）
1. 動物體的組成與恆定性　2. 循環與消化　3. 呼吸與排泄　4. 感應　5. 防禦　6. 生殖

## 檔案
- `index.html`、`chapter1~6.html`：由 `build_site3.py` 產生，內容資料（簡介、本節重點、關鍵詞、頁碼、影片 ID）在 `chapters3.py`
- `style.css`、`app.js`：共用樣式與互動（與必修、選修Ⅰ入口網站同一套）
- `img/cover1~6.jpg`：課本章扉頁；`img/s*.jpg`：各節課本代表圖；`img/a*.jpg`：探討活動課本圖

## 修改方式
編輯 `chapters3.py` 後，在本資料夾執行 `python3 build_site3.py .`。
