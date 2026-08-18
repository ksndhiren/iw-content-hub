# Internwise — social analytics

Tools to pull real performance data so the content plan is driven by what works,
not guesses.

## Instagram insights (`fetch_ig_insights.py`)

Pulls per-post IG insights (reach, impressions/views, saves, shares, likes,
comments) for the **linked** Internwise IG Business account and writes
`ig_insights.csv`.

### 1. Get an access token (one time, ~5 min)

You do this part — **the token never gets pasted into chat or committed.**

1. Go to **developers.facebook.com/apps** → **Create app** → choose **Business** →
   name it (e.g. "Internwise Analytics"). Skip this if you already have an app.
2. Open the **Graph API Explorer**: developers.facebook.com/tools/explorer
3. Top right: select your app.
4. Click **Add permissions** and tick all of:
   - `instagram_basic`
   - `instagram_manage_insights`
   - `pages_read_engagement`
   - `pages_show_list`
5. Click **Generate Access Token** → log in → when asked, grant access to the
   **Internwise** Business portfolio, the **Facebook Page**, and the **linked
   Instagram** account (the "Facebook + Instagram" asset, not the standalone IG).
6. Copy the token string.

### 2. Save the token locally

Create the file `analytics/ig_token.txt` and paste **only** the token into it:

```
EAAG...your-token...ZDZD
```

Keep this file private. Do not share it, screenshot it, or commit it.

### 3. Run

```bash
python3 analytics/fetch_ig_insights.py
```

Output: `analytics/ig_insights.csv`. Hand that CSV over and I'll run the audit.

### Token lifetime
The Explorer token is **short-lived (~1–2 hours)** — fine for a one-off pull. For
the recurring weekly loop, swap it for a **long-lived (~60-day)** token:

```
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=<APP_ID>&client_secret=<APP_SECRET>&fb_exchange_token=<SHORT_TOKEN>
```

Paste the returned `access_token` into `ig_token.txt` instead.

## Note on link clicks
Instagram's API does **not** expose per-post outbound link clicks for organic feed
posts. To measure clicks-to-site from IG (and every other platform), we use
**UTM-tagged links + GA4** — that's the universal traffic tracker. This CSV covers
the reach/engagement side, which is the current bottleneck.
