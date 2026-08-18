# Internwise Social Media Campaign — Automation Guide

Complete system for automated posting to Instagram, Facebook, and Threads with manual X/LinkedIn support.

---

## What This Does

This system automates the Internwise "Back & Better" campaign:

- **10 unique posts** across 2 weeks (April 14-25, 2026)
- **3 platforms automated:** Instagram, Facebook, Threads
- **2 platforms manual:** X (Twitter), LinkedIn
- **Scheduling:** All posts at 2:00 PM UK time on scheduled dates
- **Content types:** Carousels (5-slides) and single image tip cards
- **Brand consistent:** All posts use www.internwise.co.uk, brand colors, and approved captions

---

## Files Overview

### Documentation (Start Here!)

| File | Purpose | Read When |
|------|---------|-----------|
| **CAMPAIGN_STATUS.md** | Complete campaign overview and checklist | First thing — see what's ready |
| **META_API_SETUP_GUIDE.md** | Step-by-step credential setup | Before running automation |
| **AUTOMATION_QUICK_START.md** | Command reference and how-to | When ready to post |
| **posting_schedule_buffer.md** | All captions for every platform | When manually posting to X/LinkedIn |

### Code Files

| File | Purpose |
|------|---------|
| `meta_business_suite_automation.py` | Main automation script (Instagram/FB/Threads) |
| `.env.example` | Credentials template (copy to `.env` and fill in) |
| `tools/carousel_*.py` | Post generators (10 total) |
| `campaigns/outputs/` | Generated images and captions (auto-created) |

### Post Generator Scripts

Located in `tools/`:

```
carousel_comeback.py              Post 1 — Comeback (5 slides)
tipcard_cv_mistakes.py             Post 2 — CV Mistakes (1 image)
carousel_star_method.py            Post 3 — STAR Method (4 slides)
carousel_chatgpt_prompts.py        Post 4 — ChatGPT Prompts (5 slides)
carousel_ikigai.py                 Post 5 — Ikigai (3 slides)
carousel_networking.py             Post 6 — Networking (5 slides)
tipcard_confidence.py              Post 7 — Confidence (1 image)
carousel_ai_jobs.py                Post 8 — AI Jobs (4 slides)
carousel_wealth.py                 Post 9 — Wealth (5 slides)
carousel_campaign_close.py         Post 10 — Campaign Close (5 slides)
```

---

## Quick Start (5 Steps)

### 1. Get Credentials (30-45 minutes)

Follow **META_API_SETUP_GUIDE.md** to obtain:
- `META_PAGE_ACCESS_TOKEN` (Facebook Page Access Token)
- `META_PAGE_ID` (Your Facebook Page ID)
- `META_INSTAGRAM_BUSINESS_ACCOUNT_ID` (Your Instagram Business Account ID)

### 2. Configure .env (5 minutes)

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env  # or your editor
```

Fill in the three tokens from Step 1.

### 3. Test Setup (2 minutes)

```bash
python3 meta_business_suite_automation.py --test-credentials
```

Expected output:
```
✓ Credentials valid!
  Page: Internwise
  Page ID: ...
  Instagram Account ID: ...
```

### 4. Preview Campaign (10 minutes)

```bash
python3 meta_business_suite_automation.py --dry-run
```

This shows all 10 posts with captions and image counts — **no posts are created**.

### 5. Schedule Campaign (30-50 minutes)

```bash
python3 meta_business_suite_automation.py --schedule
```

This uploads images, creates posts, and schedules them for the correct dates.

---

## Full Campaign Schedule

All posts scheduled for **2:00 PM UK time**:

| Date | Post | Type |
|------|------|------|
| **Mon, Apr 14** | Comeback | 5-slide carousel |
| **Tue, Apr 15** | CV Mistakes | Single image |
| **Wed, Apr 16** | STAR Method | 4-slide carousel |
| **Thu, Apr 17** | ChatGPT Prompts | 5-slide carousel |
| **Fri, Apr 18** | Ikigai | 3-slide carousel |
| **Mon, Apr 21** | Networking | 5-slide carousel |
| **Tue, Apr 22** | Confidence | Single image |
| **Wed, Apr 23** | AI Jobs | 4-slide carousel |
| **Thu, Apr 24** | Wealth | 5-slide carousel |
| **Fri, Apr 25** | Campaign Close | 5-slide carousel |

---

## What's Automated vs. Manual

### ✅ Automated (Meta Business Suite API)
- Instagram carousels and single images
- Facebook feed posts
- Threads posts
- Image uploads
- Scheduling
- Caption formatting

**Time to automate:** ~40 minutes (credentials setup + scheduling)

### 📝 Manual (API restrictions)
- X (Twitter) — Use `posting_schedule_buffer.md`
- LinkedIn — Use `posting_schedule_buffer.md`

**Time to manual:** ~2-3 minutes per post × 10 posts = ~20-30 minutes total

---

## Command Reference

### Test credentials
```bash
python3 meta_business_suite_automation.py --test-credentials
```

### Preview without posting
```bash
python3 meta_business_suite_automation.py --dry-run
```

### Schedule all posts (LIVE)
```bash
python3 meta_business_suite_automation.py --schedule
```

### Check results
```bash
cat scheduling_results.json
```

---

## File Descriptions

### CAMPAIGN_STATUS.md
Comprehensive checklist of all 10 posts with:
- Content summary for each post
- Which files are involved
- Generation status (all ✓)
- Next steps for the user
- Success metrics to track

**Read this first** to understand what's ready.

### META_API_SETUP_GUIDE.md
Detailed step-by-step guide for:
1. Creating a Meta developer app
2. Adding Instagram Graph API
3. Generating and extending access tokens
4. Getting your Page ID and Instagram Business Account ID
5. Configuring .env file
6. Testing credentials
7. Troubleshooting common errors

**Read this before running automation.**

### AUTOMATION_QUICK_START.md
Quick reference for:
- All commands with expected output
- Campaign schedule table
- Platform-specific notes
- Troubleshooting section
- Advanced customization options

**Keep this handy while running automation.**

### posting_schedule_buffer.md
Raw captions formatted for Buffer, including:
- Full captions for Instagram/Facebook/LinkedIn
- X (Twitter) thread versions (multi-tweet)
- Hashtags for each platform
- Links (www.internwise.co.uk)

**Copy/paste from this when manually posting to X and LinkedIn.**

---

## How It Works

### Image Generation
1. Each post has a Python script (e.g., `carousel_comeback.py`)
2. Script generates 1-5 PNG images (1080×1080 for Instagram)
3. Images are saved to `campaigns/outputs/` directory

### Automation Flow
```
meta_business_suite_automation.py
├── Load credentials from .env
├── For each post (1-10):
│   ├── Run carousel/tipcard generator script
│   ├── Get generated images
│   ├── Upload images to Meta servers
│   ├── Create carousel/single image post
│   ├── Schedule for specified date/time
│   └── Log result to scheduling_results.json
└── Print summary
```

### Scheduling
- Posts are created as "scheduled" items
- Meta platform stores them until scheduled time
- Posts automatically publish at 2:00 PM on their date
- No additional action needed

### Manual Posting (X/LinkedIn)
- Open `posting_schedule_buffer.md`
- Copy caption for desired post
- Post to X/LinkedIn manually at same time as automated posts
- Ensures consistency across all 5 platforms

---

## Troubleshooting

### "Invalid Access Token"
→ See **META_API_SETUP_GUIDE.md** Step 3.3-3.4

### "Instagram Business Account not found"
→ See **META_API_SETUP_GUIDE.md** Step 4.2

### "Posts not appearing at scheduled time"
→ See **AUTOMATION_QUICK_START.md** troubleshooting section

### "Image upload failed"
→ Check image files in `campaigns/outputs/` folder or regenerate with specific script

### Any other error
1. Check `scheduling_results.json` for detailed error message
2. Review relevant documentation file
3. Check that you're using correct credentials
4. Verify .env file is in correct location

---

## Architecture

```
Internwise Social Media System
├── Automation Layer
│   └── meta_business_suite_automation.py (main script)
├── Generation Layer
│   └── tools/ (10 carousel/tipcard generators)
├── Output Layer
│   └── campaigns/outputs/ (generated images & captions)
├── Configuration Layer
│   └── .env (credentials)
└── Documentation Layer
    ├── META_API_SETUP_GUIDE.md
    ├── AUTOMATION_QUICK_START.md
    ├── CAMPAIGN_STATUS.md
    └── posting_schedule_buffer.md
```

---

## Dependencies

Required Python packages:
```
anthropic>=0.25.0    # For potential future AI integration
requests>=2.31.0     # For Meta API calls
python-dotenv>=1.0.0 # For .env file loading
```

Install:
```bash
pip install requests python-dotenv
```

---

## Security Notes

⚠️ **Important:**
- `.env` file contains sensitive tokens — never commit to Git
- `.env` should be in `.gitignore` (already configured)
- Treat tokens like passwords
- Rotate tokens every 30-60 days
- Revoke if exposed

---

## Support & Resources

### Documentation
- **Setup:** See META_API_SETUP_GUIDE.md
- **Commands:** See AUTOMATION_QUICK_START.md
- **Status:** See CAMPAIGN_STATUS.md
- **Captions:** See posting_schedule_buffer.md

### External Resources
- Meta Graph API: https://developers.facebook.com/docs/instagram-api
- Facebook Business Manager: https://business.facebook.com/
- Meta Developer Console: https://developers.facebook.com/apps

---

## Next Actions

1. ✅ **Read:** CAMPAIGN_STATUS.md (understand what's ready)
2. ✅ **Setup:** META_API_SETUP_GUIDE.md (get credentials)
3. ✅ **Configure:** .env file (add your tokens)
4. ✅ **Test:** Run `--test-credentials` command
5. ✅ **Preview:** Run `--dry-run` to see campaign
6. ✅ **Schedule:** Run `--schedule` to post live
7. ✅ **Manual:** Post to X/LinkedIn using posting_schedule_buffer.md
8. ✅ **Monitor:** Track engagement and analytics

---

## Timeline

| Phase | Duration | Action |
|-------|----------|--------|
| **Setup** | 45 min | Get credentials, configure .env, test |
| **Preview** | 10 min | Run --dry-run to check everything |
| **Schedule** | 50 min | Run --schedule to post live |
| **Manual Post** | 30 min | Post to X/LinkedIn manually |
| **Monitor** | 11 days | Track metrics and engagement |

**Total setup:** ~2.5 hours before first post  
**Automation benefit:** 10 hours saved on image uploads and scheduling

---

## Campaign Metrics to Track

After going live, monitor:
- **Reach:** Total people who saw posts
- **Engagement:** Likes, comments, shares
- **Traffic:** Clicks to www.internwise.co.uk
- **Followers:** Growth during campaign
- **Platform Performance:** Which platform performed best?

---

Ready to post? Start with **CAMPAIGN_STATUS.md** → **META_API_SETUP_GUIDE.md** → **AUTOMATION_QUICK_START.md** 🚀
