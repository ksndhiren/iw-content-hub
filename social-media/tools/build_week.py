"""Week 14 (w/c 31 Aug 2026) orchestrator - non-education lanes.

Renders the 20 non-education posts (5 days x news/quote/fun/employer), each in a
rotating design world, and patches the day-based `data/weeks.json`. Education
(5 bespoke posts) is added separately later to complete each day's 5.

    python3 tools/build_week.py            # render + patch weeks.json
    python3 tools/build_week.py --dry      # render only, no weeks.json write
"""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L
import lane_quote, lane_fun, lane_employer, news_card

HUB   = os.path.dirname(L.BASE)                       # iw-content-hub
IMG   = os.path.join(HUB, "images", "week14")
WEEKS = os.path.join(HUB, "data", "weeks.json")
WID   = "week14"

DAYS = [("mon", "Mon 31 Aug"), ("tue", "Tue 1 Sep"), ("wed", "Wed 2 Sep"),
        ("thu", "Thu 3 Sep"), ("fri", "Fri 4 Sep")]

# ----- content assignments (world/pose/quote rotate so nothing repeats) -----
QUOTE = [("editorial", "q001"), ("spotlight", "q002"), ("colorblock", "q003"),
         ("split", "q004"), ("paper", "q005")]
FUN = [("bingo", "bingo"), ("tierlist", "tier_list"), ("greenflags", "green_flags"),
       ("pov", "pov"), ("starterpack", "checklist")]
EMPLOYER = [("benefits", "e001"), ("bigstat", "e004"), ("process", "e003"),
            ("trust", "e005"), ("statement", "e002")]

# News: real current stories, ALL copy reworded in Internwise's voice (no paste).
NEWS = [
    {"kicker": "JOB MARKET", "title": "Graduate vacancies slump to a decade low",
     "brief": ["New figures point to one of the toughest graduate markets in years - recruitment data suggests only around 8,000 graduate roles were advertised in July, the fewest since 2016.",
               "It is a hard backdrop for this year's leavers, but not a hopeless one. When fewer roles are advertised, applying early, searching wider and showing real proof of skills matter more than ever.",
               "Internships are one of the clearest routes through a squeeze like this: they build experience employers can see, and they often lead to a first full-time role."],
     "sidebar": ["Start early and apply consistently", "Widen your search beyond big-name schemes", "Use internships to build real proof"],
     "pull": "Fewer roles means standing out matters more, not less.", "source": "The Guardian / Adzuna"},
    {"kicker": "SKILLS", "title": "Skills are becoming the new currency",
     "brief": ["This summer's education reforms sent a clear signal - technical skills and practical pathways are moving to the centre of how the UK trains and hires.",
               "For students and graduates the takeaway is simple: what you can actually do is starting to matter as much as where you studied.",
               "Internships are one of the fastest ways to turn learning into a demonstrable skill, and to show an employer you can apply it."],
     "sidebar": ["Focus on skills you can demonstrate", "Build a portfolio of real work", "Treat an internship as skill-building"],
     "pull": "What you can do is becoming as important as where you studied.", "source": "FE News"},
    {"kicker": "CAREERS", "title": "A tougher market needs a sharper plan",
     "brief": ["With hiring slower than usual, this year's cohort faces a real question: how to aim their energy so it actually lands.",
               "The answer is rarely 'apply to everything'. It is a focused search - fewer, better-matched applications, backed by evidence of skill.",
               "A well-chosen internship narrows the gap between study and work, and gives your applications something concrete to point to."],
     "sidebar": ["Target roles that fit, not every role", "Quality applications over quantity", "Let an internship give you proof"],
     "pull": "In a slow market, focus beats volume.", "source": "FE News"},
    {"kicker": "SKILLS", "title": "Employers are hungry for tech skills",
     "brief": ["Fresh investment in tech-skills training across UK regions underlines what employers keep saying - demand for digital and technical ability is only growing.",
               "You do not need a computer science degree to benefit. Practical, job-ready tech skills are increasingly valued across almost every sector.",
               "An internship is a low-risk way to build those skills on real projects, and to prove them to your next employer."],
     "sidebar": ["Build job-ready digital skills", "You don't need a tech degree to start", "Prove skills on real projects"],
     "pull": "Digital skills are in demand across every sector, not just tech.", "source": "FE News"},
    {"kicker": "JOB MARKET", "title": "When big employers trim, read it right",
     "brief": ["Headlines about large-scale job cuts at major firms can be unsettling when you are just starting out.",
               "But restructures at big companies rarely close the door on early-career talent - they often shift where the opportunities are, toward smaller, faster-growing teams.",
               "Internships at growing companies are a smart place to look when the giants are cutting back."],
     "sidebar": ["Don't be put off by big-company cuts", "Look at smaller, growing teams", "Internships open doors headlines miss"],
     "pull": "When the giants trim, growing teams are where early-career doors open.", "source": "Personnel Today"},
]

TAGS = {
    "news":     {"ig-fb": ["#GraduateJobs", "#UKJobs", "#JobMarket", "#Careers", "#Internships", "#Internwise"],
                 "linkedin": ["#GraduateJobs", "#JobMarket", "#EarlyCareers"], "x": ["#GraduateJobs", "#UKJobs"]},
    "quote":    {"ig-fb": ["#CareerMotivation", "#Internships", "#GraduateJobs", "#CareerAdvice", "#Internwise"],
                 "linkedin": ["#CareerAdvice", "#Internships"], "x": ["#CareerMotivation", "#Internships"]},
    "fun":      {"ig-fb": ["#InternLife", "#GraduateLife", "#JobHunt", "#Relatable", "#Internwise"],
                 "linkedin": ["#EarlyCareers", "#JobHunt"], "x": ["#InternLife", "#JobHunt"]},
    "employer": {"ig-fb": ["#Hiring", "#Internships", "#EarlyCareers", "#Recruitment", "#Internwise"],
                 "linkedin": ["#Hiring", "#EarlyCareers", "#Recruitment"], "x": ["#Hiring", "#Internships"]},
}


def _cap_news(n):
    body = " ".join(n["brief"])
    igfb = (f"\U0001F4F0 {n['title']}.\n\n{body}\n\nRead the full story - link in bio.\n\n"
            f"Source: {n['source']}.")
    li = f"{n['title']}.\n\n{body}\n\nRead more: internwise.co.uk\n\nSource: {n['source']}."
    x = f"{n['title']}. {n['brief'][1][:120].rsplit(' ',1)[0]}... internwise.co.uk (via {n['source']})"
    return {"ig-fb": igfb, "linkedin": li, "x": x}

def _cap_quote(q):
    t, a, cta = q["text"], q["author"], q.get("cta", "internwise.co.uk")
    igfb = f"“{t}”\n- {a}\n\nYour next opportunity starts with one step. Find your internship - link in bio.\n\n\U0001F517"
    li = f"“{t}” - {a}\n\nEvery career starts somewhere. Browse internships and graduate roles at internwise.co.uk"
    x = f"“{t}” - {a}\n\ninternwise.co.uk"
    return {"ig-fb": igfb, "linkedin": li, "x": x}

def _cap_fun(title, line):
    igfb = f"{title} \U0001F643\n\n{line}\n\nLooking for the real thing? Find your internship - link in bio."
    li = f"{title}\n\n{line}\n\nStart your search at internwise.co.uk"
    x = f"{title} {line} internwise.co.uk"
    return {"ig-fb": igfb, "linkedin": li, "x": x}

def _cap_employer(a):
    b = " ".join(a.get("benefits", [a.get("body", "")]))
    igfb = f"\U0001F4BC {a['headline']}.\n\n{a.get('body','')} {b}.\n\nPost your internship - link in bio."
    li = f"{a['headline']}.\n\n{a.get('body','')} {b}.\n\nPost a role and reach early-career talent: internwise.co.uk"
    x = f"{a['headline']}. Reach early-career talent at internwise.co.uk"
    return {"ig-fb": igfb, "linkedin": li, "x": x}


FUN_TITLES = {"bingo": ("Graduate job-hunt bingo", "How many have you ticked off? We've all been there."),
              "tierlist": ("Interview questions, ranked by dread", "Which one makes you sweat the most?"),
              "greenflags": ("Green flags in a good internship", "Know your worth - a good internship gives you real tasks, feedback and fair pay."),
              "pov": ("POV: you just got the offer email", "That screenshot-to-group-chat speed run is unmatched."),
              "starterpack": ("The 'I'm basically a pro now' starter pack", "New job energy is a feeling like no other.")}


def build(dry=False):
    quotes = {q["id"]: q for q in L.load("quotes_bank.json")["quotes"]}
    ideas  = {i["format"]: i for i in L.load("fun_ideas.json")["ideas"]}
    angles = {a["id"]: a for a in L.load("employer_angles.json")["angles"]}
    posts = []

    for di, (dkey, dlabel) in enumerate(DAYS):
        # NEWS
        n = NEWS[di]
        pid = f"w14-{dkey}-news"
        pdate = datetime.datetime(2026, 8, 31) + datetime.timedelta(days=di)   # Mon 31 Aug -> Fri 4 Sep
        news_card.render_news({"kicker": n["kicker"], "date": pdate}, os.path.join(IMG, pid),
                              issue_no=di + 1, headline=n["title"], brief=n["brief"],
                              sidebar=n["sidebar"], pull=n["pull"])
        posts.append(_post(pid, dlabel, "news", n["title"], _cap_news(n), TAGS["news"]))

        # QUOTE
        world, qid = QUOTE[di]; q = quotes[qid]
        pid = f"w14-{dkey}-quote"
        lane_quote.render_quote(q, world, os.path.join(IMG, pid))
        posts.append(_post(pid, dlabel, "quote", f"Quote: {q['author']}", _cap_quote(q), TAGS["quote"]))

        # FUN
        world, fkey = FUN[di]; idea = ideas.get(fkey, {})
        pid = f"w14-{dkey}-fun"
        lane_fun.render_fun(idea, world, os.path.join(IMG, pid))
        ft, fl = FUN_TITLES[world]
        posts.append(_post(pid, dlabel, "fun", ft, _cap_fun(ft, fl), TAGS["fun"]))

        # EMPLOYER
        world, aid = EMPLOYER[di]; a = angles[aid]
        pid = f"w14-{dkey}-employer"
        lane_employer.render_employer(a, world, os.path.join(IMG, pid))
        posts.append(_post(pid, dlabel, "employer", a["headline"], _cap_employer(a), TAGS["employer"]))

    if dry:
        print(f"\nDRY: rendered {len(posts)} posts, weeks.json NOT written.")
        return posts

    data = json.load(open(WEEKS))
    data["weeks"] = [w for w in data["weeks"] if w.get("id") != WID]
    data["weeks"].append({"id": WID, "label": "Week 14", "weekCommencing": "2026-08-31", "posts": posts})
    json.dump(data, open(WEEKS, "w"), indent=2, ensure_ascii=False)
    print(f"\nWrote {len(posts)} posts to {WEEKS} (week14).")
    return posts


def _post(pid, day, lane, title, captions, tags):
    return {"id": pid, "day": day, "lane": lane, "title": title,
            "platform": "Multi-Platform", "format": "Single", "slides": ["slide_1.png"],
            "status": "in-review", "caption": captions["ig-fb"], "hashtags": tags["ig-fb"],
            "captions": captions, "hashtagsByPlatform": tags}


if __name__ == "__main__":
    build(dry="--dry" in sys.argv)
