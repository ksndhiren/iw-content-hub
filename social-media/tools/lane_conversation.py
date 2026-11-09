"""Poll/Conversation lane - the fifth Daily-5 post.

This replaces the old "fun" lane for future builds. The post should be useful
even without comments or votes: a career decision prompt, poll-like A/B/C
choice, comparison, or clear next step that nudges users toward saving/applying
on Internwise.

    render_conversation(idea, world, out_dir, "slide_1.png")
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L

NAVY, DEEP, INK = L.NAVY, L.DEEP, L.INK
AMBER, CORAL, GREEN = L.AMBER, L.CORAL, L.GREEN
CREAM = "#F3EADA"
NAVYT = "#152743"
LI_BLUE = "#0A66C2"


def _logo_dark(left=56, top=44, h=None):
    # h defaults to the uniform weekly LOGO height. Worlds that draw an inner
    # frame override it so the mark sits INSIDE the panel with real clear space
    # instead of straddling the border.
    return f"<img src='{L.DARKLOGO}' style='position:absolute;left:{left}px;top:{top}px;height:{h or L.LOGO}px;'>"


def _logo_white():
    return L.logo_tl()


def _footer(text="internwise.co.uk"):
    return (f"<div style='position:absolute;left:56px;bottom:46px;display:flex;align-items:center;gap:13px;'>"
            f"<div style='width:34px;height:34px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;'>"
            f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{DEEP}' stroke-width='2.6' "
            f"stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:22px;color:{NAVYT};letter-spacing:.3px;\">{text}</span></div>")


def _comment_prompt(left, top, dark=False, text="Comment A, B or C below"):
    ink = "#fff" if dark else NAVYT
    border = "rgba(255,255,255,.28)" if dark else "rgba(21,39,67,.18)"
    bg = "rgba(255,255,255,.10)" if dark else "rgba(255,255,255,.72)"
    return (f"<div style='position:absolute;left:{left}px;top:{top}px;height:46px;padding:0 18px;border-radius:23px;"
            f"background:{bg};border:2px solid {border};display:flex;align-items:center;gap:11px;'>"
            f"<div style='width:12px;height:12px;border-radius:50%;background:{AMBER};'></div>"
            f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:19px;color:{ink};letter-spacing:.4px;\">{text}</span></div>")


def _profile_avatar(left, top, size, border=6):
    src = L.img(os.path.join(L.BASE, "assets", "nuno", "linkedin_profile_black_male_professional.png"))
    inner = size - border * 2
    return (f"<div style='position:absolute;left:{left}px;top:{top}px;width:{size}px;height:{size}px;border-radius:50%;"
            f"background:#F8FBFF;border:{border}px solid #F8FBFF;overflow:hidden;box-shadow:0 8px 22px rgba(21,39,67,.16);'>"
            f"<img src='{src}' style='width:{inner}px;height:{inner}px;object-fit:cover;object-position:center top;'></div>")


def _option_rows(options, palette, dark=False):
    rows = ""
    letters = ["A", "B", "C"]
    ink = "#fff" if dark else NAVYT
    sub = "rgba(255,255,255,.72)" if dark else "#6F6350"
    for i, option in enumerate(options[:3]):
        rows += (f"<div style='display:flex;align-items:center;gap:16px;margin-bottom:16px;'>"
                 f"<div style='flex:0 0 52px;width:52px;height:52px;border-radius:50%;background:{palette[i]};"
                 f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:24px;color:{NAVYT};'>{letters[i]}</div>"
                 f"<div style=\"font-family:Inter;font-weight:900;font-size:31px;letter-spacing:-.7px;color:{ink};line-height:1.06;\">{option}</div>"
                 f"</div>")
    return rows


def w_decision_prompt(idea):
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
    texture = ("<div style='position:absolute;inset:0;opacity:.45;"
               "background-image:radial-gradient(rgba(21,39,67,.10) 1.3px,transparent 1.3px);"
               "background-size:32px 32px;'></div>")
    rail = f"<div style='position:absolute;right:0;top:0;bottom:0;width:192px;background:{NAVYT};'></div>"
    hook = (f"<div style=\"position:absolute;left:58px;top:176px;width:642px;font-family:Inter;font-weight:950;"
            f"font-size:64px;line-height:1.0;letter-spacing:-2.1px;color:{NAVYT};\">{idea['hook']}</div>")
    sub = (f"<div style=\"position:absolute;left:62px;top:404px;width:548px;font-family:'DM Sans';font-weight:750;"
           f"font-size:26px;line-height:1.28;color:#6F6350;\">{idea.get('subhead','')}</div>")
    board = (f"<div style='position:absolute;left:58px;top:542px;width:650px;background:#fff;border:3px solid {NAVYT};"
             f"box-shadow:0 26px 54px rgba(21,39,67,.14);padding:24px 24px 14px;'>")
    rows = ""
    colors = [AMBER, CORAL, GREEN]
    letters = ["A", "B", "C"]
    for i, option in enumerate(options):
        rows += (f"<div style='display:flex;align-items:center;gap:18px;margin-bottom:18px;'>"
                 f"<div style='flex:0 0 50px;width:50px;height:50px;border-radius:14px;background:{colors[i]};"
                 f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:24px;color:{NAVYT};'>{letters[i]}</div>"
                 f"<div style=\"font-family:Inter;font-weight:950;font-size:31px;line-height:1.05;letter-spacing:-.8px;color:{NAVYT};\">{option}</div></div>")
    board += rows + "</div>"
    rail_mark = (f"<div style='position:absolute;right:50px;top:250px;width:80px;height:540px;border:2px solid rgba(255,255,255,.18);'></div>"
                 f"<div style=\"position:absolute;right:44px;top:326px;font-family:'DM Sans';font-weight:900;font-size:18px;"
                 f"color:{AMBER};letter-spacing:5px;writing-mode:vertical-rl;transform:rotate(180deg);\">TRUST CHECK</div>")
    cta = (f"<div style='position:absolute;left:58px;top:820px;height:58px;padding:0 24px;border-radius:12px;background:{CORAL};"
           f"display:flex;align-items:center;box-shadow:0 16px 28px rgba(255,107,107,.24);'>"
           f"<span style=\"font-family:Inter;font-weight:900;font-size:24px;color:#fff;\">{idea.get('cta','Start at internwise.co.uk')}</span></div>")
    label = (f"<div style='position:absolute;right:58px;top:58px;height:42px;padding:0 18px;border-radius:21px;background:{AMBER};"
             f"display:flex;align-items:center;font-family:'DM Sans';font-weight:900;font-size:17px;color:{NAVYT};letter-spacing:2px;'>CAREER CHOICE</div>")
    return bg + texture + rail + rail_mark + _logo_dark() + label + hook + sub + board + cta + _comment_prompt(58, 900) + _footer()


def w_proofboard(idea):
    """Evidence-board layout for proof/application prompts. Distinct from the
    Monday decision-board: no right rail, no cream/plum diagonal language."""
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(135deg,#F7F4EC 0%,#E9F3F5 100%);'></div>"
    pinboard = (f"<div style='position:absolute;left:44px;top:160px;width:992px;height:744px;border-radius:28px;"
                f"background:#fff;box-shadow:0 28px 70px rgba(21,39,67,.15);border:4px solid {NAVYT};'></div>")
    top_rule = f"<div style='position:absolute;left:88px;right:88px;top:232px;height:4px;background:{AMBER};'></div>"
    label = (f"<div style='position:absolute;left:88px;top:198px;font-family:\"DM Sans\";font-weight:900;font-size:18px;"
             f"letter-spacing:4px;color:{LI_BLUE};'>APPLICATION PROOF</div>")
    headline = (f"<div style=\"position:absolute;left:88px;top:274px;width:600px;font-family:Inter;font-weight:950;"
                f"font-size:60px;line-height:1.02;letter-spacing:-1.8px;color:{NAVYT};\">{idea['hook']}</div>")
    note = (f"<div style=\"position:absolute;left:88px;top:488px;width:438px;font-family:'DM Sans';font-weight:700;"
            f"font-size:27px;line-height:1.28;color:#6F6350;\">{idea.get('subhead','')}</div>")
    profile = (f"<div style='position:absolute;right:92px;top:244px;width:280px;height:330px;border-radius:22px;background:{LI_BLUE};"
               f"box-shadow:0 22px 44px rgba(10,102,194,.24);overflow:hidden;'>"
               f"{_profile_avatar(24, 24, 74)}"
               f"<div style='position:absolute;left:24px;top:120px;width:210px;height:18px;border-radius:9px;background:#fff;'></div>"
               f"<div style='position:absolute;left:24px;top:154px;width:150px;height:12px;border-radius:6px;background:rgba(255,255,255,.62);'></div>"
               f"<div style='position:absolute;left:24px;right:24px;bottom:28px;height:86px;border-radius:16px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.28);'></div>"
               f"<div style=\"position:absolute;right:22px;top:20px;font-family:Inter;font-weight:950;font-size:46px;color:#fff;\">in</div></div>")
    card = (f"<div style='position:absolute;left:88px;top:628px;width:540px;padding:24px 28px 12px;border-radius:20px;"
            f"background:{NAVYT};box-shadow:0 20px 40px rgba(21,39,67,.18);'>{_option_rows(options, [AMBER, GREEN, CORAL], dark=True)}</div>")
    takeaway = (f"<div style='position:absolute;right:92px;top:612px;width:278px;font-family:IWSerif,Georgia,serif;font-style:italic;"
                f"font-weight:700;font-size:29px;line-height:1.2;color:{NAVYT};'>{idea.get('takeaway','')}</div>")
    # Comment pill and CTA share one row clear of the board (it ends at 904):
    # the pill used to sit on the board's bottom edge, half on, half off.
    cta = (f"<div style='position:absolute;right:92px;top:930px;height:54px;padding:0 20px;border-radius:8px;background:{AMBER};"
           f"display:flex;align-items:center;font-family:Inter;font-weight:900;font-size:22px;color:{NAVYT};'>{idea.get('cta','Start at internwise.co.uk')}</div>")
    return bg + _logo_dark() + pinboard + top_rule + label + headline + note + profile + card + takeaway + cta + _comment_prompt(88, 934)


def w_debate(idea):
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:{NAVYT};'></div>"
    split = f"<div style='position:absolute;left:0;top:0;bottom:0;width:48%;background:#F3EADA;clip-path:polygon(0 0,100% 0,78% 100%,0 100%);'></div>"
    hook = (f"<div style=\"position:absolute;left:60px;top:196px;width:430px;font-family:Inter;font-weight:950;"
            f"font-size:64px;line-height:1.02;letter-spacing:-1.8px;color:{NAVYT};\">{idea['hook']}</div>")
    sub = (f"<div style=\"position:absolute;left:64px;top:540px;width:360px;font-family:'DM Sans';font-weight:800;"
           f"font-size:27px;line-height:1.24;color:#6F6350;\">{idea.get('subhead','')}</div>")
    rows = ""
    for i, option in enumerate(options):
        y = 218 + i * 150
        rows += (f"<div style='position:absolute;right:72px;top:{y}px;width:430px;min-height:104px;border-radius:18px;"
                 f"background:rgba(255,255,255,.09);border:2px solid rgba(255,255,255,.16);padding:22px 24px;'>"
                 f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:18px;color:{AMBER};letter-spacing:3px;\">OPTION {chr(65+i)}</div>"
                 f"<div style=\"margin-top:8px;font-family:Inter;font-weight:950;font-size:36px;line-height:1.05;color:#fff;\">{option}</div></div>")
    cta = (f"<div style='position:absolute;right:72px;bottom:90px;width:430px;font-family:IWSerif,Georgia,serif;font-style:italic;"
           f"font-weight:700;font-size:34px;line-height:1.12;color:{AMBER};'>{idea.get('cta','Start at internwise.co.uk')}</div>")
    return bg + split + _logo_dark() + _comment_prompt(578, 664, dark=True) + hook + sub + rows + cta + L.watermark(w=380, right=-80, bottom=-120, op=.06)


def w_scorecard(idea):
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:#EAF2FB;'></div>"
    header = f"<div style='position:absolute;left:0;right:0;top:0;height:180px;background:{NAVYT};'></div>"
    hook = (f"<div style=\"position:absolute;left:58px;top:222px;width:850px;font-family:Inter;font-weight:950;"
            f"font-size:62px;line-height:1.0;letter-spacing:-2px;color:{NAVYT};\">{idea['hook']}</div>")
    grid = ""
    for i, option in enumerate(options):
        x = 58 + i * 328
        grid += (f"<div style='position:absolute;left:{x}px;top:500px;width:292px;height:218px;border-radius:20px;background:#fff;"
                 f"box-shadow:0 18px 44px rgba(21,39,67,.14);padding:24px;border-top:12px solid {[AMBER,GREEN,CORAL][i]};'>"
                 f"<div style=\"font-family:Inter;font-weight:950;font-size:58px;color:{[AMBER,GREEN,CORAL][i]};\">{chr(65+i)}</div>"
                 f"<div style=\"font-family:Inter;font-weight:950;font-size:31px;line-height:1.08;color:{NAVYT};\">{option}</div></div>")
    takeaway = (f"<div style=\"position:absolute;left:62px;top:754px;width:640px;font-family:'DM Sans';font-weight:800;"
                f"font-size:25px;line-height:1.24;color:#53627A;\">{idea.get('takeaway','')}</div>")
    return bg + header + L.logo_tl() + _comment_prompt(644, 70, dark=True) + hook + grid + takeaway + _footer(idea.get("cta", "internwise.co.uk"))


def w_signal(idea):
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,#0C3038,#071615);'></div>"
    rings = (f"<div style='position:absolute;right:-180px;top:120px;width:690px;height:690px;border-radius:50%;border:44px solid {GREEN};opacity:.18;'></div>"
             f"<div style='position:absolute;right:20px;top:318px;width:290px;height:290px;border-radius:50%;border:24px solid {AMBER};opacity:.26;'></div>")
    label = (f"<div style=\"position:absolute;left:58px;top:196px;font-family:'DM Sans';font-weight:900;font-size:18px;"
             f"color:{GREEN};letter-spacing:5px;\">QUICK SIGNAL CHECK</div>")
    hook = (f"<div style=\"position:absolute;left:58px;top:250px;width:560px;font-family:Inter;font-weight:950;"
            f"font-size:68px;line-height:1.0;letter-spacing:-2px;color:#fff;\">{idea['hook']}</div>")
    rows = ""
    for i, option in enumerate(options):
        rows += (f"<div style='height:70px;margin-bottom:18px;display:flex;align-items:center;gap:18px;'>"
                 f"<div style='width:70px;height:70px;border-radius:18px;background:{[AMBER,GREEN,CORAL][i]};display:flex;align-items:center;justify-content:center;"
                 f"font-family:Inter;font-weight:950;font-size:30px;color:{NAVYT};'>{chr(65+i)}</div>"
                 f"<div style=\"font-family:Inter;font-weight:950;font-size:34px;color:#fff;\">{option}</div></div>")
    board = f"<div style='position:absolute;left:58px;top:584px;width:620px;'>{rows}</div>"
    cta = (f"<div style=\"position:absolute;left:58px;bottom:74px;font-family:'DM Sans';font-weight:900;font-size:25px;color:{AMBER};\">{idea.get('cta','internwise.co.uk')}</div>")
    return bg + rings + L.logo_tl() + label + hook + board + _comment_prompt(58, 850, dark=True) + cta


def w_vote_cards(idea):
    """Social poll layout: looks like a poll sticker/card, not a test question."""
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,#F5EFE3,#E8F4F2);'></div>"
    phone = (f"<div style='position:absolute;right:70px;top:150px;width:360px;height:760px;border-radius:48px;background:{NAVYT};"
             f"box-shadow:0 32px 70px rgba(21,39,67,.28);overflow:hidden;'>"
             f"<div style='position:absolute;left:28px;right:28px;top:30px;height:52px;border-radius:26px;background:rgba(255,255,255,.10);'></div>"
             f"<div style='position:absolute;left:28px;right:28px;bottom:32px;height:10px;border-radius:5px;background:rgba(255,255,255,.22);'></div></div>")
    sticker = (f"<div style='position:absolute;right:104px;top:250px;width:292px;background:#fff;border-radius:28px;"
               f"box-shadow:0 24px 54px rgba(0,0,0,.24);padding:28px 26px 18px;'>"
               f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:17px;color:{LI_BLUE};letter-spacing:3px;margin-bottom:18px;\">LIVE POLL</div>"
               f"<div style=\"font-family:Inter;font-weight:950;font-size:31px;line-height:1.05;color:{NAVYT};letter-spacing:-.7px;margin-bottom:24px;\">Pick the blocker</div>")
    for i, opt in enumerate(options):
        sticker += (f"<div style='height:64px;border:3px solid {[AMBER,GREEN,CORAL][i]};border-radius:32px;margin-bottom:14px;"
                    f"display:flex;align-items:center;padding:0 20px;gap:12px;'>"
                    f"<div style='width:28px;height:28px;border-radius:50%;border:4px solid {[AMBER,GREEN,CORAL][i]};'></div>"
                    f"<div style=\"font-family:Inter;font-weight:900;font-size:23px;color:{NAVYT};line-height:1.05;\">{opt}</div></div>")
    sticker += "</div>"
    label = (f"<div style=\"position:absolute;left:58px;top:192px;font-family:'DM Sans';font-weight:900;font-size:19px;"
             f"color:{GREEN};letter-spacing:5px;\">COMMENT YOUR VOTE</div>")
    hook = (f"<div style=\"position:absolute;left:58px;top:250px;width:570px;font-family:Inter;font-weight:950;"
            f"font-size:76px;line-height:.98;letter-spacing:-2.4px;color:{NAVYT};\">{idea['hook']}</div>")
    sub = (f"<div style=\"position:absolute;left:62px;top:560px;width:520px;font-family:'DM Sans';font-weight:800;"
           f"font-size:31px;line-height:1.26;color:#6F6350;\">{idea.get('subhead','')}</div>")
    cta = (f"<div style='position:absolute;left:58px;bottom:94px;height:62px;padding:0 26px;border-radius:31px;background:{AMBER};"
           f"display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:25px;color:{NAVYT};'>{idea.get('cta','Start at internwise.co.uk')}</div>")
    return bg + _logo_dark() + phone + sticker + label + hook + sub + _comment_prompt(58, 804) + cta


def w_shortlist_poll(idea):
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:{NAVYT};'></div>"
    board = f"<div style='position:absolute;left:52px;right:52px;top:168px;bottom:92px;border-radius:0;background:#F3EADA;box-shadow:0 28px 70px rgba(0,0,0,.28);'></div>"
    label = (f"<div style='position:absolute;left:94px;top:216px;height:44px;padding:0 18px;background:{AMBER};display:flex;align-items:center;'>"
             f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:18px;color:{NAVYT};letter-spacing:3px;\">SHORTLIST POLL</span></div>")
    hook = (f"<div style=\"position:absolute;left:94px;top:300px;width:780px;font-family:IWSerif,Georgia,serif;font-weight:700;"
            f"font-size:68px;line-height:1.0;color:{NAVYT};\">{idea['hook']}</div>")
    cards = ""
    for i, opt in enumerate(options):
        x = 94 + i * 300
        cards += (f"<div style='position:absolute;left:{x}px;top:610px;width:256px;height:236px;background:#fff;border:3px solid {NAVYT};"
                  f"box-shadow:10px 10px 0 {[AMBER,GREEN,CORAL][i]};padding:24px;'>"
                  f"<div style='width:44px;height:44px;border-radius:50%;border:4px solid {NAVYT};margin-bottom:20px;'></div>"
                  f"<div style=\"font-family:Inter;font-weight:950;font-size:32px;line-height:1.04;color:{NAVYT};letter-spacing:-.8px;\">{opt}</div>"
                  f"<div style=\"position:absolute;left:24px;bottom:22px;font-family:'DM Sans';font-weight:900;font-size:16px;color:#6F6350;letter-spacing:2px;\">OPTION {chr(65+i)}</div></div>")
    note = (f"<div style=\"position:absolute;left:94px;bottom:128px;font-family:'DM Sans';font-weight:900;font-size:27px;color:#6F6350;\">"
            f"{idea.get('cta','Compare roles at internwise.co.uk')}</div>")
    return bg + board + _logo_white() + label + hook + cards + _comment_prompt(94, 870) + note


def w_cv_poll(idea):
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,#0B1D36,#132B4A);'></div>"
    slip = f"<div style='position:absolute;left:70px;top:170px;width:940px;height:770px;border-radius:30px;background:#fff;transform:rotate(-1.2deg);box-shadow:0 30px 70px rgba(0,0,0,.35);'></div>"
    label = (f"<div style=\"position:absolute;left:120px;top:230px;font-family:'DM Sans';font-weight:900;font-size:18px;color:{CORAL};letter-spacing:4px;\">CV PROOF POLL</div>")
    hook = (f"<div style=\"position:absolute;left:120px;top:286px;width:600px;font-family:Inter;font-weight:950;font-size:68px;line-height:1.0;letter-spacing:-2px;color:{NAVYT};\">{idea['hook']}</div>")
    poll = ""
    for i, opt in enumerate(options):
        y = 560 + i * 104
        poll += (f"<div style='position:absolute;left:120px;top:{y}px;width:760px;height:74px;border-radius:37px;background:#F3EADA;"
                 f"display:flex;align-items:center;padding:0 22px;gap:18px;'>"
                 f"<div style='width:42px;height:42px;border-radius:50%;background:{[AMBER,GREEN,CORAL][i]};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:950;font-size:22px;color:{NAVYT};'>{chr(65+i)}</div>"
                 f"<div style=\"font-family:Inter;font-weight:950;font-size:31px;color:{NAVYT};letter-spacing:-.7px;\">{opt}</div>"
                 f"<div style='margin-left:auto;width:34px;height:34px;border:4px solid {NAVYT};border-radius:9px;'></div></div>")
    cta = (f"<div style='position:absolute;left:120px;bottom:116px;height:58px;padding:0 24px;border-radius:12px;background:{AMBER};"
           f"display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:24px;color:{NAVYT};'>{idea.get('cta','Build proof at internwise.co.uk')}</div>")
    return bg + slip + _logo_white() + label + hook + poll + _comment_prompt(120, 838) + cta


def w_route_map(idea):
    """Journey-map poll: each answer is a different route, useful for application blockers."""
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:#F6F1E7;'></div>"
    grid = ("<div style='position:absolute;inset:0;opacity:.34;"
            "background-image:linear-gradient(rgba(21,39,67,.11) 1px,transparent 1px),"
            "linear-gradient(90deg,rgba(21,39,67,.11) 1px,transparent 1px);"
            "background-size:54px 54px;'></div>")
    map_card = (f"<div style='position:absolute;left:66px;top:170px;width:948px;height:770px;background:#fff;"
                f"border:4px solid {NAVYT};box-shadow:16px 18px 0 {GREEN};'></div>")
    route = (f"<svg style='position:absolute;left:116px;top:520px;width:832px;height:230px;' viewBox='0 0 832 230' fill='none'>"
             f"<path d='M32 178 C190 50 310 42 444 136 S666 238 796 44' stroke='{NAVYT}' stroke-width='12' stroke-linecap='round' stroke-dasharray='20 22'/>"
             f"<circle cx='32' cy='178' r='20' fill='{AMBER}'/><circle cx='444' cy='136' r='20' fill='{CORAL}'/><circle cx='796' cy='44' r='20' fill='{GREEN}'/>"
             f"</svg>")
    label = (f"<div style=\"position:absolute;left:116px;top:232px;font-family:'DM Sans';font-weight:900;font-size:18px;"
             f"color:{GREEN};letter-spacing:5px;\">APPLICATION ROUTE</div>")
    hook = (f"<div style=\"position:absolute;left:116px;top:292px;width:720px;font-family:IWSerif,Georgia,serif;font-weight:700;"
            f"font-size:76px;line-height:.98;color:{NAVYT};\">{idea['hook']}</div>")
    sub = ""
    chips = ""
    for i, opt in enumerate(options):
        x = [116, 382, 640][i]
        y = [760, 682, 770][i]
        chips += (f"<div style='position:absolute;left:{x}px;top:{y}px;width:230px;min-height:92px;background:{[AMBER,CORAL,GREEN][i]};"
                  f"border:3px solid {NAVYT};box-shadow:8px 8px 0 rgba(21,39,67,.18);padding:16px 18px;'>"
                  f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:16px;letter-spacing:3px;color:{NAVYT};\">ROUTE {chr(65+i)}</div>"
                  f"<div style=\"font-family:Inter;font-weight:950;font-size:26px;line-height:1.02;color:{NAVYT};margin-top:6px;\">{opt}</div></div>")
    cta = (f"<div style=\"position:absolute;left:650px;top:904px;height:46px;padding:0 20px;border-radius:23px;background:{NAVYT};"
           f"display:flex;align-items:center;font-family:'DM Sans';font-weight:900;font-size:20px;color:#fff;\">"
           f"{idea.get('cta','Start at internwise.co.uk')}</div>")
    return bg + grid + map_card + _logo_dark() + label + hook + sub + route + chips + _comment_prompt(116, 900) + cta


def w_comment_wall(idea):
    """Editorial comment-wall poll: feels like a social conversation, not an MCQ card."""
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:{DEEP};'></div>"
    glow = (f"<div style='position:absolute;right:-180px;top:-140px;width:560px;height:560px;border-radius:50%;background:{CORAL};opacity:.16;'></div>"
            f"<div style='position:absolute;left:-130px;bottom:-140px;width:520px;height:520px;border-radius:50%;background:{GREEN};opacity:.13;'></div>")
    paper = (f"<div style='position:absolute;left:70px;top:150px;width:940px;height:724px;border-radius:34px;background:#F7F1E7;"
             f"box-shadow:0 34px 80px rgba(0,0,0,.38);overflow:hidden;'></div>")
    band = f"<div style='position:absolute;left:70px;top:150px;width:940px;height:112px;background:{AMBER};'></div>"
    label = (f"<div style=\"position:absolute;left:116px;top:190px;font-family:'DM Sans';font-weight:950;font-size:18px;"
             f"letter-spacing:5px;color:{NAVYT};\">COMMENT THREAD</div>")
    hook = (f"<div style=\"position:absolute;left:116px;top:302px;width:560px;font-family:Inter;font-weight:950;"
            f"font-size:68px;line-height:.98;letter-spacing:-2.1px;color:{NAVYT};\">{idea['hook']}</div>")
    quote = (f"<div style='position:absolute;right:116px;top:500px;width:258px;background:#fff;border:3px solid {NAVYT};"
             f"box-shadow:8px 8px 0 rgba(21,39,67,.12);padding:16px 18px 18px;'>"
             f"<div style=\"font-family:'DM Sans';font-weight:950;font-size:13px;letter-spacing:3px;color:{GREEN};margin-bottom:9px;\">WHY IT MATTERS</div>"
             f"<div style=\"font-family:IWSerif,Georgia,serif;font-style:italic;font-weight:700;font-size:23px;line-height:1.12;color:{CORAL};\">{idea.get('takeaway','')}</div></div>")
    bubbles = ""
    for i, opt in enumerate(options):
        y = 676 + i * 66
        width = [700, 620, 672][i]
        bubbles += (f"<div style='position:absolute;left:116px;top:{y}px;width:{width}px;min-height:54px;border-radius:28px;"
                    f"background:{['#fff','#EAF2FB','#fff'][i]};border:3px solid {NAVYT};display:flex;align-items:center;gap:16px;"
                    f"padding:8px 18px;box-shadow:7px 7px 0 rgba(21,39,67,.12);'>"
                    f"<div style='width:38px;height:38px;border-radius:50%;background:{[AMBER,GREEN,CORAL][i]};display:flex;align-items:center;justify-content:center;"
                    f"font-family:Inter;font-weight:950;font-size:18px;color:{NAVYT};'>{chr(65+i)}</div>"
                    f"<div style=\"font-family:Inter;font-weight:950;font-size:25px;color:{NAVYT};letter-spacing:-.5px;\">{opt}</div></div>")
    cta = (f"<div style='position:absolute;right:116px;bottom:92px;height:50px;padding:0 22px;border-radius:25px;background:{NAVYT};"
           f"display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:23px;color:#fff;'>{idea.get('cta','internwise.co.uk')}</div>")
    return bg + glow + paper + band + L.logo_tl() + label + hook + quote + bubbles + _comment_prompt(116, 884) + cta


# =================================================================================
#  WEEK 22 ADDITIONS
#  The bank held exactly 10 worlds and the lane only blocked ONE previous week, so
#  5-a-week selection became a hard two-week loop: week19 and week21 shipped the
#  identical five designs. Six more worlds plus a two-week block (build_week.py)
#  give the lane 16 to choose 5 from, so a design cannot return inside three weeks.
#  Each is a different physical metaphor, not a recolour of an existing one.
# =================================================================================

def w_ballot(idea):
    """Polling-station ballot paper: tick boxes, pencil, serial number, torn edge."""
    options = idea.get("options", [])[:3]
    bg = (f"<div style='position:absolute;inset:0;background:{NAVYT};'></div>"
          f"<div style='position:absolute;inset:0;opacity:.30;background-image:"
          f"linear-gradient(rgba(255,255,255,.10) 1px,transparent 1px);background-size:100% 46px;'></div>")

    # One pencil, built as a single rotated stack. The amber bar and its tip used
    # to be two siblings that each rotated about their OWN centre, so the point
    # drifted off the end of the body and read as a loose floating wedge.
    pencil = (f"<div style='position:absolute;left:946px;top:296px;width:38px;height:476px;transform:rotate(12deg);'>"
              f"<div style='height:30px;background:#E2857A;border-radius:7px 7px 0 0;'></div>"
              f"<div style='height:16px;background:#C9CDD4;'></div>"
              f"<div style='height:392px;background:{AMBER};'></div>"
              f"<div style='height:38px;background:#F0DEBE;clip-path:polygon(0 0,100% 0,50% 100%);'></div>"
              f"<div style='position:absolute;left:11px;top:460px;width:16px;height:16px;background:{NAVYT};"
              f"clip-path:polygon(0 0,100% 0,50% 100%);'></div></div>")

    # Everything printed on the ballot lives inside ONE rotated wrapper. Each
    # element used to carry its own transform:rotate(-1.2deg) and so turned about
    # its own centre, which left the torn strip visibly out of register with the
    # paper's bottom edge. The slip also now starts at y=182: at 122 its rotated
    # top-left corner rose into the logo instead of clearing it.
    serial = (f"<div style=\"position:absolute;left:48px;top:44px;font-family:'DM Sans';font-weight:700;font-size:20px;"
              f"color:#A2957E;letter-spacing:6px;\">BALLOT &middot; INTERNWISE &middot; NO. 022</div>")
    rule = f"<div style='position:absolute;left:48px;top:82px;width:676px;height:3px;background:{NAVYT};opacity:.75;'></div>"
    hook = (f"<div style='position:absolute;left:48px;top:120px;width:640px;'>"
            + L.hero(idea['hook'], "underline", NAVYT, NAVYT, hi=CORAL, size=58, width=640) + "</div>")
    sub = (f"<div style=\"position:absolute;left:50px;top:382px;width:600px;font-family:'DM Sans';font-weight:700;"
           f"font-size:27px;line-height:1.26;color:#6F6350;\">{idea.get('subhead','')}</div>")
    rows = ""
    for i, option in enumerate(options):
        y = 468 + i * 100
        rows += (f"<div style='position:absolute;left:48px;top:{y}px;width:664px;height:86px;display:flex;align-items:center;"
                 f"gap:24px;border-bottom:2px dashed rgba(21,39,67,.22);'>"
                 f"<div style='flex:0 0 62px;width:62px;height:62px;border:4px solid {NAVYT};display:flex;align-items:center;"
                 f"justify-content:center;font-family:Inter;font-weight:900;font-size:28px;color:{NAVYT};'>{chr(65+i)}</div>"
                 f"<div style=\"font-family:Inter;font-weight:800;font-size:34px;line-height:1.05;letter-spacing:-.8px;color:{NAVYT};\">{option}</div></div>")
    teeth = "".join("<div style='width:28px;height:26px;background:#FBF7EE;clip-path:polygon(0 0,100% 0,50% 100%);'></div>"
                    for _ in range(28))
    tear = f"<div style='position:absolute;left:0;top:782px;width:772px;display:flex;'>{teeth}</div>"
    slip = (f"<div style='position:absolute;left:92px;top:182px;width:772px;height:782px;background:#FBF7EE;"
            f"box-shadow:0 34px 74px rgba(0,0,0,.42);transform:rotate(-1.2deg);'>"
            f"{serial}{rule}{hook}{sub}{rows}{tear}</div>")

    cta = (f"<div style=\"position:absolute;left:142px;bottom:30px;font-family:'DM Sans';font-weight:900;font-size:24px;"
           f"color:{AMBER};\">{idea.get('cta','Start at internwise.co.uk')}</div>")
    return bg + pencil + slip + L.logo_tl() + cta


def w_dial(idea):
    """Gauge/meter: the three answers are positions on one arc, so the post reads as
    a spectrum ("where are you right now?") rather than a multiple-choice test."""
    options = idea.get("options", [])[:3]
    bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(120% 95% at 50% 110%,#17395F 0%,#0C1E38 58%,#07132A 100%);'></div>")
    arc = (f"<svg style='position:absolute;left:90px;top:300px;width:900px;height:520px;' viewBox='0 0 900 520' fill='none'>"
           f"<path d='M60 470 A390 390 0 0 1 840 470' stroke='rgba(255,255,255,.14)' stroke-width='58' stroke-linecap='round'/>"
           f"<path d='M60 470 A390 390 0 0 1 300 128' stroke='{CORAL}' stroke-width='58' stroke-linecap='round'/>"
           f"<path d='M330 112 A390 390 0 0 1 570 112' stroke='{AMBER}' stroke-width='58' stroke-linecap='round'/>"
           f"<path d='M600 128 A390 390 0 0 1 840 470' stroke='{GREEN}' stroke-width='58' stroke-linecap='round'/>"
           f"<circle cx='450' cy='470' r='26' fill='#fff'/>"
           f"<path d='M450 470 L246 236' stroke='#fff' stroke-width='14' stroke-linecap='round'/></svg>")
    label = (f"<div style='position:absolute;left:56px;top:150px;height:46px;padding:0 20px;border-radius:23px;"
             f"border:2px solid rgba(255,255,255,.26);display:flex;align-items:center;'>"
             f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:18px;color:{AMBER};letter-spacing:5px;\">WHERE ARE YOU TODAY</span></div>")
    hook = (f"<div style='position:absolute;left:56px;top:214px;width:700px;'>"
            + L.hero(idea['hook'], "serif_italic", "#fff", AMBER, hi=AMBER, size=58, width=700) + "</div>")
    cols = [CORAL, AMBER, GREEN]
    rows = ""
    for i, option in enumerate(options):
        x = 56 + i * 328
        rows += (f"<div style='position:absolute;left:{x}px;top:826px;width:304px;'>"
                 f"<div style='width:46px;height:46px;border-radius:50%;background:{cols[i]};display:flex;align-items:center;"
                 f"justify-content:center;font-family:Inter;font-weight:900;font-size:22px;color:{NAVYT};margin-bottom:14px;'>{chr(65+i)}</div>"
                 f"<div style=\"font-family:Inter;font-weight:800;font-size:31px;line-height:1.08;letter-spacing:-.7px;color:#fff;\">{option}</div></div>")
    return (bg + arc + L.logo_tl() + label + hook + rows
            + _comment_prompt(56, 988, dark=True, text="Comment A, B or C below"))


def w_receipt(idea):
    """Till receipt: the answers are itemised line entries under a total. Good for
    cost/trade-off prompts, and nothing else in the bank is a narrow centre column."""
    options = idea.get("options", [])[:3]
    bg = (f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
          f"<div style='position:absolute;inset:0;opacity:.5;background-image:"
          f"radial-gradient(rgba(21,39,67,.09) 1.4px,transparent 1.4px);background-size:30px 30px;'></div>")
    slip = (f"<div style='position:absolute;left:286px;top:176px;width:508px;height:788px;background:#fff;"
            f"box-shadow:0 30px 66px rgba(21,39,67,.20);'></div>")
    zig = "".join("<div style='width:26px;height:22px;background:#fff;clip-path:polygon(0 0,100% 0,50% 100%);'></div>" for _ in range(20))
    tear = f"<div style='position:absolute;left:286px;top:964px;width:508px;display:flex;'>{zig}</div>"
    head = (f"<div style=\"position:absolute;left:286px;top:212px;width:508px;text-align:center;font-family:'DM Sans';"
            f"font-weight:700;font-size:17px;color:#A2957E;letter-spacing:4px;\">CAREER LEDGER &middot; THIS WEEK</div>"
            f"<div style='position:absolute;left:326px;top:248px;width:428px;height:3px;background:{NAVYT};opacity:.2;'></div>")
    hook = (f"<div style=\"position:absolute;left:326px;top:278px;width:428px;text-align:center;font-family:Inter;"
            f"font-weight:900;font-size:44px;line-height:1.04;letter-spacing:-1.4px;color:{NAVYT};\">{idea['hook']}</div>")
    rows = ""
    for i, option in enumerate(options):
        y = 470 + i * 106
        rows += (f"<div style='position:absolute;left:326px;top:{y}px;width:428px;'>"
                 f"<div style='display:flex;align-items:baseline;gap:12px;'>"
                 f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:19px;color:{AMBER};letter-spacing:3px;\">{chr(65+i)}</span>"
                 f"<span style='flex:1;border-bottom:3px dotted rgba(21,39,67,.28);'></span></div>"
                 f"<div style=\"margin-top:6px;font-family:Inter;font-weight:800;font-size:33px;line-height:1.08;"
                 f"letter-spacing:-.7px;color:{NAVYT};\">{option}</div></div>")
    total = (f"<div style='position:absolute;left:326px;top:758px;width:428px;border-top:4px double {NAVYT};padding-top:14px;'>"
             f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:17px;color:#A2957E;letter-spacing:4px;\">TAKEAWAY</div>"
             f"<div style=\"margin-top:8px;font-family:IWSerif,Georgia,serif;font-style:italic;font-size:26px;"
             f"line-height:1.2;color:{NAVYT};\">{idea.get('takeaway','')}</div></div>")
    barcode = ("<div style='position:absolute;left:366px;top:900px;display:flex;align-items:flex-end;gap:4px;'>"
               + "".join(f"<div style='width:{3 if i%3 else 7}px;height:38px;background:{NAVYT};'></div>" for i in range(38))
               + "</div>")
    cta = (f"<div style=\"position:absolute;left:0;right:0;bottom:28px;text-align:center;font-family:'DM Sans';"
           f"font-weight:900;font-size:24px;color:{NAVYT};\">{idea.get('cta','Start at internwise.co.uk')}</div>")
    return (bg + slip + tear + head + hook + rows + total + barcode
            + _logo_dark() + cta + _comment_prompt(56, 186, text="A, B or C?"))


def w_stickies(idea):
    """Whiteboard with angled sticky notes - a workshop/brainstorm feel. The only
    world in the bank where the options are physical objects at different angles."""
    options = idea.get("options", [])[:3]
    bg = (f"<div style='position:absolute;inset:0;background:#F6F7F4;'></div>"
          f"<div style='position:absolute;left:40px;top:40px;right:40px;bottom:40px;border:14px solid #D8D2C4;border-radius:10px;'></div>"
          f"<div style='position:absolute;left:54px;top:54px;right:54px;bottom:54px;background:#FFFFFF;'></div>")
    tray = (f"<div style='position:absolute;left:54px;bottom:54px;right:54px;height:26px;background:#D8D2C4;'></div>"
            f"<div style='position:absolute;left:640px;bottom:62px;width:170px;height:16px;border-radius:8px;background:{CORAL};'></div>"
            f"<div style='position:absolute;left:826px;bottom:62px;width:130px;height:16px;border-radius:8px;background:{NAVYT};'></div>")
    hook = (f"<div style='position:absolute;left:100px;top:190px;width:600px;'>"
            + L.hero(idea['hook'], "highlight", NAVYT, NAVYT, hi=AMBER, size=56, width=600) + "</div>")
    sub = (f"<div style=\"position:absolute;left:102px;top:456px;width:520px;font-family:'DM Sans';font-weight:700;"
           f"font-size:26px;line-height:1.28;color:#6F6350;\">{idea.get('subhead','')}</div>")
    notes = ""
    spec = [(96, 556, -3.4, AMBER), (396, 592, 2.6, GREEN), (690, 548, -1.8, CORAL)]
    for i, option in enumerate(options):
        x, y, rot, col = spec[i]
        notes += (f"<div style='position:absolute;left:{x}px;top:{y}px;width:278px;height:278px;background:{col};"
                  f"transform:rotate({rot}deg);box-shadow:0 18px 32px rgba(21,39,67,.18);padding:26px;box-sizing:border-box;'>"
                  f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:18px;color:{NAVYT};letter-spacing:4px;opacity:.72;\">{chr(65+i)}</div>"
                  f"<div style=\"margin-top:14px;font-family:Inter;font-weight:800;font-size:34px;line-height:1.08;"
                  f"letter-spacing:-.9px;color:{NAVYT};\">{option}</div></div>")
    # The whiteboard's inner panel starts at 54px. At the uniform logo height and
    # left:56/top:44 the mark straddled the 14px frame border with no clear space,
    # so here it is sized down and inset to sit properly within the panel.
    return (bg + tray + _logo_dark(left=98, top=92, h=70) + hook + sub + notes
            + _comment_prompt(100, 904))


def w_bars(idea):
    """Poll-result bars - the look of a poll AFTER voting, which invites people to
    argue with the ranking. Deliberately has no option cards or circles."""
    options = idea.get("options", [])[:3]
    bg = (f"<div style='position:absolute;inset:0;background:#0B1E3A;'></div>"
          f"<div style='position:absolute;right:-180px;top:-140px;width:620px;height:620px;border-radius:50%;"
          f"background:radial-gradient(circle at 42% 42%,{AMBER}26,transparent 64%);'></div>")
    label = (f"<div style='position:absolute;left:56px;top:154px;height:44px;padding:0 18px;background:{AMBER};"
             f"display:flex;align-items:center;'>"
             f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:18px;color:{NAVYT};letter-spacing:4px;\">THE WEEKLY POLL</span></div>")
    hook = (f"<div style='position:absolute;left:56px;top:216px;width:820px;'>"
            + L.hero(idea['hook'], "scalejump", "#fff", AMBER, hi=AMBER, size=56, width=820) + "</div>")
    cols = [AMBER, GREEN, CORAL]
    widths = [856, 672, 498]
    rows = ""
    for i, option in enumerate(options):
        y = 586 + i * 136
        rows += (f"<div style='position:absolute;left:56px;top:{y}px;width:{widths[i]}px;height:112px;"
                 f"background:{cols[i]};display:flex;align-items:center;padding:0 26px;box-sizing:border-box;'>"
                 f"<div style=\"font-family:Inter;font-weight:900;font-size:35px;line-height:1.05;letter-spacing:-.9px;"
                 f"color:{NAVYT};\">{option}</div></div>"
                 f"<div style=\"position:absolute;left:{56 + widths[i] + 20}px;top:{y + 30}px;font-family:Inter;"
                 f"font-weight:900;font-size:40px;color:rgba(255,255,255,.34);\">{chr(65+i)}</div>")
    return (bg + L.logo_tl() + label + hook + rows
            + _comment_prompt(56, 988, dark=True, text="Which one would you put top?"))


def w_marquee(idea):
    """Three full-height colour columns, one answer each, set as a type poster. The
    only world that fills the whole canvas with the options themselves."""
    options = idea.get("options", [])[:3]
    cols = [CORAL, AMBER, GREEN]
    inks = ["#fff", NAVYT, NAVYT]
    # The column runs 470 -> 1080, but letter + label only filled its top ~230px,
    # leaving a flat slab of colour across the bottom third of the poster. Lay the
    # column out as a flex stack instead: letter at the top, the option set BIG in
    # the middle, and the reply hint on the baseline, so the colour carries content
    # all the way down.
    panels = ""
    for i, option in enumerate(options):
        x = i * 360
        hint_ink = "rgba(255,255,255,.72)" if i == 0 else "rgba(21,39,67,.62)"
        rule = "rgba(255,255,255,.34)" if i == 0 else "rgba(21,39,67,.26)"
        panels += (f"<div style='position:absolute;left:{x}px;top:470px;width:360px;bottom:0;background:{cols[i]};"
                   f"padding:34px 30px 38px;box-sizing:border-box;display:flex;flex-direction:column;"
                   f"justify-content:space-between;'>"
                   f"<div style=\"font-family:IWSerif,Georgia,serif;font-size:116px;line-height:.78;color:{inks[i]};opacity:.34;\">{chr(65+i)}</div>"
                   f"<div style=\"font-family:Inter;font-weight:900;font-size:46px;line-height:1.02;"
                   f"letter-spacing:-1.6px;color:{inks[i]};\">{option}</div>"
                   f"<div style='border-top:3px solid {rule};padding-top:14px;'>"
                   f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:21px;letter-spacing:1.4px;"
                   f"color:{hint_ink};\">REPLY {chr(65+i)}</span></div></div>")
    bg = f"<div style='position:absolute;inset:0;background:{NAVYT};'></div>"
    hook = (f"<div style='position:absolute;left:56px;top:178px;width:800px;'>"
            + L.hero(idea['hook'], "shadow", "#fff", AMBER, hi=CORAL, size=56, width=800) + "</div>")
    sub = (f"<div style=\"position:absolute;left:58px;top:400px;width:700px;font-family:'DM Sans';font-weight:700;"
           f"font-size:26px;line-height:1.24;color:rgba(255,255,255,.76);\">{idea.get('subhead','')}</div>")
    tag = (f"<div style=\"position:absolute;right:56px;top:60px;font-family:'DM Sans';font-weight:900;font-size:18px;"
           f"color:{AMBER};letter-spacing:5px;\">PICK YOUR LANE</div>")
    return bg + panels + L.logo_tl() + tag + hook + sub


WORLDS = {
    "decision": w_decision_prompt,
    "proofboard": w_proofboard,
    "debate": w_debate,
    "scorecard": w_scorecard,
    "signal": w_signal,
    "vote_cards": w_vote_cards,
    "shortlist_poll": w_shortlist_poll,
    "cv_poll": w_cv_poll,
    "route_map": w_route_map,
    "comment_wall": w_comment_wall,
    "ballot": w_ballot,
    "dial": w_dial,
    "receipt": w_receipt,
    "stickies": w_stickies,
    "bars": w_bars,
    "marquee": w_marquee,
}


def render_conversation(idea, world, out_dir, filename="slide_1.png"):
    return L.render(out_dir, filename, WORLDS[world](idea))


if __name__ == "__main__":
    ideas = L.load("conversation_ideas.json")["ideas"]
    for idea in ideas[:1]:
        render_conversation(idea, "decision", os.path.join(L.OUTROOT, "week18", "_conversation_test"))
