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
import story_card
from playwright.sync_api import sync_playwright

SEARCH_URL = "https://www.internwise.co.uk/internship-search"
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # "IW social media"
HUB_DIR    = os.environ.get(
    "FEATURED_HUB_DIR",
    os.path.abspath(os.path.join(BASE_DIR, "..", "iw-content-hub"))
)
FEATURED_JSON = os.path.join(HUB_DIR, "data", "featured.json")
PUBLISHED_JSON = os.path.join(HUB_DIR, "data", "featured_published.json")
IMAGES_DIR    = os.path.join(HUB_DIR, "images", "featured")

# JS that returns ONLY featured-job cards. The search page now renders one job
# results list and marks promoted listings with an orange "Featured" badge. Use
# that badge as the source of truth, with the older tinted-card rule as fallback.
# Read each field from its own element in the card (robust to line-order quirks):
#   .job-title h4     -> title      .job-title p       -> company
#   .job-descriptions > p           -> sector/fields
#   .job-descriptions .descriptions p (x3, any order)  -> location / type / date
EXTRACT_JS = r"""
() => {
  const isTransparent = c => !c || c === 'transparent' || c === 'rgba(0, 0, 0, 0)';
  const txt = el => el ? el.textContent.replace(/\s+/g, ' ').trim() : '';
  const own = el => el ? [...el.childNodes].filter(n => n.nodeType === 3)
                         .map(n => n.textContent).join(' ').replace(/\s+/g, ' ').trim() : '';
  const hasFeaturedBadge = card => [...card.querySelectorAll('*')].some(el =>
     /^Featured$/i.test(txt(el)));

  // Current Internwise search page: Tailwind `<article>` cards with an orange
  // "Featured" badge. Keep the old `.list-job` selector as fallback for older
  // deployments because the cloud job may run across a frontend rollout.
  const cards = [...document.querySelectorAll('article, .list-job')].filter(card =>
     hasFeaturedBadge(card) || (card.matches('.list-job') && !isTransparent(getComputedStyle(card).backgroundColor)));
  if (!cards.length) return [];

  return cards.map(card => {
    const a = card.querySelector('.job-title h4 a') || card.querySelector('h3 a[href*="/job/"]') || card.querySelector('a[href*="/job/"]');
    const title = txt(card.querySelector('.job-title h4')) || txt(card.querySelector('h3')) || txt(a);
    const company = txt(card.querySelector('.job-title p')) || txt(card.querySelector('h3 + p'));
    const fields = own(card.querySelector('.job-descriptions > p')) || txt([...card.querySelectorAll('p')].at(-1));
    const descLines = [...card.querySelectorAll('.job-descriptions .descriptions p')].map(own);
    if (!descLines.length) {
      const meta = [...card.querySelectorAll('p.flex span')]
        .map(el => own(el) || txt(el))
        .filter(Boolean);
      descLines.push(...meta);
    }
    return {
      href: a ? a.getAttribute('href') : '',
      title,
      company,
      fields,
      descLines,
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
        pg.wait_for_selector("article, .list-job", timeout=45000)
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


def _job_key(title, company):
    """Stable title+company key so re-listed jobs do not re-enter the queue."""
    t = fj._sanitize(fj.strip_year(title or "")).replace("&amp;", "and").lower()
    c = fj._sanitize(company or "").replace("&amp;", "and").lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t); c = re.sub(r"[^a-z0-9 ]", " ", c)
    t = re.sub(r"\s+", " ", t).strip(); c = re.sub(r"\s+", " ", c).strip()
    return f"{t}|{c}"


def load_published():
    if not os.path.exists(PUBLISHED_JSON):
        return {"ids": set(), "keys": set()}
    try:
        with open(PUBLISHED_JSON) as f:
            d = json.load(f)
        return {"ids": set(str(x) for x in d.get("publishedIds", [])),
                "keys": set(str(x) for x in d.get("publishedKeys", []))}
    except Exception:
        return {"ids": set(), "keys": set()}


def is_published(pub, sid, title="", company=""):
    if str(sid) in pub["ids"]:
        return True
    return _job_key(title, company) in pub["keys"] if (title or company) else False


def caption_context(job):
    """Role-specific caption body. Must not repeat the graphic hook or mention
    the employer name."""
    style = fj.pick_style_for_job(job)
    mapping = {
        "events": "Good if you want to build proof around research, speaker outreach, agenda planning, and keeping a commercial event moving from idea to delivery.",
        "sales": "Good if you want evidence of confidence, client communication, lead handling, and turning conversations into measurable outcomes.",
        "marketing": "Good if you want practical proof across content, campaign thinking, social channels, and the weekly rhythm of brand growth.",
        "social": "Good if you want hands-on examples of planning, shooting, editing, publishing, and learning what makes people stop scrolling.",
        "finance": "Good if you want detail-led experience with numbers, process, reporting, and the kind of accuracy employers look for early.",
        "property": "Good if you want commercial exposure, client-facing work, site detail, and a clearer story around how property decisions are made.",
        "tech": "Good if you want practical evidence of problem-solving, tools, delivery, and the habits that make junior technical applicants easier to trust.",
    }
    return mapping.get(style, "Good if you want a real workplace example you can later turn into CV bullets, interview stories, and clearer proof of fit.")


def build_caption(job):
    role = _plain(job["title"])
    sector = _plain(job.get("fields", "").split(",")[0])
    location = _plain(job.get("location", ""))
    jtype = _plain(job.get("jtype", ""))
    duration = _plain(job.get("duration", ""))
    url = job["url"]
    return (
        f"FEATURED INTERNSHIP: {role}\n\n"
        f"{caption_context(job)}\n\n"
        f"Field: {sector}\n"
        f"Location: {location}\n"
        f"Format: {jtype}\n"
        f"Length: {duration}\n\n"
        f"Apply here: {url}"
    )


def build_hashtags(job):
    style = fj.pick_style_for_job(job)
    base = {
        "design":    ["#graphicdesign", "#designjobs"],
        "tech":      ["#techjobs", "#internship"],
        "social":    ["#contentcreator", "#socialmedia"],
        "property":  ["#realestate", "#propertyjobs"],
        "finance":   ["#financejobs", "#accounting"],
        "pr":        ["#publicrelations", "#communications"],
        "media":     ["#mediajobs", "#contentcreator"],
        "sales":     ["#salesjobs", "#businessdevelopment"],
        "marketing": ["#marketingjobs", "#socialmedia"],
        "events":    ["#eventjobs", "#hospitalityjobs"],
        "generic":   ["#internship", "#careers"],
    }.get(style, ["#internship", "#careers"])
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

    published = load_published()
    print(f"Published ledger: {len(published['ids'])} ids, {len(published['keys'])} keys")

    fj._load_logos()
    auto_posts, new_count = [], 0

    for job in scraped:
        sid = job["id"]
        if is_published(published, sid, job.get("title", ""), job.get("company", "")):
            old = os.path.join(IMAGES_DIR, f"job-{sid}")
            if os.path.isdir(old):
                shutil.rmtree(old, ignore_errors=True)
            print(f"  - skipped already published job-{sid}: {_plain(job.get('title', ''))}")
            continue
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
        graphic_path = os.path.join(out_dir, fname)
        fj.generate(cfg, graphic_path, art_mode="graphic")
        story_card.make_story(graphic_path, os.path.join(out_dir, "story.png"))
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
    live_ids = {f"job-{j['id']}" for j in scraped
                if not is_published(published, j["id"], j.get("title", ""), j.get("company", ""))}
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
