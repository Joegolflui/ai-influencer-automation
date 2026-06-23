# AI Influencer Image Generation & Posting Workflow

## 概述

本 workflow 描述從參考照片生成 AI 影像到 Instagram 自動發布的完整流程。

**特點:**
- 使用 Gemini Flash Image API 進行 image-to-image 生成
- 4-shot carousel 系統（90/50/35/28mm）
- 短 prompt（<30 字）保持 face consistency
- 真實奢華品牌與景點
- 可重複使用生成的好圖片

---

## 目錄

1. [Persona 定義](#persona-定義)
2. [參考照片管理](#參考照片管理)
3. [Image Generation Pipeline](#image-generation-pipeline)
4. [Instagram API 設定](#instagram-api-設定)
5. [Posting Workflow](#posting-workflow)
6. [Token 管理](#token-管理)
7. [常見問題與解決](#常見問題與解決)
8. [檔案結構](#檔案結構)

---

## Persona 定義

### Julia Lui (`julia.lui.ig`)
- **類型:** Luxury Travel + 高級時尚
- **參考:** IMG_0077.JPG（正面清晰、長波浪棕色髮、東亞女性）
- **風格:** 奢華旅遊、名牌時尚、陽光海灘
- **地點:** Santorini, Bali, Maldives, Tokyo, Paris
- **品牌:** Chanel, Versace, YSL, Dior

### Edan Lu (`edanlu.jp`)
- **類型:** Luxury Travel + 男士時尚
- **參考:** edan-1.jpg（側面、短髮、東亞男性）
- **風格:** 精緻厨房、陽光海島、都市優雅
- **地點:** Bali, Maldives, Santorini

### Piglet Chu (`iampiglet.g`)
- **類型:** 時尚/旅行
- **設定:** 25歲, 165cm, 49kg, D cup
- **髮型:** 短黑子彈頭
- **風格:** 活潑、可愛、年輕

### Olivia Kam (`iamolivia.k`)
- **類型:** 時尚/旅行
- **設定:** 26歲, 170cm, 52kg, C cup
- **髮型:** 長波浪棕色髮
- **風格:** 優雅、性感、奢華

### Andy Park (`iamandy.em`)
- **類型:** 健身/運動
- **參考:** jaeyoungjoon 風格（肌肉、旅行、陽光）
- **設定:** 韓國男性、健身達人
- **風格:** 健身房、戶外運動、海灘運動

### Phoenix Yi (`iamphoenix.y`)
- **類型:** 健身/運動
- **設定:** 健身達人、户外探險
- **風格:** 力量感、陽剛、户外

---

## 參考照片管理

### 存放位置
```
~/ai-influencer-ref/
  julia/
    julia-main-reference.jpg  # 舊參考（不推薦）
    IMG_0077.JPG              # 首選正面參考
    IMG_0078.JPG              # 備用
    IMG_2311.JPG              # 備用
    IMG_2313.JPG              # 備用
  edan/
    edan-1.jpg                # 首選參考
```

### 選擇標準
- 必須是 **正面照** 或 **半側面**
- 臉部清晰、光線良好
- 背景簡單最佳
- 避免戴眼鏡或遮擋物

---

---

## 👕 品牌服裝圖下載 + Image-to-Image 流程（新增）

> **用戶要求:** 不可只靠文字描述，必須下載真實品牌服裝圖片作為 image-to-image 參考，增加時尚度與真實感。

### Step A: 下載品牌服裝圖

**來源:**
1. 品牌官方網店新品頁（nike.com, adidas.com, gucci.com, prada.com 等）
2. 街頭攝影時裝博主（Instagram / Pinterest）
3. 時尚雜誌網站（Vogue, Elle, Harpers Bazaar）

**`下載方法（瀏覽器）:`**
```python
# 瀏覽品牌網店，下載服裝參考圖
# 例如: Nike 官網 新品頁
browser_navigate("https://www.nike.com/w/new-3n82y")
# 擷取服裝圖片下載
```

**`下載後存放:`**
```
~/ai-influencer-ref/clothing/
  julia/
    versace-swimsuit-001.jpg
    gucci-dress-002.jpg
  edan/
    loro-piana-shirt-001.jpg
    nike-techwear-002.jpg
  ...
```

### Step B: 服裝分析（Clothing Analysis）

**生成前必須做服裝分析！** 用 `vision_analyze` 分析現有已發布圖片，提取：
- 顏色調色板
- 常用布料
- 品牌 signature
- 衣物類型
- 風格模式

**`建立 clothing database:`**
```bash
# 每個 persona 獨立 clothing database
references/clothing-database-{persona}.md
```

### Step C: Image-to-Image 生成（使用服裝參考）

**核心技術: Chain Reference**
```
Shot 1:  Julia face ref + 服裝參考圖  →  生成（確立臉 + 衣服）
Shot 2:  Shot 1 圖片  →  生成（繼承臉 + 衣服）
Shot 3:  Shot 1 圖片  →  生成（繼承臉 + 衣服）
Shot 4:  Shot 1 圖片  →  生成（繼承臉 + 衣服）
```

**API Payload（使用服裝參考）:**
```json
{
  "contents": [{
    "parts": [
      {"inlineData": {"mimeType": "image/jpeg", "data": "JULIA_FACE_REF_B64"}},
      {"inlineData": {"mimeType": "image/jpeg", "data": "CLOTHING_REF_B64"}},
      {"text": "Same exact woman, same face. Wearing this outfit. [scene]. Leica M10, 90mm."}
    ]
  }],
  "generationConfig": {"responseModalities": ["Text", "Image"]}
}
```

**Shots 2-4（用 Shot 1 作為參考）:**
```json
{
  "contents": [{
    "parts": [
      {"inlineData": {"mimeType": "image/jpeg", "data": "SHOT1_B64"}},
      {"text": "Same exact woman, same face, same outfit. [pose/scene change only]. Leica M10, 50mm."}
    ]
  }]
}
```

### 品牌混搭規則（Brand Mix）

| Persona | 奢華品牌 | 街頭/運動品牌 |
|---------|---------|-------------|
| Julia | Chanel, Versace, YSL, Dior, Hermes, LV, Gucci, Prada | Nike, Adidas（點綴） |
| Edan | Loro Piana, Brunello Cucinelli, Ralph Lauren, LV | Nike, Adidas, Off-White（非正式） |
| Piglet | — | **Nike, Adidas 為主** — 街頭風 |
| Olivia | Chanel, Dior, Prada | **Nike, Adidas, Supreme — High-low mix** |
| Andy | — | **Nike, Adidas, Lululemon, Gymshark — 運動風** |
| Phoenix | — | **The North Face, Patagonia, Arc'teryx — 戶外** |

**`每套衣服必須混搭至少 2 個品牌層級！`**

---

## Image Generation Pipeline

### Step 1: 準備 API Key
```python
import yaml
with open(os.path.expanduser("~/.hermes/config.yaml")) as f:
    cfg = yaml.safe_load(f)
API_KEY = cfg["providers"]["gemini"]["api_key"]
```

### Step 2: 轉換參考照片為 base64
```python
import base64
with open("ref.jpg", "rb") as f:
    ref_b64 = base64.b64encode(f.read()).decode()
```

### Step 3: 4-shot Carousel 生成

**每個 Post 生成 4 張圖：**

| Shot | 焦段 | 用途 | 特點 |
|------|------|------|------|
| s1 | 90mm | 特寫 / 頭部 | 臉部最清晰 |
| s2 | 50mm | 半身 | 服裝 + 背景 |
| s3 | 35mm | 全身 | 場景感 |
| s4 | 28mm | 廣角 / 環境 | 環境氛圍 |

**API 請求範例：**
```python
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

payload = {
    "contents": [{
        "parts": [
            {"text": "Image reference for face: must maintain exact face"},
            {"inline_data": {"mime_type": "image/jpeg", "data": ref_b64}},
            {"text": prompt}  # 短 prompt <30 字
        ]
    }],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
}
```

### Step 4: Prompt 範例

**Julia 範例（短、精確）：**
```
90mm portrait of woman in pink floral silk dress under cherry blossom trees, holding matcha cup, Leica camera around neck, soft spring light
```

**Edan 範例：**
```
90mm portrait of man in white linen shirt at infinity pool, Santorini sunset, golden light
```

### Step 5: 保存和呼叫間隔
- 每張圖保存為 `.jpg`
- 每張圖間隔 **5 秒**
- 避免 rate limit

### 輸出目錄結構
```
~/ai-influencer-output/
  {persona}_{group}_{date}/
    p1_s1_90mm.jpg
    p1_s2_50mm.jpg
    p1_s3_35mm.jpg
    p1_s4_28mm.jpg
    p2_s1_90mm.jpg
    ...
```

---

## Instagram API 設定

### 必要資訊
- **App ID:** `1015262304382656`
- **App Secret:** 存於 credentials 檔
- **Page Access Token:** 每個 persona 獨立

### Token 保存位置
```
~/instagram_api_credentials.json
~/edan_instagram_credentials.txt
```

### Token 延期方法
```bash
curl -X GET "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN"
```

### 帳號 ID 映射
```json
{
  "edan_lu": {
    "page_id": "358558740683460",
    "ig_business_id": "17841424208132858",
    "ig_username": "edanlu.jp"
  },
  "julia_lui": {
    "page_id": "17841444402259411",
    "ig_business_id": "17841448618621779",
    "ig_username": "julia.lui.ig"
  }
}
```

---

## Posting Workflow

### Carousel Post 流程

1. **上傳 4 張圖為 media items**
```python
for img_url in images:
    resp = requests.post(f"https://graph.facebook.com/v18.0/{IG_ID}/media",
        params={"image_url": img_url, "is_carousel_item": "true", "access_token": TOKEN})
    media_ids.append(resp.json()["id"])
    time.sleep(1)
```

2. **創建 Carousel**
```python
resp = requests.post(f"https://graph.facebook.com/v18.0/{IG_ID}/media",
    params={
        "caption": caption,
        "media_type": "CAROUSEL",
        "children": ",".join(media_ids),
        "access_token": TOKEN
    })
```

3. **發布**
```python
resp = requests.post(f"https://graph.facebook.com/v18.0/{IG_ID}/media_publish",
    params={"creation_id": carousel_id, "access_token": TOKEN})
```

### Caption 結構
- 中文描述 + emoji
- 問題互動（"你們...?）
- 5-8 個 hashtags
- 中文對話式

---

## Token 管理

### 定期檢查到期日
```python
resp = requests.get(f"https://graph.facebook.com/debug_token",
    params={"input_token": TOKEN, "access_token": f"{APP_ID}|{APP_SECRET}"})
data = resp.json()["data"]
expires_at = data.get("expires_at", 0)
```

### 自動延期
- Token 有效期約 60 天
- 到期前需手動延期
- 使用 long-lived token

---

## 常見問題與解決

### 1. Safety Filter 觸發
**錯誤：** `FinishReason.SAFETY`

**解決：**
- 避免使用明顯性感詞彙（如 `sheer`, `micro bikini`）
- 改用時尚術語（如 `elegant evening gown`, `designer swimwear`）
- 使用品牌名稱替代描述

### 2. Face 不一致
**原因：**
- prompt 太長
- 參考照片質素不好
- 未強調 "exact same face"

**解決：**
- 使用短 prompt（<30 字）
- 在每個 prompt 前加上參考照片
- 使用 "exact same face as reference"

### 3. Rate Limit
**解決：**
- 每次生成間隔 5 秒
- 每個帳號每天限制發文數量

### 4. Carousel 發布失敗
**解決：**
- 確保所有 4 張圖都成功上傳
- 使用 raw.githubusercontent.com 直鏈
- 檢查圖片 URL 可訪問

---

## 檔案結構

```
ai-influencer-automation/
├── README.md
├── docs/
│   ├── WORKFLOW.md              # 本文件
│   ├── instagram-api-setup.md
│   └── instagram-link-guide.md
├── images/
│   ├── julia-lui/
│   │   └── images/
│   │       ├── post1_shot1.jpg ~ post1_shot4.jpg
│   │       ├── post2_shot1.jpg ~ post2_shot4.jpg
│   │       └── ...
│   └── edan-lu/
│       └── images/
├── workflows/
│   ├── kimi-workflow-v7.json
│   └── kimi-workflow-gemini-only.json
└── personas.json                # 所有 persona 定義
```

---

## 重要提醒

1. **永遠使用 Gemini API 於當前設備**（Green Bull Bot），勿用 5090/Red Bull Bot
2. **短 prompt 保持 face consistency**
3. **每個帳號獨立 token**，定期延期
4. **好的圖片可重複使用**，勿浪費
5. **出 post 前先 check face 一致性**
6. **使用品牌名稱避免 safety filter**
7. **定期備份 credentials**

---

*最後更新：2026-06-22*