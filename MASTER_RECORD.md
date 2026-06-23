# AI Influencer Pipeline — 6 IG 帳號完整主記錄

> **最後更新:** 2026-06-23 (品牌指引更新)  
> **記錄目的:** 防止記憶丟失，統一管理6個AI Influencer IG帳號的所有關鍵資訊  
> **⚠️ 安全提醒:** 真實 Access Token 已從本文件移除，請參考下方「憑證存放位置」取得

---

## 📋 帳號總覽

| # | Persona | IG Handle | 類型 | Page ID | IG Business ID | 狀態 | Posts |
|---|---------|-----------|------|---------|----------------|------|-------|
| 1 | **Julia Lui** | `julia.lui.ig` / `julialui628` | Luxury Travel + Fashion | `2093043784340839` | `17841448618621779` | ✅ Active | 16 media |
| 2 | **Edan Lu** | `edanlu.jp` | Luxury Travel + Mens | `358558740683460` | `17841424208132858` | ✅ Active | 7 media |
| 3 | **Piglet Chu** | `iampiglet.g` | Fashion/Travel | `1145207708679853` | `17841424759535803` | ✅ Active | 9 media |
| 4 | **Olivia Kam** | `iamolivia.k` | Fashion/Travel | `1103643402839891` | `17841403006909543` | ✅ Active | 9 media |
| 5 | **Andy Park** | `iamandy.em` | Gym/Fitness | `1093999120474280` | `17841410985341885` | ✅ Active | 9 media |
| 6 | **Phoenix Yi** | `iamphoenix.y` | Gym/Fitness | `1112505928620181` | `17841419378546538` | ✅ Active | 9 media |

---

## 🔐 憑證存放位置

### 主要憑證檔案

| 檔案路徑 | 內容 | 帳號數量 |
|----------|------|----------|
| `~/instagram_api_credentials.json` | Page ID + IG Business ID + Token | 2 (Julia, Edan) — 註：其余4個帳號的 IG Business ID 可直接從 Graph API 查詢 |
| `~/edan_instagram_credentials.txt` | Edan 專用 App ID / App Secret / Token | 1 (Edan) |
| `~/instagram-auto-delete/playwright-scripts/fb_page_tokens_long_lived.txt` | **全部6個帳號**的 Long-Lived Page Access Token + IG Business ID | 6 |
| `~/instagram-auto-delete/playwright-scripts/fb_page_tokens.txt` | 舊版 Token（標記為 FAILED） | 6 |

### App 層級憑證
- **App ID:** `1015262304382656`
- **App Secret:** 存放於 `~/edan_instagram_credentials.txt`

---

## 👤 詳細 Persona 定義

### 1. Julia Lui (`julia.lui.ig`)
- **年齡:** 25
- **族裔:** East Asian
- **風格:** Luxury travel, high fashion, sun-kissed beaches
- **參考照片:** `IMG_0077.JPG`（正面清晰、長波浪棕色髮、東亞女性）
- **參考目錄:** `~/ai-influencer-ref/julia/`
- **地點:** Santorini, Bali, Maldives, Tokyo, Paris, Mallorca
- **品牌:** Chanel, Versace, YSL, Dior, Hermes, **Louis Vuitton, Gucci, Prada**
- **內容支柱:** luxury resorts, designer fashion, scenic destinations, sunset vibes, poolside elegance
- **語調:** elegant, confident, aspirational

### 2. Edan Lu (`edanlu.jp`)
- **年齡:** 28
- **族裔:** East Asian
- **風格:** Refined kitchen, sun-kissed islands, urban elegance
- **參考照片:** `edan-1.jpg`（側面、短髮、東亞男性）
- **參考目錄:** `~/ai-influencer-ref/edan/`
- **地點:** Bali, Maldives, Santorini, Tokyo
- **品牌:** Loro Piana, Brunello Cucinelli, Ralph Lauren Purple Label, **Louis Vuitton, Gucci, Prada**
- **內容支柱:** culinary arts, luxury travel, fine dining, resort life
- **語調:** sophisticated, warm, cultured

### 3. Piglet Chu (`iampiglet.g`)
- **年齡:** 25
- **身高:** 165cm
- **體重:** 49kg
- **三圍:** 89-59-88
- **罩杯:** D cup
- **酒窩:** ✅
- **髮型:** Short black bob with slight mess and layers
- **風格:** Cute, lively, young fashion, **streetwear mix**
- **品牌:** **Nike, Adidas, local street brands, casual designer**
- **內容支柱:** street fashion, cafe hopping, travel vlogs, daily life
- **語調:** playful, energetic, cute

### 4. Olivia Kam (`iamolivia.k`)
- **年齡:** 26
- **身高:** 170cm
- **體重:** 52kg
- **三圍:** 86-60-89
- **罩杯:** C cup
- **酒窩:** ❌
- **髮型:** Long wavy brown hair
- **臉型:** Refined V-face, soft jawline
- **眼睛:** Large clear eyes with watery shine
- **嘴唇:** Naturally plump pink lips
- **膚色:** Extremely fair porcelain skin
- **風格:** Elegant, sexy, luxury, **high-low fashion mix**
- **品牌:** **Chanel, Dior, Nike, Adidas, Prada, streetwear labels**
- **內容支柱:** travel adventures, fashion looks, sexy elegant style, luxury lifestyle, beach and resort
- **語調:** elegant, subtly seductive, confident

### 5. Andy Park (`iamandy.em`)
- **年齡:** 27
- **族裔:** Korean
- **風格參考:** `jaeyoungjoon`（肌肉、旅行、陽光、勵志）
- **風格:** Muscular, travel, sunshine, aspirational, **athleisure**
- **品牌:** **Nike, Adidas, Lululemon, Gymshark, Under Armour**
- **內容支柱:** gym workouts, outdoor fitness, beach sports, protein lifestyle
- **語調:** confident, energetic, motivational

### 6. Phoenix Yi (`iamphoenix.y`)
- **年齡:** 28
- **風格:** Powerful, rugged, outdoor adventure
- **品牌:** **The North Face, Patagonia, Arc'teryx, Nike, outdoor brands**
- **內容支柱:** strength training, mountain climbing, extreme sports, wilderness
- **語調:** strong, adventurous, fearless

---

## 📁 關鍵檔案結構

```
~/ai-influencer-automation/           # GitHub repo
├── README.md
├── CHANGELOG.md
├── personas.json                     # 全部6個 persona 定義
├── MASTER_RECORD.md                  # ← 本文件
├── docs/
│   ├── WORKFLOW.md                   # 完整圖片生成+發布流程
│   ├── instagram-api-setup.md        # Graph API 設定指南
│   └── instagram-link-guide.md       # IG 連結 FB 專頁指南
├── images/
│   ├── julia-lui/images/             # 16 media × 4 shots = 64 images
│   ├── edan-lu/images/               # 7 media × 4 shots = 28 images
│   ├── iampiglet.g/                  # 9 media × 部分 shots
│   ├── iamolivia.k/                  # 9 media × 部分 shots
│   ├── iamandy.em/                   # 9 media × 部分 shots
│   └── iamphoenix.y/                 # 9 media × 部分 shots
└── workflows/
    ├── kimi-workflow-v7.json
    └── kimi-workflow-gemini-only.json

~/ai-influencer-ref/                  # 參考照片
├── julia/
│   ├── IMG_0077.JPG                  # Julia 首選參考
│   ├── IMG_0078.JPG
│   ├── IMG_2311.JPG
│   └── IMG_2313.JPG
└── edan/
    └── edan-1.jpg                    # Edan 首選參考

~/instagram-auto-delete/              # 自動化工具（獨立項目）
├── playwright-scripts/
│   ├── fb_page_tokens_long_lived.txt # ⚠️ 6個帳號 Long-Lived Tokens
│   └── fb_page_tokens.txt            # 舊版（FAILED）
└── ...

~/instagram_api_credentials.json      # Julia + Edan API 憑證
~/edan_instagram_credentials.txt      # Edan 專用憑證
~/instagram_cleanup.log               # iamolivia.k 取消追蹤日誌
```

---

## 🛠️ 技術架構

### 圖片生成
- **API:** Gemini Flash Image API (image-to-image)
- **模型:** `gemini-2.5-flash`
- **裝置:** Green Bull Bot（當前 macOS 設備）
- **Prompt 規則:** <30 字，短而精確

### 發布系統
- **API:** Instagram Graph API + Facebook Graph API
- **格式:** 4-shot Carousel（90/50/35/28mm）
- **Token 類型:** Long-Lived Page Access Token
- **Token 有效期:** ~60 天，需定期延期

### 自動化工具
- **n8n Workflows:** `kimi-workflow-v7.json`, `kimi-workflow-gemini-only.json`
- **Playwright 腳本:** 用於 IG 網頁自動化（登入、取消追蹤等）
- **API Server:** Express + Playwright (Port 3001)

---

## 👕 品牌指引（Brand Guidelines）

> **核心原則:** 不限於傳統高級品牌，必須混搭平民/街頭品牌，增加真實感與時尚度。

### 高級品牌（Luxury）
Chanel, Versace, YSL, Dior, Hermes, Louis Vuitton, Gucci, Prada, Loro Piana, Brunello Cucinelli, Ralph Lauren Purple Label

### 平民/街頭品牌（Streetwear / Casual）
Nike, Adidas, Lululemon, Gymshark, Under Armour, The North Face, Patagonia, Arc'teryx, Supreme, Stüssy, local street brands

### 時裝拼搭源泉
- 街頭攝影時裝（Street-style photography）
- 品牌官方網店新品頁（e.g. nike.com, adidas.com, gucci.com）
- 時尚博主/網紅穿搭分享
- 實景拍攝：咖啡廳、街角、海灘、健身房

### 每個 Persona 品牌定位
| Persona | 主力品牌 | 可混搭平民品牌 |
|---------|-----------|----------------|
| Julia | Chanel, Versace, YSL, Dior, Hermes, LV, Gucci, Prada | ✅ 可添加街頭元素 |
| Edan | Loro Piana, Brunello Cucinelli, Ralph Lauren, LV, Gucci, Prada | ✅ 非正式場合可穿街頭 |
| Piglet | Nike, Adidas, local street, casual designer | ✅ 以街頭為主 |
| Olivia | Chanel, Dior, Prada, streetwear labels | ✅ High-low mix 重點 |
| Andy | Nike, Adidas, Lululemon, Gymshark, Under Armour | ✅ 運動風為主 |
| Phoenix | The North Face, Patagonia, Arc'teryx, Nike | ✅ 戶外功能為主 |

---

## ⚠️ 重要規則

1. **永遠使用 Gemini API 於當前設備**（Green Bull Bot），**禁止**使用 5090/Red Bull Bot
2. **短 Prompt（<30 字）** 保持 face consistency
3. **每個帳號獨立 Token**，定期延期
4. **重用高質量圖片**，避免浪費 generation
5. **發布前檢查 face 一致性**
6. **使用真實品牌名稱** 避免 safety filter
7. **必須混搭平民/街頭品牌** 增加時尚真實感，不可只用傳統高級品牌
8. **定期備份憑證** 到安全位置
9. **n8n workflow 必須用 Kimi Code / Claude Code / Codex 生成**，禁止手寫 JSON

---

## 📊 目前進度

| 帳號 | 已發 Posts | 已發 Images | 狀態 |
|------|-----------|-------------|------|
| Julia Lui | 16 media | 68 | ✅ 運作中 |
| Edan Lu | 7 media | 28 | ✅ 運作中 |
| Piglet Chu | 9 media | 16 | ✅ 運作中 |
| Olivia Kam | 9 media | 16 | ✅ 運作中 |
| Andy Park | 9 media | 16 | ✅ 運作中 |
| Phoenix Yi | 9 media | 16 | ✅ 運作中 |

**總計:** 50 posts / 160 images / 6 of 6 active

---

## 🔗 相關連結

- **GitHub Repo:** `https://github.com/Joegolflui/ai-influencer-automation`
- **參考帳號分析:** `~/ai_influencer_research.md`
- **Instagram Graph API Explorer:** `https://developers.facebook.com/tools/explorer/`

---

*本文件由 Hermes Agent 於 2026-06-23 自動生成，目的為防止記憶丟失。*
