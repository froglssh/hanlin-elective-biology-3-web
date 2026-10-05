#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
選修生物(Ⅲ) 短網址目錄同步腳本
將各單元生成的教學網頁 index.html 自動複製到根目錄的短網址目錄中
例如：CH1-1-動物組織的構造與功能/教學網頁/index.html -> ch1-1/index.html
"""

import os
import shutil

UNIT_MAP = [
    # 第 1 章
    ("CH1-1-動物組織的構造與功能", "ch1-1"),
    ("CH1-2-恆定的生理意義與重要性", "ch1-2"),
    ("探討活動1-1-動物組織的觀察", "lab1-1"),
    
    # 第 2 章
    ("CH2-1-循環系統", "ch2-1"),
    ("CH2-2-消化系統", "ch2-2"),
    ("探討活動2-1-心臟的觀察", "lab2-1"),
    
    # 第 3 章
    ("CH3-1-呼吸系統", "ch3-1"),
    ("CH3-2-排泄系統", "ch3-2"),
    ("探討活動3-1-腎臟的觀察", "lab3-1"),
    
    # 第 4 章
    ("CH4-1-神經系統", "ch4-1"),
    ("CH4-2-體內的受器", "ch4-2"),
    ("CH4-3-肌肉與骨骼", "ch4-3"),
    ("CH4-4-內分泌系統", "ch4-4"),
    ("探討活動4-1-肌肉與骨骼的運作", "lab4-1"),
    
    # 第 5 章
    ("CH5-1-免疫系統", "ch5-1"),
    ("CH5-2-先天性免疫", "ch5-2"),
    ("CH5-3-後天性免疫", "ch5-3"),
    ("CH5-4-免疫失調與排斥", "ch5-4"),
    ("探討活動5-1-藉由ABO血型的鑑定探討抗原與抗體反應的基本模式", "lab5-1"),
    
    # 第 6 章
    ("CH6-1-生殖系統", "ch6-1"),
    ("CH6-2-配子的形成", "ch6-2"),
    ("CH6-3-受精過程", "ch6-3"),
    ("CH6-4-胚胎發育與懷孕", "ch6-4"),
    ("探討活動6-1-生殖腺與生殖細胞的觀察", "lab6-1"),
    ("探討活動6-2-代理孕母的倫理與法律問題", "lab6-2"),
    ("探討活動6-3-蛙外部形態及內部構造的觀察", "lab6-3"),
]

def sync():
    root = os.path.abspath(os.path.dirname(__file__))
    synced = 0
    missing = 0
    
    print("=== 開始同步選修生物(Ⅲ) 短網址目錄 ===")
    for folder, short_name in UNIT_MAP:
        src_path = os.path.join(root, folder, "教學網頁", "index.html")
        dest_dir = os.path.join(root, short_name)
        dest_path = os.path.join(dest_dir, "index.html")
        
        if os.path.exists(src_path):
            os.makedirs(dest_dir, exist_ok=True)
            # 複製檔案
            shutil.copy2(src_path, dest_path)
            size = os.path.getsize(dest_path)
            print(f"[OK] {short_name:<8} <- {folder} ({size:,} bytes)")
            synced += 1
        else:
            print(f"[WAIT] {short_name:<8} 尚未生成 ({folder})")
            missing += 1
            
    print(f"=== 同步完成: 已完成 {synced} / {len(UNIT_MAP)} 個單元, 等候 {missing} 個單元 ===")
    return synced, missing

if __name__ == "__main__":
    sync()
