# -*- coding: utf-8 -*-
"""
選修生物（Ⅲ）獨立單檔教學網頁組裝與備份腳本
比照選修生物（Ⅰ）規範，將「選生三新網頁」中抽離圖片的優化版 HTML，
將 WebP 圖片重新轉換為 Base64 Data URI 內嵌，
還原為完全自包含、可離線獨立運作的完整單檔 HTML，
並備份輸出至各小節的「教學網頁/」資料夾中（包含原檔名與 index.html）。
"""
import os, sys, re, json, base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

UNITS_MAPPING = [
    ('1-1_動物組織探險館_優化版.html', '1-1', 'CH1-1-動物組織的構造與功能'),
    ('1-2_恆定平衡觀測站_優化版.html', '1-2', 'CH1-2-恆定的生理意義與重要性'),
    ('2-1_循環系統運籌館_優化版.html', '2-1', 'CH2-1-循環系統'),
    ('2-2_消化吸收智慧驛站_優化版.html', '2-2', 'CH2-2-消化系統'),
    ('3-1_呼吸氣體交換中心_優化版.html', '3-1', 'CH3-1-呼吸系統'),
    ('3-2_泌尿排泄恆定工房_優化版.html', '3-2', 'CH3-2-排泄系統'),
    ('4-1_神經調節樞紐站_優化版.html', '4-1', 'CH4-1-神經系統'),
    ('4-2_體內受器感知廊_優化版.html', '4-2', 'CH4-2-體內的受器'),
    ('4-3_骨骼肌肉動力所_優化版.html', '4-3', 'CH4-3-肌肉與骨骼'),
    ('4-4_內分泌訊號調度站_優化版.html', '4-4', 'CH4-4-內分泌系統'),
    ('5-1_免疫防禦作戰部_優化版.html', '5-1', 'CH5-1-免疫系統'),
    ('5-2_先天防線衛戍站_優化版.html', '5-2', 'CH5-2-先天性免疫'),
    ('5-3_特異性免疫兵工廠_優化版.html', '5-3', 'CH5-3-後天性免疫'),
    ('5-4_免疫調控與醫療探索坊_優化版.html', '5-4', 'CH5-4-免疫失調與排斥'),
    ('6-1_生殖器官奧秘館_優化版.html', '6-1', 'CH6-1-生殖系統'),
    ('6-2_配子生成與週期演繹驛站_優化版.html', '6-2', 'CH6-2-配子的形成'),
    ('6-3_受精機制探索站_優化版.html', '6-3', 'CH6-3-受精過程'),
    ('6-4_生命孕育胚胎發育長廊_優化版.html', '6-4', 'CH6-4-胚胎發育與懷孕'),
    ('活動1-1_動物組織顯微觀察工坊_優化版.html', 'lab1-1', '探討活動1-1-動物組織的觀察'),
    ('活動2-1_心臟解剖解密實驗室_優化版.html', 'lab2-1', '探討活動2-1-心臟的觀察'),
    ('活動3-1_腎臟解剖觀察工作坊_優化版.html', 'lab3-1', '探討活動3-1-腎臟的觀察'),
    ('活動4-1_肌骨連動實作探秘_優化版.html', 'lab4-1', '探討活動4-1-肌肉與骨骼的運作'),
    ('活動5-1_血型凝集抗原抗體實驗室_優化版.html', 'lab5-1', '探討活動5-1-藉由ABO血型的鑑定探討抗原與抗體反應的基本模式'),
    ('活動6-1_生殖細胞顯微鑑賞坊_優化版.html', 'lab6-1', '探討活動6-1-生殖腺與生殖細胞的觀察'),
    ('活動6-2_代孕倫理思辨論壇_優化版.html', 'lab6-2', '探討活動6-2-代理孕母的倫理與法律問題'),
    ('活動6-3_青蛙解剖比較生物學館_優化版.html', 'lab6-3', '探討活動6-3-蛙外部形態及內部構造的觀察'),
]

def get_mime(filename):
    lower = filename.lower()
    if lower.endswith('.png'): return 'image/png'
    if lower.endswith(('.jpg', '.jpeg')): return 'image/jpeg'
    if lower.endswith('.gif'): return 'image/gif'
    if lower.endswith('.svg'): return 'image/svg+xml'
    return 'image/webp'

def main():
    print("=== 開始組裝選修生物（Ⅲ）全 26 單元單檔獨立網頁 ===")
    total_bytes = 0
    success_count = 0

    for html_file, slug, folder in UNITS_MAPPING:
        src_html_path = os.path.join(BASE_DIR, html_file)
        if not os.path.exists(src_html_path):
            print(f"[SKIP] 找不到來源檔案: {html_file}")
            continue

        with open(src_html_path, "r", encoding="utf-8") as f:
            content = f.read()

        m_img = re.search(r"const\s+IMG\s*=\s*(\{.*?\});", content, re.DOTALL)
        if not m_img:
            print(f"[WARN] {html_file} 未發現 const IMG 定義")
            continue

        raw_img = json.loads(m_img.group(1))
        assembled_img = {}

        for k, v in raw_img.items():
            if isinstance(v, str) and v.startswith("assets/"):
                img_path = os.path.join(BASE_DIR, v)
                if os.path.exists(img_path):
                    with open(img_path, "rb") as img_f:
                        b64 = base64.b64encode(img_f.read()).decode("ascii")
                    mime = get_mime(img_path)
                    assembled_img[k] = f"data:{mime};base64,{b64}"
                else:
                    assembled_img[k] = v
            else:
                assembled_img[k] = v

        img_json_str = f"const IMG = {json.dumps(assembled_img, ensure_ascii=False, indent=2)};"
        full_content = content[:m_img.start()] + img_json_str + content[m_img.end():]

        dst_dir = os.path.join(PARENT_DIR, folder, "教學網頁")
        os.makedirs(dst_dir, exist_ok=True)

        target_named = os.path.join(dst_dir, html_file)
        target_index = os.path.join(dst_dir, "index.html")

        with open(target_named, "w", encoding="utf-8") as f:
            f.write(full_content)
        with open(target_index, "w", encoding="utf-8") as f:
            f.write(full_content)

        size = os.path.getsize(target_named)
        total_bytes += size
        success_count += 1
        print(f"[{slug:6s}] -> {folder}/教學網頁/ | {size/1024/1024:6.2f} MB (圖片數: {len(assembled_img):3d})")

    print("=" * 65)
    print(f"完成！成功組裝 {success_count}/{len(UNITS_MAPPING)} 單元，總體積: {total_bytes/1024/1024:.2f} MB")

if __name__ == "__main__":
    main()
