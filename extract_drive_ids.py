import os, subprocess, json

base_dir = "/Users/froglssh/Library/CloudStorage/GoogleDrive-frog@lssh.tp.edu.tw/我的雲端硬碟/04教科書/0自編教材/翰林/PPT動畫/選修生物3"

def get_xattr(path):
    try:
        res = subprocess.run(["xattr", "-p", "com.google.drivefs.item-id#S", path], capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return ""

units = [
    ("正課", "CH1-1", "CH1-1-動物組織的構造與功能", "動物組織的構造與功能"),
    ("正課", "CH1-2", "CH1-2-恆定的生理意義與重要性", "恆定的生理意義與重要性"),
    ("正課", "CH2-1", "CH2-1-循環系統", "循環系統"),
    ("正課", "CH2-2", "CH2-2-消化系統", "消化系統"),
    ("正課", "CH3-1", "CH3-1-呼吸系統", "呼吸系統"),
    ("正課", "CH3-2", "CH3-2-排泄系統", "排泄系統"),
    ("正課", "CH4-1", "CH4-1-神經系統", "神經系統"),
    ("正課", "CH4-2", "CH4-2-體內的受器", "體內的受器"),
    ("正課", "CH4-3", "CH4-3-肌肉與骨骼", "肌肉與骨骼"),
    ("正課", "CH4-4", "CH4-4-內分泌系統", "內分泌系統"),
    ("正課", "CH5-1", "CH5-1-免疫系統", "免疫系統"),
    ("正課", "CH5-2", "CH5-2-先天性免疫", "先天性免疫"),
    ("正課", "CH5-3", "CH5-3-後天性免疫", "後天性免疫"),
    ("正課", "CH5-4", "CH5-4-免疫失調與排斥", "免疫失調與排斥"),
    ("正課", "CH6-1", "CH6-1-生殖系統", "生殖系統"),
    ("正課", "CH6-2", "CH6-2-配子的形成", "配子的形成"),
    ("正課", "CH6-3", "CH6-3-受精過程", "受精過程"),
    ("正課", "CH6-4", "CH6-4-胚胎發育與懷孕", "胚胎發育與懷孕"),
    ("探討活動", "探討1-1", "探討活動1-1-動物組織的觀察", "動物組織的觀察"),
    ("探討活動", "探討2-1", "探討活動2-1-心臟的觀察", "心臟的觀察"),
    ("探討活動", "探討3-1", "探討活動3-1-腎臟的觀察", "腎臟的觀察"),
    ("探討活動", "探討4-1", "探討活動4-1-肌肉與骨骼的運作", "肌肉與骨骼的運作"),
    ("探討活動", "探討5-1", "探討活動5-1-藉由ABO血型的鑑定探討抗原與抗體反應的基本模式", "藉由ABO血型的鑑定探討抗原與抗體反應的基本模式"),
    ("探討活動", "探討6-1", "探討活動6-1-生殖腺與生殖細胞的觀察", "生殖腺與生殖細胞的觀察"),
    ("探討活動", "探討6-2", "探討活動6-2-代理孕母的倫理與法律問題", "代理孕母的倫理與法律問題"),
    ("探討活動", "探討6-3", "探討活動6-3-蛙外部形態及內部構造的觀察", "蛙外部形態及內部構造的觀察"),
]

data = []

for category, code, folder_name, title in units:
    fpath = os.path.join(base_dir, folder_name)
    vdir = os.path.join(fpath, "教學影片")
    
    mp4_name = ""
    file_id = ""
    size_mb = 0
    if os.path.exists(vdir):
        mp4s = [f for f in os.listdir(vdir) if f.endswith(".mp4") and "backup" not in f]
        if mp4s:
            mp4_name = mp4s[0]
            mp4_path = os.path.join(vdir, mp4_name)
            file_id = get_xattr(mp4_path)
            size_mb = round(os.path.getsize(mp4_path) / (1024*1024), 2)
            
    vfolder_id = get_xattr(vdir) if os.path.exists(vdir) else ""
    
    data.append({
        "category": category,
        "code": code,
        "folder_name": folder_name,
        "title": title,
        "mp4_name": mp4_name,
        "file_id": file_id,
        "size_mb": size_mb,
        "vfolder_id": vfolder_id,
        "preview_url": f"https://drive.google.com/file/d/{file_id}/preview" if file_id else "",
        "view_url": f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk" if file_id else "",
        "folder_url": f"https://drive.google.com/drive/folders/{vfolder_id}" if vfolder_id else ""
    })

# 輸出成 Markdown 表格
md_lines = [
    "# 翰林版 選修生物（Ⅲ）教學影片 Google 雲端硬碟網址總表",
    "",
    "> 整理時間：2026-10-11  ",
    "> 本表包含選修生物（Ⅲ）全冊 18 個正課單元與 8 個探討活動單元（共 26 部教學影片）之 Google Drive 檔案識別碼 (File ID)、線上預覽嵌入連結與直接觀看網址。",
    "",
    "## 一、正課教學影片（共 18 單元）",
    "",
    "| 單元編號 | 單元名稱 | 影片檔案名稱 | 大小 (MB) | Google Drive File ID | 預覽嵌入網址 (Preview) | 雲端硬碟觀看網址 (View) |",
    "| :--- | :--- | :--- | :---: | :--- | :--- | :--- |"
]

for item in data:
    if item["category"] == "正課":
        code = item["code"]
        title = item["title"]
        mp4_name = item["mp4_name"]
        size_mb = item["size_mb"]
        fid = item["file_id"]
        p_url = item["preview_url"]
        v_url = item["view_url"]
        md_lines.append(f"| **{code}** | {title} | `{mp4_name}` | {size_mb} | `{fid}` | [預覽連結]({p_url}) | [觀看連結]({v_url}) |")

md_lines.extend([
    "",
    "## 二、探討活動教學影片（共 8 單元）",
    "",
    "| 單元編號 | 活動名稱 | 影片檔案名稱 | 大小 (MB) | Google Drive File ID | 預覽嵌入網址 (Preview) | 雲端硬碟觀看網址 (View) |",
    "| :--- | :--- | :--- | :---: | :--- | :--- | :--- |"
])

for item in data:
    if item["category"] == "探討活動":
        code = item["code"]
        title = item["title"]
        mp4_name = item["mp4_name"]
        size_mb = item["size_mb"]
        fid = item["file_id"]
        p_url = item["preview_url"]
        v_url = item["view_url"]
        md_lines.append(f"| **{code}** | {title} | `{mp4_name}` | {size_mb} | `{fid}` | [預覽連結]({p_url}) | [觀看連結]({v_url}) |")

md_lines.extend([
    "",
    "## 三、JSON 資料格式（供程式批次替換使用）",
    "```json",
    json.dumps(data, ensure_ascii=False, indent=2),
    "```",
    ""
])

out_md = os.path.join(base_dir, "選修生物3教學影片雲端硬碟網址總表.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print("Markdown generated successfully at:", out_md)
print(f"Total units processed: {len(data)}, missing ID: {len([x for x in data if not x['file_id']])}")
