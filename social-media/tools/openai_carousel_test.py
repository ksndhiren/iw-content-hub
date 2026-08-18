"""TEST: full creative control to OpenAI (gpt-image-2) for a 4-slide carousel.
We only supply Nuno's reference photo; OpenAI designs everything else.
Key + model read from the Downloads docx at runtime - never printed or stored."""
import os, re, base64, sys, traceback
from docx import Document
from openai import OpenAI
sec=os.path.expanduser("~/Downloads/Secrets-Open AI.docx")
txt="\n".join(x.text for x in Document(sec).paragraphs)
KEY=re.findall(r'sk-[A-Za-z0-9_\-]{20,}',txt)[0]
MODEL=(re.findall(r'gpt-image[\w.\-]*',txt,re.I) or ["gpt-image-1"])[0]
client=OpenAI(api_key=KEY)
H=os.path.expanduser
STYLE=(" Design a cohesive premium Instagram carousel slide (1:1) for 'Internwise', a UK internship and "
       "graduate-jobs brand. Deep navy background with amber accents, bold modern typography, part of a matching set. "
       "Feature the man in the reference photo and keep his exact face and likeness. Spell all text correctly. Sharp, professional.")
SLIDES=[
 ("Solo/CV would be ideal","Situational/CV/Gemini_Generated_Image_dsla2pdsla2pdsla.jpeg",
  "Hook slide. Big headline: 'A recruiter reads your CV in 7 seconds.' He is reviewing a CV."+STYLE),
 ("howto","Solo/How to/Gemini_Generated_Image_n1of1yn1of1yn1of.jpeg",
  "Tip slide titled 'Win the top third' - recruiters scan the top first: name, target role, key skills. He is explaining."+STYLE),
 ("howto2","Solo/How to/Gemini_Generated_Image_r33uydr33uydr33u.jpeg",
  "Tip slide: 'Show impact, not duties' - e.g. 'Grew Instagram 3x in 4 months' beats 'Responsible for socials'."+STYLE),
 ("cta","Solo/Do This/Gemini_Generated_Image_htumc0htumc0htum.jpeg",
  "Call-to-action slide: 'Find your internship at internwise.co.uk'. He is giving a thumbs up, upbeat."+STYLE),
]
out="campaigns/outputs/openai_test"; os.makedirs(out,exist_ok=True)
print(f"model={MODEL}; generating {len(SLIDES)} slides (spends OpenAI credits)...")
for i,(_,ref,prompt) in enumerate(SLIDES,1):
    try:
        r=client.images.edit(model=MODEL,image=[open(H("~/Downloads/Nuno Pictures/"+ref),"rb")],
                             prompt=prompt,size="1024x1024")
        open(f"{out}/slide_{i}.png","wb").write(base64.b64decode(r.data[0].b64_json))
        print(f"  ok slide_{i}")
    except Exception as e:
        print(f"  FAIL slide_{i}: {type(e).__name__}: {str(e)[:200]}")
print("done")
