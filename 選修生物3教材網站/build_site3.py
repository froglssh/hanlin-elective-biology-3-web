# -*- coding: utf-8 -*-
"""選修生物（Ⅲ）教材入口網站產生器：內容依翰林版《選修生物Ⅲ（全）》課本改寫。
修改網址、簡介或重點時，改本檔的 CHAPTERS 資料後重新執行即可。"""
import html, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'site'
BASE = ''  # 各單元網頁在本資料夾內（ch1-1/ … lab6-3/），用相對路徑
DRIVE = 'https://drive.google.com/file/d/{}/view'

ICON_OUT = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_GO = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_ZOOM = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="m16 16 4.5 4.5M8.5 11h5M11 8.5v5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
ICON_PLAY = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 8.5v7l6-3.5z" fill="currentColor"/></svg>'
ICON_BOOK = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5C6.5 4.5 9.5 4.5 12 6c2.5-1.5 5.5-1.5 8-.5v13c-2.5-1-5.5-1-8 .5-2.5-1.5-5.5-1.5-8-.5z M12 6v13.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'

E = html.escape

from chapters3 import CHAPTERS

TOTAL_UNITS = sum(len(c['units']) for c in CHAPTERS)
TOTAL_LABS = sum(len(c['labs']) for c in CHAPTERS)

def url(u): return u['slug'] + '/'
def vurl(u): return DRIVE.format(u['vid'])

HEAD = '''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="{theme}">
<link rel="icon" href="img/hanlin-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
'''

FOOT = '''<footer class="foot">
  <div class="foot-in">
    <img src="img/hanlin-logo.png" alt="" width="34" height="34">
    <p>內容整理自翰林版高中《選修生物Ⅲ（全）》課本，簡介依課文重點改寫，圖片取自課本，僅供課堂教學使用。<br>各節互動教學網頁由臺北市立麗山高中生物科自編製作，發布於 GitHub Pages；教學影片存放於 Google 雲端硬碟。</p>
  </div>
</footer>
<div class="lightbox" id="lightbox" hidden>
  <button class="lb-close" aria-label="關閉">×</button>
  <figure><img alt=""><figcaption></figcaption></figure>
</div>
<script src="app.js"></script>
</body>
</html>
'''

def chstyle(c): return f"--a:{c['a']};--a2:{c['a2']};--t:{c['t']}"

def build_index():
    o = [HEAD.format(title='翰林版 選修生物（Ⅲ）｜互動教學網站',
        desc=f'翰林版高中選修生物Ⅲ（全）六章 {TOTAL_UNITS} 節與 {TOTAL_LABS} 個探討活動的互動教學網頁與教學影片入口', theme='#9e1c3f')]
    o.append('''<body class="home">
<header class="hero">
  <svg class="globe" viewBox="0 0 600 600" aria-hidden="true">
    <g fill="none" stroke="currentColor" stroke-width="1.2">
      <path d="M0 330h150l30-60 40 150 50-260 45 220 30-50h255" stroke-width="3"/>
      <circle cx="300" cy="300" r="290" stroke-dasharray="10 8" opacity=".5"/>
    </g>
  </svg>
  <div class="hero-in">
    <img class="hero-logo" src="img/hanlin-logo-wide.png" alt="翰林出版 HAN LIN PUBLISHING" width="1240" height="324">
    <div class="hero-rule"><span></span><em>自然科學領域　加深加廣選修</em><span></span></div>
    <h1>選修生物（Ⅲ）<span>互動教學網站</span></h1>
    <p class="hero-sub">翰林版《選修生物Ⅲ（全）》· 從動物組織與恆定，到循環、消化、呼吸、排泄、感應、防禦與生殖，每一節都有專屬的互動闖關網頁與教學影片</p>
    <ul class="stats">
''' + f'''      <li><b>{len(CHAPTERS)}</b><span>章</span></li><li><b>{TOTAL_UNITS}</b><span>節正課</span></li><li><b>{TOTAL_LABS}</b><span>個探討活動</span></li><li><b>{TOTAL_UNITS+TOTAL_LABS}</b><span>個互動網頁</span></li>
    </ul>
  </div>
</header>
<main>
  <section class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">CHAPTERS</span><h2>選擇章節，開始探索</h2><p>點選章節封面進入章節，瀏覽每一節的課本概念圖、重點簡介與教學影片。</p></div>
    <div class="ch-grid">
''')
    for c in CHAPTERS:
        lis = ''.join(f"<li><span>{u['code']}</span>{E(u['title'])}</li>" for u in c['units'])
        meta = f"<span>{len(c['units'])} 節正課</span>" + (f"<span>{len(c['labs'])} 個探討活動</span>" if c['labs'] else '')
        o.append(f'''      <a class="ch-card reveal" href="chapter{c['n']}.html" style="{chstyle(c)}">
        <div class="ch-cover"><img src="img/cover{c['n']}.jpg" alt="第{c['n']}章 {c['title']} 章節封面" loading="lazy" width="1000" height="1328"></div>
        <div class="ch-body">
          <div class="ch-kicker">CHAPTER 0{c['n']} · {c['en']}</div>
          <h2>第 {c['n']} 章　{c['title']}</h2>
          <ul class="ch-list">{lis}</ul>
          <div class="ch-meta">{meta}</div>
          <span class="ch-go">進入本章 {ICON_GO}</span>
        </div>
      </a>
''')
    o.append('''    </div>
  </section>
  <section class="wrap quick-wrap">
    <div class="sec-head reveal"><span class="eyebrow">QUICK ACCESS</span><h2>全部互動網頁快速入口</h2><p>老師上課或學生複習時，可直接開啟各節的互動教學網頁（另開新分頁）；教學影片請由章節頁進入。</p></div>
    <div class="quick">''')
    for c in CHAPTERS:
        o.append(f'<div class="qcol reveal" style="--a:{c["a"]};--t:{c["t"]}"><h3><b>{c["n"]}</b>{c["title"]}</h3>')
        for u in c['units']:
            o.append(f'<a target="_blank" rel="noopener" href="{url(u)}" class="q"><span class="q-code">{u["code"]}</span><span class="q-t">{E(u["web"])}<small>{E(u["title"])}</small></span>{ICON_OUT}</a>')
        for l in c['labs']:
            o.append(f'<a target="_blank" rel="noopener" href="{url(l)}" class="q q-lab"><span class="q-code">{l["code"].replace(" ","")}</span><span class="q-t">{E(l["web"])}<small>{E(l["title"])}</small></span>{ICON_OUT}</a>')
        o.append('</div>')
    o.append('''</div>
  </section>
</main>
''' + FOOT)
    return ''.join(o)

def nav(cur):
    return ''.join(f'<a href="chapter{c["n"]}.html" class="nav-ch{" on" if c["n"]==cur else ""}" style="--a:{c["a"]}"><b>{c["n"]}</b><span>{c["title"]}</span></a>' for c in CHAPTERS)

def figure(key, cap, cls='fig-btn'):
    return f'''<button class="{cls}" data-full="img/{key}.jpg" data-cap="{E(cap)}" aria-label="放大圖片：{E(cap)}">
          <img src="img/{key}.jpg" alt="{E(cap)}" loading="lazy" decoding="async"><span class="zoom">{ICON_ZOOM}放大</span>
        </button>'''

def build_chapter(c):
    n = c['n']
    o = [HEAD.format(title=f"第 {n} 章 {c['title']}｜翰林版 選修生物（Ⅲ）", desc=E(c['lead']), theme=c['a'])]
    jumps = ''.join(f'<a href="#u{u["code"]}"><b>{u["code"]}</b>{E(u["title"])}</a>' for u in c['units'])
    if c['labs']: jumps += f'<a href="#labs" class="j-lab"><b>探討</b>活動 × {len(c["labs"])}</a>'
    o.append(f'''<body class="chapter" style="{chstyle(c)}">
<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="index.html" aria-label="回到首頁">
      <img src="img/hanlin-logo.png" alt="翰林出版" width="40" height="40">
      <span class="brand-t"><small>翰林版</small>選修生物（Ⅲ）</span>
    </a>
    <nav class="nav">{nav(n)}</nav>
  </div>
</header>
<header class="ch-hero">
  <div class="ch-hero-in">
    <div class="ch-hero-text">
      <div class="ch-kicker">CHAPTER 0{n} · {c['en']}</div>
      <h1><span class="big">{n}</span><span class="t">第 {n} 章<br><strong>{c['title']}</strong></span></h1>
      <p class="lead">{E(c['lead'])}</p>
      <div class="jump">{jumps}</div>
    </div>
    <div class="ch-hero-cover"><img src="img/cover{n}.jpg" alt="第 {n} 章 章節封面" width="1000" height="1328"></div>
  </div>
</header>
<main class="wrap units">
''')
    from PIL import Image
    for i, u in enumerate(c['units']):
        iw, ih = Image.open(os.path.join(OUT, 'img', u['fig'] + '.jpg')).size
        wide = iw / ih >= 2.2
        subs = ''.join(f'<li>{E(s)}</li>' for s in u['subs'])
        tags = ''.join(f'<span>{E(t)}</span>' for t in u['tags'])
        o.append(f'''    <article class="unit reveal{' wide' if wide else (' flip' if i % 2 else '')}" id="u{u['code']}">
      <figure class="fig">
        {figure(u['fig'], u['cap'])}
        <figcaption>{E(u['cap'])}</figcaption>
      </figure>
      <div class="unit-body">
        <div class="unit-top"><span class="code">{u['code']}</span><span class="web-pill">互動網頁｜{E(u['web'])}</span><span class="pg-pill">{ICON_BOOK}課本 {u['pages']}</span></div>
        <h2>{E(u['title'])}</h2>
        <a class="intro" href="{url(u)}" target="_blank" rel="noopener" title="開啟「{E(u['web'])}」教學網頁">
          <p>{E(u['intro'])}</p>
          <span class="intro-hint">點選文字即可開啟教學網頁 {ICON_OUT}</span>
        </a>
        <div class="subs"><h3>本節重點</h3><ol>{subs}</ol></div>
        <div class="tags">{tags}</div>
        <div class="btn-row">
          <a class="btn" href="{url(u)}" target="_blank" rel="noopener">進入「{E(u['web'])}」{ICON_OUT}</a>
          <a class="btn ghost vid" href="{vurl(u)}" target="_blank" rel="noopener">{ICON_PLAY}教學影片</a>
        </div>
      </div>
    </article>
''')
    if c['labs']:
        one = ' one' if len(c['labs']) == 1 else ''
        o.append(f'''  <section class="labs" id="labs">
    <div class="sec-head reveal"><span class="eyebrow">HANDS-ON LAB</span><h2>探討活動</h2><p>動手操作、記錄變因與數據，把課文中的概念轉化為自己的實驗證據。</p></div>
    <div class="lab-grid{one}">
''')
        for l in c['labs']:
            o.append(f'''      <article class="lab reveal" id="{l['slug']}">
        {figure(l['fig'], l['cap'], 'lab-fig fig-btn')}
        <div class="lab-body">
          <div class="unit-top"><span class="code sm">{l['code']}</span><span class="web-pill">{E(l['web'])}</span><span class="pg-pill">{ICON_BOOK}課本 {l['pages']}</span></div>
          <h3>{E(l['title'])}</h3>
          <a class="intro" href="{url(l)}" target="_blank" rel="noopener"><p>{E(l['intro'])}</p><span class="intro-hint">開啟教學網頁 {ICON_OUT}</span></a>
          <div class="btn-row">
            <a class="btn ghost" href="{url(l)}" target="_blank" rel="noopener">進入「{E(l['web'])}」{ICON_OUT}</a>
            <a class="btn ghost vid" href="{vurl(l)}" target="_blank" rel="noopener">{ICON_PLAY}教學影片</a>
          </div>
        </div>
      </article>
''')
        o.append('    </div>\n  </section>\n')
    prev = f'<a class="pg" href="chapter{n-1}.html"><small>PREVIOUS</small>← 第 {n-1} 章　{CHAPTERS[n-2]["title"]}</a>' if n > 1 else '<a class="pg" href="index.html"><small>HOME</small>← 回首頁總覽</a>'
    nxt = f'<a class="pg next" href="chapter{n+1}.html"><small>NEXT CHAPTER</small>第 {n+1} 章　{CHAPTERS[n]["title"]} →</a>' if n < len(CHAPTERS) else '<a class="pg next" href="index.html"><small>HOME</small>回首頁總覽 →</a>'
    o.append(f'  <nav class="pager">\n    {prev}\n    {nxt}\n  </nav>\n</main>\n' + FOOT)
    return ''.join(o)

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(build_index())
for c in CHAPTERS:
    open(os.path.join(OUT, f'chapter{c["n"]}.html'), 'w', encoding='utf-8').write(build_chapter(c))
print('ok', TOTAL_UNITS, TOTAL_LABS)
