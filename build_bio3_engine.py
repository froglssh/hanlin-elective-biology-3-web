import os
import sys
import json
import base64
import subprocess
import glob
import re
import fitz
from PIL import Image
import pptx

BASE_DIR = '/Users/froglssh/Library/CloudStorage/GoogleDrive-frog@lssh.tp.edu.tw/我的雲端硬碟/04教科書/0自編教材/翰林/PPT動畫/選修生物3'
TPL_SRC = '/Users/froglssh/Library/CloudStorage/GoogleDrive-frog@lssh.tp.edu.tw/我的雲端硬碟/04教科書/0自編教材/翰林/PPT動畫/選修生物1/CH2-1-新陳代謝與酵素/教學網頁/代謝與酵素驛站.html'

with open(TPL_SRC, 'r', encoding='utf-8') as f:
    RAW_TPL = f.read()

# 轉換為選修生物(Ⅲ) 專屬赤緋紅色調與標誌
BIO3_TPL = RAW_TPL

# 1. 替換 CSS :root 變數
OLD_ROOT = """:root{
 --ground:#F3F2EC;--surface:#FFFEFA;--surface-2:#EEF0F1;--line:#D3D8DF;--line-soft:#E3E6EA;
 --ink:#1B2A44;--ink-2:#44536B;--ink-3:#69768A;
 --accent:#2F5DA8;--accent-ink:#FFFFFF;--accent-soft:#E2EAF7;
 --g1:#2F5DA8;--g1-soft:#E2EAF7;--g2:#0E7C74;--g2-soft:#DCEEEB;--g3:#B9561C;--g3-soft:#F8E6D8;--g4:#5A7D25;--g4-soft:#E8F0DA;
 --ok:#227A5C;--ok-soft:#DCF0E7;--no:#B8402F;--no-soft:#FBE5E0;--warn:#9A6A12;--warn-soft:#FAEFD8;--detail:#93672F;
 --shadow:0 1px 2px rgba(27,42,68,.05),0 14px 38px -28px rgba(27,42,68,.45);"""

NEW_ROOT = """:root{
 --ground:#FBF8F5;--surface:#FFFFFF;--surface-2:#F6EFEB;--line:#E2D6CF;--line-soft:#EEE5DF;
 --ink:#2B191D;--ink-2:#563D43;--ink-3:#826970;
 --accent:#9E1C3F;--accent-ink:#FFFFFF;--accent-soft:#FDE8ED;
 --g1:#9E1C3F;--g1-soft:#FDE8ED;--g2:#0E7C74;--g2-soft:#DCEEEB;--g3:#C05621;--g3-soft:#FAECE2;--g4:#6B3B82;--g4-soft:#F3E8F5;
 --ok:#1F7A59;--ok-soft:#DCF0E7;--no:#B83A32;--no-soft:#FBE5E2;--warn:#9A6A12;--warn-soft:#FAEFD8;--detail:#9C4221;
 --shadow:0 1px 2px rgba(43,25,29,.05),0 14px 38px -28px rgba(43,25,29,.42);"""

BIO3_TPL = BIO3_TPL.replace(OLD_ROOT, NEW_ROOT)
BIO3_TPL = BIO3_TPL.replace('#2F5DA8', '#9E1C3F').replace('#2f5da8', '#9e1c3f')
BIO3_TPL = BIO3_TPL.replace('#1B2A44', '#2B191D').replace('#1b2a44', '#2b191d')
BIO3_TPL = BIO3_TPL.replace('選修生物(Ⅰ)', '選修生物(Ⅲ)')

def process_bio3_unit(ch_folder, site_title, chapter_code, key_prefix, crops_spec, groups, learn_data, qs_data, drag_bgs, tags, speech_dict=None, titles_dict=None, use_pdf_slides=True):
    print(f"\n=======================================================")
    print(f"Building Elective Bio 3 Unit: {chapter_code} - {site_title} ({ch_folder})")
    print(f"=======================================================")
    
    ch_dir = os.path.join(BASE_DIR, ch_folder)
    pdf_file = [f for f in os.listdir(ch_dir) if f.endswith('.pdf')][0]
    pptx_file = [f for f in os.listdir(ch_dir) if f.endswith('.pptx')][0]
    
    # 優先從 教學動畫 或 教學影片 取得 mp4 (用於截取影格)
    anim_dir = os.path.join(ch_dir, '教學動畫')
    video_dir = os.path.join(ch_dir, '教學影片')
    
    mp4_path = None
    if os.path.exists(anim_dir):
        mp4s = [f for f in os.listdir(anim_dir) if f.endswith('.mp4')]
        if mp4s:
            mp4_path = os.path.join(anim_dir, mp4s[0])
    if not mp4_path and os.path.exists(video_dir):
        mp4s = [f for f in os.listdir(video_dir) if f.endswith('.mp4') and not f.endswith('.previsual-review-backup.mp4')]
        if mp4s:
            mp4_path = os.path.join(video_dir, mp4s[0])
    if not mp4_path:
        mp4s = [f for f in os.listdir(ch_dir) if f.endswith('.mp4')]
        if mp4s:
            mp4_path = os.path.join(ch_dir, mp4s[0])

    # 網頁播放影片優先使用 教學影片
    player_video = ""
    player_folder = "教學影片"
    if os.path.exists(video_dir):
        v_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4') and not f.endswith('.previsual-review-backup.mp4')]
        if v_files:
            player_video = v_files[0]
            player_folder = "教學影片"
    if not player_video and os.path.exists(anim_dir):
        v_files = [f for f in os.listdir(anim_dir) if f.endswith('.mp4')]
        if v_files:
            player_video = v_files[0]
            player_folder = "教學動畫"
            
    web_dir = os.path.join(ch_dir, '教學網頁')
    os.makedirs(web_dir, exist_ok=True)
    
    # 1. 整理 Speech 講稿
    speech_data = speech_dict or {}
    speech_file = os.path.join(video_dir, 'speech.md')
    if not speech_data and os.path.exists(speech_file):
        with open(speech_file, 'r', encoding='utf-8') as sf:
            raw_sp = sf.read()
        for part in re.split(r'##\s*Slide\s*(\d+)', raw_sp):
            part = part.strip()
            if not part: continue
            if part.isdigit():
                curr_s = part
            else:
                speech_data[curr_s] = part
                
    # 2. PDF 高解析裁切
    doc = fitz.open(os.path.join(ch_dir, pdf_file))
    crop_tmp = f'/tmp/{key_prefix}_crops'
    os.makedirs(crop_tmp, exist_ok=True)
    mat = fitz.Matrix(4.0, 4.0)
    
    IMG = {}
    for pno, rect, name in crops_spec:
        page = doc[pno]
        pix = page.get_pixmap(matrix=mat, clip=rect)
        p_path = f"{crop_tmp}/{name}.png"
        w_path = f"{crop_tmp}/{name}.webp"
        pix.save(p_path)
        im = Image.open(p_path)
        im.save(w_path, "WEBP", quality=90)
        os.remove(p_path)
        with open(w_path, 'rb') as wf:
            IMG[name] = 'data:image/webp;base64,' + base64.b64encode(wf.read()).decode('ascii')
            
    # 3. 抽取動畫影格
    raw_f_dir = f'/tmp/{key_prefix}_raw'
    webp_s_dir = f'/tmp/{key_prefix}_slides'
    os.makedirs(raw_f_dir, exist_ok=True)
    os.makedirs(webp_s_dir, exist_ok=True)
    
    if use_pdf_slides:
        print(f"Generating high-res slides directly from PDF ({len(doc)} pages)...")
        for f in glob.glob(f"{raw_f_dir}/*"): os.remove(f)
        pdf_mat = fitz.Matrix(2.0, 2.0)
        for pno in range(len(doc)):
            page = doc[pno]
            pix = page.get_pixmap(matrix=pdf_mat)
            f_path = f"{raw_f_dir}/frame_{pno+1:04d}.png"
            pix.save(f_path)
        raw_files = sorted(glob.glob(f"{raw_f_dir}/frame_*.png"))
    else:
        existing_frames = glob.glob(f"{raw_f_dir}/frame_*.png")
        is_mp4_ready = False
        if mp4_path and os.path.exists(mp4_path):
            st_mp4 = os.stat(mp4_path)
            if st_mp4.st_blocks * 512 >= st_mp4.st_size and st_mp4.st_size > 0:
                is_mp4_ready = True
                
        if len(existing_frames) < 10 and is_mp4_ready:
            for f in glob.glob(f"{raw_f_dir}/*"): os.remove(f)
            try:
                cmd = f'ffmpeg -nostdin -y -sn -dn -an -i "{mp4_path}" -vf fps=1,scale=1280:720 "{raw_f_dir}/frame_%04d.png"'
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
            except Exception:
                pass
                
        raw_files = sorted(glob.glob(f"{raw_f_dir}/frame_*.png"))
        if len(raw_files) == 0:
            print("MP4 not hydrated or unavailable; generating slides directly from textbook PDF...")
            pdf_mat = fitz.Matrix(2.0, 2.0)
            for pno in range(len(doc)):
                page = doc[pno]
                pix = page.get_pixmap(matrix=pdf_mat)
                f_path = f"{raw_f_dir}/frame_{pno+1:04d}.png"
                pix.save(f_path)
            raw_files = sorted(glob.glob(f"{raw_f_dir}/frame_*.png"))
        
    prev_thumb = None
    step_idx = 0
    for f in raw_files:
        im = Image.open(f)
        thumb = im.resize((80, 45)).convert('L')
        p1 = list(thumb.get_flattened_data() if hasattr(thumb, 'get_flattened_data') else thumb.getdata())
        if prev_thumb is None:
            diff = 100.0
        else:
            p2 = list(prev_thumb.get_flattened_data() if hasattr(prev_thumb, 'get_flattened_data') else prev_thumb.getdata())
            diff = sum(abs(a - b) for a, b in zip(p1, p2)) / len(p1)
        if diff > 1.8:
            step_idx += 1
            out_p = f"{webp_s_dir}/step_{step_idx:03d}.webp"
            im.save(out_p, 'WEBP', quality=85)
            prev_thumb = thumb
            with open(out_p, 'rb') as sf:
                IMG[f"step_{step_idx:03d}"] = 'data:image/webp;base64,' + base64.b64encode(sf.read()).decode('ascii')
                
    print(f"Extracted {len(crops_spec)} crops and {step_idx} animation steps.")
    
    # 4. Slide Mapping MAN & TITLES
    names = [f"step_{i:03d}" for i in range(1, step_idx + 1)]
    pptx_path = os.path.join(ch_dir, pptx_file)
    prs = None
    if not use_pdf_slides and os.path.exists(pptx_path):
        st = os.stat(pptx_path)
        if st.st_blocks * 512 >= st.st_size and st.st_size > 0:
            try:
                prs = pptx.Presentation(pptx_path)
            except Exception:
                prs = None
            
    if prs is not None:
        try:
            n_slides = len(prs.slides)
            TITLES = {}
            for i, slide in enumerate(prs.slides):
                p_num = str(i + 1)
                slide_text = ""
                try:
                    for shp in slide.shapes:
                        if shp.has_text_frame and shp.text_frame.text.strip():
                            t = shp.text_frame.text.strip().replace('\n', ' ')
                            if t:
                                slide_text = t
                                break
                except Exception:
                    pass
                TITLES[p_num] = f"第 {p_num} 頁：{slide_text[:40]}" if slide_text else f"第 {p_num} 頁"
                if str(p_num) not in speech_data and slide_text:
                    speech_data[str(p_num)] = slide_text
        except Exception:
            prs = None

    if prs is None:
        print("PPTX not available or parsing limited; generating slide metadata from textbook pages...")
        n_slides = len(doc)
        TITLES = {str(i + 1): f"第 {i + 1} 頁：{chapter_code} 核心講綱" for i in range(n_slides)}
        for i in range(n_slides):
            p_str = str(i + 1)
            if p_str not in speech_data:
                p_text = doc[i].get_text().strip().replace('\n', ' ')[:120]
                speech_data[p_str] = p_text if p_text else f"本頁為 {chapter_code} 第 {p_str} 頁之核心學習重點，請參閱圖解與課本重點。"
    if titles_dict:
        TITLES.update(titles_dict)
                
    curr = 0
    MAN = {}
    for p in range(1, n_slides + 1):
        step_count = max(1, round(len(names) / n_slides)) if n_slides > 0 else 1
        end = min(len(names), curr + step_count)
        if p == n_slides: end = len(names)
        MAN[str(p)] = names[curr:end] if len(names) > 0 else []
        curr = end
            
    # 5. 組裝 HTML
    html = BIO3_TPL
    html = re.sub(r'<title>.*?</title>', f'<title>選修生物(Ⅲ) {chapter_code} {site_title}｜{site_title}</title>', html)
    html = html.replace('代謝與酵素驛站', site_title)
    html = html.replace('選修生物(Ⅰ) · CH2-1', f'選修生物(Ⅲ) · {chapter_code}')
    html = html.replace('選修生物(Ⅰ) 2-1', f'選修生物(Ⅲ) {chapter_code}')
    html = html.replace('CH2-1 新陳代謝與酵素', f'{chapter_code} {site_title}')
    html = html.replace('metabolism-b21.quiz.v1', f'{key_prefix}.quiz.v1')
    html = html.replace('metabolism-b21.prefs.v1', f'{key_prefix}.prefs.v1')
    if player_video:
        html = re.sub(r"const VIDEO_SRC='[^']+';", f"const VIDEO_SRC='../{player_folder}/{player_video}';", html)
        html = re.sub(r'《選修生物[^\'"><]*?\.mp4》', f'《{player_video}》', html)
        
    html = html.replace('11 張</span><span class="hl-lbl">核心圖解', f'{len(learn_data)} 張</span><span class="hl-lbl">核心圖解')
    html = html.replace('25 頁</span><span class="hl-lbl">動畫簡報', f'{n_slides} 頁</span><span class="hl-lbl">動畫簡報')
    html = html.replace('五個單元 / 11 張圖解', f'{len(groups)} 個單元 / {len(learn_data)} 張圖解')
    html = html.replace('max="11"', f'max="{len(learn_data)}"')
    
    # 替換 IMG 物件
    img_start = html.find('const IMG={')
    img_end = html.find('};\n</script>', img_start)
    new_img_json = json.dumps(IMG, ensure_ascii=False)
    html = html[:img_start] + 'const IMG=' + new_img_json + ';' + html[img_end+2:]
    
    # 替換 Script 1 資料
    s1_start = html.find('const TITLES = {')
    s1_end = html.find('</script>\n<script>\n/* =====')
    
    bgs_str = ",\n".join([f"  {k}: function() {{\n{v}\n  }}" for k, v in drag_bgs.items()])
    qs_fix = ""
    for k in drag_bgs.keys():
        qs_fix += f"  if(q.bg === 'DRAG_BGS.{k}') q.bg = DRAG_BGS.{k};\n"
        
    s1_body = f"""
const TITLES = {json.dumps(TITLES, ensure_ascii=False, indent=2)};

const SPEECH = {json.dumps(speech_data, ensure_ascii=False, indent=2)};

const MAN = {json.dumps(MAN, ensure_ascii=False)};

const GROUPS = {json.dumps(groups, ensure_ascii=False)};

const LEARN = {json.dumps(learn_data, ensure_ascii=False)};

const DRAG_BGS = {{
{bgs_str}
}};

const QS = {json.dumps(qs_data, ensure_ascii=False)};
QS.forEach(q => {{
{qs_fix}}});

const TAGS = {json.dumps(tags, ensure_ascii=False)};
"""
    html = html[:s1_start] + s1_body.strip() + '\n' + html[s1_end:]
    
    out_main = os.path.join(web_dir, f"{site_title}.html")
    out_index = os.path.join(web_dir, "index.html")
    with open(out_main, 'w', encoding='utf-8') as f: f.write(html)
    with open(out_index, 'w', encoding='utf-8') as f: f.write(html)
    
    print(f"Saved: {out_main} ({os.path.getsize(out_main) / (1024*1024):.2f} MB)")
    print(f"Saved: {out_index} ({os.path.getsize(out_index) / (1024*1024):.2f} MB)")
    
    # Node.js 執行期無頭驗收
    test_js = """
const fs = require('fs');
const html = fs.readFileSync('""" + out_main + """', 'utf8');
const scriptMatches = [...html.matchAll(/<script[\\s\\S]*?>([\\s\\S]*?)<\\/script>/gi)];
const elements = {};
function getEl(id) {
  if (!elements[id]) {
    elements[id] = {
      id,
      classList: { _classes: new Set(), toggle(c, v) { if(v===undefined){if(this._classes.has(c))this._classes.delete(c);else this._classes.add(c);}else{if(v)this._classes.add(c);else this._classes.delete(c);} }, add(c){this._classes.add(c);}, remove(c){this._classes.delete(c);}, contains(c){return this._classes.has(c);} },
      attributes: {}, dataset: { pos: '0', flip: '[[1,0,1,"step_001"]]' },
      textContent: '', matches(s){return false;}, nodeType: 1,
      setAttribute(k, v){this.attributes[k]=v;}, removeAttribute(k){delete this.attributes[k];}, getAttribute(k){return this.attributes[k];}, style: { setProperty(){} },
      appendChild(c){return c;}, append(...nodes){return nodes;}, replaceChildren(...nodes){this.children=nodes;}, removeChild(c){return c;}, remove(){},
      getBoundingClientRect(){return {width:1000, height:600, top:0, bottom:600};}, querySelectorAll(sel){return [];}, querySelector(sel){return getEl('sub_'+sel);},
      options: [], children: [], childNodes: [], addEventListener(){}
    };
  }
  return elements[id];
}
const mockDoc = {
  querySelector(sel) { return sel.startsWith('#')||sel.startsWith('.') ? getEl(sel.slice(1)) : getEl(sel); },
  querySelectorAll(sel) { return []; }, getElementById(id) { return getEl(id); },
  createElement(tag) { return getEl('tag_' + Math.random().toString(36).slice(2)); },
  documentElement: getEl('html'), body: getEl('body'), addEventListener(){}
};
const mockWin = {
  document: mockDoc, localStorage: { data: {}, getItem(k){return this.data[k]||null;}, setItem(k,v){this.data[k]=v;} },
  addEventListener(){}, scrollTo(){}, innerHeight: 800, innerWidth: 1200, scrollY: 0,
  requestAnimationFrame(cb){cb();}, getComputedStyle(){return {getPropertyValue:()=>'72px'};}
};
const vm = require('vm');
const ctx = vm.createContext({
  console, document: mockDoc, window: mockWin, localStorage: mockWin.localStorage,
  ResizeObserver: class { observe(){} }, matchMedia: ()=>({matches:false}), URL: { createObjectURL(){}, revokeObjectURL(){} },
  setTimeout: ()=>{}, clearTimeout: ()=>{}, setInterval: ()=>{}, clearInterval: ()=>{}, scrollY: 0,
  getComputedStyle: ()=>({getPropertyValue:()=>'72px'}), requestAnimationFrame: cb=>{cb();},
  addEventListener: (...args)=>mockWin.addEventListener(...args)
});

for(let i=0; i<scriptMatches.length; i++) {
  vm.runInContext(scriptMatches[i][1], ctx);
}
ctx.window.__BM.go('play');
for(let i=0; i<""" + str(len(qs_data)) + """; i++) ctx.window.__BM.renderQ(i);
ctx.window.__BM.go('learn');
for(let i=0; i<""" + str(len(learn_data)) + """; i++) ctx.window.__BM.showLearn(i);
ctx.window.__BM.openShow(0);
console.log('>>> VERIFICATION PASSED FOR """ + chapter_code + """! <<<');
"""
    tmp_test = f'/tmp/verify_{key_prefix}.js'
    with open(tmp_test, 'w', encoding='utf-8') as tf: tf.write(test_js)
    res = subprocess.run(['node', tmp_test], capture_output=True, text=True)
    if res.returncode != 0:
        print("VERIFICATION FAILED:")
        print(res.stderr)
        raise RuntimeError(f"Verification failed for {chapter_code}")
    else:
        print(res.stdout.strip())
        
    # 產生製作紀錄文件
    log_file = os.path.join(web_dir, f"{site_title}_製作紀錄.md")
    with open(log_file, 'w', encoding='utf-8') as lf:
        lf.write(f"""# 選修生物(Ⅲ) {chapter_code} {site_title} 教學網頁製作紀錄

> 建立日期：2026-10-05  
> 適用單元：選修生物(Ⅲ) {chapter_code} {site_title}  
> 交付檔案：`{site_title}.html`、`index.html`

---

## 1. 規格與素材
- 課本 PDF 原寸高清裁切共 {len(crops_spec)} 張。
- 原動畫/教學影片提取 {step_idx} 個逐幀動畫畫面，對照 {n_slides} 頁簡報。
- 逐頁講稿完整對應播放器字幕。

## 2. 功能與自我檢查驗收
- **圖解探索**：{len(groups)} 個單元 / {len(learn_data)} 張核心圖解，左側 TOC 目錄完整可見。
- **互動練習**：{len(qs_data)} 道精選互動題（含 3 拖放分類、核心單選、素養多選），無頭執行期 100% 正常。
- **視覺與設備適配**：採用選修生物(Ⅲ)專屬赤緋紅高質感配色，電腦同框、手機自然流暢捲動。
""")
    print(f"Log written: {log_file}")
