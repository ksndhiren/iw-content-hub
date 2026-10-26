"""Nuno cutout pipeline: FSRCNN x4 super-res -> rembg -> tonal (Shadows -30) -> DOWNSCALE to target
-> unsharp -> edge clean. x4-then-downscale gives crisp real detail; ~0.7s SR/image (fast enough to batch)."""
import os, sys, glob, re, numpy as np, cv2
from rembg import remove
from PIL import Image, ImageFilter
_sr=None
def _get():
    global _sr
    if _sr is None:
        _sr=cv2.dnn_superres.DnnSuperResImpl_create(); _sr.readModel(os.path.join(os.path.dirname(__file__),"..","models","FSRCNN_x4.pb")); _sr.setModel("fsrcnn",4)
    return _sr
def cutout(src,dst,shadows=-0.30,highlights=0.0,target_h=1700):
    bgr=_get().upsample(cv2.imread(src))
    pil=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)).convert("RGBA")
    im=remove(pil); im=im.crop(im.getbbox())
    a=np.asarray(im).astype(np.float32); rgb=a[...,:3]/255.0; al=a[...,3:4]
    lum=0.299*rgb[...,0:1]+0.587*rgb[...,1:2]+0.114*rgb[...,2:3]; sm=np.clip(1-lum/0.5,0,1)**1.4
    rgb=rgb-abs(shadows)*sm*rgb if shadows<0 else rgb+shadows*sm*(1-rgb)
    if highlights>0:
        hm=np.clip((lum-0.5)/0.5,0,1)**1.4; rgb=rgb-highlights*hm*rgb
    rgb=np.clip(rgb,0,1)*255
    img=Image.fromarray(np.concatenate([rgb,al],-1).astype(np.uint8))
    w,h=img.size; img=img.resize((round(w*target_h/h),target_h),Image.LANCZOS)
    r,g,b,aa=img.split(); rgbimg=Image.merge("RGB",(r,g,b)).filter(ImageFilter.UnsharpMask(radius=2,percent=110,threshold=2))
    aa=aa.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    Image.merge("RGBA",(*rgbimg.split(),aa)).save(dst); print("ok",os.path.basename(dst),img.size,flush=True)
# Sources live under "Nuno Pictures/Generations/<group>/<category>/*.jpeg". Two
# earlier gotchas are fixed here: the tree gained a "Generations" level (the old
# base path no longer existed), and the walk only descended into <category>
# dirs, so generations sitting LOOSE in a group folder were invisible forever -
# that is how three usable Solo poses sat unused for months. Loose files are now
# picked up as nuno_<group>_<i>. Run with --audit to list what is on disk vs
# what each source maps to WITHOUT cutting anything.
if __name__=="__main__":
    H=os.path.expanduser; base=H("~/Downloads/Nuno Pictures/Generations")
    # heroes used by D1 (explicit names)
    # Explicit names override the positional nuno_<tag>_<i> scheme, for heroes and
    # for loose generations that deserve a semantic family rather than "solo_N".
    jobs={"nuno_cv.png":"Situational/CV/Gemini_Generated_Image_dsla2pdsla2pdsla.jpeg",
          "nuno_thumbsup.png":"Solo/Do This/Gemini_Generated_Image_htumc0htumc0htum.jpeg",
          # The four loose Solo/ files are NOT new material: each is the same
          # photograph as a cutout already in the library (verified identical by
          # nuno_identity). Named here so the walk claims them and --audit stops
          # reporting them as an outstanding gap.
          "nuno_dothis_5.png":"Solo/Gemini_Generated_Image_aj4n5gaj4n5gaj4n.jpeg",  # == dothis_4
          "nuno_cv_6.png":"Solo/Gemini_Generated_Image_ecbt9xecbt9xecbt.jpeg",      # == offers_cover
          "nuno_howto_4.png":"Solo/Gemini_Generated_Image_kaph5akaph5akaph.jpeg",   # == utility_4
          "nuno_cv_9.png":"Solo/Gemini_Generated_Image_smtbasmtbasmtbas.jpeg"}      # glass "Portfolio" panel
    # Held back on purpose - rembg leaves translucent artefacts or the wardrobe is
    # off-brand. Listed so --audit stops reporting them as an outstanding gap.
    SKIP={"nuno_cv_7.png",    # white sheet goes see-through; beige suit, not the navy blazer
          "nuno_cv_9.png"}    # glass panel ghosts the background on dark worlds
    # whole library (Solo + Situational). "Full Scene" is deliberately excluded:
    # those are landscape two-person environment shots, not cutout material.
    def _imgs(d):
        return sorted(glob.glob(d+"/*.jpeg")+glob.glob(d+"/*.jpg"))
    # A source already named explicitly above must not also be claimed by the
    # positional walk, or it gets cut twice under two names (nuno_dothis_6 AND
    # nuno_solo_1). setdefault only guards the NAME, so guard the SOURCE too.
    claimed=set(jobs.values())
    for g in ["Solo","Situational"]:
        gdir=os.path.join(base,g)
        for cat in sorted(os.listdir(gdir)):
            cdir=os.path.join(gdir,cat)
            if not os.path.isdir(cdir): continue
            tag=re.sub(r'[^a-z0-9]+','',cat.lower())
            for i,f in enumerate(_imgs(cdir),1):
                rel=os.path.relpath(f,base)
                if rel not in claimed:
                    jobs.setdefault(f"nuno_{tag}_{i}.png",rel)
        # loose generations directly inside the group folder - previously skipped
        for i,f in enumerate(_imgs(gdir),1):
            rel=os.path.relpath(f,base)
            if rel not in claimed:
                jobs.setdefault(f"nuno_{g.lower()}_{i}.png",rel)

    have={os.path.splitext(n)[0] for n in os.listdir("assets/nuno")}
    todo={n:r for n,r in jobs.items() if os.path.splitext(n)[0] not in have and n not in SKIP}
    if "--audit" in sys.argv:
        for name,rel in sorted(jobs.items()):
            tag="MISSING " if name in todo else ("skipped " if name in SKIP else "present ")
            print(tag+name,"<-",rel)
        print(f"AUDIT {len(jobs)} sources, {len(todo)} not yet cut",flush=True); raise SystemExit
    # only cut what is missing, so a re-run is cheap and never clobbers a cutout
    # that was hand-reviewed or deliberately dropped (e.g. nuno_cv_7, whose white
    # sheet rembg eats through).
    for name,rel in todo.items():
        cutout(os.path.join(base,rel),"assets/nuno/"+name)
    print("LIBRARY DONE",len(todo),"new of",len(jobs),"sources",flush=True)
