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
NUNO_CV=_img(os.path.join(BASE,"assets","nuno","nuno_cv.png"))
NUNO_THUMB=_img(os.path.join(BASE,"assets","nuno","nuno_thumbsup.png"))
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

if __name__=="__main__":
    d1_hook(); d1_s2(); d1_s3(); d1_s4(); d1_cta(); print("DONE D1")
