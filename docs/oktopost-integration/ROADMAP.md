# Oktopost Integration - Roadmap

## Current State (v1.1 - Feb 2026)

API confirmed working. Scripts operational. Content generation skill active. Manual CSV export step still required.

---

## Phase 1: Foundation (COMPLETE)

- [x] Oktopost API authentication (Basic Auth)
- [x] Create draft messages via API
- [x] List messages by campaign
- [x] Retrieve messages by ID
- [x] `post-to-oktopost.py` — CSV, single post, interactive modes
- [x] `generate-and-post.py` — Template content generation + posting
- [x] `list-oktopost-drafts.sh` — Draft listing
- [x] `oktopost-post-ui.js` — Playwright fallback
- [x] `bluprintx-social-content` skill — Claude content generation (24 posts/week)
- [x] API issue resolved with Oktopost support

## Phase 2: Pipeline Automation (NEXT)

Goal: Remove manual CSV export step. Claude generates -> script posts -> Oktopost receives.

- [ ] **Auto-export from Claude skill to CSV** — Skill outputs structured CSV directly
- [ ] **Direct JSON pipeline** — Skip CSV, pass structured data from skill to posting script
- [ ] **Delete endpoint testing** — Verify if DELETE actually works or needs workaround
- [ ] **Error handling & retry logic** — Handle API rate limits, network errors gracefully
- [ ] **Post verification** — After posting, list by campaign to confirm all drafts created
- [ ] **Duplicate detection** — Check if post already exists before creating

## Phase 3: Asset Integration (HIGH PRIORITY)

Goal: Attach images/visuals to posts automatically.

- [ ] **Media upload endpoint research** — Find how to upload images to Oktopost via API
- [ ] **Canva -> Oktopost pipeline** — Generate visuals in Canva, upload to Oktopost
- [ ] **Bannerbear integration** — Auto-generate branded images from templates
- [ ] **Instagram media attachment** — Auto-attach images (currently using holding image ID)
- [ ] **LinkedIn carousel support** — Upload PDF carousels via API
- [ ] **Asset dimension validation** — Verify dimensions match platform requirements

## Phase 4: Scheduling & Workflow (MEDIUM PRIORITY)

Goal: Move beyond drafts to scheduled posts.

- [ ] **Schedule posts via API** — Set publish date/time when creating messages
- [ ] **Workflow integration** — Assign posts to approval workflows
- [ ] **Status tracking** — Monitor draft -> approved -> published lifecycle
- [ ] **Calendar view sync** — Cross-reference with content calendar
- [ ] **Leader-specific scheduling** — Auto-schedule Mon/Wed/Thu for leaders

## Phase 5: Analytics & Feedback Loop (FUTURE)

Goal: Measure content performance and feed insights back into generation.

- [ ] **Post performance tracking** — Engagement, reach, clicks per post
- [ ] **A/B hook testing** — Track which of the 3 hooks performs best
- [ ] **Content type analysis** — Which formats (single image, carousel, thread) perform best
- [ ] **Platform comparison** — LinkedIn vs Instagram vs Twitter performance
- [ ] **Feedback to Claude skill** — Top-performing patterns inform future content generation
- [ ] **Weekly performance report** — Auto-generated summary of content metrics

## Phase 6: Full Autonomy (FUTURE)

Goal: End-to-end automation with minimal human intervention.

- [ ] **Cron-based weekly generation** — Auto-run content generation every Friday
- [ ] **Auto-posting with human approval gate** — Generate + post as drafts + notify for review
- [ ] **Slack/WhatsApp notifications** — "24 new drafts ready for review"
- [ ] **One-click approval** — Approve all drafts from notification
- [ ] **Trending topic integration** — Adjust content based on current industry trends
- [ ] **Multi-campaign support** — Post to different campaigns based on content type

---

## Dependencies

| Dependency | Status | Impact |
|------------|--------|--------|
| Oktopost API | Active | Core functionality |
| Claude AI (content skill) | Active | Content generation |
| Oktopost credentials | Configured | Auth |
| Canva API/OAuth | Not started | Asset generation (Phase 3) |
| Bannerbear API | Not started | Templated images (Phase 3) |

## Timeline Estimates

| Phase | Target |
|-------|--------|
| Phase 1 | COMPLETE |
| Phase 2 | Next sprint |
| Phase 3 | After Canva/Bannerbear credentials secured |
| Phase 4 | After Phase 2 stable |
| Phase 5 | After sufficient content published |
| Phase 6 | Long-term goal |

---

*Created: 2026-02-20*
