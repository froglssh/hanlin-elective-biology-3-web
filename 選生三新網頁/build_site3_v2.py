# -*- coding: utf-8 -*-
"""選修生物（Ⅲ）教材入口網站產生器【第二版・獨立新版】
內容依翰林版《選修生物Ⅲ（全）》課本改寫。
連結第二版 26 個優化版互動教學網頁（依章節順序冠以前綴，如 1-1_*.html、活動1-1_*.html）。
與第一版入口網頁完全獨立。
"""
import html, os, sys
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
DRIVE = 'https://drive.google.com/file/d/{}/view?usp=drivesdk'

ICON_OUT = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_GO = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_ZOOM = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="m16 16 4.5 4.5M8.5 11h5M11 8.5v5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
ICON_PLAY = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 8.5v7l6-3.5z" fill="currentColor"/></svg>'
ICON_BOOK = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5C6.5 4.5 9.5 4.5 12 6c2.5-1.5 5.5-1.5 8-.5v13c-2.5-1-5.5-1-8 .5-2.5-1.5-5.5-1.5-8-.5z M12 6v13.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ICON_SPARKLE = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" style="color:#d97706"><path d="m12 3 2.8 5.7L21 9.5l-4.5 4.4 1.1 6.1L12 17.2 6.4 20l1.1-6.1L3 9.5l6.2-.8z" fill="currentColor"/></svg>'

E = html.escape

# Google 雲端硬碟教學影片 ID（來源：選修生物3網頁發布總表.md）
V = {
 'ch1-1':'1IMSZbtkA2grOFY_84XxxePFveWir7wdb','ch1-2':'1HlwVSZpTCPfowHKZLHIc4eOs_Gkoc78L','lab1-1':'1n0WN-MD4PjrTMVMmji5VHZ0kqFblhSMi',
 'ch2-1':'18aM6X13PLFrN1Vv1EXZd_lJwl5JXyZ0T','ch2-2':'1dKWYcINVh87g3hVd0DdcAWlyYanNj6g3','lab2-1':'1LhdTyFFunu5xXNfLqw8cWslzRYNzcXdL',
 'ch3-1':'1g2rj9m2nYDhUu_nhyrRZZ2ft9-9LubOY','ch3-2':'1qMvQUo1ipJO6KpsuTfKJ-yuf9KL7Yhcd','lab3-1':'12mNIM7F-pWnF64m6-O711x8HxUmckozX',
 'ch4-1':'10XCgiSafAd72WhzPJGxhqPC16NvWlVlE','ch4-2':'1_wrdC3AbbqCCJtjQYjjsjnJ9SIsTQL2f','ch4-3':'1iiWEFENT_sFKvtLsetScMV8aPo-cQ6Fx','ch4-4':'1g0S4bb2n7-I2cgaXiwApRAcJDzGH2Z78','lab4-1':'1DIyFomb5ydMd48B6UjEJh-xb9mVTETpA',
 'ch5-1':'1lUkQishZyDR0YU8Kz7sbQljuJI_l6Tdm','ch5-2':'1wB2BrgDuN5uYegCkdp9C8jCp0FVjKYqf','ch5-3':'1Ph_ZxxLoKbkIf_emkSxDU1nxJekS5SbX','ch5-4':'1zYKLrSe8VNV8gDIkUikZGnNJYMgyEY3Z','lab5-1':'1Cc3U4_7yknfJFSEIWWh7xc3x4AFJMhnU',
 'ch6-1':'15_KcCw9UEtTcnllGDLL4HJq4_BlC4-HW','ch6-2':'1NKJt-HqWSEtMo62yB2WOAkPgVzLLRCVg','ch6-3':'1adyibv8qII-XlF6wgQLkJyb9y7Ko9Jdi','ch6-4':'1JfIlmGDWunraeylm0XHVP95f1Cj6Cu6U',
 'lab6-1':'1slcKFdUCsYMUudj58ldy4Nj7atK335S3','lab6-2':'1_Ay_ViuPqT7YpymHWFS93NHxFv9JDOVi','lab6-3':'1afm3j97kmoTD8QJGeRPU3buXnjbQGf77',
}

def U(code, title, web, pages, fig, cap, intro, subs, tags):
    slug = 'ch' + code
    file_name = f"{code}_{web}_優化版.html"
    return dict(code=code, title=title, web=web, slug=slug, file=file_name, vid=V[slug], pages=pages, fig=fig, cap=cap, intro=intro, subs=subs, tags=tags)

def L(code, title, web, pages, fig, cap, intro):
    slug = 'lab' + code
    code_str = '活動 ' + code
    file_name = f"活動{code}_{web}_優化版.html"
    return dict(code=code_str, title=title, web=web, slug=slug, file=file_name, vid=V[slug], pages=pages, fig=fig, cap=cap, intro=intro)

CHAPTERS = [
 dict(n=1, title='動物體的組成與恆定性', en='Organization &amp; Homeostasis', a='#0d9488', a2='#2dd4bf', t='#f0fdfa',
  lead='動物體由細胞、組織、器官到器官系統層層組成。本章先認識上皮、肌肉、神經與結締四類組織的形態與功能，再跟著伯納與坎能理解「恆定」的意義，以及回饋控制、拮抗作用與協同作用如何讓體溫、血糖等生理數值維持在穩定範圍。',
  units=[
   U('1-1', '動物組織的構造與功能', '動物組織探險館', 'P.8–15', 's1-1', '圖 1－1　動物體的組成層次',
     '功能與形態相似的細胞加上細胞間質聚集成組織，動物組織分為四類：上皮組織緊密排列、以基底膜與結締組織相連，依形態分為扁平、立方與柱狀上皮，負責保護、吸收、分泌等；肌肉組織分為骨骼肌、心肌與平滑肌，前兩者具橫紋，只有骨骼肌是隨意肌；神經組織由神經元與神經膠細胞組成，負責傳遞訊息；結締組織細胞間質豐富，包含硬骨、軟骨、脂肪與血液等，具支持、連結與運輸功能。',
     ['1-1.1 上皮組織', '1-1.2 肌肉組織', '1-1.3 神經組織', '1-1.4 結締組織'],
     ['組成層次', '扁平・立方・柱狀上皮', '骨骼肌・心肌・平滑肌', '神經元與神經膠細胞', '細胞間質', '結締組織']),
   U('1-2', '恆定的生理意義與重要性', '恆定平衡觀測站', 'P.16–20', 's1-2', '圖 1－6　循環、呼吸、消化和泌尿系統間的功能聯繫',
     '伯納於 1857 年提出生物會維持穩定的「內在環境」，坎能在 1932 年將其命名為恆定。體溫、體液組成、血液酸鹼值、血糖與激素濃度等都維持在一定範圍，一旦超出調節能力就可能中暑、失溫甚至死亡。恆定靠回饋控制維持：負回饋削弱刺激的影響，正回饋則增強刺激；胰島素與升糖素作用相反稱為拮抗作用，不同激素效果相加則為協同作用。',
     ['1-2.1 恆定概念的發展與重要性', '1-2.2 恆定的維持與調節'],
     ['內在環境', '伯納與坎能', '負回饋', '正回饋', '拮抗作用', '協同作用']),
  ],
  labs=[
   L('1-1', '動物組織的觀察', '動物組織顯微觀察工坊', 'P.21–28', 'a1-1', '比對小腸、骨骼肌等永久玻片中的組織特徵',
     '以複式顯微鏡觀察小腸、骨骼肌、脂肪組織、脊髓灰質與氣管等永久玻片標本，記錄細胞形態、排列方式、間距與細胞核數量和位置，並用顯微測量量測細胞大小，歸納四類組織的特徵；再以亞甲藍染色觀察雞胸軟骨的新鮮切片。'),
  ]),
 dict(n=2, title='循環與消化', en='Circulation &amp; Digestion', a='#be123c', a2='#fb7185', t='#fff1f2',
  lead='細胞要獲得養分、排除廢物，得靠循環系統運送，也得靠消化系統把食物分解成可吸收的小分子。本章從心臟構造、血液循環、心搏週期、血管與血壓，一路談到血液與淋巴，再走過消化道認識食物的消化與養分的吸收運輸。',
  units=[
   U('2-1', '循環系統', '循環系統運籌館', 'P.32–44', 's2-1', '圖 2－3　心臟構造的示意圖（腹面觀）',
     '人體循環系統包含心血管循環系統與淋巴循環系統。心臟由心肌構成，分為兩心房兩心室，左心室壁最厚；房室瓣（二尖瓣、三尖瓣）與半月瓣防止血液逆流。血液經體循環與肺循環運行，心搏週期包含心房、心室的收縮與舒張，心音與心電圖可反映其變化。動脈、微血管、靜脈結構各有特色，血壓由心臟收縮產生；血液由血漿與血球組成，組織液則由淋巴管回收，經淋巴結過濾後送回靜脈。',
     ['2-1.1 心臟的構造', '2-1.2 血液循環', '2-1.3 心搏週期', '2-1.4 血管與血壓', '2-1.5 血液與淋巴的組成', '2-1.6 淋巴循環'],
     ['開放式與封閉式循環', '房室瓣與半月瓣', '體循環與肺循環', '心搏週期', '血壓', '淋巴循環']),
   U('2-2', '消化系統', '消化吸收智慧驛站', 'P.45–55', 's2-2', '圖 2－15　消化道的運動方式與胃壁的肌肉層',
     '消化系統包括消化道與消化腺。消化道管壁由黏膜層、黏膜下層、肌肉層與漿膜層構成，藉蠕動推送食物；胃有縱肌、環肌與斜行肌，可反覆攪拌食糜，小腸則以分節運動使食糜與消化液充分混合。物理性消化讓食物變小，化學性消化則由各種消化酵素把醣類、蛋白質、脂質分解為小分子。養分主要在小腸絨毛被吸收，經微血管或乳糜管進入循環系統運送全身。',
     ['2-2.1 人體的消化構造與食物的消化', '2-2.2 養分的吸收與運輸'],
     ['消化道管壁分層', '蠕動與分節運動', '物理性與化學性消化', '消化酵素', '小腸絨毛', '肝門靜脈']),
  ],
  labs=[
   L('2-1', '心臟的觀察', '心臟解剖解密實驗室', 'P.56–65', 'a2-1', '辨識連結心臟的血管並比較動脈與靜脈管壁',
     '解剖新鮮豬心，先分辨腹面與背面、心房與心室，比較左右心室的肌肉厚度，並辨識主動脈、肺動脈、上下大靜脈與肺靜脈；再由上大靜脈與肺動脈注水觀察血流方向，剖開心臟觀察房室瓣、腱索與半月瓣，推論心臟如何確保血液單向流動。'),
  ]),
 dict(n=3, title='呼吸與排泄', en='Respiration &amp; Excretion', a='#15803d', a2='#4ade80', t='#f0fdf4',
  lead='細胞代謝需要氧氣、會產生二氧化碳與含氮廢物。本章認識人體的呼吸構造，理解肋間肌與橫膈如何改變胸腔體積完成呼吸運動與氣體交換；再走進腎臟，看腎元如何經過濾、再吸收與分泌形成尿液，並維持體液的恆定。',
  units=[
   U('3-1', '呼吸系統', '呼吸氣體交換中心', 'P.70–75', 's3-1', '圖 3－1　人體的呼吸系統',
     '呼吸系統由鼻腔、咽、喉、氣管、支氣管與肺組成，氣管以 C 型軟骨維持管腔，肺泡表面密布微血管，是氣體交換的主要區域。肺本身沒有肌肉，吸氣時橫膈肌與肋間肌收縮，胸腔體積變大、肺內壓力低於大氣壓而使空氣流入；呼氣時肌肉放鬆、胸腔縮小。O₂ 與 CO₂ 依分壓差在肺泡與組織間擴散，並由血液運輸。',
     ['3-1.1 人體的呼吸構造', '3-1.2 人體呼吸運動的原理'],
     ['呼吸作用與呼吸運動', '肺泡', '橫膈肌與肋間肌', '肺內壓力', '氣體分壓', '氣體運輸']),
   U('3-2', '排泄系統', '泌尿排泄恆定工房', 'P.76–84', 's3-2', '圖 3－6　腎臟的內部構造示意圖',
     '動物的含氮廢物有氨、尿素與尿酸三種型式，毒性、溶解度與排泄所需水量各不相同。人體泌尿系統包括腎臟、輸尿管、膀胱與尿道；腎元由腎小體（絲球體與鮑氏囊）與腎小管組成。尿液經過濾作用、再吸收作用與分泌作用形成，葡萄糖與胺基酸在近曲小管幾乎全部被再吸收；抗利尿素等激素則調節水分與無機鹽的再吸收，以維持體液恆定。',
     ['3-2.1 腎元的構造與功能', '3-2.2 尿液的形成', '3-2.3 體液的恆定'],
     ['氨・尿素・尿酸', '腎元', '絲球體與鮑氏囊', '過濾・再吸收・分泌', '抗利尿素', '體液恆定']),
  ],
  labs=[
   L('3-1', '腎臟的觀察', '腎臟解剖觀察工作坊', 'P.85–92', 'a3-1', '剔除脂肪後觀察腎臟側邊的管狀構造',
     '解剖新鮮豬腎，依管壁特性分辨腎動脈、腎靜脈與輸尿管，再由腎動脈注入黑色色素，縱切後觀察皮質、髓質、腎錐體與腎盂的分布；最後以顯微鏡觀察腎臟永久玻片中的絲球體與腎小管，推論尿液形成的途徑。'),
  ]),
 dict(n=4, title='感應', en='Sensing &amp; Response', a='#4f46e5', a2='#818cf8', t='#eef2ff',
  lead='生物要感受刺激並做出反應。本章從細胞膜電位與動作電位談起，認識神經元間的訊號傳遞與人體神經系統；接著介紹各種受器，再看神經如何協調肌肉與骨骼完成隨意與不隨意運動，最後認識內分泌系統的激素調節。',
  units=[
   U('4-1', '神經系統', '神經調節樞紐站', 'P.96–107', 's4-1', '圖 4－8　人體的中樞神經系統與周圍神經系統',
     '神經元依傳遞方向分為感覺、聯絡與運動神經元。霍奇金與赫胥黎以烏賊巨大軸突發現：靜止膜電位約 －70 mV，受刺激去極化達閾值後鈉離子通道大量開啟，產生動作電位，再經鉀離子外流再極化。有髓鞘軸突以跳躍式傳導加快速度；訊號到軸突末梢時釋放神經傳遞物，經突觸傳給下一個細胞。人體神經系統分為腦與脊髓構成的中樞神經系統，以及周圍神經系統。',
     ['4-1.1 細胞膜電位', '4-1.2 動作電位', '4-1.3 神經元間的訊號傳遞', '4-1.4 人體的神經系統'],
     ['靜止膜電位', '去極化與再極化', '動作電位', '跳躍式傳導', '突觸與神經傳遞物', '中樞與周圍神經']),
   U('4-2', '體內的受器', '體內受器感知廊', 'P.108–113', 's4-2', '圖 4－11　視網膜的內部構造示意圖',
     '受器把刺激轉換成神經訊號，傳到中樞神經系統整合。視網膜上的光受器有視桿細胞（感受弱光）與視錐細胞（藍、綠、紅錐，負責色覺）；皮膚中有冷覺與熱覺的溫度受器、痛覺受器，以及巴氏小體等機械受器；耳蝸毛細胞感受聲波振動，也屬機械受器；味覺與嗅覺則由化學受器偵測。',
     ['4-2.1 光受器', '4-2.2 溫度受器', '4-2.3 痛覺受器', '4-2.4 機械受器', '4-2.5 化學受器'],
     ['視桿與視錐細胞', '溫度受器', '痛覺受器', '巴氏小體', '耳蝸毛細胞', '味覺與嗅覺']),
   U('4-3', '肌肉與骨骼', '骨骼肌肉動力所', 'P.114–119', 's4-3', '圖 4－20　運動終板',
     '體神經系統控制骨骼肌完成隨意運動，自律神經系統則調控平滑肌、心肌與腺體。成對骨骼肌如肱二頭肌與肱三頭肌互相拮抗；骨骼包含硬骨與軟骨，關節以韌帶固定。運動神經元在神經肌肉會合處釋放乙醯膽鹼，引發肌纖維收縮，一個運動神經元與其支配的肌纖維稱為運動單位；自律神經系統的交感與副交感神經作用多相反。',
     ['4-3.1 神經系統對運動的協調', '4-3.2 體神經系統與隨意運動', '4-3.3 自律神經系統與不隨意運動'],
     ['體神經與自律神經', '肌肉拮抗作用', '硬骨・軟骨・韌帶', '乙醯膽鹼', '運動單位', '交感與副交感神經']),
   U('4-4', '內分泌系統', '內分泌訊號調度站', 'P.120–134', 's4-4', '圖 4－26　人體主要的內分泌腺與激素對照示意圖',
     '貝利士與史塔冷於 1902 年提出激素的概念。內分泌腺沒有導管，激素經血液運送到目標細胞，與專一性受體結合，作用慢但持久。下視丘與腦垂腺是調控中心，此外還有甲狀腺、副甲狀腺、腎上腺、胰島與性腺等；激素依性質可作用於細胞膜受體或進入細胞內，並透過負回饋（以及少數正回饋）維持血糖、血鈣與體液等恆定。',
     ['4-4.1 激素與人體的內分泌系統', '4-4.2 激素的作用機制', '4-4.3 內分泌維持恆定的機制'],
     ['激素', '下視丘與腦垂腺', '甲狀腺素', '胰島素與升糖素', '激素受體', '負回饋調節']),
  ],
  labs=[
   L('4-1', '肌肉與骨骼的運作', '肌骨連動實作探秘', 'P.135–137', 'a4-1', '去除雞翅表皮，對照人體手臂的三節構造',
     '以新鮮雞翅對照人體手臂，去皮後分離第一節的肌肉，尋找關節、肌腱與骨骼的連接位置，拉動不同側的肌肉觀察翅膀彎曲或伸展，理解肌肉的拮抗作用；延伸活動可用筷子與橡皮筋設計模型模擬雞翅運動。'),
  ]),
 dict(n=5, title='防禦', en='Immune Defense', a='#b45309', a2='#f59e0b', t='#fffbeb',
  lead='人體每天面對病毒、細菌與寄生蟲等病原體。本章先認識白血球與淋巴器官，再分別介紹皮膜屏障、吞噬作用與發炎反應等先天性免疫，以及由 T 細胞與 B 細胞執行的後天性免疫與疫苗，最後探討過敏、自體免疫疾病、免疫缺失症與器官移植的排斥。',
  units=[
   U('5-1', '免疫系統', '免疫防禦作戰部', 'P.142–148', 's5-1', '圖 5－1　血液中血球的種類及其細胞起源',
     '白血球都由骨髓的造血幹細胞分化而來：骨髓先驅細胞形成嗜中性球、嗜酸性球、嗜鹼性球、肥大細胞與單核球（可再分化為巨噬細胞與樹突細胞），淋巴先驅細胞則形成 T 細胞、B 細胞與自然殺手細胞。血液檢查中各類白血球的變化可協助判斷感染類型。免疫反應分為非專一性的先天性免疫與具專一性的後天性免疫，並仰賴骨髓、胸腺、淋巴結與脾臟等淋巴器官。',
     ['5-1.1 白血球的種類', '5-1.2 淋巴器官', '5-1.3 免疫反應'],
     ['造血幹細胞', '顆粒球', '巨噬細胞與樹突細胞', '淋巴球', '淋巴器官', '先天性與後天性免疫']),
   U('5-2', '先天性免疫', '先天防線衛戍站', 'P.149–154', 's5-2', '圖 5－7　發炎反應與吞噬作用',
     '先天性免疫屬非專一性防禦。第一道防線是皮膜屏障，包括角質化表皮、纖毛擺動等物理性防禦，汗液與淚液中的溶菌酶、胃酸等化學性防禦，以及共生微生物的生物性防禦。病原體突破屏障後，嗜中性球、巨噬細胞與樹突細胞進行吞噬作用；受傷組織的肥大細胞釋放組織胺，引起紅、熱、腫、痛的發炎反應，發燒則是全身性發炎反應的保護作用。',
     ['5-2.1 皮膜屏障', '5-2.2 吞噬作用與發炎反應'],
     ['皮膜屏障', '溶菌酶', '吞噬作用', '肥大細胞與組織胺', '發炎反應', '發燒']),
   U('5-3', '後天性免疫', '特異性免疫兵工廠', 'P.155–165', 's5-3', '圖 5－12　體液免疫',
     '後天性免疫由 T 細胞與 B 細胞執行，具專一性、多樣性與記憶性。抗原呈現細胞把抗原片段與 MHC 分子結合呈現在細胞表面，活化輔助 T 細胞；輔助 T 細胞分泌細胞介素，啟動胞毒 T 細胞的細胞媒介免疫（誘發受感染細胞凋亡），並協助 B 細胞分化為漿細胞分泌抗體，進行體液免疫。記憶細胞使再次感染時反應更快更強，這正是疫苗的原理。',
     ['5-3.1 後天性免疫的活化', '5-3.2 細胞媒介免疫', '5-3.3 體液免疫', '5-3.4 免疫記憶性與疫苗'],
     ['抗原與 MHC', '輔助 T 細胞', '胞毒 T 細胞', '漿細胞與抗體', '記憶細胞', '疫苗']),
   U('5-4', '免疫失調與排斥', '免疫調控與醫療探索坊', 'P.166–170', 's5-4', '圖 5－15　過敏反應',
     '免疫系統失調會引發疾病：過敏是對花粉、塵蟎等過敏原的過度反應，再次接觸時肥大細胞釋出組織胺而產生症狀；自體免疫疾病是免疫系統攻擊自身細胞，如第一型糖尿病、全身性紅斑狼瘡、類風溼性關節炎；免疫缺失症則使防禦能力下降，如 HIV 感染引起的後天免疫缺乏症候群。器官移植時，受贈者會依 MHC 差異排斥外來器官，需配對組織並使用免疫抑制劑。',
     ['5-4.1 過敏', '5-4.2 自體免疫疾病', '5-4.3 免疫缺失症', '5-4.4 器官移植時的排斥作用'],
     ['過敏原', '組織胺', '第一型糖尿病', '紅斑狼瘡', '免疫缺失症', '移植排斥']),
  ],
  labs=[
   L('5-1', '藉由ABO血型的鑑定探討抗原與抗體反應的基本模式', '血型凝集抗原抗體實驗室', 'P.171–174', 'a5-1', '抗 A、抗 B 血清與血液混合觀察凝集反應',
     '以抗 A 與抗 B 血清分別和自己的血液混合，在低倍顯微鏡下觀察是否凝集，判定 ABO 血型並統計全班結果；再以 10 倍稀釋的抗血清重複實驗，探討抗原與抗體反應的專一性，以及抗體是否需要足夠的量才有明顯作用。'),
  ]),
 dict(n=6, title='生殖', en='Reproduction', a='#be185d', a2='#f472b6', t='#fdf2f8',
  lead='生殖讓生命得以延續。本章認識男性與女性的生殖系統、精子與卵的形成以及女性生殖週期的激素調控，接著觀察受精作用的過程，最後追蹤胚胎從卵裂、著床到懷孕與分娩，並了解產前遺傳篩檢的意義。',
  units=[
   U('6-1', '生殖系統', '生殖器官奧秘館', 'P.178–179', 's6-1', '圖 6－1　人類的生殖系統',
     '男性生殖系統包括睪丸、副睪、輸精管、儲精囊、攝護腺、尿道球腺、陰莖與陰囊：睪丸的細精管產生精子，間質細胞分泌睪固酮，精子在副睪成熟，再與腺體分泌物混合成弱鹼性的精液。女性生殖系統由卵巢、輸卵管、子宮與陰道組成：卵巢內的濾泡分泌動情素，排出的次級卵母細胞進入輸卵管，通常在此受精；子宮是囊胚著床與胚胎發育的場所。',
     ['6-1.1 男性的生殖系統', '6-1.2 女性的生殖系統'],
     ['睪丸與細精管', '間質細胞與睪固酮', '精液', '卵巢與濾泡', '輸卵管', '子宮']),
   U('6-2', '配子的形成', '配子生成與週期演繹驛站', 'P.180–185', 's6-2', '圖 6－2、6－3　精子的生成過程與構造',
     '精原細胞經有絲分裂與分化成為初級精母細胞，經減數分裂產生四個精細胞，再分化為具頭部（頂體與細胞核）、中節（粒線體）與鞭毛的精子。女性在出生前初級卵母細胞即停在減數分裂第一階段前期，青春期後每月通常只有一個完成第一階段而排出次級卵母細胞，受精後才完成第二階段，且細胞質不均等分裂形成極體。卵巢週期與子宮週期受下視丘、腦垂腺與卵巢激素的回饋調控。',
     ['6-2.1 男性的配子形成', '6-2.2 女性的配子形成', '6-2.3 女性的生殖週期'],
     ['精原細胞', '減數分裂', '頂體', '次級卵母細胞與極體', 'FSH 與 LH', '月經週期']),
   U('6-3', '受精過程', '受精機制探索站', 'P.186–187', 's6-3', '圖 6－6　受精過程的示意圖',
     '受精作用通常發生在輸卵管前端。精子先穿過次級卵母細胞外層的放射冠，頭部的頂體分泌頂體蛋白溶解透明帶；當一隻精子的細胞膜與次級卵母細胞融合時，卵母細胞表面結構隨即改變，阻止其他精子進入以避免多重受精。之後次級卵母細胞完成減數分裂第二階段，精核與卵核結合形成受精卵。',
     ['受精作用的過程', '知識補給站：次級卵母細胞外圍的構造'],
     ['放射冠', '透明帶', '頂體蛋白', '避免多重受精', '第二極體', '受精卵']),
   U('6-4', '胚胎發育與懷孕', '生命孕育胚胎發育長廊', 'P.188–192', 's6-4', '圖 6－7　胚胎由受精至著床的主要變化示意圖',
     '受精卵經卵裂形成囊胚，於受精後約 7～10 天著床於子宮內膜；內細胞團分化為外胚層、中胚層與內胚層，胚胎周圍則形成羊膜、絨毛膜、卵黃囊與尿囊四種胚外膜。第 9 週起進入胎兒期，母體與胎兒透過胎盤與臍帶交換氣體、養分與廢物，胎盤也分泌 hCG 等激素維持妊娠。分娩約在第 38～40 週發生；產前遺傳篩檢有助及早發現遺傳疾病。',
     ['6-4.1 胚胎發育', '6-4.2 懷孕與分娩', '6-4.3 產前遺傳篩檢'],
     ['卵裂與囊胚', '著床', '三胚層', '四種胚外膜', '胎盤與臍帶', '產前遺傳篩檢']),
  ],
  labs=[
   L('6-1', '生殖腺與生殖細胞的觀察', '生殖細胞顯微鑑賞坊', 'P.193–198', 'a6-1', '雌鼠卵巢永久玻片中的濾泡',
     '以顯微鏡觀察鼠或兔的睪丸與卵巢永久玻片標本：在細精管由管壁到管腔排列不同發育階段的生殖細胞，推論精子的生成順序；在卵巢中比較不同大小的濾泡、濾泡腔與卵母細胞，推論卵的發育過程。'),
   L('6-2', '代理孕母的倫理與法律問題', '代孕倫理思辨論壇', 'P.199–201', 'a6-2', '試管嬰兒：體外受精並培育胚胎',
     '從試管嬰兒與生殖輔助醫學出發，閱讀印度、泰國代理孕母的案例，比較法國、德國、英國、美國加州等地不同的立法態度，以及我國人工生殖法的立法過程，分組討論代理孕母在倫理、法律、心理與宗教層面的爭議。'),
   L('6-3', '蛙外部形態及內部構造的觀察', '青蛙解剖比較生物學館', 'P.202–211', 'a6-3', '觀察蛙的外部形態並判斷性別',
     '遵循動物實驗 3R 原則，以丁香油溶液麻醉蛙後，先觀察外部形態並判斷雌雄，再依序解剖觀察循環、消化、呼吸、泌尿與生殖系統的構造與相對位置，並與人體的器官系統比較，連結其生理功能與生態習性。'),
  ]),
]

TOTAL_UNITS = sum(len(c['units']) for c in CHAPTERS)
TOTAL_LABS = sum(len(c['labs']) for c in CHAPTERS)

def url(u): return u['file']
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
    o = [HEAD.format(title='翰林版 選修生物（Ⅲ）｜互動教學網站【第二版】',
        desc=f'翰林版高中選修生物Ⅲ（全）六章 {TOTAL_UNITS} 節與 {TOTAL_LABS} 個探討活動的互動教學網頁與教學影片入口（第二版）', theme='#9e1c3f')]
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
    <h1>選修生物（Ⅲ）<span>互動教學網站【第二版】</span></h1>
    <p class="hero-sub">翰林版《選修生物Ⅲ（全）》· 全新優化版課堂闖關與教學影片，包含動物體組成與恆定、循環、消化、呼吸、排泄、感應、防禦與生殖全單元</p>
    <ul class="stats">
''' + f'''      <li><b>{len(CHAPTERS)}</b><span>章</span></li><li><b>{TOTAL_UNITS}</b><span>節正課</span></li><li><b>{TOTAL_LABS}</b><span>個探討活動</span></li><li><b>{TOTAL_UNITS+TOTAL_LABS}</b><span>個優化版網頁</span></li>
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
    <div class="sec-head reveal"><span class="eyebrow">QUICK ACCESS</span><h2>全部優化版互動網頁快速入口</h2><p>老師上課或學生複習時，可直接開啟各節的優化版互動教學網頁（另開新分頁）；教學影片請由章節頁進入。</p></div>
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
    o = [HEAD.format(title=f"第 {n} 章 {c['title']}｜翰林版 選修生物（Ⅲ）【第二版】", desc=E(c['lead']), theme=c['a'])]
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
        <div class="unit-top"><span class="code">{u['code']}</span><span class="web-pill">{ICON_SPARKLE}優化版｜{E(u['web'])}</span><span class="pg-pill">{ICON_BOOK}課本 {u['pages']}</span></div>
        <h2>{E(u['title'])}</h2>
        <a class="intro" href="{url(u)}" target="_blank" rel="noopener" title="開啟「{E(u['web'])}」優化版教學網頁">
          <p>{E(u['intro'])}</p>
          <span class="intro-hint">點選文字即可開啟優化版教學網頁 {ICON_OUT}</span>
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
          <div class="unit-top"><span class="code sm">{l['code']}</span><span class="web-pill">{ICON_SPARKLE}{E(l['web'])}</span><span class="pg-pill">{ICON_BOOK}課本 {l['pages']}</span></div>
          <h3>{E(l['title'])}</h3>
          <a class="intro" href="{url(l)}" target="_blank" rel="noopener"><p>{E(l['intro'])}</p><span class="intro-hint">開啟優化版教學網頁 {ICON_OUT}</span></a>
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
print('Successfully generated v2 site:', TOTAL_UNITS, 'units,', TOTAL_LABS, 'labs')
