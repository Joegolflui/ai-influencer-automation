# Blue Bull Bot 環境設置指南

> **目標：** 在 WSL2 (Blue Bull Bot) 上完整配置 rclone + Google Drive + Instagram API 自動化環境
>
> **機器：** DESKTOP-AR0HRRN WSL Ubuntu (joegolflui / emofficemba)
> **Tailscale IP：** 100.86.252.119

---

## 目錄

1. [rclone 安裝 + Google Drive 配置](#1-rclone-安裝--google-drive-配置)
2. [Instagram API 憑證設置](#2-instagram-api-憑證設置)
3. [Google Drive 同步腳本](#3-google-drive-同步腳本)
4. [Kimi Code CLI 安裝](#4-kimi-code-cli-安裝)
5. [DNS 修復](#5-dns-修復)

---

## 1. rclone 安裝 + Google Drive 配置

### 1.1 安裝 rclone

```bash
curl -s https://rclone.org/install.sh | sudo bash
rclone version
```

### 1.2 準備 Service Account JSON

將 `google_drive_service_account.json` 放在：
```
/home/joegolflui/google_drive_service_account.json
```

權限設為 `600`：
```bash
chmod 600 ~/google_drive_service_account.json
```

### 1.3 配置 rclone

創建 `~/.config/rclone/rclone.conf`：

```ini
[gdrive]
type = drive
scope = drive
service_account_file = /home/joegolflui/google_drive_service_account.json
```

### 1.4 測試連線

```bash
rclone lsd gdrive:
```

如果看到文件夾列表 = 連線成功！

### 1.5 共享文件夾設定

Service Account 領域獨立於個人帳戶，需要手動分享：

1. 在 Google Drive 網頁版選擇目標文件夾
2. 按右鍵 → **分享**
3. 加入 Service Account email：
   ```
   drive-sa-242742@my-project-manus-488620.iam.gserviceaccount.com
   ```
4. 設為 **Viewer** 或 **Editor**

---

## 2. Instagram API 憑證設置

### 2.1 傳送憑證檔案

將 `instagram_api_credentials.json` 放在：
```
/home/joegolflui/instagram_api_credentials.json
```

權限：
```bash
chmod 600 ~/instagram_api_credentials.json
```

### 2.2 JSON 格式範例

```json
{
  "accounts": {
    "julialui628": {
      "ig_business_id": "178414...",
      "fb_page_id": "...",
      "access_token": "EAA...",
      "token_expires": "2026-07-30"
    }
  }
}
```

> **提醒：** Token 有效期通常為 60 天，記得定期更新！

---

## 3. Google Drive 同步腳本

### 3.1 從 Drive 下載到本機

建立 `~/scripts/sync_csd_from_drive.sh`：

```bash
#!/bin/bash
set -e

LOCAL_DIR="/home/joegolflui/csd_girl_group"
REMOTE_DIR="gdrive:CSD_Girl_Group/03_generated"

echo "Syncing CSD Girl Group from Google Drive..."
mkdir -p "$LOCAL_DIR"
rclone sync "$REMOTE_DIR" "$LOCAL_DIR" --progress
echo "Done! Files in: $LOCAL_DIR"
```

### 3.2 從本機上傳到 Drive

建立 `~/scripts/sync_csd_to_drive.sh`：

```bash
#!/bin/bash
set -e

LOCAL_DIR="/home/joegolflui/csd_girl_group"
REMOTE_DIR="gdrive:CSD_Girl_Group/03_generated"

echo "Syncing CSD Girl Group to Google Drive..."
rclone sync "$LOCAL_DIR" "$REMOTE_DIR" --progress
echo "Done!"
```

### 3.3 快速 Alias

在 `~/.bashrc` 加入：

```bash
alias csd_from_drive="bash /home/joegolflui/scripts/sync_csd_from_drive.sh"
alias csd_to_drive="bash /home/joegolflui/scripts/sync_csd_to_drive.sh"
```

載入：
```bash
source ~/.bashrc
```

### 3.4 常用 rclone 指令

```bash
# 列出 Drive 文件夾
rclone lsd gdrive:

# 上傳單個文件
rclone copy local_file.png "gdrive:Green Bull Bot/毒女團/01-冰兒/"

# 同步整個目錄（本機 → 雲端）
rclone sync ~/csd_girl_group "gdrive:Green Bull Bot/毒女團"

# 下載整個目錄（雲端 → 本機）
rclone sync "gdrive:Green Bull Bot/毒女團" ~/csd_girl_group
```

---

## 4. Kimi Code CLI 安裝

### 4.1 下載安裝

```bash
# 安裝到 ~/.local/bin
curl -fsSL https://cdn.kimi.com/coding/cli/install.sh | bash

# 加入 PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 4.2 登入

```bash
kimi login
```

按指示在瀏覽器打開授權鏈接。

### 4.3 測試

```bash
kimi --version
kimi -p "Say hello"
```

### 4.4 配置檔位置

```
~/.kimi-code/config.toml          # 主配置
~/.kimi-code/credentials/         # 憑證
~/.kimi-code/logs/                # 日誌
```

---

## 5. DNS 修復

WSL2 + Tailscale 導致 DNS 被覆蓋為 `100.100.100.100`，影響外部 API 連線。

### 5.1 臨時修復

```bash
sudo bash -c 'echo nameserver 8.8.8.8 > /etc/resolv.conf && echo nameserver 1.1.1.1 >> /etc/resolv.conf'
```

### 5.2 永久修復（選擇性）

創建 `/etc/wsl.conf`：

```ini
[network]
generateResolvConf = false
```

然後在 `/etc/resolv.conf` 手動加入：

```
nameserver 8.8.8.8
nameserver 1.1.1.1
```

重啛 WSL：
```bash
wsl --shutdown
```

---

## 快速參考表

| 指令 | 功能 |
|------|------|
| `rclone lsd gdrive:` | 列出 Drive 文件夾 |
| `csd_from_drive` | 從 Drive 下載 CSD 圖片 |
| `csd_to_drive` | 上傳 CSD 圖片到 Drive |
| `kimi -p "prompt"` | Kimi AI 執行指令 |
| `rclone copy local remote` | 單向複製檔案 |
| `rclone sync local remote` | 雙向同步（小心會刪除！） |

---

## 故障排除

### 問題：`couldn't fetch token: invalid_request`

**解決：** Token 過期，需要重新授權。用 `rclone config reconnect gdrive:` 或更新 token JSON。

### 問題：`directory not found`

**解決：** Service Account 沒有該文件夾的讀取權限。在 Google Drive 網頁版分享文件夾給 Service Account email。

### 問題：`fetch failed` (kimi login)

**解決：** DNS 問題或 IPv6 連線失敗。先修復 DNS，或設定：
```bash
export NODE_OPTIONS='--dns-result-order=ipv4first'
```

---

*Last updated: 2026-06-30*
