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
import os, re, json, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import featured_job as fj
from playwright.sync_api import sync_playwright

SEARCH_URL = "https://www.internwise.co.uk/internship-search"
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # "IW social media"
HUB_DIR    = os.environ.get(
    "FEATURED_HUB_DIR",
    os.path.abspath(os.path.join(BASE_DIR, "..", "iw-content-hub"))
)
FEATURED_JSON = os.path.join(HUB_DIR, "data", "featured.json")
IMAGES_DIR    = os.path.join(HUB_DIR, "images", "featured")

# JS that returns the featured-job cards as {href, lines[]} using the validated
# "Featured Jobs heading -> section -> .list-job" structure.
# Read each field from its own element in the card (robust to line-order quirks):
#   .job-title h4     -> title      .job-title p       -> company
#   .job-descriptions > p           -> sector/fields
#   .job-descriptions .descriptions p (x3, any order)  -> location / type / date
EXTRACT_JS = r"""
() => {
  const heading = [...document.querySelectorAll('*')].find(e =>
     /(^|\s)Featured Jobs(\s|$)/.test(e.textContent) &&
     ![...e.children].some(c => /Featured Jobs/.test(c.textContent)));
  if (!heading) return [];
  let cards = [];
  let sec = heading;
  for (let i = 0; i < 6 && sec; i++) {
    const jobs = sec.querySelectorAll(':scope .list-job');
    if (jobs.length) { cards = [...jobs]; break; }
    sec = sec.parentElement;
  }
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


def build_caption(job):
    return (
        f"FEATURED JOB: {_plain(job['title'])} at {_plain(job['company'])}\n\n"
        f"{fj.SECTOR_STYLES[fj._pick_style(job.get('fields',''))][6]}\n\n"
        f"Sector: {_plain(job.get('fields','').split(',')[0])}\n"
        f"Location: {_plain(job.get('location',''))}\n"
        f"Type: {_plain(job.get('jtype',''))}\n"
        f"Duration: {_plain(job.get('duration',''))}\n\n"
        f"Apply now at internwise.co.uk (link in the post)"
    )


def build_hashtags(job):
    style = fj._pick_style(job.get("fields", ""))
    base = {
        "design":    ["#graphicdesign", "#designjobs"],
        "property":  ["#realestate", "#propertyjobs"],
        "marketing": ["#marketingjobs", "#socialmedia"],
        "social":    ["#contentcreator", "#socialmedia"],
        "generic":   ["#internship", "#careers"],
    }[style]
    return base + ["#internship", "#londonjobs", "#graduatejobs"]


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

    fj._load_logos()
    auto_posts, new_count = [], 0

    for job in scraped:
        sid = job["id"]
        if sid in existing_auto:
            auto_posts.append(existing_auto[sid])  # keep graphic + review status
            continue

        # New featured job -> generate a graphic
        post_id = f"job-{sid}"
        out_dir = os.path.join(IMAGES_DIR, post_id)
        os.makedirs(out_dir, exist_ok=True)
        version = re.sub(r"[^a-zA-Z0-9]+", "-", fj.SECTOR_PALETTE_VERSION).strip("-")
        fname = f"{post_id}-{version}.png"
        cfg = fj.build_config(job)
        fj.generate(cfg, os.path.join(out_dir, fname), art_mode="graphic")
        auto_posts.append({
            "id": post_id,
            "sourceId": sid,
            "sourceUrl": job["url"],
            "day": _plain(job["company"]),
            "title": _plain(job["title"]),
            "platform": "Featured Job",
            "format": "Single",
            "slides": [fname],
            "status": "in-review",
            "caption": build_caption(job),
            "hashtags": build_hashtags(job),
        })
        new_count += 1
        print(f"  + generated {post_id} ({cfg['_style']}): {_plain(job['title'])}")

    # Drop images for auto jobs no longer featured
    live_ids = {f"job-{j['id']}" for j in scraped}
    removed = 0
    for sid, p in existing_auto.items():
        if f"job-{sid}" not in live_ids:
            old = os.path.join(IMAGES_DIR, p["id"])
            if os.path.isdir(old):
                shutil.rmtree(old, ignore_errors=True)
            removed += 1

    data["posts"] = manual + auto_posts
    with open(FEATURED_JSON, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Done. New: {new_count}, kept auto: {len(auto_posts)-new_count}, "
          f"removed stale: {removed}, manual preserved: {len(manual)}.")
    print(f"Wrote {FEATURED_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
