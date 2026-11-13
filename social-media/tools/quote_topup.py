"""Quote bank top-up - keeps the Saturday build from running out of quotes.

The weekly build needs 5 quotes whose author has a portrait and has never been
posted before (posted authors are blocked for good). Nothing used to refill the
bank, so it ran dry (7 Nov 2026 build failure). This adds NEW AUTHORS until the
bank holds at least TARGET_FRESH fresh, portrait-backed quotes.

Accuracy rules (why this does not just ask an LLM for quotes):
  - Quote TEXT comes only from the "Sourced" section of the author's English
    Wikiquote page, and only quotes that carry a citation line.
  - The LLM (OPENAI_API_KEY) may only CHOOSE one of those verbatim quotes and
    write the theme/CTA; the chosen text is checked to match exactly.
  - Portraits are the author's Wikipedia lead image, downloaded only when the
    Commons licence is public domain / CC0 / CC BY / CC BY-SA, and logged in
    assets/quote_authors/SOURCES.md.
Authors come from content/quote_author_seeds.json; when that runs low the LLM
proposes more NAMES, which still have to pass both checks above.

    python3 tools/quote_topup.py            # top up to TARGET_FRESH
    python3 tools/quote_topup.py --dry      # report only, write nothing
    python3 tools/quote_topup.py --add 3    # force-add up to 3 new authors
"""
import os, sys, re, json, io, argparse, urllib.parse
import requests
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
BANK = os.path.join(SM, "content", "quotes_bank.json")
SEEDS = os.path.join(SM, "content", "quote_author_seeds.json")
AUTH_DIR = os.path.join(SM, "assets", "quote_authors")
SOURCES_MD = os.path.join(AUTH_DIR, "SOURCES.md")
TARGET_FRESH = 15          # three weeks of quotes in hand
MAX_ADD_PER_RUN = 10
UA = {"User-Agent": "quote-topup-bot/1.0 (automated quote bank maintenance)"}
OK_LICENCE = re.compile(r"^(public domain|pd\b|pd-|cc0|cc[ -]by(-sa)?[ -]?\d|cc[ -]by(-sa)?$)", re.I)
BANNED = re.compile(r"\b(god|lord|jesus|christ|allah|heaven|hell|sin|church|bible|prayer|war|kill|blood|"
                    r"slave|nation|government|party|vote|politic|king|queen|women are|men are|wife|husband|drunk|"
                    r"man|men|mankind|profits?|money|rich|wealth)\b", re.I)
GOOD = re.compile(r"\b(work|learn|begin|start|effort|try|courage|persever|patien|habit|skill|practi|success|"
                  r"fail|study|knowledge|time|today|act|do|progress|improv|curio|imagin|dream|goal|purpose)\w*", re.I)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


class FetchError(RuntimeError):
    """Network/rate-limit trouble - NOT evidence that an author has no quotes."""


def _get(url, **params):
    """Polite Wikimedia GET: ~1 request/second, backs off on 429/5xx."""
    import time
    for attempt in range(5):
        time.sleep(1.2 * (attempt + 1) ** 2 if attempt else 1.0)
        try:
            r = requests.get(url, params=params, headers=UA, timeout=30)
        except requests.RequestException as e:
            err = str(e)
            continue
        if r.status_code == 429 or r.status_code >= 500:
            err = f"HTTP {r.status_code}"
            time.sleep(float(r.headers.get("Retry-After", 0) or 0))
            continue
        r.raise_for_status()
        return r.json()
    raise FetchError(err)


# ---------------------------------------------------------------- bank state
def load_bank():
    return json.load(open(BANK))


def has_portrait(author):
    s = slug(author)
    return any(os.path.exists(os.path.join(AUTH_DIR, f"{s}.{e}")) for e in ("jpg", "jpeg", "png", "webp"))


def posted_authors():
    """Authors whose quote went out through Ayrshare - the weekly build blocks them for good.
    Reads the data files directly (no build_week import, so the lean cloud job can run it)."""
    hub = os.path.dirname(SM)
    posted = {k.split(":", 1)[0] for k in json.load(open(os.path.join(SM, "content", "ayrshare_posted.json")))}
    out = set()
    for w in json.load(open(os.path.join(hub, "data", "weeks.json"))).get("weeks", []):
        for p in w.get("posts", []):
            if p.get("lane") == "quote" and p.get("id") in posted:
                m = re.match(r"Quote:\s*(.+)", p.get("title", ""))
                if m:
                    out.add(m.group(1).strip().lower())
    return out


def fresh_quotes(bank, blocked):
    seen, out = set(), []
    for q in bank["quotes"]:
        a = q.get("author", "").strip()
        if a.lower() in blocked or a.lower() in seen or a == "Internwise" or not has_portrait(a):
            continue
        seen.add(a.lower())
        out.append(q)
    return out


# ---------------------------------------------------------------- wikiquote
def _clean(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"\[https?://\S+ ([^\]]+)\]", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s).replace("'''", "").replace("''", "")
    s = s.replace("—", " - ").replace("–", "-").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", s).strip()


FOREIGN = re.compile(r"\b(le|la|les|et|du|des|est|qui|une|que|pas|und|der|die|das|ist|nicht|il|che|non|el|los|las|y|que|est)\b", re.I)


def is_english(text):
    """Wikiquote often lists the original-language line first; keep English only."""
    accents = sum(1 for c in text if ord(c) > 127 and c not in "\u2018\u2019\u201c\u201d")
    return accents <= 1 and len(FOREIGN.findall(text)) < 2


def is_verse(text):
    """Poem lines keep a capital at each line start ("... in sight, Than gain my ..."); cards need prose."""
    return bool(re.search(r"[a-z][;:,][A-Z]", text)) or len(re.findall(r"[a-z,;] ?(?!I\b)[A-Z][a-z]", text)) >= 2


def sourced_quotes(author):
    """[(text, citation)] from the Sourced/Quotes section of the author's Wikiquote page."""
    j = _get("https://en.wikiquote.org/w/api.php", action="parse", page=author, prop="wikitext",
             format="json", formatversion=2, redirects=1)       # FetchError propagates: retry next run
    wt = j.get("parse", {}).get("wikitext", "")
    if not wt:
        return []
    # keep text from the first quotes section up to the first "not his/her" section
    start = re.search(r"^==\s*(Sourced|Quotes|Quotations)\s*==\s*$", wt, re.M | re.I)
    body = wt[start.end():] if start else wt
    stop = re.search(r"^==\s*(Disputed|Misattributed|Attributed|Quotes about|About|External links|See also)", body, re.M | re.I)
    body = body[:stop.start()] if stop else body
    out, lines, work = [], body.splitlines(), ""
    for i, ln in enumerate(lines):
        h = re.match(r"^===+\s*(.+?)\s*===+\s*$", ln)
        if h:
            work = _clean(h.group(1))
            continue
        if not ln.startswith("* ") or ln.startswith("**"):
            continue
        cite = lines[i + 1][2:].strip() if i + 1 < len(lines) and lines[i + 1].startswith("**") else ""
        text = _clean(ln[2:])
        if not cite or not text or re.search(r"quoted to|misattributed|attributed to", cite, re.I):
            continue
        cite = _clean(cite)
        if work and work.lower() not in cite.lower() and len(cite) < 70:
            cite = f"{work}, {cite}"
        if not is_english(text) or is_verse(text):
            continue
        if not 30 <= len(text) <= 130 or any(c in text for c in "[]{}|=") or text.count('"') % 2:
            continue
        out.append((text, cite[:160]))
    return out


# ---------------------------------------------------------------- portrait
def fetch_portrait(author, dry=False):
    """Download the Wikipedia lead image if its Commons licence is free. Returns a SOURCES row or None."""
    try:
        j = _get("https://en.wikipedia.org/w/api.php", action="query", titles=author, prop="pageimages",
                 piprop="name", format="json", formatversion=2, redirects=1)
        name = j["query"]["pages"][0].get("pageimage")
        if not name:
            return None
        j = _get("https://commons.wikimedia.org/w/api.php", action="query", titles=f"File:{name}",
                 prop="imageinfo", iiprop="url|extmetadata", iiurlwidth=1200, format="json", formatversion=2)
        info = j["query"]["pages"][0]["imageinfo"][0]
    except FetchError:
        raise
    except Exception:
        return None
    meta = info.get("extmetadata", {})
    lic = re.sub(r"<[^>]+>", "", meta.get("LicenseShortName", {}).get("value", "")).strip()
    if not OK_LICENCE.match(lic):
        print(f"    portrait licence not usable ({lic or 'unknown'}) - skipping {author}")
        return None
    artist = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip()
    page = info.get("descriptionurl", "")
    if dry:
        return {"licence": lic, "page": page}
    im = None
    for attempt in range(6):
        import time
        time.sleep(3 * (attempt + 1) ** 2)          # 3s, 12s, 27s ... - the media server rate-limits hard
        try:
            r = requests.get(info.get("thumburl") or info["url"], headers=UA, timeout=60)
            if r.status_code == 429:
                time.sleep(float(r.headers.get("Retry-After", 0) or 0))
                continue
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("image/"):
                im = Image.open(io.BytesIO(r.content)).convert("RGB")
                break
        except Exception:
            pass
    if im is None:
        raise FetchError("portrait download failed")
    if min(im.size) < 300:
        print(f"    portrait too small {im.size} - skipping {author}")
        return None
    im.save(os.path.join(AUTH_DIR, f"{slug(author)}.jpg"), quality=92)
    note = lic + (f", {artist[:60]}" if artist and lic.lower().startswith("cc") else "")
    return {"row": f"| {author} | `{slug(author)}.jpg` | {page} | {note}. Auto-added by quote_topup.py. |",
            "licence": lic, "page": page}


# ---------------------------------------------------------------- choosing
def choose(author, candidates):
    """Pick one verbatim quote + theme + CTA. LLM if available, keyword fallback otherwise."""
    cands = [(t, c) for t, c in candidates if not BANNED.search(t)][:40]
    if not cands:
        return None
    if os.getenv("OPENAI_API_KEY"):
        try:
            import writer
            listing = "\n".join(f"{i}. {t}" for i, (t, _) in enumerate(cands))
            j = writer._chat(
                f"These are verified, sourced quotes by {author}. Pick the ONE that best motivates UK students and "
                f"graduates looking for internships or a first job. It must read naturally ON ITS OWN as advice "
                f"about work, learning, effort, courage, failure or starting out. Reject: fiction dialogue addressed "
                f"to another character, advice for business owners (costs, profits, managing staff), anything "
                f"religious, political, dated, gendered, bleak or confusing out of context. If none fits, return "
                f"index -1 (a skipped author is fine).\n\n{listing}\n\n"
                'Return JSON: {"index": int, "theme": one lowercase word (e.g. "persistence"), '
                '"cta": a 3-6 word nudge ending with " - internwise.co.uk" (no em dashes)}', max_tokens=200)
            i = int(j.get("index", -1))
            if 0 <= i < len(cands):
                cta = str(j.get("cta", "")).replace("—", "-").strip()
                cta = cta[:1].upper() + cta[1:]
                if not cta.endswith("internwise.co.uk"):
                    cta = "Take the next step - internwise.co.uk"
                return cands[i][0], cands[i][1], str(j.get("theme", "motivation")).lower()[:20], cta
            return None
        except Exception as e:
            print(f"    LLM choice failed ({e}); using keyword fallback")
    scored = sorted(cands, key=lambda tc: (-len(GOOD.findall(tc[0])), len(tc[0])))
    if not GOOD.search(scored[0][0]):
        return None
    return scored[0][0], scored[0][1], "motivation", "Take the next step - internwise.co.uk"


def more_seed_names(existing):
    if not os.getenv("OPENAI_API_KEY"):
        return []
    try:
        import writer
        j = writer._chat(
            "List 30 historical figures (died before 1960) with an English Wikiquote page who wrote or said "
            "memorable things about work, learning, effort or courage. Scientists, writers, artists, inventors, "
            "philosophers; no politicians, religious leaders or military figures. Use their exact English "
            f"Wikipedia article title. Exclude: {', '.join(sorted(existing))[:3000]}.\n"
            'Return JSON: {"names": [string]}', max_tokens=700)
        return [n for n in j.get("names", []) if isinstance(n, str) and n.lower() not in existing]
    except Exception as e:
        print(f"  (could not extend seed list: {e})")
        return []


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--add", type=int, default=0, help="force-add up to N authors even if the bank is full")
    a = ap.parse_args()

    bank = load_bank()
    blocked = posted_authors()
    fresh = fresh_quotes(bank, blocked)
    need = max(a.add, TARGET_FRESH - len(fresh))
    print(f"fresh portrait-backed quotes from never-posted authors: {len(fresh)} (target {TARGET_FRESH})")
    if need <= 0:
        print("bank is healthy - nothing to add.")
        return
    need = min(need, MAX_ADD_PER_RUN)

    seeds = json.load(open(SEEDS))
    in_bank = {q["author"].strip().lower() for q in bank["quotes"]}
    tried = {s.lower() for s in seeds.get("rejected", [])}
    queue = [n for n in seeds["authors"] if n.lower() not in in_bank and n.lower() not in tried]
    if len(queue) < need + 15:
        extra = more_seed_names(in_bank | tried | {n.lower() for n in seeds["authors"]})
        if extra:
            print(f"  seed list low - added {len(extra)} LLM-suggested names (still verified below)")
            seeds["authors"] += extra
            queue += extra

    added, rows = [], []
    next_id = max(int(q["id"][1:]) for q in bank["quotes"] if re.match(r"q\d+$", q["id"])) + 1
    for author in queue:
        if len(added) >= need:
            break
        print(f"- {author}")
        try:
            cands = sourced_quotes(author)
        except FetchError as e:
            print(f"    fetch failed ({e}) - will retry next run")
            continue
        if not cands:
            print("    no sourced, cited quotes of usable length")
            seeds.setdefault("rejected", []).append(author)
            continue
        pick = choose(author, cands)
        if not pick:
            print("    no quote fits the brand")
            seeds.setdefault("rejected", []).append(author)
            continue
        text, cite, theme, cta = pick
        assert any(text == t for t, _ in cands)            # verbatim from Wikiquote, never rewritten
        try:
            port = fetch_portrait(author, dry=a.dry)
        except FetchError as e:
            print(f"    portrait fetch failed ({e}) - will retry next run")
            continue
        if not port:
            seeds.setdefault("rejected", []).append(author)
            continue
        q = {"id": f"q{next_id:03d}", "text": text, "author": author, "theme": theme, "cta": cta,
             "used": None, "source": cite, "verifiedVia": "Wikiquote (Sourced)"}
        next_id += 1
        added.append(q)
        if port.get("row"):
            rows.append(port["row"])
        print(f"    + \"{text}\" ({port['licence']})")

    print(f"\nadded {len(added)} new author(s)")
    if a.dry or not added:
        return
    bank["quotes"] += added
    json.dump(bank, open(BANK, "w"), indent=2, ensure_ascii=False)
    json.dump(seeds, open(SEEDS, "w"), indent=2, ensure_ascii=False)
    with open(SOURCES_MD, "a") as f:
        for r in rows:
            f.write(r + "\n")
    print(f"fresh quotes now: {len(fresh_quotes(load_bank(), blocked))}")


if __name__ == "__main__":
    main()
