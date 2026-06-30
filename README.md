# AI Influencer Automation

多機协作自動化框架 — 管理 AI Influencer 與 CSD 女團禁毒宣傳的 Instagram / Facebook 內容生成與發佈。

## 機器分工

- **Blue Bull Bot** (WSL): n8n 自動化、IG/FB 發佈、排程任務
- **Red Bull Bot** (5090): AI 圖像/影片生成、重負載運算
- **Green Bull Bot** (Gemini API): 主力圖像生成

## 目錄結構

```
├── n8n-workflows/          # n8n Workflow JSON（可导入）
├── csd-girl-group/
│   ├── scripts/            # 圖像生成腳本
│   └── references_final/   # 角色參考圖
├── configs/
│   └── instagram_api_credentials.template.json
└── docs/
    └── MULTI_MACHINE_SETUP.md
```

## 6 個 AI Influencer

Julia (@julialui628) · Edan (@edanlu.jp) · Piglet (@iampiglet.g) · Olivia (@iamolivia.k) · Andy (@iamandy.em) · Phoenix (@iamphoenix.y)

## CSD AI 女團

冰兒 · 草草 · 小悠 · 可樂

## 安裝

見 [docs/MULTI_MACHINE_SETUP.md](docs/MULTI_MACHINE_SETUP.md)
