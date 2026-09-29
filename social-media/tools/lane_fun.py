"""Fun lane - a LIBRARY of distinct, self-contained relatable formats.
No polls / vote-bait (socials have little engagement yet); each post stands on
its own. Worlds: bingo, tierlist, starterpack, pov, greenflags, tabstack.

    render_fun(idea, world, out_dir, "slide_1.png")
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L

NAVY, DEEP, INK, MUT = L.NAVY, L.DEEP, L.INK, L.MUT
AMBER, CORAL, GREEN = L.AMBER, L.CORAL, L.GREEN
BLUE = "#7B9CFF"


def _badge(txt, color, ink=DEEP):
    return (f"<div style='position:absolute;right:56px;top:60px;display:inline-flex;align-items:center;height:46px;"
            f"padding:0 22px;border-radius:23px;background:{color};'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:20px;color:{ink};letter-spacing:3px;\">{txt}</span></div>")

def _eyebrow(txt, top=196):
    return (f"<div style=\"position:absolute;left:58px;top:{top}px;font-family:'DM Sans';font-weight:700;"
            f"font-size:22px;color:{CORAL};letter-spacing:5px;\">{txt}</div>")

def _confetti():
    return (L.dots("right:-30px;top:-10px;", color="rgba(255,177,32,.5)", w=300, h=170) +
            L.dots("left:-20px;top:150px;", color="rgba(65,217,138,.4)", w=200, h=150) +
            L.dots("right:60px;bottom:-20px;", color="rgba(255,107,107,.4)", w=240, h=120))


# ---- bingo ----
def w_bingo(idea):
    cells = ["'We'll be in touch'", "Rewrote CV for the 9th time", "Ghosted after round 3",
             "'Entry-level, 5 yrs exp'", "FREE", "Refreshed inbox x40",
             "LinkedIn-stalked the team", "Cover letter deja vu", "Mock interview with mum"]
    bg = f"<div style='position:absolute;inset:0;background:radial-gradient(130% 120% at 15% -10%,#1a2f57,{NAVY} 55%,{DEEP});'></div>"
    title = (f"<div style=\"position:absolute;left:58px;top:236px;font-family:Inter;font-weight:800;font-size:62px;"
             f"line-height:1.02;letter-spacing:-1.5px;color:{INK};\">Graduate<br>job-hunt bingo</div>")
    tints = [AMBER, GREEN, CORAL, BLUE]
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
    closer = (f"<div style=\"position:absolute;left:58px;bottom:96px;font-family:'DM Sans';font-weight:700;font-size:30px;color:{AMBER};\">We&rsquo;ve all been there.</div>")
    return bg+_confetti()+L.logo_tl()+_badge("BINGO",AMBER)+_eyebrow("REAL TALK")+title+grid+closer+L.url_footer()

# ---- tier list ----
def w_tierlist(idea):
    tiers = [("S", "instant sweat", CORAL, ["Tell me about yourself", "What's your biggest weakness"]),
             ("A", "manageable", AMBER, ["Why this company?", "Where in 5 years?"]),
             ("B", "free points", GREEN, ["Any questions for us?"])]
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,#141d33,{DEEP});'></div>"
    title = (f"<div style=\"position:absolute;left:58px;top:236px;font-family:Inter;font-weight:800;font-size:58px;"
             f"line-height:1.04;letter-spacing:-1.5px;color:{INK};\">Interview questions,<br>ranked by dread</div>")
    rows = ""
    for letter, label, color, items in tiers:
        chips = "".join(f"<span style='display:inline-block;margin:0 10px 10px 0;padding:12px 20px;border-radius:14px;"
                        f"background:rgba(255,255,255,.06);border:1.5px solid {color}55;font-family:Inter;font-weight:700;"
                        f"font-size:25px;color:{INK};'>{it}</span>" for it in items)
        rows += (f"<div style='display:flex;gap:20px;align-items:stretch;margin-bottom:18px;'>"
                 f"<div style='flex:0 0 118px;border-radius:16px;background:{color};display:flex;flex-direction:column;"
                 f"align-items:center;justify-content:center;padding:14px 0;'>"
                 f"<div style=\"font-family:Inter;font-weight:800;font-size:52px;color:{DEEP};line-height:.9;\">{letter}</div>"
                 f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:16px;color:{DEEP};text-align:center;\">{label}</div></div>"
                 f"<div style='flex:1;display:flex;flex-wrap:wrap;align-content:center;'>{chips}</div></div>")
    grid = f"<div style='position:absolute;left:58px;right:58px;top:440px;'>{rows}</div>"
    return bg+L.logo_tl()+_badge("TIER LIST",GREEN)+_eyebrow("REAL TALK")+title+grid+L.url_footer()+L.watermark(op=.04)

# ---- starter pack ----
def w_starterpack(idea):
    items = [("briefcase","One (1) blazer"), ("doc","A notebook you'll use twice"),
             ("user","A LinkedIn banner you overthought"), ("rocket","3-day-old confidence"),
             ("clock","Arriving painfully early"), ("chat","'Just circling back' emails")]
    bg = "<div style='position:absolute;inset:0;background:#F3EADA;'></div>"
    tex = "<div style='position:absolute;inset:0;opacity:.5;background-image:radial-gradient(rgba(138,123,98,.12) 1.5px,transparent 1.5px);background-size:30px 30px;'></div>"
    title = (f"<div style=\"position:absolute;left:58px;top:236px;font-family:Inter;font-weight:800;font-size:58px;"
             f"line-height:1.04;letter-spacing:-1.5px;color:#152743;\">The &lsquo;I&rsquo;m basically a pro<br>now&rsquo; starter pack</div>")
    tints = [AMBER, CORAL, GREEN, BLUE, AMBER, CORAL]
    tiles = ""
    for i, (icon, txt) in enumerate(items):
        ac = tints[i]
        tiles += (f"<div style='display:flex;gap:16px;align-items:center;background:#fff;border-radius:18px;"
                  f"box-shadow:0 14px 30px rgba(20,30,50,.1);padding:20px 22px;'>"
                  f"<div style='flex:0 0 56px;width:56px;height:56px;border-radius:14px;background:{ac}22;border:2px solid {ac};"
                  f"display:flex;align-items:center;justify-content:center;'>{L.svg(icon,ac,28)}</div>"
                  f"<span style=\"font-family:Inter;font-weight:700;font-size:26px;color:#1c2740;line-height:1.14;\">{txt}</span></div>")
    grid = (f"<div style='position:absolute;left:58px;right:58px;top:440px;display:grid;grid-template-columns:1fr 1fr;gap:18px;'>{tiles}</div>")
    darklogo = f"<div style='position:absolute;left:56px;top:44px;'><img src='{L.DARKLOGO}' style='height:{L.LOGO}px;'></div>"
    return bg+tex+darklogo+_badge("STARTER PACK",AMBER)+_eyebrow_dark("REAL TALK")+title+grid+_footer_dark()

def _eyebrow_dark(txt, top=196):
    return (f"<div style=\"position:absolute;left:58px;top:{top}px;font-family:'DM Sans';font-weight:700;"
            f"font-size:22px;color:{CORAL};letter-spacing:5px;\">{txt}</div>")
def _footer_dark():
    return (f"<div style='position:absolute;left:56px;bottom:44px;display:flex;align-items:center;gap:13px;'>"
            f"<div style='width:34px;height:34px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;'>"
            f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{DEEP}' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
            f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:#8A7B62;letter-spacing:1px;\">internwise.co.uk</span></div>")

# ---- POV ----
def w_pov(idea):
    bg = f"<div style='position:absolute;inset:0;background:radial-gradient(90% 80% at 50% 20%,#1c4d3a,{DEEP} 70%);'></div>"
    tag = (f"<div style='position:absolute;left:0;right:0;top:300px;text-align:center;font-family:Inter;font-weight:800;"
           f"font-size:34px;color:{GREEN};letter-spacing:4px;'>POV:</div>")
    body = (f"<div style='position:absolute;left:90px;right:90px;top:360px;text-align:center;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:70px;line-height:1.12;letter-spacing:-1.5px;color:{INK};word-break:keep-all;\">"
            f"you just got the &lsquo;we&rsquo;d love to offer you the role&rsquo; email</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:30px;color:{MUT};margin-top:30px;\">The screenshot-to-group-chat speed run begins.</div></div>")
    return bg+_confetti()+L.logo_tl()+_badge("POV",GREEN)+tag+body+L.url_footer()

# ---- green flags ----
def w_greenflags(idea):
    items = idea.get("items", [])
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,#123528,{DEEP});'></div>"
    title = (f"<div style=\"position:absolute;left:58px;top:236px;font-family:Inter;font-weight:800;font-size:60px;"
             f"line-height:1.04;letter-spacing:-1.5px;color:{INK};\">Green flags in a<br>good internship</div>")
    rows = ""
    for it in items:
        rows += (f"<div style='display:flex;gap:18px;align-items:center;margin-bottom:20px;'>"
                 f"<div style='flex:0 0 52px;width:52px;height:52px;border-radius:50%;background:{GREEN}1f;border:2px solid {GREEN};"
                 f"display:flex;align-items:center;justify-content:center;'>{L.svg('check',GREEN,28)}</div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:31px;color:{INK};letter-spacing:-.3px;\">{it}</span></div>")
    grid = f"<div style='position:absolute;left:58px;right:64px;top:420px;'>{rows}</div>"
    return bg+L.logo_tl()+_badge("GREEN FLAGS",GREEN)+_eyebrow("KNOW YOUR WORTH")+title+grid+L.url_footer()


# ---- tab stack ----
def w_tabstack(idea):
    tabs = idea.get("tabs") or ["CV v12 FINAL", "Company reviews", "LinkedIn profile", "Deadline tracker"]
    bg = "<div style='position:absolute;inset:0;background:#F3EADA;'></div>"
    paper = ("<div style='position:absolute;inset:0;opacity:.55;"
             "background-image:radial-gradient(rgba(21,39,67,.10) 1.5px,transparent 1.5px);background-size:34px 34px;'></div>")
    browser = (f"<div style='position:absolute;left:58px;right:58px;top:286px;height:612px;border-radius:22px;"
               f"background:#fff;box-shadow:0 28px 65px rgba(21,39,67,.18);overflow:hidden;border:3px solid #152743;'>"
               f"<div style='height:78px;background:#152743;display:flex;align-items:center;gap:13px;padding:0 26px;'>"
               f"<span style='width:18px;height:18px;border-radius:50%;background:{CORAL};'></span>"
               f"<span style='width:18px;height:18px;border-radius:50%;background:{AMBER};'></span>"
               f"<span style='width:18px;height:18px;border-radius:50%;background:{GREEN};'></span></div></div>")
    cards = ""
    colors = [AMBER, CORAL, GREEN, BLUE, AMBER, CORAL]
    for i, tab in enumerate(tabs[:6]):
        top = 374 + i * 76
        left = 104 + (i % 2) * 24
        rot = [-1.2, .9, -.7, 1.1, -.9, .6][i]
        cards += (f"<div style='position:absolute;left:{left}px;right:{104 - (i % 2) * 40}px;top:{top}px;"
                  f"height:64px;border-radius:14px;background:#F8FBFF;border:2px solid #152743;"
                  f"box-shadow:0 12px 26px rgba(21,39,67,.12);transform:rotate({rot}deg);"
                  f"display:flex;align-items:center;gap:18px;padding:0 24px;'>"
                  f"<div style='width:34px;height:34px;border-radius:10px;background:{colors[i]};display:flex;align-items:center;justify-content:center;"
                  f"font-family:Inter;font-weight:900;font-size:18px;color:#152743;'>{i+1}</div>"
                  f"<div style=\"font-family:Inter;font-weight:800;font-size:30px;color:#152743;letter-spacing:-.5px;\">{tab}</div></div>")
    title = (f"<div style=\"position:absolute;left:58px;top:166px;width:720px;font-family:Inter;font-weight:900;"
             f"font-size:60px;line-height:1.02;letter-spacing:-1.7px;color:#152743;\">How many job-search tabs is too many?</div>")
    note = (f"<div style='position:absolute;right:76px;top:188px;width:210px;transform:rotate(3deg);"
            f"background:{AMBER};padding:18px 20px;box-shadow:0 14px 26px rgba(21,39,67,.16);'>"
            f"<div style=\"font-family:Georgia,serif;font-weight:700;font-style:italic;font-size:31px;line-height:1;color:#152743;\">all of them.</div></div>")
    closer = (f"<div style=\"position:absolute;left:58px;bottom:104px;font-family:'DM Sans';font-weight:800;"
              f"font-size:30px;color:#152743;\">Save the role before the tab disappears.</div>")
    darklogo = f"<div style='position:absolute;left:56px;top:44px;'><img src='{L.DARKLOGO}' style='height:{L.LOGO}px;'></div>"
    return bg + paper + darklogo + _badge("REAL TALK", AMBER) + title + note + browser + cards + closer + _footer_dark()


WORLDS = {"bingo": w_bingo, "tierlist": w_tierlist, "starterpack": w_starterpack,
          "pov": w_pov, "greenflags": w_greenflags, "tabstack": w_tabstack}

def render_fun(idea, world, out_dir, filename="slide_1.png"):
    return L.render(out_dir, filename, WORLDS[world](idea))


if __name__ == "__main__":
    ideas = {i["format"]: i for i in L.load("fun_ideas.json")["ideas"]}
    demo = {"bingo": ideas.get("bingo", {}), "tierlist": ideas.get("tier_list", {}),
            "starterpack": ideas.get("checklist", {}), "pov": ideas.get("pov", {}),
            "greenflags": ideas.get("green_flags", {}), "tabstack": ideas.get("tab_stack", {})}
    for world, idea in demo.items():
        render_fun(idea, world, os.path.join(L.OUTROOT, "week14", "_ftest", world))
