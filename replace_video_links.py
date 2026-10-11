import os, re, json

base_dir = "/Users/froglssh/Library/CloudStorage/GoogleDrive-frog@lssh.tp.edu.tw/我的雲端硬碟/04教科書/0自編教材/翰林/PPT動畫/選修生物3"
md_path = os.path.join(base_dir, "選修生物3教學影片雲端硬碟網址總表.md")

with open(md_path, "r", encoding="utf-8") as f:
    t = f.read()
json_str = t.split("```json\n")[1].split("\n```")[0]
data = json.loads(json_str)

units_by_folder = {item["folder_name"]: item for item in data}

# 1. 處理 25 個含有 質感新版 的單元
modified_count = 0

for folder, item in units_by_folder.items():
    if folder == "CH4-3-肌肉與骨骼":
        continue
    w = os.path.join(base_dir, folder, "教學網頁")
    htmls = [f for f in os.listdir(w) if "質感新版" in f]
    if not htmls:
        continue
    
    target_path = os.path.join(w, htmls[0])
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    file_id = item["file_id"]
    preview_url = item["preview_url"]
    view_url = item["view_url"]
    
    # 替換 video frame
    # 原始: <div class="video-frame"><video id="teaching-video" controls playsinline preload="none" aria-label="...教學影片"></video></div>
    content = re.sub(
        r'<div class="video-frame"><video[^>]*id="teaching-video"[^>]*></video></div>',
        f'<div class="video-frame" style="position:relative;width:100%;padding-top:56.25%;background:#000;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.15)">'
        f'<iframe id="teaching-video" src="" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>'
        f'</div>',
        content
    )
    
    # 替換外部按鈕描述
    # 原始: <p>本節教學影片。若播放器無法播放，可開啟影片檔案。</p><a class="btn ghost" id="video-external" target="_blank" rel="noopener noreferrer">開啟影片檔案 ↗</a>
    content = re.sub(
        r'<p>本節教學影片。若播放器無法播放，可開啟影片檔案。</p>\s*<a class="btn ghost" id="video-external" target="_blank" rel="noopener noreferrer">開啟影片檔案 ↗</a>',
        f'<div style="margin-top:12px;text-align:right">'
        f'<a class="btn ghost" id="video-external" target="_blank" rel="noopener noreferrer" style="display:inline-flex;align-items:center;gap:6px">在 Google 雲端硬碟中開啟觀看 ↗</a>'
        f'</div>',
        content
    )
    
    # 替換 VIDEO_SRC 定義
    content = re.sub(
        r"const VIDEO_SRC='../教學影片/'\+encodeURIComponent\([^\)]+\);",
        f"const VIDEO_SRC='{preview_url}';\nconst VIDEO_VIEW_URL='{view_url}';",
        content
    )
    
    # 替換 navigateAfter 中的清理邏輯
    old_cleanup = "el('teaching-video').pause();el('teaching-video').removeAttribute('src');el('teaching-video').load();"
    new_cleanup = "const tv=el('teaching-video');if(tv){if(typeof tv.pause==='function')tv.pause();if(tv.tagName==='IFRAME')tv.src='about:blank';else{tv.removeAttribute('src');if(typeof tv.load==='function')tv.load();}}"
    content = content.replace(old_cleanup, new_cleanup)
    
    # 替換 video-external.href
    old_href = "el('video-external').href=VIDEO_SRC;"
    new_href = "el('video-external').href=typeof VIDEO_VIEW_URL!=='undefined'?VIDEO_VIEW_URL:VIDEO_SRC;"
    content = content.replace(old_href, new_href)
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    modified_count += 1
    print(f"[OK] Modified 質感新版: {folder}/{htmls[0]}")

# 2. 處理 CH4-3-肌肉與骨骼
ch43_item = units_by_folder["CH4-3-肌肉與骨骼"]
ch43_w = os.path.join(base_dir, "CH4-3-肌肉與骨骼", "教學網頁")
ch43_files = ["骨骼肌肉動力所.html", "index.html"]

for fname in ch43_files:
    fpath = os.path.join(ch43_w, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    file_id = ch43_item["file_id"]
    preview_url = ch43_item["preview_url"]
    view_url = ch43_item["view_url"]
    
    # 替換 video-player
    content = content.replace(
        '<div class="video-player"><video id="teaching-video" controls preload="none" playsinline></video><div class="video-msg hidden" id="video-msg"></div></div>',
        f'<div class="video-player" style="position:relative;width:100%;padding-top:56.25%;background:#000;border-radius:12px;overflow:hidden"><iframe id="teaching-video" src="" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe><div class="video-msg hidden" id="video-msg"></div></div>'
    )
    
    # 替換 VIDEO_SRC 與 VIDEO_URL
    content = re.sub(
        r"const VIDEO_SRC='../教學影片/[^']+';",
        f"const VIDEO_SRC='{preview_url}';",
        content
    )
    content = re.sub(
        r"const VIDEO_URL='';",
        f"const VIDEO_URL='{view_url}';",
        content
    )
    
    # 替換 startVideo / stopVideo
    old_start = "function startVideo(){const v=$('#teaching-video'),m=$('#video-msg');m.classList.add('hidden');v.src=VIDEO_SRC;v.load();\n v.onerror=()=>{m.innerHTML='找不到影片檔。<br>請從課程資料夾開啟本網頁，並確認「教學影片」資料夾內有<br>《CH4-3_肌肉與骨骼_教學影片.mp4》。';m.classList.remove('hidden')};\n $('#video-link').innerHTML=VIDEO_URL?`<a href=\"${VIDEO_URL}\" target=\"_blank\" rel=\"noopener\">另開影片 ↗</a>`:''}"
    new_start = "function startVideo(){const v=$('#teaching-video'),m=$('#video-msg');m.classList.add('hidden');v.src=VIDEO_SRC;\n $('#video-link').innerHTML=VIDEO_URL?`<a href=\"${VIDEO_URL}\" target=\"_blank\" rel=\"noopener\" class=\"btn\" style=\"display:inline-flex;align-items:center;gap:6px\">在 Google 雲端硬碟中開啟觀看 ↗</a>`:''}"
    content = content.replace(old_start, new_start)
    
    old_stop = "function stopVideo(){const v=$('#teaching-video');try{v.pause()}catch(e){}v.removeAttribute('src');v.load()}"
    new_stop = "function stopVideo(){const v=$('#teaching-video');if(v){if(v.tagName==='IFRAME')v.src='about:blank';else{try{v.pause()}catch(e){}v.removeAttribute('src');try{v.load()}catch(e){}}}}"
    content = content.replace(old_stop, new_stop)
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
        
    modified_count += 1
    print(f"[OK] Modified CH4-3: {fname}")

print(f"\nAll updates complete! Total files modified: {modified_count}")
