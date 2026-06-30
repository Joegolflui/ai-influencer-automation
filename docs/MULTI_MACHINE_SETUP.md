# Multi-Machine Setup: Blue Bull Bot + Red Bull Bot

## 分工

| 機器 | 角色 | IP | 負責任務 |
|------|------|-----|---------|
| **Blue Bull Bot** | WSL (Ubuntu) | 100.86.252.119 | n8n 自動化排程、IG/FB 發佈、定時任務、社交媒體管理 |
| **Red Bull Bot** | 5090 GPU | (本地) | AI 圖像生成、視頻處理、大模型推理、重負載運算 |
| **Green Bull Bot** | Gemini API | (雲端) | AI 圖像生成（主力） |

## 同步策略

1. **GitHub Repo (`ai-influencer-automation`)** 作為中央配置庫
2. 兩部機都用 `git pull` 同步最新 workflow / 腳本 / 守則
3. **Token 不放 GitHub**，每台機本地放 `configs/instagram_api_credentials.json`

## 每台機必需檔案

```
ai-influencer-automation/
├── configs/
│   └── instagram_api_credentials.json   # 本地放置，勿上傳
├── n8n-workflows/                       # 從 GitHub pull
├── csd-girl-group/scripts/              # 從 GitHub pull
└── docs/                                # 從 GitHub pull
```

## n8n 同步

- **Blue Bull**: 運行 n8n 主實例 (`tmux` session)
- **Red Bull**: 可選擇性運行 n8n worker 或獨立 instance
- Workflow JSON 导入：手動從 GitHub `n8n-workflows/` 目錄 import

## 安裝步驟

### Blue Bull Bot (WSL)
```bash
cd ~
git clone https://github.com/joegolflui/ai-influencer-automation.git
cd ai-influencer-automation
# 放置 credentials
cp configs/instagram_api_credentials.template.json configs/instagram_api_credentials.json
# 填入真實 token
nano configs/instagram_api_credentials.json
```

### Red Bull Bot (5090)
```bash
cd ~
git clone https://github.com/joegolflui/ai-influencer-automation.git
cd ai-influencer-automation
# 如果需要發佈，同樣放 credentials
# 主要負責圖像/影片生成
```

## 定時同步 (cron)

在兩部機加上：
```bash
# crontab -e
*/30 * * * * cd ~/ai-influencer-automation && git pull origin main
```

## 角色對應表

| 角色 | IG | FB Page ID | 殊对應機器 |
|------|-----|-----------|------------|
| Julia | @julialui628 | 100299989830209 | Blue/Red |
| Edan | @edanlu.jp | 100912816100497 | Blue/Red |
| Piglet | @iampiglet.g | - | Blue/Red |
| Olivia | @iamolivia.k | - | Blue/Red |
| Andy | @iamandy.em | - | Blue/Red |
| Phoenix | @iamphoenix.y | - | Blue/Red |
| 冰兒 | @csd_binger | - | Blue/Red |
| 草草 | @csd_caocao | - | Blue/Red |
| 小悠 | @csd_xiaoyou | - | Blue/Red |
| 可樂 | @csd_kele | - | Blue/Red |
