"""News lane - THE fixed template (the only templated lane in the Daily-5 system).

A single 1080x1080 rendered as a real NEWSPAPER FRONT PAGE (per client refs):
aged newsprint, branded blue masthead with the white Internwise logo, date/section line,
a centered full-width headline, then TWO justified serif columns plus a sidebar box and
an optional relevant image panel. Do not use fake volume/issue metadata. On-screen it is a BRIEF - the full story + source
go in the caption, so the foot points the reader there.

    from news_card import render_news
    render_news(item, out_dir, "slide_1.png", brief=[...], sidebar=[...], image_path="...")
"""
import os, sys, datetime, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L

PAPER="#F1E9D6"; INK="#1A1712"; SUB="#4A443A"; RULE="#1A1712"; AMBER=L.AMBER
# NB: no quoted font names - this string goes inside single-quoted style attrs,
# so an inner quote would close the attribute early and drop later properties.
SERIF = "Georgia,serif"


def _hsize(text):
    n = len(text)
    if n <= 34:  return 76
    if n <= 50:  return 62
    if n <= 70:  return 54
    if n <= 96:  return 46
    return 40


def _complete_sentences(text, max_chars):
    """Trim display copy at sentence boundaries so the newspaper never ends mid-thought."""
    text = re.sub(r"\s+", " ", (text or "").replace("...", ".")).strip()
    if len(text) <= max_chars and re.search(r"[.!?]$", text):
        return text
    bits = re.findall(r"[^.!?]+[.!?]", text)
    out = ""
    for bit in bits:
        cand = (out + " " + bit.strip()).strip()
        if len(cand) > max_chars:
            break
        out = cand
    if out:
        return out
    words = text[:max_chars].split()
    while words and words[-1].lower().strip(",;:") in {"and", "or", "for", "with", "to", "of", "the", "those"}:
        words.pop()
    return (" ".join(words).rstrip(",;:") + ".") if words else ""


def _safe_brief(paras):
    cleaned = []
    limits = [230, 175, 170]
    for i, p in enumerate(paras or []):
        s = _complete_sentences(p, limits[min(i, len(limits) - 1)])
        if s:
            cleaned.append(s)
    return cleaned[:3]


def _safe_sidebar(items):
    cleaned = []
    for item in items or []:
        s = re.sub(r"\s+", " ", (item or "").replace("...", "")).strip(" .")
        if not s:
            continue
        words = s.split()
        cleaned.append(" ".join(words[:6]).rstrip(",;:"))
    return cleaned[:3]


def _rule(x, y, w, kind="double"):
    if kind == "double":
        return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:4px;background:{RULE};'></div>"
                f"<div style='position:absolute;left:{x}px;top:{y+7}px;width:{w}px;height:1.5px;background:{RULE};'></div>")
    if kind == "thin":
        return f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:1.5px;background:{RULE};opacity:.55;'></div>"
    return f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:3px;background:{RULE};'></div>"


def render_news(item, out_dir, filename="slide_1.png", issue_no=1,
                headline=None, brief=None, sidebar=None, pull=None, image_path=None,
                image_caption=None):
    """Render the newspaper card.

    IMPORTANT - no plagiarism: the RSS `item` is a TOPIC + FACT seed only. The
    live pipeline MUST pass `headline`, `brief`, `sidebar`, `pull` rewritten in
    Internwise's own voice. Never display the feed's exact headline/summary text
    (that is duplicate content). The raw item fields are a dev-only fallback.
    """
    if not image_path:
        raise ValueError("News cards require image_path; do not render text-only news graphics.")
    kicker  = (item.get("kicker") or "JOB MARKET").upper()
    # `title` = display headline. Prefer the reworded `headline`; fall back to
    # the raw feed title only in dev (flagged by the pipeline otherwise).
    title   = (headline or item.get("title") or "").replace("—","-").replace("–","-")
    summary = (item.get("summary") or "").replace("—","-").replace("–","-")
    date    = item.get("date")
    if isinstance(date, str) or date is None:
        date = datetime.datetime.utcnow()
    dstr    = date.strftime("%a %d %b %Y").upper()
    title_disp = title.replace("-", "‑")
    hsize   = _hsize(title)

    # Default editorial copy (brand commentary - no invented facts) if none supplied.
    if brief is None:
        brief = [summary or "",
                 "The message for this year's leavers is not to panic but to adapt: apply early, look "
                 "beyond household-name schemes, and build proof of skills.",
                 "Internships remain one of the most reliable routes in - real experience, a foot in the "
                 "door, and a strong path to a full-time offer."]
    sidebar = sidebar or ["Apply early, and apply often",
                          "Target internships, not just graduate schemes",
                          "Show proof of skills over polish"]
    pull = pull or "Internships remain one of the strongest ways into a competitive market."
    brief = _safe_brief(brief)
    sidebar = _safe_sidebar(sidebar)
    pull = _complete_sentences(pull, 120)

    X, W = 48, 984
    FOOT_Y = 980          # everything above this; footer strip lives below
    paper = (f"<div style='position:absolute;inset:0;background:{PAPER};'></div>"
             f"<div style='position:absolute;inset:0;opacity:.55;"
             f"background-image:radial-gradient(rgba(26,23,18,.06) 1px,transparent 1px);background-size:6px 6px;'></div>"
             f"<div style='position:absolute;inset:0;background:radial-gradient(120% 120% at 50% 40%,transparent 60%,rgba(80,60,20,.10));'></div>")

    # --- Masthead ---
    # Brand header only: Internwise blue band + real white logo. The article body
    # stays on newsprint so the post still reads as a news article, not a poster.
    m = (f"<div style='position:absolute;left:0;right:0;top:0;height:190px;background:{L.NAVY};'></div>"
         + f"<div style='position:absolute;left:{X}px;right:{X}px;top:32px;height:3px;background:rgba(255,255,255,.86);'></div>"
         + f"<img src='{L.WHT}' style='position:absolute;left:50%;top:56px;transform:translateX(-50%);height:112px;'>"
         + f"<div style='position:absolute;left:{X}px;right:{X}px;top:174px;height:5px;background:{AMBER};'></div>")
    dot = f"<span style='color:{AMBER};font-size:20px;vertical-align:middle;'>&#10022;</span>"
    info = (f"<div style='position:absolute;left:{X}px;top:206px;width:{W}px;display:flex;align-items:center;justify-content:space-between;'>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:18px;color:{INK};letter-spacing:2px;\">THE INTERNWISE WIRE</span>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:18px;color:{INK};letter-spacing:2px;\">{dstr}</span></div>"
            + _rule(X, 246, W, "double"))

    # --- Section header ---
    sec = (f"<div style='position:absolute;left:{X}px;right:{X}px;top:256px;height:76px;background:#fff;"
           f"border-top:3px solid {RULE};border-bottom:3px solid {RULE};display:flex;align-items:center;justify-content:center;'>"
           f"<span style='font-family:{SERIF};font-weight:700;font-size:44px;color:{INK};letter-spacing:2px;'>{kicker} NEWS</span></div>")

    # --- Headline + byline + two columns as ONE top-anchored flex column ---
    # The wrapped height of a proportional serif headline cannot be predicted
    # from a character count, so any guessed byline/column offset silently
    # overlaps when a headline wraps to more lines than assumed (the old bug).
    # Instead: headline and byline take their natural height, and the two
    # columns take whatever vertical space remains and clip to it. Nothing
    # below the section rule can ever be stamped on top of the headline.
    HEAD_TOP = 340
    stack_h = FOOT_Y - HEAD_TOP

    head = (f"<div style='flex:0 0 auto;text-align:center;font-family:{SERIF};font-weight:700;"
            f"font-size:{min(hsize + 8, 82)}px;line-height:.98;color:{INK};letter-spacing:-.5px;word-break:keep-all;text-transform:none;'>{title_disp}</div>")

    byline = (f"<div style='flex:0 0 auto;margin-top:16px;'>"
              f"<div style='width:100%;height:1.5px;background:{RULE};opacity:.55;'></div>"
              f"<div style=\"margin-top:11px;text-align:left;font-family:'DM Sans';font-weight:800;"
              f"font-size:18px;color:{SUB};letter-spacing:3px;\">"
              f"THE INTERNWISE WIRE</div></div>")

    # left column: drop cap + justified body paragraphs
    drop = brief[0][:1] if brief and brief[0] else ""
    rest0 = brief[0][1:] if brief and brief[0] else ""
    paras = ""
    if brief and brief[0]:
        paras += (f"<p style='margin:0 0 13px;text-align:left;font-family:{SERIF};font-size:24px;line-height:1.32;color:{INK};'>"
                  f"<span style='float:left;font-family:{SERIF};font-weight:700;font-size:74px;line-height:.72;color:{AMBER};margin:5px 11px 0 0;'>{drop}</span>"
                  f"{rest0}</p>")
    for p in brief[1:]:
        paras += f"<p style='margin:0 0 13px;text-align:left;font-family:{SERIF};font-size:23px;line-height:1.32;color:{INK};'>{p}</p>"
    colL = f"<div style='flex:0 0 490px;height:100%;overflow:hidden;'>{paras}</div>"

    divider = f"<div style='flex:0 0 1.5px;align-self:stretch;background:{RULE};opacity:.5;'></div>"

    bullets = "".join(
        f"<div style='display:flex;gap:10px;margin-bottom:10px;'>"
        f"<span style='color:{AMBER};font-family:{SERIF};font-weight:700;font-size:22px;line-height:1;'>&#9642;</span>"
        f"<span style='font-family:{SERIF};font-size:22px;line-height:1.24;color:{INK};'>{b}</span></div>" for b in sidebar)
    box = (f"<div style='border:2.5px solid {INK};padding:18px 20px;'>"
           f"<div style='font-family:{SERIF};font-weight:700;font-size:21px;letter-spacing:2px;color:{INK};"
           f"text-align:center;border-bottom:2px solid {INK};padding-bottom:9px;margin-bottom:13px;'>WHAT STUDENTS SHOULD NOTICE</div>"
           f"{bullets}</div>")
    if image_path:
        src = L.img(image_path)
        cap = image_caption or "Relevant workplace context for this story."
        pq = (f"<div style='margin-top:16px;border:2.5px solid {INK};height:178px;overflow:hidden;position:relative;background:#d8d0bd;'>"
              f"<img src='{src}' style='width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.08);'>"
              f"<div style='position:absolute;left:0;right:0;bottom:0;background:rgba(241,233,214,.86);"
              f"border-top:2px solid {INK};padding:7px 12px;font-family:{SERIF};font-style:italic;"
              f"font-weight:700;font-size:16px;line-height:1.05;color:{INK};'>{cap}</div></div>")
    else:
        pq = (f"<div style='margin-top:20px;border-top:3px solid {INK};border-bottom:3px solid {INK};padding:15px 4px;'>"
              f"<div style='font-family:{SERIF};font-style:italic;font-weight:700;font-size:27px;line-height:1.22;color:{INK};text-align:center;'>&ldquo;{pull}&rdquo;</div></div>")
    colR = f"<div style='flex:0 0 446px;height:100%;overflow:hidden;'>{box}{pq}</div>"

    cols = (f"<div style='flex:1 1 auto;min-height:0;margin-top:20px;display:flex;"
            f"justify-content:space-between;'>{colL}{divider}{colR}</div>")

    stack = (f"<div style='position:absolute;left:{X}px;top:{HEAD_TOP}px;width:{W}px;height:{stack_h}px;"
             f"display:flex;flex-direction:column;'>{head}{byline}{cols}</div>")

    # --- Foot: continued in caption ---
    foot = (_rule(X, FOOT_Y + 6, W, "double")
            + f"<div style='position:absolute;left:{X}px;top:{FOOT_Y+26}px;width:{W}px;display:flex;justify-content:space-between;align-items:center;'>"
              f"<span style='font-family:{SERIF};font-weight:700;font-style:italic;font-size:25px;color:{INK};'>"
              f"The full story continues in the caption &darr;</span>"
              f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:21px;color:{INK};letter-spacing:1px;\">INTERNWISE.CO.UK</span></div>")

    inner = paper + m + info + sec + stack + foot
    return L.render(out_dir, filename, inner)


if __name__ == "__main__":
    import news_fetch
    got = news_fetch.fetch()
    item = got[0] if got else news_fetch.sample_item()
    # Demo of the required workflow: facts from the feed, ALL copy rewritten in
    # Internwise's own words (nothing pasted from the source).
    render_news(
        item, os.path.join(L.OUTROOT, "week14", "news_sample"),
        headline="Graduate openings fall to a record low",
        brief=[
            "The number of graduate vacancies advertised across the UK has slipped to its lowest "
            "level on record, leaving many of this year's leavers facing a tougher start than they "
            "had planned for.",
            "It is a harder market, but not a closed one. The graduates who get hired tend to move "
            "early, widen their search beyond the big-name schemes, and let real work do the talking.",
            "That is where internships earn their keep: hands-on experience, a genuine way into a "
            "company, and often the bridge to a first full-time role.",
        ],
        sidebar=["Start applying early, and keep at it",
                 "Look at internships, not only graduate schemes",
                 "Let proof of skills beat a polished CV"],
        pull="A tougher market rewards the graduates who start early and keep going.",
        image_path=os.path.join(L.BASE, "assets", "news", "jobs-guarantee-work-placement.png"),
    )
    print("rendered (reworded copy):", item["title"])
