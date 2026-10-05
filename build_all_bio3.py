import subprocess
import sys
import time

scripts = [
    # 第一章
    "make_ch1_1.py",
    "make_ch1_2.py",
    "make_lab1_1.py",
    # 第二章
    "make_ch2_1.py",
    "make_ch2_2.py",
    "make_lab2_1.py",
    # 第三章
    "make_ch3_1.py",
    "make_ch3_2.py",
    "make_lab3_1.py",
    # 第四章
    "make_ch4_1.py",
    "make_ch4_2.py",
    "make_ch4_3.py",
    "make_ch4_4.py",
    "make_lab4_1.py",
    # 第五章
    "make_ch5_1.py",
    "make_ch5_2.py",
    "make_ch5_3.py",
    "make_ch5_4.py",
    "make_lab5_1.py",
    # 第六章
    "make_ch6_1.py",
    "make_ch6_2.py",
    "make_ch6_3.py",
    "make_ch6_4.py",
    "make_lab6_1.py",
    "make_lab6_2.py",
    "make_lab6_3.py"
]

print(f"==================================================")
print(f"開始批次重構編譯選修生物(Ⅲ)全部 {len(scripts)} 個單元網頁")
print(f"==================================================")

start_all = time.time()
passed = []
failed = []

for idx, s in enumerate(scripts, 1):
    t0 = time.time()
    print(f"\n[{idx}/{len(scripts)}] 正在重新編譯: {s} ...")
    res = subprocess.run([sys.executable, s], capture_output=True, text=True)
    cost = time.time() - t0
    if res.returncode == 0:
        passed.append(s)
        # 尋找驗證輸出
        v_lines = [l for l in res.stdout.splitlines() if 'VERIFICATION PASSED' in l]
        v_msg = v_lines[0] if v_lines else 'OK'
        print(f"  ✓ 成功 ({cost:.1f}s) - {v_msg}")
    else:
        failed.append(s)
        print(f"  ✗ 失敗 ({cost:.1f}s)")
        print("STDERR:\n" + res.stderr[-500:])
        print("STDOUT:\n" + res.stdout[-500:])

print("\n" + "="*50)
print(f"編譯總結：成功 {len(passed)} / {len(scripts)}，耗時 {time.time()-start_all:.1f}s")
if failed:
    print(f"失敗列表: {failed}")
    sys.exit(1)
else:
    print("全部單元重構與驗收 100% 成功通過！")
