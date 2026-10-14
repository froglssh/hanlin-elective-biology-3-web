# -*- coding: utf-8 -*-
"""
抽取選修生物3新網頁 26 個單元 HTML 中的 base64 圖片至獨立 WebP 靜態檔案，
將原本 5~35 MB 的巨大單檔 HTML 瘦身為 50~150 KB 的極速秒開網頁。
"""
import os, sys, re, json, base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UNITS = [
    ("1-1_動物組織探險館_優化版.html", "1-1"),
    ("1-2_恆定平衡觀測站_優化版.html", "1-2"),
    ("2-1_循環系統運籌館_優化版.html", "2-1"),
    ("2-2_消化吸收智慧驛站_優化版.html", "2-2"),
    ("3-1_呼吸氣體交換中心_優化版.html", "3-1"),
    ("3-2_泌尿排泄恆定工房_優化版.html", "3-2"),
    ("4-1_神經調節樞紐站_優化版.html", "4-1"),
    ("4-2_體內受器感知廊_優化版.html", "4-2"),
    ("4-3_骨骼肌肉動力所_優化版.html", "4-3"),
    ("4-4_內分泌訊號調度站_優化版.html", "4-4"),
    ("5-1_免疫防禦作戰部_優化版.html", "5-1"),
    ("5-2_先天防線衛戍站_優化版.html", "5-2"),
    ("5-3_特異性免疫兵工廠_優化版.html", "5-3"),
    ("5-4_免疫調控與醫療探索坊_優化版.html", "5-4"),
    ("6-1_生殖器官奧秘館_優化版.html", "6-1"),
    ("6-2_配子生成與週期演繹驛站_優化版.html", "6-2"),
    ("6-3_受精機制探索站_優化版.html", "6-3"),
    ("6-4_生命孕育胚胎發育長廊_優化版.html", "6-4"),
    ("活動1-1_動物組織顯微觀察工坊_優化版.html", "lab1-1"),
    ("活動2-1_心臟解剖解密實驗室_優化版.html", "lab2-1"),
    ("活動3-1_腎臟解剖觀察工作坊_優化版.html", "lab3-1"),
    ("活動4-1_肌骨連動實作探秘_優化版.html", "lab4-1"),
    ("活動5-1_血型凝集抗原抗體實驗室_優化版.html", "lab5-1"),
    ("活動6-1_生殖細胞顯微鑑賞坊_優化版.html", "lab6-1"),
    ("活動6-2_代孕倫理思辨論壇_優化版.html", "lab6-2"),
    ("活動6-3_青蛙解剖比較生物學館_優化版.html", "lab6-3"),
]

def sanitize_filename(name):
    return re.sub(r'[^\w\.\-]', '_', name)

def get_ext_from_header(header):
    if "png" in header: return ".png"
    if "jpeg" in header or "jpg" in header: return ".jpg"
    if "gif" in header: return ".gif"
    if "svg" in header: return ".svg"
    return ".webp"

def process_unit(filename, slug):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"[SKIP] {filepath} not found")
        return

    orig_size = os.path.getsize(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    assets_dir = os.path.join(BASE_DIR, "assets", slug)
    os.makedirs(assets_dir, exist_ok=True)

    m_img = re.search(r"const\s+IMG\s*=\s*(\{.*?\});", content, re.DOTALL)
    if not m_img:
        print(f"[WARN] No const IMG found in {filename}")
        return

    raw_img = json.loads(m_img.group(1))
    new_img = {}
    saved_count = 0

    for k, v in raw_img.items():
        if isinstance(v, str) and v.startswith("data:image/"):
            header, b64 = v.split(",", 1)
            ext = get_ext_from_header(header)
            lower_k = k.lower()
            if lower_k.endswith((".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg")):
                img_name = sanitize_filename(k)
            else:
                img_name = f"{sanitize_filename(k)}{ext}"
            
            target_path = os.path.join(assets_dir, img_name)
            with open(target_path, "wb") as img_f:
                img_f.write(base64.b64decode(b64))
            
            new_img[k] = f"assets/{slug}/{img_name}"
            saved_count += 1
        else:
            new_img[k] = v

    new_img_str = f"const IMG = {json.dumps(new_img, ensure_ascii=False, indent=2)};"
    new_content = content[:m_img.start()] + new_img_str + content[m_img.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    new_size = os.path.getsize(filepath)
    reduction = (1 - new_size / orig_size) * 100
    print(f"[{slug:6s}] {orig_size/1024/1024:6.2f} MB -> {new_size/1024:6.1f} KB (節省 {reduction:5.1f}%) | 圖片抽出: {saved_count:3d} 張")

def main():
    print("=== 開始選修生物3 小節網頁瘦身優化 ===")
    total_orig = 0
    total_new = 0
    for filename, slug in UNITS:
        fp = os.path.join(BASE_DIR, filename)
        if os.path.exists(fp):
            total_orig += os.path.getsize(fp)
        process_unit(filename, slug)
        if os.path.exists(fp):
            total_new += os.path.getsize(fp)
    
    total_red = (1 - total_new / total_orig) * 100 if total_orig else 0
    print("=" * 60)
    print(f"總計 HTML 體積: {total_orig/1024/1024:.2f} MB -> {total_new/1024/1024:.2f} MB (總共節省 {total_red:.1f}%)")
    print("=== 全部優化完成 ===")

if __name__ == "__main__":
    main()
