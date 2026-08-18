"""Week 11 (w/c 10 Aug) - 3 carousels + 2 singles, data-driven. Photo-free, lean."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wk11_base as b
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "campaigns", "outputs", "week11")

def save(post, slides, bgs):
    d = os.path.join(OUT, post); os.makedirs(d, exist_ok=True)
    for i,(body,bg) in enumerate(zip(slides,bgs),1):
        b.render(body, os.path.join(d, f"slide_{i}.png"), bg)

def carousel(post, d, hook, stats, tips, cta):
    slides=[]; bgs=[]
    for bg,body in [b.hook(d,*hook), b.stats(d,*stats)] + [b.tip(d,i+1,*t) for i,t in enumerate(tips)] + [b.cta(d,*cta)]:
        bgs.append(bg); slides.append(body)
    save(post, slides, bgs)

# ============ POST 1 - Assessment Centre (dark control room) ============
d1=dict(dark=True,bg="radial-gradient(ellipse at 50% 0%,#1b2b45 0%,#0d1526 70%)",acc=b.LIME,on=b.INK,
        txt="#EDF2F8",sub="#93A2B4",kick="Interviews / assessment day",card="#16202f")
carousel("d1-assessment", d1,
  ("Interviews / assessment day", "The assessment<br>centre is where<br>offers are <span style='color:%s;'>won.</span>"%b.LIME,
   "Most candidates over-prepare the interview and wing the AC. That is backwards - flip it."),
  ("Where the offer is really decided.",
   [("2-3","of ~8 finalists get an offer. The AC is the real cut."),("60%","of the score is how you work with others, not raw answers."),("1 day","that outweighs every round before it.")],
   "Sources: ISE, Prospects 2026"),
  [("Own the group exercise",["Contribute early, and pull quieter people in too.","Assessors score collaboration, not domination.","Watch the clock and steer the group to a decision."]),
   ("Nail the in-tray or case",["Prioritise ruthlessly and say your reasoning out loud.","It is fine not to finish - show a clear method.","Flag your assumptions instead of guessing silently."]),
   ("You are assessed at lunch too",["The informal chats count toward the score.","Be genuinely curious about the team and role.","Consistency all day beats one big moment."])],
  ("Walk in ready for<br>the <span style='color:%s;'>whole day.</span>"%b.LIME,["Group: contribute and include","Case: method over finishing","A question ready for everyone","Same energy at lunch"]))

# ============ POST 2 - Follow-up email (light professional) ============
d2=dict(dark=False,bg=b.CREAM,acc=b.DEEP,on="#ffffff",txt="#1a2b40",sub="#5b7089",kick="After you apply",card="#ffffff")
carousel("d2-followup", d2,
  ("After you apply", f"Only <span style='color:{b.DEEP};'>4%</span> send<br>a follow-up email.",
   "The ones who do stand out instantly. Here is the message that gets a reply, not a left-on-read."),
  ("A tiny effort, a big edge.",
   [("4%","of applicants ever follow up. Be one of them."),("27%","reply rate on a short, researched message."),("48h","the window to follow up while you are fresh.")],
   "Sources: LinkedIn, Jobvite 2026"),
  [("Time it right",["Send 24 to 48 hours after the interview or close.","Reply in the same thread if there is one.","One follow-up is plenty - do not chase weekly."]),
   ("Keep it three sentences",["Thank them and name one thing you discussed.","Restate the single reason you are a strong fit.","Ask about next steps and the timeline."]),
   ("Make it about them",["Reference something real - a project, a value.","Skip the generic 'just checking in'.","Proofread once - a typo undoes the effort."])],
  (f"Send the email the<br>other <span style='color:{b.DEEP};'>96%</span> won't.",["24 to 48 hours after","Three sentences","One specific detail","Ask about next steps"]))

# ============ POST 3 - 2026 grad market (bold editorial) ============
d3=dict(dark=True,bg=b.INK,acc=b.CORAL,on="#ffffff",txt=b.CREAM,sub="#b3aca0",kick="UK grad market / 2026",card="#20242e")
carousel("d3-market", d3,
  ("UK grad market / 2026", "The 2026 grad<br>market is <span style='color:%s;'>brutal.</span>"%b.CORAL,
   "Record applicants, fewer openings, silent inboxes. It is not you - but here is how to beat the odds anyway."),
  ("Why it feels impossible right now.",
   [("140+","applications per graduate role, on average."),("1 in 3","employers cut graduate intake this year."),("70%","of schemes close before Christmas.")],
   "Source: ISE Student Recruitment Survey 2026"),
  [("Play the volume game smarter",["Fewer, tailored applications beat 100 copy-pastes.","Apply the week a scheme opens - slots fill fast.","Track everything in one sheet so nothing slips."]),
   ("Go where the crowd isn't",["SMEs and startups hire year-round, less competition.","Referrals and speculative routes skip the queue.","A warm intro beats a cold portal every time."]),
   ("Make yourself un-ghostable",["Follow up - only 4% of applicants do.","Turn every rejection into one concrete fix.","Build public proof of skill so you are findable."])],
  ("The market is hard.<br>You can still <span style='color:%s;'>win.</span>"%b.CORAL,["Tailor, don't spray","Apply early","Chase the hidden market","Follow up and improve"]))

# ============ POST 4 - Decode the job ad (SINGLE) ============
def single_decode():
    d=dict(dark=True,acc=b.AMBER,on=b.INK); bg="linear-gradient(160deg,#264D7E 0%,#162d4a 100%)"
    rows=[("'2+ years experience'","We would like it, not need it. Apply anyway."),
          ("'Fast-paced environment'","Be ready to juggle and self-manage."),
          ("'Wear many hats'","Small team - you will learn a lot, fast."),
          ("'Competitive salary'","Ask the number. They expect you to.")]
    r=""
    for a,m in rows:
        r+=(f"<div style='display:flex;align-items:center;gap:20px;margin-bottom:20px;'>"
            f"<div style=\"flex:0 0 340px;font-family:'DM Sans';font-weight:700;font-size:25px;color:{b.AMBER};\">{a}</div>"
            f"<div style='color:rgba(255,255,255,.4);font-size:26px;'>&rarr;</div>"
            f"<div style=\"flex:1;font-family:'DM Sans';font-weight:500;font-size:25px;color:#EDF2F8;line-height:1.3;\">{m}</div></div>")
    title=b.head("What the job ad says<br>vs what it <span style='color:%s;'>means.</span>"%b.AMBER,56,"#fff")
    body=(b.hdr(d,"Decode the ad")+
        f"<div style='margin-top:34px;'>{title}</div>"
        f"<div style='flex:1;display:flex;flex-direction:column;justify-content:center;'>{r}</div>"
        f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:24px;color:{b.AMBER};\">Recruiters write a wishlist. You still apply. &nbsp;internwise.co.uk</div>")
    save("d4-decode",[body],[bg])

# ============ POST 5 - Negotiation stat (SINGLE) ============
def single_negotiate():
    d=dict(dark=True,acc=b.LIME,on=b.INK); bg="radial-gradient(ellipse at 30% 20%,#5B3FC4 0%,#2B1E63 75%)"
    steps=["Say thank you, then ask - politely.","Name a number backed by quick research.","Then stop talking. Let them respond."]
    st=""
    for i,s in enumerate(steps,1):
        st+=(f"<div style='display:flex;gap:14px;align-items:center;margin-bottom:12px;'>"
             f"<span style=\"color:{b.LIME};font-family:Inter;font-weight:700;font-size:24px;\">{i}</span>"
             f"<span style=\"font-family:'DM Sans';font-weight:500;font-size:26px;color:#EDEAF9;\">{s}</span></div>")
    body=(b.hdr(d,"Get paid")+
        f"<div style='flex:1;display:flex;flex-direction:column;justify-content:center;'>"
        f"<div style=\"font-family:Inter;font-weight:700;font-size:200px;color:{b.LIME};letter-spacing:-8px;line-height:0.9;\">58%</div>"
        f"<div style=\"font-family:Inter;font-weight:700;font-size:44px;color:#fff;letter-spacing:-1px;margin-top:10px;max-width:840px;line-height:1.05;\">of grads accept the first offer without asking for more.</div>"
        f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:26px;color:#C9BEEF;margin-top:20px;margin-bottom:28px;\">One polite sentence can be worth thousands over a career.</div>{st}"
        f"</div>"
        f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:24px;color:{b.LIME};\">internwise.co.uk</div>")
    save("d5-negotiate",[body],[bg])

single_decode(); single_negotiate()
print("DONE week 11")
