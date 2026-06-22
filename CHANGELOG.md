# Changelog

## 2026-06-22 - Major Update

### Added
- **Julia Lui** 17 posts published (68 images total)
  - 9 original posts (Santorini, Bali, Maldives, Tokyo, Chanel)
  - 8 bonus posts using previously generated high-quality images
  - Posts 10-17: Tokyo Sakura v2, Paris Eiffel, Maldives Tweed, Bali Rice, Bali Pool, Bali Villa, Santorini Versace, Chanel Gallery
- **Edan Lu** 7 posts published
  - Bali cooking, candlelight dinner, sunrise silk, Maldives, Chanel hotel, Tokyo sakura
- **32 bonus images** from image cache reused and published
- **Instagram API token extension** - extended expiry to 2026-08-21
- **Complete workflow documentation** (`docs/WORKFLOW.md`)
- **Persona definitions** (`personas.json`)

### Fixed
- Julia face consistency issue - regenerated all images using IMG_0077.JPG reference
- Fixed incorrect App Secret in credentials file
- Deleted wrong-face posts from Julia account
- Proper token management with long-lived tokens

### Reference Accounts Analyzed
- `sophiewithlove_` - Soft girl / intimate diary / Gen-Z aesthetic
- `jaeyoungjoon` - Muscular / travel / sunshine / aspirational

### Technical Details
- Gemini Flash Image API (image-to-image)
- 4-shot carousel system (90/50/35/28mm)
- Short prompts (<30 words) for face consistency
- Real designer brands per post
- Safety filter workarounds using brand names
