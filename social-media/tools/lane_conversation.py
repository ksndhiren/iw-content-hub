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


def _logo_dark():
    return f"<img src='{L.DARKLOGO}' style='position:absolute;left:56px;top:44px;height:{L.LOGO}px;'>"


def _footer(text="internwise.co.uk"):
    return (f"<div style='position:absolute;left:56px;bottom:46px;display:flex;align-items:center;gap:13px;'>"
            f"<div style='width:34px;height:34px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;'>"
            f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{DEEP}' stroke-width='2.6' "
            f"stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:22px;color:{NAVYT};letter-spacing:.3px;\">{text}</span></div>")


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


WORLDS = {"decision": w_decision_prompt}


def render_conversation(idea, world, out_dir, filename="slide_1.png"):
    return L.render(out_dir, filename, WORLDS[world](idea))


if __name__ == "__main__":
    ideas = L.load("conversation_ideas.json")["ideas"]
    for idea in ideas[:1]:
        render_conversation(idea, "decision", os.path.join(L.OUTROOT, "week18", "_conversation_test"))
