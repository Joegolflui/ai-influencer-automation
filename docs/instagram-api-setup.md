# Instagram Graph API 設定指南

## 需要什麼？
- Facebook 個人帳號
- Instagram Business/Creator Account（非個人帳號）

---

## Step 1: 登入 Facebook Developer
前往：https://developers.facebook.com/apps/
- 按「使用 Facebook 帳號繼續」

## Step 2: 建立 App
1. 按「建立應用程式」
2. 選「其他」
3. 填寫應用程式名稱：`AI Influencer Auto Post`
4. 按「建立應用程式」

## Step 3: 加入 Instagram Graph API
1. 左側面板按「新增產品」
2. 找 Instagram Graph API 按「設定」
3. 追蹤指示完成

## Step 4: 獲取 Access Token
1. 去 Instagram Graph API -> API 設定
2. 按「產生存取權杖」
3. 選擇要管理的 Instagram 帳號
4. 複製 Token（長串英文）

## Step 5: 設定 n8n 環境變數
將 Token 貼到 n8n 環境變數：
- 變數名：`INSTAGRAM_ACCESS_TOKEN`
- 值：你複製的 Token

---

## 測試 API
Token 獲取後，可用以下 URL 測試：
```
https://graph.instagram.com/me?fields=id,username&access_token=你的TOKEN
```

## 重要提醒
- Token 有有效期，需定期更新
- Instagram 帳號必須是 Business 或 Creator 類型
- 個人帳號無法使用 Graph API
