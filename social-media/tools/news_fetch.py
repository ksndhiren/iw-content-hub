"""News lane - live RSS fetcher (stdlib only, no feedparser dependency).

Pulls recent UK employment / job-market / early-career news from a curated set
of RSS feeds, filters to relevant + recent items, de-dupes against a log, and
returns items shaped for `news_card.render_news()`.

Run standalone to preview what today would pull:
    python3 tools/news_fetch.py
"""
import os, re, sys, json, html, time, datetime, urllib.request, urllib.error
import xml.etree.ElementTree as ET


def _utcnow():
    """Naive UTC "now". Feed dates are parsed naive, so the freshness comparison in
    fetch() has to stay naive too; datetime.utcnow() itself is deprecated."""
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
LOG  = os.path.join(BASE, "content", "news_used.json")

# Curated UK employment / labour-market / early-career feeds.
# Kept broad on purpose - some sites bot-block RSS (403) or move URLs (404), so we
# over-provision reliable feeds and keyword-filter for relevance downstream.
FEEDS = [
    ("Personnel Today",    "https://www.personneltoday.com/feed/"),
    ("The Guardian",       "https://www.theguardian.com/money/work-and-careers/rss"),
    ("The Guardian",       "https://www.theguardian.com/education/students/rss"),
    ("BBC Business",       "https://feeds.bbci.co.uk/news/business/rss.xml"),
    ("BBC Education",      "https://feeds.bbci.co.uk/news/education/rss.xml"),
    # NB: US/international feeds (e.g. Indeed Hiring Lab US) are intentionally
    # excluded - Internwise news is UK job-market ONLY. See _is_uk() below.
    ("FE News",            "https://www.fenews.co.uk/feed/"),
    ("WonkHE",             "https://wonkhe.com/feed"),      # NB: no trailing slash - /feed/ 308s
    ("GOV.UK",             "https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=department-for-work-pensions"),
    # Backups: the cloud runner is sometimes CDN-blocked on the feeds above
    # (Personnel Today 403s from GitHub IPs), so keep spare UK supply in rotation.
    ("GOV.UK Education",   "https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=department-for-education"),
    ("The Guardian",       "https://www.theguardian.com/education/universities/rss"),
    ("BBC UK",             "https://feeds.bbci.co.uk/news/uk/rss.xml"),
]

# Bias toward items relevant to a job-board / early-career audience.
KEYWORDS = re.compile(
    r"\b(job|jobs|hiring|hire|graduate|intern|internship|apprentice|"
    r"recruit|recruitment|vacan|employ|labour market|labor market|"
    r"skills|wage|salary|pay|workforce|early careers?|entry.?level|"
    r"talent|unemploy|redundan|remote work|hybrid work|gen z)\b", re.I)

CORE_JOB_MARKET = re.compile(
    r"\b(job|jobs|hiring|hire|graduate|intern|internship|apprentice|"
    r"recruit|recruitment|vacan|employ|labour market|labor market|"
    r"skills|workforce|early careers?|entry.?level|talent|unemploy|"
    r"redundan|remote work|hybrid work|gen z)\b", re.I)
INTERNWISE_NEWS_CANON = re.compile(
    r"\b(students?|graduates?|grad\b|interns?|internships?|"
    r"apprentices?|apprenticeships?|early careers?|entry.?level|school.?leavers?|"
    r"universit(?:y|ies)|college|job applicants?|candidates?|"
    r"jobseekers?|interview\w*|applicat\w+|applicants?|"
    r"cv|cover letter|portfolio|employability|work experience|placements?|"
    r"first job|first role|career starter|"
    # young-worker framing is core early-careers news even without the words
    # above ("Young bearing brunt of hiring slump") - keep it in the canon.
    r"young (?:people|workers?|jobseekers?|adults)|under.?25s?)\b", re.I)
ACTIONABLE_EARLY_CAREER = re.compile(
    r"\b(appl(?:y|ies|ied|ying)|applicat\w+|applicants?|interview\w*|cv|cover letter|"
    r"portfolio|skills?|training|work experience|placements?|apprenticeships?|"
    r"job.?ready|employability|graduate earnings|tuition fees|university costs|"
    r"student (?:loans?|debt|finance)|job contracts?|non.?compete|candidates?|"
    r"hiring|recruit\w*|vacanc\w+|graduate (?:scheme|schemes|jobs?|roles?))\b", re.I)
WORK_PAY_CONTEXT = re.compile(
    r"\b(payroll|minimum wage|living wage|pay rise|pay deal|grading|"
    r"staff|worker|workers|employee|employees|employer|"
    r"union|industrial action|public sector|council|nhs|dwp|hmrc)\b", re.I)
LIFESTYLE_MONEY = re.compile(
    r"\b(boyfriend|girlfriend|husband|wife|partner|dating|marriage|"
    r"relationship|couple|family finances|personal finance|mortgage|"
    r"inheritance|divorce)\b", re.I)
NON_NEWS_FLUFF = re.compile(
    r"\b(cartoon|crossword|quiz|recipe|horoscope|oil prices?|diesel cost|"
    r"fuel prices?|costly oil|energy bills?)\b", re.I)
ORG_PR_OR_LOCAL_ONLY = re.compile(
    r"\b(launches new brand platform|brand platform|webinar|register now|"
    # corporate M&A / funding is trade news, never a reader takeaway
    r"acquires?|acquisition|acquired by|merger|merges with|takeover bid|"
    r"shortlisted for .*award|national award|award shortlist|"
    r"strategic partnership|partner(?:s|ship) with|"
    r"regional workforce summit|conference to bring industry together|"
    r"appoints .*managing director|promotion of .*leader|"
    r"students lend their skills|shine at .*festival|recognised for driving growth)\b", re.I)
# Single-institution PR: a named college/university/school promoting its own
# event, building or students ("Kirklees College celebrates graduates", "Exeter
# College's new £5.3m centre opens"). Internwise does not promote institutions,
# so these are rejected even when they mention students or skills. Sector-wide
# stories ("Colleges face pay and funding issues") name no institution and pass.
NAMED_INSTITUTION = re.compile(
    r"\b(?:[A-Z][\w'&.-]+ ){1,4}(?:College|University|Academy|School|Institute|Campus)\b"
    r"|\b(?:University|College) of (?:[A-Z][\w'&.-]+ ?){1,3}")
INSTITUTION_PROMO = re.compile(
    r"\b(celebrat\w+|graduat(?:es|ion) (?:ceremony|celebration)|ceremony|"
    r"opens?|opening|officially opened|unveil\w*|launch(?:es|ed)?|"
    r"new (?:centre|center|campus|building|facility|hub|wing)|centre opens|"
    r"open (?:day|evening)|awards? (?:evening|night|ceremony)|"
    r"anniversary|welcomes?|visit(?:s|ed)?|showcase\w*|take ?over|"
    r"students? (?:shine|impress|win|scoop)|graduates? (?:after|from)|"
    r"placement propels|dream job|success stor\w+)\b", re.I)
EXCLUDED_JOB_TYPES = re.compile(
    r"\b(plumb(?:er|ers|ing)|gas engineer|heating engineer|boiler repair|"
    r"electrician|carpenter|joiner|bricklayer|roofer|scaffold(?:er|ing)|"
    r"construction trade|manual trades?|butcher|butchery|engineering profession)\b", re.I)
# Sport is fine as an industry (marketing, media, analytics, events roles) but
# stories about playing careers - footballers, academies, homegrown talent -
# are not Internwise news. Rejected unless an off-pitch job angle is present.
SPORT_PLAYING = re.compile(
    r"\b(football\w*|soccer|rugby|cricket\w*|premiership|premier league|"
    r"championship side|athletes?|players?|squads?|homegrown|first.?team|"
    r"academy (?:players?|graduates?|products?)|scouts?|transfer window)\b", re.I)
SPORT_INDUSTRY_JOB = re.compile(
    r"\b(sports? (?:marketing|media|business|industry|management|science|"
    r"analytics?|journalism|events?)|marketing|media|analyst|journalis\w+|"
    r"physio\w*|commercial|ticketing|events team|broadcast\w*)\b", re.I)

# --- UK-ONLY GUARD -----------------------------------------------------------
# Internwise news is about the UK job market only. Even UK publications carry the
# odd US/overseas story, so every candidate is screened: an item is dropped when
# it clearly concerns another country UNLESS it also carries a clear UK signal.
_FOREIGN_CI = re.compile(
    r"\b(united states|america\w*|canad\w+|australia\w*|new zealand|"
    r"india\b|indian|chin(?:a|ese)|japan\w*|german\w*|france|french|"
    r"spain|spanish|itali\w+|silicon valley|wall street|federal reserve|"
    r"abroad|overseas)\b", re.I)
_FOREIGN_CS = re.compile(r"\b(?:U\.?S\.?A?|US)\b")     # case-sensitive: US, USA, U.S.
_UK_HINT = re.compile(
    r"\b(u\.?k\.?|united kingdom|britain|british|england|scotland|scottish|"
    r"wales|welsh|northern ireland|london|manchester|birmingham|nhs|dwp|hmrc|"
    r"westminster|whitehall|ofsted|ucas|russell group|a-?levels?|gcses?|"
    r"apprenticeship|universal credit|£)\b", re.I)


_YOUTH_SIGNAL = re.compile(r"\b(young|youth|under.?25s?|16.?24s?|18.?24s?|neet)\b", re.I)


def _is_youth_labour_story(hay):
    """True for youth-labour-market stories that use none of the canon nouns,
    e.g. 'Young bearing brunt of hiring slump'. Requires both a youth signal and
    core job-market language so general 'young people' stories don't slip in."""
    return bool(_YOUTH_SIGNAL.search(hay) and CORE_JOB_MARKET.search(hay))


def _is_uk(hay):
    """True if the story is UK-relevant. Foreign-market stories are kept only
    when they also mention the UK (e.g. 'US firms expand UK graduate hiring')."""
    if _UK_HINT.search(hay):
        return True
    return not (_FOREIGN_CI.search(hay) or _FOREIGN_CS.search(hay))


def _is_job_market_relevant(hay):
    """True only for Internwise-fit employment/early-career stories.

    The canon is deliberately stricter than "job market": a story needs a
    student/intern/graduate/applicant angle and a practical reader takeaway.
    Broad hiring movement, PR launches, awards, webinars, local one-offs and
    sector-only trade stories are rejected even if they contain job keywords.
    """
    if NON_NEWS_FLUFF.search(hay):
        return False
    if ORG_PR_OR_LOCAL_ONLY.search(hay):
        return False
    if NAMED_INSTITUTION.search(hay) and INSTITUTION_PROMO.search(hay):
        return False
    if EXCLUDED_JOB_TYPES.search(hay):
        return False
    if SPORT_PLAYING.search(hay) and not SPORT_INDUSTRY_JOB.search(hay):
        return False
    if LIFESTYLE_MONEY.search(hay) and not CORE_JOB_MARKET.search(hay):
        return False
    youth = _is_youth_labour_story(hay)
    if not INTERNWISE_NEWS_CANON.search(hay) and not youth:
        return False
    if not ACTIONABLE_EARLY_CAREER.search(hay) and not youth:
        return False
    if CORE_JOB_MARKET.search(hay):
        return True
    return bool(re.search(r"\b(wage|salary|pay)\b", hay, re.I) and WORK_PAY_CONTEXT.search(hay))


# A plain bot UA gets 403'd by several of these publishers' CDNs when the request
# comes from a datacentre IP (which every GitHub-hosted runner has). Present as a
# normal browser and accept the usual feed content types.
UA = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/131.0.0.0 Safari/537.36"),
    "Accept": "application/rss+xml, application/atom+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.5",
    "Accept-Language": "en-GB,en;q=0.9",
}


def _text(el):
    return html.unescape((el.text or "").strip()) if el is not None else ""


_DASHES = {"—": "-", "–": "-", "‒": "-", "‑": "-", "‐": "-"}

def _clean(s, limit=None):
    s = re.sub(r"<[^>]+>", "", s or "")          # strip HTML tags
    s = html.unescape(s)
    for d, r in _DASHES.items():
        s = s.replace(d, r)
    # strip common RSS footer boilerplate ("The post X appeared first on Y.")
    s = re.sub(r"\s*The post .*?appeared first on .*$", "", s, flags=re.I)
    s = re.sub(r"\s*(Continue reading|Read more).*$", "", s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip()
    if limit and len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0].rstrip(",.;:") + "..."
    return s


def _parse_date(s):
    if not s:
        return None
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z",
                "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            d = datetime.datetime.strptime(s.strip(), fmt)
            return d.replace(tzinfo=None)
        except ValueError:
            continue
    return None


class _Redirect308(urllib.request.HTTPRedirectHandler):
    """urllib handles 301/302/303/307 but not 308, which several feeds now use."""
    def http_error_308(self, req, fp, code, msg, headers):
        return self.http_error_301(req, fp, 301, msg, headers)


_OPENER = urllib.request.build_opener(_Redirect308)


def _fetch_feed(source, url, timeout=12, attempts=2):
    """Fetch and parse one feed. Never raises: a dead feed returns [] so the
    remaining feeds still supply the pool."""
    raw = None
    for n in range(attempts):
        try:
            req = urllib.request.Request(url, headers=UA)
            raw = _OPENER.open(req, timeout=timeout).read()
            break
        except Exception as e:
            if n + 1 >= attempts:
                print(f"  ! {source}: {e}", file=sys.stderr)
                return []
            time.sleep(1.5)            # transient 5xx / rate-limit; one retry
    try:
        root = ET.fromstring(raw)
    except Exception as e:
        print(f"  ! {source}: unparseable feed ({e})", file=sys.stderr)
        return []
    items = []
    for it in root.iter("item"):              # RSS 2.0
        items.append((it, "rss"))
    ns = "{http://www.w3.org/2005/Atom}"
    for it in root.iter(ns + "entry"):        # Atom
        items.append((it, "atom"))
    out = []
    for it, kind in items:
        if kind == "rss":
            title = _clean(_text(it.find("title")))
            link = _text(it.find("link"))
            desc = _clean(_text(it.find("description")), 180)
            date = _parse_date(_text(it.find("pubDate")))
        else:
            title = _clean(_text(it.find(ns + "title")))
            le = it.find(ns + "link")
            link = le.get("href") if le is not None else ""
            desc = _clean(_text(it.find(ns + "summary")), 180)
            date = _parse_date(_text(it.find(ns + "updated")) or _text(it.find(ns + "published")))
        if title:
            out.append({"source": source, "title": title, "url": link,
                        "summary": desc, "date": date})
    return out


def _load_used():
    if os.path.exists(LOG):
        try:
            return set(json.load(open(LOG)))
        except Exception:
            return set()
    return set()


def fetch(max_age_days=5, limit=8):
    """Return a ranked list of fresh, relevant, unused news items."""
    used = _load_used()
    now = _utcnow()
    pool = []
    seen_titles = set()
    for source, url in FEEDS:
        for it in _fetch_feed(source, url):
            key = (it["url"] or it["title"]).strip()
            if key in used:
                continue
            tkey = re.sub(r"[^a-z0-9]", "", it["title"].lower())[:40]
            if tkey in seen_titles:      # drop exact/near-duplicate headlines
                continue
            seen_titles.add(tkey)
            if it["date"] and (now - it["date"]).days > max_age_days:
                continue
            hay = it["title"] + " " + it["summary"]
            if not _is_uk(hay):          # UK job market ONLY - drop foreign stories
                continue
            if not _is_job_market_relevant(hay):
                continue
            it["score"] = len(KEYWORDS.findall(hay))
            if it["score"] == 0:
                continue
            it["key"] = key
            pool.append(it)
    pool.sort(key=lambda x: (x["score"], x["date"] or datetime.datetime.min), reverse=True)
    return pool[:limit]


def mark_used(items):
    used = _load_used()
    for it in items:
        used.add(it.get("key") or it.get("url") or it.get("title"))
    json.dump(sorted(used), open(LOG, "w"), indent=0)


def sample_item():
    """Offline fixture so the news card can be previewed without network."""
    return {
        "source": "Personnel Today",
        "title": "UK graduate vacancies rise as employers reopen early-careers hiring",
        "summary": "Firms are expanding intern and graduate schemes heading into the new academic year, with demand strongest in tech, finance and green energy.",
        "url": "https://www.personneltoday.com",
        "date": _utcnow(),
        "kicker": "JOB MARKET",
    }


if __name__ == "__main__":
    got = fetch()
    if not got:
        print("No live items (network blocked or nothing relevant). Sample item:")
        print(json.dumps(sample_item(), default=str, indent=2))
    for i, it in enumerate(got, 1):
        print(f"{i}. [{it['source']}] ({it['score']}) {it['title']}")
