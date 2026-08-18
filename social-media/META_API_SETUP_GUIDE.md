# Meta Business Suite API — Setup Guide

This guide walks you through obtaining the credentials needed to automate posting to Instagram, Facebook, and Threads using the Meta Business Suite API.

---

## Step 1: Create/Access Your Meta Developer App

### 1.1 Visit Meta Developers
- Go to https://developers.facebook.com/
- Log in with your Facebook account (must be an admin/developer of your page)

### 1.2 Create an App (if needed)
- Click **My Apps** → **Create App**
- Choose **Business** as the app type
- Fill in app details:
  - **App Name**: "Internwise Social Automation" (or your preference)
  - **App Contact Email**: Your email
  - **Purpose**: Select relevant business category
  - Click **Create App**

### 1.3 Select Your App
- If you already have an app, click **My Apps** and select it
- You'll see your **App ID** in the dashboard (save this)

---

## Step 2: Add Instagram Graph API Product

### 2.1 Add Product
- In your app dashboard, click **Add Product**
- Search for **Instagram Graph API**
- Click **Set Up** (this may say "Next" or similar)

### 2.2 Configure Permissions
- You should now see Instagram Graph API in your dashboard
- Go to **Settings** → **Basic**
- Scroll down to find permissions and set these scopes:

```
instagram_business_management
pages_manage_metadata
pages_read_engagement
pages_manage_posts
pages_read_user_content
```

---

## Step 3: Generate Your Page Access Token

### 3.1 Connect Your Facebook Page
- Go to **Tools** → **Graph API Explorer** (or navigate to https://developers.facebook.com/tools/explorer)
- In the top-right, make sure you've selected your app from the dropdown

### 3.2 Generate Token
- Click the **User token** dropdown (top-right of Graph API explorer)
- Select **Generate Access Token** (this will be a **User Token**)
- You'll be prompted to select permissions; ensure the ones from Step 2.2 are checked
- A token will appear in the text field

### 3.3 Extend Token Expiration (Recommended)
- By default, user tokens expire in ~1 hour
- To get a long-lived token (60 days), you'll need to swap it:

**Using Terminal/cURL:**
```bash
curl -i -X GET "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
```

Replace:
- `YOUR_APP_ID` - From your app dashboard
- `YOUR_APP_SECRET` - Go to **Settings** → **Basic** and find "App Secret" (click Show)
- `YOUR_SHORT_LIVED_TOKEN` - The token you just generated

The response will include a long-lived token in the format:
```json
{
  "access_token": "very_long_token_string...",
  "token_type": "bearer"
}
```

**Save this long-lived token** — this is your `META_PAGE_ACCESS_TOKEN`

### 3.4 Alternative: Generate Permanent Page Access Token
If you want a token that doesn't expire, generate it from your **Business Manager**:
- Go to https://business.facebook.com/
- Select your Business
- Go to **Settings** → **Users**
- Find your admin user
- Under the user, click **View** → **Admin Token**
- Copy the token

---

## Step 4: Get Your Page ID and Instagram Business Account ID

### 4.1 Get Page ID
**Option A - Graph API Explorer:**
```
1. In Graph API Explorer, change dropdown from "User" to "Page"
2. Select your Facebook page
3. Run: GET /me
4. In response, find "id" field
```

**Option B - Facebook Page Settings:**
```
1. Go to your Facebook page
2. Go to Settings → Page Info
3. Scroll down to find "Page ID"
```

Save this as `META_PAGE_ID`

### 4.2 Get Instagram Business Account ID
**Using Graph API Explorer:**

1. In Graph API explorer, use your page token
2. Run: `GET /{PAGE_ID}/instagram_business_account`
3. Response will include your Instagram Business Account ID
4. Save as `META_INSTAGRAM_BUSINESS_ACCOUNT_ID`

**Alternative - Direct from Instagram:**
1. Go to https://www.instagram.com/accounts/login/
2. Log in to your Internwise Instagram account
3. Go to Settings → Account → Business Account Info
4. Find your Business Account ID (or use the API method above, which is more reliable)

---

## Step 5: Configure Your .env File

In the project root (`/Users/abhishekutkarsha/Claude/IW social media/`), create or edit `.env`:

```env
# Meta Business Suite API
META_PAGE_ACCESS_TOKEN=your_long_lived_page_access_token_here
META_PAGE_ID=your_facebook_page_id_here
META_INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_business_account_id_here

# Optional: Other platforms (for future expansion)
# THREADS_API_TOKEN=your_threads_token
# LINKEDIN_ACCESS_TOKEN=your_linkedin_token
```

**Important:** 
- Never commit `.env` to Git
- Keep your tokens secure — don't share them
- If a token is leaked, regenerate it immediately

---

## Step 6: Test Your Credentials

Run the test command:

```bash
cd /Users/abhishekutkarsha/Claude/IW\ social\ media/

python3 meta_business_suite_automation.py --test-credentials
```

Expected output:
```
🔐 Testing Meta API credentials...
✓ Credentials valid!
  Page: Internwise
  Page ID: 123456789
  Instagram Account ID: 987654321
```

If you see errors, verify:
1. All three tokens are correct and have not expired
2. Your page is linked to your Instagram Business Account
3. Your Instagram account is in Business mode (not Creator mode)

---

## Step 7: Run Your First Campaign (Dry Run)

Test posting without actually creating posts:

```bash
python3 meta_business_suite_automation.py --dry-run
```

This will:
- Load all 10 posts
- Show what would be posted
- Display image counts, captions, and scheduled times
- **NOT create any actual posts**

---

## Step 8: Schedule All Posts

Once you've verified everything works, schedule the full campaign:

```bash
python3 meta_business_suite_automation.py --schedule
```

This will:
1. Upload all carousel/single images
2. Create posts with captions
3. Schedule for the correct dates/times (2:00 PM UK time)
4. Post to Instagram, Facebook, and Threads
5. Save results to `scheduling_results.json`

---

## Troubleshooting

### Error: "Invalid Access Token"
- Verify token hasn't expired (user tokens expire in 60 days, extend if needed)
- Regenerate via Graph API Explorer

### Error: "User does not have permission"
- Ensure you're an admin/developer of the Facebook page
- Check that you have all required permissions granted
- Regenerate token with full scopes selected

### Error: "Instagram Business Account not found"
- Verify your Instagram account is switched to Business mode:
  - Instagram app → Settings → Account type
  - Should show "Business Account"
- Make sure your FB page is linked to your IG account:
  - Instagram Settings → Apps and Websites → Connected Apps
  - Ensure your FB page is listed

### Error: "Image upload failed"
- Check image file paths are correct
- Verify images are PNG format and under 8MB
- Check image dimensions are 1080x1080 (or valid carousel dimensions)

### Posts not appearing on schedule
- Meta API scheduling has a minimum wait time (~15 minutes from now)
- Don't schedule posts in the past
- Check timezone is correct (should be +01:00 for UK/BST)

---

## Permissions Explained

| Permission | Purpose |
|-----------|---------|
| `instagram_business_management` | Manage Instagram business account content |
| `pages_manage_metadata` | Edit page info (name, description, etc.) |
| `pages_read_engagement` | Read post insights and engagement |
| `pages_manage_posts` | Create, edit, delete page posts |
| `pages_read_user_content` | Read user-generated content on page |

---

## Rate Limits

Meta API has rate limits:
- **Tier 1**: 200 requests per hour for new apps
- **Tier 2**: 10,000 requests per day after 7 days
- **Tier 3**: Higher limits after app review

Our automation script:
- Uploads 10 posts with ~25-30 images total = ~50 API calls
- Safe within limits for any tier
- Includes 0.5-second delays between uploads to be conservative

---

## Security Best Practices

1. **Never share tokens** — treat like passwords
2. **Rotate tokens regularly** — regenerate every 30 days
3. **Use long-lived tokens** — minimum 60 days
4. **Monitor app activity** — check Settings → Active Sessions
5. **Revoke unused tokens** — in Settings → Permissions
6. **Keep .env secure** — add to .gitignore (should already be there)

---

## Next Steps

1. ✅ Follow steps 1-5 above to get credentials
2. ✅ Run `--test-credentials` to verify setup
3. ✅ Run `--dry-run` to preview campaign
4. ✅ Run `--schedule` to post to Instagram, Facebook, and Threads
5. ✅ Monitor posts on platforms (they'll appear at scheduled time)
6. ✅ Manually post to X (Twitter) and LinkedIn (as per your workflow)

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review API responses in terminal output
3. Check `scheduling_results.json` for detailed error logs
4. Visit https://developers.facebook.com/docs/instagram-api for API documentation
