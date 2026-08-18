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
if __name__=="__main__":
    H=os.path.expanduser; base=H("~/Downloads/Nuno Pictures")
    # heroes used by D1 (explicit names)
    jobs={"nuno_cv.png":"Situational/CV/Gemini_Generated_Image_dsla2pdsla2pdsla.jpeg",
          "nuno_thumbsup.png":"Solo/Do This/Gemini_Generated_Image_htumc0htumc0htum.jpeg"}
    # whole library (Solo + Situational)
    for g in ["Solo","Situational"]:
        for cat in sorted(os.listdir(os.path.join(base,g))):
            cdir=os.path.join(base,g,cat)
            if not os.path.isdir(cdir): continue
            tag=re.sub(r'[^a-z0-9]+','',cat.lower())
            for i,f in enumerate(sorted(glob.glob(cdir+"/*.jpeg")+glob.glob(cdir+"/*.jpg")),1):
                jobs.setdefault(f"nuno_{tag}_{i}.png",os.path.relpath(f,base))
    for name,rel in jobs.items():
        cutout(os.path.join(base,rel),"assets/nuno/"+name)
    print("LIBRARY DONE",len(jobs),flush=True)
