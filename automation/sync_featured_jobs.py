"""
sync_featured_jobs.py

Scrapes the live "Featured Jobs" section of the Internwise internship-search page,
generates a portrait job-ad graphic for each NEW featured job (dedup by the job's
numeric id in its /job/<id>/ URL), and updates the content-hub's data/featured.json.

Design: HOLD FOR REVIEW. This script only writes files + images into the hub repo.
It never commits or pushes. In the cloud routine, a wrapper commits the result to a
branch and opens a PR for a human to approve before it reaches the live dashboard.

- Auto-managed entries carry "sourceId"; hand-made demo entries (no sourceId) are
  preserved untouched. Auto entries no longer featured are dropped.
- Graphics use the self-contained 3D-cluster mode (no Pexels, no rembg needed).

Run:  python3 sync_featured_jobs.py            (writes into ../../iw-content-hub)
      FEATURED_HUB_DIR=/path/to/hub python3 sync_featured_jobs.py
"""
import os, re, json, sys, shutil, datetime
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
# Point the generator at the vendored brand assets before importing it.
os.environ.setdefault("IW_BRANDING_DIR", os.path.join(_HERE, "branding"))
os.environ.setdefault("IW_FONTS_DIR",    os.path.join(_HERE, "assets", "fonts"))
import featured_job as fj
from playwright.sync_api import sync_playwright

SEARCH_URL = "https://www.internwise.co.uk/internship-search"
# The hub repo root is the parent of this automation/ folder.
HUB_DIR    = os.environ.get("FEATURED_HUB_DIR", os.path.dirname(_HERE))
FEATURED_JSON = os.path.join(HUB_DIR, "data", "featured.json")
IMAGES_DIR    = os.path.join(HUB_DIR, "images", "featured")

# JS that returns ONLY the featured-job cards. Featured jobs are the star-marked
# ones with the grey card background (rgba(38, 77, 126, 0.1)); the general job
# listings below have a transparent background. We select .list-job cards whose
# background is not transparent, which excludes non-featured listings.
# Read each field from its own element in the card (robust to line-order quirks):
#   .job-title h4     -> title      .job-title p       -> company
#   .job-descriptions > p           -> sector/fields
#   .job-descriptions .descriptions p (x3, any order)  -> location / type / date
EXTRACT_JS = r"""
() => {
  const isTransparent = c => !c || c === 'transparent' || c === 'rgba(0, 0, 0, 0)';
  const cards = [...document.querySelectorAll('.list-job')].filter(card =>
     !isTransparent(getComputedStyle(card).backgroundColor));
  if (!cards.length) return [];
  const txt = el => el ? el.textContent.replace(/\s+/g, ' ').trim() : '';
  // Only the element's OWN text nodes - skips nested icon/schema spans that would
  // otherwise leak tokens like "GeographicReference" into the location.
  const own = el => el ? [...el.childNodes].filter(n => n.nodeType === 3)
                         .map(n => n.textContent).join(' ').replace(/\s+/g, ' ').trim() : '';
  return cards.map(card => {
    const a = card.querySelector('.job-title h4 a') || card.querySelector('a[href*="/job/"]');
    return {
      href:      a ? a.getAttribute('href') : '',
      title:     txt(card.querySelector('.job-title h4')),
      company:   txt(card.querySelector('.job-title p')),
      fields:    own(card.querySelector('.job-descriptions > p')),
      descLines: [...card.querySelectorAll('.job-descriptions .descriptions p')].map(own),
    };
  });
}
"""

# A description line is a DATE, a TYPE(+duration), or (by elimination) the LOCATION.
_DATE_RE = re.compile(r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}', re.I)
_TYPE_RE = re.compile(r'(part[-\s]?time|full[-\s]?time|internship|placement|permanent|contract|temporary|apprentice)', re.I)


def scrape_featured():
    """Return a list of job dicts from the live featured section."""
    jobs = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        pg.goto(SEARCH_URL, wait_until="domcontentloaded", timeout=60000)
        # The job cards are rendered client-side; wait for them explicitly rather
        # than networkidle (the site keeps long-lived connections open).
        pg.wait_for_selector(".list-job", timeout=45000)
        pg.wait_for_timeout(1500)  # let the featured section settle
        raw = pg.evaluate(EXTRACT_JS)
        br.close()

    seen = set()
    for item in raw:
        href = item.get("href", "") or ""
        m = re.search(r"/job/(\d+)/", href)
        if not m:
            continue
        jid = m.group(1)
        if jid in seen:
            continue
        seen.add(jid)

        title   = (item.get("title") or "").strip()
        company = (item.get("company") or "").strip()
        fields  = (item.get("fields") or "").strip()
        if not title:
            continue  # can't render a job with no title

        # Classify the 3 description lines by pattern rather than fixed position.
        location, type_raw = "", ""
        for d in item.get("descLines", []):
            d = (d or "").strip()
            if not d or _DATE_RE.search(d):
                continue
            if _TYPE_RE.search(d):
                type_raw = d
            elif not location:
                location = d
        jtype, duration = _split_type(type_raw)

        jobs.append({
            "id": jid,
            "url": href if href.startswith("http") else "https://www.internwise.co.uk" + href,
            "title": title, "company": company, "fields": fields,
            "location": location, "jtype": jtype, "duration": duration,
        })
    return jobs


def _split_type(raw):
    """'Part-time (1 - 3 months)' -> ('Part-time', '1 - 3 months')"""
    raw = re.sub(r"\s+", " ", raw or "").strip()
    m = re.match(r"(.*?)\s*\((.*?)\)\s*$", raw)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return raw, ""


def _plain(s):
    """Sanitized plain text (no HTML entities) for JSON fields."""
    return fj._sanitize(s).replace("&amp;", "&")


def _clean_title(s):
    """Plain title with any trailing year in parens removed."""
    return fj.strip_year(_plain(s))


def build_captions(job):
    """Featured caption: the sector hook line, the location, and the apply link to
    the job's own page. No title, no company. Same clean format across platforms
    (Threads removed - users cross-post from Instagram)."""
    loc  = _plain(job.get("location", ""))
    hook = fj.SECTOR_STYLES[fj._pick_style(job.get("fields", ""))][6]
    url  = job["url"]
    text = f"{hook}\n\n\U0001F4CD {loc}\n\nApply now \U0001F449 {url}"
    return {"ig-fb": text, "linkedin": text, "x": text}


# One sector-specific hashtag per style, used across the platform sets below.
_STYLE_TAG = {
    "design": "#designjobs", "tech": "#techjobs", "social": "#socialmediajobs",
    "property": "#realestatejobs", "finance": "#financejobs", "pr": "#prjobs",
    "media": "#mediajobs", "sales": "#salesjobs", "marketing": "#marketingjobs",
    "generic": "#internships",
}

def build_hashtags_by_platform(job):
    """Different hashtag sets per platform (broad on IG, professional on LinkedIn,
    tight on X). Threads removed."""
    tag = _STYLE_TAG[fj._pick_style(job.get("fields", ""))]
    return {
        "ig-fb":    ["#internship", "#londonjobs", tag, "#hiring", "#graduatejobs"],
        "linkedin": ["#hiring", "#internship", tag, "#careers"],
        "x":        [tag, "#hiring"],
    }


def load_featured():
    if not os.path.exists(FEATURED_JSON):
        return {"id": "featured", "label": "Featured Jobs", "posts": []}
    with open(FEATURED_JSON) as f:
        return json.load(f)


def main():
    print(f"Hub: {HUB_DIR}")
    scraped = scrape_featured()
    print(f"Scraped {len(scraped)} featured jobs: " + ", ".join(j['id'] for j in scraped))
    if not scraped:
        print("No featured jobs found - leaving featured.json untouched.")
        return 0

    data = load_featured()
    existing = data.get("posts", [])
    manual   = [p for p in existing if not p.get("sourceId")]
    existing_auto = {p["sourceId"]: p for p in existing if p.get("sourceId")}

    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    fj._load_logos()
    auto_posts, new_count = [], 0

    for job in scraped:
        sid = job["id"]
        if sid in existing_auto:
            p = existing_auto[sid]
            p.setdefault("addedAt", now_iso)  # backfill so sort order is stable
            auto_posts.append(p)              # keep graphic + review status
            continue

        # New featured job -> generate a graphic
        post_id = f"job-{sid}"
        out_dir = os.path.join(IMAGES_DIR, post_id)
        os.makedirs(out_dir, exist_ok=True)
        fname = f"{post_id}.png"
        cfg = fj.build_config(job)
        fj.generate(cfg, os.path.join(out_dir, fname), art_mode="graphic")
        captions = build_captions(job)
        htags    = build_hashtags_by_platform(job)
        auto_posts.append({
            "id": post_id,
            "sourceId": sid,
            "sourceUrl": job["url"],
            "addedAt": now_iso,
            "day": _plain(job["company"]),
            "title": _clean_title(job["title"]),
            "platform": "Featured Job",
            "format": "Single",
            "slides": [fname],
            "status": "in-review",
            "caption": captions["ig-fb"],            # default / fallback
            "hashtags": htags["ig-fb"],              # default / fallback
            "captions": captions,                    # per-platform text
            "hashtagsByPlatform": htags,             # per-platform tags
        })
        new_count += 1
        print(f"  + generated {post_id} ({cfg['_style']}): {_clean_title(job['title'])}")

    # Drop images for auto jobs no longer featured
    live_ids = {f"job-{j['id']}" for j in scraped}
    removed = 0
    for sid, p in existing_auto.items():
        if f"job-{sid}" not in live_ids:
            old = os.path.join(IMAGES_DIR, p["id"])
            if os.path.isdir(old):
                shutil.rmtree(old, ignore_errors=True)
            removed += 1

    # Newest first: most recently added, then by numeric job id.
    auto_posts.sort(key=lambda p: (p.get("addedAt", ""), int(p.get("sourceId", "0") or 0)),
                    reverse=True)
    data["posts"] = auto_posts + manual
    with open(FEATURED_JSON, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Done. New: {new_count}, kept auto: {len(auto_posts)-new_count}, "
          f"removed stale: {removed}, manual preserved: {len(manual)}.")
    print(f"Wrote {FEATURED_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
