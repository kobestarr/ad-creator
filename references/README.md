# Reference Library

## BluprintX Content References
Location: `/root/clawd/references/bluprintx/`

### Core Files
- `SKILL.md` - Claude content generation skill
- `references/bluprintx_brand_info.md` - Brand overview, mission, pillars
- `references/bluprintx_tone_hook_strategy.md` - Outcome-first hooks, messaging rules
- `references/social_media_best_practices_2025.md` - Platform specs, best practices

### Leadership Voices
- `references/phil_petrelli_tone_analysis.md` - Phil's voice (CRO, American English)
- `references/at_trzaskus_tone_analysis.md` - AT's voice (VP Marketing, American English)
- `references/lee_hackett_tone_analysis.md` - Lee's voice (CEO, British English)

## How to Add New References

1. Upload files to: `/root/clawd/references/bluprintx/references/`
2. Update this README with new file descriptions
3. Scripts will auto-load from this location

## Usage in Scripts

```python
# Load brand info
with open('/root/clawd/references/bluprintx/references/bluprintx_brand_info.md') as f:
    brand_info = f.read()

# Load Lee's voice
with open('/root/clawd/references/bluprintx/references/lee_hackett_tone_analysis.md') as f:
    lee_voice = f.read()
```

---

*Last Updated: 2026-02-01*
