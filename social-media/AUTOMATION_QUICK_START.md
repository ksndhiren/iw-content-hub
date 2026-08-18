# Meta Business Suite Automation — Quick Start

Fast reference guide for posting to Instagram, Facebook, and Threads.

---

## Prerequisites

Before running, ensure:

1. ✅ You have credentials (see `META_API_SETUP_GUIDE.md`):
   - `META_PAGE_ACCESS_TOKEN`
   - `META_PAGE_ID`
   - `META_INSTAGRAM_BUSINESS_ACCOUNT_ID`

2. ✅ Credentials are in `.env` file at project root:
   ```bash
   cp .env.example .env
   # Then edit .env with your actual tokens
   ```

3. ✅ All post generator scripts exist:
   - `carousel_comeback.py`
   - `tipcard_cv_mistakes.py`
   - `carousel_star_method.py`
   - `carousel_chatgpt_prompts.py`
   - `carousel_ikigai.py`
   - `carousel_networking.py`
   - `tipcard_confidence.py`
   - `carousel_ai_jobs.py`
   - `carousel_wealth.py`
   - `carousel_campaign_close.py`

---

## Basic Commands

### 1. Test Your Credentials (Do This First!)

```bash
python3 meta_business_suite_automation.py --test-credentials
```

**Expected output:**
```
🔐 Testing Meta API credentials...
✓ Credentials valid!
  Page: Internwise
  Page ID: 123456789
  Instagram Account ID: 987654321
```

**Troubleshooting:**
- If error occurs, review credentials in `.env`
- If token expired, regenerate via Graph API Explorer
- See `META_API_SETUP_GUIDE.md` for detailed help

---

### 2. Preview Campaign (Dry Run)

See what will be posted without actually posting:

```bash
python3 meta_business_suite_automation.py --dry-run
```

**What this does:**
- ✓ Loads all 10 posts
- ✓ Shows image counts for each post
- ✓ Displays captions (preview first 100 chars)
- ✓ Shows scheduled dates/times
- ✓ Lists all platforms (Instagram, Facebook, Threads)
- ✗ Does NOT create any posts
- ✗ Does NOT upload images

**Review output carefully:**
- Check post order and dates
- Verify captions look good
- Confirm platform list is correct
- If changes needed, edit the carousel/tipcard scripts

---

### 3. Schedule Campaign (LIVE)

Post to Instagram, Facebook, and Threads:

```bash
python3 meta_business_suite_automation.py --schedule
```

**What this does:**
- ✓ Generates all images from carousel/tipcard scripts
- ✓ Uploads images to Meta servers
- ✓ Creates carousel/single image posts
- ✓ Schedules posts for specified dates/times (2:00 PM UK time)
- ✓ Saves results to `scheduling_results.json`

**Timeline:**
- Starts immediately
- Each post processes in sequence
- 10 posts × ~3-5 minutes per post = ~30-50 minutes total
- Posts will appear on platforms at scheduled times

**Monitor progress:**
- Watch terminal output for ✓ and ✗ indicators
- Check `scheduling_results.json` for detailed results

---

### 4. Check Results

After scheduling completes, check:

```bash
cat scheduling_results.json | head -50
```

**Expected results:**
```json
{
  "total_posts": 10,
  "scheduled": 10,
  "errors": 0,
  "posts": [
    {
      "post_id": 1,
      "title": "Comeback Carousel",
      "status": "SCHEDULED",
      "scheduled_time": "2026-04-14T14:00:00+01:00",
      "image_count": 5
    },
    ...
  ],
  "error_details": []
}
```

---

## Campaign Schedule

All posts scheduled for **2:00 PM UK time (14:00)**:

| Date | Post | Type | Images |
|------|------|------|--------|
| Mon, Apr 14 | Comeback | Carousel | 5 |
| Tue, Apr 15 | CV Mistakes | Single | 1 |
| Wed, Apr 16 | STAR Method | Carousel | 4 |
| Thu, Apr 17 | ChatGPT Prompts | Carousel | 5 |
| Fri, Apr 18 | Ikigai | Carousel | 3 |
| Mon, Apr 21 | Networking 101 | Carousel | 5 |
| Tue, Apr 22 | Confidence | Single | 1 |
| Wed, Apr 23 | AI Jobs | Carousel | 4 |
| Thu, Apr 24 | Wealth | Carousel | 5 |
| Fri, Apr 25 | Campaign Close | Carousel | 5 |

---

## Manual Posting (X / Twitter, LinkedIn)

For X (Twitter) and LinkedIn, you'll post manually since they're not in the automation script:

### X (Twitter)
Use the captions in `posting_schedule_buffer.md`:
- Tweets are already broken into threads
- Copy each tweet from the file
- Use X's native threading feature
- Post same dates/times for consistency

### LinkedIn
Use the captions in `posting_schedule_buffer.md`:
- Use full LinkedIn caption (longer format)
- Can include image carousel (up to 10 images)
- Post same dates/times for consistency

---

## Troubleshooting

### Error: "Invalid Access Token"
```bash
# Regenerate token:
# 1. Go to https://developers.facebook.com/tools/explorer
# 2. Select your app from dropdown
# 3. Click "Generate Access Token"
# 4. Extend it to long-lived (60 days)
# 5. Update .env with new token
```

### Error: "Instagram Business Account not found"
```bash
# Verify account setup:
# 1. Go to Instagram settings
# 2. Settings → Account → Switch to Business Account
# 3. Link to Facebook page: Settings → Apps and Websites → Instagram Accounts
# 4. Get account ID via Graph API Explorer:
#    GET /{PAGE_ID}/instagram_business_account
```

### Posts not appearing at scheduled time
- Check timezone is correct (+01:00 for UK)
- Meta requires minimum 15 minutes from now to schedule
- Check your Facebook page timezone settings
- Posts should appear on platform at scheduled time

### Some images failed to upload
- Check image dimensions (should be 1080×1080)
- Check file sizes (under 8MB)
- Check image paths are correct
- Try regenerating the carousel script: `python3 carousel_comeback.py`

---

## Advanced: Custom Scheduling

To change post times or dates, edit `meta_business_suite_automation.py`:

```python
# Find this section in PostScheduler class:
POSTS = [
    {
        "post_id": 1,
        "date": "2026-04-14",      # ← Change date here
        "time": "14:00",            # ← Change time here (24-hour format)
        ...
    },
]
```

Then run normally:
```bash
python3 meta_business_suite_automation.py --schedule
```

---

## Advanced: Posting to Specific Platforms Only

To post to only Instagram (skip Facebook and Threads):

```python
# Edit the POSTS configuration:
{
    "platforms": ["instagram"],  # ← Only Instagram
    ...
}
```

Available options:
- `["instagram"]` — Instagram only
- `["facebook"]` — Facebook only
- `["threads"]` — Threads only
- `["instagram", "facebook"]` — Instagram and Facebook
- `["instagram", "facebook", "threads"]` — All platforms (default)

---

## After Posting

1. ✅ Check Instagram/Facebook/Threads to verify posts appeared
2. ✅ Post to X (Twitter) and LinkedIn manually
3. ✅ Monitor engagement metrics for 24-48 hours
4. ✅ Document results in your analytics tracker
5. ✅ Save `scheduling_results.json` for records

---

## Next Steps

1. **Day 1**: Run `--test-credentials` to verify setup
2. **Day 1**: Run `--dry-run` to preview campaign
3. **Day 1**: Review output and make any final adjustments
4. **Day 2**: Run `--schedule` to post live
5. **Daily**: Monitor posts on platforms
6. **Daily**: Post to X/LinkedIn manually

---

## Questions?

See `META_API_SETUP_GUIDE.md` for detailed setup help or API documentation at:
https://developers.facebook.com/docs/instagram-api
