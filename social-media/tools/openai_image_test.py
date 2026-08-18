"""One-off test: let OpenAI's image model generate a full Internwise slide (full control).
Key is read from a local gitignored file or env - never hardcoded.
Usage: python3 tools/openai_image_test.py
"""
import os, base64, sys
KEY = (os.environ.get("OPENAI_API_KEY")
       or (open(os.path.expanduser("~/.config/iw/openai_key.txt")).read().strip()
           if os.path.exists(os.path.expanduser("~/.config/iw/openai_key.txt")) else None))
if not KEY:
    sys.exit("No key. Put it in ~/.config/iw/openai_key.txt (one line) or export OPENAI_API_KEY.")
MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")  # set to the 2.0 id if different
from openai import OpenAI
client = OpenAI(api_key=KEY)
REF = os.path.expanduser("~/Downloads/Nuno Pictures/Solo/Do This/Gemini_Generated_Image_htumc0htumc0htum.jpeg")
PROMPT = ("A polished 1:1 social media graphic for a UK internship brand 'Internwise'. "
          "Deep navy background with a faint grid. Left side, bold white headline: "
          "'A recruiter reads your CV in 7 seconds' with '7 seconds' in amber. "
          "Right side: this same man (keep his exact face), waist-up, natural studio look, "
          "compositing cleanly into the scene. A small amber 'Find your internship' button. "
          "Clean, modern, professional, sharp. Leave the man's likeness identical to the reference.")
out = "campaigns/outputs/openai_test"; os.makedirs(out, exist_ok=True)
print(f"Model: {MODEL} - generating (this spends your OpenAI credits)...")
r = client.images.edit(model=MODEL, image=[open(REF, "rb")], prompt=PROMPT, size="1024x1024")
img = base64.b64decode(r.data[0].b64_json)
p = os.path.join(out, "openai_cv_test.png"); open(p, "wb").write(img)
print("saved", p)
