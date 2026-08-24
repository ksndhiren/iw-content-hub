"""Week 14 (w/c 31 Aug) - Phase 1 design samples for the three bespoke lanes.

One post each for FUN, QUOTE, EMPLOYER, each in its OWN design language
(distinct palette + device), to sign off the creative direction for each lane
before scaling to the full week. News uses its fixed template (news_card.py).

    python3 tools/w14_samples.py         # renders all three
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L
import wk11_base as b

NAVY, DEEP, INK, MUT = L.NAVY, L.DEEP, L.INK, L.MUT
AMBER, CORAL, GREEN = L.AMBER, L.CORAL, L.GREEN
BLU = "data:image/png;base64,"+b.LOGO_B      # blue logo for light backgrounds
OUT = os.path.join(L.OUTROOT, "week14")


# ============================================================ QUOTE ==========
# Design world: warm cream editorial. Giant amber quotation glyph, navy serif-
# weight headline, coral rule, author plate. Calm, premium, print-like.
def quote_sample():
    q = L.load("quotes_bank.json")["quotes"][0]   # q001
    text, author = q["text"], q["author"]
    cta = q.get("cta", "Start today at internwise.co.uk")
    CREAM="#F3EADA"; PAPER="#EFE3CE"; NAVYT="#152743"; COFFEE="#8A7B62"
    bg = (f"<div style='position:absolute;inset:0;background:"
          f"radial-gradient(120% 100% at 15% 0%,{CREAM},{PAPER});'></div>")
    # faint paper texture lines
    tex = ("<div style='position:absolute;inset:0;opacity:.5;"
           "background-image:radial-gradient(rgba(138,123,98,.12) 1.5px,transparent 1.5px);"
           "background-size:30px 30px;'></div>")
    # opener mark sitting well below the logo, directly above the quote text
    glyph = (f"<div style='position:absolute;left:52px;top:322px;font-family:Georgia,serif;"
             f"font-weight:700;font-size:240px;line-height:.7;color:{AMBER};opacity:.9;'>&ldquo;</div>")
    logo = f"<div style='position:absolute;left:56px;top:52px;'><img src='{L.DARKLOGO}' style='height:{L.LOGO}px;'></div>"
    eyebrow = (f"<div style=\"position:absolute;right:60px;top:76px;font-family:'DM Sans';font-weight:700;"
               f"font-size:21px;color:{COFFEE};letter-spacing:5px;\">QUOTE OF THE DAY</div>")
    body = (f"<div style='position:absolute;left:60px;right:70px;top:520px;'>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:78px;line-height:1.12;"
            f"letter-spacing:-1.5px;color:{NAVYT};word-break:keep-all;\">{text}</div>"
            f"<div style='width:96px;height:6px;background:{CORAL};border-radius:3px;margin:44px 0 30px;'></div>"
            f"<div style='display:inline-flex;align-items:center;gap:16px;'>"
            f"<div style='width:52px;height:52px;border-radius:50%;background:{NAVYT};display:flex;"
            f"align-items:center;justify-content:center;'>{L.svg('user',AMBER,26)}</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:34px;color:{NAVYT};\">{author}</div></div></div>")
    # tailored one-line CTA (leads to the site), phrased to echo the quote
    footer = (f"<div style='position:absolute;left:56px;right:70px;bottom:50px;'>"
              f"<div style='height:2px;background:{NAVYT};opacity:.18;margin-bottom:20px;'></div>"
              f"<div style='display:flex;align-items:center;gap:16px;'>"
              f"<div style='flex:0 0 auto;width:48px;height:48px;border-radius:50%;background:{CORAL};display:flex;align-items:center;justify-content:center;'>"
              f"<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.6' "
              f"stroke-linecap='round' stroke-linejoin='round'><path d='M5 12h14M13 6l6 6-6 6'/></svg></div>"
              f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;color:{NAVYT};letter-spacing:-.3px;\">{cta}</span></div></div>")
    wm = L.watermark(w=520, right=-70, bottom=-130, op=.05, tint="dark")
    inner = bg+tex+wm+glyph+logo+eyebrow+body+footer
    return L.render(os.path.join(OUT,"quote_sample"), "slide_1.png", inner)


# ============================================================ FUN ============
# Design world: playful 'bingo card'. Self-contained relatable humour (no poll,
# no vote needed - works even with zero engagement). Confetti dots, a 3x3 grid
# of graduate job-hunt truths with a free centre square, warm closer line.
def fun_sample():
    idea = L.load("fun_ideas.json")["ideas"][2]   # f003 bingo
    cells = ["'We'll be in touch'", "Rewrote CV for the 9th time", "Ghosted after round 3",
             "'Entry-level, 5 yrs exp'", "FREE", "Refreshed inbox x40",
             "LinkedIn-stalked the team", "Cover letter deja vu", "Mock interview with mum"]
    bg = (f"<div style='position:absolute;inset:0;background:"
          f"radial-gradient(130% 120% at 15% -10%,#1a2f57,{NAVY} 55%,{DEEP});'></div>")
    confetti = (
        L.dots("right:-30px;top:-10px;", color="rgba(255,177,32,.5)", w=300, h=170) +
        L.dots("left:-20px;top:150px;", color="rgba(65,217,138,.4)", w=200, h=150) +
        L.dots("right:60px;bottom:-20px;", color="rgba(255,107,107,.4)", w=240, h=120))
    logo = L.logo_tl()
    badge = (f"<div style='position:absolute;right:56px;top:60px;display:inline-flex;align-items:center;gap:10px;"
             f"height:46px;padding:0 22px;border-radius:23px;background:{AMBER};'>"
             f"<span style=\"font-family:Inter;font-weight:800;font-size:20px;color:{DEEP};letter-spacing:3px;\">BINGO</span></div>")
    eyebrow = (f"<div style=\"position:absolute;left:58px;top:196px;font-family:'DM Sans';font-weight:700;"
               f"font-size:22px;color:{CORAL};letter-spacing:5px;\">REAL TALK</div>")
    title = (f"<div style=\"position:absolute;left:58px;top:236px;font-family:Inter;font-weight:800;"
             f"font-size:62px;line-height:1.02;letter-spacing:-1.5px;color:{INK};\">Graduate<br>job-hunt bingo</div>")
    tints = ["#FFB120", "#41D98A", "#FF6B6B", "#7B9CFF"]
    tiles = ""
    for i, c in enumerate(cells):
        if c == "FREE":
            tiles += (f"<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;"
                      f"background:{AMBER};border-radius:18px;padding:14px;text-align:center;'>"
                      f"<div style=\"font-family:Inter;font-weight:800;font-size:26px;color:{DEEP};letter-spacing:1px;\">FREE</div>"
                      f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:20px;color:{DEEP};\">applied anyway</div></div>")
        else:
            ac = tints[i % 4]
            tiles += (f"<div style='display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.05);"
                      f"border:2px solid {ac}55;border-radius:18px;padding:16px 14px;text-align:center;'>"
                      f"<span style=\"font-family:Inter;font-weight:700;font-size:24px;color:{INK};line-height:1.18;letter-spacing:-.3px;\">{c}</span></div>")
    grid = (f"<div style='position:absolute;left:58px;right:58px;top:398px;display:grid;"
            f"grid-template-columns:repeat(3,1fr);grid-auto-rows:156px;gap:16px;'>{tiles}</div>")
    closer = (f"<div style=\"position:absolute;left:58px;bottom:96px;font-family:'DM Sans';font-weight:700;"
              f"font-size:30px;color:{AMBER};\">We&rsquo;ve all been there.</div>")
    inner = bg+confetti+logo+badge+eyebrow+title+grid+closer+L.url_footer()
    return L.render(os.path.join(OUT,"fun_sample"), "slide_1.png", inner)


# ============================================================ EMPLOYER =======
# Design world: B2B teal, confident and corporate-clean (clearly a different
# audience from jobseeker posts). Founder Nuno (authority pose) as the face, with
# an amber arc behind for separation + a soft grounding shadow (NOT a glow).
# Benefit-led: real Internwise value props (verified from the site), NO pricing.
def employer_sample():
    a = L.load("employer_angles.json")["angles"][0]   # e001 - talent pool
    hi, benefits = a["headline"], a["benefits"]
    TEAL="#0B2B33"; TEAL2="#0A1D24"; SUBT="#9FC2C9"
    NUNO = L.nuno_src("nuno_authority_1")
    bg = (f"<div style='position:absolute;inset:0;background:linear-gradient(150deg,{TEAL},{TEAL2});'></div>")
    grid = ("<div style='position:absolute;inset:0;background-image:"
            "linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),"
            "linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);"
            "background-size:60px 60px;'></div>")
    arc = (f"<div style='position:absolute;right:-70px;bottom:-40px;width:760px;height:760px;border-radius:50%;"
           f"background:radial-gradient(circle at 50% 45%,{AMBER}2e,{AMBER}00 66%);'></div>")
    ground = (f"<div style='position:absolute;right:150px;bottom:34px;width:520px;height:70px;border-radius:50%;"
              f"background:radial-gradient(ellipse,rgba(0,0,0,.5),rgba(0,0,0,0) 70%);'></div>")
    nuno = (f"<img src='{NUNO}' style='position:absolute;right:-40px;bottom:0;height:800px;"
            f"filter:drop-shadow(0 22px 34px rgba(0,0,0,.5));'>")
    logo = L.logo_tl()
    tag = (f"<div style='position:absolute;left:58px;top:172px;display:inline-flex;align-items:center;gap:10px;"
           f"height:46px;padding:0 20px;border-radius:23px;background:{GREEN}1f;border:1.5px solid {GREEN}80;'>"
           f"{L.svg('briefcase',GREEN,22)}<span style=\"font-family:Inter;font-weight:700;font-size:19px;color:{INK};letter-spacing:2px;\">FOR EMPLOYERS</span></div>")
    head = (f"<div style='position:absolute;left:58px;top:242px;width:580px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:60px;line-height:1.04;letter-spacing:-1.5px;"
            f"color:{INK};word-break:keep-all;\">Your next intern is <span style='color:{GREEN};'>already here.</span></div></div>")
    icons = ["users", "rocket", "clipboard"]
    rows = ""
    for icon, bn in zip(icons, benefits):
        rows += (f"<div style='display:flex;gap:18px;align-items:center;margin-bottom:22px;'>"
                 f"<div style='flex:0 0 58px;width:58px;height:58px;border-radius:50%;border:2px solid {GREEN}88;"
                 f"background:{GREEN}14;display:flex;align-items:center;justify-content:center;'>{L.svg(icon,GREEN,28)}</div>"
                 f"<div style=\"font-family:Inter;font-weight:700;font-size:30px;color:{INK};letter-spacing:-.4px;line-height:1.12;\">{bn}</div></div>")
    blist = f"<div style='position:absolute;left:58px;top:400px;width:600px;'>{rows}</div>"
    def chip(name):
        src = L.img(os.path.join(L.BASE, "assets", "employer_logos", name+".png"))
        return (f"<div style='display:inline-flex;align-items:center;justify-content:center;height:66px;width:132px;"
                f"background:#FFFFFF;border-radius:12px;box-shadow:0 8px 20px rgba(0,0,0,.22);'>"
                f"<img src='{src}' style='max-width:100px;max-height:44px;object-fit:contain;'></div>")
    chips = "".join(chip(n) for n in ["nike","oracle","o-1","manutd"])
    trust = (f"<div style='position:absolute;left:58px;top:678px;'>"
             f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:19px;color:{SUBT};letter-spacing:2px;\">TRUSTED BY</div>"
             f"<div style='display:flex;gap:12px;margin-top:12px;'>{chips}</div></div>")
    cta = (f"<div style='position:absolute;left:58px;bottom:120px;display:inline-flex;align-items:center;gap:14px;"
           f"height:66px;padding:0 32px;border-radius:33px;background:{GREEN};'>"
           f"<span style=\"font-family:Inter;font-weight:800;font-size:26px;color:{DEEP};\">Post your internship</span>"
           f"<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='{DEEP}' stroke-width='2.8' "
           f"stroke-linecap='round' stroke-linejoin='round'><path d='M5 12h14M13 6l6 6-6 6'/></svg></div>")
    inner = bg+grid+arc+ground+nuno+logo+tag+head+blist+trust+cta+L.url_footer(color=SUBT)
    return L.render(os.path.join(OUT,"employer_sample"), "slide_1.png", inner)


if __name__ == "__main__":
    quote_sample()
    fun_sample()
    employer_sample()
    print("done: quote_sample, fun_sample, employer_sample")
