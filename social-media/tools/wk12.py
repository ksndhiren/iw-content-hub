"""Week 12 (w/c 17 Aug) - Nuno-integrated designs. D1 CV Clinic.
Design language upgraded with lessons from the gpt-image-2 test: amber arc behind
subject, icon-badge lists, eyebrow underline, progress indicator, brand footer,
callout box, halftone dot accents - all in our exact brand (real logo/copy/colours)."""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wk11_base as b
from playwright.sync_api import sync_playwright
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(BASE,"campaigns","outputs","week12")
F=b.fonts()
WHT="data:image/png;base64,"+b.LOGO_W
def _img(p): return "data:image/png;base64,"+base64.b64encode(open(p,"rb").read()).decode()
def _nuno(name): return _img(os.path.join(BASE,"assets","nuno",name+".png"))
NUNO_CV=_nuno("nuno_cv"); NUNO_THUMB=_nuno("nuno_thumbsup")
NUNO_HOWTO=_nuno("nuno_howto_1"); NUNO_AUTHORITY=_nuno("nuno_authority_1")
NUNO_WELCOMING=_nuno("nuno_welcoming_1"); NUNO_UTILITY=_nuno("nuno_utility_1")
NUNO_DOTHIS2=_nuno("nuno_dothis_2")
ICONMARK="data:image/svg+xml;base64,"+base64.b64encode(open(os.path.join(BASE,"assets","iw_icon_mark.svg"),"rb").read()).decode()
MONO="'Courier New',monospace"; LOGO=100
RIM="drop-shadow(0 14px 30px rgba(0,0,0,.42))"
NAVY="#0E2141"; DEEP="#0A1830"; INK="#EAF2FB"; MUT="#93AAC9"; AMBER="#FFB120"; CORAL="#FF6B6B"; GREEN="#41D98A"

def R(post,i,inner):
    d=os.path.join(OUT,post); os.makedirs(d,exist_ok=True); path=os.path.join(d,f"slide_{i}.png")
    html=(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{F}*{{margin:0;padding:0;box-sizing:border-box;}}"
          f"body{{width:1080px;height:1080px;overflow:hidden;}}.r{{width:1080px;height:1080px;position:relative;overflow:hidden;}}"
          f"</style></head><body><div class='r'>{inner}</div></body></html>")
    with sync_playwright() as p:
        br=p.chromium.launch(); pg=br.new_page(viewport={"width":1080,"height":1080},device_scale_factor=2)
        pg.set_content(html,wait_until="networkidle"); pg.screenshot(path=path,type="png"); br.close()
    print("  ok",post,i)

def ic(n):
    return {
     "user":"<circle cx='12' cy='8' r='4'/><path d='M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7'/>",
     "target":"<circle cx='12' cy='12' r='9'/><circle cx='12' cy='12' r='4.5'/><circle cx='12' cy='12' r='1.2' fill='currentColor' stroke='none'/>",
     "star":"<path d='M12 3.5l2.6 5.7 6.2.6-4.7 4.1 1.4 6.1L12 16.9 6.5 20.1l1.4-6.1L3.2 9.8l6.2-.6z'/>",
     "search":"<circle cx='11' cy='11' r='7'/><path d='M20 20l-4.5-4.5'/>",
     "doc":"<rect x='5' y='3' width='14' height='18' rx='2'/><path d='M8.5 8h7M8.5 12h7M8.5 16h4'/>",
     "rocket":"<path d='M12 3c3.4 2 5.4 5.4 5.4 9.4L12 16l-5.4-3.6C6.6 8.4 8.6 5 12 3z'/><circle cx='12' cy='10' r='1.7'/><path d='M9 16c-1.6 1-2.2 3-2.2 5 2 0 4-.6 5-2.2'/>",
     "check":"<path d='M4 12.5l5 5 11-11'/>",
     "x":"<path d='M6 6l12 12M18 6L6 18'/>",
     "clock":"<circle cx='12' cy='12' r='9'/><path d='M12 7.5v5l3.5 2.5'/>",
     "eye":"<path d='M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z'/><circle cx='12' cy='12' r='3'/>",
     "chat":"<path d='M4 5h16v10H10l-4 4v-4H4z'/>",
     "calendar":"<rect x='4' y='5' width='16' height='16' rx='2'/><path d='M4 10h16M8 3v4M16 3v4'/>",
     "arrowup":"<path d='M12 19V6M6 12l6-6 6 6'/>",
     "refresh":"<path d='M20 11a8 8 0 1 0-.6 4'/><path d='M20 5v6h-6'/>",
     "bulb":"<path d='M9 18h6M10 21h4'/><path d='M8.5 14A5 5 0 1 1 15.5 14c-.6.6-1 1.3-1 2h-5c0-.7-.4-1.4-1-2z'/>",
     "heart":"<path d='M12 20s-6.6-4.3-8.6-8C1.8 8.4 4 5.4 7 6c2 .4 3.2 2 5 3.6C13.8 8 15 6.4 17 6c3-.6 5.2 2.4 3.6 6-2 3.7-8.6 8-8.6 8z'/>",
     "flag":"<path d='M6 21V4M6 4h11l-2 3.5L17 11H6'/>",
     "briefcase":"<rect x='3' y='8' width='18' height='12' rx='2'/><path d='M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2'/>",
     "handshake":"<path d='M8 13l2.5 2.5 2-2 2.5 2.5M4 9l4-3 4 2.5 4-2.5 4 3v5l-3 3'/>",
    }.get(n,"")
def svg(name,color,sz=30):
    return f"<svg width='{sz}' height='{sz}' viewBox='0 0 24 24' fill='none' stroke='{color}' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>{ic(name)}</svg>"

def bg():
    return ("<div style='position:absolute;inset:0;background-color:"+NAVY+";"
            "background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);"
            "background-size:56px 56px;'></div>")
def dots(css,color="rgba(255,177,32,.45)",w=176,h=120):
    return f"<div style='position:absolute;{css}width:{w}px;height:{h}px;background-image:radial-gradient({color} 3px,transparent 3px);background-size:24px 24px;'></div>"
def arc(cx,cy,r,color=AMBER,op=1.0):
    return f"<div style='position:absolute;left:{cx-r}px;top:{cy-r}px;width:{r*2}px;height:{r*2}px;border-radius:50%;background:{color};opacity:{op};'></div>"
def head(n,total=5):
    return (f"<div style='position:absolute;left:56px;top:44px;'><img src='{WHT}' style='height:{LOGO}px;'></div>"
            f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;color:{MUT};letter-spacing:2px;\"><span style='color:{AMBER};'>0{n}</span> / 0{total}</div>")
def eyebrow(tag,top):
    return (f"<div style=\"position:absolute;left:58px;top:{top}px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{AMBER};letter-spacing:4px;\">{tag}</div>"
            f"<div style='position:absolute;left:58px;top:{top+34}px;width:64px;height:4px;background:{AMBER};border-radius:2px;'></div>")
def footer(swipe=True):
    f=(f"<div style='position:absolute;left:56px;bottom:44px;display:flex;align-items:center;gap:13px;'>"
       f"<div style='width:34px;height:34px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;'>"
       f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{DEEP}' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
       f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:{MUT};letter-spacing:1px;\">internwise.co.uk</span></div>")
    if swipe:
        f+=f"<div style=\"position:absolute;right:58px;bottom:44px;font-family:'DM Sans';font-weight:600;font-size:23px;color:{AMBER};\">Swipe &rarr;</div>"
    return f
def wm(w=540,right=-90,bottom=-120,op=.05):
    return f"<img src='{ICONMARK}' style='position:absolute;right:{right}px;bottom:{bottom}px;width:{w}px;filter:brightness(0) invert(1);opacity:{op};pointer-events:none;'>"
def badgelist(rows,color=AMBER):
    out=""
    for icon,label,desc in rows:
        out+=(f"<div style='display:flex;gap:20px;align-items:center;margin-bottom:26px;'>"
              f"<div style='flex:0 0 64px;width:64px;height:64px;border-radius:50%;border:2px solid {color}88;background:{color}14;display:flex;align-items:center;justify-content:center;'>{svg(icon,color,30)}</div>"
              f"<div><div style=\"font-family:Inter;font-weight:700;font-size:30px;color:{INK};letter-spacing:-.5px;\">{label}</div>"
              f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:25px;color:{MUT};line-height:1.28;margin-top:1px;\">{desc}</div></div></div>")
    return out
def callout(icon,html,color=AMBER,w=560):
    return (f"<div style='display:inline-flex;align-items:center;gap:16px;max-width:{w}px;border:1.5px solid {color}80;border-radius:16px;padding:18px 24px;background:{DEEP};'>"
            f"{svg(icon,color,30)}<div style=\"font-family:'DM Sans';font-weight:500;font-size:26px;color:{INK};line-height:1.3;\">{html}</div></div>")
def nuno(src,h,right,bottom):
    return f"<img src='{src}' style='position:absolute;right:{right}px;bottom:{bottom}px;height:{h}px;filter:{RIM};'>"

def cv_card(w=372, mode="plain"):
    def bar(width,h=13,c="#cdd6e3",mt=0): return f"<div style='width:{width};height:{h}px;border-radius:4px;background:{c};margin-top:{mt}px;'></div>"
    d3="".join("<div style='width:32px;height:8px;border-radius:4px;background:#d7deea;'></div>" for _ in range(3))
    top=(f"<div style='padding:24px 24px 0;'>{bar('62%',22,'#25324e')}<div style='height:9px;'></div>{bar('42%',14,'#E8A21C')}"
         f"<div style='display:flex;gap:8px;margin-top:13px;'>{d3}</div></div>")
    def sec(t):
        body="".join(bar('93%' if i<2 else '68%',11,'#d3dbe6',12) for i in range(3))
        return f"<div style='padding:0 24px;margin-top:18px;'><div style=\"font-family:'DM Sans';font-weight:700;font-size:13px;letter-spacing:2px;color:#94a0b2;\">{t}</div>{body}</div>"
    skills="".join(f"<div style='height:24px;width:{sw}px;background:#eef2f8;border-radius:20px;'></div>" for sw in [72,52,86,60])
    body=(f"{top}{sec('EXPERIENCE')}{sec('EDUCATION')}<div style='padding:0 24px;margin-top:18px;'>"
          f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:13px;letter-spacing:2px;color:#94a0b2;\">SKILLS</div>"
          f"<div style='display:flex;gap:8px;flex-wrap:wrap;margin-top:11px;'>{skills}</div></div>")
    over=""
    if mode=="heat":
        over=(f"<div style='position:absolute;left:0;right:0;top:0;height:37%;background:linear-gradient(180deg,rgba(255,177,32,.34),rgba(255,177,32,.04));'></div>"
              f"<div style='position:absolute;left:0;right:0;top:37%;height:2px;background:rgba(255,177,32,.7);box-shadow:0 0 14px {AMBER};'></div>")
    elif mode=="focus":
        over=(f"<div style='position:absolute;left:8px;right:8px;top:8px;height:34%;border:2.5px solid {AMBER};border-radius:12px;box-shadow:0 0 22px rgba(255,177,32,.4);'></div>"
              f"<div style='position:absolute;left:0;right:0;top:calc(34% + 8px);bottom:0;background:rgba(14,33,65,.55);'></div>")
    return f"<div style='position:relative;width:{w}px;background:#FBFCFE;border-radius:16px;box-shadow:0 30px 60px rgba(0,0,0,.45);padding-bottom:24px;overflow:hidden;'>{body}{over}</div>"

def flashcard(q,hint,w=440,rot=0,tag="Q",accent=AMBER):
    return (f"<div style='position:relative;width:{w}px;background:#FBFCFE;border-radius:18px;box-shadow:0 26px 55px rgba(0,0,0,.42);padding:24px 26px;transform:rotate({rot}deg);'>"
            f"<div style='display:inline-flex;align-items:center;height:38px;padding:0 14px;border-radius:10px;background:{accent};font-family:Inter;font-weight:700;font-size:18px;color:{DEEP};letter-spacing:1px;'>{tag}</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:30px;color:#1c2740;letter-spacing:-.5px;margin-top:16px;line-height:1.12;\">{q}</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:23px;color:#5b6b82;margin-top:9px;line-height:1.3;\">{hint}</div></div>")
def qrow(tag,q,hint,w=900):
    return (f"<div style='display:flex;gap:20px;align-items:center;background:#FBFCFE;border-radius:16px;box-shadow:0 16px 38px rgba(0,0,0,.32);padding:20px 24px;margin-bottom:18px;width:{w}px;'>"
            f"<div style='flex:0 0 auto;display:flex;align-items:center;justify-content:center;height:52px;padding:0 16px;border-radius:12px;background:{AMBER};font-family:Inter;font-weight:700;font-size:20px;color:{DEEP};'>{tag}</div>"
            f"<div><div style=\"font-family:Inter;font-weight:700;font-size:28px;color:#1c2740;letter-spacing:-.5px;\">{q}</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:22px;color:#5b6b82;margin-top:2px;\">{hint}</div></div></div>")
def chips(items,color=AMBER,txt=INK):
    return "".join(f"<span style='display:inline-block;margin:0 10px 12px 0;padding:9px 18px;border-radius:30px;border:1.5px solid {color}88;background:{color}1f;font-family:Inter;font-weight:700;font-size:22px;color:{txt};'>{t}</span>" for t in items)
def proofcard(title,parts,w=470):
    ch=chips(parts,color="#C98A12",txt="#26324a")
    return (f"<div style='width:{w}px;background:#FBFCFE;border-radius:18px;box-shadow:0 22px 50px rgba(0,0,0,.4);padding:24px 26px;'>"
            f"<div style='display:inline-flex;align-items:center;height:34px;padding:0 13px;border-radius:9px;background:{DEEP};font-family:Inter;font-weight:700;font-size:16px;color:{AMBER};letter-spacing:1px;'>PROOF CARD</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:28px;color:#1c2740;letter-spacing:-.5px;margin:14px 0 16px;\">{title}</div>"
            f"<div style='display:flex;flex-wrap:wrap;'>{ch}</div></div>")
def idbadge(w=360,week=1):
    def bar(width,h=12,c="#cdd6e3",mt=0): return f"<div style='width:{width};height:{h}px;border-radius:3px;background:{c};margin-top:{mt}px;'></div>"
    off="#dfe4ec"
    seg="".join(f"<div style='flex:1;height:9px;border-radius:4px;background:{AMBER if i<week else off};'></div>" for i in range(12))
    return (f"<div style='position:relative;width:{w}px;background:#FBFCFE;border-radius:18px;box-shadow:0 30px 60px rgba(0,0,0,.45);padding:30px 28px 26px;'>"
            f"<div style='position:absolute;left:50%;top:-13px;transform:translateX(-50%);width:74px;height:13px;background:{DEEP};border-radius:7px;'></div>"
            f"<div style='display:flex;gap:18px;align-items:center;'>"
            f"<div style='flex:0 0 84px;width:84px;height:84px;border-radius:14px;background:{AMBER}22;border:2px solid {AMBER};display:flex;align-items:center;justify-content:center;'>{svg('user',AMBER,40)}</div>"
            f"<div style='flex:1;'>{bar('82%',18,'#25324e')}<div style='height:9px;'></div>{bar('55%',13,'#E8A21C')}</div></div>"
            f"<div style='margin-top:20px;padding-top:16px;border-top:1px solid #e5e9f0;'>"
            f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:13px;letter-spacing:3px;color:#94a0b2;\">INTERN PASS &middot; WEEK {week} OF 12</div>"
            f"<div style='display:flex;gap:6px;margin-top:12px;'>{seg}</div></div></div>")

# ---- Slide 1: hook ----
def d1_hook():
    hl="<span style='color:"+AMBER+";'>7 seconds.</span>"
    timer=(f"<div style='display:inline-flex;align-items:center;gap:12px;background:{DEEP};border:1px solid rgba(255,177,32,.5);border-radius:14px;padding:12px 20px;'>"
           f"<span style='width:14px;height:14px;border-radius:50%;background:{CORAL};box-shadow:0 0 0 4px rgba(255,107,107,.25);'></span>"
           f"<span style=\"font-family:{MONO};font-weight:700;font-size:30px;color:{INK};letter-spacing:2px;\">00:07</span>"
           f"<span style=\"font-family:'DM Sans';font-weight:600;font-size:20px;color:{MUT};letter-spacing:2px;\">SCANNING CV</span></div>")
    inner=(bg()+arc(1010,470,360)+dots("left:58px;bottom:150px;")
           +nuno(NUNO_CV,840,-40,0)
           +head(1)
           +eyebrow("THE CV CLINIC",204)
           +f"<div style=\"position:absolute;left:56px;top:266px;width:480px;font-family:Inter;font-weight:700;font-size:64px;line-height:1.0;letter-spacing:-2px;color:{INK};word-break:keep-all;\">A recruiter reads your CV in {hl}</div>"
           +f"<div style='position:absolute;left:58px;top:580px;'>{timer}</div>"
           +footer(swipe=False))
    R("d1-cv",1,inner)

# ---- Slide 2: the 7-second scan ----
def d1_s2():
    inner=(bg()+dots("right:60px;bottom:150px;")
           +head(2)+eyebrow("THE 7-SECOND SCAN",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:500px;font-family:Inter;font-weight:700;font-size:56px;line-height:1.02;letter-spacing:-1.5px;color:{INK};'>Most of it hits the <span style='color:{AMBER};'>top third.</span></div>"
           +f"<div style=\"position:absolute;left:58px;top:452px;width:470px;font-family:'DM Sans';font-weight:500;font-size:30px;line-height:1.4;color:{MUT};\">Name, target role and top skills are your audition. Miss it there and they never reach the good bits.</div>"
           +f"<div style='position:absolute;left:58px;top:660px;'>{callout('clock','First impressions happen in <b style=color:'+AMBER+'>7 seconds.</b>')}</div>"
           +f"<div style='position:absolute;right:96px;top:236px;'>{cv_card(mode='heat')}"
           +f"<div style='position:absolute;left:-42px;top:120px;transform:rotate(-90deg);transform-origin:left top;font-family:Inter;font-weight:700;font-size:20px;color:{AMBER};letter-spacing:3px;'>FIRST 7 SEC</div></div>"
           +footer())
    R("d1-cv",2,inner)

# ---- Slide 3: own the top third ----
def d1_s3():
    li=badgelist([("user","Name &amp; target role","The exact job you are after."),
                  ("target","A two-line summary","Lead with your strongest proof."),
                  ("star","Matching skills","Echo the words in the advert.")])
    inner=(bg()+head(3)+eyebrow("WIN THE TOP THIRD",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:520px;font-family:Inter;font-weight:700;font-size:58px;line-height:1.0;letter-spacing:-2px;color:{INK};'>Put these three first.</div>"
           +f"<div style='position:absolute;left:58px;top:392px;width:520px;'>{li}</div>"
           +f"<div style='position:absolute;right:80px;top:280px;'>{cv_card(mode='focus')}</div>"
           +footer())
    R("d1-cv",3,inner)

# ---- Slide 4: cut what gets you binned ----
def d1_s4():
    li=badgelist([("x","Typos &amp; wonky dates","One slip and it is gone."),
                  ("x","Walls of text","No one reads a grey block."),
                  ("x","'Responsible for...'","Duties with nothing to show.")],color=CORAL)
    ba=(f"<div style='position:absolute;left:56px;right:56px;bottom:132px;background:{DEEP};border-radius:18px;padding:26px 30px;border:1px solid rgba(255,255,255,.08);'>"
        f"<div style='display:flex;align-items:center;gap:14px;margin-bottom:16px;'><span style=\"font-family:{MONO};font-weight:700;font-size:19px;color:{CORAL};letter-spacing:2px;\">BEFORE</span>"
        f"<span style=\"font-family:'DM Sans';font-size:28px;color:{MUT};text-decoration:line-through;\">Responsible for the socials.</span></div>"
        f"<div style='display:flex;align-items:center;gap:14px;'><span style=\"font-family:{MONO};font-weight:700;font-size:19px;color:{GREEN};letter-spacing:2px;\">AFTER&nbsp;</span>"
        f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:28px;color:{INK};\">Grew Instagram 3x in 4 months.</span></div></div>")
    inner=(bg()+head(4)+eyebrow("RED FLAGS",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:760px;font-family:Inter;font-weight:700;font-size:58px;line-height:1.0;letter-spacing:-2px;color:{INK};'>Cut what gets you <span style='color:{CORAL};'>binned.</span></div>"
           +f"<div style='position:absolute;left:58px;top:388px;width:840px;'>{li}</div>"
           +ba+footer())
    R("d1-cv",4,inner)

# ---- Slide 5: CTA ----
def d1_cta():
    li=badgelist([("search","Discover","live UK internships"),
                  ("doc","Build","a CV that gets seen"),
                  ("rocket","Launch","your career")])
    urlpill=(f"<div style='display:inline-flex;align-items:center;border:2px solid {AMBER};border-radius:14px;padding:10px 22px;'>"
             f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;color:{AMBER};\">internwise.co.uk</span></div>")
    inner=(bg()+arc(1010,470,360)+nuno(NUNO_THUMB,780,-30,0)
           +f"<div style='position:absolute;left:56px;top:44px;'><img src='{WHT}' style='height:{LOGO}px;'></div>"
           +f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;color:{MUT};letter-spacing:2px;\"><span style='color:{AMBER};'>05</span> / 05</div>"
           +eyebrow("YOUR MOVE",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:470px;font-family:Inter;font-weight:700;font-size:60px;line-height:1.0;letter-spacing:-2px;color:{INK};'>Now go get it <span style='color:{AMBER};'>seen.</span></div>"
           +f"<div style='position:absolute;left:58px;top:406px;width:470px;'>{li}</div>"
           +f"<div style='position:absolute;left:58px;top:706px;'>{urlpill}</div>"
           +footer(swipe=False))
    R("d1-cv",5,inner)

def urlpill():
    return (f"<div style='display:inline-flex;align-items:center;border:2px solid {AMBER};border-radius:14px;padding:10px 22px;'>"
            f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;color:{AMBER};\">internwise.co.uk</span></div>")
def logo_tl():
    return f"<div style='position:absolute;left:56px;top:44px;'><img src='{WHT}' style='height:{LOGO}px;'></div>"

# ============ D2 - Interview: Proof Cards (LIGHT index-card world) ============
CREAM="#EFE7D6"; INKB="#26201A"; INKM="#6E6455"; TEAL="#0E8C86"; TEALD="#0B6E69"; REDC="#E1613B"
def d2_paper():
    return ("<div style='position:absolute;inset:0;background-color:"+CREAM+";'></div>"
            "<div style='position:absolute;inset:0;background-image:radial-gradient(rgba(120,96,52,.07) 2px,transparent 2px);background-size:32px 32px;'></div>"
            "<div style='position:absolute;inset:0;background:radial-gradient(ellipse at 82% 60%,rgba(14,140,134,.12),transparent 55%);'></div>")
def d2_disc():
    return "<div style='position:absolute;right:-70px;top:150px;width:700px;height:700px;border-radius:50%;background:rgba(14,140,134,.10);'></div>"
def d2_logo():
    return f"<div style='position:absolute;left:56px;top:44px;'><img src='{WHT}' style='height:{LOGO}px;filter:brightness(0);'></div>"
def d2_head(n):
    return (d2_logo()+f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;color:{INKM};letter-spacing:2px;\"><span style='color:{TEAL};'>0{n}</span> / 05</div>")
def d2_eye(tag,top):
    return (f"<div style=\"position:absolute;left:58px;top:{top}px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{TEAL};letter-spacing:4px;\">{tag}</div>"
            f"<div style='position:absolute;left:58px;top:{top+34}px;width:64px;height:4px;background:{REDC};border-radius:2px;'></div>")
def d2_foot(swipe=True):
    f=(f"<div style='position:absolute;left:56px;bottom:44px;display:flex;align-items:center;gap:13px;'>"
       f"<div style='width:34px;height:34px;border-radius:50%;background:{TEAL};display:flex;align-items:center;justify-content:center;'>"
       f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
       f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:{INKM};letter-spacing:1px;\">internwise.co.uk</span></div>")
    if swipe: f+=f"<div style=\"position:absolute;right:58px;bottom:44px;font-family:'DM Sans';font-weight:600;font-size:23px;color:{TEAL};\">Swipe &rarr;</div>"
    return f
def d2_nuno(src,h,right,bottom):
    return f"<img src='{src}' style='position:absolute;right:{right}px;bottom:{bottom}px;height:{h}px;filter:drop-shadow(0 18px 34px rgba(50,38,20,.30));'>"
def icard(tab,title,parts,w=440,rot=-3):
    tags="".join(f"<span style='display:inline-block;margin:0 8px 9px 0;padding:7px 14px;border-radius:7px;background:{TEAL}12;border:1.5px solid {TEAL}55;font-family:Inter;font-weight:700;font-size:19px;color:{TEALD};'>{t}</span>" for t in parts)
    return (f"<div style='position:relative;width:{w}px;background:#FFFFFF;border-radius:14px;box-shadow:0 24px 48px rgba(60,44,20,.24);transform:rotate({rot}deg);overflow:hidden;'>"
            f"<div style='display:flex;align-items:center;gap:10px;background:{TEAL};padding:13px 20px;'>"
            f"<span style='width:10px;height:10px;border-radius:50%;background:#fff;opacity:.85;'></span>"
            f"<span style=\"font-family:Inter;font-weight:700;font-size:15px;color:#fff;letter-spacing:2px;\">{tab}</span></div>"
            f"<div style='padding:22px 26px 24px;'>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:28px;color:{INKB};letter-spacing:-.5px;line-height:1.08;\">{title}</div>"
            f"<div style='margin-top:16px;'>{tags}</div></div></div>")
def d2_list(rows):
    out=""
    for icon,label,desc in rows:
        out+=(f"<div style='display:flex;gap:20px;align-items:center;margin-bottom:24px;'>"
              f"<div style='flex:0 0 62px;width:62px;height:62px;border-radius:14px;background:{TEAL}12;border:1.5px solid {TEAL}55;display:flex;align-items:center;justify-content:center;'>{svg(icon,TEAL,30)}</div>"
              f"<div><div style=\"font-family:Inter;font-weight:700;font-size:30px;color:{INKB};letter-spacing:-.5px;\">{label}</div>"
              f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:25px;color:{INKM};line-height:1.28;\">{desc}</div></div></div>")
    return out
def d2_urlbtn():
    return (f"<div style='display:inline-flex;align-items:center;background:{TEAL};border-radius:14px;padding:14px 26px;box-shadow:0 14px 28px rgba(14,140,134,.3);'>"
            f"<span style=\"font-family:Inter;font-weight:700;font-size:28px;color:#fff;\">internwise.co.uk</span></div>")

def d2_hook():
    memo="<span style='color:"+REDC+";'>memorising</span>"
    card=icard("PROOF CARD","Tell me about yourself.",["Role","Proof","Direction"],w=430,rot=-3)
    inner=(d2_paper()+d2_disc()+d2_nuno(NUNO_HOWTO,840,-30,0)+d2_head(1)+d2_eye("THE INTERVIEW ROOM",204)
           +f"<div style=\"position:absolute;left:56px;top:262px;width:480px;font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;letter-spacing:-2px;color:{INKB};word-break:keep-all;\">Stop {memo} interview answers.</div>"
           +f"<div style='position:absolute;left:56px;top:566px;'>{card}</div>"
           +d2_foot(swipe=False))
    R("d2-interview",1,inner)
def d2_s2():
    hl="<span style='color:"+TEAL+";'>proof.</span>"
    c1=f"<div style='position:absolute;left:40px;top:60px;'>{icard('CARD 1','Tell me about yourself',['Role','Proof','Direction'],w=330,rot=-5)}</div>"
    c2=f"<div style='position:absolute;left:378px;top:20px;'>{icard('CARD 2','Why us?',['Product','People','Mission'],w=330,rot=2)}</div>"
    c3=f"<div style='position:absolute;left:716px;top:70px;'>{icard('CARD 3','Give me a challenge',['Situation','Action','Result'],w=330,rot=-3)}</div>"
    inner=(d2_paper()+d2_head(2)+d2_eye("BUILD 3 PROOF CARDS",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:900px;font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;letter-spacing:-2px;color:{INKB};'>Not speeches - {hl}</div>"
           +f"<div style='position:absolute;left:0;right:0;top:430px;height:420px;'>{c1}{c2}{c3}</div>"
           +d2_foot())
    R("d2-interview",2,inner)
def d2_s3():
    hl="<span style='color:"+TEAL+";'>yourself.</span>"
    li=d2_list([("user","Role","Who you are, in one line."),
                ("star","Proof","One result that backs it up."),
                ("arrowup","Direction","Why this, why now.")])
    inner=(d2_paper()+d2_head(3)+d2_eye("PROOF CARD 1",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:500px;font-family:Inter;font-weight:700;font-size:54px;line-height:1.0;letter-spacing:-2px;color:{INKB};'>Tell me about {hl}</div>"
           +f"<div style='position:absolute;left:58px;top:392px;width:500px;'>{li}</div>"
           +f"<div style='position:absolute;right:70px;top:410px;'>{icard('PROOF CARD','Tell me about yourself',['Role','Proof','Direction'],w=420,rot=3)}</div>"
           +d2_foot())
    R("d2-interview",3,inner)
def d2_s4():
    c2=icard("CARD 2","Why us?",["Product","People","Mission"],w=880,rot=-1)
    c3=icard("CARD 3","Give me a challenge",["Situation","Action","Result","Lesson"],w=880,rot=1)
    inner=(d2_paper()+d2_head(4)+d2_eye("PROOF CARDS 2 &amp; 3",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:880px;font-family:Inter;font-weight:700;font-size:54px;line-height:1.0;letter-spacing:-2px;color:{INKB};'>Same trick, two more.</div>"
           +f"<div style='position:absolute;left:100px;top:384px;'>{c2}<div style='height:26px;'></div>{c3}</div>"
           +d2_foot())
    R("d2-interview",4,inner)
def d2_cta():
    hl="<span style='color:"+TEAL+";'>proof.</span>"
    li=d2_list([("check","Three proof cards","tell-me / why-us / challenge"),
                ("star","Backed by results","not memorised lines"),
                ("chat","Questions ready","end strong")])
    inner=(d2_paper()+d2_disc()+d2_nuno(NUNO_AUTHORITY,800,-20,0)+d2_logo()
           +f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;color:{INKM};letter-spacing:2px;\"><span style='color:{TEAL};'>05</span> / 05</div>"
           +d2_eye("YOUR MOVE",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:470px;font-family:Inter;font-weight:700;font-size:60px;line-height:1.0;letter-spacing:-2px;color:{INKB};'>Walk in with {hl}</div>"
           +f"<div style='position:absolute;left:58px;top:406px;width:470px;'>{li}</div>"
           +f"<div style='position:absolute;left:58px;top:726px;'>{d2_urlbtn()}</div>"
           +d2_foot(swipe=False))
    R("d2-interview",5,inner)

# ============ D3 - First Internship: Day One (WARM sunrise world) ============
SUNA="#F26D5B"; SUNB="#FF9E6B"; CRW="#FFF5EC"; NVY3="#1B2A4A"
def d3_bg():
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(155deg,{SUNA} 0%,{SUNB} 100%);'></div>"
            "<div style='position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.10) 2px,transparent 2px);background-size:34px 34px;'></div>"
            "<div style='position:absolute;right:-130px;top:-130px;width:520px;height:520px;border-radius:50%;background:rgba(255,255,255,.10);'></div>")
def d3_logo():
    return f"<div style='position:absolute;left:56px;top:44px;'><img src='{WHT}' style='height:{LOGO}px;'></div>"
def d3_head(n):
    return (d3_logo()+f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;color:rgba(255,255,255,.7);letter-spacing:2px;\"><span style='color:#fff;'>0{n}</span> / 05</div>")
def d3_eye(tag,top):
    return (f"<div style=\"position:absolute;left:58px;top:{top}px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{CRW};letter-spacing:4px;\">{tag}</div>"
            f"<div style='position:absolute;left:58px;top:{top+34}px;width:64px;height:4px;background:{NVY3};border-radius:2px;'></div>")
def d3_foot(swipe=True):
    f=(f"<div style='position:absolute;left:56px;bottom:44px;display:flex;align-items:center;gap:13px;'>"
       f"<div style='width:34px;height:34px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;'>"
       f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{SUNA}' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
       f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:{CRW};letter-spacing:1px;\">internwise.co.uk</span></div>")
    if swipe: f+=f"<div style=\"position:absolute;right:58px;bottom:44px;font-family:'DM Sans';font-weight:600;font-size:23px;color:#fff;\">Swipe &rarr;</div>"
    return f
def d3_nuno(src,h,right,bottom):
    return f"<img src='{src}' style='position:absolute;right:{right}px;bottom:{bottom}px;height:{h}px;filter:drop-shadow(0 18px 34px rgba(90,30,20,.35));'>"
def d3_list(rows):
    out=""
    for icon,label,desc in rows:
        out+=(f"<div style='display:flex;gap:20px;align-items:center;margin-bottom:24px;'>"
              f"<div style='flex:0 0 62px;width:62px;height:62px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;'>{svg(icon,SUNA,30)}</div>"
              f"<div><div style=\"font-family:Inter;font-weight:700;font-size:30px;color:#fff;letter-spacing:-.5px;\">{label}</div>"
              f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:25px;color:{CRW};line-height:1.28;\">{desc}</div></div></div>")
    return out
def d3_pass(week=1):
    off="#e7ddd0"
    seg="".join(f"<div style='flex:1;height:9px;border-radius:4px;background:{SUNA if i<week else off};'></div>" for i in range(12))
    def bar(width,h=12,c="#d8cabb",mt=0): return f"<div style='width:{width};height:{h}px;border-radius:3px;background:{c};margin-top:{mt}px;'></div>"
    return (f"<div style='position:relative;width:400px;background:#fff;border-radius:18px;box-shadow:0 30px 60px rgba(90,30,20,.30);padding:30px 28px 26px;'>"
            f"<div style='position:absolute;left:50%;top:-13px;transform:translateX(-50%);width:74px;height:13px;background:{NVY3};border-radius:7px;'></div>"
            f"<div style='display:flex;gap:18px;align-items:center;'>"
            f"<div style='flex:0 0 84px;width:84px;height:84px;border-radius:14px;background:{SUNA}22;border:2px solid {SUNA};display:flex;align-items:center;justify-content:center;'>{svg('user',SUNA,40)}</div>"
            f"<div style='flex:1;'>{bar('82%',18,'#2a3550')}<div style='height:9px;'></div>{bar('55%',13,SUNA)}</div></div>"
            f"<div style='margin-top:20px;padding-top:16px;border-top:1px solid #eee2d6;'>"
            f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:13px;letter-spacing:3px;color:#9a8c7d;\">INTERN PASS &middot; WEEK {week} OF 12</div>"
            f"<div style='display:flex;gap:6px;margin-top:12px;'>{seg}</div></div></div>")
def d3_urlbtn():
    return (f"<div style='display:inline-flex;align-items:center;background:#fff;border-radius:14px;padding:14px 26px;box-shadow:0 14px 28px rgba(90,30,20,.25);'>"
            f"<span style=\"font-family:Inter;font-weight:700;font-size:28px;color:{SUNA};\">internwise.co.uk</span></div>")
def d3_hook():
    hl="<span style='color:"+NVY3+";'>audition.</span>"
    inner=(d3_bg()+d3_nuno(NUNO_UTILITY,840,-30,0)+d3_head(1)+d3_eye("DAY ONE",204)
           +f"<div style=\"position:absolute;left:56px;top:262px;width:490px;font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;letter-spacing:-2px;color:#fff;word-break:keep-all;\">Your internship is a 12-week {hl}</div>"
           +f"<div style='position:absolute;left:58px;top:566px;'>{d3_pass(1)}</div>"+d3_foot(swipe=False))
    R("d3-internship",1,inner)
def d3_s2():
    hl="<span style='color:"+NVY3+";'>first week.</span>"
    li=d3_list([("user","Learn names fast","People remember who remembered them."),
                ("chat","Ask the 'dumb' questions","Week one is the only free pass."),
                ("target","Find the one goal","Know what good looks like here.")])
    inner=(d3_bg()+d3_head(2)+d3_eye("WEEK ONE",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:820px;font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;letter-spacing:-2px;color:#fff;'>Nail the {hl}</div>"
           +f"<div style='position:absolute;left:58px;top:392px;width:900px;'>{li}</div>"+d3_foot())
    R("d3-internship",2,inner)
def d3_s3():
    hl="<span style='color:"+NVY3+";'>noticed.</span>"
    li=d3_list([("check","Be the reliable one","Do what you said, on time."),
                ("bulb","Take the boring jobs","Own them, then improve them."),
                ("doc","Follow up in writing","A short recap after each task.")])
    inner=(d3_bg()+d3_head(3)+d3_eye("STAND OUT",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:820px;font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;letter-spacing:-2px;color:#fff;'>Then get {hl}</div>"
           +f"<div style='position:absolute;left:58px;top:392px;width:900px;'>{li}</div>"+d3_foot())
    R("d3-internship",3,inner)
def d3_s4():
    hl="<span style='color:"+NVY3+";'>offer.</span>"
    li=d3_list([("arrowup","Show impact","Numbers, not tasks."),
                ("heart","Build real relationships","People hire people they rate."),
                ("handshake","Ask before you leave","'What would it take to stay?'")])
    inner=(d3_bg()+d3_head(4)+d3_eye("THE ENDGAME",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:860px;font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;letter-spacing:-2px;color:#fff;'>Turn it into an {hl}</div>"
           +f"<div style='position:absolute;left:58px;top:392px;width:900px;'>{li}</div>"+d3_foot())
    R("d3-internship",4,inner)
def d3_cta():
    hl="<span style='color:"+NVY3+";'>count.</span>"
    li=d3_list([("check","Own the first week","learn, ask, aim"),
                ("star","Reliable and visible","impact over tasks"),
                ("handshake","Ask for the offer","before you leave")])
    inner=(d3_bg()+d3_nuno(NUNO_DOTHIS2,780,-20,0)+d3_logo()
           +f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;color:rgba(255,255,255,.7);letter-spacing:2px;\"><span style='color:#fff;'>05</span> / 05</div>"
           +d3_eye("YOUR MOVE",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:470px;font-family:Inter;font-weight:700;font-size:60px;line-height:1.0;letter-spacing:-2px;color:#fff;'>Make it {hl}</div>"
           +f"<div style='position:absolute;left:58px;top:406px;width:470px;'>{li}</div>"
           +f"<div style='position:absolute;left:58px;top:726px;'>{d3_urlbtn()}</div>"+d3_foot(swipe=False))
    R("d3-internship",5,inner)

# ============ D4 - Hidden Job Market (OCEAN world, single, no Nuno) ============
SURF="#1C8FA0"; DEEP4="#062A44"; ICE="#EAF4FA"; CYAN="#66D6E6"
def d4_bg():
    bubbles="".join(f"<div style='position:absolute;left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;border:2px solid rgba(255,255,255,.13);'></div>" for (x,y,r) in [(120,650,26),(180,760,14),(96,860,18),(560,700,20),(640,830,12),(500,900,16)])
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(180deg,{SURF} 0%,#0d5a6e 42%,{DEEP4} 100%);'></div>"+bubbles
            +"<div style='position:absolute;left:0;right:0;top:372px;height:3px;background:rgba(160,232,242,.65);box-shadow:0 0 22px rgba(120,222,236,.55);'></div>"
            +"<div style='position:absolute;left:0;right:0;top:302px;height:70px;background:linear-gradient(180deg,rgba(255,255,255,.10),transparent);'></div>")
def d4_logo():
    return f"<div style='position:absolute;left:56px;top:44px;'><img src='{WHT}' style='height:{LOGO}px;'></div>"
def d4_eye(tag,top):
    return (f"<div style=\"position:absolute;left:58px;top:{top}px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{CYAN};letter-spacing:4px;\">{tag}</div>"
            f"<div style='position:absolute;left:58px;top:{top+34}px;width:64px;height:4px;background:{CYAN};border-radius:2px;'></div>")
def d4_foot():
    return (f"<div style='position:absolute;left:56px;bottom:44px;display:flex;align-items:center;gap:13px;'>"
            f"<div style='width:34px;height:34px;border-radius:50%;background:{CYAN};display:flex;align-items:center;justify-content:center;'>"
            f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{DEEP4}' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
            f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:{ICE};letter-spacing:1px;\">internwise.co.uk</span></div>")
def d4_list(rows):
    out=""
    for icon,label,desc in rows:
        out+=(f"<div style='display:flex;gap:18px;align-items:center;margin-bottom:22px;'>"
              f"<div style='flex:0 0 58px;width:58px;height:58px;border-radius:50%;border:2px solid {CYAN}99;background:rgba(102,214,230,.12);display:flex;align-items:center;justify-content:center;'>{svg(icon,CYAN,28)}</div>"
              f"<div><div style=\"font-family:Inter;font-weight:700;font-size:29px;color:#fff;letter-spacing:-.5px;\">{label}</div>"
              f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:24px;color:#Bfe0ea;line-height:1.26;\">{desc}</div></div></div>")
    return out
def d4():
    hl="<span style='color:"+CYAN+";'>tip.</span>"
    ice=("<svg width='430' height='560' viewBox='0 0 430 560'>"
         "<polygon points='215,40 286,222 144,222' fill='#EAF4FA'/><polygon points='215,40 286,222 215,222' fill='#CFE2F0'/>"
         "<polygon points='142,222 290,222 378,392 318,540 100,548 52,392' fill='#5E86A6'/>"
         "<polygon points='142,222 215,222 182,346 100,346' fill='#7AA0BE' opacity='.5'/>"
         "<polygon points='215,222 290,222 378,392 238,384' fill='#4C7290' opacity='.6'/></svg>")
    berg=(f"<div style='position:absolute;right:64px;top:150px;width:430px;height:560px;'>{ice}"
          f"<div style=\"position:absolute;left:0;right:0;top:8px;text-align:center;font-family:Inter;font-weight:700;font-size:18px;color:{ICE};letter-spacing:3px;\">ADVERTISED</div>"
          f"<div style=\"position:absolute;left:0;right:0;top:330px;text-align:center;font-family:Inter;font-weight:700;font-size:26px;color:#EAF4FA;letter-spacing:1px;line-height:1.2;\">THE HIDDEN<br>MARKET</div></div>")
    li=d4_list([("handshake","Referrals","A warm intro beats the portal."),
                ("chat","Speculative emails","Ask before a role exists."),
                ("briefcase","SMEs &amp; startups","They hire all year, less noise."),
                ("user","Your network","Tutors, alumni, past managers.")])
    inner=(d4_bg()+d4_logo()+d4_eye("THE HIDDEN JOB MARKET",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:540px;font-family:Inter;font-weight:700;font-size:54px;line-height:1.02;letter-spacing:-2px;color:#fff;'>The jobs you see are the {hl}</div>"
           +berg
           +f"<div style='position:absolute;left:58px;top:452px;width:520px;'>{li}</div>"
           +d4_foot())
    R("d4-hidden",1,inner)

# ============ D5 - Rejected? Reset (PLUM world, single, no Nuno) ============
PLUM1="#3A1F5C"; PLUM2="#20123A"; LIME="#C8FF4D"; LAV="#CBB8E8"; INKW="#F3EEFA"
def d5_bg():
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,{PLUM1} 0%,{PLUM2} 100%);'></div>"
            "<div style='position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.05) 1.5px,transparent 1.5px);background-size:30px 30px;'></div>")
def d5_logo():
    return f"<div style='position:absolute;left:56px;top:44px;'><img src='{WHT}' style='height:{LOGO}px;'></div>"
def d5_eye(tag,top):
    return (f"<div style=\"position:absolute;left:58px;top:{top}px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{LIME};letter-spacing:4px;\">{tag}</div>"
            f"<div style='position:absolute;left:58px;top:{top+34}px;width:64px;height:4px;background:{LIME};border-radius:2px;'></div>")
def d5_foot():
    return (f"<div style='position:absolute;left:56px;bottom:44px;display:flex;align-items:center;gap:13px;'>"
            f"<div style='width:34px;height:34px;border-radius:50%;background:{LIME};display:flex;align-items:center;justify-content:center;'>"
            f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{PLUM2}' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
            f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:{LAV};letter-spacing:1px;\">internwise.co.uk</span></div>")
def d5_list(rows):
    out=""
    for icon,label,desc in rows:
        out+=(f"<div style='display:flex;gap:18px;align-items:center;margin-bottom:22px;'>"
              f"<div style='flex:0 0 58px;width:58px;height:58px;border-radius:50%;border:2px solid {LIME}88;background:rgba(200,255,77,.10);display:flex;align-items:center;justify-content:center;'>{svg(icon,LIME,28)}</div>"
              f"<div><div style=\"font-family:Inter;font-weight:700;font-size:29px;color:#fff;letter-spacing:-.5px;\">{label}</div>"
              f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:24px;color:{LAV};line-height:1.26;\">{desc}</div></div></div>")
    return out
def d5():
    hl="<span style='color:"+LIME+";'>data,</span>"
    grid="".join(f"<line x1='0' y1='{y}' x2='940' y2='{y}' stroke='rgba(255,255,255,.06)' stroke-width='1'/>" for y in (40,100,160,220))
    chart=(f"<svg width='940' height='260' viewBox='0 0 940 260'>{grid}"
           "<polyline points='30,120 190,124 350,214 520,182 700,104 910,40' fill='none' stroke='#C8FF4D' stroke-width='6' stroke-linecap='round' stroke-linejoin='round'/>"
           "<circle cx='350' cy='214' r='11' fill='#FF6B6B'/><circle cx='910' cy='40' r='11' fill='#C8FF4D'/>"
           "<text x='350' y='250' text-anchor='middle' font-family='Inter' font-weight='700' font-size='22' fill='#FF6B6B'>Rejected</text>"
           "<text x='906' y='30' text-anchor='end' font-family='Inter' font-weight='700' font-size='22' fill='#C8FF4D'>Offer</text></svg>")
    li=d5_list([("chat","Ask for one specific fix","'What would have made me a yes?'"),
                ("bulb","Change one thing","Not everything - one thing."),
                ("refresh","Send the next one","Momentum beats moping.")])
    inner=(d5_bg()+d5_logo()+d5_eye("REJECTED? RESET.",196)
           +f"<div style='position:absolute;left:56px;top:250px;width:680px;font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;letter-spacing:-2px;color:#fff;'>A 'no' is {hl} not a verdict.</div>"
           +f"<div style='position:absolute;left:56px;top:392px;'>{chart}</div>"
           +f"<div style='position:absolute;left:58px;top:686px;width:960px;'>{li}</div>"
           +d5_foot())
    R("d5-rejection",1,inner)

if __name__=="__main__":
    import sys
    only=sys.argv[1:]
    posts={"d1":[d1_hook,d1_s2,d1_s3,d1_s4,d1_cta],"d2":[d2_hook,d2_s2,d2_s3,d2_s4,d2_cta],
           "d3":[d3_hook,d3_s2,d3_s3,d3_s4,d3_cta],"d4":[d4],"d5":[d5]}
    for k,fns in posts.items():
        if only and k not in only: continue
        for fn in fns: fn()
    print("DONE",only or "ALL")
