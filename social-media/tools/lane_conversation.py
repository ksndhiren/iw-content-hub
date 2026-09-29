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


def _logo_dark():
    return f"<img src='{L.DARKLOGO}' style='position:absolute;left:56px;top:44px;height:{L.LOGO}px;'>"


def _footer(text="internwise.co.uk"):
    return (f"<div style='position:absolute;left:56px;bottom:46px;display:flex;align-items:center;gap:13px;'>"
            f"<div style='width:34px;height:34px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;'>"
            f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{DEEP}' stroke-width='2.6' "
            f"stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:22px;color:{NAVYT};letter-spacing:.3px;\">{text}</span></div>")


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
    rail = f"<div style='position:absolute;right:0;top:0;bottom:0;width:168px;background:{NAVYT};'></div>"
    hook = (f"<div style=\"position:absolute;left:58px;top:190px;width:690px;font-family:Inter;font-weight:900;"
            f"font-size:74px;line-height:1.02;letter-spacing:-2.5px;color:{NAVYT};\">{idea['hook']}</div>")
    sub = (f"<div style=\"position:absolute;left:62px;top:374px;width:560px;font-family:'DM Sans';font-weight:700;"
           f"font-size:30px;line-height:1.28;color:#6F6350;\">{idea.get('subhead','')}</div>")
    board = (f"<div style='position:absolute;left:58px;top:510px;width:690px;background:#fff;border:3px solid {NAVYT};"
             f"box-shadow:0 26px 54px rgba(21,39,67,.14);padding:26px 26px 18px;'>")
    rows = ""
    colors = [AMBER, CORAL, GREEN]
    letters = ["A", "B", "C"]
    for i, option in enumerate(options):
        rows += (f"<div style='display:flex;align-items:center;gap:18px;margin-bottom:18px;'>"
                 f"<div style='flex:0 0 54px;width:54px;height:54px;border-radius:14px;background:{colors[i]};"
                 f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:26px;color:{NAVYT};'>{letters[i]}</div>"
                 f"<div style=\"font-family:Inter;font-weight:900;font-size:36px;letter-spacing:-.9px;color:{NAVYT};\">{option}</div></div>")
    board += rows + "</div>"
    rail_mark = (f"<div style='position:absolute;right:42px;top:270px;width:74px;height:520px;border:2px solid rgba(255,255,255,.18);'></div>"
                 f"<div style=\"position:absolute;right:38px;top:330px;font-family:'DM Sans';font-weight:900;font-size:18px;"
                 f"color:{AMBER};letter-spacing:5px;writing-mode:vertical-rl;transform:rotate(180deg);\">SAVE ONE ROLE</div>")
    cta = (f"<div style='position:absolute;left:58px;top:835px;height:58px;padding:0 24px;border-radius:12px;background:{CORAL};"
           f"display:flex;align-items:center;box-shadow:0 16px 28px rgba(255,107,107,.24);'>"
           f"<span style=\"font-family:Inter;font-weight:900;font-size:24px;color:#fff;\">{idea.get('cta','Start at internwise.co.uk')}</span></div>")
    label = (f"<div style='position:absolute;right:58px;top:58px;height:42px;padding:0 18px;border-radius:21px;background:{AMBER};"
             f"display:flex;align-items:center;font-family:'DM Sans';font-weight:900;font-size:17px;color:{NAVYT};letter-spacing:2px;'>CAREER CHOICE</div>")
    return bg + texture + rail + rail_mark + _logo_dark() + label + hook + sub + board + cta + _footer()


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
               f"<div style='position:absolute;left:24px;top:24px;width:74px;height:74px;border-radius:50%;background:#fff;'></div>"
               f"<div style='position:absolute;left:24px;top:120px;width:210px;height:18px;border-radius:9px;background:#fff;'></div>"
               f"<div style='position:absolute;left:24px;top:154px;width:150px;height:12px;border-radius:6px;background:rgba(255,255,255,.62);'></div>"
               f"<div style='position:absolute;left:24px;right:24px;bottom:28px;height:86px;border-radius:16px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.28);'></div>"
               f"<div style=\"position:absolute;right:22px;top:20px;font-family:Inter;font-weight:950;font-size:46px;color:#fff;\">in</div></div>")
    card = (f"<div style='position:absolute;left:88px;top:628px;width:540px;padding:24px 28px 12px;border-radius:20px;"
            f"background:{NAVYT};box-shadow:0 20px 40px rgba(21,39,67,.18);'>{_option_rows(options, [AMBER, GREEN, CORAL], dark=True)}</div>")
    takeaway = (f"<div style='position:absolute;right:92px;top:612px;width:278px;font-family:Georgia,serif;font-style:italic;"
                f"font-weight:700;font-size:29px;line-height:1.2;color:{NAVYT};'>{idea.get('takeaway','')}</div>")
    cta = (f"<div style='position:absolute;right:92px;bottom:118px;height:54px;padding:0 20px;border-radius:8px;background:{AMBER};"
           f"display:flex;align-items:center;font-family:Inter;font-weight:900;font-size:22px;color:{NAVYT};'>{idea.get('cta','Start at internwise.co.uk')}</div>")
    return bg + _logo_dark() + pinboard + top_rule + label + headline + note + profile + card + takeaway + cta


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
    cta = (f"<div style='position:absolute;right:72px;bottom:90px;width:430px;font-family:Georgia,serif;font-style:italic;"
           f"font-weight:700;font-size:34px;line-height:1.12;color:{AMBER};'>{idea.get('cta','Start at internwise.co.uk')}</div>")
    return bg + split + _logo_dark() + hook + sub + rows + cta + L.watermark(w=380, right=-80, bottom=-120, op=.06)


def w_scorecard(idea):
    options = idea.get("options", [])[:3]
    bg = f"<div style='position:absolute;inset:0;background:#EAF2FB;'></div>"
    header = f"<div style='position:absolute;left:0;right:0;top:0;height:180px;background:{NAVYT};'></div>"
    hook = (f"<div style=\"position:absolute;left:58px;top:232px;width:850px;font-family:Inter;font-weight:950;"
            f"font-size:66px;line-height:1.0;letter-spacing:-2px;color:{NAVYT};\">{idea['hook']}</div>")
    grid = ""
    for i, option in enumerate(options):
        x = 58 + i * 328
        grid += (f"<div style='position:absolute;left:{x}px;top:520px;width:292px;height:230px;border-radius:20px;background:#fff;"
                 f"box-shadow:0 18px 44px rgba(21,39,67,.14);padding:24px;border-top:12px solid {[AMBER,GREEN,CORAL][i]};'>"
                 f"<div style=\"font-family:Inter;font-weight:950;font-size:58px;color:{[AMBER,GREEN,CORAL][i]};\">{chr(65+i)}</div>"
                 f"<div style=\"font-family:Inter;font-weight:950;font-size:31px;line-height:1.08;color:{NAVYT};\">{option}</div></div>")
    takeaway = (f"<div style=\"position:absolute;left:62px;bottom:158px;width:750px;font-family:'DM Sans';font-weight:800;"
                f"font-size:28px;line-height:1.25;color:#53627A;\">{idea.get('takeaway','')}</div>")
    return bg + header + L.logo_tl() + hook + grid + takeaway + _footer(idea.get("cta", "internwise.co.uk"))


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
    return bg + rings + L.logo_tl() + label + hook + board + cta


WORLDS = {
    "decision": w_decision_prompt,
    "proofboard": w_proofboard,
    "debate": w_debate,
    "scorecard": w_scorecard,
    "signal": w_signal,
}


def render_conversation(idea, world, out_dir, filename="slide_1.png"):
    return L.render(out_dir, filename, WORLDS[world](idea))


if __name__ == "__main__":
    ideas = L.load("conversation_ideas.json")["ideas"]
    for idea in ideas[:1]:
        render_conversation(idea, "decision", os.path.join(L.OUTROOT, "week18", "_conversation_test"))
