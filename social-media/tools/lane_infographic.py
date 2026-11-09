"""Infographic lane - a single tall 4:5 card that carries a whole framework.

Replaces the engagement/conversation lane. Where that lane asked one question on
a square card, this lane answers one in full: a dense, saveable reference card of
the kind people screenshot and come back to.

Canvas is 1080x1350 (4:5), the tallest ratio Instagram shows uncropped in feed,
so the card gets ~25% more vertical room than the square lanes without being
cropped on any network.

Visual vocabulary, so the card reads as an infographic and not a text table:
  - Nuno photo cutout bleeding into the navy masthead, with rotated sticker
    callouts overlapping him (brand character; assets/nuno).
  - A circular icon chip on every single line, coloured per block.
  - Chevron arrows for the decode rows and a chevron ribbon for the framework,
    so the eye is pushed left-to-right rather than down a list.
  - Sparkles, dot fields, and a large faint icon watermark behind each block.

Content is a SPEC dict so the writer can generate it later; nothing about the
layout is topic-specific. Density is capped at four blocks - the reference
infographics that carry eight only work when the viewer can zoom, and a feed
card has to read at thumb size.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L

W, H = 1080, 1350

NAVY, DEEP, AMBER = L.NAVY, L.DEEP, L.AMBER
CORAL, GREEN = L.CORAL, L.GREEN
CREAM, PURPLE, SKY, MINT = "#FAF5EC", "#7B5CE6", "#5FA7E5", "#7FDBB6"


ADVERT = {
    "kicker": "APPLICATION SKILLS",
    "title": "Read a Job Advert",
    "title_hero": "Like a Recruiter",
    "sub": "What the wording really tells you — before you spend an hour applying.",
    "nuno": "nuno_job_description",
    "sticky": "What does it\nactually say?",
    "decode": {
        "label": "What the words actually mean",
        "icon": "search",
        "rows": [
            ("clock",   "“Fast-paced environment”", "Understaffed, or genuinely busy"),
            ("briefcase", "“Wear many hats”",        "The role is undefined"),
            ("coin",    "“Competitive salary”",      "No band published — ask for it"),
            ("user",    "“Self-starter”",            "Little training on offer"),
            ("refresh", "“Immediate start”",         "Someone left suddenly; ask why"),
        ],
    },
    "flags": {
        "good": ("Worth your time", "star", [
            ("user", "A named manager or team"),
            ("clipboard", "Clear tasks for week one"),
            ("coin", "Pay and hours stated"),
            ("calendar", "A real closing date"),
        ]),
        "bad": ("Walk away", "flag", [
            ("x", "No pay figure anywhere"),
            ("coin", "“Expenses only” full-time"),
            ("clock", "Pressure to reply today"),
            ("chat", "Personal email, no domain"),
        ]),
    },
    "score": {
        "label": "Score it before you apply",
        "icon": "target",
        "rows": [("coin", "Pay stated"), ("clipboard", "Tasks specific"),
                 ("users", "Training offered"), ("rocket", "Fits your plan")],
        "verdict": "3–4 yes → apply.   2 → ask first.   0–1 → skip it.",
    },
    "footer": "Spend your hour on the advert that respects it.",
}

CV_NO_EXPERIENCE = {
    "kicker": "CV CLINIC",
    "title": "Write a CV When",
    "title_hero": "You Have No Job Yet",
    "sub": "You have more evidence than you think — it is the wording that is failing you.",
    "nuno": "nuno_cv",
    "sticky": "Proof, not\nadjectives!",
    "decode": {
        "label": "Swap the weak line for the real one",
        "icon": "refresh",
        "rows": [
            ("users",     "“Hard-working team player”", "Ran a 4-person group project"),
            ("doc",       "“Good with computers”",      "Built the society booking sheet"),
            ("chat",      "“Excellent communicator”",   "Answered 30+ queries a shift"),
            ("bulb",      "“Fast learner”",             "Trained two new starters"),
            ("search",    "“Attention to detail”",      "Cut till errors to zero"),
        ],
    },
    "flags": {
        "good": ("This counts", "star", [
            ("briefcase", "Part-time and seasonal work"),
            ("doc", "Course and society projects"),
            ("heart", "Volunteering and caring roles"),
            ("rocket", "Anything you built or ran"),
        ]),
        "bad": ("Leave it off", "x", [
            ("calendar", "GCSEs once you have A-levels"),
            ("star", "Hobbies with no detail"),
            ("user", "A photo, age or address"),
            ("eye", "Skills you cannot evidence"),
        ]),
    },
    "score": {
        "label": "Check it before you send",
        "icon": "check",
        "rows": [("trend", "Numbers in it"), ("doc", "One page"),
                 ("target", "Tailored to this"), ("clipboard", "Saved as PDF")],
        "verdict": "4 yes → send it.   2–3 → one more pass.   0–1 → start again.",
    },
    "footer": "Evidence beats adjectives, every time.",
}

# --- November 2026, week 1 (topic evidence: content/infographic_november_prompts.md) ---

MARKETING_ROLES = {
    "kicker": "CAREER MAP",
    "title": "Every Type of",
    "title_hero": "Marketing Role",
    "sub": "What each job actually involves, so you can pick one and aim every application at it.",
    "nuno": "nuno_tablet",
    "sticky": "Which one\nis you?",
    "decode": {
        "label": "The role, and what you would actually do",
        "icon": "search",
        "rows": [
            ("chat",   "Social media executive", "Plans, posts and reports on channels"),
            ("doc",    "Content marketer",       "Writes blogs, emails and scripts"),
            ("search", "SEO / PPC executive",    "Gets the brand found on Google"),
            ("trend",  "Marketing analyst",      "Turns campaign data into decisions"),
            ("users",  "PR and comms assistant", "Pitches stories, looks after press"),
        ],
    },
    "flags": {
        "good": ("Start here, no experience", "rocket", [
            ("briefcase", "Marketing assistant"),
            ("chat", "Social media intern"),
            ("doc", "Content executive"),
            ("users", "Events assistant"),
        ]),
        "bad": ("Myths to drop", "x", [
            ("doc", "You need a marketing degree"),
            ("star", "It is all creative work"),
            ("clock", "You need two years first"),
            ("eye", "Followers count as skills"),
        ]),
    },
    "score": {
        "label": "Ready to apply?",
        "icon": "target",
        "rows": [("target", "Picked one role"), ("doc", "Made one sample"),
                 ("bulb", "Learnt one tool"), ("eye", "Studied 3 brands")],
        "verdict": "4 yes → apply now.   2–3 → one more week.   0–1 → pick a role first.",
    },
    "footer": "Pick one lane. Apply like you mean it.",
}

DEADLINES_2027 = {
    "kicker": "DEADLINE WATCH",
    "title": "Your 2027 Internship",
    "title_hero": "Deadline Map",
    "sub": "Summer 2027 places are being filled now. Here is when each sector usually closes.",
    "nuno": "nuno_planning_1",
    "sticky": "Rolling means\napply now!",
    "decode": {
        "label": "When each sector usually closes",
        "icon": "calendar",
        "rows": [
            ("coin",      "Banking and finance",   "Earliest: many shut Oct to Nov"),
            ("doc",       "Law vacation schemes",  "Spring and summer: Dec to Jan"),
            ("rocket",    "Tech and engineering",  "Often rolling; some close 1 Dec"),
            ("briefcase", "Consulting and Big 4",  "Rolling: places fill as they go"),
            ("users",     "Graduate schemes",      "Mostly rolling: early is better"),
        ],
    },
    "flags": {
        "good": ("Apply this month", "clock", [
            ("coin", "Finance roles still open"),
            ("doc", "Law spring and summer schemes"),
            ("rocket", "STEM schemes due 1 Dec"),
            ("briefcase", "Anything marked rolling"),
        ]),
        "bad": ("Deadline traps", "flag", [
            ("calendar", "Rolling = first come"),
            ("clock", "Closing early when full"),
            ("x", "Trusting old tracker dates"),
            ("eye", "Missing test invite windows"),
        ]),
    },
    "score": {
        "label": "Before you submit",
        "icon": "check",
        "rows": [("doc", "CV tailored"), ("chat", "Cover letter ready"),
                 ("calendar", "Date checked"), ("target", "Tests practised")],
        "verdict": "4 yes → submit.   2–3 → finish tonight.   0–1 → start with the CV.",
    },
    "footer": "Always check the date on the employer's own careers page.",
}

WORK_EXPERIENCE = {
    "kicker": "CV QUESTION",
    "title": "Does an Internship",
    "title_hero": "Count as Experience?",
    "sub": "Short answer: yes. Here is what counts, and how to write it so recruiters notice.",
    "nuno": "nuno_cv_proof_highlight",
    "sticky": "Yes, it\ncounts!",
    "decode": {
        "label": "What counts, and where it goes",
        "icon": "check",
        "rows": [
            ("coin",     "Paid internship",    "Yes: list it under Experience"),
            ("heart",    "Unpaid internship",  "Yes: same section, same detail"),
            ("calendar", "Placement year",     "Yes: often your strongest entry"),
            ("eye",      "Work shadowing",     "Partly: list it as an insight week"),
            ("users",    "Volunteering",       "Yes, if you did real tasks"),
        ],
    },
    "flags": {
        "good": ("Write it like this", "star", [
            ("trend", "Lead with a result"),
            ("target", "Use your real job title"),
            ("clock", "Give dates and length"),
            ("doc", "Name the tools you used"),
        ]),
        "bad": ("Not like this", "x", [
            ("x", "“Helped with various tasks”"),
            ("eye", "Hidden under Education"),
            ("clipboard", "Duties with no results"),
            ("star", "Shadowing called a job"),
        ]),
    },
    "score": {
        "label": "Is your entry strong?",
        "icon": "target",
        "rows": [("trend", "Has a number"), ("target", "Matches the advert"),
                 ("doc", "Two or three bullets"), ("calendar", "Title and dates")],
        "verdict": "4 yes → it is working.   2–3 → add a result.   0–1 → rewrite it.",
    },
    "footer": "Experience is what you did, not what you were paid.",
}

EMPLOYER_AD = {
    "kicker": "FOR EMPLOYERS",
    "title": "Write an Internship Ad",
    "title_hero": "That Gets Applicants",
    "sub": "Students read the pay, the tasks and the dates first. Put them where they can see them.",
    "nuno": "nuno_welcoming_1",
    "sticky": "Pay first,\nperks later",
    "decode": {
        "label": "Swap the vague line for the clear one",
        "icon": "refresh",
        "rows": [
            ("star",      "“Rockstar wanted”",       "Marketing intern, 12 weeks"),
            ("coin",      "“Competitive salary”",    "£12.71 an hour, paid monthly"),
            ("rocket",    "“Fast-paced startup”",    "Five-person team, weekly launches"),
            ("clipboard", "“Ad hoc tasks”",          "Run our Instagram, 3 posts a week"),
            ("calendar",  "“Immediate start”",       "Starts 12 Jan, 3 days a week"),
        ],
    },
    "flags": {
        "good": ("Candidates look for", "star", [
            ("coin", "Pay and hours stated"),
            ("user", "A named mentor"),
            ("bulb", "What they will learn"),
            ("calendar", "Start date and length"),
        ]),
        "bad": ("Puts them off", "x", [
            ("x", "No pay figure anywhere"),
            ("clipboard", "Ten bullets of must-haves"),
            ("clock", "Two years' experience asked"),
            ("eye", "No idea what week one is"),
        ]),
    },
    "score": {
        "label": "Before you post",
        "icon": "check",
        "rows": [("coin", "Pay stated"), ("clipboard", "Tasks named"),
                 ("user", "Mentor named"), ("calendar", "Dates clear")],
        "verdict": "4 yes → post it.   2–3 → fill the gaps.   0–1 → rewrite it.",
    },
    "footer": "Post your internship where 14,000+ UK employers already hire.",
}

TELL_ME = {
    "kicker": "INTERVIEW SKILLS",
    "title": "Tell Me About Yourself",
    "title_hero": "in 60 Seconds",
    "sub": "Every interview opens with it. Use a structure, not your life story.",
    "nuno": "nuno_welcoming_2",
    "sticky": "Now, proof,\nthen why you",
    "decode": {
        "label": "Swap the ramble for the formula",
        "icon": "refresh",
        "rows": [
            ("user",   "“I was born in…”",         "Start with now: course and focus"),
            ("star",   "“I'm a hard worker”",      "Give one proof, with a number"),
            ("doc",    "Your whole CV, in order",  "Pick two things that fit this role"),
            ("target", "“I just need a job”",      "Say why this role, this company"),
            ("clock",  "Five minutes long",        "60 to 90 seconds, then stop"),
        ],
    },
    "flags": {
        "good": ("Put this in", "star", [
            ("user", "Who you are right now"),
            ("trend", "One result you are proud of"),
            ("target", "Why this role fits"),
            ("chat", "A clean ending line"),
        ]),
        "bad": ("Leave this out", "x", [
            ("heart", "Your full life story"),
            ("coin", "Salary or holidays"),
            ("x", "Moaning about a past job"),
            ("doc", "Reading out your CV"),
        ]),
    },
    "score": {
        "label": "The 60-second check",
        "icon": "clock",
        "rows": [("user", "Starts with now"), ("trend", "Has one number"),
                 ("target", "Names the role"), ("clock", "Under 90 seconds")],
        "verdict": "4 yes → you are ready.   2–3 → practise aloud.   0–1 → rewrite it.",
    },
    "footer": "Say it out loud three times before the interview.",
}

TOPICS = {"advert": ADVERT, "cv": CV_NO_EXPERIENCE,
          "01_marketing_roles": MARKETING_ROLES, "02_deadlines": DEADLINES_2027,
          "03_work_experience": WORK_EXPERIENCE, "04_employer_ad": EMPLOYER_AD,
          "05_tell_me": TELL_ME}
SPEC = ADVERT

CSS = """
.r{background:#FAF5EC;font-family:'DM Sans',sans-serif;}
.card{position:absolute;border:3px solid #0A1830;border-radius:20px;
      box-shadow:7px 7px 0 #0A1830;overflow:hidden;}
.hd{font-family:'Inter',sans-serif;font-weight:800;letter-spacing:-.6px;}
.bar{position:absolute;top:0;left:0;width:7px;height:100%;}
.chip{flex:none;display:flex;align-items:center;justify-content:center;
      border-radius:50%;border:2.5px solid #0A1830;}
.sticky{position:absolute;font-family:'DM Sans';font-weight:700;font-style:italic;
        line-height:1.2;border:2.5px solid #0A1830;box-shadow:4px 5px 0 rgba(10,24,48,.55);}
.wm{position:absolute;pointer-events:none;}
"""


def _sp(x, y, s=22, c="#FFB120", op=.9, rot=0):
    """Four-pointed sparkle."""
    return (f"<svg style='position:absolute;left:{x}px;top:{y}px;opacity:{op};"
            f"transform:rotate({rot}deg);' width='{s}' height='{s}' viewBox='0 0 24 24'>"
            f"<path d='M12 0c.6 7 4.4 11 12 12-7.6 1-11.4 5-12 12-.6-7-4.4-11-12-12 7.6-1 11.4-5 12-12z'"
            f" fill='{c}'/></svg>")


def _chip(icon, bg, sz=40, isz=21, stroke="#0A1830"):
    return (f"<div class='chip' style='width:{sz}px;height:{sz}px;background:{bg};'>"
            f"{L.svg(icon, stroke, isz)}</div>")


def _wm(icon, x, y, s, c, op=.07):
    return (f"<div class='wm' style='left:{x}px;top:{y}px;opacity:{op};'>"
            f"{L.svg(icon, c, s)}</div>")


def _sticky(text, x, y, rot, bg=AMBER, w=172, fs=19):
    body = text.replace("\n", "<br>")
    return (f"<div class='sticky' style='left:{x}px;top:{y}px;width:{w}px;background:{bg};"
            f"color:{DEEP};font-size:{fs}px;padding:13px 15px;border-radius:6px;"
            f"transform:rotate({rot}deg);z-index:18;'>{body}</div>")


def _head(x, y, n, label, accent, icon, col="#0A1830"):
    """Numbered disc + icon chip + block title."""
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;display:flex;"
            f"align-items:center;gap:13px;z-index:4;'>"
            f"<div style='width:36px;height:36px;border-radius:50%;background:{accent};"
            f"border:2.5px solid {DEEP};display:flex;align-items:center;justify-content:center;"
            f"font-family:\"Inter\";font-weight:800;font-size:19px;color:{DEEP};'>{n}</div>"
            f"<div class='hd' style='font-size:26px;color:{col};'>{label}</div>"
            f"{L.svg(icon, accent, 25)}</div>")


def build(spec=SPEC, out_dir=None, filename="infographic.png"):
    s = spec
    o = []

    # ============================== masthead 0-300 ==============================
    o.append(f"<div style='position:absolute;left:0;top:0;width:{W}px;height:300px;background:{NAVY};'>"
             f"<div style='position:absolute;inset:0;background-image:radial-gradient("
             f"rgba(255,255,255,.05) 1px,transparent 1px);background-size:3px 3px;'></div></div>")
    o.append(L.dots("left:612px;top:236px;", "rgba(255,177,32,.33)", 300, 56))
    # Nuno cutout, bottom-aligned to the masthead edge.
    o.append(f"<img src='{L.nuno_src(s['nuno'])}' style='position:absolute;right:26px;bottom:1052px;"
             f"height:258px;z-index:6;filter:drop-shadow(-10px 6px 16px rgba(0,0,0,.45));'>")
    o.append(_sticky(s["sticky"], 648, 150, -7))
    o.append(_sp(596, 92, 26, AMBER, .95, 10) + _sp(1016, 44, 19, MINT, .9, -14)
             + _sp(566, 214, 15, CORAL, .85, 22))
    o.append(f"<img src='{L.WHT}' style='position:absolute;left:40px;top:26px;height:46px;opacity:.95;'>")
    o.append(f"<div style='position:absolute;left:40px;top:92px;background:{AMBER};color:{DEEP};"
             f"font-family:\"DM Sans\";font-weight:800;font-size:14px;letter-spacing:2.6px;"
             f"padding:7px 16px;border-radius:40px;transform:rotate(-1.5deg);'>{s['kicker']}</div>")
    o.append(f"<div class='hd' style='position:absolute;left:40px;top:132px;width:600px;font-size:50px;"
             f"line-height:1.0;color:#fff;letter-spacing:-2px;'>{s['title']}<br>"
             f"<span style='color:{AMBER};'>{s['title_hero']}</span></div>")
    o.append(f"<div style='position:absolute;left:42px;top:248px;width:560px;font-size:18px;"
             f"color:#B9CFE9;line-height:1.3;'>{s['sub']}</div>")

    # ============================ 1. decode 312-688 =============================
    d = s["decode"]
    rows = []
    for i, (icon, phrase, mean) in enumerate(d["rows"]):
        top = 68 + i * 61
        tint = "#F4F8FD" if i % 2 == 0 else "#FFFFFF"
        rows.append(
            f"<div style='position:absolute;left:20px;top:{top}px;width:{W-100}px;height:55px;"
            f"background:{tint};border-radius:12px;display:flex;align-items:center;gap:12px;"
            f"padding:0 13px;'>"
            f"{_chip(icon, SKY, 36, 19)}"
            f"<div style='width:276px;font-weight:700;font-size:19px;color:{NAVY};"
            f"font-style:italic;line-height:1.15;'>{phrase}</div>"
            f"<div style='flex:none;width:34px;height:22px;background:{AMBER};"
            f"clip-path:polygon(0 22%,62% 22%,62% 0,100% 50%,62% 100%,62% 78%,0 78%);'></div>"
            f"<div style='flex:1;font-size:18px;color:#24405F;line-height:1.2;'>{mean}</div></div>")
    body = _wm(d["icon"], 862, 286, 150, SKY, .09) + "".join(rows)
    o.append(f"<div class='card' style='left:30px;top:312px;width:{W-60}px;height:376px;background:#fff;'>"
             f"<div class='bar' style='background:{SKY};'></div>{body}</div>")
    o.append(_head(54, 332, 1, d["label"], SKY, d["icon"]))

    # ========================== 2+3. flags 700-986 ==============================
    def _flagcard(x, label, icon, items, accent, bg, n):
        rows = []
        for i, (ic_, t) in enumerate(items):
            rows.append(f"<div style='position:absolute;left:20px;top:{66+i*52}px;width:420px;"
                        f"display:flex;align-items:center;gap:11px;'>"
                        f"{_chip(ic_, accent, 33, 17)}"
                        f"<div style='font-size:18px;color:{NAVY};line-height:1.2;'>{t}</div></div>")
        inner = _wm(icon, 352, 182, 110, accent, .1) + "".join(rows)
        return (f"<div class='card' style='left:{x}px;top:700px;width:502px;height:286px;background:{bg};'>"
                f"<div class='bar' style='background:{accent};'></div>{inner}</div>"), _head(x+24, 718, n, label, accent, icon)

    gl, gic, gi = s["flags"]["good"]
    bl, bic, bi = s["flags"]["bad"]
    c, h = _flagcard(30, gl, gic, gi, GREEN, "#F1FBF6", 2); o += [c, h]
    c, h = _flagcard(548, bl, bic, bi, CORAL, "#FEF3F3", 3); o += [c, h]
    o.append(_sp(540, 964, 20, PURPLE, .8, 12))

    # =========================== 4. framework 998-1256 ==========================
    sc = s["score"]
    seg = []
    cols = [MINT, SKY, AMBER, "#C9B6F5"]
    for i, (ic_, t) in enumerate(sc["rows"]):
        x = 22 + i * 244
        notch = ("polygon(0 0,calc(100% - 22px) 0,100% 50%,calc(100% - 22px) 100%,0 100%)"
                 if i == 0 else
                 "polygon(0 0,calc(100% - 22px) 0,100% 50%,calc(100% - 22px) 100%,0 100%,22px 50%)")
        seg.append(f"<div style='position:absolute;left:{x}px;top:62px;width:240px;height:74px;"
                   f"background:{cols[i]};clip-path:{notch};display:flex;align-items:center;"
                   f"gap:10px;padding-left:{18 if i==0 else 34}px;'>"
                   f"{_chip(ic_, '#FFFFFF', 34, 18)}"
                   f"<div style='font-family:\"Inter\";font-weight:800;font-size:17px;color:{DEEP};"
                   f"line-height:1.1;letter-spacing:-.3px;'>{t}</div></div>")
    seg.append(f"<div style='position:absolute;left:22px;top:154px;width:{W-104}px;height:50px;"
               f"background:{AMBER};border:2.5px solid {DEEP};border-radius:12px;display:flex;"
               f"align-items:center;justify-content:center;font-family:\"Inter\";font-weight:800;"
               f"font-size:19px;color:{DEEP};letter-spacing:-.2px;'>{sc['verdict']}</div>")
    o.append(f"<div class='card' style='left:30px;top:998px;width:{W-60}px;height:258px;background:{CREAM};'>"
             f"<div class='bar' style='background:{PURPLE};'></div>"
             f"{_wm(sc['icon'], 884, 150, 130, PURPLE, .08)}{''.join(seg)}</div>")
    o.append(_head(54, 1016, 4, sc["label"], PURPLE, sc["icon"]))

    # ================================ footer ====================================
    o.append(f"<div style='position:absolute;left:0;bottom:0;width:{W}px;height:94px;background:{NAVY};"
             f"display:flex;align-items:center;justify-content:space-between;padding:0 40px;'>"
             f"<div style='font-size:19px;color:#CBDCF0;font-weight:500;'>{s['footer']}</div>"
             f"<div style='font-family:\"Inter\";font-weight:800;font-size:19px;color:{AMBER};'>{L.URL}</div>"
             f"</div>")
    o.append(_sp(498, 1272, 17, AMBER, .5, 8))

    out_dir = out_dir or os.path.join(L.BASE, "test_output_infographic")
    return L.render(out_dir, filename, "".join(o), CSS, w=W, h=H)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Render one infographic-lane card.")
    ap.add_argument("--topic", default="advert", choices=sorted(TOPICS))
    a = ap.parse_args()
    build(TOPICS[a.topic], filename=f"infographic_{a.topic}.png")
