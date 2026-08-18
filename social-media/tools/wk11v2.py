"""Week 11 v2 - 5 bespoke art directions (CSS/SVG). 3 carousels + 2 singles."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wk11_base as b
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "campaigns", "outputs", "week11")
F = b.fonts()
WHT="data:image/png;base64,"+b.LOGO_W; BLU="data:image/png;base64,"+b.LOGO_B
import base64 as _b64
_ICONPATH=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"assets","iw_icon_mark.svg")
ICON="data:image/svg+xml;base64,"+_b64.b64encode(open(_ICONPATH,"rb").read()).decode()
def wm(w=520,right=-70,bottom=-95,opacity=.05,light=False):
    """Faint logo-icon watermark for slides that are >=50% empty. Bleeds off bottom-right."""
    filt="filter:brightness(0) invert(1);" if light else "filter:brightness(0);"
    return (f"<img src='{ICON}' style='position:absolute;right:{right}px;bottom:{bottom}px;width:{w}px;"
            f"{filt}opacity:{opacity};pointer-events:none;'>")

def R(post, i, inner):
    d=os.path.join(OUT,post); os.makedirs(d,exist_ok=True); path=os.path.join(d,f"slide_{i}.png")
    html=(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{F}*{{margin:0;padding:0;box-sizing:border-box;}}"
          f"body{{width:1080px;height:1080px;overflow:hidden;}}.r{{width:1080px;height:1080px;position:relative;overflow:hidden;}}"
          f"</style></head><body><div class='r'>{inner}</div></body></html>")
    with sync_playwright() as p:
        br=p.chromium.launch(); pg=br.new_page(viewport={"width":1080,"height":1080},device_scale_factor=2)
        pg.set_content(html,wait_until="networkidle"); pg.screenshot(path=path,type="png"); br.close()
    print("  ok",post,i)

MONO="'Courier New',monospace"; SERIF="Georgia,'Times New Roman',serif"
# Uniform logo height across ALL weekly designs (mobile-prominent). Keep identical everywhere.
LOGO=100
# Mobile note: these 1080px graphics are viewed on phones as small as 6" (~375px wide),
# so 1080-canvas text scales down ~0.35x. Keep body/content text >= 30px and labels >= 22px.

# ═══════════════ POST 1 — BLUEPRINT (Assessment centre) ═══════════════
def blueprint():
    BG="#0A2540"; CY="#4FD6E6"; INK="#EAF4FA"; MUT="#7FA8C4"
    grid=(f"position:absolute;inset:0;background-color:{BG};"
          "background-image:linear-gradient(rgba(79,214,230,.10) 1px,transparent 1px),linear-gradient(90deg,rgba(79,214,230,.10) 1px,transparent 1px),"
          "linear-gradient(rgba(79,214,230,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(79,214,230,.05) 1px,transparent 1px);"
          "background-size:216px 216px,216px 216px,36px 36px,36px 36px;")
    def marks():
        m=""
        for x,y in [(30,30),(1010,30),(30,1010),(1010,1010)]:
            m+=f"<div style='position:absolute;left:{x}px;top:{y}px;width:40px;height:40px;border:2px solid {CY};opacity:.5;'></div>"
        return m
    def block(sheet,label):
        return (f"<div style='position:absolute;right:44px;bottom:44px;width:360px;border:2px solid {CY};background:rgba(10,37,64,.85);'>"
                f"<div style='display:flex;justify-content:space-between;border-bottom:1px solid {CY}66;padding:12px 16px;'>"
                f"<img src='{WHT}' style='height:56px;'><span style=\"font-family:{MONO};color:{CY};font-size:15px;letter-spacing:1px;\">SHEET {sheet}/05</span></div>"
                f"<div style=\"font-family:{MONO};color:{INK};font-size:16px;letter-spacing:2px;padding:12px 16px;\">{label}<br><span style='color:{MUT};font-size:13px;'>ASSESSMENT CENTRE &middot; SCALE 1:1</span></div></div>")
    def mono(t,c=CY,s=19):
        return f"<div style=\"font-family:{MONO};color:{c};font-size:{s}px;letter-spacing:3px;\">{t}</div>"
    def H(t,size=76):
        return f"<div style=\"font-family:Inter;font-weight:700;font-size:{size}px;color:{INK};line-height:1.0;letter-spacing:-2px;word-break:keep-all;\">{t}</div>"
    def shell(sheet,label,body):
        return f"<div style='{grid}'></div>{marks()}<div style='position:absolute;left:64px;top:64px;right:64px;'>{body}</div>{block(sheet,label)}"
    # hook — with isometric table schematic
    iso=(f"<svg width='560' height='300' style='position:absolute;right:20px;top:540px;'>"
         f"<polygon points='180,60 470,60 540,180 110,180' fill='rgba(79,214,230,.10)' stroke='{CY}' stroke-width='2.5'/>"
         + "".join(f"<circle cx='{cx}' cy='{cy}' r='14' fill='none' stroke='%s' stroke-width='2.5'/>"%CY for cx,cy in [(210,44),(320,44),(430,44),(150,120),(500,120),(240,200),(410,200)])
         + f"<line x1='325' y1='120' x2='325' y2='250' stroke='{CY}' stroke-dasharray='5 5' stroke-width='1.5'/>"
         f"<text x='325' y='275' fill='{CY}' font-family=\"{MONO}\" font-size='16' text-anchor='middle' letter-spacing='2'>GROUP EXERCISE</text></svg>")
    dim=(f"<div style='display:flex;align-items:center;gap:10px;margin-top:34px;'>"
         f"<span style=\"font-family:{MONO};color:{CY};font-size:16px;\">&larr;</span>"
         f"<div style='flex:0 0 260px;border-top:1.5px dashed {CY};'></div>"
         f"<span style=\"font-family:{MONO};color:{MUT};font-size:15px;letter-spacing:1px;\">THE REAL CUT: 60% OF SCORE</span></div>")
    h_hook=H("The assessment<br>centre is where<br>offers are <span style='color:%s;'>won.</span>"%CY)
    body=(mono("// FIG.01 &mdash; ASSESSMENT DAY")+f"<div style='margin-top:22px;'>{h_hook}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:27px;color:{MUT};margin-top:24px;max-width:600px;line-height:1.4;\">Most candidates over-prepare the interview and wing the AC. That is backwards.</div>{dim}{iso}")
    R("d1-assessment",1,shell("01","FIG.01",body))
    # stats
    cards=""
    for n,l in [("2-3","OF ~8 FINALISTS GET AN OFFER"),("60%","IS HOW YOU WORK WITH OTHERS"),("1 DAY","OUTWEIGHS EVERY ROUND BEFORE")]:
        cards+=(f"<div style='flex:1;border:2px solid {CY}55;background:rgba(79,214,230,.05);padding:34px 26px;'>"
                f"<div style=\"font-family:Inter;font-weight:700;font-size:76px;color:{CY};letter-spacing:-3px;line-height:1;\">{n}</div>"
                f"<div style=\"font-family:{MONO};color:{INK};font-size:16px;letter-spacing:1px;margin-top:18px;line-height:1.4;\">{l}</div></div>")
    body=(mono("// FIG.02 &mdash; THE SPEC")+f"<div style='margin-top:20px;'>{H('Read the drawing<br>before the day.',60)}</div>"
          f"<div style='display:flex;gap:22px;margin-top:60px;'>{cards}</div>")
    R("d1-assessment",2,shell("02","FIG.02",body))
    # tips
    def tipslide(sheet,rev,title,pts):
        rows=""
        for p in pts:
            rows+=(f"<div style='display:flex;gap:18px;margin-bottom:22px;'><div style='flex:0 0 14px;height:14px;border:2px solid {CY};margin-top:8px;'></div>"
                   f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:29px;color:{INK};line-height:1.4;\">{p}</div></div>")
        body=(mono(f"// REV.{rev} &mdash; DETAIL")+f"<div style='margin-top:20px;'>{H(title,56)}</div>"
              f"<div style='margin-top:44px;border-left:2px dashed {CY}66;padding-left:34px;'>{rows}</div>")
        R("d1-assessment",sheet,shell(f"0{sheet}",f"REV.{rev}",body))
    tipslide(3,"A","Own the group exercise.",["Contribute early, and pull quieter people in too.","Assessors score collaboration, not domination.","Watch the clock and steer the group to a decision."])
    tipslide(4,"B","Method beats finishing.",["Prioritise out loud on the in-tray and case.","It is fine not to finish - show a clear system.","Flag assumptions instead of guessing silently."])
    # cta
    stamp=(f"<div style='position:absolute;right:70px;top:150px;transform:rotate(-14deg);border:4px solid {CY};color:{CY};padding:14px 26px;"
           f"font-family:{MONO};font-size:34px;letter-spacing:4px;font-weight:700;opacity:.85;'>CLEARED<br><span style='font-size:22px;'>FOR OFFER</span></div>")
    checks="".join(f"<div style='display:flex;gap:12px;align-items:center;margin-bottom:12px;'><span style='color:{CY};font-family:{MONO};'>[x]</span><span style=\"font-family:'DM Sans';font-weight:600;font-size:25px;color:{INK};\">{c}</span></div>" for c in ["Group: contribute + include","Case: method over finishing","A question ready for everyone","Same energy at lunch"])
    h_cta=H("Walk in ready<br>for the <span style='color:%s;'>whole day.</span>"%CY,60)
    body=(mono("// FIG.05 &mdash; SIGN-OFF")+f"<div style='margin-top:20px;'>{h_cta}</div><div style='margin-top:40px;'>{checks}</div>{stamp}"
          f"<div style=\"margin-top:34px;font-family:{MONO};color:{CY};font-size:22px;letter-spacing:2px;\">&rarr; INTERNWISE.CO.UK</div>")
    R("d1-assessment",5,shell("05","FIG.05",body))

# ═══════════════ POST 2 — EMAIL CLIENT (Follow-up) ═══════════════
def email():
    BG="#E7EDF5"; BLUE="#2F6BFF"; DEEP="#16233b"; MUT="#7C8DA6"; PANE="#ffffff"
    def app(inner, title="Mail", mark=False):
        bar=(f"<div style='height:70px;background:#F4F7FB;border-bottom:1px solid #E3E9F1;display:flex;align-items:center;padding:0 26px;gap:10px;'>"
             f"<span style='width:14px;height:14px;border-radius:50%;background:#FF5F57;'></span><span style='width:14px;height:14px;border-radius:50%;background:#FEBC2E;'></span>"
             f"<span style='width:14px;height:14px;border-radius:50%;background:#28C840;'></span>"
             f"<span style=\"margin-left:16px;font-family:'DM Sans';font-weight:600;color:{MUT};font-size:20px;\">{title}</span></div>")
        markhtml=wm(w=470,right=-30,bottom=-70,opacity=.05) if mark else ""
        return (f"<div style='position:absolute;inset:0;background:{BG};'></div>"
                f"<div style='position:absolute;left:52px;top:40px;'><img src='{WHT}' style='height:{LOGO}px;filter:brightness(0);opacity:.82;'></div>"
                f"<div style='position:absolute;left:52px;right:52px;top:172px;bottom:60px;background:{PANE};border-radius:26px;overflow:hidden;box-shadow:0 30px 60px rgba(30,50,90,.18);'>{bar}<div style='padding:36px 40px;'>{inner}</div>{markhtml}</div>")
    def avatar(t,c=BLUE):
        return f"<div style='flex:0 0 56px;height:56px;border-radius:50%;background:{c};color:#fff;display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;'>{t}</div>"
    def ticks():
        return f"<svg width='34' height='18'><path d='M2 9 l5 5 l9-11 M14 9 l5 5 l9-11' stroke='{BLUE}' stroke-width='2.5' fill='none' stroke-linecap='round'/></svg>"
    # hook — compose window
    badge=(f"<div style='position:absolute;right:80px;top:150px;transform:rotate(6deg);background:{BLUE};color:#fff;padding:16px 24px;border-radius:16px;"
           f"font-family:Inter;font-weight:700;font-size:24px;box-shadow:0 14px 30px rgba(47,107,255,.4);'>Only 4% send this</div>")
    compose=(f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:22px;color:{DEEP};border-bottom:1px solid #EEF2F8;padding-bottom:16px;\">New message</div>"
             f"<div style=\"font-family:'DM Sans';font-size:22px;color:{MUT};padding:16px 0;border-bottom:1px solid #EEF2F8;\">To: <span style='color:{DEEP};'>Hiring Manager</span></div>"
             f"<div style=\"font-family:'DM Sans';font-size:22px;color:{MUT};padding:16px 0;border-bottom:1px solid #EEF2F8;\">Subject: <span style='color:{DEEP};font-weight:600;'>Following up on the Marketing Intern role</span></div>"
             f"<div style=\"font-family:Inter;font-weight:700;font-size:52px;color:{DEEP};line-height:1.05;letter-spacing:-1.5px;margin:30px 0;\">Only <span style='color:{BLUE};'>4%</span> of applicants send a follow-up.<span style='border-left:3px solid {BLUE};margin-left:6px;'>&nbsp;</span></div>"
             f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:31px;color:{MUT};line-height:1.4;\">The ones who do stand out instantly. Swipe for the message that gets a reply.</div>"
             f"<div style='margin-top:40px;display:flex;align-items:center;gap:16px;'><div style='background:{BLUE};color:#fff;padding:14px 40px;border-radius:40px;font-family:Inter;font-weight:700;font-size:23px;'>Send</div>"
             f"<span style=\"font-family:'DM Sans';color:{MUT};font-size:20px;\">Swipe &rarr;</span></div>")
    R("d2-followup",1,app(compose,"New Message")+badge)
    # stats — three notification rows
    rows=""
    for n,l in [("4%","of applicants ever follow up. Be one of them."),("27%","reply rate on a short, researched note."),("48h","the window while you are still fresh.")]:
        rows+=(f"<div style='display:flex;align-items:center;gap:22px;padding:26px 0;border-bottom:1px solid #EEF2F8;'>{avatar(n[:2],BLUE)}"
               f"<div><div style=\"font-family:Inter;font-weight:700;font-size:40px;color:{DEEP};letter-spacing:-1px;\">{n}</div>"
               f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:29px;color:{MUT};\">{l}</div></div></div>")
    inner=f"<div style=\"font-family:Inter;font-weight:700;font-size:44px;color:{DEEP};letter-spacing:-1px;margin-bottom:10px;\">A tiny effort, a big edge.</div>{rows}<div style=\"font-family:'DM Sans';color:{MUT};font-size:22px;text-align:right;margin-top:14px;\">Sources: LinkedIn, Jobvite 2026</div>"
    R("d2-followup",2,app(inner,"Inbox"))
    # tips — email cards
    def tipmail(sheet,name,init,subj,pts):
        body="".join(f"<div style='display:flex;gap:14px;margin-bottom:18px;'><span style='color:{BLUE};font-size:28px;'>&bull;</span><span style=\"font-family:'DM Sans';font-weight:500;font-size:31px;color:{DEEP};line-height:1.4;\">{p}</span></div>" for p in pts)
        inner=(f"<div style='display:flex;align-items:center;gap:18px;border-bottom:1px solid #EEF2F8;padding-bottom:22px;'>{avatar(init)}"
               f"<div style='flex:1;'><div style=\"font-family:'DM Sans';font-weight:700;font-size:24px;color:{DEEP};\">{name}</div>"
               f"<div style=\"font-family:'DM Sans';color:{MUT};font-size:20px;\">to you {ticks()}</div></div>"
               f"<span style=\"font-family:'DM Sans';color:{MUT};font-size:19px;\">now</span></div>"
               f"<div style=\"font-family:Inter;font-weight:700;font-size:36px;color:{DEEP};margin:26px 0 30px;letter-spacing:-.5px;\">{subj}</div>{body}")
        R("d2-followup",sheet,app(inner,"Inbox",mark=True))
    tipmail(3,"Rule 1 — Timing","T1","Send 24 to 48h after.",["Reply in the same thread if there is one.","One follow-up is plenty - do not chase weekly.","Fresh in their mind beats forgotten."])
    tipmail(4,"Rule 2 — The message","M2","Keep it three sentences.",["Thank them and name one thing you discussed.","Restate the single reason you are a strong fit.","Ask about next steps and the timeline."])
    # cta — sent screen
    checks="".join(f"<div style='display:flex;gap:14px;align-items:center;margin-bottom:16px;'>{ticks()}<span style=\"font-family:'DM Sans';font-weight:600;font-size:30px;color:{DEEP};\">{c}</span></div>" for c in ["24 to 48 hours after","Three sentences","One specific detail","Ask about next steps"])
    inner=(f"<div style='display:flex;flex-direction:column;align-items:center;text-align:center;margin-top:6px;'>"
           f"<div style='width:104px;height:104px;border-radius:50%;background:{BLUE};display:flex;align-items:center;justify-content:center;'><svg width='58' height='38'><path d='M6 20 l14 14 l34-30' stroke='#fff' stroke-width='6' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg></div>"
           f"<div style=\"font-family:Inter;font-weight:700;font-size:46px;color:{DEEP};margin-top:20px;letter-spacing:-1px;\">Send the email the<br>other <span style='color:{BLUE};'>96%</span> won't.</div></div>"
           f"<div style='margin-top:26px;'>{checks}</div>"
           f"<div style='margin-top:22px;display:flex;flex-direction:column;align-items:center;gap:12px;'>"
           f"<div style='background:{BLUE};color:#fff;padding:17px 44px;border-radius:44px;font-family:Inter;font-weight:700;font-size:28px;'>Find your internship &rarr;</div>"
           f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:25px;color:{DEEP};\">internwise.co.uk</div></div>")
    R("d2-followup",5,app(inner,"Sent"))

# ═══════════════ POST 3 — NEWSPAPER (2026 market) ═══════════════
def newspaper():
    PAP="#F1E9D6"; INK="#171512"; RED="#D8382B"; MUT="#5c554a"
    def paper(inner):
        return (f"<div style='position:absolute;inset:0;background:{PAP};'></div>"
                "<div style='position:absolute;inset:0;background-image:radial-gradient(rgba(0,0,0,.03) 1px,transparent 1px);background-size:4px 4px;'></div>"
                f"<div style='position:absolute;left:60px;right:60px;top:56px;bottom:56px;'>{inner}</div>")
    def masthead():
        folio=(f"<div style='display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid {INK}66;padding-bottom:12px;margin-bottom:12px;'>"
               f"<img src='{WHT}' style='height:{LOGO}px;filter:brightness(0);'>"
               f"<span style=\"font-family:{SERIF};font-size:22px;color:{MUT};letter-spacing:2px;\">internwise.co.uk</span></div>")
        return (folio+f"<div style='text-align:center;border-bottom:4px double {INK};padding-bottom:12px;'>"
                f"<div style=\"font-family:{SERIF};font-weight:700;font-size:62px;color:{INK};letter-spacing:-1px;\">The Graduate Times</div>"
                f"<div style=\"font-family:{SERIF};font-size:20px;color:{MUT};letter-spacing:3px;margin-top:4px;\">LONDON &middot; AUGUST 2026 &middot; CAREERS EDITION</div></div>")
    def chart():
        bars=[('J',150),('F',135),('M',120),('A',96),('M',78),('J',54)]
        svg=f"<svg width='460' height='240'>"
        for i,(m,h) in enumerate(bars):
            x=20+i*72; y=200-h
            svg+=f"<rect x='{x}' y='{y}' width='50' height='{h}' fill='{RED if i>=4 else INK}'/><text x='{x+25}' y='224' fill='{MUT}' font-family=\"{SERIF}\" font-size='16' text-anchor='middle'>{m}</text>"
        svg+=f"<polyline points='45,50 117,65 189,80 261,104 333,122 405,146' fill='none' stroke='{RED}' stroke-width='3' stroke-dasharray='6 4'/></svg>"
        return svg
    def stamp(txt="BRUTAL"):
        return (f"<div style='position:absolute;right:74px;top:250px;transform:rotate(-11deg);border:5px solid {RED};color:{RED};padding:8px 22px;"
                f"font-family:Inter;font-weight:700;font-size:56px;letter-spacing:2px;opacity:.9;'>{txt}</div>")
    # hook
    lede=(f"<p style=\"font-family:{SERIF};font-size:30px;color:{INK};line-height:1.55;\">"
          f"<span style='float:left;font-family:{SERIF};font-weight:700;font-size:92px;line-height:.72;padding:6px 14px 0 0;color:{RED};'>R</span>"
          "ecord applicants. Fewer openings. Inboxes that never reply. The class of 2026 is facing the toughest graduate market in a decade - and most people are playing it wrong. Inside: how to beat the odds anyway.</p>")
    inner=(masthead()+f"<div style='border-bottom:1px solid {INK};padding:10px 0;font-family:{SERIF};font-size:21px;color:{MUT};letter-spacing:2px;'>FRONT PAGE &middot; THE JOBS CRISIS</div>"
           f"<div style=\"font-family:Inter;font-weight:700;font-size:80px;color:{INK};line-height:.94;letter-spacing:-3px;margin:18px 0 18px;\">Grad market<br>in freefall.</div>"
           f"<div style='display:flex;gap:46px;align-items:flex-start;'><div style='flex:1;'>{lede}</div><div style='flex:0 0 440px;'>{chart()}<div style=\"font-family:{SERIF};font-size:20px;color:{MUT};text-align:center;margin-top:6px;\">Openings index, Jan&ndash;Jun 2026</div></div></div>{stamp()}"
           f"<div style=\"position:absolute;bottom:0;font-family:{SERIF};font-size:19px;color:{MUT};letter-spacing:2px;\">TURN THE PAGE &rarr;</div>")
    R("d3-market",1,paper(inner))
    # stats — three columns
    cols=""
    for n,l in [("140+","applications per graduate role, on average."),("1 in 3","employers cut graduate intake this year."),("70%","of schemes close before Christmas.")]:
        cols+=(f"<div style='flex:1;padding:0 26px;border-right:1px solid {INK}44;'>"
               f"<div style=\"font-family:Inter;font-weight:700;font-size:92px;color:{RED};letter-spacing:-3px;line-height:1;\">{n}</div>"
               f"<div style=\"font-family:{SERIF};font-size:30px;color:{INK};margin-top:16px;line-height:1.4;\">{l}</div></div>")
    inner=(masthead()+f"<div style=\"font-family:Inter;font-weight:700;font-size:60px;color:{INK};margin:30px 0;letter-spacing:-2px;\">By the numbers.</div>"
           f"<div style='display:flex;margin-top:30px;'>{cols}</div>"
           f"<div style=\"position:absolute;bottom:0;font-family:{SERIF};font-size:20px;color:{MUT};\">Source: ISE Student Recruitment Survey 2026</div>"
           +wm(w=560,right=-80,bottom=-110,opacity=.05))
    R("d3-market",2,paper(inner))
    # tips — survival guide
    def tipcol(sheet,no,title,pts):
        body="".join(f"<p style=\"font-family:{SERIF};font-size:31px;color:{INK};line-height:1.5;margin-bottom:18px;\"><span style='color:{RED};font-weight:700;'>-</span> {p}</p>" for p in pts)
        inner=(masthead()+f"<div style=\"font-family:{SERIF};font-size:20px;color:{RED};letter-spacing:3px;margin-top:22px;\">SURVIVAL GUIDE &middot; NO.{no}</div>"
               f"<div style=\"font-family:Inter;font-weight:700;font-size:64px;color:{INK};letter-spacing:-2px;margin:6px 0 34px;\">{title}</div>{body}"
               +wm(w=560,right=-80,bottom=-110,opacity=.05))
        R("d3-market",sheet,paper(inner))
    tipcol(3,"I","Play it smarter.",["Fewer, tailored applications beat 100 copy-pastes.","Apply the week a scheme opens - slots fill fast.","Track everything in one sheet so nothing slips."])
    tipcol(4,"II","Skip the queue.",["SMEs and startups hire year-round, less competition.","Referrals and speculative routes bypass the portal.","A warm intro beats a cold application every time."])
    # cta — classified
    ad=(f"<div style='border:3px solid {INK};padding:44px;text-align:center;'>"
        f"<div style=\"font-family:{SERIF};font-size:22px;color:{RED};letter-spacing:4px;\">SITUATIONS VACANT</div>"
        f"<div style=\"font-family:Inter;font-weight:700;font-size:60px;color:{INK};margin:18px 0;letter-spacing:-2px;\">The market is hard.<br>You can still win.</div>"
        f"<div style=\"font-family:{SERIF};font-size:30px;color:{INK};line-height:1.5;\">Tailor, don't spray &middot; Apply early<br>Chase the hidden market &middot; Follow up &amp; improve</div>"
        f"<div style='margin-top:28px;'>"
        f"<div style=\"font-family:{SERIF};font-size:23px;color:{MUT};letter-spacing:1px;margin-bottom:12px;\">Browse live UK internships today</div>"
        f"<div style='display:inline-block;background:{INK};color:{PAP};padding:16px 40px;font-family:Inter;font-weight:700;font-size:28px;'>internwise.co.uk</div></div></div>")
    inner=masthead()+f"<div style=\"font-family:{SERIF};font-size:20px;color:{MUT};letter-spacing:3px;margin:22px 0;\">BACK PAGE &middot; CLASSIFIEDS</div>{ad}"
    R("d3-market",5,paper(inner))

# ═══════════════ POST 4 — REDACTED DOC (Decode) SINGLE ═══════════════
def redacted():
    PAP="#E9DFC6"; INK="#20201c"; HI="#FCE96A"; RED="#C0392B"; MUT="#6a6353"
    def hl(t): return f"<span style='background:{HI};padding:2px 6px;box-decoration-break:clone;'>{t}</span>"
    def bar(w): return f"<span style='display:inline-block;width:{w}px;height:24px;background:{INK};vertical-align:middle;border-radius:2px;'></span>"
    ad=(f"<div style=\"font-family:{MONO};font-size:27px;color:{INK};line-height:1.9;\">"
        f"We are seeking a candidate with {hl('2+ years experience')} to thrive in our {hl('fast-paced environment')}. "
        f"You will {hl('wear many hats')} and receive a {hl('competitive salary')} plus {bar(150)} and {bar(90)}.</div>")
    rows=[("'2+ years experience'","We'd like it, not need it. Apply anyway."),
          ("'Fast-paced environment'","Be ready to juggle and self-manage."),
          ("'Wear many hats'","Small team - you will learn a lot, fast."),
          ("'Competitive salary'","Ask the number. They expect you to.")]
    dec=""
    for a,m in rows:
        dec+=(f"<div style='display:flex;align-items:center;gap:18px;margin-bottom:16px;'>"
              f"<span style='background:{HI};color:{INK};font-family:{MONO};font-weight:700;font-size:20px;padding:4px 10px;flex:0 0 330px;'>{a}</span>"
              f"<span style='color:{RED};font-size:24px;'>&rarr;</span>"
              f"<span style=\"font-family:'DM Sans';font-weight:600;font-size:24px;color:{INK};\">{m}</span></div>")
    stamp=(f"<div style='position:absolute;right:80px;top:250px;transform:rotate(9deg);border:5px solid {RED};color:{RED};padding:10px 22px;"
           f"font-family:{MONO};font-weight:700;font-size:38px;letter-spacing:4px;opacity:.85;'>DECODED</div>")
    inner=(f"<div style='position:absolute;inset:0;background:{PAP};'></div>"
           "<div style='position:absolute;inset:0;background-image:radial-gradient(rgba(0,0,0,.035) 1px,transparent 1px);background-size:5px 5px;'></div>"
           f"<div style='position:absolute;left:64px;right:64px;top:60px;'>"
           f"<div style='display:flex;justify-content:space-between;align-items:center;'><img src='{WHT}' style='height:84px;filter:brightness(0);opacity:.82;'>"
           f"<span style=\"font-family:{MONO};color:{MUT};letter-spacing:3px;font-size:17px;\">FILE: JOB-AD.TXT</span></div>"
           f"<div style=\"font-family:Inter;font-weight:700;font-size:58px;color:{INK};letter-spacing:-2px;margin:30px 0 14px;\">What the ad says<br>vs what it <span style='color:{RED};'>means.</span></div>"
           f"<div style='border-left:4px solid {INK}44;padding-left:24px;margin:24px 0 34px;'>{ad}</div>"
           f"<div style=\"font-family:{MONO};color:{MUT};letter-spacing:3px;font-size:18px;margin-bottom:18px;\">// DECODED &mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;</div>{dec}"
           f"<div style=\"margin-top:24px;font-family:'DM Sans';font-weight:700;font-size:24px;color:{RED};\">Recruiters write a wishlist. You still apply. &nbsp;internwise.co.uk</div></div>{stamp}")
    R("d4-decode",1,inner)

# ═══════════════ POST 5 — RECEIPT (Negotiate) SINGLE ═══════════════
def receipt():
    GRN="#0E6B4F"; PAP="#FBFAF6"; INK="#1c1c1a"; RED="#D8382B"; MUT="#6a6a64"
    zig="polygon(0 0,3% 100%,6% 0,9% 100%,12% 0,15% 100%,18% 0,21% 100%,24% 0,27% 100%,30% 0,33% 100%,36% 0,39% 100%,42% 0,45% 100%,48% 0,51% 100%,54% 0,57% 100%,60% 0,63% 100%,66% 0,69% 100%,72% 0,75% 100%,78% 0,81% 100%,84% 0,87% 100%,90% 0,93% 100%,96% 0,99% 100%,100% 0)"
    items=[("Say thank you, then ask","+ credibility"),("Name a researched number","+ leverage"),("Then stop talking","+ the offer")]
    li=""
    for a,m in items:
        li+=(f"<div style='display:flex;justify-content:space-between;font-family:{MONO};font-size:26px;color:{INK};padding:11px 0;border-bottom:1px dashed #d8d5cc;'>"
             f"<span>{a}</span><span style='color:{GRN};font-weight:700;'>{m}</span></div>")
    barcode="".join(f"<div style='width:{w}px;height:52px;background:{INK};'></div>" for w in [3,1,4,2,1,5,2,3,1,2,4,1,3,2,5,1,2,3,1,4,2,1,3,2,4,1,2,5,1,3])
    stamp=(f"<div style='position:absolute;right:118px;top:140px;transform:rotate(12deg);border:5px solid {RED};color:{RED};padding:10px 20px;"
           f"font-family:{MONO};font-weight:700;font-size:30px;letter-spacing:3px;opacity:.9;'>NEVER<br>ASKED</div>")
    inner=(f"<div style='position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,#12805e,#0a4f3a);'></div>"
           f"<div style='position:absolute;left:52px;top:44px;'><img src='{WHT}' style='height:{LOGO}px;'></div>"
           f"<div style='position:absolute;left:170px;right:170px;top:184px;background:{PAP};padding:34px 44px 38px;border-radius:6px;box-shadow:0 24px 50px rgba(0,0,0,.3);'>"
           "<div style='position:absolute;left:0;right:0;top:-11px;height:22px;background:repeating-linear-gradient(90deg,#0a4f3a 0 2px,transparent 2px 20px);'></div>"
           f"<div style='text-align:center;border-bottom:2px solid {INK};padding-bottom:14px;margin-bottom:6px;'>"
           f"<div style=\"font-family:{MONO};font-weight:700;font-size:28px;color:{INK};letter-spacing:3px;\">SALARY RECEIPT</div>"
           f"<div style=\"font-family:{MONO};font-size:20px;color:{MUT};letter-spacing:1px;\">THE COST OF NOT ASKING</div></div>"
           f"<div style='text-align:center;margin:18px 0;'><div style=\"font-family:Inter;font-weight:700;font-size:124px;color:{GRN};letter-spacing:-6px;line-height:.9;\">58%</div>"
           f"<div style=\"font-family:Inter;font-weight:700;font-size:31px;color:{INK};letter-spacing:-.5px;max-width:540px;margin:10px auto 0;line-height:1.14;\">of grads accept the first offer without asking for more.</div></div>"
           f"<div style=\"font-family:{MONO};font-size:20px;color:{MUT};letter-spacing:2px;margin-bottom:6px;\">HOW TO ASK ------------------------</div>{li}"
           f"<div style='display:flex;justify-content:space-between;font-family:{MONO};font-weight:700;font-size:28px;color:{INK};padding:14px 0;border-top:2px solid {INK};margin-top:8px;'>"
           f"<span>TOTAL</span><span style='color:{RED};'>ASK FOR MORE</span></div>"
           f"<div style='display:flex;justify-content:center;gap:2px;align-items:flex-end;margin-top:18px;'>{barcode}</div>"
           f"<div style=\"text-align:center;font-family:{MONO};font-size:19px;color:{MUT};margin-top:10px;letter-spacing:2px;\">NO. 0058 &middot; KEEP THIS RECEIPT</div></div>"
           f"<div style='position:absolute;left:0;right:0;bottom:40px;text-align:center;'>"
           f"<span style='display:inline-block;background:{PAP};color:#0a4f3a;font-family:Inter;font-weight:700;font-size:28px;padding:16px 44px;border-radius:44px;box-shadow:0 12px 26px rgba(0,0,0,.25);'>Find your internship &rarr;</span>"
           f"<div style=\"font-family:Inter;font-weight:700;font-size:24px;color:#CDEBD9;margin-top:14px;\">internwise.co.uk</div></div>{stamp}")
    R("d5-negotiate",1,inner)

blueprint(); email(); newspaper(); redacted(); receipt()
print("DONE v2")
