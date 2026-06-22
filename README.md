# AI Influencer Instagram Automation

Complete Instagram automation pipeline for AI influencers using Gemini Flash Image API + Instagram Graph API.

## 🚀 Features

- **6 AI Personas** - Julia, Edan, Piglet, Olivia, Andy, Phoenix
- **4-shot Carousel** - 90/50/35/28mm focal length system
- **Image-to-Image** - Gemini Flash API with face consistency
- **Auto-Posting** - Instagram Graph API carousel posts
- **Token Management** - Automatic token tracking and renewal
- **Image Reuse** - Cache and reuse high-quality generated images

## 📝 Documentation

| File | Description |
|------|-------------|
| `docs/WORKFLOW.md` | **Complete image generation & posting workflow** |
| `docs/instagram-api-setup.md` | How to get Instagram Graph API token |
| `docs/instagram-link-guide.md` | Link IG professional account to Facebook Page |
| `personas.json` | All 6 persona definitions |
| `CHANGELOG.md` | Update history |

## 👥 Personas

| Name | IG Handle | Type | Status |
|------|-----------|------|--------|
| **Julia Lui** | julia.lui.ig | Luxury Travel/Fashion | ✅ 17 posts |
| **Edan Lu** | edanlu.jp | Luxury Travel/Mens | ✅ 7 posts |
| **Piglet Chu** | iampiglet.g | Fashion/Travel | 🔲 Pending |
| **Olivia Kam** | iamolivia.k | Fashion/Travel | 🔲 Pending |
| **Andy Park** | iamandy.em | Gym/Fitness | 🔲 Pending |
| **Phoenix Yi** | iamphoenix.y | Gym/Fitness | 🔲 Pending |

## 🖼️ Image Structure

```
images/
├── julia-lui/
│   └── images/
│       ├── post1_shot1.jpg ~ post1_shot4.jpg   # Santorini Pool
│       ├── post2_shot1.jpg ~ post2_shot4.jpg   # Santorini White
│       └── ... post17_shot1.jpg ~ post17_shot4.jpg
└── edan-lu/
    └── images/
        ├── post1_shot1.jpg ~ post1_shot4.jpg   # Bali Cooking
        └── ...
```

## 🔧 Workflows

| File | Description |
|------|-------------|
| `workflows/kimi-workflow-v7.json` | Full n8n workflow with analytics |
| `workflows/kimi-workflow-gemini-only.json` | Simplified Gemini-only version |

## 🔐 APIs Used

- **Gemini Flash Image API** - Image generation (image-to-image)
- **Instagram Graph API** - Auto-posting carousels
- **Facebook Graph API** - Token management

## ⚠️ Important Rules

1. **Always use Gemini API on current device** (Green Bull Bot) - never use 5090/Red Bull Bot
2. **Short prompts (<30 words)** for best face consistency
3. **Use brand names** to avoid safety filters
4. **Check face consistency** before posting
5. **Reuse good images** - don't waste generations
6. **Extend tokens** before expiry (60-day cycle)

## 📈 Stats

- **Total Posts:** 24
- **Total Images:** 96
- **Personas Active:** 2/6
- **Last Updated:** 2026-06-22

---

*Repository: https://github.com/Joegolflui/ai-influencer-automation*
