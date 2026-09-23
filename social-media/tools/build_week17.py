"""Week 17 (w/c 2026-09-21) - hand-authored catch-up build.

Uses the operator-approved copy (search-demand led) + THREE brand-new education
carousel worlds (tabs/marker/flash) and TWO new quote worlds (marquee/stamp) so
every design is a genuinely new art direction (the hard rule: no rotation reuse).
Renders the graphics, records the design + Nuno ledgers, and patches data/weeks.json.

News + employer for the week are handled by their own pipelines (news day-prior;
employer lane) and are not built here. Reels are the two operator-supplied videos.

    python3 tools/build_week17.py
"""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L
import lane_education, lane_quote
import design_ledger, nuno_ledger

WID, WLABEL, WC = "week17", "Week 17", "2026-09-21"
HUB = os.path.dirname(L.BASE)
WEEKS = os.path.join(HUB, "data", "weeks.json")
IMG = os.path.join(HUB, "images", WID)

# ---------------------------------------------------------------- approved copy
EDU = {
    "thu": {
        "world": "tabs",
        "copy": {
            "eyebrow": "WORK EXPERIENCE",
            "headline": "Does your internship count?",
            "tone": "practical",
            "slides": [
                {"tag": "Short answer", "title": "Yes, it counts", "body": "Recruiters treat internships as real experience, if you describe them as proof, not duties."},
                {"tag": "The fix", "title": "Show the result", "body": "Swap \"supported the team\" for \"ran 3 campaigns, lifted open rates 12%.\""},
                {"tag": "On your CV", "title": "Put it up top", "body": "One well-described internship can outweigh months of vague part-time lines. Lead with it."},
            ],
            "cta": "Get experience that counts. Find internships today.",
        },
        "captions": {
            "ig-fb": "Does an internship count as work experience? Yes, and recruiters treat it as real experience when you describe it right. Swap vague duties for proof: what you did, how you did it, and the result it drove. One strong internship can outweigh months of vague lines on a CV. Find internships to build that experience: link in bio. #cvtips #internships #careeradvice #graduatejobs",
            "linkedin": "\"Does an internship count as work experience?\" It's one of the most searched career questions, and the answer is yes. But only if you describe it as evidence, not duties. Replace \"supported the marketing team\" with \"ran 3 email campaigns and lifted open rates 12%.\" Recruiters scan for role fit and results, not responsibility lists. One well-described internship can carry a graduate CV. Find internships at internwise.co.uk. #careeradvice #cvtips #graduatejobs",
            "x": "Does an internship count as work experience? Yes, if you write it as proof, not duties. \"Ran 3 campaigns, +12% open rate\" beats \"supported the team.\" Find internships: internwise.co.uk #cvtips #internships",
        },
        "hashtags": {"ig-fb": ["#cvtips", "#internships", "#careeradvice", "#graduatejobs"],
                     "linkedin": ["#careeradvice", "#cvtips", "#graduatejobs"],
                     "x": ["#cvtips", "#internships"]},
        "day": "Thu 24 Sep",
    },
    "sat": {
        "world": "marker",
        "copy": {
            "eyebrow": "CV CLINIC",
            "headline": "The 'About Me' that gets read",
            "tone": "practical",
            "slides": [
                {"tag": "The problem", "title": "Stop the horoscope", "body": "\"Hardworking, passionate team player\" tells a recruiter nothing about you."},
                {"tag": "The formula", "title": "Be specific", "body": "Who you are, your focus, and the value you bring. In one clear line."},
                {"tag": "Example", "title": "Like this", "body": "\"Final-year marketing student focused on content, ready to turn 3 live campaigns into impact.\""},
            ],
            "cta": "Build a CV that gets read. Start today.",
        },
        "captions": {
            "ig-fb": "Your CV \"About Me\" might be the reason you're not getting shortlisted. \"Hardworking, passionate team player\" tells a recruiter nothing. Try: who you are, your focus, and the value you bring, in one specific line. Specific beats impressive every time. Full guide: link in bio. #cvtips #careeradvice #graduatejobs #internships",
            "linkedin": "The \"About Me\" line on most graduate CVs reads like a horoscope: hardworking, passionate, team player. Recruiters skip it. What works is specificity: who you are, your focus, and the value you bring. \"Final-year marketing student focused on content, looking to turn 3 live campaigns into impact for a growing team\" tells a recruiter everything in one line. Specific beats impressive. More CV tips at internwise.co.uk. #careeradvice #cvtips #graduatejobs",
            "x": "Your CV \"About Me\" is probably too generic. Swap \"hardworking team player\" for who you are + your focus + your value, in one line. Specific beats impressive. internwise.co.uk #cvtips #careeradvice",
        },
        "hashtags": {"ig-fb": ["#cvtips", "#careeradvice", "#graduatejobs", "#internships"],
                     "linkedin": ["#careeradvice", "#cvtips", "#graduatejobs"],
                     "x": ["#cvtips", "#careeradvice"]},
        "day": "Sat 26 Sep",
    },
    "sun": {
        "world": "flash",
        "copy": {
            "eyebrow": "CV CLINIC",
            "headline": "Creative CV: clever or risky?",
            "tone": "practical",
            "slides": [
                {"tag": "It depends", "title": "Where you apply", "body": "A designed CV can stand out, or get auto-rejected. The channel decides."},
                {"tag": "Watch out", "title": "Software scans first", "body": "Applying through an ATS? Keep it simple. Heavy graphics break the scan."},
                {"tag": "When it works", "title": "Small teams notice", "body": "Applying direct to a studio or startup? Clean design can win attention."},
            ],
            "cta": "Content first, design second. Find roles at internwise.co.uk.",
        },
        "captions": {
            "ig-fb": "Creative CV: does it help or hurt? It depends where you're applying. Through recruitment software, heavy graphics can break the scan and get you auto-rejected. Direct to a small team or studio, design can win attention. Rule of thumb: content first, design second, and when unsure, send the clean version. Full breakdown: link in bio. #cvtips #careeradvice #graduatejobs #jobsearch",
            "linkedin": "\"Should I use a creative CV?\" It's a common question with a nuanced answer. If you're applying through applicant tracking software, heavy design often breaks the scan and works against you. If you're applying directly to a small team, studio or startup, a well-designed CV can genuinely stand out. The safe rule: content first, design second, and never let layout hide your evidence. When in doubt, the clean version never counts against you. More at internwise.co.uk. #careeradvice #cvtips #graduatejobs",
            "x": "Creative CV, help or hurt? Through recruitment software: keep it simple or get auto-rejected. Direct to a small team: design can win. Content first, design second. internwise.co.uk #cvtips #jobsearch",
        },
        "hashtags": {"ig-fb": ["#cvtips", "#careeradvice", "#graduatejobs", "#jobsearch"],
                     "linkedin": ["#careeradvice", "#cvtips", "#graduatejobs"],
                     "x": ["#cvtips", "#jobsearch"]},
        "day": "Sun 27 Sep",
    },
}

QUOTES = {
    "wed": {
        "world": "marquee",
        "q": {"text": "Opportunities don't happen. You create them.", "author": "Chris Grosser",
              "cta": "Find your internship at internwise.co.uk"},
        "captions": {
            "ig-fb": "\"Opportunities don't happen. You create them.\" A reminder that the right role rarely lands in your lap, you go and find it. Start creating yours: internships and graduate roles at internwise.co.uk. Link in bio. #careergrowth #internships #graduatejobs #motivation",
            "linkedin": "\"Opportunities don't happen. You create them.\" For students and graduates, that often means putting yourself forward before you feel ready. Internships are one of the clearest ways to create momentum early. Explore roles at internwise.co.uk. #careerdevelopment #internships #graduatesuccess",
            "x": "\"Opportunities don't happen. You create them.\" Go create yours. Internships and graduate roles at internwise.co.uk #careergrowth #internships",
        },
        "hashtags": {"ig-fb": ["#careergrowth", "#internships", "#graduatejobs", "#motivation"],
                     "linkedin": ["#careerdevelopment", "#internships", "#graduatesuccess"],
                     "x": ["#careergrowth", "#internships"]},
        "day": "Wed 23 Sep",
    },
    "sat": {
        "world": "stamp",
        "q": {"text": "The expert in anything was once a beginner.", "author": "Helen Hayes",
              "cta": "Start your career at internwise.co.uk"},
        "captions": {
            "ig-fb": "\"The expert in anything was once a beginner.\" Every career starts somewhere, usually with a first role that teaches more than it pays in status. Find your starting point: internships and graduate roles at internwise.co.uk. Link in bio. #motivation #internships #careergrowth #graduatejobs",
            "linkedin": "\"The expert in anything was once a beginner.\" Worth remembering if you're early in your career and comparing yourself to people 10 years ahead. The goal isn't to skip the start, it's to make a strong one. Internships are a good place to begin: internwise.co.uk. #careerdevelopment #internships #graduatesuccess",
            "x": "\"The expert in anything was once a beginner.\" Make a strong start. Internships and graduate roles at internwise.co.uk #motivation #internships",
        },
        "hashtags": {"ig-fb": ["#motivation", "#internships", "#careergrowth", "#graduatejobs"],
                     "linkedin": ["#careerdevelopment", "#internships", "#graduatesuccess"],
                     "x": ["#motivation", "#internships"]},
        "day": "Sat 26 Sep",
    },
}

REELS = {
    "wed": {
        "video": "IW Reels.mp4", "day": "Wed 23 Sep", "title": "Reel: The simplest way to hire early talent",
        "captions": {
            "ig-fb": "Meet the simplest way to hire early-career talent in the UK. Post a role in minutes, search 400K students and graduates by sector, skills and location, then message and hire in one place. No agencies, no CV pile. Ready to find your next intern? Link in bio. #hiringuk #internships #startuphiring #earlycareers",
            "linkedin": "UK employers spend weeks buried in CVs for one intern hire. It shouldn't be that hard. Internwise lets you post a role in minutes, search 400,000 students and graduates by sector, skills and location, and message candidates directly. Over 14,000 employers already hire this way. See how it works: internwise.co.uk/hire-interns #talentacquisition #earlycareers #ukbusiness",
            "x": "Hiring your first intern shouldn't take weeks. Post a role, search 400K UK students and graduates, message and hire in one place. internwise.co.uk/hire-interns #hiringuk #internships",
        },
        "hashtags": {"ig-fb": ["#hiringuk", "#internships", "#startuphiring", "#earlycareers"],
                     "linkedin": ["#talentacquisition", "#earlycareers", "#ukbusiness"],
                     "x": ["#hiringuk", "#internships"]},
    },
    "fri": {
        "video": "IW Reels 1.mp4", "day": "Fri 25 Sep", "title": "Reel: The CV line recruiters skip",
        "captions": {
            "ig-fb": "Recruiters don't read your CV the way you think. They scan for role fit, then look for proof. The lines that quietly lose interviews are the vague ones that read like a job description. Fix: swap \"responsible for X\" for \"did X, this way, with this result.\" Save this before your next application. More CV tips: link in bio. #cvtips #careeradvice #graduatejobs #jobsearch",
            "linkedin": "Your CV isn't being read the way you think. Recruiters scan for role fit first, then hunt for evidence. The lines that quietly cost you interviews are the vague ones that sound like a job description instead of proof. Replace \"responsible for social media\" with \"grew the channel 20% in 3 months.\" Action, skill, result. Small change, big difference. More at internwise.co.uk. #careeradvice #cvtips #graduatejobs",
            "x": "Recruiters scan your CV for proof, not duties. \"Grew the channel 20% in 3 months\" beats \"responsible for social media.\" Fix this before your next application. internwise.co.uk #cvtips #jobsearch",
        },
        "hashtags": {"ig-fb": ["#cvtips", "#careeradvice", "#graduatejobs", "#jobsearch"],
                     "linkedin": ["#careeradvice", "#cvtips", "#graduatejobs"],
                     "x": ["#cvtips", "#jobsearch"]},
    },
}


def _post(pid, day, lane, title, fmt, slides, captions, hashtags):
    return {"id": pid, "day": day, "lane": lane, "title": title, "platform": "Multi-Platform",
            "format": fmt, "slides": slides, "status": "in-review",
            "caption": captions.get("ig-fb", ""), "hashtags": hashtags.get("ig-fb", []),
            "captions": captions, "hashtagsByPlatform": hashtags}


def main():
    posts = []
    print(f"Building {WID} (w/c {WC})")

    # Wed - Reel A + Quote (marquee)
    r = REELS["wed"]; pid = f"{WID}-wed-reel"
    posts.append(_post(pid, r["day"], "reel", r["title"], "Reel", [], r["captions"], r["hashtags"]))
    posts[-1].update({"videoSource": r["video"], "status": "needs-captions",
                      "note": "Add burned-in captions + 3s hook + end card, then export 1080x1920."})

    qd = QUOTES["wed"]; pid = f"{WID}-wed-quote"
    lane_quote.render_quote(qd["q"], qd["world"], os.path.join(IMG, pid))
    posts.append(_post(pid, qd["day"], "quote", f"Quote: {qd['q']['author']}", "Single",
                       ["slide_1.png"], qd["captions"], qd["hashtags"]))
    posts[-1]["world"] = qd["world"]

    # Thu - Education carousel (tabs)
    ed = EDU["thu"]; pid = f"{WID}-thu-education"
    paths = lane_education.render_education(ed["copy"], ed["world"], os.path.join(IMG, pid), week_id=WID)
    posts.append(_post(pid, ed["day"], "education", ed["copy"]["headline"], "Carousel",
                       [os.path.basename(p) for p in paths], ed["captions"], ed["hashtags"]))
    posts[-1]["world"] = ed["world"]
    posts[-1]["onSlide"] = {k: ed["copy"].get(k) for k in ("eyebrow", "headline", "tone", "slides", "cta")}

    # Fri - Reel B
    r = REELS["fri"]; pid = f"{WID}-fri-reel"
    posts.append(_post(pid, r["day"], "reel", r["title"], "Reel", [], r["captions"], r["hashtags"]))
    posts[-1].update({"videoSource": r["video"], "status": "needs-captions",
                      "note": "Low-res source (480p); re-export at 1080x1920 if possible. Add captions + hook + end card."})

    # Sat - Education carousel (marker) + Quote (stamp)
    ed = EDU["sat"]; pid = f"{WID}-sat-education"
    paths = lane_education.render_education(ed["copy"], ed["world"], os.path.join(IMG, pid), week_id=WID)
    posts.append(_post(pid, ed["day"], "education", ed["copy"]["headline"], "Carousel",
                       [os.path.basename(p) for p in paths], ed["captions"], ed["hashtags"]))
    posts[-1]["world"] = ed["world"]
    posts[-1]["onSlide"] = {k: ed["copy"].get(k) for k in ("eyebrow", "headline", "tone", "slides", "cta")}

    qd = QUOTES["sat"]; pid = f"{WID}-sat-quote"
    lane_quote.render_quote(qd["q"], qd["world"], os.path.join(IMG, pid))
    posts.append(_post(pid, qd["day"], "quote", f"Quote: {qd['q']['author']}", "Single",
                       ["slide_1.png"], qd["captions"], qd["hashtags"]))
    posts[-1]["world"] = qd["world"]

    # Sun - Education carousel (flash)
    ed = EDU["sun"]; pid = f"{WID}-sun-education"
    paths = lane_education.render_education(ed["copy"], ed["world"], os.path.join(IMG, pid), week_id=WID)
    posts.append(_post(pid, ed["day"], "education", ed["copy"]["headline"], "Carousel",
                       [os.path.basename(p) for p in paths], ed["captions"], ed["hashtags"]))
    posts[-1]["world"] = ed["world"]
    posts[-1]["onSlide"] = {k: ed["copy"].get(k) for k in ("eyebrow", "headline", "tone", "slides", "cta")}

    # Record design ledger (hard rule: these worlds are now 'used' for week17)
    design_ledger.record("edu_carousel", WID, ["tabs", "marker", "flash"])
    design_ledger.record("quote", WID, ["marquee", "stamp"])

    # Patch weeks.json
    data = json.load(open(WEEKS))
    data["weeks"] = [w for w in data["weeks"] if w.get("id") != WID]
    built_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    data["weeks"].append({"id": WID, "label": WLABEL, "weekCommencing": WC,
                          "builtAt": built_at, "posts": posts})
    json.dump(data, open(WEEKS, "w"), indent=2, ensure_ascii=False)
    open(WEEKS, "a").write("\n")
    print(f"\nWrote {len(posts)} posts to weeks.json ({WID}).")

    if nuno_ledger.REPEATS:
        need = {}
        for rp in nuno_ledger.REPEATS:
            need[rp["family"]] = need.get(rp["family"], 0) + 1
        print("\nNuno poses REPEATED (need fresh cutouts): "
              + ", ".join(f"{n}x{fam}" for fam, n in need.items()))


if __name__ == "__main__":
    main()
