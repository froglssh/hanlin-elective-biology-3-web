import os, shutil, json

base_dir = "/Users/froglssh/Library/CloudStorage/GoogleDrive-frog@lssh.tp.edu.tw/我的雲端硬碟/04教科書/0自編教材/翰林/PPT動畫/選修生物3"
site_dir = os.path.join(base_dir, "選修生物3教材網站")
os.makedirs(site_dir, exist_ok=True)

# 讀取雲端影片總表 JSON
md_path = os.path.join(base_dir, "選修生物3教學影片雲端硬碟網址總表.md")
with open(md_path, "r", encoding="utf-8") as f:
    t = f.read()
json_str = t.split("```json\n")[1].split("\n```")[0]
video_data = json.loads(json_str)
video_map = {item["code"]: item for item in video_data}

# 章節定義結構 (選修生物3 共 6 章)
chapters = [
    {
        "id": 1,
        "title": "動物體的組成與恆定性",
        "desc": "探索動物四大基本組織（皮膜、結締、肌肉、神經）的微觀構造與生理功能，並理解體內恆定機制的負回饋調節核心思維。",
        "icon": "🧬",
        "cover": "img/cover1.jpg",
        "units": [
            {
                "code": "CH1-1",
                "slug": "ch1-1",
                "folder": "CH1-1-動物組織的構造與功能",
                "title": "動物組織的構造與功能",
                "desc": "深入剖析上皮、結締、肌肉與神經四大組織之細胞特化型態、排列方式與生理分工。",
                "img": "img/s1-1.jpg"
            },
            {
                "code": "CH1-2",
                "slug": "ch1-2",
                "folder": "CH1-2-恆定的生理意義與重要性",
                "title": "恆定的生理意義與重要性",
                "desc": "探討內環境恆定之概念，解析神經與內分泌系統協同調控體溫、血糖、水鹽之負回饋機制。",
                "img": "img/s1-2.jpg"
            },
            {
                "code": "探討1-1",
                "slug": "lab1-1",
                "folder": "探討活動1-1-動物組織的觀察",
                "title": "動物組織的觀察",
                "desc": "實作顯微鏡觀察人體與動物之各類切片標本，精準判讀組織細胞特徵與染色表現。",
                "img": "img/a1-1.jpg"
            }
        ]
    },
    {
        "id": 2,
        "title": "循環與消化",
        "desc": "從心血管動力學、微血管物質交換，到消化道各器官之機械消化與化學水解作用，透視動物體能量與物質流通的生命中樞。",
        "icon": "❤️",
        "cover": "img/cover2.jpg",
        "units": [
            {
                "code": "CH2-1",
                "slug": "ch2-1",
                "folder": "CH2-1-循環系統",
                "title": "循環系統",
                "desc": "解析心臟跳動週期、瓣膜啟閉、動靜脈血管構造、血壓調節機制及淋巴循環之物質回收。",
                "img": "img/s2-1.jpg"
            },
            {
                "code": "CH2-2",
                "slug": "ch2-2",
                "folder": "CH2-2-消化系統",
                "title": "消化系統",
                "desc": "探索口腔、胃、小腸及大腸之酵素水解歷程，解析小腸絨毛吸收與乳糜管運輸原理。",
                "img": "img/s2-2.jpg"
            },
            {
                "code": "探討2-1",
                "slug": "lab2-1",
                "folder": "探討活動2-1-心臟的觀察",
                "title": "心臟的觀察",
                "desc": "藉由哺乳動物（豬心）解剖觀察心房、心室、瓣膜與大血管出入口之立體解剖連通關係。",
                "img": "img/a2-1.jpg"
            }
        ]
    },
    {
        "id": 3,
        "title": "呼吸與排泄",
        "desc": "掌握肺臟氣體交換與氧氣/二氧化碳血液運輸化學，並深入腎元之過濾、再吸收與分泌機制，解析體液滲透壓與酸鹼恆定。",
        "icon": "🫁",
        "cover": "img/cover3.jpg",
        "units": [
            {
                "code": "CH3-1",
                "slug": "ch3-1",
                "folder": "CH3-1-呼吸系統",
                "title": "呼吸系統",
                "desc": "探討胸廓呼吸運動、肺泡氣體交換、血紅素氧氣解離曲線及血液中二氧化碳的運輸模式。",
                "img": "img/s3-1.jpg"
            },
            {
                "code": "CH3-2",
                "slug": "ch3-2",
                "folder": "CH3-2-排泄系統",
                "title": "排泄系統",
                "desc": "剖析腎臟皮質與髓質構造，詳解絲球體過濾、近曲小管再吸收與遠曲小管分泌的尿液形成歷程。",
                "img": "img/s3-2.jpg"
            },
            {
                "code": "探討3-1",
                "slug": "lab3-1",
                "folder": "探討活動3-1-腎臟的觀察",
                "title": "腎臟的觀察",
                "desc": "解剖豬腎觀察皮質、髓質、腎盂構造，並以顯微玻片辨識腎元構造之細胞型態特徵。",
                "img": "img/a3-1.jpg"
            }
        ]
    },
    {
        "id": 4,
        "title": "感應（神經、受器、肌肉與內分泌）",
        "desc": "從動作電位產生與突觸傳遞、各類感覺受器感知，到肌肉滑動學說及下視丘-腦下腺軸線的荷爾蒙調控，完整理解體內精準訊息網絡。",
        "icon": "⚡",
        "cover": "img/cover4.jpg",
        "units": [
            {
                "code": "CH4-1",
                "slug": "ch4-1",
                "folder": "CH4-1-神經系統",
                "title": "神經系統",
                "desc": "解析神經元靜止膜電位、動作電位全有全無律、神經傳導物質釋放與大腦脊髓中樞反射。",
                "img": "img/s4-1.jpg"
            },
            {
                "code": "CH4-2",
                "slug": "ch4-2",
                "folder": "CH4-2-體內的受器",
                "title": "體內的受器",
                "desc": "探討視覺視網膜光受器、聽覺耳蝸毛細胞、平衡覺前庭及化學受器（味覺嗅覺）之訊息轉換。",
                "img": "img/s4-2.jpg"
            },
            {
                "code": "CH4-3",
                "slug": "ch4-3",
                "folder": "CH4-3-肌肉與骨骼",
                "title": "肌肉與骨骼",
                "desc": "解析骨骼肌肌節構造、肌動蛋白與肌原纖維滑動學說、鈣離子調控機制及關節運動槓桿。",
                "img": "img/s4-3.jpg"
            },
            {
                "code": "CH4-4",
                "slug": "ch4-4",
                "folder": "CH4-4-內分泌系統",
                "title": "內分泌系統",
                "desc": "系統整合下視丘、腦垂腺、甲狀腺、腎上腺、胰臟胰島與生殖腺之荷爾蒙反饋調控網絡。",
                "img": "img/s4-4.jpg"
            },
            {
                "code": "探討4-1",
                "slug": "lab4-1",
                "folder": "探討活動4-1-肌肉與骨骼的運作",
                "title": "肌肉與骨骼的運作",
                "desc": "實作解剖或模型觀察骨骼肌肉關節槓桿運動，探討拮抗肌肌群協同收縮原理。",
                "img": "img/a4-1.jpg"
            }
        ]
    },
    {
        "id": 5,
        "title": "防禦（免疫系統）",
        "desc": "建立人體三道防線知識體系，從皮膜物理化學屏障、發炎反應，到 B 細胞抗體免疫與 T 細胞細胞介導免疫之特異性防禦機制。",
        "icon": "🛡️",
        "cover": "img/cover5.jpg",
        "units": [
            {
                "code": "CH5-1",
                "slug": "ch5-1",
                "folder": "CH5-1-免疫系統",
                "title": "免疫系統",
                "desc": "認識淋巴器官（骨髓、胸腺、脾臟、淋巴結）與各類白血球細胞的生成分化與免疫監視網絡。",
                "img": "img/s5-1.jpg"
            },
            {
                "code": "CH5-2",
                "slug": "ch5-2",
                "folder": "CH5-2-先天性免疫",
                "title": "先天性免疫",
                "desc": "剖析皮膜屏障、吞噬細胞吞噬作用、自然殺手細胞、補體系統活化與發炎反應紅腫熱痛機制。",
                "img": "img/s5-2.jpg"
            },
            {
                "code": "CH5-3",
                "slug": "ch5-3",
                "folder": "CH5-3-後天性免疫",
                "title": "後天性免疫",
                "desc": "深入抗原呈現細胞 (APC)、輔助 T 細胞、胞毒 T 細胞、B 細胞漿細胞抗體分泌及免疫記憶機制。",
                "img": "img/s5-3.jpg"
            },
            {
                "code": "CH5-4",
                "slug": "ch5-4",
                "folder": "CH5-4-免疫失調與排斥",
                "title": "免疫失調與排斥",
                "desc": "探討過敏反應 (IgE)、自體免疫疾病、後天免疫缺乏症候群 (HIV/AIDS) 及器官移植排斥。",
                "img": "img/s5-4.jpg"
            },
            {
                "code": "探討5-1",
                "slug": "lab5-1",
                "folder": "探討活動5-1-藉由ABO血型的鑑定探討抗原與抗體反應的基本模式",
                "title": "藉由ABO血型的鑑定探討抗原與抗體反應的基本模式",
                "desc": "運用抗 A / 抗 B 標準血清模擬鑑定紅血球表面凝集原與血清凝集素之特異性抗原抗體結合反應。",
                "img": "img/a5-1.jpg"
            }
        ]
    },
    {
        "id": 6,
        "title": "生殖與胚胎發育",
        "desc": "涵蓋男女生殖系統解剖、減數分裂精卵生成、月經與卵巢週期、受精卵裂，以及胚胎三胚層分化與母胎胎盤物質交換歷程。",
        "icon": "🌱",
        "cover": "img/cover6.jpg",
        "units": [
            {
                "code": "CH6-1",
                "slug": "ch6-1",
                "folder": "CH6-1-生殖系統",
                "title": "生殖系統",
                "desc": "剖析男性睪丸、副睪、輸精管及女性卵巢、輸卵管、子宮等內外生殖器官構造與生理功能。",
                "img": "img/s6-1.jpg"
            },
            {
                "code": "CH6-2",
                "slug": "ch6-2",
                "folder": "CH6-2-配子的形成",
                "title": "配子的形成",
                "desc": "精卵生成減數分裂歷程對比，解析 FSH、LH、動情素及黃體素調控之卵巢週期與子宮內膜週期。",
                "img": "img/s6-2.jpg"
            },
            {
                "code": "CH6-3",
                "slug": "ch6-3",
                "folder": "CH6-3-受精過程",
                "title": "受精過程",
                "desc": "探索精子獲能、頂體反應、透明帶穿透、皮質顆粒反應阻斷多精入卵及核融合過程。",
                "img": "img/s6-3.jpg"
            },
            {
                "code": "CH6-4",
                "slug": "ch6-4",
                "folder": "CH6-4-胚胎發育與懷孕",
                "title": "胚胎發育與懷孕",
                "desc": "解析卵裂、桑椹胚、囊胚著床、羊膜胚盤三胚層分化、胎盤臍帶形成及分娩泌乳調控歷程。",
                "img": "img/s6-4.jpg"
            },
            {
                "code": "探討6-1",
                "slug": "lab6-1",
                "folder": "探討活動6-1-生殖腺與生殖細胞的觀察",
                "title": "生殖腺與生殖細胞的觀察",
                "desc": "以高倍顯微鏡觀察睪丸曲細精管切片及卵巢濾泡切片，精準辨識各發育階段配子形態。",
                "img": "img/a6-1.jpg"
            },
            {
                "code": "探討6-2",
                "slug": "lab6-2",
                "folder": "探討活動6-2-代理孕母的倫理與法律問題",
                "title": "代理孕母的倫理與法律問題",
                "desc": "跨領域探討生殖醫學輔助生殖科技（ART）應用、代孕倫理思辨與現行法規權益爭議。",
                "img": "img/a6-2.jpg"
            },
            {
                "code": "探討6-3",
                "slug": "lab6-3",
                "folder": "探討活動6-3-蛙外部形態及內部構造的觀察",
                "title": "蛙外部形態及內部構造的觀察",
                "desc": "藉由經典兩生類青蛙解剖，全面觀察消化、呼吸、循環、泌尿與生殖系統之比較解剖構造。",
                "img": "img/a6-3.jpg"
            }
        ]
    }
]

# 1. 複製各單元置換好雲端影片的最新 HTML 至 clean slug 目錄
print("=== 正在複製單元網頁至 Clean Slug 目錄 ===")
for ch in chapters:
    for u in ch["units"]:
        slug = u["slug"]
        folder = u["folder"]
        src_web_dir = os.path.join(base_dir, folder, "教學網頁")
        
        # 尋找目標檔案
        if folder == "CH4-3-肌肉與骨骼":
            src_file = os.path.join(src_web_dir, "骨骼肌肉動力所.html")
        else:
            cand = [f for f in os.listdir(src_web_dir) if "質感新版" in f]
            if cand:
                src_file = os.path.join(src_web_dir, cand[0])
            else:
                src_file = os.path.join(src_web_dir, "index.html")
                
        dest_dir = os.path.join(site_dir, slug)
        os.makedirs(dest_dir, exist_ok=True)
        dest_file = os.path.join(dest_dir, "index.html")
        shutil.copy2(src_file, dest_file)
        print(f"[Copied] {folder} -> {slug}/index.html")

# 2. 生成首頁 index.html
print("=== 正在生成選修生物3全冊首頁 index.html ===")
index_html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>翰林版 高中選修生物（Ⅲ）互動教學網站</title>
  <meta name="description" content="翰林版高中選修生物（Ⅲ）動物體的構造與功能全套互動教材網站。涵蓋動物組織恆定、循環消化、呼吸排泄、神經受器與肌肉、免疫防禦及生殖發育。內建 Google Drive 教學影片與高清課本圖解。">
  <link rel="icon" href="img/hanlin-logo.png">
  <link rel="stylesheet" href="style.css">
  <script defer src="app.js"></script>
</head>
<body>

  <!-- 頂部導覽列 -->
  <header class="site-header">
    <div class="nav-container">
      <a href="index.html" class="nav-brand">
        <img src="img/hanlin-logo-wide.png" alt="翰林出版" class="brand-logo">
        <div class="brand-divider"></div>
        <div class="brand-title">
          <span class="series-name">108課綱 高中生物</span>
          <span class="page-name">選修生物（Ⅲ）教材網站</span>
        </div>
      </a>
      <nav>
        <ul class="nav-links">
          <li><a href="index.html" class="nav-link active">全冊總覽</a></li>
          <li><a href="chapter1.html" class="nav-link">第1章</a></li>
          <li><a href="chapter2.html" class="nav-link">第2章</a></li>
          <li><a href="chapter3.html" class="nav-link">第3章</a></li>
          <li><a href="chapter4.html" class="nav-link">第4章</a></li>
          <li><a href="chapter5.html" class="nav-link">第5章</a></li>
          <li><a href="chapter6.html" class="nav-link">第6章</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <!-- 橫幅 Hero 區塊 -->
  <section class="hero">
    <div class="hero-inner">
      <div class="hero-content">
        <div class="badge">
          <span>🧬</span> 108課綱 · 動物體的構造與功能 · 全單元精準解析
        </div>
        <h1>選修生物（Ⅲ）<br>生命生理機制與動態恆定</h1>
        <p>
          從微觀細胞組織的分工協同、神經與內分泌的毫秒訊號調節，到各大器官系統的精密運作與免疫衛戍防禦。本站完整整合全冊 6 大章節、18 個核心主題與 8 大探討活動，內建 Google 雲端高畫質教學影片與互動實作練習！
        </p>
        <div class="hero-stats">
          <div class="stat-item">
            <div class="stat-number">6</div>
            <div class="stat-label">全冊章節</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">18</div>
            <div class="stat-label">核心小節</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">8</div>
            <div class="stat-label">探討活動</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">26</div>
            <div class="stat-label">雲端教學影片</div>
          </div>
        </div>
      </div>
      <div class="hero-visual">
        <div class="hero-cover-stack">
          <img src="img/cover1.jpg" alt="選修生物(Ⅲ)課本封面" class="hero-cover-img" data-lightbox>
        </div>
      </div>
    </div>
  </section>

  <!-- 主要內容區：章節總覽卡片 Grid -->
  <main class="main-container">
    <div class="chapter-nav-grid">
"""

for ch in chapters:
    cid = ch["id"]
    ctitle = ch["title"]
    cdesc = ch["desc"]
    cicon = ch["icon"]
    
    units_html = ""
    for u in ch["units"]:
        code = u["code"]
        slug = u["slug"]
        utitle = u["title"]
        units_html += f"""
          <a href="{slug}/" class="unit-item" title="{utitle}">
            <div class="unit-info">
              <span class="unit-code">{code}</span>
              <span class="unit-name">{utitle}</span>
            </div>
            <div class="unit-action">
              進入 <span>&rarr;</span>
            </div>
          </a>
        """
        
    index_html += f"""
      <div class="chapter-card">
        <div class="chapter-card-header">
          <div class="chapter-badge-wrap">
            <span class="chapter-number">CHAPTER 0{cid}</span>
            <h2 class="chapter-title">{ctitle}</h2>
          </div>
          <div class="chapter-icon">{cicon}</div>
        </div>
        <div class="chapter-card-body">
          <p class="chapter-desc">{cdesc}</p>
          <div class="unit-list">
            {units_html}
          </div>
        </div>
        <div class="chapter-card-footer">
          <span style="font-size:13px;color:var(--text-muted)">共 {len(ch["units"])} 個學習單元</span>
          <a href="chapter{cid}.html" class="btn-chapter-detail">
            瀏覽章節圖解與詳情 <span>&rarr;</span>
          </a>
        </div>
      </div>
    """

index_html += """
    </div>
  </main>

  <!-- 頁尾 Footer -->
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <img src="img/hanlin-logo-wide.png" alt="翰林出版" class="footer-logo">
      </div>
      <p class="footer-desc">
        本教材網站依據 108 課綱技術與學科規範建置，整合高質感微型圖解探索、即時檢核題庫、逐步課堂簡報與 Google Drive 串流教學影片，提供師生無縫線上教學體驗。
      </p>
      <div class="footer-copyright">
        &copy; 翰林出版事業股份有限公司 · 選修生物（Ⅲ）互動教學網站
      </div>
    </div>
  </footer>

</body>
</html>
"""

with open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print("[Done] index.html generated.")

# 3. 生成各章節專屬頁面 chapter1.html ~ chapter6.html
for ch in chapters:
    cid = ch["id"]
    ctitle = ch["title"]
    cdesc = ch["desc"]
    cicon = ch["icon"]
    
    units_cards_html = ""
    for u in ch["units"]:
        code = u["code"]
        slug = u["slug"]
        utitle = u["title"]
        udesc = u["desc"]
        uimg = u["img"]
        vinfo = video_map.get(code, {})
        v_view = vinfo.get("view_url", "")
        
        btn_view_html = f'<a href="{v_view}" target="_blank" rel="noopener noreferrer" class="btn-secondary" title="在 Google 雲端硬碟開啟觀看">雲端影片 ↗</a>' if v_view else ''
        
        units_cards_html += f"""
          <div class="unit-detail-card">
            <div class="unit-thumb-wrap">
              <img src="{uimg}" alt="{utitle} 核心圖解" class="unit-thumb-img" data-lightbox>
              <div class="unit-badge-tag">{code}</div>
            </div>
            <div class="unit-detail-body">
              <h3 class="unit-detail-title">{utitle}</h3>
              <p class="unit-detail-desc">{udesc}</p>
              <div class="unit-detail-links">
                <a href="{slug}/" class="btn-primary">進入互動學習 &rarr;</a>
                {btn_view_html}
              </div>
            </div>
          </div>
        """
        
    nav_links_html = ""
    for other_ch in chapters:
        active_cls = 'active' if other_ch["id"] == cid else ''
        nav_links_html += f'<li><a href="chapter{other_ch["id"]}.html" class="nav-link {active_cls}">第{other_ch["id"]}章</a></li>\n'

    ch_html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>第 {cid} 章 {ctitle}｜選修生物（Ⅲ）教材網站</title>
  <meta name="description" content="翰林版選修生物（Ⅲ）第 {cid} 章 {ctitle}。完整單元圖解導覽、互動實作練習與 Google Drive 串流教學影片。">
  <link rel="icon" href="img/hanlin-logo.png">
  <link rel="stylesheet" href="style.css">
  <script defer src="app.js"></script>
</head>
<body>

  <!-- 頂部導覽列 -->
  <header class="site-header">
    <div class="nav-container">
      <a href="index.html" class="nav-brand">
        <img src="img/hanlin-logo-wide.png" alt="翰林出版" class="brand-logo">
        <div class="brand-divider"></div>
        <div class="brand-title">
          <span class="series-name">108課綱 高中生物</span>
          <span class="page-name">選修生物（Ⅲ）教材網站</span>
        </div>
      </a>
      <nav>
        <ul class="nav-links">
          <li><a href="index.html" class="nav-link">全冊總覽</a></li>
          {nav_links_html}
        </ul>
      </nav>
    </div>
  </header>

  <!-- 章節 Hero 橫幅 -->
  <section class="chapter-hero">
    <div class="chapter-hero-inner">
      <div class="breadcrumb">
        <a href="index.html">選修生物（Ⅲ）全冊</a>
        <span>&rsaquo;</span>
        <span>第 {cid} 章 {ctitle}</span>
      </div>
      <h1>第 {cid} 章 {ctitle} {cicon}</h1>
      <p>{cdesc}</p>
    </div>
  </section>

  <!-- 單元列表 Grid -->
  <main class="main-container">
    <div class="units-detail-grid">
      {units_cards_html}
    </div>
  </main>

  <!-- 頁尾 Footer -->
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <img src="img/hanlin-logo-wide.png" alt="翰林出版" class="footer-logo">
      </div>
      <p class="footer-desc">
        本教材網站依據 108 課綱技術與學科規範建置，整合高質感微型圖解探索、即時檢核題庫、逐步課堂簡報與 Google Drive 串流教學影片。
      </p>
      <div class="footer-copyright">
        &copy; 翰林出版事業股份有限公司 · 選修生物（Ⅲ）互動教學網站
      </div>
    </div>
  </footer>

</body>
</html>
"""
    ch_path = os.path.join(site_dir, f"chapter{cid}.html")
    with open(ch_path, "w", encoding="utf-8") as f:
        f.write(ch_html)
    print(f"[Done] chapter{cid}.html generated.")

# 4. 生成根目錄 index.html (自動導向到 選修生物3教材網站/)
root_index_html = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>翰林版 選修生物（Ⅲ）互動教學網站</title>
<meta http-equiv="refresh" content="0; url=選修生物3教材網站/">
<link rel="icon" href="選修生物3教材網站/img/hanlin-logo.png">
<script>
  window.location.replace("選修生物3教材網站/");
</script>
<style>
  body {
    margin: 0;
    padding: 60px 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Noto Sans TC", "Segoe UI", Roboto, sans-serif;
    background: #faf7f5;
    color: #1c1917;
    text-align: center;
  }
  .box {
    max-width: 520px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 16px;
    padding: 40px 32px;
    box-shadow: 0 10px 30px rgba(158,28,63,0.08);
    border: 1px solid #f0e6e0;
  }
  h1 { font-size: 22px; color: #9e1c3f; margin-bottom: 12px; }
  p { font-size: 15px; color: #57534e; margin-bottom: 24px; line-height: 1.6; }
  a {
    display: inline-block;
    padding: 12px 28px;
    background: linear-gradient(135deg, #881337, #be123c);
    color: #ffffff;
    text-decoration: none;
    font-weight: 700;
    border-radius: 8px;
  }
</style>
</head>
<body>
<div class="box">
  <h1>翰林版 選修生物（Ⅲ）互動教學網站</h1>
  <p>正在為您導向至全冊互動教材網站首頁，若瀏覽器未自動跳轉，請點擊下方按鈕前往。</p>
  <a href="選修生物3教材網站/">進入選修生物（Ⅲ）教材首頁 &rarr;</a>
</div>
</body>
</html>
"""

with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(root_index_html)
print("[Done] root index.html generated.")

# 5. 生成 .nojekyll
with open(os.path.join(base_dir, ".nojekyll"), "w", encoding="utf-8") as f:
    f.write("")
print("[Done] .nojekyll created.")

# 6. 生成選修生物3網頁發布總表.md
pub_md_lines = [
    "# 翰林版 選修生物（Ⅲ）線上發布總表",
    "",
    "> 發布時間：2026-10-11  ",
    "> 線上網站：https://froglssh.github.io/hanlin-elective-biology-3-web/  ",
    "> GitHub 儲存庫：https://github.com/froglssh/hanlin-elective-biology-3-web  ",
    "",
    "## 一、教材入口與各章節瀏覽導覽頁",
    "",
    "| 頁面 | 描述 | 線上網址 (GitHub Pages) |",
    "| :--- | :--- | :--- |",
    "| **全冊首頁（根目錄跳轉）** | 自動導向教材網站入口 | https://froglssh.github.io/hanlin-elective-biology-3-web/ |",
    "| **選修生物（Ⅲ）全冊首頁** | 完整 6 章 26 單元首頁入口 | https://froglssh.github.io/hanlin-elective-biology-3-web/選修生物3教材網站/ |",
    "| **第 1 章 動物體的組成與恆定性** | 動物組織與負回饋恆定機制 | https://froglssh.github.io/hanlin-elective-biology-3-web/選修生物3教材網站/chapter1.html |",
    "| **第 2 章 循環與消化** | 心臟血管動力與消化酵素水解 | https://froglssh.github.io/hanlin-elective-biology-3-web/選修生物3教材網站/chapter2.html |",
    "| **第 3 章 呼吸與排泄** | 氣體交換運輸與腎元尿液形成 | https://froglssh.github.io/hanlin-elective-biology-3-web/選修生物3教材網站/chapter3.html |",
    "| **第 4 章 感應（神經、受器、肌骨、內分泌）** | 動作電位、受器、肌肉滑動與荷爾蒙 | https://froglssh.github.io/hanlin-elective-biology-3-web/選修生物3教材網站/chapter4.html |",
    "| **第 5 章 防禦（免疫系統）** | 先天性防線、後天性特異免疫與失調 | https://froglssh.github.io/hanlin-elective-biology-3-web/選修生物3教材網站/chapter5.html |",
    "| **第 6 章 生殖與發育** | 配子形成、受精卵裂、胚層分化與母胎 | https://froglssh.github.io/hanlin-elective-biology-3-web/選修生物3教材網站/chapter6.html |",
    "",
    "## 二、全冊 26 個學習單元 Clean URL 線上連結總表",
    "",
    "| 單元編號 | 單元名稱 | 章節 | Clean URL (GitHub Pages) | Google 雲端教學影片 |",
    "| :--- | :--- | :---: | :--- | :--- |"
]

for ch in chapters:
    cid = ch["id"]
    for u in ch["units"]:
        code = u["code"]
        title = u["title"]
        slug = u["slug"]
        vinfo = video_map.get(code, {})
        vview = vinfo.get("view_url", "")
        pub_md_lines.append(f"| **{code}** | {title} | 第 {cid} 章 | [進入學習](https://froglssh.github.io/hanlin-elective-biology-3-web/選修生物3教材網站/{slug}/) | [觀看影片]({vview}) |")

pub_md_path = os.path.join(base_dir, "選修生物3網頁發布總表.md")
with open(pub_md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(pub_md_lines))
# 也放一份在 選修生物3教材網站/
shutil.copy2(pub_md_path, os.path.join(site_dir, "選修生物3網頁發布總表.md"))
print("[Done] 選修生物3網頁發布總表.md generated.")
print("\nAll build steps finished successfully!")
